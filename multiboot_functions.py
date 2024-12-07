import dataclasses
import random
from typing import Union, List
import os
import os.path
from subprocess import Popen
import subprocess
import multiboot_global
from const_vars import LanguageType
from translations import translations
import configparser
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog
import webbrowser
import ttkbootstrap as ttk
import libuvk5
from serial import Serial
from const_vars import FIRMWARE_VERSION_LIST, EEPROM_SIZE
import serial_utils
import serial.tools.list_ports



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

BL_Name_1 = 'BL_3_001'
BL_Name_2 = 'BL_4_001'
BL_Name_3 = 'BL_6_001'
BL_Name_4 = 'L_BL002'

#Кнопка ЧаВо
def FAQ():
    webbrowser.open(translations[language]['multiboot_url'],new=1)

#Строка в последовательность байтов ASCII
def string_to_byte_seq(input_string):
    #.extend(map(ord, s))
    #np.frombuffer(b'ABC', dtype=np.uint8)
    #.encode('utf-8')
    return b''.join(bytes([ord(char)]) for char in input_string)

#Последовательность байтов в строку ASCII
def byte_seq_to_string(byte_seq):
    return byte_seq.decode('ascii')

#Число в последовательность байтов (4 байта)
def int_to_littleendian_byte_seq(value):
    value = int(value)
    return value.to_bytes(4, byteorder='little')

#Проверка на запаковку
def is_decrypted(data):
    #Миша, это не работает, прости
    #return data[:4] == b'\x88\x13\x00\x20' or data[:4] == b'\x88\x11\x00\x20'

    #я знаю что это уродство, но я ленивая жопа
    return data[0x10:0x20] == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

#Распаковка прошивки
def fw_unpack(data):
    libuvk5.crc16_ccitt_le(data[:-2]) == data[-2:]
    #if libuvk5.crc16_ccitt_le(data[:-2]) == data[-2:]:
        #Messagebox.show_info('Файл прошивки прошёл проверку CRC', translations[language]['Error'])
        #print('CRC OK')
    #else:
        #Messagebox.show_error('Файл прошивки не прошёл проверку CRC', translations[language]['Error'])
        #print('CRC MISMATCH!')
    data = libuvk5.firmware_xor(data[:-2])
    return data

#Выполнить .bat
def execute(file):
    #os.system(os.getcwd()+'/resources/OpenOCD/'+'openocd -f '+os.getcwd()+'/resources/OpenOCD/'+'interface/stlink.cfg -f '+os.getcwd()+'/resources/OpenOCD/'+'target/dp32g030.cfg -c "uv_flash_bl '+file+'" -c "shutdown')
    #subprocess.run([os.getcwd()+'/resources/'+file])
    #subprocess.call([os.getcwd()+'/resources/'+file], shell=False)
    Popen(os.getcwd()+'/resources/'+file, creationflags=subprocess.CREATE_NEW_CONSOLE)

#Сброс ячейки: обнуляет имя, сбрасывает файлы, вес файла прошивки
def Reset(tab, partition):
    multiboot_global.names[tab-1,partition-1,0] = ''
    multiboot_global.FW_sizes[tab-1,partition-1] = 0
    #удаляем временные файлы
    filenames = [(os.getcwd()+'/temp/tab'+str(tab)+'/FW'+str(partition)+'.bin'),
                 (os.getcwd()+'/temp/tab'+str(tab)+'/CFG'+str(partition)+'.bin'),
                 (os.getcwd()+'/temp/tab'+str(tab)+'/CAL'+str(partition)+'.bin')]
    for filename in filenames:
        if os.path.isfile(filename):
            os.remove(filename)
    #если есть предзагруженный ЕЕПРОМ, то вычищаем ячейку, формируя файлы пустышки
    if os.path.isfile(os.getcwd()+'/temp/tab'+str(tab)+'/EEPROM_preloaded.bin'):
        #пустой файл прошивки
        filename = os.getcwd()+'/temp/tab'+str(tab)+'/FW'+str(partition)+'.bin'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as fp:
            fp.write(bytearray([0xFF] * 60*1024))
        #пустой конфиг с калибровкой
        filename = os.getcwd()+'/temp/tab'+str(tab)+'/CFG'+str(partition)+'.bin'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as fp:
            fp.write(bytearray([0xFF] * 8*1024))

#Открыть файл (вкладка 1/2/3/4, ячейка 1/2/3/4/5/6, тип файла 1-прошивка/2-конфиг/3-калибровки)
def Open_file(tab, partition, filetype):
    file_path = filedialog.askopenfilename(filetypes=[("Binary files", "*.bin"), ("All files", "*.*")])
    multiboot_global.file_path = file_path
    if not file_path:
            Messagebox.show_info(translations[language]['Canceled'], translations[language]['Error'])
            return
    #Если файл - прошивка
    if filetype == 1:       
        #читаем файл
        with open(file_path, 'rb') as fp:
            firmware_data = fp.read()
        #если размер больше 60 килобайт - прерываем и показываем ошибку
        if len(firmware_data) > 61440:
            Messagebox.show_error(translations[language]['multiboot_open_FW'], translations[language]['Error'])
            multiboot_global.file_path = ''
            return
        #иначе проверяем энкрипчена ли прошивка (запакована) Простите, я так и не смог придумать качественную проверку, возможны проблемки
        else:
            filename = os.getcwd()+'/temp/tab'+str(tab)+'/FW'+str(partition)+'.bin'
            #если распакована, то сохраняем файлик в наш темп
            if is_decrypted(firmware_data):
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with open(filename, 'wb') as fp:
                    fp.write(firmware_data)              
            #если запакована - распаковываем
            else:
                firmware_data=fw_unpack(firmware_data)
                firmware_data=firmware_data[:0x2000]+firmware_data[0x2000+16:]
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with open(filename, 'wb') as fp:
                    fp.write(firmware_data)
            #пишем размер
            multiboot_global.FW_sizes[tab-1,partition-1]=len(firmware_data)
    #Если файл - конфиг
    elif filetype == 2:
        #читаем файл
        with open(file_path, 'rb') as fp:
            configuration_data = fp.read()
        #если размер больше 8килобайт и меньше 7 килобайт - прерываем и показываем ошибку
        if (len(configuration_data) > 8192)or(len(configuration_data) < 7424):
            Messagebox.show_error(translations[language]['multiboot_open_CFG'], translations[language]['Error'])
            multiboot_global.file_path = ''
            return
        else:
            filename = os.getcwd()+'/temp/tab'+str(tab)+'/CFG'+str(partition)+'.bin'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'wb') as fp:
                fp.write(configuration_data)
    #Если файл - калибровка
    else:       
        #читаем файл
        with open(file_path, 'rb') as fp:
            calibration_data = fp.read()
        #если размер не равен 512 байтам - прерываем и показываем ошибку
        if len(calibration_data) != 512:
            Messagebox.show_error(translations[language]['multiboot_open_CAL'], translations[language]['Error'])
            multiboot_global.file_path = ''
            return
        else:
            filename = os.getcwd()+'/temp/tab'+str(tab)+'/CAL'+str(partition)+'.bin'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'wb') as fp:
                fp.write(calibration_data)

#Загрузить слепок ЕЕПРОМ для редактирования (ДОДЕЛАТЬ! Полностью разбирает слепок на временные файлы)
def Load_EEPROM(tab):
    file_path = filedialog.askopenfilename(filetypes=[("Binary files", "*.bin"), ("All files", "*.*")])
    multiboot_global.file_path = file_path
    if not file_path:
            Messagebox.show_info('Файл не выбран', translations[language]['Error'])
            return
    if tab==1:
        with open(file_path, 'rb') as fp:
            eeprom_data = fp.read()
        #если размер больше 8килобайт и меньше 7 килобайт - прерываем и показываем ошибку
        if (len(eeprom_data) != 256*1024):
            Messagebox.show_error('Размер слепка EEPROM должен быть 256 KiB', translations[language]['Error'])
            multiboot_global.file_path = ''
            return
        #если по адресу нет идентификатора названия загрузчика показываем ошибку
        elif (eeprom_data[0xFF88:0xFF90] != string_to_byte_seq(BL_Name_1)):
            Messagebox.show_error('Выбрана неправильная вкладка или файл испорчен', translations[language]['Error'])
            multiboot_global.file_path = ''
            return        
        else:
            filename = os.getcwd()+'/temp/tab'+str(tab)+'/EEPROM_preloaded.bin'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'wb') as fp:
                fp.write(eeprom_data)
    else:
        with open(file_path, 'rb') as fp:
            eeprom_data = fp.read()
        #если размер больше 8килобайт и меньше 7 килобайт - прерываем и показываем ошибку
        if (len(eeprom_data) != 512*1024):
            Messagebox.show_error('Размер слепка EEPROM должен быть равен 512 KiB', translations[language]['Error'])
            multiboot_global.file_path = ''
            return
        else:
            filename = os.getcwd()+'/temp/tab'+str(tab)+'/EEPROM_preloaded.bin'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'wb') as fp:
                fp.write(eeprom_data)
    return eeprom_data

#Функция создания болванки ЕЕПРОМ заполненной FF байтами
def Make_EEPROM_FF(tab):
    if tab==1:
        data = bytearray([0xFF] * 256 * 1024)
    else:
        data = bytearray([0xFF] * 512 * 1024)
    return data

#Функция сборки ЕЕПРОМ из кусочков и конфигурирование мета данных
def Make_EEPROM(tab):
    #формируем массив пустышку для перезаписи вспомогательных загрузчиков
    #BL_blanc = bytearray([0xFF] * 0x3000)
    #если есть предзагруженный файл еепром temp/tab#/EEPROM.bin то пишем в него
    if (os.path.isfile(os.getcwd()+'/temp/tab'+str(tab)+'/EEPROM_preloaded.bin'))==0:
        Base = Make_EEPROM_FF(tab)
        multiboot_global.is_new=True
    else:
        with open(os.getcwd()+'/temp/tab'+str(tab)+'/EEPROM_preloaded.bin', 'rb') as fp:
            Base = fp.read() 
        multiboot_global.is_new=False

    if tab == 1:
        addresses = multiboot_global.Adresses_1
        address_Meta = 0xFF80
        address_BL = 0x10000
        BL_Name = BL_Name_1
        address_CFG1 = 0x9F80
        max=[0,1,2]
        Names = multiboot_global.names[0,:,0]
        FW_address=[0x13000,0x22000,0x31000]
        FW_size=multiboot_global.FW_sizes[0,:]

    elif tab == 2:
        addresses = multiboot_global.Adresses_2
        address_Meta = 0x40000
        address_BL = 0x41000
        BL_Name = BL_Name_2
        address_CFG1 = 0x38000
        max=[0,1,2,3]
        Names = multiboot_global.names[1,:,0]
        FW_address=[0x44000,0x53000,0x62000,0x71000]
        FW_size=multiboot_global.FW_sizes[1,:]

    elif tab == 3:
        addresses = multiboot_global.Adresses_3
        address_Meta = 0x22F20
        address_BL = 0x23000
        BL_Name = BL_Name_3
        address_CFG1 = 0x16F20
        max=[0,1,2,3,4,5]
        Names = multiboot_global.names[2,:,0]
        FW_address=[0x26000,0x35000,0x44000,0x53000,0x62000,0x71000]
        FW_size=multiboot_global.FW_sizes[2,:]

    else:
        addresses = multiboot_global.Adresses_4
        address_Meta = 0x40000
        address_BL = 0x41000
        BL_Name = BL_Name_4
        address_CFG1 = 0x0
        max=[0,1,2,3]
        Names = multiboot_global.names[3,:,0]
        FW_address=[0x44000,0x53000,0x62000,0x71000]
        FW_size=multiboot_global.FW_sizes[3,:]
    
    #Если файл новый, то
    if multiboot_global.is_new:        
        #Формируем мета данные
        #(количество прошивок)
        address_FW_num=address_Meta
        Base [address_FW_num]=len([item for item in FW_size if item != 0])
        #(Переменная режима для основного загрузчика. Всегда значение 01)
        address_Boot_mode = address_Meta+1
        Base [address_Boot_mode]=1
        #(Переменная текущей прошивки. Всегда значение 01
        address_Current_firm = address_Meta+2
        Base [address_Current_firm]=1
        #(Имя вспомогательного загрузчика)
        address_BL_name = address_Meta+8
        Base[address_BL_name:address_BL_name+8] = string_to_byte_seq(BL_Name)

        for n in max:
            if FW_size[n]!=0:
                #Имя прошивки, 13 байт
                address_Meta_name = address_Meta+(32*(n+1))
                Base[address_Meta_name:address_Meta_name+13] = string_to_byte_seq(Names[n])
                #Адрес старт 4 байта
                Meta_address_start = address_Meta+(32*(n+1))+16
                Base[Meta_address_start:Meta_address_start+4] = int_to_littleendian_byte_seq(FW_address[n])
                #Адрес стоп 4 байта
                Meta_address_end = address_Meta+(32*(n+1))+20
                Base[Meta_address_end:Meta_address_end+4] = int_to_littleendian_byte_seq(FW_address[n]+FW_size[n])
            #Если нет данных о размере файла
            else:
                Meta_address_start = address_Meta+(32*(n+1))+16
                Base[Meta_address_start:Meta_address_start+8] = b'\x00\x00\x00\x00\x00\x00\x00\x00'
        
        #Записываем вспомогательный загрузчик
        print(f"Writing bootloader at {hex(address_BL)}")
        with open(os.getcwd()+'/resources/'+BL_Name+'.bin', 'rb') as f:
            file_data = f.read()
        #Base [address_BL : address_BL + 0x3000] = BL_blanc
        Base [address_BL : address_BL + len(file_data)] = file_data

    #Записываем файлы исходя из словарей с адресами
    for mapping in addresses:
        file_name = mapping['filename']
        address = mapping['address']
        if not os.path.isfile(os.getcwd()+'/temp/tab'+str(tab)+'/'+file_name):
            continue
        with open(os.getcwd()+'/temp/tab'+str(tab)+'/'+file_name, 'rb') as f:
            file_data = f.read()
        print(f"Writing {file_name} to address {hex(address)} (size: {len(file_data)} bytes)")
        Base [address : address + len(file_data)] = file_data

    #Дублируем CFG1 область в [0x0:0x2000]
    if tab!=4:
        Base [0x0 : 0x2000] = Base[address_CFG1 : address_CFG1 + 0x2000]

    print(multiboot_global.FW_sizes)
    print(multiboot_global.FW_sizes.dtype)

    return Base

@dataclasses.dataclass
class SerialPortCheckResult:
    status: bool
    message: str
    firmware_version: int
    eeprom_size: int
    raw_version_text: str

#Опрос COM портов
def get_all_serial_port():
    ports = serial.tools.list_ports.comports()
    ports = [port.device for port in ports]
    return ports

def serial_port_combo_postcommand(combo: ttk.Combobox):
    combo['values'] = get_all_serial_port()

#Проверка ЕЕПРОМ на возможность записи
def check_eeprom_writeable(serial_port: serial.Serial, addr: int) -> bool:
    read_data = serial_utils.read_extra_eeprom(serial_port, addr, 8)
    random_bytes = bytes([random.randint(0, 255) for _ in range(8)])
    serial_utils.write_extra_eeprom(serial_port, addr, random_bytes)
    read_write_data = serial_utils.read_extra_eeprom(serial_port, addr, 8)
    serial_utils.write_extra_eeprom(serial_port, addr, read_data)
    return read_write_data == random_bytes

#Опрос рации инфа о прошивках итд
def check_serial_port(serial_port: serial.Serial,auto_detect: bool = True) -> SerialPortCheckResult:
    try:
        version = serial_utils.sayhello(serial_port)
        eeprom_size = 0
        if auto_detect:
            if version.startswith('LOSEHU'):
                firmware_version = 0
                if version.endswith('K') or version.endswith('H'):
                    firmware_version = 1
            else:
                firmware_version = 2

            if firmware_version == 1:
                # 检查EEPROM大小
                for i in range(1, 5):
                    # 128 KiB offset 0x1, 256 KiB offset 0x3, 384 KiB offset 0x5, 512 KiB offset 0x7
                    # 1 -> 0x1, 2 -> 0x3, 3 -> 0x5, 4 -> 0x7 符合 2n-1
                    if check_eeprom_writeable(serial_port, (2 * i - 1) * 0x10000 + 0x8000):
                        eeprom_size = i
                    else:
                        break
            msg = translations[language]['Сheck_port_1'] + version + translations[language]['Сheck_port_2'] + FIRMWARE_VERSION_LIST[firmware_version]+ '\n'
            if firmware_version != 1:
                msg += translations[language]['NOT']+FIRMWARE_VERSION_LIST[1]+translations[language]['Сheck_port_3']
            else:
                msg += translations[language]['Сheck_port_4'] + EEPROM_SIZE[eeprom_size]
        else:
            msg = translations[language]['Сheck_port_1'] + version + '\n'
            firmware_version = 2
            eeprom_size = 0
        return SerialPortCheckResult(True, msg, firmware_version, eeprom_size, version)
    except Exception as e:
        msg = translations[language]['Сheck_port_6'] + str(e)
        return SerialPortCheckResult(False, msg, 2, 0, '')

#Опрос
def serial_port_combo_callback(_, serial_port: str, eeprom_size_combo: ttk.Combobox):
    with serial.Serial(serial_port, 38400, timeout=2) as serial_port:
        serial_check = check_serial_port(serial_port)
        if serial_check.status:
            Messagebox.show_info(serial_check.message, translations[language]['Info'])
        else:
            Messagebox.show_error(serial_check.message, translations[language]['Error'])
        eeprom_size_combo.set(EEPROM_SIZE[serial_check.eeprom_size])

#Функция записи данных в EEPROM
def write_data(serial_port: Serial, start_addr: int, data: Union[bytes, List[int]],
               progress: ttk.Progressbar, window, step: int = 128):
    data_len = len(data)
    total_page = data_len // 128
    addr = start_addr
    current_step = 0
    while addr < start_addr + data_len:
        percent_float = (current_step / total_page) * 100
        percent = int(percent_float)
        progress['value'] = percent
        window.update()

        writing_data = bytes(data[:step])
        data = data[step:]
        if start_addr + data_len < 0x10000:
            serial_utils.write_eeprom(serial_port, addr, writing_data)
        else:
            serial_utils.write_extra_eeprom(serial_port, addr, writing_data)
        addr += step
        current_step += 1
    progress['value'] = 0
    window.update()

#Бэкап ЕЕПРОМ
def backup_eeprom(serial_port_text: str, window, progress: ttk.Progressbar, eeprom_size: int):
    if len(serial_port_text) == 0:
        Messagebox.show_error(translations[language]['COM_NONE'], translations[language]['Error'])
        return

    if eeprom_size > 0:
        target_eeprom_offset = 0x20000 * eeprom_size
    else:
        target_eeprom_offset = 0x2000
        
    with serial.Serial(serial_port_text, 38400, timeout=2) as serial_port:
        serial_check = check_serial_port(serial_port, False)
        if not serial_check.status:
            Messagebox.show_error(serial_check.message, translations[language]['Error'])
            return

        start_addr = 0x0  # 起始地址为0x0
        total_steps = (target_eeprom_offset - start_addr) // 128  # 计算总步数
        current_step = 0
        addr = start_addr

        backup_data = b''

        while addr < target_eeprom_offset:  # 限制地址范围为start_addr到target_eeprom_offset
            if target_eeprom_offset < 0x10000:
                read_data = serial_utils.read_eeprom(serial_port, addr, 128)
            else:
                read_data = serial_utils.read_extra_eeprom(serial_port, addr, 128)
            backup_data += read_data
            addr += 128
            current_step += 1
            percent_float = (current_step / total_steps) * 100
            progress['value'] = percent_float
            window.update()

        # 弹出文件保存对话框
        file_path = filedialog.asksaveasfilename(defaultextension=".bin", filetypes=[("Binary files", "*.bin"), ("All files", "*.*")])
        if not file_path:
            Messagebox.show_info(translations[language]['Canceled'], translations[language]['Error'])
            return 
        with open(file_path, 'wb') as fp:
            fp.write(backup_data)
        Messagebox.show_info(translations[language]['Backup_success'], translations[language]['Success'])

#Восстановление ЕЕПРОМ
def restore_eeprom(serial_port_text: str, window, progress: ttk.Progressbar, eeprom_size: int):
    if len(serial_port_text) == 0:
        Messagebox.show_error(translations[language]['COM_NONE'], translations[language]['Error'])
        return

    start_addr = 0x0
    if eeprom_size > 0:
        target_eeprom_offset = 0x20000 * eeprom_size
    else:
        target_eeprom_offset = 0x2000
        
    file_path = filedialog.askopenfilename(filetypes=[("Binary files", "*.bin"), ("All files", "*.*")])

    if not file_path:
        Messagebox.show_info(translations[language]['Canceled'], translations[language]['Info'])
        return

    with open(file_path, 'rb') as fp:
        restore_data = fp.read()

    if len(restore_data) != target_eeprom_offset:
        if Messagebox.yesno(translations[language]['Incompatible_1'] + str(len(restore_data)) + translations[language]['Incompatible_2'] + str(target_eeprom_offset) + translations[language]['Incompatible_3'], translations[language]['Info']) == 'No':
            Messagebox.show_info(translations[language]['Canceled'], translations[language]['Info'])
            return

    with serial.Serial(serial_port_text, 38400, timeout=2) as serial_port:
        serial_check = check_serial_port(serial_port, False)
        if not serial_check.status:
            Messagebox.show_error(serial_check.message, translations[language]['Error'])
            return
        write_data(serial_port, start_addr, restore_data, progress, window)
        #serial_utils.reset_radio(serial_port)
        Messagebox.show_info(translations[language]['Write_done'], translations[language]['Success'])

#Перезагрузка станции
def reset_radio(serial_port_text: str):
    with serial.Serial(serial_port_text, 38400, timeout=2) as serial_port:
        serial_check = check_serial_port(serial_port, False)
        if not serial_check.status:
            Messagebox.show_error(serial_check.message, translations[language]['Error'])
            return
        serial_utils.reset_radio(serial_port)

#Очистка ЕЕПРОМ
def clean_eeprom(serial_port_text: str, window, progress: ttk.Progressbar, eeprom_size: int):

    if not Messagebox.yesno(translations[language]['clean_warning_1'],translations[language]['Warning']) == 'Yes':
        return
    if not Messagebox.yesno(translations[language]['clean_warning_2'],translations[language]['Warning']) == 'Yes':
        return
    if Messagebox.yesno(translations[language]['clean_warning_3'],translations[language]['Warning']) == 'Yes':
        return

    if len(serial_port_text) == 0:
        Messagebox.show_error(translations[language]['COM_NONE'], translations[language]['Error'])
        return

    with serial.Serial(serial_port_text, 38400, timeout=2) as serial_port:
        serial_check = check_serial_port(serial_port, False)
        if not serial_check.status:
            Messagebox.showerror(serial_check.message, translations[language]['Error'])
            return
            """if firmware_version != 1:
            msg = translations[language]['NOT']+FIRMWARE_VERSION_LIST[1]+translations[language]['May_not_cleared']
            Messagebox.show_info(msg, translations[language]['Unexpanded'])
            for i in range(0, 64):
                percent_float = (i + 1) / 64 * 100
                percent = int(percent_float)
                progress['value'] = percent
                window.update()
                serial_utils.write_eeprom(serial_port, i * 128, b'\xff' * 128)"""
        else:
            target_eeprom_offset = 0x2000
            if eeprom_size > 0:
                target_eeprom_offset = 0x20000 * eeprom_size
            write_data(serial_port, 0, b'\xff' * target_eeprom_offset, progress, window)
        progress['value'] = 0
        window.update()
        #serial_utils.reset_radio(serial_port)
        Messagebox.show_info(translations[language]['EEROM_Cleared'], translations[language]['Success'])
