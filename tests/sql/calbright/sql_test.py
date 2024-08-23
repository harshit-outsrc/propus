import random
from sqlalchemy.exc import IntegrityError
import string
import unittest
from unittest.mock import MagicMock, Mock

from propus.calbright_sql.calbright import Calbright
from propus.calbright_sql.enrollment_status import EnrollmentStatus
from propus.calbright_sql.program_version_course import ProgramVersionCourse


class TestSqlCalbright(unittest.TestCase):
    def setUp(self):
        self.last_random = None
        self.required_attributes = ["__tablename__", "__repr__", "col_names", "to_dict"]
        self.all_models = Calbright.all_models
        # TODO: `EnrollmentStatus` and `ProgramVersionCourse`
        # have additional methods (i.e. fetch terms from anthology)
        # within them which would have to be mocked out
        skip_models = (EnrollmentStatus, ProgramVersionCourse)
        self.seed_tables = [m for m in self.all_models if "seed_data" in dir(m) and m not in skip_models]
        self.input_record = {
            "Name": self.get_random(),
            "Ethnicity": self.get_random(True),
            "Gender": self.get_random(True),
            "Id": self.get_random(),
            "anthology_id": self.get_random(True),
        }

        self.error = "Error: Catch this error"
        self.user_session_commit = False
        self.session_commit_called = False
        self.session_roll_back_called = False
        self.fetch_comp_called = False

    def get_random(self, return_last=False):
        if return_last:
            return self.last_random
        self.last_random = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        return self.last_random

    def test_all_models_have_necessary_items(self):
        for model in self.all_models:
            for attr in self.required_attributes:
                self.assertTrue(
                    hasattr(model, attr),
                    msg="{m} is missing attribute {a}".format(m=model, a=attr),
                )
            defined_columns = model.col_names()
            for column in defined_columns:
                self.assertTrue(
                    hasattr(model, column),
                    msg="{m} is missing defined column {c}".format(m=model, c=column),
                )
            extra_columns_in_to_dict = set(model.to_dict(model()).keys()) - set(defined_columns)
            self.assertTrue(
                len(extra_columns_in_to_dict) == 0,
                msg="{m} has additional columns in to_dict not present in columns: {c}".format(
                    m=model, c=extra_columns_in_to_dict
                ),
            )
            repr_string = model.__repr__(model())
            self.assertTrue(
                repr_string is not None and isinstance(repr_string, str) and "None" in repr_string,
                msg="{m} __repr__ class does not return a correct string",
            )

    async def receive_data(self, _):
        return {"value": [self.input_record]}

    def receive_competencies(self, **kwargs):
        if self.fetch_comp_called:
            return []
        self.fetch_comp_called = True
        return [
            {
                "id": "227",
                "state": "active",
                "description": "this is the description",
                "title": "This is the title",
            }
        ]

    def session_add(self, data):
        for key, value in data.to_dict().items():
            if value is None:
                continue
            if self.input_record.get(key):
                self.assertEqual(value, self.input_record.get(key))

    def session_commit(self):
        if self.user_session_commit:
            self.session_roll_back_called = True
        if self.session_commit_called is False or self.user_session_commit:
            self.session_commit_called = True
            return
        if self.session_roll_back_called is False:
            raise IntegrityError("error", "UniqueViolation constraint_failure", "error")
        raise Exception(self.error)

    def session_rollback(self):
        self.session_roll_back_called = True

    def test_seed_data_scripts(self):
        anth_mock = MagicMock()
        anth_mock.fetch_configurations = Mock(side_effect=self.receive_data)

        strut_mock = MagicMock()
        strut_mock.fetch_competencies = Mock(side_effect=self.receive_competencies)

        session_mock = MagicMock()
        session_mock.add = Mock(side_effect=self.session_add)
        session_mock.commit = Mock(side_effect=self.session_commit)
        session_mock.rollback = Mock(side_effect=self.session_rollback)

        for model in self.seed_tables:
            if not hasattr(model, "seed_data") or model.__tablename__ == "user":
                continue
            self.session_commit_called = False
            self.session_roll_back_called = False
            self.user_session_commit = True if model.__tablename__ == "user" else False

            model.seed_data(self=model, session=session_mock, anthology=anth_mock, strut=strut_mock)
            self.assertTrue(self.session_commit_called)
            model.seed_data(self=model, session=session_mock, anthology=anth_mock, strut=strut_mock)
            self.assertTrue(self.session_roll_back_called)
            try:
                model.seed_data(
                    self=model,
                    session=session_mock,
                    anthology=anth_mock,
                    strut=strut_mock,
                )
            except Exception as err:
                self.assertEqual(str(err), self.error)


if __name__ == "__main__":
    unittest.main()
