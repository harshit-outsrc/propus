configuration_read_endpoints = {
    "billing_method": "/ds/campusnexus/BillingMethods?$filter=Id eq 1",
    "catalog_year": (
        "/ds/campusnexus/ProgramVersions/CampusNexus.GetAreaOfStudyCatalogList"
        + "(programVersionId=<program_version_id>)?&$format=json&$count=true&$filter=IsMapped eq true "
        + "and IsActive eq true or(Id eq <program_version_id> and IsActive eq false)&$orderby=Name",
        ["<program_version_id>"],
    ),
    "ethnicity": "/ds/odata/Ethnicities?$filter=IsActive%20eq%20true&$select=Id,Name",
    "gender": "/ds/odata/Genders?$filter=IsActive%20eq%20true&$select=Id,Name",
    "grade_level": "/ds/campusnexus/GradeLevels?&$format=json&$count=true&$filter=IsActive eq true&$orderby=Name",
    "program_version": (
        "/ds/campusnexus/ProgramVersions/CampusNexus.GetEnrollmentProgramVersions"
        + "(campusId=<campus_id>)?&$format=json&$count=true&$filter=ProgramId eq <program_id> "
        + "and IsActive eq true and IsDegreeProgram eq false or (Id eq 0)&$orderby=Name",
        ["<campus_id>", "<program_id>"],
    ),
    "program": (
        "/ds/campusnexus/Programs/CampusNexus.GetEnrollmentProgramList(campusId=<campus_id>"
        + ",degreeProgram=0)?&$format=json&$filter=IsActive eq true or (Id eq 0)&$orderby=Name",
        ["<campus_id>"],
    ),
    "pronoun": "/ds/odata/GenderPronouns?$filter=IsActive eq true&$select=Id,Name",
    "school_status": "/ds/odata/SchoolStatuses?$filter=IsActive eq true&$select=Id,Name",
    "shift": (
        "/ds/campusnexus/Shifts?$select=Id,Code,Name,IsActive&$format=json&$count=true"
        + "&$filter=CampusGroup/CampusList/any(cl:cl/CampusId eq <campus_id>) and IsActive eq true&$orderby=Name",
        ["<campus_id>"],
    ),
    "start_date": (
        "/ds/campusnexus/SchoolStartDates/CampusNexus.GetEnrollmentSchoolStartDates"
        + "(campusId=<campus_id>,programVersionId=<program_version_id>)?&$format=json&$count=true"
        + "&$filter=IsActive eq true&$orderby=StartDate desc",
        ["<campus_id>", "<program_version_id>"],
    ),
    "suffix": "/ds/odata/Suffixes?$filter=IsActive eq true&$select=Id,Code",
    "term": "/ds/odata/Terms?$orderby=StartDate&$select=Code,StartDate,EndDate,AddDropDate,Id",
    "title": "/ds/odata/Titles?$filter=IsActive eq true&$select=Id,Name",
}

configuration_create_endpoints = {
    "create_term": "/api/commands/Academics/Term/SaveNew",
    "create_start_date": "/api/commands/Academics/ShiftSchoolStartDate/SaveNew",
    "save_school_start_date": "/api/commands/Academics/ShiftSchoolStartDate/SaveSchoolStartDate",
}

configuration_copy_endpoints = {"copy_class_schedule": "/api/commands/Academics/ClassSection/CopyClassSchedule"}
