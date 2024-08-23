import unittest
import unittest.mock
import json

from propus.logging_utility import Logging


class ModuleUsingLogging:
    def __init__(self):
        self.logger = Logging.get_logger()


class TestLogging(unittest.TestCase):
    def test_get_logger(self):
        with unittest.mock.patch("logging.getLogger") as mock_get_logger:
            mod = ModuleUsingLogging()
            mock_get_logger.assert_called_with(mod.__module__)

            mock_get_logger.reset_mock()
            logger_name = "myname"
            Logging.get_logger("myname")
            mock_get_logger.assert_called_with(logger_name)

    def test_logger(self):
        debug_logger = Logging.get_logger(log_name="debug", debug=True)
        with self.assertLogs(logger="debug") as debug_cm:
            debug_logger.info("hello world")

        for log in debug_cm.output:
            with self.assertRaises(json.JSONDecodeError):
                json.loads(log)


if __name__ == "__main__":
    unittest.main()
