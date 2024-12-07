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
