# Copyright 2016 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test DestroyPool.
"""

import time
import unittest

from stratis_cli._constants import TOP_OBJECT

from stratis_cli._dbus import Manager
from stratis_cli._dbus import Pool
from stratis_cli._dbus import get_object

from stratis_cli._actions._stratisd_constants import StratisdErrorsGen

from .._constants import _DEVICES

from .._misc import _device_list
from .._misc import Service


class Destroy1TestCase(unittest.TestCase):
    """
    Test 'destroy' on empty database.

    'destroy' should always succeed on an empty database.
    """
    _POOLNAME = 'deadpool'

    def setUp(self):
        """
        Start the stratisd daemon with the simulator.
        """
        self._service = Service()
        self._service.setUp()
        time.sleep(1)
        self._proxy = get_object(TOP_OBJECT)

    def tearDown(self):
        """
        Stop the stratisd simulator and daemon.
        """
        self._service.tearDown()

    def testExecution(self):
        """
        Destroy should succeed.
        """
        (rc, message) = Manager(self._proxy).DestroyPool(
           self._POOLNAME
        )
        self.assertEqual(rc, StratisdErrorsGen.get_object().STRATIS_OK)
        self.assertEqual(type(rc), int)
        self.assertEqual(type(message), str)

        (_, rc1, _) = Manager(self._proxy).GetPoolObjectPath(
           self._POOLNAME
        )

        expected_rc = StratisdErrorsGen.get_object().STRATIS_POOL_NOTFOUND
        self.assertEqual(rc1, expected_rc)


class Destroy2TestCase(unittest.TestCase):
    """
    Test 'destroy' on database which contains the given pool.
    """
    _POOLNAME = 'deadpool'

    def setUp(self):
        """
        Start the stratisd daemon with the simulator.
        """
        self._service = Service()
        self._service.setUp()
        time.sleep(1)
        self._proxy = get_object(TOP_OBJECT)
        Manager(self._proxy).CreatePool(
           self._POOLNAME,
           [d.device_node for d in _device_list(_DEVICES, 1)],
           0
        )

    def tearDown(self):
        """
        Stop the stratisd simulator and daemon.
        """
        self._service.tearDown()

    def testExecution(self):
        """
        The pool was just created, so must be destroyable.
        """
        (rc, message) = Manager(self._proxy).DestroyPool(
           self._POOLNAME
        )
        self.assertEqual(rc, StratisdErrorsGen.get_object().STRATIS_OK)
        self.assertEqual(type(rc), int)
        self.assertEqual(type(message), str)

        (_, rc1, _) = Manager(self._proxy).GetPoolObjectPath(
           self._POOLNAME
        )

        expected_rc = StratisdErrorsGen.get_object().STRATIS_POOL_NOTFOUND
        self.assertEqual(rc1, expected_rc)


class Destroy3TestCase(unittest.TestCase):
    """
    Test 'destroy' on database which contains the given pool and a volume.
    """
    _POOLNAME = 'deadpool'
    _VOLNAME = 'vol'

    def setUp(self):
        """
        Start the stratisd daemon with the simulator.
        Create a pool and a filesystem.
        """
        self._service = Service()
        self._service.setUp()

        time.sleep(1)
        self._proxy = get_object(TOP_OBJECT)
        (poolpath, _, _) = Manager(self._proxy).CreatePool(
           self._POOLNAME,
           [d.device_node for d in _device_list(_DEVICES, 1)],
           0
        )
        (_, _, _) = Pool(get_object(poolpath)).CreateVolumes(
           [(self._VOLNAME, '', '')]
        )

    def tearDown(self):
        """
        Stop the stratisd simulator and daemon.
        """
        self._service.tearDown()

    @unittest.expectedFailure
    def testExecution(self):
        """
        This should fail since it has a filesystem on it.
        """
        (rc, message) = Manager(self._proxy).DestroyPool(
           self._POOLNAME
        )
        self.assertNotEqual(rc, StratisdErrorsGen.get_object().STRATIS_OK)
        self.assertEqual(type(rc), int)
        self.assertEqual(type(message), str)
