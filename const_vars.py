# Copyright 2024 hank9999
# https://github.com/hank9999
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

from enum import Enum

FIRMWARE_VERSION_LIST = ['LoseHu', 'LoseHu +', 'Other']
EEPROM_SIZE = ['8KiB (factory)', '128KiB (1M)', '256KiB (2M)', '384KiB (3M)', '512KiB (4M)']
EEPROM_MLTBT_SIZE = ['256KiB (2M)', '512KiB (4M)']


class FontType(Enum):
    GB2312_COMPRESSED = '压缩GB2312'
    GB2312_UNCOMPRESSED = '未压缩GB2312'
    LOSEHU_FONT = '萝狮虎字库'


class LanguageType(Enum):
    SIMPLIFIED_CHINESE = '简体中文'
    ENGLISH = 'English'
    RUSSIAN = 'Русский'

    @staticmethod
    def find_value(value: str) -> 'LanguageType':
        for item in LanguageType:
            if item.value == value:
                return item
        return LanguageType.ENGLISH

    @staticmethod
    def find_name(name: str) -> 'LanguageType':
        for item in LanguageType:
            if item.name == name:
                return item
        return LanguageType.ENGLISH

    @staticmethod
    def value_list():
        return list(map(lambda i: i.value, LanguageType))
