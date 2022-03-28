# Copyright (C) 2022 FireEye, Inc. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
# You may obtain a copy of the License at: [package root]/LICENSE.txt
# Unless required by applicable law or agreed to in writing, software distributed under the License
#  is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

import textwrap

import pytest

import capa.rules


def test_rule_scope_instruction():
    capa.rules.Rule.from_yaml(
        textwrap.dedent(
            """
            rule:
                meta:
                    name: test rule
                    scope: instruction
                features:
                  - and:
                    - mnemonic: mov
                    - arch: i386
                    - os: windows
            """
        )
    )

    with pytest.raises(capa.rules.InvalidRule):
        capa.rules.Rule.from_yaml(
            textwrap.dedent(
                """
                rule:
                    meta:
                        name: test rule
                        scope: instruction
                    features:
                        - characteristic: embedded pe
                """
            )
        )
