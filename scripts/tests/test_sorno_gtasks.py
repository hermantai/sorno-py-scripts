"""
Tests for sorno_gtasks


   Copyright 2015 Heung Ming Tai

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import inspect
import mock
import unittest

from sornobase import loggingutil
import sorno_gtasks


loggingutil.setup_logger(sorno_gtasks._log)
sorno_gtasks._plain_logger = sorno_gtasks._log
sorno_gtasks._plain_error_logger = sorno_gtasks._log

class GoogleTasksConsoleAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = sorno_gtasks.GoogleTasksConsoleApp()
        self.app.auth = mock.MagicMock()
        self.args = mock.MagicMock()

    def test_copy_tasks_action(self):
        """
        The action should first make a call to get task lists for the user
        and show two task lists, ask for input to choose a task list.

        The test inputs "2", then the action should get task lists for that
        task list. The task list contains three items. The action should ask
        which tasks the user wants.

        The test inputs "1,3", then the action should show the tasks and
        ask the user to choose the destination task list.

        The test inputs "1", then the action should ask to confirm.

        The test inputs "y", then the action should make some calls to copy
        the tasks.
        """
        print(self._get_calling_method_name())

        tasklists = [
            {'id': "101", 'title': "tasklist1"},
            {'id': "102", 'title': "tasklist2"},
        ]
        tasklist2_tasks = [
            {'id': "501", 'title': "task1"},
            {'id': "502", 'title': "task2"},
            {'id': "503", 'title': "task3"},
        ]

        self.app.get_tasklists = mock.MagicMock(return_value=tasklists)

        def get_tasks_from_tasklist(tasklist_id):
            if tasklist_id == "102":
                return tasklist2_tasks
            else:
                raise ValueError(
                    tasklist_id + " is not 102"
                )

        self.app.get_tasks_from_tasklist = mock.MagicMock(
            side_effect=get_tasks_from_tasklist
        )

        self.app.insert_task = mock.MagicMock()

        with mock.patch(
            "sorno.consoleutil.input",
            side_effect=("2", "1,3", "1"),
        ), mock.patch(
            "sorno.consoleutil.confirm",
            return_value=True,
        ):
            self.app.copy_tasks_action(self.args)

        self.app.auth.assert_called_once_with(
            self.args,
            use_credentials_cache=self.args.use_credentials_cache,
        )

        self.app.insert_task.assert_has_calls(
            [
                mock.call("101", tasklist2_tasks[0]),
                mock.call("101", tasklist2_tasks[2]),
            ],
            any_order=True,
        )

    def test_copy_tasks_action_Aborted(self):
        """
        The action should first make a call to get task lists for the user
        and show two task lists, ask for input to choose a task list.

        The test inputs "2", then the action should get task lists for that
        task list. The task list contains three items. The action should ask
        which tasks the user wants.

        The test inputs "1,3", then the action should show the tasks and
        ask the user to choose the destination task list.

        The test inputs "1", then the action should ask to confirm.

        The test inputs "n", then the action should be aborted.
        """
        print(self._get_calling_method_name())

        tasklists = [
            {'id': "101", 'title': "tasklist1"},
            {'id': "102", 'title': "tasklist2"},
        ]
        tasklist2_tasks = [
            {'id': "501", 'title': "task1"},
            {'id': "502", 'title': "task2"},
            {'id': "503", 'title': "task3"},
        ]

        self.app.get_tasklists = mock.MagicMock(return_value=tasklists)

        def get_tasks_from_tasklist(tasklist_id):
            if tasklist_id == "102":
                return tasklist2_tasks
            else:
                raise ValueError(
                    tasklist_id + " is not 102"
                )

        self.app.get_tasks_from_tasklist = mock.MagicMock(
            side_effect=get_tasks_from_tasklist
        )

        self.app.insert_task = mock.MagicMock()

        with mock.patch(
            "sorno.consoleutil.input",
            side_effect=("2", "1,3", "1"),
        ), mock.patch(
            "sorno.consoleutil.confirm",
            return_value=False,
        ):
            self.app.copy_tasks_action(self.args)

        self.app.auth.assert_called_once_with(
            self.args,
            use_credentials_cache=self.args.use_credentials_cache,
        )

        self.assertFalse(self.app.insert_task.called)

    def test_delete_tasks_action_Aborted(self):
        """
        The action should first make a call to get task lists for the user
        and show two task lists, ask for input to choose a task list.

        The test inputs "2", then the action should get task lists for that
        task list. The task list contains three items. The action should ask
        which tasks the user wants.

        The test inputs "1,3", then the action should show the tasks and ask
        to confirm.

        The test inputs "n", then the action should be aborted.
        """
        print(self._get_calling_method_name())

        tasklists = [
            {'id': "101", 'title': "tasklist1"},
            {'id': "102", 'title': "tasklist2"},
        ]
        tasklist2_tasks = [
            {'id': "501", 'title': "task1"},
            {'id': "502", 'title': "task2"},
            {'id': "503", 'title': "task3"},
        ]

        self.app.get_tasklists = mock.MagicMock(return_value=tasklists)

        def get_tasks_from_tasklist(tasklist_id):
            if tasklist_id == "102":
                return tasklist2_tasks
            else:
                raise ValueError(
                    tasklist_id + " is not 102"
                )

        self.app.get_tasks_from_tasklist = mock.MagicMock(
            side_effect=get_tasks_from_tasklist
        )

        self.app.delete_task = mock.MagicMock()

        with mock.patch(
            "sorno.consoleutil.input",
            side_effect=("2", "1,3"),
        ), mock.patch(
            "sorno.consoleutil.confirm",
            return_value=False,
        ):
            self.app.delete_tasks_action(self.args)

        self.app.auth.assert_called_once_with(
            self.args,
            use_credentials_cache=self.args.use_credentials_cache,
        )

        self.assertFalse(self.app.delete_task.called)

    def test_delete_tasks_action(self):
        """
        The action should first make a call to get task lists for the user
        and show two task lists, ask for input to choose a task list.

        The test inputs "2", then the action should get task lists for that
        task list. The task list contains three items. The action should ask
        which tasks the user wants.

        The test inputs "1,3", then the action should show the tasks and ask
        to confirm.

        The test inputs "y", then the action should make some calls to delete
        the tasks.
        """
        print(self._get_calling_method_name())

        tasklists = [
            {'id': "101", 'title': "tasklist1"},
            {'id': "102", 'title': "tasklist2"},
        ]
        tasklist2_tasks = [
            {'id': "501", 'title': "task1"},
            {'id': "502", 'title': "task2"},
            {'id': "503", 'title': "task3"},
        ]

        self.app.get_tasklists = mock.MagicMock(return_value=tasklists)

        def get_tasks_from_tasklist(tasklist_id):
            if tasklist_id == "102":
                return tasklist2_tasks
            else:
                raise ValueError(
                    tasklist_id + " is not 102"
                )

        self.app.get_tasks_from_tasklist = mock.MagicMock(
            side_effect=get_tasks_from_tasklist
        )

        self.app.delete_task = mock.MagicMock()

        with mock.patch(
            "sorno.consoleutil.input",
            side_effect=("2", "1,3"),
        ), mock.patch(
            "sorno.consoleutil.confirm",
            return_value=True,
        ):
            self.app.delete_tasks_action(self.args)

        self.app.delete_task.assert_has_calls(
            [
                mock.call("102", tasklist2_tasks[0]['id']),
                mock.call("102", tasklist2_tasks[2]['id']),
            ],
            any_order=True,
        )

    def _get_calling_method_name(self):
        return inspect.stack()[1][3]
