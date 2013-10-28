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



LogChronicle usage example

This is the main entry point file.  A call is made to another module (test2.py)
in order to show that binds can persist across the project.  And example
sample project with logging commands are provided below for a quick start.

Note: Line numbers may be incorrect in examples below due to ongoing
documentation changes.
"""

from log_chronicle import LOG


# ***** Step 1 *****
# Log a startup message no matter what the log level is
LOG.always("My App v1.0 starting...")

"""
The user friendly log output of this command would be:

{
    "loglevel": "ALWAYS",
    "timestamp": "2013-10-28T21:26:31Z",
    "lineno": 14,
    "file": "test.py",
    "event": "My App v1.0 starting..."
}

... notice how an ISO 8601 timestamp (UTC), loglevel, file and line number are
automatically added.
"""


# ***** Step 2 *****
# A user connects to the system
# Connection received from 1.2.3.4, save this information for later
# A unique_log_id is randomly generated in order to tie all logs together
# for this session.
LOG.bind(ipaddress='1.2.3.4', unique_log_id=54321)
# Note: bind() doesn't log, it just saves the data for later log commands


# ***** Step 3 *****
# Detected an attempted to log in by user Paul, the 'Logging in' data is not
# considered confidential data but the 'User is Paul' is
# marked private/confidential to enable easy filtering of logs before showing
# to users.  The way to mark any data confidential, by default, is to make
# the key value begin with 'private'.  This value is configurable.
LOG.bind(status='Logging in', private='User is Paul')


# ***** Step 4 *****
# Encountered an error authenticating, actually log the data.  There are two
# confidential log entries in this single statement.  Notice that each
# private key must be unique.  As long as the key starts with 'private', it
# will work.
LOG.error('Invalid user login credentials',
          private="Failed database access code 32 (exception data goes here)",
          private2="Login name does not exist")

"""
Log output will look like:

{
    "status": "Logging in",
    "loglevel": "ERROR",
    "timestamp": "2013-10-28T21:26:31Z",
    "private": [
        "User is Paul",
        "Login name does not exist",
        "Failed database access code 32 (exception data goes here)"
    ],
    "lineno": 56,
    "file": "test.py",
    "unique_log_id": 54321,
    "ipaddress": "1.2.3.4",
    "event": "Invalid user login credentials"
}

Note how unique_log_id is carried forward enabling easy log collation
"""


# ***** Step 5 *****
# Show binds persisting across modules
# The test2.py module will create a new bind() and a new log entry
import test2
test2.log_func()

"""
Log output from this module will look like:

{
    "status": "Logging in",
    "loglevel": "WARNING",
    "timestamp": "2013-10-28T21:26:31Z",
    "private": [
        "User is Paul",
        "Login name does not exist",
        "Failed database access code 32 (exception data goes here)"
    ],
    "lineno": 6,
    "file": "/user/code/log/test2.py",
    "unique_log_id": 54321,
    "ipaddress": "1.2.3.4",
    "event": "Set backoff timer",
    "login_backoff_timer": [30, "seconds"]
}

Note how the binds all persist when executing in test2.py.  They also persist
in the original test.py file (test2.py used bind() on the login_backoff_timer).
Also, login_backoff_timer uses an array to demonstrate the various variable
types supported (even though the example may not make much sense).
"""


# ***** Step 6 *****
# Delete bound data and prepare for new login
# Log again just to show what it looks like
LOG.clear_bindings()
LOG.warning("Test log to show that previous bindings are deleted.")

"""
Log output:

{
    "loglevel": "WARNING",
    "timestamp": "2013-10-28T21:26:31Z",
    "lineno": 77,
    "file": "test.py",
    "event": "Test log to show that previous bindings are deleted."
}

The system is now ready to receive new user logins without the old bind() data
still hanging around.
"""
