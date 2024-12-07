import numpy as np

#4 Сета (таб вкладки) 6 Рядов (Ячейка), 4 Столбца (0 Имя в меню бутлодера / 1 имя файла прошивки / 2 имя файла конфиг / 3 имя файла калибровки)

#               name   FW_filename   CFG_filename     CAL_filename
#tab # 1 ---- [[[ '',  'Прошивка',  'Конфигурация',  'Калибровки'],  ---- Partition 1
#               [ '',  'Прошивка',  'Конфигурация',  'Калибровки'],  ---- Partition 2
#               [ '',  'Прошивка',  'Конфигурация',  'Калибровки']], ---- Partition 3

#tab # 2 ----  [[ '',  'Прошивка',  'Конфигурация',  'Калибровки'],  ---- Partition 1
#               [ '',  'Прошивка',  'Конфигурация',  'Калибровки'],  ---- Partition 2
#               [ '',  'Прошивка',  'Конфигурация',  'Калибровки'],  ---- Partition 3
#               [ '',  'Прошивка',  'Конфигурация',  'Калибровки']]] ---- Partition 4

#tab # 3 ----  [[ '',  'Прошивка',  'Конфигурация',  'Калибровки'],  ---- Partition 1
#               [ '',  'Прошивка',  'Конфигурация',  'Калибровки'],  ---- Partition 2
#               [ '',  'Прошивка',  'Конфигурация',  'Калибровки'],  ---- Partition 3
#               [ '',  'Прошивка',  'Конфигурация',  'Калибровки'],  ---- Partition 4
#               [ '',  'Прошивка',  'Конфигурация',  'Калибровки'],  ---- Partition 5
#               [ '',  'Прошивка',  'Конфигурация',  'Калибровки']]] ---- Partition 6

#tab # 4 ----  [[ '',  'Прошивка',  'Конфигурация',  'Калибровки'],  ---- Partition 1
#               [ '',  'Прошивка',  'Конфигурация',  'Калибровки'],  ---- Partition 2
#               [ '',  'Прошивка',  'Конфигурация',  'Калибровки'],  ---- Partition 3
#               [ '',  'Прошивка',  'Конфигурация',  'Калибровки']]] ---- Partition 4
names = np.ndarray(shape=(4,6,4),dtype='<U15') 


#sizes(in bytes) FW1 FW2 FW3 FW4 FW5 FW6
#              [[ 0,  0,  0,  0,  0,  0],  ---- tab 1
#               [ 0,  0,  0,  0,  0,  0],  ---- tab 2
#               [ 0,  0,  0,  0,  0,  0],  ---- tab 3
#               [ 0,  0,  0,  0,  0,  0]]] ---- tab 4
FW_sizes = np.zeros(shape=(4,6)).astype(int)

file_path = ''


Adresses_1 =   [{'filename':'FW1.bin', 'address':0x13000},
                {'filename':'FW2.bin', 'address':0x22000},
                {'filename':'FW3.bin', 'address':0x31000},
                {'filename':'CFG1.bin', 'address':0x9F80},
                {'filename':'CFG2.bin', 'address':0xBF80},
                {'filename':'CFG3.bin', 'address':0xDF80},
                {'filename':'CAL1.bin', 'address':0xBD80}, #+1e00
                {'filename':'CAL2.bin', 'address':0xDD80}, 
                {'filename':'CAL3.bin', 'address':0xFD80}
                ]
                #{'filename':'BL', 'address':0x10000}
                #{'filename':'Meta', 'address':0xFF80}

Adresses_2 =   [{'filename':'FW1.bin', 'address':0x44000},
                {'filename':'FW2.bin', 'address':0x53000},
                {'filename':'FW3.bin', 'address':0x62000},
                {'filename':'FW4.bin', 'address':0x71000},
                {'filename':'CFG1.bin', 'address':0x38000},
                {'filename':'CFG2.bin', 'address':0x3A000},
                {'filename':'CFG3.bin', 'address':0x3C000},
                {'filename':'CFG4.bin', 'address':0x3E000},
                {'filename':'CAL1.bin', 'address':0x39E00}, #+1e00
                {'filename':'CAL2.bin', 'address':0x3BE00},
                {'filename':'CAL3.bin', 'address':0x3DE00},
                {'filename':'CAL4.bin', 'address':0x3FE00}
                ]
                #{'filename':'BL', 'address':0x41000}
                #{'filename':'Meta', 'address':0x40000}

Adresses_3 =   [{'filename':'FW1.bin', 'address':0x26000},
                {'filename':'FW2.bin', 'address':0x35000},
                {'filename':'FW3.bin', 'address':0x44000},
                {'filename':'FW4.bin', 'address':0x53000},
                {'filename':'FW5.bin', 'address':0x62000},
                {'filename':'FW6.bin', 'address':0x71000},
                {'filename':'CFG1.bin', 'address':0x16F20},
                {'filename':'CFG2.bin', 'address':0x18F20},
                {'filename':'CFG3.bin', 'address':0x1AF20},
                {'filename':'CFG4.bin', 'address':0x1CF20},
                {'filename':'CFG5.bin', 'address':0x1EF20},
                {'filename':'CFG6.bin', 'address':0x20F20},
                {'filename':'CAL1.bin', 'address':0x18D20}, #+1e00
                {'filename':'CAL2.bin', 'address':0x1AD20},
                {'filename':'CAL3.bin', 'address':0x1CD20},
                {'filename':'CAL4.bin', 'address':0x1ED20},
                {'filename':'CAL5.bin', 'address':0x20D20},
                {'filename':'CAL6.bin', 'address':0x22D20}
                ]
                #{'filename':'BL', 'address':0x23000}
                #{'filename':'Meta', 'address':0x22F20}

Adresses_4 =   [{'filename':'FW1.bin', 'address':0x44000},
                {'filename':'FW2.bin', 'address':0x53000},
                {'filename':'FW3.bin', 'address':0x62000},
                {'filename':'FW4.bin', 'address':0x71000},
                {'filename':'CFG1.bin', 'address':0x0000},
                {'filename':'CAL1.bin', 'address':0x1E00},
                ]
                #{'filename':'BL', 'address':0x41000}
                #{'filename':'Meta', 'address':0x40000}





    #FW_num=Meta (количество прошивок)
    #Boot_mode = Meta+1 (Переменная режима для основного загрузчика. Всегда значение 01)
    #Current_firm = Meta+2 (Переменная текущей прошивки. Если это новый мультибут из чистового EEPROM_FF, то значение 01)
    #BL_name = Meta+8 (Имя вспомогательного загрузчика)
    
    #Meta_name(partition) = Meta+(32*partition) (имя прошивки, 13 байт)
    #Meta_address_start(partition) = Meta+(32*partition)+16
    #Meta_address_end(partition) = Meta+(32*partition)+20

    #адреса калибровок=адреса конфигов+7680 байт
    
"""{'BL':0x10000, 'Meta':0xFF80, 'FW1':0x13000, 'FW2':0x22000, 'FW3':0x31000, 'CFG1':0x9F80, 'CFG2':0xDF7F, 'CFG3':0xFF7F},
    {'BL':0x41000, 'Meta':0x40000, 'FW1':0x44000, 'FW2':0x53000, 'FW3':0x62000, 'FW4':0x71000, 'CFG1':0x38000, 'CFG2':0x3A000, 'CFG3':0x3C000, 'CFG4':0x3E000},
    {'BL':0x23000, 'Meta':0x22F20, 'FW1':0x26000, 'FW2':0x35000, 'FW3':0x44000, 'FW4':0x53000, 'FW5':0x62000, 'FW6':0x71000, 'CFG1':0x16F20, 'CFG2':0x18F20, 'CFG3':0x1AF20, 'CFG4':0x1CF20, 'CFG5':0x1EF20, 'CFG6':0x20F20},
    {'BL':0x41000, 'Meta':0x40000, 'FW1':0x44000, 'FW2':0x53000, 'FW3':0x62000, 'FW4':0x71000}"""

is_new = True