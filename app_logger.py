# -------------< Library Imports >-----------
from flask import has_request_context, request
import logging
import global_variables

to_hide_fields_from_body = ['password']
class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.method = request.method
            record.remote_addr = request.remote_addr
            record.params = request.args.to_dict()
            record.body = request.get_json()
            if record.body and type(record.body) is dict:
                shortened_data = {k: "_______" for k in to_hide_fields_from_body if k in record.body and record.body[k]}
                if shortened_data:
                    to_be_shortened_data = {k: record.body[k] for k in record.body}
                    to_be_shortened_data.update(shortened_data)
                    record.body = to_be_shortened_data
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
