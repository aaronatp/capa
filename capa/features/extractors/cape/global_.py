# Copyright (C) 2020 Mandiant, Inc. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
# You may obtain a copy of the License at: [package root]/LICENSE.txt
# Unless required by applicable law or agreed to in writing, software distributed under the License
#  is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

import logging
from typing import Tuple, Iterator

from capa.features.common import (
    OS,
    OS_ANY,
    ARCH_ANY,
    OS_LINUX,
    ARCH_I386,
    FORMAT_PE,
    ARCH_AMD64,
    FORMAT_ELF,
    OS_WINDOWS,
    FORMAT_UNKNOWN,
    Arch,
    Format,
    Feature,
)
from capa.features.address import NO_ADDRESS, Address

logger = logging.getLogger(__name__)


def guess_elf_os(file_output) -> Iterator[Tuple[Feature, Address]]:
    # operating systems recognized by the file command: https://github.com/file/file/blob/master/src/readelf.c#L609
    if "Linux" in file_output:
        return OS(OS_LINUX), NO_ADDRESS
    elif "Hurd" in file_output:
        return OS("hurd"), NO_ADDRESS
    elif "Solaris" in file_output:
        return OS("solaris"), NO_ADDRESS
    elif "kFreeBSD" in file_output:
        return OS("freebsd"), NO_ADDRESS
    elif "kNetBSD" in file_output:
        return OS("netbsd"), NO_ADDRESS
    else:
        return OS(OS_ANY), NO_ADDRESS


def extract_arch(static) -> Iterator[Tuple[Feature, Address]]:
    if "Intel 80386" in static["target"]["type"]:
        return Arch(ARCH_I386), NO_ADDRESS
    elif "x86-64" in static["target"]["type"]:
        return Arch(ARCH_AMD64), NO_ADDRESS
    else:
        return Arch(ARCH_ANY)


def extract_format(static) -> Iterator[Tuple[Feature, Address]]:
    if "PE" in static["target"]["type"]:
        return Format(FORMAT_PE), NO_ADDRESS
    elif "ELF" in static["target"]["type"]:
        return Format(FORMAT_ELF), NO_ADDRESS
    else:
        logger.debug(f"unknown file format, file command output: {static['target']['type']}")
        return Format(FORMAT_UNKNOWN), NO_ADDRESS


def extract_os(static) -> Iterator[Tuple[Feature, Address]]:
    # this variable contains the output of the file command
    file_command = static["target"]["type"]

    if "WINDOWS" in file_command:
        return OS(OS_WINDOWS), NO_ADDRESS
    elif "ELF" in file_command:
        # implement os guessing from the cape trace
        return guess_elf_os(file_command)
    else:
        # the sample is shellcode
        logger.debug(f"unsupported file format, file command output: {file_command}")
        return OS(OS_ANY), NO_ADDRESS


def extract_features(static) -> Iterator[Tuple[Feature, Address]]:
    for global_handler in GLOBAL_HANDLER:
        for feature, addr in global_handler(static):
            yield feature, addr


GLOBAL_HANDLER = (
    extract_arch,
    extract_format,
    extract_os,
)
