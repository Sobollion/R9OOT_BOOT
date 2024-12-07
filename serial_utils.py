import struct
import serial
from logger import log
from translations import translations
from const_vars import LanguageType
import configparser
import os


appdata_path = os.getenv('APPDATA') if os.getenv('APPDATA') is not None else ''
config_dir = os.path.join(appdata_path, 'R9OOT-BOOT')
config_path = os.path.join(config_dir, 'config.ini')

config = configparser.ConfigParser()
config.read(config_path)

if 'ConfigVersion' not in config:
    config['ConfigVersion'] = {}
if 'configversion' not in config['ConfigVersion']:
    config['ConfigVersion']['configversion'] = '0.2'
if 'Settings' not in config:
    config['Settings'] = {}
if 'theme' not in config['Settings']:
    config['Settings']['theme'] = 'darkly'
if 'language' not in config['Settings']:
    config['Settings']['language'] = LanguageType.ENGLISH.name

config_version = config.get('ConfigVersion', 'configversion')
language = LanguageType.find_name(config.get('Settings', 'language'))


def xor_arr(data: bytes):
    tbl = [22, 108, 20, 230, 46, 145, 13, 64, 33, 53, 213, 64, 19, 3, 233, 128]
    x = b""
    r = 0
    for byte in data:
        x += bytes([byte ^ tbl[r]])
        r = (r + 1) % len(tbl)
    return x


def calculate_crc16_xmodem(data: bytes):
    poly = 0x1021
    crc = 0x0
    for byte in data:
        crc = crc ^ (byte << 8)
        for i in range(8):
            crc = crc << 1
            if crc & 0x10000:
                crc = (crc ^ poly) & 0xFFFF
    return crc & 0xFFFF


def send_command(serial_port: serial.Serial, data: bytes):
    crc = calculate_crc16_xmodem(data)
    data2 = data + struct.pack("<H", crc)

    command = struct.pack(">HBB", 0xabcd, len(data), 0) + \
              xor_arr(data2) + \
              struct.pack(">H", 0xdcba)
    try:
        result = serial_port.write(command)
    except Exception:
        raise Exception(translations[language]['Exception_1'])
    return result


def receive_reply(serial_port: serial.Serial):
    header = serial_port.read(4)
    if len(header) != 4:
        raise Exception(translations[language]['Exception_2'])
    if header[0] != 0xAB or header[1] != 0xCD or header[3] != 0x00:
        raise Exception(translations[language]['Exception_3'])

    cmd = serial_port.read(int(header[2]))
    if len(cmd) != int(header[2]):
        raise Exception(translations[language]['Exception_4'])

    footer = serial_port.read(4)

    if len(footer) != 4:
        raise Exception(translations[language]['Exception_5'])

    if footer[2] != 0xDC or footer[3] != 0xBA:
        raise Exception(translations[language]['Exception_6'])

    cmd2 = xor_arr(cmd)
    return cmd2


def get_string(data: bytes, begin: int, max_len: int):
    tmp_len = min(max_len + 1, len(data))
    s = [data[i] for i in range(begin, tmp_len)]
    index = 0
    for key, val in enumerate(s):
        index = key
        if val < ord(' ') or val > ord('~'):
            break
    return ''.join(chr(x) for x in s[0:index])


def sayhello(serial_port: serial.Serial):
    log('发送hello指令')
    hello_packet = b"\x14\x05\x04\x00\x6a\x39\x57\x64"

    try:
        tries = 5
        while True:
            send_command(serial_port, hello_packet)
            o = receive_reply(serial_port)
            if o:
                break
            tries -= 1
            if tries == 0:
                raise Exception(translations[language]['Exception_7'])
    except Exception as e:
        raise Exception(  translations[language]['Exception_7'] +'<-' + str(e))
    firmware = get_string(o, 4, len(o))
    return firmware


def read_eeprom(serial_port: serial.Serial, offset: int, length: int):
    read_mem = b"\x1b\x05\x08\x00" + \
        struct.pack("<HBB", offset, length, 0) + \
        b"\x6a\x39\x57\x64"
    send_command(serial_port, read_mem)
    o = receive_reply(serial_port)
    return o[8:]


def read_extra_eeprom(serial_port: serial.Serial, addr: int, length: int):
    offset = addr >> 16
    extra = addr & 0xFFFF
    extra_bytes = struct.pack("<H", extra)
    read_mem = b"\x2b\x05\x08\x00" + \
               struct.pack("<HBB", offset, length, 0) + \
               b"\x6a\x39\x57\x64" + \
               extra_bytes
    send_command(serial_port, read_mem)
    o = receive_reply(serial_port)
    return o[8:]


def write_eeprom(serial_port: serial.Serial, offset: int, data: bytes):
    dlen = len(data)
    write_mem = b"\x1d\x05" + \
                struct.pack("<BBHBB", dlen + 8, 0, offset, dlen, 1) + \
                b"\x6a\x39\x57\x64" + data

    send_command(serial_port, write_mem)
    o = receive_reply(serial_port)

    if (o[0] == 0x1e
            and
            o[4] == (offset & 0xff)
            and
            o[5] == (offset >> 8) & 0xff):
        return True
    else:
        raise Exception(translations[language]['Exception_8'])


def write_extra_eeprom(serial_port: serial.Serial, addr: int, data: bytes):
    offset = addr >> 16
    extra = addr & 0xFFFF
    extra = struct.pack("<H", extra)
    length = len(data) + len(extra)

    write_mem = b"\x38\x05\x1c\x00" + \
                struct.pack("<HBB", offset, length, 0) + \
                b"\x6a\x39\x57\x64" + \
                extra + data

    send_command(serial_port, write_mem)
    o = receive_reply(serial_port)

    if (o[0] == 0x1e
            and
            o[4] == (offset & 0xff)
            and
            o[5] == (offset >> 8) & 0xff):
        return True
    else:
        raise Exception(translations[language]['Exception_9'])


def reset_radio(serial_port: serial.Serial):
    log('发送复位指令')
    reset_packet = b"\xdd\x05\x00\x00"
    send_command(serial_port, reset_packet)
