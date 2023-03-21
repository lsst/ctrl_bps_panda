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

from lsst.ctrl.bps.panda.receiver import MessagingReceiver


logger = logging.getLogger("test_receiver")


if __name__ == "__main__":
    config_file = "${CTRL_BPS_PANDA_DIR}/config/bps_idds_receiver.yaml"
    msg_receiver = MessagingReceiver(config_file, logger)
    msg_receiver()
