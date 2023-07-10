#!/usr/bin/env python
#
# Copyright (C) 2020-2023 Embedded AMS B.V. - All Rights Reserved
#
# This file is part of Embedded Proto.
#
# Embedded Proto is open source software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, version 3 of the license.
#
# Embedded Proto  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Embedded Proto. If not, see <https://www.gnu.org/licenses/>.
#
# For commercial and closed source application please visit:
# <https://EmbeddedProto.com/license/>.
#
# Embedded AMS B.V.
# Info:
#   info at EmbeddedProto dot com
#
# Postal address:
#   Atoomweg 2
#   1627 LE, Hoorn
#   the Netherlands
#

from os.path import abspath, dirname
from os.path import join as path_join
import subprocess
import os.path
import shutil
import sys
import os

# Constants
SCRIPT_DIR = abspath(dirname(__file__))  # The directory of this script
ROOT_DIR = abspath(path_join(SCRIPT_DIR, "..", ".."))  # Project root directory

PLUGIN = path_join("venv", "bin", "protoc-gen-eams")


def run_cmd(cmd):
    print(f"Executing {cmd}")
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    os.chdir(ROOT_DIR)

    try:
        shutil.rmtree("./code_coverage_report")
    except FileNotFoundError:
        pass

    os.makedirs("./code_coverage_report")

    cmd = [
        "gcovr",
        "--exclude",
        "external/",
        "--exclude",
        "test/",
    ]

    if len(sys.argv) > 1 and sys.argv[1] in ("-l", "--local"):
        cmd.extend(["--html", "--html-details", "-o" "code_coverage_report/index.html"])
    else:
        cmd.extend(["--sonarqube", "-o", "code_coverage_report/coverage.xml"])

    run_cmd(cmd)
