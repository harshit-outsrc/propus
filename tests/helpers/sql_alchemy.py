import unittest
import uuid

from mock_alchemy.mocking import AlchemyMagicMock
from sqlalchemy.orm.exc import NoResultFound
from unittest.mock import patch, MagicMock

from propus.helpers.exceptions import InvalidKeyList
from propus.helpers.input_validations import validate_uuid
from propus.helpers.sql_alchemy import (
    build_query,
    create_field_map,
    create_field_map_many_to_many,
    get_or_create,
    get_validation_function_by_model_field,
    update_or_create,
    map_value_to_foreign_key,
    apply_mappings,
    upsert_changes,
)
from propus.calbright_sql.salutation import Salutation
from propus.calbright_sql.course import Course
from propus.calbright_sql.program_version_course import ProgramVersionCourse


class TestSqlAlchemyHelpers(unittest.TestCase):
    def setUp(self) -> None:
        # Test data
        self.fields = ["anthology_id", "created_at", "salutation"]
        self.query = "SELECT anthology_id, created_at, salutation FROM salutation"
        self.salutation = Salutation(salutation="Mx.")
        session = AlchemyMagicMock()
        session.add(self.salutation)
        self.session = session
        self.table = "salutation"
        self.dictionary = {"some_key": "some_value"}
        self.mappings = [
            {
                "old_key": "cfg_Learner_Status__c",
                "new_key": "learner_status_id",
                "model": self.table,
                "map_from": "status",
                "map_to": "id",
                "return_map": True,
            }
        ]
        self.mapping_data = [{"cfg_Learner_Status__c": "Expressed Interest"}]
        self.course1 = Course(
            course_name="Course1",
            status="Active",
            course_id=1,
            control_number="CN1",
            department_name="IT",
            department_number=500,
            course_classification_status="C",
            top_code="TC1",
            last_updated_by_college="2022-01-01",
            minimum_course_contact_hours=3.0,
            maximum_course_contact_hours=5.0,
            anthology_course_id=2,
        )

        self.course2 = Course(
            course_name="Course2",
            status="Inactive",
            course_id=2,
            control_number="CN2",
            department_name="WF",
            department_number=510,
            course_classification_status="I",
            top_code="TC2",
            last_updated_by_college="2022-01-02",
            minimum_course_contact_hours=2.0,
            maximum_course_contact_hours=4.0,
            anthology_course_id=3,
        )
        self.program_version_id = uuid.uuid4()
        self.course_version_id = uuid.uuid4()
        self.program_version_course = ProgramVersionCourse(
            program_version_id=self.program_version_id, course_version_id=self.course_version_id
        )
        self.courses = [self.course1, self.course2]

    def test_build_query(self):
        self.assertEqual(build_query(self.table, self.fields), self.query)

    def test_build_query_error_fields(self):
        with self.assertRaises(ValueError):
            build_query(self.table, None)

    def test_build_query_error_filters(self):
        with self.assertRaises(ValueError):
            build_query(self.table, self.fields, dict(foo="bar"))

    def test_build_query_error_table(self):
        with self.assertRaises(ValueError):
            build_query(None, self.fields)

    def test_create_field_map(self):
        self.session.scalars.return_value.all.return_value = [self.salutation]
        field_map = create_field_map(self.session, Salutation, map_from="salutation")

        for k, v in field_map.items():
            self.assertEqual(k, self.salutation.salutation)
            self.assertIsNone(v)

    def test_create_field_map_many_to_many_default_args(self):
        self.session.query.return_value.all.return_value = [self.salutation]
        field_map = create_field_map_many_to_many(self.session, Salutation, map_from=["salutation"])

        for k, v in field_map.items():
            self.assertEqual(k[0], (self.salutation.salutation))
            self.assertIsNone(v[0])

    def test_create_field_map_many_to_many_single_mapped_fields(self):
        with patch("propus.helpers.sql_alchemy.select", return_value=Course) as mock_select:
            self.session.scalars.return_value.all.return_value = [self.course1, self.course2]
            expected_field_map = {
                (getattr(self.course1, "course_name"),): [getattr(self.course1, "course_id")],
                (getattr(self.course2, "course_name"),): [getattr(self.course2, "course_id")],
            }
            field_map = create_field_map_many_to_many(self.session, Course, ["course_name"], ["course_id"])
            mock_select.assert_called_once_with(Course)
            self.assertEqual(field_map, expected_field_map)

    def test_create_field_map_many_to_many_with_multiple_mapped_fields(self):
        self.session.scalars.return_value.all.return_value = [self.course1, self.course2]
        field_map = create_field_map_many_to_many(
            self.session, Course, map_from=["course_name", "course_id"], map_to=["department_name", "department_number"]
        )
        expected_field_map = {
            (getattr(course, "course_name"), getattr(course, "course_id")): [
                getattr(course, "department_name"),
                getattr(course, "department_number"),
            ]
            for course in [self.course1, self.course2]
        }

        self.assertEqual(field_map, expected_field_map)

    def test_create_field_map_many_to_many_with_mapped_fields_and_key_list(self):
        self.session.execute.return_value.scalars.return_value.first.side_effect = [self.course1, self.course2]
        key_list = [(getattr(self.course1, "course_name"), getattr(self.course1, "course_id"))]

        field_map = create_field_map_many_to_many(
            self.session,
            Course,
            map_from=["course_name", "course_id"],
            map_to=["department_name", "department_number"],
            key_list=key_list,
        )

        expected_field_map = {
            (getattr(self.course1, "course_name"), getattr(self.course1, "course_id")): [
                getattr(self.course1, "department_name"),
                getattr(self.course1, "department_number"),
            ]
        }
        self.assertEqual(field_map, expected_field_map)

    @patch("propus.helpers.sql_alchemy.get_validation_function_by_model_field")
    def test_create_field_map_many_to_many_invalid_key_list(self, mock_get_validation_function):
        mock_get_validation_function.return_value = validate_uuid
        key_list = [(getattr(self.course1, "course_name"))]

        with self.assertRaises(InvalidKeyList):
            create_field_map_many_to_many(
                self.session, ProgramVersionCourse, ["program_version_id"], ["course_version_id"], key_list
            )

    @patch("propus.helpers.sql_alchemy.get_validation_function_by_model_field")
    def test_create_field_map_many_to_many_valid_key_list(self, mock_get_validation_function):
        self.session.execute.return_value.scalars.return_value.first.return_value = self.program_version_course
        mock_get_validation_function.return_value = validate_uuid
        key_list = [(str(self.program_version_id),)]

        field_map = create_field_map_many_to_many(
            self.session, ProgramVersionCourse, ["program_version_id"], ["course_version_id"], key_list
        )

        expected_field_map = {(str(self.program_version_id),): [self.course_version_id]}
        self.assertEqual(field_map, expected_field_map)

    def test_get_validation_function_by_model_field(self):
        for field in self.fields:
            f = get_validation_function_by_model_field(self.session, Salutation, field)
            self.assertIsNone(f)

    def test_get_or_create(self):
        defaults = dict(salutation="foo")
        self.session.execute.return_value.scalars.return_value.one.side_effect = NoResultFound
        _, created = get_or_create(self.session, Salutation, defaults=defaults)
        self.assertTrue(created)

    def test_update_or_create(self):
        defaults = dict(salutation="foo")
        self.session.query.with_for_update(key_share=True).filter_by.one.return_value = self.salutation
        _, created = update_or_create(self.session, Salutation, defaults=defaults)
        self.assertFalse(created)

    @patch("propus.helpers.sql_alchemy.select")
    def test_mapping_existing_value(self, mock_select):
        # Mock the query, filter, and first to return a UUID
        with patch.object(self.session, "execute") as mock_query:
            mock_query.return_value.scalars.return_value.first.return_value = ("mock_uuid",)
            result = map_value_to_foreign_key(
                self.session, self.dictionary, "some_key", "new_id_key", MagicMock(), "value"
            )
        # Check if mapping was successful
        self.assertIn("new_id_key", result)
        self.assertEqual(result["new_id_key"], "mock_uuid")

    def test_apply_mappings(self):
        resolve_mappings_mock = MagicMock(
            return_value=({"learner_status_id": "<UUID>"}, [], {"Expressed Interest": "1"})
        )
        with patch("propus.helpers.sql_alchemy.resolve_mappings", resolve_mappings_mock):
            result, failed_records, mapping_dict = apply_mappings(self.session, self.mapping_data, self.mappings)

        expected_result = resolve_mappings_mock(self.session, self.mapping_data, **self.mappings[0])
        self.assertEqual(result, expected_result[0])
        self.assertEqual(failed_records, expected_result[1])
        self.assertEqual(mapping_dict, {"learner_status_id": expected_result[2]})

    def test_upsert_changes(self):
        update_or_create_mock = MagicMock(return_value=(self.salutation, False))
        with patch("propus.helpers.sql_alchemy.update_or_create", update_or_create_mock):
            defaults = {"anthology_id": -1}
            kwargs = {"salutation": "Mx."}
            upserts, upserted = upsert_changes(self.session, Salutation, self.salutation, defaults, **kwargs)
            self.assertEqual(upserts, defaults)
            self.assertEqual(upserted, True)

    def test_no_upsert_changes(self):
        self.salutation.anthology_id = 5
        defaults = {"anthology_id": 5}
        kwargs = {"salutation": "Mx."}
        upserts, upserted = upsert_changes(self.session, Salutation, self.salutation, defaults, **kwargs)
        self.assertEqual(upserts, {})
        self.assertEqual(upserted, False)


if __name__ == "__main__":
    unittest.main()
