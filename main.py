import time
import serial.tools.list_ports
from const_vars import EEPROM_SIZE, LanguageType
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
import shutil
from PIL import Image, ImageTk
from tkinter import filedialog
from ttkbootstrap.dialogs import Messagebox
from translations import translations
import configparser
import threading

from multiboot_functions import (
    execute,
    Reset,
    Open_file,
    FAQ,
    Load_EEPROM,
    byte_seq_to_string,
    Make_EEPROM,
    serial_port_combo_postcommand,
    serial_port_combo_callback,
    clean_eeprom,
    backup_eeprom,
    restore_eeprom,
    reset_radio,
    write_data,
    check_serial_port
)

import multiboot_global

multiboot_window = ttk.Window()

multiboot_version = '0.1'


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
style = ttk.Style(config.get('Settings', 'theme'))
language = LanguageType.find_name(config.get('Settings', 'language'))

#ресетим 3д массив
multiboot_global.names[:,:,0] = ''
multiboot_global.names[:,:,1] = translations[language]['multiboot_Firmware']
multiboot_global.names[:,:,2] = translations[language]['multiboot_Configuration']
multiboot_global.names[:,:,3] = translations[language]['multiboot_Calibration']

tvar_FW_name = [ttk.StringVar(value=''),
                ttk.StringVar(value=''),
                ttk.StringVar(value=''),
                
                ttk.StringVar(value=''),
                ttk.StringVar(value=''),
                ttk.StringVar(value=''),
                ttk.StringVar(value=''),

                ttk.StringVar(value=''),
                ttk.StringVar(value=''),
                ttk.StringVar(value=''),
                ttk.StringVar(value=''),
                ttk.StringVar(value=''),
                ttk.StringVar(value=''),

                ttk.StringVar(value=''),
                ttk.StringVar(value=''),
                ttk.StringVar(value=''),
                ttk.StringVar(value='')
                ]
tvar_FW_button = [ttk.StringVar(value=translations[language]['multiboot_Firmware']),
                  ttk.StringVar(value=translations[language]['multiboot_Firmware']),
                  ttk.StringVar(value=translations[language]['multiboot_Firmware']),
                  
                  ttk.StringVar(value=translations[language]['multiboot_Firmware']),
                  ttk.StringVar(value=translations[language]['multiboot_Firmware']),
                  ttk.StringVar(value=translations[language]['multiboot_Firmware']),
                  ttk.StringVar(value=translations[language]['multiboot_Firmware']),

                  ttk.StringVar(value=translations[language]['multiboot_Firmware']),
                  ttk.StringVar(value=translations[language]['multiboot_Firmware']),
                  ttk.StringVar(value=translations[language]['multiboot_Firmware']),
                  ttk.StringVar(value=translations[language]['multiboot_Firmware']),
                  ttk.StringVar(value=translations[language]['multiboot_Firmware']),
                  ttk.StringVar(value=translations[language]['multiboot_Firmware']),

                  ttk.StringVar(value=translations[language]['multiboot_Firmware']),
                  ttk.StringVar(value=translations[language]['multiboot_Firmware']),
                  ttk.StringVar(value=translations[language]['multiboot_Firmware']),
                  ttk.StringVar(value=translations[language]['multiboot_Firmware'])
                  ]
tvar_CFG_button = [ttk.StringVar(value=translations[language]['multiboot_Configuration']),
                   ttk.StringVar(value=translations[language]['multiboot_Configuration']),
                   ttk.StringVar(value=translations[language]['multiboot_Configuration']),

                   ttk.StringVar(value=translations[language]['multiboot_Configuration']),
                   ttk.StringVar(value=translations[language]['multiboot_Configuration']),
                   ttk.StringVar(value=translations[language]['multiboot_Configuration']),
                   ttk.StringVar(value=translations[language]['multiboot_Configuration']),

                   ttk.StringVar(value=translations[language]['multiboot_Configuration']),
                   ttk.StringVar(value=translations[language]['multiboot_Configuration']),
                   ttk.StringVar(value=translations[language]['multiboot_Configuration']),
                   ttk.StringVar(value=translations[language]['multiboot_Configuration']),
                   ttk.StringVar(value=translations[language]['multiboot_Configuration']),
                   ttk.StringVar(value=translations[language]['multiboot_Configuration']),

                   ttk.StringVar(value=translations[language]['multiboot_Configuration']),
                   ttk.StringVar(value=translations[language]['multiboot_Configuration']),
                   ttk.StringVar(value=translations[language]['multiboot_Configuration']),
                   ttk.StringVar(value=translations[language]['multiboot_Configuration'])
                   ]
tvar_CAL_button = [ttk.StringVar(value=translations[language]['multiboot_Calibration']),
                   ttk.StringVar(value=translations[language]['multiboot_Calibration']),
                   ttk.StringVar(value=translations[language]['multiboot_Calibration']),
                   
                   ttk.StringVar(value=translations[language]['multiboot_Calibration']),
                   ttk.StringVar(value=translations[language]['multiboot_Calibration']),
                   ttk.StringVar(value=translations[language]['multiboot_Calibration']),
                   ttk.StringVar(value=translations[language]['multiboot_Calibration']),
                   
                   ttk.StringVar(value=translations[language]['multiboot_Calibration']),
                   ttk.StringVar(value=translations[language]['multiboot_Calibration']),
                   ttk.StringVar(value=translations[language]['multiboot_Calibration']),
                   ttk.StringVar(value=translations[language]['multiboot_Calibration']),
                   ttk.StringVar(value=translations[language]['multiboot_Calibration']),
                   ttk.StringVar(value=translations[language]['multiboot_Calibration']),

                   ttk.StringVar(value=translations[language]['multiboot_Calibration']),
                   ttk.StringVar(value=translations[language]['multiboot_Calibration']),
                   ttk.StringVar(value=translations[language]['multiboot_Calibration']),
                   ttk.StringVar(value=translations[language]['multiboot_Calibration'])
                    ]
tvar_eeprom = [ttk.StringVar(value=translations[language]['multiboot_Load_file']),
               ttk.StringVar(value=translations[language]['multiboot_Load_file']),
               ttk.StringVar(value=translations[language]['multiboot_Load_file']),
               ttk.StringVar(value=translations[language]['multiboot_Load_file'])
               ]


#Центрирует окно на экране.
def center_window(window):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

#Создает заставку перед основным приложением.
def splash_screen(main_app):

    splash = ttk.Toplevel()
    splash.overrideredirect(True)  # Убираем оконные границы
    #splash.geometry("400x300")  # Размер окна заставки
    # Загружаем изображение
    image = Image.open(os.getcwd()+'/resources/open.png')
    #image = image.resize((400, 300), Image.ANTIALIAS)  # Подгоняем под размер окна
    photo = ImageTk.PhotoImage(image)
    label = ttk.Label(splash, image=photo)
    label.image = photo  # Сохраняем ссылку на изображение
    label.pack()
    # Центрируем окно
    center_window(splash)
    # Показ заставки на 3 секунды
    splash.update()
    time.sleep(2)
    splash.destroy()  # Закрываем заставку
    main_app.deiconify()  # Показываем основное окно

#Операции при закрытии окна:
def on_closing():
    #Очистка временных файлов
    tempfolder=os.getcwd()+'/temp'
    if (os.path.isdir(tempfolder)):
        shutil.rmtree(tempfolder)
    #Сохранение настроек в файл конфига
    config['Settings']['theme'] = style.theme.name
    config['Settings']['language'] = language.name
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    #Уничтожение окна
    multiboot_window.destroy()

#Обработчик смены темы
def change_theme(_, theme_combo: ttk.Combobox):
    t = theme_combo.get()
    style.theme_use(t)
    theme_combo.selection_clear()

#Обработчик смены языка
def change_language(_, language_combo: ttk.Combobox):
    global language
    language = LanguageType.find_value(language_combo.get())
    if language == LanguageType.SIMPLIFIED_CHINESE:
        Messagebox.show_info('语言设置已更改为"简体中文"\n请在当前操作完成后手动重启此程序以应用更改',translations[language]['Info'])
    elif language == LanguageType.ENGLISH:
        Messagebox.show_info('Language setting has been changed to "English"\nPlease manually restart this program after the current operation is completed to apply the changes',translations[language]['Info'])
    else:
        Messagebox.show_info('Язык изменён на "Русский"\nПожалуйста, перезапустите эту программу вручную после завершения текущей операции, чтобы применить изменения.',translations[language]['Info'])

#Обработчик сброса ячейки
def Reset_handler(tab, partition,tvarindex):
    Reset(tab,partition)
    tvar_FW_name[tvarindex].set(multiboot_global.names[tab-1,partition-1,0])
    tvar_FW_button[tvarindex].set(translations[language]['multiboot_Firmware'])
    tvar_CFG_button[tvarindex].set(translations[language]['multiboot_Configuration'])
    tvar_CAL_button[tvarindex].set(translations[language]['multiboot_Calibration'])
    #если есть предзагруженный ЕЕПРОМ, то вычищаем ячейку, формируя файлы пустышки
    if os.path.isfile(os.getcwd()+'/temp/tab'+str(tab)+'/EEPROM_preloaded.bin'):
        tvar_FW_button[tvarindex].set(translations[language]['multiboot_cleared'])
        tvar_CFG_button[tvarindex].set(translations[language]['multiboot_cleared'])
        tvar_CAL_button[tvarindex].set(translations[language]['multiboot_cleared'])
        multiboot_global.FW_sizes[tab,partition]=0

#Функция сброса вкладки
def Reset_tab(tab):
    if tab==1:
        partitions=[1,2,3]
    elif tab==2:
        partitions=[1,2,3,4]
    elif tab==3:
        partitions=[1,2,3,4,5,6]
    else:
        partitions=[1,2,3,4]

    for partition in partitions:
        Reset(tab,partition)
        if tab==1:
            tvarindex=partition-1
        elif tab==2:
            tvarindex=3+partition-1
        elif tab==3:
            tvarindex=7+partition-1
        else:
            tvarindex=13+partition-1

        tvar_FW_name[tvarindex].set(multiboot_global.names[tab-1,partition-1,0])
        tvar_FW_button[tvarindex].set(translations[language]['multiboot_Firmware'])
        tvar_CFG_button[tvarindex].set(translations[language]['multiboot_Configuration'])
        tvar_CAL_button[tvarindex].set(translations[language]['multiboot_Calibration'])
    
    multiboot_global.FW_sizes[tab-1,:] = 0

#Обработчик сброса вкладки
def Reset_EEPROM_handler(tab):
    tvar_eeprom[tab-1].set(translations[language]['multiboot_Load_file'])
    filename = os.getcwd()+'/temp/tab'+str(tab)+'/EEPROM_preloaded.bin'
    if os.path.isfile(filename):
        os.remove(filename)
    Reset_tab(tab)

#Обработчик открытия файла
def Fileopen_handler(tab, partition, filetype, tvarindex):
    Open_file(tab, partition, filetype)
    if multiboot_global.file_path=='':
        if filetype==1:
            (tvar_FW_button[tvarindex]).set(multiboot_global.names[tab-1,partition-1,filetype])
        elif filetype==2:
            (tvar_CFG_button[tvarindex]).set(multiboot_global.names[tab-1,partition-1,filetype])
        else:
            (tvar_CAL_button[tvarindex]).set(multiboot_global.names[tab-1,partition-1,filetype])
        
    else:
        if filetype==1:
            tvar_FW_name[tvarindex].set(((multiboot_global.file_path).split("/")[-1])[:13])
            (tvar_FW_button[tvarindex]).set((multiboot_global.file_path).split("/")[-1])
        elif filetype==2:
            (tvar_CFG_button[tvarindex]).set((multiboot_global.file_path).split("/")[-1])
        else:
            (tvar_CAL_button[tvarindex]).set((multiboot_global.file_path).split("/")[-1])
            
#Обработчик предзагрузки ЕЕПРОМ
def LoadEEPROM_handler(tab):

    eeprom_data=Load_EEPROM(tab)
    #сброс всех ячеек
    Reset_tab(tab)
    #если не загрузился файл
    if multiboot_global.file_path=='':
        (tvar_eeprom[tab-1]).set(translations[language]['multiboot_Load_file'])
    else:
        (tvar_eeprom[tab-1]).set((multiboot_global.file_path).split("/")[-1])
        #здесь нужно организовать проверку содержимого файла EEPROM 

        # если есть хоть немного данных по адресам в зависимости от вкладки
        # то помечаем надписи на кнопках "занято"
        #tvar[tvarindex+1].set(translations[language]['multiboot_occupied'])
        #tvar[tvarindex+2].set(translations[language]['multiboot_occupied'])
        if tab == 1:
            fws=[0,1,2]
            for fw in fws:
                name_bytes=eeprom_data[0xFFA0+32*fw:0xFFA0+32*fw+13]
                tvar_FW_name[fw].set(byte_seq_to_string(name_bytes))
                tvar_FW_button[fw].set(translations[language]['multiboot_occupied'])
        elif tab == 2:
            fws=[3,4,5,6]
            for fw in fws:
                name_bytes=eeprom_data[0x40020+32*fw:0x40020+32*fw+13]
                tvar_FW_name[fw].set(byte_seq_to_string(name_bytes))
                tvar_FW_button[fw].set(translations[language]['multiboot_occupied'])
        elif tab == 3:
            fws=[7,8,9,10,11,12]
            for fw in fws:
                name_bytes=eeprom_data[0x22F40+32*fw:0x22F40+32*fw+13]
                tvar_FW_name[fw].set(byte_seq_to_string(name_bytes))
                tvar_FW_button[fw].set(translations[language]['multiboot_occupied'])
        else:
            fws=[13,14,15,16]
            for fw in fws:
                name_bytes=eeprom_data[0x40020+32*fw:0x40020+32*fw+13]
                tvar_FW_name[fw].set(byte_seq_to_string(name_bytes))
                tvar_FW_button[fw].set(translations[language]['multiboot_occupied'])
    
    #Флаг о том что еепром не новый            
    multiboot_global.is_new=False

#Сохранить имена прошивок в глобальные переменные
def NamesToGlobal(tab):
    if tab == 1:
        multiboot_global.names[0,0,0] = tvar_FW_name[0].get()
        multiboot_global.names[0,1,0] = tvar_FW_name[1].get()
        multiboot_global.names[0,2,0] = tvar_FW_name[2].get()
    elif tab == 2:
        multiboot_global.names[1,0,0] = tvar_FW_name[3].get()
        multiboot_global.names[1,1,0] = tvar_FW_name[4].get()
        multiboot_global.names[1,2,0] = tvar_FW_name[5].get()
        multiboot_global.names[1,3,0] = tvar_FW_name[6].get()
    elif tab == 3:
        multiboot_global.names[2,0,0] = tvar_FW_name[7].get()
        multiboot_global.names[2,1,0] = tvar_FW_name[8].get()
        multiboot_global.names[2,2,0] = tvar_FW_name[9].get()
        multiboot_global.names[2,3,0] = tvar_FW_name[10].get()    
        multiboot_global.names[2,4,0] = tvar_FW_name[11].get()
        multiboot_global.names[2,5,0] = tvar_FW_name[12].get()
    else:
        multiboot_global.names[3,0,0] = tvar_FW_name[13].get()
        multiboot_global.names[3,1,0] = tvar_FW_name[14].get()
        multiboot_global.names[3,2,0] = tvar_FW_name[15].get()
        multiboot_global.names[3,3,0] = tvar_FW_name[16].get()

#Сохранить файлик ЕЕПРОМ
def Save_EEPROM(tab):
    NamesToGlobal(tab)
    file_path=os.getcwd()+'/temp/tab'+str(tab)+'/EEPROM_final.bin'
    if (os.path.isfile(file_path)):
        with open(file_path, 'rb') as fp:
            eeprom_data = fp.read()
    else:
        eeprom_data=Make_EEPROM(tab)
    file_path = filedialog.asksaveasfilename(defaultextension=".bin", filetypes=[("Binary files", "*.bin"), ("All files", "*.*")])
    if not file_path:
            Messagebox.show_info(translations[language]['Canceled'], translations[language]['Error'])
            return
    with open(file_path, 'wb') as fp:
        fp.write(eeprom_data)

    Messagebox.show_info(translations[language]['multiboot_saved'], translations[language]['Success'])

#Записть ЕЕПРОМ в рацию
def Write_EEPROM(tab, serial_port_text: str, window, progress: ttk.Progressbar, eeprom_size: int):
    NamesToGlobal(tab)
    file_path=os.getcwd()+'/temp/tab'+str(tab)+'/EEPROM_final.bin'
    if (os.path.isfile(file_path)):
        with open(file_path, 'rb') as fp:
            eeprom_data = fp.read()
    else:
        eeprom_data=Make_EEPROM(tab)
    if len(serial_port_text) == 0:
        Messagebox.show_error(translations[language]['COM_NONE'], translations[language]['Error'])
        return

    start_addr = 0x0
    if eeprom_size > 0:
        target_eeprom_offset = 0x20000 * eeprom_size
    else:
        target_eeprom_offset = 0x2000

    if len(eeprom_data) != target_eeprom_offset:
        if Messagebox.yesno(translations[language]['Incompatible_1'] + str(len(eeprom_data)) + translations[language]['Incompatible_2'] + str(target_eeprom_offset) + translations[language]['Incompatible_3'], translations[language]['Info']) == 'No':
            Messagebox.show_info(translations[language]['Canceled'], translations[language]['Info'])
            return

    with serial.Serial(serial_port_text, 38400, timeout=2) as serial_port:
        serial_check = check_serial_port(serial_port, False)
        if not serial_check.status:
            Messagebox.show_error(serial_check.message, translations[language]['Error'])
            return
        # Прячем основное окно до окончания заставки
        #multiboot_window.withdraw()
        Messagebox.show_info(translations[language]['multiboot_write_start'], translations[language]['Info'])
        write_data(serial_port, start_addr, eeprom_data, progress, window)
        #serial_utils.reset_radio(serial_port)
        if Messagebox.yesno(translations[language]['multiboot_write_done'], translations[language]['Info']) == 'Yes':
            Save_EEPROM(tab)
        else:
            return
        #multiboot_window.deiconify()  # Показываем основное окно

#Разбролировка интерфейса        
def enable(childList):
    for child in childList:
        child.configure(state='normal')

def disable(childList):
    for child in childList:
        child.configure(state='disabled')



#Графический интерфейс
def multiboot():
    multiboot_window.title(f"{translations[language]['multiboot_tool_name']} v{multiboot_version}")
    multiboot_window.geometry('700x850')
    multiboot_window.resizable(False, False)


    def check_files():
        while True:
            #Проверка первой вкладки
            if (os.path.isdir(os.getcwd()+'/temp/tab1')) and (os.path.isfile(os.getcwd()+'/temp/tab1/FW1.bin')):
                enable(tab1_FW2.winfo_children())
                if (os.path.isfile(os.getcwd()+'/temp/tab1/FW2.bin')):
                    enable(tab1_FW3.winfo_children())
                else:
                    disable(tab1_FW3.winfo_children())
                    Reset_handler(1,3,2)
            else:
                disable(tab1_FW2.winfo_children())
                Reset_handler(1,2,1)
                disable(tab1_FW3.winfo_children())
                Reset_handler(1,3,2)

            #Проверка второй вкладки
            
            if (os.path.isdir(os.getcwd()+'/temp/tab2')) and (os.path.isfile(os.getcwd()+'/temp/tab2/FW1.bin')):
                enable(tab2_FW2.winfo_children())
                if (os.path.isfile(os.getcwd()+'/temp/tab2/FW2.bin')):
                    enable(tab2_FW3.winfo_children())
                    if (os.path.isfile(os.getcwd()+'/temp/tab2/FW3.bin')):
                        enable(tab2_FW4.winfo_children())
                    else:
                        disable(tab2_FW4.winfo_children())
                        Reset_handler(2,4,6)
                else:
                    disable(tab2_FW3.winfo_children())
                    Reset_handler(2,3,5)
                    disable(tab2_FW4.winfo_children())
                    Reset_handler(2,4,6)

            else:
                disable(tab2_FW2.winfo_children())
                Reset_handler(2,2,4)
                disable(tab2_FW3.winfo_children())
                Reset_handler(2,3,5)
                disable(tab2_FW4.winfo_children())
                Reset_handler(2,4,6)

            #Проверка третьей вкладки

            if (os.path.isdir(os.getcwd()+'/temp/tab3')) and (os.path.isfile(os.getcwd()+'/temp/tab3/FW1.bin')):
                enable(tab3_FW2.winfo_children())
                if (os.path.isfile(os.getcwd()+'/temp/tab3/FW2.bin')):
                    enable(tab3_FW3.winfo_children())
                    if (os.path.isfile(os.getcwd()+'/temp/tab3/FW3.bin')):
                        enable(tab3_FW4.winfo_children())
                        if (os.path.isfile(os.getcwd()+'/temp/tab3/FW4.bin')):
                            enable(tab3_FW5.winfo_children())
                            if (os.path.isfile(os.getcwd()+'/temp/tab3/FW5.bin')):
                                enable(tab3_FW6.winfo_children())
                            else:
                                disable(tab3_FW6.winfo_children())
                                Reset_handler(3,6,12)
                        else:
                            disable(tab3_FW5.winfo_children())
                            Reset_handler(3,5,11)
                            disable(tab3_FW6.winfo_children())
                            Reset_handler(3,6,12)
                    else:
                        disable(tab3_FW4.winfo_children())
                        Reset_handler(3,4,10)
                        disable(tab3_FW5.winfo_children())
                        Reset_handler(3,5,11)
                        disable(tab3_FW6.winfo_children())
                        Reset_handler(3,6,12)
                else:
                    disable(tab3_FW3.winfo_children())
                    Reset_handler(3,3,9)
                    disable(tab3_FW4.winfo_children())
                    Reset_handler(3,4,10)
                    disable(tab3_FW5.winfo_children())
                    Reset_handler(3,5,11)
                    disable(tab3_FW6.winfo_children())
                    Reset_handler(3,6,12)

            else:
                disable(tab3_FW2.winfo_children())
                Reset_handler(3,2,8)
                disable(tab3_FW3.winfo_children())
                Reset_handler(3,3,9)
                disable(tab3_FW4.winfo_children())
                Reset_handler(3,4,10)
                disable(tab3_FW5.winfo_children())
                Reset_handler(3,5,11)
                disable(tab3_FW6.winfo_children())
                Reset_handler(3,6,12)

            #Проверка четвертой вкладки
            
            if (os.path.isdir(os.getcwd()+'/temp/tab4')) and (os.path.isfile(os.getcwd()+'/temp/tab4/FW1.bin')):
                tab4_FW2_FWButton.configure(state='normal')
                tab4_FW2_FWName.configure(state='normal')
                tab4_FW2_RESETButton.configure(state='normal')
                if (os.path.isfile(os.getcwd()+'/temp/tab4/FW2.bin')):
                    tab4_FW3_FWButton.configure(state='normal')
                    tab4_FW3_FWName.configure(state='normal')
                    tab4_FW3_RESETButton.configure(state='normal')
                    if (os.path.isfile(os.getcwd()+'/temp/tab4/FW3.bin')):
                        tab4_FW4_FWButton.configure(state='normal')
                        tab4_FW4_FWName.configure(state='normal')
                        tab4_FW4_RESETButton.configure(state='normal')
                    else:
                        tab4_FW4_FWButton.configure(state='disable')
                        tab4_FW4_FWName.configure(state='disable')
                        tab4_FW4_RESETButton.configure(state='disable')
                        Reset_handler(4,4,16) 
                else:
                    tab4_FW3_FWButton.configure(state='disable')
                    tab4_FW3_FWName.configure(state='disable')
                    tab4_FW3_RESETButton.configure(state='disable')
                    Reset_handler(4,3,15) 
                    tab4_FW4_FWButton.configure(state='disable')
                    tab4_FW4_FWName.configure(state='disable')
                    tab4_FW4_RESETButton.configure(state='disable')
                    Reset_handler(4,4,16) 
            else:
                tab4_FW2_FWButton.configure(state='disable')
                tab4_FW2_FWName.configure(state='disable')
                tab4_FW2_RESETButton.configure(state='disable')
                Reset_handler(4,2,14)
                tab4_FW3_FWButton.configure(state='disable')
                tab4_FW3_FWName.configure(state='disable')
                tab4_FW3_RESETButton.configure(state='disable')   
                Reset_handler(4,3,15) 
                tab4_FW4_FWButton.configure(state='disable')
                tab4_FW4_FWName.configure(state='disable')
                tab4_FW4_RESETButton.configure(state='disable')
                Reset_handler(4,4,16) 

            time.sleep(1)

    # Центрируем окно при запуске
    center_window(multiboot_window)

    # Прячем основное окно до окончания заставки
    multiboot_window.withdraw()

    # Показываем заставку
    splash_screen(multiboot_window)

    multiboot_window.protocol('WM_DELETE_WINDOW', on_closing)

    frame0 = ttk.Frame(multiboot_window, padding=10)
    frame0.pack(side=TOP)
    Warning_label = ttk.Label(frame0, text=translations[language]['multiboot_warning_text'])
    Warning_label.pack(side=LEFT, padx=10)
    FAQ_Button = ttk.Button(frame0, text=translations[language]['multiboot_FAQ_text'], width=10, command=lambda: FAQ())
    FAQ_Button.pack(side=RIGHT)
    
    frame01 = ttk.ttk.Labelframe(multiboot_window, text=translations[language]['multiboot_EEPROM_operations'], padding=10)
    frame01.pack(side=TOP, padx=5, fill=X )

    frame02 = ttk.Frame(frame01, padding=0)
    frame02.pack(side=TOP, fill=X)
    theme_combo = ttk.Combobox(frame02, width=10, state='readonly', values=style.theme_names())
    theme_combo.current(style.theme_names().index(style.theme.name))
    theme_combo.pack(side=RIGHT,  expand=YES)
    theme_combo.bind('<<ComboboxSelected>>',lambda event: change_theme(event, theme_combo))
    theme_label = ttk.Label(frame02, text=translations[language]['theme_label_text'])
    theme_label.pack(side=RIGHT, expand=YES)
    language_combo = ttk.Combobox(frame02, width=10, state='readonly', values=LanguageType.value_list())
    language_combo.current(LanguageType.value_list().index(language.value))
    language_combo.pack(side=RIGHT, expand=YES)
    language_combo.bind('<<ComboboxSelected>>',lambda event: change_language(event, language_combo))
    language_label = ttk.Label(frame02, text='Language')
    language_label.pack(side=RIGHT)
    serial_port_label = ttk.Label(frame02, text=translations[language]['serial_port_text'])
    serial_port_label.pack(side=LEFT, expand=YES)
    serial_port_combo = ttk.Combobox(frame02, values=[], width=10, state='readonly')
    serial_port_combo['postcommand'] = lambda: serial_port_combo_postcommand(serial_port_combo)
    serial_port_combo.bind('<<ComboboxSelected>>',lambda event: serial_port_combo_callback(event, serial_port_combo.get(), eeprom_size_combo))
    serial_port_combo.pack(side=LEFT, expand=YES)
    eeprom_size_label = ttk.Label(frame02, text='EEPROM')
    eeprom_size_label.pack(side=LEFT)
    eeprom_size_combo = ttk.Combobox(frame02, values=EEPROM_SIZE, width=10, state='readonly')
    eeprom_size_combo.pack(side=LEFT, expand=YES)

    frame03 = ttk.Frame(frame01, padding=5)
    frame03.pack(side=TOP, fill=X)
    backup_eeprom_button = ttk.Button(frame03, width=22, text=translations[language]['backup_eeprom_button_text'], command=lambda:backup_eeprom(serial_port_combo.get(), multiboot_window, progress, EEPROM_SIZE.index(eeprom_size_combo.get())) )
    backup_eeprom_button.pack(side=LEFT, expand=YES, pady=1)   
    restore_eeprom_button = ttk.Button(frame03, width=22, text=translations[language]['restore_eeprom_button_text'], command=lambda:restore_eeprom(serial_port_combo.get(), multiboot_window, progress,EEPROM_SIZE.index(eeprom_size_combo.get())))
    restore_eeprom_button.pack(side=LEFT, expand=YES, pady=1) 
    clean_eeprom_button = ttk.Button(frame03, width=22, text=translations[language]['clean_eeprom_button_text'], command=lambda: clean_eeprom(serial_port_combo.get(), multiboot_window, progress, EEPROM_SIZE.index(eeprom_size_combo.get())))
    clean_eeprom_button.pack(side=LEFT, expand=YES, pady=1) 
    reset_radio_button = ttk.Button(frame03, width=22, text=translations[language]['reset_radio_text'], command=lambda: reset_radio(serial_port_combo.get()))
    reset_radio_button.pack(side=LEFT, expand=YES, pady=1) 

    frame04=ttk.Frame(frame01, padding=5)
    frame04.pack(side=TOP,fill=X)
    progress = ttk.Progressbar(frame04, orient='horizontal', mode='determinate', bootstyle=(SUCCESS, STRIPED))
    progress.pack(side=TOP, padx=0, pady=(0), expand=YES, fill=X)

    frame1 = ttk.Frame(multiboot_window, padding=5)
    frame1.pack(side=TOP, fill=X)
    #виджет вкладок
    notebook = ttk.Notebook(frame1)
    notebook.pack(side=LEFT,fill=X)
   
    #ВКЛАДКА1
    tab1=ttk.Frame(notebook, padding=5)
    tab1.pack(side=TOP,fill=X)
    tab1_label = ttk.Label(tab1, font="-size 10 -weight bold", text=translations[language]['multiboot_3_warninginfo_text'])
    tab1_label.pack(side=TOP, padx=10, fill=X)
    ttk.Separator(tab1).pack(fill=X, padx=10, pady=10)
    tab1_FW_config = ttk.Labelframe(tab1, text=translations[language]['multiboot_FW_config_info_1'], padding=(5))
    tab1_FW_config.pack(fill=X, side=TOP, padx=0)
    tab1_FW_info = ttk.Label(tab1_FW_config, text=translations[language]['multiboot_FW_config_info_2'], padding=(0))
    tab1_FW_info.pack(fill=X, side=TOP, padx=10, pady=5)

    tab1_FW_config_sub=ttk.Frame(tab1_FW_config, padding=0)
    tab1_FW_config_sub.pack(side=TOP,fill=BOTH, expand=YES)
    tab1_FW1=ttk.Labelframe(tab1_FW_config_sub, text=translations[language]['multiboot_Partition']+' 1', padding=5)
    tab1_FW1.pack(side=LEFT,fill=X, expand=YES)
    tab1_FW1_FWButton = ttk.Button(tab1_FW1, textvariable=tvar_FW_button[0], width=15, command=lambda: Fileopen_handler(1, 1, 1, 0))
    tab1_FW1_FWButton.pack(side=TOP, pady=1)
    tab1_FW1_CFGButton = ttk.Button(tab1_FW1, textvariable=tvar_CFG_button[0], width=15, command=lambda: Fileopen_handler(1, 1, 2, 0))
    tab1_FW1_CFGButton.pack(side=TOP, pady=1)
    tab1_FW1_CALButton = ttk.Button(tab1_FW1, textvariable=tvar_CAL_button[0], width=15, command=lambda: Fileopen_handler(1, 1, 3, 0))
    tab1_FW1_CALButton.pack(side=TOP, pady=1)
    tab1_FW1_FWName = ttk.Entry(tab1_FW1, width=15, textvariable=tvar_FW_name[0])
    tab1_FW1_FWName.pack(fill=X, pady=3)
    tab1_FW1_RESETButton = ttk.Button(tab1_FW1, text=translations[language]['multiboot_Reset'], width=15, bootstyle=(DANGER), command=lambda: Reset_handler(1, 1, 0))
    tab1_FW1_RESETButton.pack(side=TOP, pady=1)

    tab1_FW2=ttk.Labelframe(tab1_FW_config_sub, text=translations[language]['multiboot_Partition']+' 2',  padding=5)
    tab1_FW2.pack(side=LEFT,fill=X, expand=YES)
    tab1_FW2_FWButton = ttk.Button(tab1_FW2, textvariable=tvar_FW_button[1], width=15, command=lambda: Fileopen_handler(1, 2, 1, 1))
    tab1_FW2_FWButton.pack(side=TOP, pady=1)
    tab1_FW2_CFGButton = ttk.Button(tab1_FW2, textvariable=tvar_CFG_button[1], width=15, command=lambda: Fileopen_handler(1, 2, 2, 1))
    tab1_FW2_CFGButton.pack(side=TOP, pady=1)
    tab1_FW2_CALButton = ttk.Button(tab1_FW2, textvariable=tvar_CAL_button[1], width=15, command=lambda: Fileopen_handler(1, 2, 3, 1))
    tab1_FW2_CALButton.pack(side=TOP, pady=1)
    tab1_FW2_FWName = ttk.Entry(tab1_FW2, width=15, textvariable=tvar_FW_name[1])
    tab1_FW2_FWName.pack(fill=X, pady=3)
    tab1_FW2_RESETButton = ttk.Button(tab1_FW2, text=translations[language]['multiboot_Reset'], width=15, bootstyle=(DANGER), command=lambda: Reset_handler(1, 2, 1))
    tab1_FW2_RESETButton.pack(side=TOP, pady=1)

    tab1_FW3=ttk.Labelframe(tab1_FW_config_sub, text=translations[language]['multiboot_Partition']+' 3', padding=5)
    tab1_FW3.pack(side=LEFT,fill=X, expand=YES)
    tab1_FW3_FWButton = ttk.Button(tab1_FW3, textvariable=tvar_FW_button[2], width=15, command=lambda: Fileopen_handler(1, 3, 1, 2))
    tab1_FW3_FWButton.pack(side=TOP, pady=1)
    tab1_FW3_CFGButton = ttk.Button(tab1_FW3, textvariable=tvar_CFG_button[2], width=15, command=lambda: Fileopen_handler(1, 3, 2, 2))
    tab1_FW3_CFGButton.pack(side=TOP, pady=1)
    tab1_FW3_CALButton = ttk.Button(tab1_FW3, textvariable=tvar_CAL_button[2], width=15, command=lambda: Fileopen_handler(1, 3, 3, 2))
    tab1_FW3_CALButton.pack(side=TOP, pady=1)
    tab1_FW3_FWName = ttk.Entry(tab1_FW3, width=15, textvariable=tvar_FW_name[2])
    tab1_FW3_FWName.pack(fill=X, pady=3)
    tab1_FW3_RESETButton = ttk.Button(tab1_FW3, text=translations[language]['multiboot_Reset'], width=15, bootstyle=(DANGER), command=lambda: Reset_handler(1, 3, 2))
    tab1_FW3_RESETButton.pack(side=TOP, pady=1)

    #ВЫВОД
    tab1_OUT=ttk.Labelframe(tab1_FW_config_sub, text=translations[language]['multiboot_Output'], padding=5)
    tab1_OUT.pack(side=RIGHT,fill=BOTH, expand=YES)
    #tab1_LoadButton = ttk.Button(tab1_OUT, textvariable=tvar_eeprom[0], width=20, bootstyle=(INFO), command=lambda: LoadEEPROM_handler(1))
    #tab1_LoadButton.pack(side=TOP, pady=1)
    tab1_FILEButton = ttk.Button(tab1_OUT, text=translations[language]['multiboot_Save_to_file'], width=20, bootstyle=(SUCCESS), command=lambda: Save_EEPROM(1))
    tab1_FILEButton.pack(side=TOP, pady=1)
    tab1_OUTButton = ttk.Button(tab1_OUT, text=translations[language]['multiboot_Write_to_EEPROM'], width=20, bootstyle=(DANGER), command=lambda: Write_EEPROM(1, serial_port_combo.get(), multiboot_window, tab1_progress, EEPROM_SIZE.index(eeprom_size_combo.get())))
    tab1_OUTButton.pack(side=TOP, pady=1) 
    tab1_OUT_RESETButton = ttk.Button(tab1_OUT, text=translations[language]['multiboot_Reset_all'], width=20, bootstyle=(DANGER), command=lambda: Reset_EEPROM_handler(1))
    tab1_OUT_RESETButton.pack(side=BOTTOM, pady=1)

    tab1_progress = ttk.Progressbar(tab1_FW_config, orient='horizontal', mode='determinate', bootstyle=(SUCCESS, STRIPED))
    tab1_progress.pack(side=TOP, padx=0, pady=(10), expand=YES, fill=X)

    #БАЗОВЫЙ ЗАГРУЗЧИК
    tab1_BASEBOOT = ttk.Labelframe(tab1, text=translations[language]['multiboot_BASEBOOT_info'], padding=(10))
    tab1_BASEBOOT.pack(fill=X, side=TOP, pady=10)
    tab1_BASEBOOT_Flash_button = ttk.Button(tab1_BASEBOOT, text=translations[language]['multiboot_Flash']+' BASE_BOOTLOADER_3.bin', width=50, bootstyle=(DANGER), command=lambda: execute('R9OOT_BASE_BOOTLOADER_3.bat'))
    tab1_BASEBOOT_Flash_button.pack(side=LEFT, pady=1, expand=YES)
    tab1_BASEBOOT_Rollback_button = ttk.Button(tab1_BASEBOOT, text=translations[language]['multiboot_Rollback']+' qs_bl.bin', width=50, bootstyle=(WARNING), command=lambda: execute('qs_bl.bat'))
    tab1_BASEBOOT_Rollback_button.pack(side=RIGHT, pady=1, expand=YES) 

    notebook.add(
        tab1, 
        text=translations[language]['multiboot_tab_1'], 
        sticky=NW)
    





    #ВКЛАДКА2
    tab2=ttk.Frame(notebook, padding=5)
    tab2.pack(side=TOP,fill=X)
    tab2_label = ttk.Label(tab2, font="-size 10 -weight bold", text=translations[language]['multiboot_4_warninginfo_text'])
    tab2_label.pack(side=TOP, padx=10, fill=X)
    ttk.Separator(tab2).pack(fill=X, padx=10, pady=10)
    tab2_FW_config = ttk.Labelframe(tab2, text=translations[language]['multiboot_FW_config_info_1'], padding=(5))
    tab2_FW_config.pack(fill=X, side=TOP, padx=0)
    tab2_FW_info = ttk.Label(tab2_FW_config, text=translations[language]['multiboot_FW_config_info_2'], padding=(0))
    tab2_FW_info.pack(fill=X, side=TOP, padx=10, pady=5)

    tab2_FW_config_sub=ttk.Frame(tab2_FW_config, padding=0)
    tab2_FW_config_sub.pack(side=TOP,fill=BOTH, expand=YES)
    tab2_FW1=ttk.Labelframe(tab2_FW_config_sub, text=translations[language]['multiboot_Partition']+' 1', padding=5)
    tab2_FW1.pack(side=LEFT,fill=X, expand=YES)
    tab2_FW1_FWButton = ttk.Button(tab2_FW1, textvariable=tvar_FW_button[3], width=15, command=lambda: Fileopen_handler(2, 1, 1, 3))
    tab2_FW1_FWButton.pack(side=TOP, pady=1)
    tab2_FW1_CFGButton = ttk.Button(tab2_FW1, textvariable=tvar_CFG_button[3], width=15, command=lambda: Fileopen_handler(2, 1, 2, 3))
    tab2_FW1_CFGButton.pack(side=TOP, pady=1)
    tab2_FW1_CALButton = ttk.Button(tab2_FW1, textvariable=tvar_CAL_button[3], width=15, command=lambda: Fileopen_handler(2, 1, 3, 3))
    tab2_FW1_CALButton.pack(side=TOP, pady=1)
    tab2_FW1_FWName = ttk.Entry(tab2_FW1, width=15, textvariable=tvar_FW_name[3])
    tab2_FW1_FWName.pack(fill=X, pady=3)
    tab2_FW1_RESETButton = ttk.Button(tab2_FW1, text=translations[language]['multiboot_Reset'], width=15, bootstyle=(DANGER), command=lambda: Reset_handler(2, 1, 3))
    tab2_FW1_RESETButton.pack(side=TOP, pady=1)

    tab2_FW2=ttk.Labelframe(tab2_FW_config_sub, text=translations[language]['multiboot_Partition']+' 2',  padding=5)
    tab2_FW2.pack(side=LEFT,fill=X, expand=YES)
    tab2_FW2_FWButton = ttk.Button(tab2_FW2, textvariable=tvar_FW_button[4], width=15, command=lambda: Fileopen_handler(2, 2, 1, 4))
    tab2_FW2_FWButton.pack(side=TOP, pady=1)
    tab2_FW2_CFGButton = ttk.Button(tab2_FW2, textvariable=tvar_CFG_button[4], width=15, command=lambda: Fileopen_handler(2, 2, 2, 4))
    tab2_FW2_CFGButton.pack(side=TOP, pady=1)
    tab2_FW2_CALButton = ttk.Button(tab2_FW2, textvariable=tvar_CAL_button[4], width=15, command=lambda: Fileopen_handler(2, 2, 3, 4))
    tab2_FW2_CALButton.pack(side=TOP, pady=1)
    tab2_FW2_FWName = ttk.Entry(tab2_FW2, width=15, textvariable=tvar_FW_name[4])
    tab2_FW2_FWName.pack(fill=X, pady=3)
    tab2_FW2_RESETButton = ttk.Button(tab2_FW2, text=translations[language]['multiboot_Reset'], width=15, bootstyle=(DANGER), command=lambda: Reset_handler(2, 2, 4))
    tab2_FW2_RESETButton.pack(side=TOP, pady=1)

    tab2_FW3=ttk.Labelframe(tab2_FW_config_sub, text=translations[language]['multiboot_Partition']+' 3', padding=5)
    tab2_FW3.pack(side=LEFT,fill=X, expand=YES)
    tab2_FW3_FWButton = ttk.Button(tab2_FW3, textvariable=tvar_FW_button[5], width=15, command=lambda: Fileopen_handler(2, 3, 1, 5))
    tab2_FW3_FWButton.pack(side=TOP, pady=1)
    tab2_FW3_CFGButton = ttk.Button(tab2_FW3, textvariable=tvar_CFG_button[5], width=15, command=lambda: Fileopen_handler(2, 3, 2, 5))
    tab2_FW3_CFGButton.pack(side=TOP, pady=1)
    tab2_FW3_CALButton = ttk.Button(tab2_FW3, textvariable=tvar_CAL_button[5], width=15, command=lambda: Fileopen_handler(2, 3, 3, 5))
    tab2_FW3_CALButton.pack(side=TOP, pady=1)
    tab2_FW3_FWName = ttk.Entry(tab2_FW3, width=15, textvariable=tvar_FW_name[5])
    tab2_FW3_FWName.pack(fill=X, pady=3)
    tab2_FW3_RESETButton = ttk.Button(tab2_FW3, text=translations[language]['multiboot_Reset'], width=15, bootstyle=(DANGER), command=lambda: Reset_handler(2, 3, 5))
    tab2_FW3_RESETButton.pack(side=TOP, pady=1)

    tab2_FW4=ttk.Labelframe(tab2_FW_config_sub, text=translations[language]['multiboot_Partition']+' 4', padding=5)
    tab2_FW4.pack(side=LEFT,fill=X, expand=YES)
    tab2_FW4_FWButton = ttk.Button(tab2_FW4, textvariable=tvar_FW_button[6], width=15, command=lambda: Fileopen_handler(2, 4, 1, 6))
    tab2_FW4_FWButton.pack(side=TOP, pady=1)
    tab2_FW4_CFGButton = ttk.Button(tab2_FW4, textvariable=tvar_CFG_button[6], width=15, command=lambda: Fileopen_handler(2, 4, 2, 6))
    tab2_FW4_CFGButton.pack(side=TOP, pady=1)
    tab2_FW4_CALButton = ttk.Button(tab2_FW4, textvariable=tvar_CAL_button[6], width=15, command=lambda: Fileopen_handler(2, 4, 3, 6))
    tab2_FW4_CALButton.pack(side=TOP, pady=1)
    tab2_FW4_FWName = ttk.Entry(tab2_FW4, width=15, textvariable=tvar_FW_name[6])
    tab2_FW4_FWName.pack(fill=X, pady=3)
    tab2_FW4_RESETButton = ttk.Button(tab2_FW4, text=translations[language]['multiboot_Reset'], width=15, bootstyle=(DANGER), command=lambda: Reset_handler(2, 4, 6))
    tab2_FW4_RESETButton.pack(side=TOP, pady=1)

    #2_ВЫВОД
    tab2_OUT=ttk.Labelframe(tab2_FW_config_sub, text=translations[language]['multiboot_Output'], padding=5)
    tab2_OUT.pack(side=RIGHT,fill=BOTH, expand=YES)
    #tab2_LoadButton = ttk.Button(tab2_OUT, textvariable=tvar_eeprom[1], width=20, bootstyle=(INFO), command=lambda: LoadEEPROM_handler(2))
    #tab2_LoadButton.pack(side=TOP, pady=1)
    tab2_FILEButton = ttk.Button(tab2_OUT, text=translations[language]['multiboot_Save_to_file'], width=20, bootstyle=(SUCCESS), command=lambda: Save_EEPROM(2))
    tab2_FILEButton.pack(side=TOP, pady=1)
    tab2_OUTButton = ttk.Button(tab2_OUT, text=translations[language]['multiboot_Write_to_EEPROM'], width=20, bootstyle=(DANGER), command=lambda: Write_EEPROM(2, serial_port_combo.get(), multiboot_window, tab2_progress, EEPROM_SIZE.index(eeprom_size_combo.get())))
    tab2_OUTButton.pack(side=TOP, pady=1)
    tab2_OUT_RESETButton = ttk.Button(tab2_OUT, text=translations[language]['multiboot_Reset_all'], width=20, bootstyle=(DANGER), command=lambda: Reset_EEPROM_handler(2))
    tab2_OUT_RESETButton.pack(side=BOTTOM, pady=1)

    tab2_progress = ttk.Progressbar(tab2_FW_config, orient='horizontal', mode='determinate', bootstyle=(SUCCESS, STRIPED))
    tab2_progress.pack(side=TOP, padx=0, pady=(10), expand=YES, fill=X)

    #2_БАЗОВЫЙ ЗАГРУЗЧИК
    tab2_BASEBOOT = ttk.Labelframe(tab2, text=translations[language]['multiboot_BASEBOOT_info'], padding=(10))
    tab2_BASEBOOT.pack(fill=X, side=TOP, pady=10)
    tab2_BASEBOOT_Flash_button = ttk.Button(tab2_BASEBOOT, text=translations[language]['multiboot_Flash']+' BASE_BOOTLOADER_4.bin', width=50, bootstyle=(DANGER), command=lambda: execute('R9OOT_BASE_BOOTLOADER_4.bat'))
    tab2_BASEBOOT_Flash_button.pack(side=LEFT, pady=1, expand=YES)
    tab2_BASEBOOT_Rollback_button = ttk.Button(tab2_BASEBOOT, text=translations[language]['multiboot_Rollback']+' qs_bl.bin', width=50, bootstyle=(WARNING), command=lambda: execute('qs_bl.bat'))
    tab2_BASEBOOT_Rollback_button.pack(side=RIGHT, pady=1, expand=YES)

    notebook.add(
        child=tab2, 
        text=translations[language]['multiboot_tab_2'], 
        sticky=NW)
    
    
    
    #ВКЛАДКА3
    tab3=ttk.Frame(notebook, padding=5)
    tab3.pack(side=TOP,fill=X)
    tab3_label = ttk.Label(tab3, font="-size 10 -weight bold", text=translations[language]['multiboot_6_warninginfo_text'])
    tab3_label.pack(side=TOP, padx=10, fill=X)
    ttk.Separator(tab3).pack(fill=X, padx=10, pady=10)
    tab3_FW_config = ttk.Labelframe(tab3, text=translations[language]['multiboot_FW_config_info_1'], padding=(5))
    tab3_FW_config.pack(fill=X, side=TOP, padx=0)
    tab3_FW_info = ttk.Label(tab3_FW_config, text=translations[language]['multiboot_FW_config_info_2'], padding=(0))
    tab3_FW_info.pack(fill=X, side=TOP, padx=10, pady=5)

    tab3_FW_config_upper_sub=ttk.Frame(tab3_FW_config, padding=0)
    tab3_FW_config_upper_sub.pack(side=TOP,fill=X, expand=YES)
    tab3_FW_config_sub=ttk.Frame(tab3_FW_config_upper_sub, padding=0)
    tab3_FW_config_sub.pack(side=LEFT,fill=X, expand=YES)

    tab3_FW_config_sub1=ttk.Frame(tab3_FW_config_sub, padding=0)
    tab3_FW_config_sub1.pack(side=TOP,fill=X, expand=YES)
    
    tab3_FW1=ttk.Labelframe(tab3_FW_config_sub1, text=translations[language]['multiboot_Partition']+' 1', padding=5)
    tab3_FW1.pack(side=LEFT,fill=X, expand=YES)
    tab3_FW1_FWButton = ttk.Button(tab3_FW1, textvariable=tvar_FW_button[7], width=15, command=lambda: Fileopen_handler(3, 1, 1, 7))
    tab3_FW1_FWButton.pack(side=TOP, pady=1)
    tab3_FW1_CFGButton = ttk.Button(tab3_FW1, textvariable=tvar_CFG_button[7], width=15, command=lambda: Fileopen_handler(3, 1, 2, 7))
    tab3_FW1_CFGButton.pack(side=TOP, pady=1)
    tab3_FW1_CALButton = ttk.Button(tab3_FW1, textvariable=tvar_CAL_button[7], width=15, command=lambda: Fileopen_handler(3, 1, 3, 7))
    tab3_FW1_CALButton.pack(side=TOP, pady=1)
    tab3_FW1_FWName = ttk.Entry(tab3_FW1, width=15, textvariable=tvar_FW_name[7])
    tab3_FW1_FWName.pack(fill=X, pady=3)
    tab3_FW1_RESETButton = ttk.Button(tab3_FW1, text=translations[language]['multiboot_Reset'], width=15, bootstyle=(DANGER), command=lambda: Reset_handler(3, 1, 7))
    tab3_FW1_RESETButton.pack(side=TOP, pady=1)

    tab3_FW2=ttk.Labelframe(tab3_FW_config_sub1, text=translations[language]['multiboot_Partition']+' 2',  padding=5)
    tab3_FW2.pack(side=LEFT,fill=X, expand=YES)
    tab3_FW2_FWButton = ttk.Button(tab3_FW2, textvariable=tvar_FW_button[8], width=15, command=lambda: Fileopen_handler(3, 2, 1, 8))
    tab3_FW2_FWButton.pack(side=TOP, pady=1)
    tab3_FW2_CFGButton = ttk.Button(tab3_FW2, textvariable=tvar_CFG_button[8], width=15, command=lambda: Fileopen_handler(3, 2, 2, 8))
    tab3_FW2_CFGButton.pack(side=TOP, pady=1)
    tab3_FW2_CALButton = ttk.Button(tab3_FW2, textvariable=tvar_CAL_button[8], width=15, command=lambda: Fileopen_handler(3, 2, 3, 8))
    tab3_FW2_CALButton.pack(side=TOP, pady=1)
    tab3_FW2_FWName = ttk.Entry(tab3_FW2, width=15, textvariable=tvar_FW_name[8])
    tab3_FW2_FWName.pack(fill=X, pady=3)
    tab3_FW2_RESETButton = ttk.Button(tab3_FW2, text=translations[language]['multiboot_Reset'], width=15, bootstyle=(DANGER), command=lambda: Reset_handler(3, 2, 8))
    tab3_FW2_RESETButton.pack(side=TOP, pady=1)

    tab3_FW3=ttk.Labelframe(tab3_FW_config_sub1, text=translations[language]['multiboot_Partition']+' 3', padding=5)
    tab3_FW3.pack(side=LEFT,fill=X, expand=YES)
    tab3_FW3_FWButton = ttk.Button(tab3_FW3, textvariable=tvar_FW_button[9], width=15, command=lambda: Fileopen_handler(3, 3, 1, 9))
    tab3_FW3_FWButton.pack(side=TOP, pady=1)
    tab3_FW3_CFGButton = ttk.Button(tab3_FW3, textvariable=tvar_CFG_button[9], width=15, command=lambda: Fileopen_handler(3, 3, 2, 9))
    tab3_FW3_CFGButton.pack(side=TOP, pady=1)
    tab3_FW3_CALButton = ttk.Button(tab3_FW3, textvariable=tvar_CAL_button[9], width=15, command=lambda: Fileopen_handler(3, 3, 3, 9))
    tab3_FW3_CALButton.pack(side=TOP, pady=1)
    tab3_FW3_FWName = ttk.Entry(tab3_FW3, width=15, textvariable=tvar_FW_name[9])
    tab3_FW3_FWName.pack(fill=X, pady=3)
    tab3_FW3_RESETButton = ttk.Button(tab3_FW3, text=translations[language]['multiboot_Reset'], width=15, bootstyle=(DANGER), command=lambda: Reset_handler(3, 3, 9))
    tab3_FW3_RESETButton.pack(side=TOP, pady=1)

    tab3_FW_config_sub2=ttk.Frame(tab3_FW_config_sub, padding=0)
    tab3_FW_config_sub2.pack(side=TOP,fill=X, expand=YES, pady=5)

    tab3_FW4=ttk.Labelframe(tab3_FW_config_sub2, text=translations[language]['multiboot_Partition']+' 4', padding=5)
    tab3_FW4.pack(side=LEFT,fill=X, expand=YES)
    tab3_FW4_FWButton = ttk.Button(tab3_FW4, textvariable=tvar_FW_button[10], width=15, command=lambda: Fileopen_handler(3, 4, 1, 10))
    tab3_FW4_FWButton.pack(side=TOP, pady=1)
    tab3_FW4_CFGButton = ttk.Button(tab3_FW4, textvariable=tvar_CFG_button[10], width=15, command=lambda: Fileopen_handler(3, 4, 2, 10))
    tab3_FW4_CFGButton.pack(side=TOP, pady=1)
    tab3_FW4_CALButton = ttk.Button(tab3_FW4, textvariable=tvar_CAL_button[10], width=15, command=lambda: Fileopen_handler(3, 4, 3, 10))
    tab3_FW4_CALButton.pack(side=TOP, pady=1)
    tab3_FW4_FWName = ttk.Entry(tab3_FW4, width=15, textvariable=tvar_FW_name[10])
    tab3_FW4_FWName.pack(fill=X, pady=3)
    tab3_FW4_RESETButton = ttk.Button(tab3_FW4, text=translations[language]['multiboot_Reset'], width=15, bootstyle=(DANGER), command=lambda: Reset_handler(3, 4, 10))
    tab3_FW4_RESETButton.pack(side=TOP, pady=1)

    tab3_FW5=ttk.Labelframe(tab3_FW_config_sub2, text=translations[language]['multiboot_Partition']+' 5', padding=5)
    tab3_FW5.pack(side=LEFT,fill=X, expand=YES)
    tab3_FW5_FWButton = ttk.Button(tab3_FW5, textvariable=tvar_FW_button[11], width=15, command=lambda: Fileopen_handler(3, 5, 1, 11))
    tab3_FW5_FWButton.pack(side=TOP, pady=1)
    tab3_FW5_CFGButton = ttk.Button(tab3_FW5, textvariable=tvar_CFG_button[11], width=15, command=lambda: Fileopen_handler(3, 5, 2, 11))
    tab3_FW5_CFGButton.pack(side=TOP, pady=1)
    tab3_FW5_CALButton = ttk.Button(tab3_FW5, textvariable=tvar_CAL_button[11], width=15, command=lambda: Fileopen_handler(3, 5, 3, 11))
    tab3_FW5_CALButton.pack(side=TOP, pady=1)
    tab3_FW5_FWName = ttk.Entry(tab3_FW5, width=15, textvariable=tvar_FW_name[11])
    tab3_FW5_FWName.pack(fill=X, pady=3)
    tab3_FW5_RESETButton = ttk.Button(tab3_FW5, text=translations[language]['multiboot_Reset'], width=15, bootstyle=(DANGER), command=lambda: Reset_handler(3, 5, 11))
    tab3_FW5_RESETButton.pack(side=TOP, pady=1)

    tab3_FW6=ttk.Labelframe(tab3_FW_config_sub2, text=translations[language]['multiboot_Partition']+' 6', padding=5)
    tab3_FW6.pack(side=LEFT,fill=X, expand=YES)
    tab3_FW6_FWButton = ttk.Button(tab3_FW6, textvariable=tvar_FW_button[12], width=15, command=lambda: Fileopen_handler(3, 6, 1, 12))
    tab3_FW6_FWButton.pack(side=TOP, pady=1)
    tab3_FW6_CFGButton = ttk.Button(tab3_FW6, textvariable=tvar_CFG_button[12], width=15, command=lambda: Fileopen_handler(3, 6, 2, 12))
    tab3_FW6_CFGButton.pack(side=TOP, pady=1)
    tab3_FW6_CALButton = ttk.Button(tab3_FW6, textvariable=tvar_CAL_button[12], width=15, command=lambda: Fileopen_handler(3, 6, 3, 12))
    tab3_FW6_CALButton.pack(side=TOP, pady=1)
    tab3_FW6_FWName = ttk.Entry(tab3_FW6, width=15, textvariable=tvar_FW_name[12])
    tab3_FW6_FWName.pack(fill=X, pady=3)
    tab3_FW6_RESETButton = ttk.Button(tab3_FW6, text=translations[language]['multiboot_Reset'], width=15, bootstyle=(DANGER), command=lambda: Reset_handler(3, 6, 12))
    tab3_FW6_RESETButton.pack(side=TOP, pady=1)

    #3_ВЫВОД
    tab3_OUT=ttk.Labelframe(tab3_FW_config_upper_sub, text=translations[language]['multiboot_Output'], padding=5)
    tab3_OUT.pack(side=RIGHT,fill=BOTH, expand=YES)
    #tab3_LoadButton = ttk.Button(tab3_OUT, textvariable=tvar_eeprom[2], width=20, bootstyle=(INFO), command=lambda: LoadEEPROM_handler(3))
    #tab3_LoadButton.pack(side=TOP, pady=1)
    tab3_FILEButton = ttk.Button(tab3_OUT, text=translations[language]['multiboot_Save_to_file'], width=20, bootstyle=(SUCCESS), command=lambda: Save_EEPROM(3))
    tab3_FILEButton.pack(side=TOP, pady=1)
    tab3_OUTButton = ttk.Button(tab3_OUT, text=translations[language]['multiboot_Write_to_EEPROM'], width=20, bootstyle=(DANGER), command=lambda: Write_EEPROM(3, serial_port_combo.get(), multiboot_window, tab3_progress, EEPROM_SIZE.index(eeprom_size_combo.get())))
    tab3_OUTButton.pack(side=TOP, pady=1) 
    tab3_OUT_RESETButton = ttk.Button(tab3_OUT, text=translations[language]['multiboot_Reset_all'], width=20, bootstyle=(DANGER), command=lambda: Reset_EEPROM_handler(3))
    tab3_OUT_RESETButton.pack(side=BOTTOM, pady=1)

    tab3_FW_config2=ttk.Frame(tab3_FW_config, padding=10)
    tab3_FW_config2.pack(side=TOP,fill=X)
    tab3_progress = ttk.Progressbar(tab3_FW_config2, orient='horizontal', mode='determinate', bootstyle=(SUCCESS, STRIPED))
    tab3_progress.pack(side=TOP, padx=0, pady=(0), expand=YES, fill=X)

    #3_БАЗОВЫЙ ЗАГРУЗЧИК
    tab3_BASEBOOT = ttk.Labelframe(tab3, text=translations[language]['multiboot_BASEBOOT_info'], padding=(10))
    tab3_BASEBOOT.pack(fill=X, side=TOP, pady=10)
    tab3_BASEBOOT_Flash_button = ttk.Button(tab3_BASEBOOT, text=translations[language]['multiboot_Flash']+' BASE_BOOTLOADER_6.bin', width=50, bootstyle=(DANGER), command=lambda: execute('R9OOT_BASE_BOOTLOADER_6.bat'))
    tab3_BASEBOOT_Flash_button.pack(side=LEFT, pady=1, expand=YES)
    tab3_BASEBOOT_Rollback_button = ttk.Button(tab3_BASEBOOT, text=translations[language]['multiboot_Rollback']+' qs_bl.bin', width=50, bootstyle=(WARNING), command=lambda: execute('qs_bl.bat'))
    tab3_BASEBOOT_Rollback_button.pack(side=RIGHT, pady=1, expand=YES) 

    notebook.add(
        child=tab3, 
        text=translations[language]['multiboot_tab_3'], 
        sticky=NW)
    



    #ВКЛАДКА4
    tab4=ttk.Frame(notebook, padding=5)
    tab4.pack(side=TOP,fill=X)
    tab4_label = ttk.Label(tab4, font="-size 10 -weight bold", text=translations[language]['multiboot_LoseHu_warninginfo_text'])
    tab4_label.pack(side=TOP, padx=10, fill=X)
    ttk.Separator(tab4).pack(fill=X, padx=10, pady=10)
    tab4_FW_config = ttk.Labelframe(tab4, text=translations[language]['multiboot_FW_config_info_1'], padding=(5))
    tab4_FW_config.pack(fill=X, side=TOP, padx=0)
    tab4_FW_info = ttk.Label(tab4_FW_config, text=translations[language]['multiboot_FW_config_info_2'], padding=(0))
    tab4_FW_info.pack(fill=X, side=TOP, padx=10, pady=5)

    tab4_FW_config_sub=ttk.Frame(tab4_FW_config, padding=0)
    tab4_FW_config_sub.pack(side=TOP,fill=BOTH, expand=YES)
    tab4_FW1=ttk.Labelframe(tab4_FW_config_sub, text=translations[language]['multiboot_Partition']+' 1', padding=5)
    tab4_FW1.pack(side=LEFT,fill=X, expand=YES)
    tab4_FW1_FWButton = ttk.Button(tab4_FW1, textvariable=tvar_FW_button[13], width=15, command=lambda: Fileopen_handler(4, 1, 1, 13))
    tab4_FW1_FWButton.pack(side=TOP, pady=1)
    tab4_FW1_CFGButton = ttk.Button(tab4_FW1, textvariable=tvar_CFG_button[13], width=15, command=lambda: Fileopen_handler(4, 1, 2, 13))
    tab4_FW1_CFGButton.pack(side=TOP, pady=1)
    tab4_FW1_CALButton = ttk.Button(tab4_FW1, textvariable=tvar_CAL_button[13], width=15, command=lambda: Fileopen_handler(4, 1, 3, 13))
    tab4_FW1_CALButton.pack(side=TOP, pady=1)
    tab4_FW1_FWName = ttk.Entry(tab4_FW1, width=15, textvariable=tvar_FW_name[13])
    tab4_FW1_FWName.pack(fill=X, pady=3)
    tab4_FW1_RESETButton = ttk.Button(tab4_FW1, text=translations[language]['multiboot_Reset'], width=15, bootstyle=(DANGER), command=lambda: Reset_handler(4, 1, 13))
    tab4_FW1_RESETButton.pack(side=TOP, pady=1)

    tab4_FW2=ttk.Labelframe(tab4_FW_config_sub, text=translations[language]['multiboot_Partition']+' 2',  padding=5)
    tab4_FW2.pack(side=LEFT,fill=X, expand=YES)
    tab4_FW2_FWButton = ttk.Button(tab4_FW2, textvariable=tvar_FW_button[14], width=15, command=lambda: Fileopen_handler(4, 2, 1, 14))
    tab4_FW2_FWButton.pack(side=TOP, pady=1)
    tab4_FW2_CFGButton = ttk.Button(tab4_FW2, textvariable=tvar_CFG_button[14], width=15, command=lambda: Fileopen_handler(4, 2, 2, 14), state=DISABLED)
    tab4_FW2_CFGButton.pack(side=TOP, pady=1)
    tab4_FW2_CALButton = ttk.Button(tab4_FW2, textvariable=tvar_CAL_button[14], width=15, command=lambda: Fileopen_handler(4, 2, 3, 14), state=DISABLED)
    tab4_FW2_CALButton.pack(side=TOP, pady=1)
    tab4_FW2_FWName = ttk.Entry(tab4_FW2, width=15, textvariable=tvar_FW_name[14])
    tab4_FW2_FWName.pack(fill=X, pady=3)
    tab4_FW2_RESETButton = ttk.Button(tab4_FW2, text=translations[language]['multiboot_Reset'], width=15, bootstyle=(DANGER), command=lambda: Reset_handler(4, 2, 14))
    tab4_FW2_RESETButton.pack(side=TOP, pady=1)

    tab4_FW3=ttk.Labelframe(tab4_FW_config_sub, text=translations[language]['multiboot_Partition']+' 3', padding=5)
    tab4_FW3.pack(side=LEFT,fill=X, expand=YES)
    tab4_FW3_FWButton = ttk.Button(tab4_FW3, textvariable=tvar_FW_button[15], width=15, command=lambda: Fileopen_handler(4, 3, 1, 15))
    tab4_FW3_FWButton.pack(side=TOP, pady=1)
    tab4_FW3_CFGButton = ttk.Button(tab4_FW3, textvariable=tvar_CFG_button[15], width=15, command=lambda: Fileopen_handler(4, 3, 2, 15), state=DISABLED)
    tab4_FW3_CFGButton.pack(side=TOP, pady=1)
    tab4_FW3_CALButton = ttk.Button(tab4_FW3, textvariable=tvar_CAL_button[15], width=15, command=lambda: Fileopen_handler(4, 3, 3, 15), state=DISABLED)
    tab4_FW3_CALButton.pack(side=TOP, pady=1)
    tab4_FW3_FWName = ttk.Entry(tab4_FW3, width=15, textvariable=tvar_FW_name[15])
    tab4_FW3_FWName.pack(fill=X, pady=3)
    tab4_FW3_RESETButton = ttk.Button(tab4_FW3, text=translations[language]['multiboot_Reset'], width=15, bootstyle=(DANGER), command=lambda: Reset_handler(4, 3, 15))
    tab4_FW3_RESETButton.pack(side=TOP, pady=1)

    tab4_FW4=ttk.Labelframe(tab4_FW_config_sub, text=translations[language]['multiboot_Partition']+' 4', padding=5)
    tab4_FW4.pack(side=LEFT,fill=X, expand=YES)
    tab4_FW4_FWButton = ttk.Button(tab4_FW4, textvariable=tvar_FW_button[16], width=15, command=lambda: Fileopen_handler(4, 4, 1, 16))
    tab4_FW4_FWButton.pack(side=TOP, pady=1)
    tab4_FW4_CFGButton = ttk.Button(tab4_FW4, textvariable=tvar_CFG_button[16], width=15, command=lambda: Fileopen_handler(4, 4, 2, 16), state=DISABLED)
    tab4_FW4_CFGButton.pack(side=TOP, pady=1)
    tab4_FW4_CALButton = ttk.Button(tab4_FW4, textvariable=tvar_CAL_button[16], width=15, command=lambda: Fileopen_handler(4, 4, 3, 16), state=DISABLED)
    tab4_FW4_CALButton.pack(side=TOP, pady=1)
    tab4_FW4_FWName = ttk.Entry(tab4_FW4, width=15, textvariable=tvar_FW_name[16])
    tab4_FW4_FWName.pack(fill=X, pady=3)
    tab4_FW4_RESETButton = ttk.Button(tab4_FW4, text=translations[language]['multiboot_Reset'], width=15, bootstyle=(DANGER), command=lambda: Reset_handler(4, 4, 16))
    tab4_FW4_RESETButton.pack(side=TOP, pady=1)

    #4_ВЫВОД
    tab4_OUT=ttk.Labelframe(tab4_FW_config_sub, text=translations[language]['multiboot_Output'], padding=5)
    tab4_OUT.pack(side=RIGHT,fill=BOTH, expand=YES)
    #tab4_LoadButton = ttk.Button(tab4_OUT, textvariable=tvar_eeprom[3], width=20, bootstyle=(INFO), command=lambda: LoadEEPROM_handler(4))
    #tab4_LoadButton.pack(side=TOP, pady=1)
    tab4_FILEButton = ttk.Button(tab4_OUT, text=translations[language]['multiboot_Save_to_file'], width=20, bootstyle=(SUCCESS), command=lambda: Save_EEPROM(4))
    tab4_FILEButton.pack(side=TOP, pady=1)
    tab4_OUTButton = ttk.Button(tab4_OUT, text=translations[language]['multiboot_Write_to_EEPROM'], width=20, bootstyle=(DANGER), command=lambda: Write_EEPROM(4, serial_port_combo.get(), multiboot_window, tab4_progress, EEPROM_SIZE.index(eeprom_size_combo.get())))
    tab4_OUTButton.pack(side=TOP, pady=1) 
    tab4_OUT_RESETButton = ttk.Button(tab4_OUT, text=translations[language]['multiboot_Reset_all'], width=20, bootstyle=(DANGER), command=lambda: Reset_EEPROM_handler(4))
    tab4_OUT_RESETButton.pack(side=BOTTOM, pady=1)

    tab4_progress = ttk.Progressbar(tab4_FW_config, orient='horizontal', mode='determinate', bootstyle=(SUCCESS, STRIPED))
    tab4_progress.pack(side=TOP, padx=0, pady=(10), expand=YES, fill=X)

    #4_БАЗОВЫЙ ЗАГРУЗЧИК
    tab4_BASEBOOT = ttk.Labelframe(tab4, text=translations[language]['multiboot_BASEBOOT_info'], padding=(10))
    tab4_BASEBOOT.pack(fill=X, side=TOP, pady=10)
    tab4_BASEBOOT_Flash_button = ttk.Button(tab4_BASEBOOT, text=translations[language]['multiboot_Flash']+' BASE_BOOTLOADER.bin', width=50, bootstyle=(DANGER), command=lambda: execute('LOSEHU_BASE_BOOTLOADER.bat'))
    tab4_BASEBOOT_Flash_button.pack(side=LEFT, pady=1, expand=YES)
    tab4_BASEBOOT_Rollback_button = ttk.Button(tab4_BASEBOOT, text=translations[language]['multiboot_Rollback']+' qs_bl.bin', width=50, bootstyle=(WARNING), command=lambda: execute('qs_bl.bat'))
    tab4_BASEBOOT_Rollback_button.pack(side=RIGHT, pady=1, expand=YES) 

    notebook.add(
        child=tab4, 
        text=translations[language]['multiboot_tab_4'], 
        sticky=NW)
    
    check_files_thread = threading.Thread(target=check_files, daemon=True)
    check_files_thread.start()

    multiboot_window.mainloop()



if __name__ == '__main__':
    multiboot()