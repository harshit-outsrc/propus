import coverage
from pprint import pformat
import sys
import unittest

cov = coverage.Coverage()
cov.start()

from propus.logging_utility import Logging

from tests.anthology.certificate.create import TestAnthologyCertificateCreate
from tests.anthology.configuration.copy import TestAnthologyConfigurationCopy
from tests.anthology.configuration.create import TestAnthologyConfigurationCreate
from tests.anthology.configuration.read import TestAnthologyConfigurationRead
from tests.anthology.course.change import TestAnthologyCourseChange
from tests.anthology.course.drop import TestAnthologyCourseDrop
from tests.anthology.course.grade import TestAnthologCourseGrade
from tests.anthology.course.read import TestAnthologyCourseRead
from tests.anthology.course.register import TestAnthologyCourseRegister
from tests.anthology.course.reinstate import TestAnthologyCourseReinstate
from tests.anthology.course.unregister import TestAnthologyCourseUnregister
from tests.anthology.enrollment.create import TestAnthologyEnrollmentCreate
from tests.anthology.student.create import TestAnthologyStudentCreate
from tests.anthology.student.read import TestAnthologyStudentRead
from tests.anthology.student.update import TestAnthologyStudentUpdate

from tests.api_client import APIClientTests

from tests.aws.s3 import TestS3
from tests.aws.ssm import TestSSM
from tests.aws.sqs import TestSQS

from tests.calendly import TestCalendly

from tests.canvas.assignment.read import TestCanvasAssignmentRead
from tests.canvas.course.create import TestCanvasCourseCreate
from tests.canvas.course.delete import TestCanvasCourseDelete
from tests.canvas.course.read import TestCanvasCourseRead
from tests.canvas.course.update import TestCanvasCourseUpdate
from tests.canvas.enrollment.create import TestCanvasEnrollmentCreate
from tests.canvas.enrollment.delete import TestCanvasEnrollmentDelete
from tests.canvas.enrollment.read import TestCanvasEnrollmentRead
from tests.canvas.enrollment.update import TestCanvasEnrollmentUpdate
from tests.canvas.module.read import TestCanvasModuleRead
from tests.canvas.submission.read import TestCanvasSubmissionRead
from tests.canvas.term.create import TestCanvasTermCreate
from tests.canvas.term.delete import TestCanvasTermDelete
from tests.canvas.term.read import TestCanvasTermRead
from tests.canvas.term.update import TestCanvasTermUpdate
from tests.canvas.user.create import TestCanvasUserCreate
from tests.canvas.user.read import TestCanvasUserRead
from tests.canvas.user.update import TestCanvasUserUpdate

from tests.dialpad import TestDialpad

from tests.events.events import TestEventSystem

from tests.geolocator import TestGeolocator

from tests.gsuite.drive import TestGoogleDrive
from tests.gsuite.licensing import TestGSuiteLicensing
from tests.gsuite.sheets import TestGoogleSheets
from tests.gsuite.user_directory_test import TestUserDirectory
from tests.gsuite.student_users_test import TestStudentUsersHelpers

from tests.helpers.anthology import TestAnthologyHelpers
from tests.helpers.canvas import TestCanvasHelpers
from tests.helpers.field_maps import TestFieldMaps
from tests.helpers.input_validations import TestInputValidations
from tests.helpers.etl import TestETL
from tests.helpers.salesforce import TestSalesforceInputValidations
from tests.helpers.sql_alchemy import TestSqlAlchemyHelpers
from tests.helpers.sql_calbright.contact import TestContactHelper
from tests.helpers.sql_calbright.course_version_sections import TestCourseVersionSectionsHelper
from tests.helpers.sql_calbright.enrollment import TestEnrollmentHelper
from tests.helpers.sql_calbright.expressed_interest import ExpressInterest
from tests.helpers.sql_calbright.term_grades import TestUpsertEotgRecords

from tests.hubspot.transactional_email import TestHubspotTransactionalEmails

from tests.key_cdn import TestKeyCDN

from tests.logging_utility import TestLogging

from tests.panda_doc_test import TestPandaDoc

from tests.salesforce.attachment import TestAttachment
from tests.salesforce.bulk_test import TestSalesforceBulkQuery
from tests.salesforce.case import TestSalesforceCaseRecord
from tests.salesforce.contact_record import TestSalesforceContactRecord
from tests.salesforce.end_of_term_grades import TestEndOfTermGrades
from tests.salesforce.event import TestSalesforceEvent
from tests.salesforce.program_enrollment import TestProgramEnrollment
from tests.salesforce.query import TestSalesforceQuery
from tests.salesforce.task import TestSalesforceTask
from tests.salesforce.terms import TestSalesforceTerms
from tests.salesforce.veteran_record import TestSalesforceVeteranRecord

from tests.security.validation import TestSecurityValidation

from tests.slack.base import TestSlack

from tests.strut import TestStrut

from tests.sql.calbright.sql_test import TestSqlCalbright

from tests.symplicity.csm import TestCSM

from tests.twilio import TestTwilio

from tests.wp_webhooks import TestWPWebhook

from tests.zero_bounce import TestZeroBounce

from tests.zoom import TestZoom
from tests.tangoe.tangoe_test import TangoeTest
from tests.tangoe.people_test import TangoePeopleTest


logger = Logging.get_logger("unit_test")


tests = [
    TestAnthologyCertificateCreate,
    TestAnthologyConfigurationCopy,
    TestAnthologyConfigurationCreate,
    TestAnthologyConfigurationRead,
    TestAnthologyCourseChange,
    TestAnthologyCourseDrop,
    TestAnthologCourseGrade,
    TestAnthologyCourseRead,
    TestAnthologyCourseRegister,
    TestAnthologyCourseReinstate,
    TestAnthologyCourseUnregister,
    TestAnthologyEnrollmentCreate,
    TestAnthologyHelpers,
    TestAnthologyStudentCreate,
    TestAnthologyStudentRead,
    TestAnthologyStudentUpdate,
    APIClientTests,
    TestS3,
    TestSSM,
    TestSQS,
    TestCalendly,
    TestCanvasAssignmentRead,
    TestCanvasCourseCreate,
    TestCanvasCourseDelete,
    TestCanvasCourseRead,
    TestCanvasCourseUpdate,
    TestCanvasEnrollmentCreate,
    TestCanvasEnrollmentDelete,
    TestCanvasEnrollmentRead,
    TestCanvasEnrollmentUpdate,
    TestCanvasModuleRead,
    TestCanvasSubmissionRead,
    TestCanvasTermCreate,
    TestCanvasTermDelete,
    TestCanvasTermRead,
    TestCanvasTermUpdate,
    TestCanvasUserCreate,
    TestCanvasUserRead,
    TestCanvasUserUpdate,
    TestDialpad,
    TestEventSystem,
    TestFieldMaps,
    TestGeolocator,
    TestGoogleDrive,
    TestGoogleSheets,
    TestGSuiteLicensing,
    TestETL,
    TestSqlAlchemyHelpers,
    TestCanvasHelpers,
    TestContactHelper,
    TestCourseVersionSectionsHelper,
    TestEnrollmentHelper,
    ExpressInterest,
    TestUpsertEotgRecords,
    TestHubspotTransactionalEmails,
    TestInputValidations,
    TestSalesforceInputValidations,
    TestKeyCDN,
    TestLogging,
    TestPandaDoc,
    TestAttachment,
    TestSalesforceBulkQuery,
    TestSalesforceContactRecord,
    TestEndOfTermGrades,
    TestSalesforceCaseRecord,
    TestSalesforceEvent,
    TestProgramEnrollment,
    TestSalesforceQuery,
    TestSalesforceTask,
    TestSalesforceTerms,
    TestSalesforceVeteranRecord,
    # TestSlack, # Broken Needs to be fixed. Was never correctly implemented
    TestStrut,
    TestStudentUsersHelpers,
    TestSecurityValidation,
    TestSqlCalbright,
    TestCSM,
    TestTwilio,
    TestUserDirectory,
    TestWPWebhook,
    TestZeroBounce,
    TestZoom,
    TangoeTest,
    TangoePeopleTest,
]


def describe_failure(test):
    if len(test) == 2 and hasattr(test[0], "_testMethodName"):
        test = "Failed Test: {}".format(test[0]._testMethodName)
    logger.error(pformat(test))


if __name__ == "__main__":
    results = unittest.TestResult()
    loaded_tests = map(lambda test: unittest.TestLoader().loadTestsFromTestCase(test), tests)

    test_suite = unittest.TestSuite(loaded_tests).run(results)
    was_successful = results.wasSuccessful()
    tests_run = results.testsRun
    failures = results.failures
    errors = results.errors

    for error in errors:
        logger.error(error)

    if was_successful:
        logger.info(f"Success running {tests_run} tests")
    else:
        logger.error(f"Failure {len(failures)}/{tests_run} tests failed. {len(errors)} Errors")
        for failure in failures:
            describe_failure(failure)

    if len(failures) or len(errors):
        sys.exit(1)

    cov.save()
    cov.xml_report()
