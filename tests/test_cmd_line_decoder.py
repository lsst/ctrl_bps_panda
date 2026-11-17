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

import os
import unittest
from unittest.mock import patch

from lsst.ctrl.bps.panda.edgenode.cmd_line_decoder import replace_environment_vars, use_map_file


class TestCmdLineDecoder(unittest.TestCase):
    """Test command line decoder functions."""

    def test_scratch_environment(self):
        with patch.dict(os.environ, {"LSST_SHARED_SCRATCH_DIR": "/scratch"}, clear=True):
            self.assertEqual(
                replace_environment_vars("<ENV:LSST_SHARED_SCRATCH_DIR>/payload"), "/scratch/payload"
            )
            self.assertNotIn("LSST_RUN_TEMP_SPACE", os.environ)

    def test_no_legacy_scratch_fallback(self):
        with patch.dict(os.environ, {"LSST_RUN_TEMP_SPACE": "/old"}, clear=True):
            with self.assertRaisesRegex(ValueError, "LSST_SHARED_SCRATCH_DIR is not found"):
                replace_environment_vars("<ENV:LSST_SHARED_SCRATCH_DIR>/payload")

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
