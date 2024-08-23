"""
This script is used to seed the database with assignment data from the Canvas API.
- It will create assessments in the assessment table for each assignment in the course.
- It pulls the competency information for each assignment based on the module that the assignment is found in.
- If run multiple times, it will update the existing assessments in the database with the new data.

"""

import asyncio
import csv
import os

from dataclasses import dataclass
from sqlalchemy import select, and_
from sqlalchemy.orm import make_transient
from typing import Union

from propus.aws.ssm import AWS_SSM
from propus.calbright_sql.calbright import Calbright
from propus.canvas import Canvas
from propus.calbright_sql.assessment import Assessment, AssessmentType, LmsType
from propus.calbright_sql.competency import Competency, CompetencyType
from propus.calbright_sql.course_version import CourseVersion
from propus.calbright_sql.enrollment import LMS

from propus.helpers.sql_alchemy import update_or_create

ssm = AWS_SSM.build("us-west-2")
creds = ssm.get_param("canvas.dev.token", param_type="json")
canvas = Canvas(base_url=creds["base_url"], application_key=creds["token"], auth_providers=creds["auth_providers"])

calbright_postgres = Calbright.build(
    {
        "db": os.environ.get("DB"),
        "host": "localhost",
        "user": os.environ.get("USER"),
        "password": os.environ.get("PASSWORD"),
    },
    verbose=False,
).session


@dataclass
class CourseData:
    canvas_id: int
    last_summative_assignment_id: int
    required_percentage_to_pass_summative: float
    final_grade_competency_name: str
    observable_skills_competency_name: str


# This COURSES variable is a list of dictionaries, each dictionary representing a course that we want to ingest into
# the database. The keys in the dictionary are the fields of the CourseData dataclass.

COURSES = [
    {
        "canvas_id": 115,
        "last_summative_assignment_id": 258,
        "required_percentage_to_pass_summative": 0.8,
        "final_grade_competency_name": "BUS500 - Data Analysis_Final Grade",
        "observable_skills_competency_name": "BUS500 - Data Analysis_Observable Skills",
    },
    {
        "canvas_id": 116,
        "last_summative_assignment_id": 325,
        "required_percentage_to_pass_summative": 0.8,
        "final_grade_competency_name": "BUS501 - Data Analysis_Final Grade",
        "observable_skills_competency_name": "BUS501 - Data Analysis_Observable Skills",
    },
]


def upsert_assessment(session, assessment_object: Assessment):
    """
    Upsert an assignment into the database.
    - If the assignment already exists in the database, it will update the existing record.
    - If the assignment does not exist in the database, it will create a new record.

    Note: You must commit the session after calling this function to persist the changes to the database!

    :param assessment_object: The assignment object to upsert into the database
    :return: None
    """
    try:
        instance = (
            session.execute(
                select(Assessment)
                .filter(
                    and_(
                        Assessment.lms_id == str(assessment_object.lms_id),
                        Assessment.lms == LMS("Canvas"),
                        Assessment.lms_type == assessment_object.lms_type,
                    )
                )
                .with_for_update(key_share=True)
            )
            .scalars()
            .one_or_none()
        )
        if instance:
            print(f'Found existing assessment "{instance.name}"')
            # Update the existing instance with new data
            instance.competency_assessment = assessment_object.competency_assessment
            instance.name = assessment_object.name
            instance.assessment_type = assessment_object.assessment_type
            instance.lms = assessment_object.lms
            instance.lms_type = assessment_object.lms_type
            # Set the state of the assessment_object to transient so that it doesn't get committed to the database,
            #   we only want to update the existing instance
            make_transient(assessment_object)
            print(f"Updated Assessment with lms_id={assessment_object.lms_id}")
        else:
            # Create a new instance if it doesn't exist
            print(f"Creating new Assessment with lms_id={assessment_object.lms_id}")
            session.add(assessment_object)
    except Exception as e:
        print(f"Failed to upsert Assessment with lms_id={assessment_object.lms_id}: {e}")
        raise


assessment_group_name_mapping = {
    "Assignments": None,
    "Pre-Assessments": AssessmentType("Pre-Assessment"),
    "Formative Assessments": AssessmentType("Formative"),
    "Formative Challenges": AssessmentType("Formative"),
    "Observable Skills": AssessmentType("Observable Skill"),
    "Milestones": AssessmentType("Milestone"),
    "Summative Assessments": AssessmentType("Summative"),
    "Survey": None,
    "Final Status": AssessmentType("Final Grade"),
    "Discussions": AssessmentType("Discussion"),
    "Final Assessment": AssessmentType("Final Grade"),
    "Course Survey": None,
}


def get_first_result(results):
    """
    Returns the first result from a query, or None if no results are found. Helper function.
    :param results: A list of results from a query
    :return: The first result from the query, or None if no results are found
    """
    return results[0] if results else None


def get_course_competencies_from_db(course_id, name: Union[str, None] = None):
    """
    Get the competencies for a course from the database.
    - The competencies are located through their association with the course version.
    :param course_id: The course lms_id
    :param name: Optional - a string to filter the competencies by. This is useful to fetch a specific competency.
    :return: A list of competencies for the course, either all or filtered by name
    """
    course_competencies = calbright_postgres.execute(
        select(Competency)
        .join(CourseVersion)
        .filter(CourseVersion.lms_id == str(course_id), Competency.is_active.is_(True), Competency.lms == "canvas")
    ).all()

    if name:
        return [c[0] for c in course_competencies if name.lower() in c[0].competency_name.lower()]
    return [c[0] for c in course_competencies]


def get_course_module_data(course_id):
    """
    Get the module data for a course from the Canvas API.
    - This is needed because the location of an assignment within a module is how we know which competency to associate
        with the assignment. There is otherwise no direct association between an assignment and a competency in Canvas.
    - This data is later combined with the assignment data to create the assessments in the database.

    :param course_id: The course lms_id
    :return: A dictionary of the course module data, grouped by type (assignment / quiz / discussion)
        Within each type - there is a dictionary of the module item data, keyed by the item id.
    """
    # Get the course competencies from the database
    competencies = get_course_competencies_from_db(course_id)

    # Get the course modules from the Canvas API - including the items in the modules (with their IDs / type)
    course_modules = asyncio.run(
        canvas.get_course_modules(
            course_id=course_id,
            include="items",
        )
    )
    course_module_data = []

    # Go through each module and its items, filtering to only include the items that are
    #   assignments, quizzes, or discussions
    for module in course_modules:
        print(f'processing module "{module["name"]}"')
        module_data = {"module_name": module["name"], "items": []}

        # Filter the modules to only include the ones that have competencies associated with them
        # This will exclude modules for things like "Orientation", "Mid-Course Survey", etc...
        filtered_competencies = [
            competency for competency in competencies if module["name"].lower() in competency.competency_name.lower()
        ]
        if not filtered_competencies:
            print(f'no competencies found for module "{module["name"]}"')
            continue

        module_data["competency"] = filtered_competencies[0]
        for item in module.get("items", []):
            if item.get("type") not in {"Assignment", "Quiz", "Discussion"}:
                continue
            module_data["items"].append(
                {"id": item["content_id"], "name": item["title"], "type": LmsType(item["type"])}
            )

        if module_data.get("items"):
            course_module_data.append(module_data)

    # Prepare the course module data for use in the ingest_course_data function
    assignment_mapping = {"assignment": {}, "quiz": {}, "discussion": {}}
    for module in course_module_data:
        for item in module["items"]:
            assignment_mapping[item["type"].name][item["id"]] = {
                "competency": module["competency"],
                "name": item["name"],
                "type": item["type"],
            }
    # return course_module_data
    return assignment_mapping


def ingest_course_data(course_data: CourseData):
    """
    Ingest the course data into the database.
    - This function will create assessments in the database for each assignment in the course.
    - It will pull the competency information for each assignment based on the module that the assignment is found in.
    - It will also create assessments for any non-graded discussions that are found in the course.

    :param course_data: CourseData: The course information for which course to ingest
    :return: None
    """
    # Get the course module data from the Canvas API
    course_module_data = get_course_module_data(course_data.canvas_id)

    # Get the observable skills and final grade competencies for the course - these are used for the observable skills
    #   and final grade assessments.
    observable_skills_competency = get_first_result(
        get_course_competencies_from_db(course_data.canvas_id, name=course_data.observable_skills_competency_name)
    )
    final_grade_competency = get_first_result(
        get_course_competencies_from_db(course_data.canvas_id, name=course_data.final_grade_competency_name)
    )
    assessments = []

    # Fetch the assignment groups for the course - including the assignments and discussion topics
    assignment_groups = asyncio.run(
        canvas.get_course_assignment_groups(
            course_id=course_data.canvas_id, include=["assignments", "discussion_topic"]
        )
    )
    created_discussions = []

    # Go through all the assignment groups and prepares assessment objects for each assignment in them...
    for group in assignment_groups:
        # This determines the type of assessment that the group is, based on the mapping from the assignment group name
        assessment_type = assessment_group_name_mapping.get(group["name"])
        if not assessment_type:
            print(f'assessment group name "{group["name"]}" not found in mapping, skipping....')
            continue
        print(f'processing assessment group name "{group["name"]}"')
        if not group["assignments"]:
            print(f'no assignments found for assessment group name "{group["name"]}"')
            continue

        # Go through each assignment in the group and prepare the assessment object
        for assignment in group["assignments"]:
            # Check to see if the assignment has a graded discussion topic associated with it
            # If it does, we will create the assessment as an ASSIGNMENT instead of a DISCUSSION
            # But - we need to use the discussion ID to locate the competency from the module data...
            discussion_topic = assignment.get("discussion_topic")
            if discussion_topic:
                # TODO: So - when a student submits a GRADED discussion, it makes both an assignment submission AND
                #    a discussion submission. What I'm doing here is creating the assessment in the database as the
                #    ASSIGNMENT, and then we will update that assessment_submission record. The "discussion" LmsType in
                #    the database will be just for the non-graded discussions.
                module_info = course_module_data["discussion"].get(discussion_topic["id"])
                print(f'Preparing discussion assessment "{assignment["name"]}"')
                assessment_data = Assessment(
                    competency_assessment=module_info["competency"],
                    name=assignment["name"],
                    assessment_type=assessment_type,
                    lms="canvas",
                    lms_id=assignment["id"],  # Note we store the ASSIGNMENT ID, not the DISCUSSION ID
                    lms_type=LmsType("Assignment"),  # Note we store the ASSIGNMENT TYPE, not the DISCUSSION TYPE
                )
                created_discussions.append(discussion_topic["id"])
            else:
                # If this isn't a discussion, then we can just use the assignment ID to locate the competency from the
                #   module data...
                module_info = course_module_data["assignment"].get(assignment["id"])
                if not module_info:
                    # The observable skills and final grade assessments are not found in the modules area, so we need
                    #   to manually associate their competency with the respective one (observable_skills/final_grade)
                    #   and type (assignment)...
                    if assessment_type == AssessmentType("Observable Skill"):
                        module_info = {"competency": observable_skills_competency, "type": LmsType("Assignment")}
                    elif assessment_type == AssessmentType("Final Grade"):
                        module_info = {"competency": final_grade_competency, "type": LmsType("Assignment")}
                    else:
                        # TODO: Handle this - it would be if there is no COMPETENCY for the assignment because it's
                        #    not found in the modules area....
                        print(f'no module info found for assignment "{assignment["name"]}"')
                        continue

                competency = module_info["competency"]
                if assessment_type == AssessmentType("Observable Skill"):
                    competency = observable_skills_competency
                elif assessment_type == AssessmentType("Final Grade"):
                    competency = final_grade_competency
                print(f'Preparing assessment "{assignment["name"]}"')
                # Finally - prepare the assessment object and store it in a list to be created in the database
                assessment_data = Assessment(
                    competency_assessment=competency,
                    name=assignment["name"],
                    assessment_type=assessment_type,
                    lms="canvas",
                    lms_id=assignment["id"],
                    lms_type=module_info["type"],
                )
                if assessment_type in {AssessmentType("Summative"), AssessmentType("Pre-Assessment")}:
                    # If the assessment is a summative or pre-assessment, we set the required percentage to pass
                    # This is defined in the CourseData for the course
                    assessment_data.required_percentage_to_pass = course_data.required_percentage_to_pass_summative
                if (
                    assessment_type == AssessmentType("Summative")
                    and assignment["id"] == course_data.last_summative_assignment_id
                ):
                    # If the assessment is the last summative of the course, set the is_last_summative_of_course flag
                    # This is defined in the CourseData for the course
                    assessment_data.is_last_summative_of_course = True
            assessments.append(assessment_data)

    # Go through and create any non-graded discussions which have not yet been created
    # These discussions we fetched from the MODULES and aren't located in assignments (like graded discussions are)
    for discussion_id in course_module_data["discussion"]:
        if discussion_id not in created_discussions:
            module_info = course_module_data["discussion"][discussion_id]
            assessment_data = Assessment(
                competency_assessment=module_info["competency"],
                name=module_info["name"],
                assessment_type=AssessmentType("Discussion"),
                lms="canvas",
                lms_id=discussion_id,
                lms_type=module_info["type"],
            )
            assessments.append(assessment_data)

    # TODO: Need to go through and compare any assignments which exist in the database and set them to inactive
    #   also above, need to include active = true when instantiating the assessment objects

    # TODO: Maybe we should change the instantiation of the assessment objects to dicts to prevent any
    #   sort of database block on the objects
    for assessment in assessments:
        upsert_assessment(calbright_postgres, assessment)
    calbright_postgres.commit()


def fetch_comptency_data():
    """
    This function loads the competency data from the CSV file.
    The CSV file is expected to have the following columns:
        - course_lms_id: The LMS ID of the course in Canvas, e.g. 115
        - course_code: The course code, e.g. BUS500
        - competency_type: One of the following: Competency, Durable Skill, Final Grade, Observable Skill
        - competency_name: The name of the competency, e.g. BUS500 - Data Analysis_Final Grade
        - description: The description of the competency
    :return: A dictionary containing the competency data and the list of course_lms_ids
    """
    csv_file_path = "canvas_competencies.csv"
    competency_data = []
    course_lms_ids = []
    with open(csv_file_path, mode="r", newline="", encoding="utf-8-sig") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            competency_data.append(row)
            course_lms_ids.append(row["course_lms_id"])
    return {"competency_data": competency_data, "course_lms_ids": list(set(course_lms_ids))}


def ingest_canvas_competencies():
    """
    Ingest the competency data from the CSV file into the database.
    :return: None
    """
    competency_data = fetch_comptency_data()
    # Get the course_version from the database where the course_version.lms_id is in the list of course_lms_ids
    course_versions = calbright_postgres.execute(
        select(CourseVersion).filter(CourseVersion.lms_id.in_(competency_data["course_lms_ids"]))
    ).all()
    course_version_data = {cv[0].lms_id: cv[0].id for cv in course_versions}
    for competency in competency_data["competency_data"]:
        data = {
            "course_version_id": course_version_data.get(competency["course_lms_id"]),
            "competency_name": competency["competency_name"],
            "description": competency["description"],
            "lms": LMS("Canvas"),
            "competency_type": CompetencyType(competency["competency_type"]),
        }
        update_or_create(
            calbright_postgres,
            Competency,
            data,
            course_version_id=data["course_version_id"],
            competency_name=data["competency_name"],
        )

    calbright_postgres.commit()


def ingest_all_course_data():
    """
    Ingest all the course data into the database.
    - This function will ingest the competency data first, and then ingest the course data.
    :return: None
    """
    ingest_canvas_competencies()
    for course in COURSES:
        ingest_course_data(CourseData(**course))


ingest_all_course_data()
