# -------------< Library Imports >-----------
import logging
from flask import has_request_context, request

multi_loggers = {}

to_hide_fields_from_body = ['password']
class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.method = request.method
            record.remote_addr = request.remote_addr
            record.params = request.args.to_dict()
            record.body = {}
            if request.is_json:
                record.body = request.get_json()
                if record.body and isinstance(record.body, dict):
                    shortened_data = {
                        k: record.body[k][:2] + "*****" + record.body[k][-2:]
                        for k in to_hide_fields_from_body
                        if k in record.body
                        and record.body[k]
                        and isinstance(record.body[k], str)
                    }
                    if shortened_data:
                        to_be_shortened_data = {
                            k: record.body[k]
                            for k in record.body
                        }
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

    multi_loggers[logger_name] = rootLogger
