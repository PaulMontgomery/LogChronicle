"""
Copyright 2013 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.



Log Chronicle - simple enhanced Python logging module

This module provides a simple extension to the Python logging module:
- Automatic support for adding filename and line number to logs
- Ability to mark 'private' admin only log data to make filtering out
    sensitive data out of logs before showing to users/customers
- Enable status logging regardless of log level (not marked as an error)
- Support for various data types in logs (not just strings)
- Structured Python dictionary-based logs
- Capability to bind() useful data to the log class which will be captured
    when a log action takes place.
- Maintain binds and log state across modules easily
- Basic features look/act like normal Python logging module
- JSON log output
"""

import datetime
import inspect
import json
import logging
import logging.handlers


class LogChronicle:
    """ Extends the Logging module and enhanced logging features """

    def __init__(self, log_name=''):
        """ Default to loglevel WARNING and a syslog destination """
        self._priv_str = 'private'
        self._bind_dict = {}
        self._priv_list = []
        self._orig_log = logging.getLogger(log_name)
        self._orig_log.setLevel(logging.WARNING)
        handler = logging.handlers.SysLogHandler(address='/dev/log')
        self._orig_log.addHandler(handler)

    def get_private_str(self):
        """ Get the private log indicator key string """
        return self._priv_str

    def set_private_str(self, priv_str):
        """ Set the private log indicator key string """
        self._priv_str = priv_str

    def set_log_level(self, loglevel):
        """ Change the log level """
        self._orig_log.setLevel(loglevel)

    def delete_handlers(self):
        """ Delete all log destinations, add_handler() should follow """
        self._orig_log.handlers = []

    def add_handler(self, handler):
        """ Add a new log destination """
        self._orig_log.addHandler(handler)

    def bind(self, **kwargs):
        """ Add new key/value pairs to be included in all subsequent logs """
        for key, val in kwargs.items():
            if key.startswith(self._priv_str):
                self._priv_list.append(val)
            else:
                self._bind_dict[key] = val

    def clear_bindings(self):
        """ Remove all key/value binding pairs """
        self._bind_dict = {}
        self._priv_list = []

    def info(self, *args, **kwargs):
        """ Calls logging.info """
        self._orig_log.info(self._add_metadata('INFO', args, kwargs))

    def warning(self, *args, **kwargs):
        """ Calls logging.warning """
        self._orig_log.warning(self._add_metadata('WARNING', args, kwargs))

    def error(self, *args, **kwargs):
        """ Calls logging.error """
        self._orig_log.error(self._add_metadata('ERROR', args, kwargs))

    def critical(self, *args, **kwargs):
        """ Calls logging.critical """
        self._orig_log.critical(self._add_metadata('CRITICAL', args, kwargs))

    def always(self, *args, **kwargs):
        """ Always log this no matter what the loglevel is """
        self._orig_log.critical(self._add_metadata('ALWAYS', args, kwargs))

    def _add_metadata(self, loglevel, args, kwargs):
        """ Automatically add time, file and line number to log data """
        temp_bind_dict = self._bind_dict
        # Format UTC timestamp in ISO 8601 format
        temp_bind_dict['timestamp'] = (
            datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
        temp_bind_dict['loglevel'] = loglevel

        # Use inspect to obtain caller information (file and lineno)
        _, file_name, line_num, _, _, _ = inspect.getouterframes(
            inspect.currentframe())[2]
        temp_bind_dict['file'] = file_name
        temp_bind_dict['lineno'] = line_num

        if len(args) > 0:  # should only be 1 arg value, others are ignored
            temp_bind_dict['event'] = args[0]

        for key, val in kwargs.items():
            if key.startswith(self._priv_str):
                self._priv_list.append(val)
            else:
                temp_bind_dict[key] = val

        if len(self._priv_list) > 0:
            temp_bind_dict[self._priv_str] = self._priv_list

        # Turn into JSON
        temp_bind_dict = json.dumps(temp_bind_dict, encoding='utf-8',
                                    ensure_ascii=False)

        return temp_bind_dict


LOG = LogChronicle()
