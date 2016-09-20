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
Miscellaneous logical actions.
"""

from __future__ import print_function

from .._errors import StratisCliRuntimeError

from .._constants import TOP_OBJECT

from .._dbus import Pool
from .._dbus import Volume
from .._dbus import get_object


from ._stratisd_constants import StratisdErrorsGen

from ._misc import get_pool
from ._misc import get_volume


class LogicalActions(object):
    """
    Actions on the logical aspects of a pool.
    """

    @staticmethod
    def create_volumes(namespace):
        """
        Create volumes in a pool.

        :raises StratisCliRuntimeError:
        """
        proxy = get_object(TOP_OBJECT)
        pool_object = get_pool(proxy, namespace.pool)

        volume_list = [(x, '', '') for x in namespace.volume]
        (_, rc, message) = \
            Pool(pool_object).CreateVolumes(volume_list)

        if rc != StratisdErrorsGen().get_object().STRATIS_OK:
            raise StratisCliRuntimeError(rc, message)

        return

    @staticmethod
    def list_volumes(namespace):
        """
        List the volumes in a pool.
        """
        proxy = get_object(TOP_OBJECT)
        pool_object = get_pool(proxy, namespace.pool)
        (result, rc, message) = Pool(pool_object).ListVolumes()
        if rc != StratisdErrorsGen().get_object().STRATIS_OK:
            raise StratisCliRuntimeError(rc, message)

        for item in result:
            print(item)

        return

    @staticmethod
    def destroy_volumes(namespace):
        """
        Destroy volumes in a pool.
        """
        proxy = get_object(TOP_OBJECT)
        pool_object = get_pool(proxy, namespace.pool)
        (_, rc, message) = \
           Pool(pool_object).DestroyVolumes(namespace.volume)
        if rc != StratisdErrorsGen().get_object().STRATIS_OK:
            raise StratisCliRuntimeError(rc, message)

        return

    @staticmethod
    def snapshot(namespace):
        """
        Create a snapshot of an existing volume.
        """
        proxy = get_object(TOP_OBJECT)
        volume_object = get_volume(proxy, namespace.pool, namespace.origin)
        (_, rc, message) = \
           Volume(volume_object).CreateSnapshot(namespace.volume)
        if rc != StratisdErrorsGen().get_object().STRATIS_OK:
            raise StratisCliRuntimeError(rc, message)

        return
