# -------------< Library Imports >-----------
from flask import has_request_context, request
import logging
import global_variables

class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.method = request.method
            record.remote_addr = request.remote_addr
            record.params = request.args.to_dict()
            record.body = request.get_json()
        else:
            record.url = 'No Route'
            record.method = 'No Method'
            record.remote_addr = 'Local Application'
            record.params = {}
            record.body = {}

        return super().format(record)

def logger_initializer(app_name: str, logger_name: str, logging_format: str, logging_level: str):
    logFormatter = RequestFormatter(logging_format)

    rootLogger = logging.getLogger(app_name)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)

    rootLogger.addHandler(consoleHandler)

    rootLogger.setLevel(logging_level)
    rootLogger.propagate = False

    global_variables.multiprocess_globals[logger_name] = rootLogger
