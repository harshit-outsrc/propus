""" Provides a common Logging Instance that can be used throughout this project

Logging has been setup as a singleton so you can initialize it once and then retrieve it multiple times throughout a
project.

Usage is as follows:
    l = Logging.get_logger(log_name='test', logging_level='warning', debug=True)
    # defaults logging_level = info, debug = False
    l.info('HELLO')
    l.warning('WORLD')

There are two different log formats:
 1) Set by debug = False (JSON format. Good for debugging within cloudWatch)
 2) Set by debug = True (Text format. Good for debugging locally)
"""

import logging
import inspect
import json_log_formatter


string_format = "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"

critical_alerts_only = ["elasticsearch", "boto", "botocore"]


def setupLogger(debug=False, log_name=None):
    Logging.debug = debug

    for alert_name in critical_alerts_only:
        logging.getLogger(alert_name).setLevel(logging.CRITICAL)

    # json_format should be used for all production runs as JSON can be search easily with cloudwatch insights
    handler = logging.StreamHandler()
    if debug:
        # string_format is fine for local development
        formatter = logging.Formatter(string_format)
    else:
        formatter = json_log_formatter.VerboseJSONFormatter()
    handler.setFormatter(formatter)
    logger = logging.getLogger(name=log_name)
    logger.handlers.clear()
    logger.addHandler(handler)


class Logging:
    debug = False

    @classmethod
    def get_logger(cls, log_name: str = "", logging_level: str = "info", debug: bool = False):
        """
        Simple logging module that will get or initialize a logger that will unify the logger across all pipelines
        :param log_name: Name of the log
        :param logging_level: Logging Level ('info', 'warning', or 'critical')
        :param debug: Boolean which sets log output format
        :return: logging instance that can be used in pipeline
        """

        debug = debug or cls.debug

        if logging_level == "info":
            log_level = logging.INFO
        elif logging_level == "warning":
            log_level = logging.WARNING
        elif logging_level == "critical":
            log_level = logging.CRITICAL

        if not log_name:
            frame = inspect.stack()[1]
            mod = inspect.getmodule(frame[0])
            if hasattr(mod, "__name__"):
                log_name = mod.__name__

        setupLogger(debug, log_name=log_name)

        logger = logging.getLogger(log_name)
        if debug:
            logger.setLevel(logging.DEBUG)
        elif log_level:
            logger.setLevel(log_level)
        return logger
