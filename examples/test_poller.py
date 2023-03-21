# This file is part of ctrl_bps_panda.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Receiver test."""

import logging
import sys


# It seems import lsst packages will setup the logger. This test just
# setup logging by itself.
# Needs to be optimized.
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format='%(asctime)s\t%(threadName)s\t%(name)s\t%(levelname)s\t%(message)s')

from lsst.ctrl.bps.panda.utils import get_tasks, get_task_detail


logger = logging.getLogger("test_poller")


if __name__ == "__main__":
    request_id = 3526
    tasks = get_tasks(request_id=request_id)
    print("tasks: %s" % str(tasks))
    for task in tasks:
        task_detail = get_task_detail(request_id=request_id, workload_id=task)
        print("task_id: %s, detail: %s" % (task, task_detail))
