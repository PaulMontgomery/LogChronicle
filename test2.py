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


LogChronicle usage example 2

This example demonstrates bind() persistance across modules and is called by
test.py.
"""

from log_chronicle import LOG


def log_func():
    """ Show binds persisting across modules """
    LOG.bind(login_backoff_timer=[30, 'seconds'])
    LOG.warning("Set backoff timer")
