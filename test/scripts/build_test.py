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
import concurrent.futures
import subprocess
import os.path
import os

# Constants
SCRIPT_DIR = abspath(dirname(__file__))  # The directory of this script
ROOT_DIR = abspath(path_join(SCRIPT_DIR, "..", ".."))  # Project root directory

PLUGIN = path_join("venv", "bin", "protoc-gen-eams")

# Which files to operate on
PROTO_FILES = [
    "./test/proto/simple_types.proto",
    "./test/proto/nested_message.proto",
    "./test/proto/repeated_fields.proto",
    "./test/proto/oneof_fields.proto",
    "./test/proto/include_other_files.proto",
    # Delibertly do not manually generate file_to_include.proto and subfolder/file_to_include_from_subfolder.proto
    # to test the automatic generation of files from including them in include_other_files.proto.
    "./test/proto/string_bytes.proto",
    "./test/proto/empty_message.proto",
    "./test/proto/optional_fields.proto",
]

EXTRA_PROTOC_ARGS = {"./test/proto/field_options.proto": ["-I./generator"]}


def run_cmd(cmd):
    print(f"Executing {cmd}")
    subprocess.run(cmd, check=True)


def protoc_eams(filename: str) -> None:
    cmd = [
        "protoc",
        f"--plugin={PLUGIN}",
        f"-I./test/proto",
        f"--eams_out=./build/EAMS",
    ]
    cmd.extend(EXTRA_PROTOC_ARGS.get(filename, []))
    cmd.append(filename)

    run_cmd(cmd)


def protoc_python(filename: str) -> None:
    cmd = [
        "protoc",
        f"--plugin={PLUGIN}",
        f"-I./test/proto",
        f"--python_out=./build/python",
    ]
    cmd.extend(EXTRA_PROTOC_ARGS.get(filename, []))
    cmd.append(filename)

    run_cmd(cmd)


if __name__ == "__main__":
    os.chdir(ROOT_DIR)

    # Create output directories
    os.makedirs("./build/EAMS", exist_ok=True)
    os.makedirs("./build/python/subfolder", exist_ok=True)

    # Generate sources using the EAMS plugin.
    with concurrent.futures.ThreadPoolExecutor() as e:
        for filename in PROTO_FILES:
            e.submit(protoc_eams, filename)

    # For validation and testing generate the same message using python
    with concurrent.futures.ThreadPoolExecutor() as e:
        for filename in PROTO_FILES:
            e.submit(protoc_python, filename)

    # Run tests
    run_cmd(["cmake", "-DCMAKE_BUILD_TYPE=Debug", "-B./build/test"])
    run_cmd(["make", "-j16", "./build/test"])
