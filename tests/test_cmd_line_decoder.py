# This file is part of ctrl_bps_panda.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This software is dual licensed under the GNU General Public License and also
# under a 3-clause BSD license. Recipients may choose which of these licenses
# to use; please see the files gpl-3.0.txt and/or bsd_license.txt,
# respectively.  If you choose the GPL option then the following text applies
# (but note that there is still no warranty even if you opt for BSD instead):
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

"""Unit tests for edgenode/cmd_line_decoder.py."""

import unittest

from lsst.ctrl.bps.panda.edgenode.cmd_line_decoder import use_map_file


class TestCmdLineDecoder(unittest.TestCase):
    """Test command line decoder functions."""

    def test_valid_input(self):
        self.assertTrue(use_map_file("PH:file12345"))

    def test_invalid_prefix(self):
        self.assertFalse(use_map_file("XX:file12345"))

    def test_missing_colon(self):
        self.assertFalse(use_map_file("PH12345"))

    def test_too_many_parts(self):
        self.assertFalse(use_map_file("PH:file123:456"))


if __name__ == "__main__":
    unittest.main()
