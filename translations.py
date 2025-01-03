from const_vars import LanguageType

translations = {
    LanguageType.SIMPLIFIED_CHINESE: {
        # UI
        'tool_name': 'K5/K6 小工具集',
        'multiboot_tool_name': 'LoseHu-R9OOT 多重引导配置器',
        'now_state_none_text': '当前操作: 无',

        'theme_label_text': '主题',
        'serial_port_text': '串口',
        'firmware_label_text': '固件版本',

        'multiboot_tab_1': '3 个固件 (256KiB)',
        'multiboot_tab_2': '4 个固件+ (512KiB)',
        'multiboot_tab_3': '6 个固件 (512KiB)',
        'multiboot_tab_4': 'LoseHu (512KiB)',

        # Buttons
        'clean_eeprom_button_text': '清空EEPROM',
        'auto_write_font_button_text': '自动写入字库',
        'read_calibration_button_text': '读取校准参数',
        'write_calibration_button_text': '写入校准参数',
        'read_config_button_text': '读取配置参数',
        'write_config_button_text': '写入配置参数',
        'write_font_conf_button_text': '写入字库配置',
        'write_tone_options_button_text': '写入亚音参数',
        'write_font_compressed_button_text': '写入压缩字库',
        'write_font_uncompressed_button_text': '写入全量字库',
        'write_font_old_button_text': '写入字库 (旧)',
        'write_pinyin_old_index_button_text': '写入拼音表（旧）',
        'write_pinyin_new_index_button_text': '写入拼音表（新）',
        'backup_eeprom_button_text': '备份EEPROM',
        'restore_eeprom_button_text': '恢复EEPROM',
        'todo_button_text': '敬请期待',
        'multiboot_button_text': '多引导加载程序',
        'multiboot_FAQ_text': '常问问题',
        'multiboot_BASEBOOT_info': '烧写主引导程序。通过 SWD 接口连接设备',
        'multiboot_Flash':'刷新',
        'multiboot_Rollback':'回滚到工厂引导加载程序',
        'multiboot_Write_to_EEPROM':'写入EEPROM',
        'multiboot_Save_to_file':'保存到文件',
        'multiboot_Firmware':'固件',
        'multiboot_Configuration':'配置',
        'multiboot_Calibration':'校准',
        'multiboot_Partition':'分区',
        'multiboot_Reset':'重置',
        'multiboot_Output':'输出',
        'multiboot_url':'https://docs.google.com/document/d/1C5G6CuUtSksKVTVCLTgiO_yrb_gvX0gqdK0sEUN4TZE/edit?usp=sharing',
        'multiboot_Load_file':'加载文件',
        'multiboot_occupied':'占用',
        'multiboot_cleared':'清除',
        'multiboot_Reset_all':'全部重置',
        'multiboot_EEPROM_operations':'EEPROM 操作',
        'reset_radio_text':'重置收音机',
        'Error':'错误',
        'Info':'提示',
        'Success':'成功地!',
        'multiboot_warning_text': '在继续构建配置之前，请仔细研究多重引导程序设计。',
        'multiboot_3_warninginfo_text': '3 个固件多重引导，具有单独的配置\n(也可以使用 REBORN 和 BL24C256 映射来实现 32KiB）',
        'multiboot_4_warninginfo_text': '4 个固件多重引导，具有单独的配置\n(也可以同时使用 REBORN 与 BL24C1024 映射 128KiB 和 IJV S 版本）',
        'multiboot_6_warninginfo_text': '6 个固件多重引导，具有单独的配置\n(也可以使用 REBORN 和 BL24C512 映射来实现 64KiB）',
        'multiboot_LoseHu_warninginfo_text': 'LoseHu 的 4 个固件的多重启动\n注意！所有固件都将使用相同的设置！）',
        'multiboot_FW_config_info_1':'将辅助引导加载程序、固件和配置写入 EEPROM',
        'multiboot_FW_config_info_2':'选择固件文件（配置和校准 - 可选）',
        'clean_warning_1':'请悉知，清空EEPROM没有任何用处，是否继续？',
        'clean_warning_2':'清空EEPROM将会删除EEPROM中的所有数据，请确保你已经备份了EEPROM中的重要数据！',
        'clean_warning_3':'该操作会清空EEPROM内所有数据(包括设置、信道、校准、字库等)\n确定清空EEPROM请点击否',
        'Warning':'警告',
        'COM_NONE':'没有选择串口！',
        'EEROM_Cleared':'清空EEPROM成功！',
        'Unexpanded':'未扩容固件',
        'NOT':'非',
        'May_not_cleared':'固件，部分扇区可能无法被清除 (仅清除前8KiB原厂大小数据)',
        'Write_done':'写入成功！',
        'Canceled':'用户取消',
        'Incompatible_1':'选择的文件大小为',
        'Incompatible_2':'，但目标eeprom大小为',
        'Incompatible_3':'，是否继续？',
        'Backup_success':'保存成功！',
        'Сheck_port_1':'串口连接成功！\n版本号: ',
        'Сheck_port_2':'\n自动检测结果如下:\n固件版本: ',
        'Сheck_port_3':'固件无法自动检测EEPROM大小\n',
        'Сheck_port_4':'EEPROM大小',
        'Сheck_port_6':'串口连接失败！<-',
        'Exception_1':'串口写入数据失败！',
        'Exception_2':'数据头长度不正确！',
        'Exception_3':'数据头响应错误！',
        'Exception_4':'指令长度不正确！',
        'Exception_5':'尾部数据长度不正确！',
        'Exception_6':'尾部数据响应错误！',
        'Exception_7':'没有收到电台应答包！',
        'Exception_8':'写入前8KiB EEPROM响应错误！',
        'Exception_9':'写入扩容部分 EEPROM响应错误！',
        'multiboot_open_FW':'固件大小不应超过 60 KiB',
        'multiboot_open_CFG':'配置大小不应小于 7 KiB 且超过 8 KiB',
        'multiboot_open_CAL':'Cal 大小应为 512 B',
        'multiboot_saved':'构建文件保存成功！',
        'multiboot_write_done':'固件和辅助引导加载程序已成功加载到无线电中！ \n是否要将程序集保存到文件中？ \n如果您确定您的操作正确，请重新启动收音机。',
        'multiboot_write_start':'正在加载数据，请按确定并耐心等待！',


        # Tooltip
        'logger_warning': '所有操作均有一定的风险，请确保您已备份校准等文件！！！',
        'eeprom_size_combo_tooltip_text': 'EEPROM芯片容量，若自动检测正确则无需修改',
        'firmware_combo_tooltip_text': '固件版本，若自动检测正确则无需修改',
        'serial_port_combo_tooltip_text': '点击选择K5/K6所在串口',
        'clean_eeprom_button_tooltip_text': '清除EEPROM中的所有数据',
        'auto_write_font_button_tooltip_text': '自动写入机器固件所需字库等文件，如不清楚点那个按钮的情况下，点这个总没错',
        'read_calibration_button_tooltip_text': '校准文件包含硬件参数校准信息，必须备份！建议终身保留以备恢复',
        'write_calibration_button_tooltip_text': '校准文件只在更换芯片或清除EEPROM数据后写一次即可',
        'read_config_button_tooltip_text': '配置文件包含了菜单设置信息、开机字符和信道信息等，如无特别需要可不备份，不同固件的菜单设置可能不通用',
        'write_config_button_tooltip_text': '配置文件如无特别需要，可以不写',
        'write_font_conf_button_tooltip_text': '写入字库配置，如果不使用自动写入，请在执行完字库写入后点击',
        'write_tone_options_button_tooltip_text': '写入亚音参数，如果不使用自动写入，请在执行完字库写入后点击',
        'write_font_compressed_button_tooltip_text': '压缩GB2312字库，萝狮虎118K、123H版本及后续版本使用',
        'write_font_uncompressed_button_tooltip_text': '全量GB2312字库，用于萝狮虎118H版本，后续未使用',
        'write_font_old_button_tooltip_text': '117版本及之前版本使用，旧字库',
        'write_pinyin_old_index_button_tooltip_text': '123版本拼音索引，如果不使用自动写入，请在执行完字库写入后点击',
        'write_pinyin_new_index_button_tooltip_text': '124及以上版本拼音索引，如果不使用自动写入，请在执行完字库写入后点击',
        'backup_eeprom_button_tooltip_text': '备份EEPROM中的数据，使用EEPROM下拉框可以选择所要备份的大小',
        'restore_eeprom_button_tooltip_text': '恢复EEPROM中的数据，使用EEPROM下拉框可以选择所要恢复的大小',
        'todo_button_tooltip_text': '敬请期待',
        'multiboot_button_tooltip_text': '适用于多种固件的引导加载程序配置器',
        'language_combo_tooltip_text': '更改语言，重启程序生效'



    },
    LanguageType.ENGLISH: {
        'tool_name': 'K5/K6 Tools',
        'multiboot_tool_name': 'LoseHu-R9OOT Multiboot configurator',
        'now_state_none_text': 'Now state: none',

        'theme_label_text': 'Theme',
        'serial_port_text': 'Serial',
        'firmware_label_text': 'Firmware',

        'multiboot_tab_1': '3 firmwares (256KiB)',
        'multiboot_tab_2': '4 firmwares+ (512KiB)',
        'multiboot_tab_3': '6 firmwares (512KiB)',
        'multiboot_tab_4': 'LoseHu (512KiB)',

        'clean_eeprom_button_text': 'Clear EEPROM',
        'auto_write_font_button_text': 'Auto write font',
        'read_calibration_button_text': 'Read calibration',
        'write_calibration_button_text': 'Write calibration',
        'read_config_button_text': 'Read config',
        'write_config_button_text': 'Write config',
        'write_font_conf_button_text': 'Write font config',
        'write_tone_options_button_text': 'Write tone config',
        'write_font_compressed_button_text': 'Write comp font',
        'write_font_uncompressed_button_text': 'Write full font',
        'write_font_old_button_text': 'Write old font',
        'write_pinyin_old_index_button_text': 'Write old index',
        'write_pinyin_new_index_button_text': 'Write new index',
        'backup_eeprom_button_text': 'Backup EEPROM',
        'restore_eeprom_button_text': 'Restore EEPROM',
        'todo_button_text': 'Coming soon',
        'multiboot_button_text': 'Multiboot',
        'multiboot_FAQ_text': 'FAQ',
        'multiboot_BASEBOOT_info': 'Flash the main bootloader. Connect the device via SWD interface',
        'multiboot_Flash':'Flash',
        'multiboot_Rollback':'Roll back to factory bootloader',
        'multiboot_Write_to_EEPROM':'Write to EEPROM',
        'multiboot_Save_to_file':'Save to file',
        'multiboot_Firmware':'Firmware',
        'multiboot_Configuration':'Configuration',
        'multiboot_Calibration':'Calibration',
        'multiboot_Partition':'Partition',
        'multiboot_Reset':'Reset',
        'multiboot_Output':'Output',
        'multiboot_url':'https://docs.google.com/document/d/1nPnri-2vnVsbrmzJG5w5rxGLy_dEQppQJSnYT3Vm6zY/edit?usp=sharing',
        'multiboot_Load_file':'Load file',
        'multiboot_occupied':'occupied',
        'multiboot_cleared':'cleared',
        'multiboot_Reset_all':'Reset all',
        'multiboot_EEPROM_operations':'EEPROM operations',
        'reset_radio_text':'reset radio',
        'Error':'Error',
        'Info':'Info',
        'Success':'Success!',
        'multiboot_warning_text': 'Carefully study the multibootloader design before proceeding with the build configuration.',
        'multiboot_3_warninginfo_text': '3-firmwares multiboot with separate configs\n(also may used REBORN with BL24C256 mapping for 32KiB)',
        'multiboot_4_warninginfo_text': '4-firmwares multiboot with separate configs\n(also may used REBORN with BL24C1024 mapping for 128KiB and IJV S version)',
        'multiboot_6_warninginfo_text': '6-firmwares multiboot with separate configs\n(also may used REBORN with BL24C512 mapping for 64KiB)',
        'multiboot_LoseHu_warninginfo_text': 'Multiboot for 4 firmwares from LoseHu\n(ATTENTION! The same settings will be used for all firmwares!)',
        'multiboot_FW_config_info_1':'Write auxiliary bootloader, firmware and configurations to EEPROM',
        'multiboot_FW_config_info_2':'Select firmware files (configurations and calibrations - optional)',
        'clean_warning_1':'Please be aware that clearing EEPROM is useless. Do you want to continue?',
        'clean_warning_2':'Clearing EEPROM will delete all data in EEPROM. Please make sure you have backed up important data in EEPROM!',
        'clean_warning_3':'This operation will clear all data in EEPROM (including settings, channels, calibration, fonts, etc.)\nConfirm to clear EEPROM, please click No',
        'Warning':'Warning',
        'COM_NONE':'No serial port selected!',
        'EEROM_Cleared':'Cleared EEPROM successfully!',
        'Unexpanded':'Unexpanded firmware',
        'NOT':'Not',
        'May_not_cleared':'Firmware, some sectors may not be cleared (only the first 8KiB of factory size data is cleared)',
        'Write_done':'Writing successfully!',
        'Canceled':'Cancelled by User',
        'Incompatible_1':'The selected file size is',
        'Incompatible_2':', but the target eeprom size is',
        'Incompatible_3':', do you want to continue? ',
        'Backup_success':'Saved successfully!',
        'Сheck_port_1':'Serial port connection successful! \nVersion number: ',
        'Сheck_port_2':'\nAutomatic detection results are as follows:\nFirmware version: ',
        'Сheck_port_3':'The firmware cannot automatically detect the EEPROM size\n',
        'Сheck_port_4':'EEPROM Size',
        'Сheck_port_6':'Serial port connection failed! <-',
        'Exception_1':'Serial port data writing failed! ',
        'Exception_2':'Data header length is incorrect! ',
        'Exception_3':'Data header response error! ',
        'Exception_4':'Instruction length is incorrect! ',
        'Exception_5':'Tail data length is incorrect! ',
        'Exception_6':'Tail data response error! ',
        'Exception_7':'No response packet received from radio! ',
        'Exception_8':'Write the first 8KiB EEPROM response error! ',
        'Exception_9':'Write the expansion part EEPROM response error! ',
        'multiboot_open_FW':'Firmware size should not exceed 60 KiB',
        'multiboot_open_CFG':'Configuration size should not be\nless than 7 KiB and greater than 8 KiB',
        'multiboot_open_CAL':'Calibration size should be 512 B',
        'multiboot_saved':'Build file saved successfully!',
        'multiboot_write_done':'Firmware and auxiliary bootloader successfully loaded into the radio! \nDont want to save the build to a file? \nIf you are sure that you have done everything correctly, reboot the radio.',
        'multiboot_write_start':'Loading data started, please press Ok and wait patiently!',


        'logger_warning': 'All operations have certain risks, please make sure you have backed up the configuration and calibration files！！！',
        'eeprom_size_combo_tooltip_text': 'EEPROM chip capacity, no need to modify if automatically detected correctly',
        'firmware_combo_tooltip_text': 'Firmware version, no need to modify if automatically detected correctly',
        'serial_port_combo_tooltip_text': 'Click to select the port where K5/K6 is located',
        'clean_eeprom_button_tooltip_text': 'Clear ALL data in the EEPROM',
        'auto_write_font_button_tooltip_text': 'Automatically write the font library and other files required for machine firmware. If you are unsure about the button next to it, clicking this one is never wrong.',
        'read_calibration_button_tooltip_text': 'The calibration file contains hardware parameter calibration information, must be backed up! It is recommended to keep it for a lifetime for recovery.',
        'write_calibration_button_tooltip_text': 'Write the calibration file only once after replacing the chip or clearing EEPROM data.',
        'read_config_button_tooltip_text': 'The configuration file contains menu settings, boot characters, channel information, etc. It is not necessary to back up if there are no special requirements. Menu settings for different firmware may not be universal.',
        'write_config_button_tooltip_text': 'You can skip writing the configuration file if not needed.',
        'write_font_conf_button_tooltip_text': 'Write font library configuration. If not using automatic writing, click after executing font library writing.',
        'write_tone_options_button_tooltip_text': 'Write t-tone parameters. If not using automatic writing, click after executing font library writing.',
        'write_font_compressed_button_tooltip_text': 'Compressed GB2312 font library, used for losehu 118K, 123H versions, and subsequent versions.',
        'write_font_uncompressed_button_tooltip_text': 'Full GB2312 font library, used for losehu 118H version and later unused versions.',
        'write_font_old_button_tooltip_text': 'Used for losehu 117 version and earlier versions, old font library.',
        'write_pinyin_old_index_button_tooltip_text': '123 version Pinyin index. If not using automatic writing, click after executing font library writing.',
        'write_pinyin_new_index_button_tooltip_text': '124 and later versions Pinyin index. If not using automatic writing, click after executing font library writing.',
        'backup_eeprom_button_tooltip_text': 'Backup data in EEPROM. Use the EEPROM dropdown to select the size to be backed up.',
        'restore_eeprom_button_tooltip_text': 'Restore data in EEPROM. Use the EEPROM dropdown to select the size to be restored.',
        'todo_button_tooltip_text': 'Coming soon',
        'multiboot_button_tooltip_text': 'Bootloader configurator for multiple firmwares',
        'language_combo_tooltip_text': 'Change language, take effect after restart.'


    },
    LanguageType.RUSSIAN: {
        'tool_name': 'K5/K6 Инструменты',
        'multiboot_tool_name': 'LoseHu-R9OOT Multiboot: Конфигуратор мультизагрузчика',
        'now_state_none_text': 'Текущая операция: Нет',

        'theme_label_text': 'Тема',
        'serial_port_text': 'COM',
        'firmware_label_text': 'Прошивка',

        'multiboot_tab_1': '3 прошивки (256KiB)',
        'multiboot_tab_2': '4 прошивки+ (512KiB)',
        'multiboot_tab_3': '6 прошивок (512KiB)',
        'multiboot_tab_4': 'LoseHu (512KiB)',

        'clean_eeprom_button_text': 'Очистить EEPROM',
        'auto_write_font_button_text': 'Автозапись шрифта',
        'read_calibration_button_text': 'Считать калибровки',
        'write_calibration_button_text': 'Записать калибровки',
        'read_config_button_text': 'Считать конфигурацию',
        'write_config_button_text': 'Записать конфигурацию',
        'write_font_conf_button_text': 'Записать конфиг шрифта',
        'write_tone_options_button_text': 'Записать конфиг тона',
        'write_font_compressed_button_text': 'Записать сжатый шрифт',
        'write_font_uncompressed_button_text': 'Записать полный шрифт',
        'write_font_old_button_text': 'Записать старый шрифт',
        'write_pinyin_old_index_button_text': 'Записать старый индекс',
        'write_pinyin_new_index_button_text': 'Записать новый индекс',
        'backup_eeprom_button_text': 'Считать EEPROM',
        'restore_eeprom_button_text': 'Записать EEPROM',
        'todo_button_text': 'Скоро',
        'multiboot_button_text': 'Мультибут',
        'multiboot_FAQ_text': 'ЧаВо',
        'multiboot_BASEBOOT_info': 'Зашить основной загрузчик в Flash. Подключите устройство по интерфейсу SWD',
        'multiboot_Flash':'Зашить',
        'multiboot_Rollback':'Откатиться на заводской загрузчик',
        'multiboot_Write_to_EEPROM':'Записать в EEPROM',
        'multiboot_Save_to_file':'Сохранить в файл',
        'multiboot_Firmware':'Прошивка',
        'multiboot_Configuration':'Конфигурация',
        'multiboot_Calibration':'Калибровки',
        'multiboot_Partition':'Ячейка',
        'multiboot_Reset':'Сбросить',
        'multiboot_Output':'Вывод',
        'multiboot_url':'https://docs.google.com/document/d/10DJ2QTfe-59tCzwhTMaSd6j8xJFYBIdcexCEjCNIav0/edit?usp=sharing',
        'multiboot_Load_file':'Загрузить файл',
        'multiboot_occupied':'занято',
        'multiboot_cleared':'очищено',
        'multiboot_Reset_all':'Сбросить всё',
        'multiboot_EEPROM_operations':'Операции с EEPROM',
        'reset_radio_text':'Перезагрузить',
        'Error':'Ошибка',
        'Info':'Информация',
        'Success':'Успех!',
        'multiboot_warning_text': 'Внимательно изучите устройство мультизагрузчика, прежде чем приступать к конфигурации сборки.',
        'multiboot_3_warninginfo_text': 'Мультибут на 3 прошивки с независимыми настройками, каналами и калибровками\n(также может быть установлен REBORN с разметкой для BL24C256 32KiB памяти)',
        'multiboot_4_warninginfo_text': 'Мультибут на 4 прошивки с независимыми настройками, каналами и калибровками\n(также могут быть установлены REBORN с разметкой для BL24C1024 128KiB и IJV версия S)',
        'multiboot_6_warninginfo_text': 'Мультибут на 6 прошивок с независимыми настройками, каналами и калибровками\n(также может быть установлен REBORN с разметкой для BL24C512 64KiB памяти)',
        'multiboot_LoseHu_warninginfo_text': 'Мультибут на 4 прошивки от LoseHu\n(ВНИМАНИЕ! Для всех прошивок будет использоваться одни и теже настройки!)',
        'multiboot_FW_config_info_1':'Записать вспомогательный загрузчик, прошивки и конфигурации в EEPROM',
        'multiboot_FW_config_info_2':'Выберите файлы прошивок (конфигураций и калибровок - необязательно)',
        'clean_warning_1':'Осторожно, очистка EEPROM сделает станцию бесполезной. Хотите продолжить?',
        'clean_warning_2':'Очистка EEPROM удалит все данные. Пожалуйста убедитесь что вы сохранили резервную копию EEPROM!',
        'clean_warning_3':'Эта операция очистит все данные в EEPROM (включая настройки, каналы, калибровки, шрифты, и.т.д.)\nЧтобы продолжить, нажмите Нет',
        'Warning':'Предупреждение',
        'COM_NONE':'Последовательный порт не выбран!',
        'EEROM_Cleared':'EEPROM успешно очищен!',
        'Unexpanded':'Нерасширенная прошивка',
        'NOT':'Не',
        'May_not_cleared':'Прошивка, некоторые сектора могут быть не очищены (очищаются только первые 8 КБ данных заводского размера)',
        'Write_done':'Успешно записано!',
        'Canceled':'Отменено Пользователем',
        'Incompatible_1':'Выбраный файл ',
        'Incompatible_2':', но целевой размер EEPROM ',
        'Incompatible_3':', хотите продолжить? ',
        'Backup_success':'Успешно сохранено!',
        'Сheck_port_1':'Успешно соединено! \nВерсия: ',
        'Сheck_port_2':'\nРезультаты автоматического определения:\nПрошивка: ',
        'Сheck_port_3':'Невозможно автоматически определить размер EEPROM\n',
        'Сheck_port_4':'размер EEPROM',
        'Сheck_port_6':'Соединение прервано! <-',
        'Exception_1':'Запись данных через последовательный порт не удалась! ',
        'Exception_2':'Длина заголовка данных неверна! ',
        'Exception_3':'Ошибка ответа заголовка данных! ',
        'Exception_4':'Длина инструкции неверна! ',
        'Exception_5':'Длина хвостовых данных неверна! ',
        'Exception_6':'Ошибка ответа хвостовых данных! ',
        'Exception_7':'Пакет ответа радиосигнала не получен! ',
        'Exception_8':'Ошибка ответа записи первых 8 КБ EEPROM! ',
        'Exception_9':'Ошибка ответа записи расширенной части EEPROM! ',
        'multiboot_open_FW':'Размер прошивки не должен превышать 60 KiB',
        'multiboot_open_CFG':'Размер конфигурации не должен быть\nменее 7 KiB и превышать 8 KiB',
        'multiboot_open_CAL':'Размер калибровки должен быть 512 B',
        'multiboot_saved':'Файл сборки успешно сохранён!',
        'multiboot_write_done':'Прошивки и вспомогательный загрузчик успешно загружены в рацию! \nНе желаете сохранить сборку в файл? \nЕсли вы уверены в правильности действий - перезагрузите рацию.',
        'multiboot_write_start':'Процесс загрузки начался, нажмите Ok и терпеливо ожидайте!',


        'logger_warning': 'Все операции сопряжены с определенными рисками. Убедитесь, что у вас есть резервные копии конфигураций и калибровок！！！',
        'eeprom_size_combo_tooltip_text': 'Объём чипа EEPROM, можно не выбирать, если определился автоматически',
        'firmware_combo_tooltip_text': 'Версия прошивки, можно не выбирать, если определилась автоматически',
        'serial_port_combo_tooltip_text': 'Нажмите для выбора порта, к которому подключена K5/K6',
        'clean_eeprom_button_tooltip_text': 'Стереть все данные в EEPROM',
        'auto_write_font_button_tooltip_text': 'Автоматически записать библиотеку шрифтов и другие файлы, необходимые для прошивки машины. Если вы не уверены, нажатие на эту кнопку не будет ошибкой.',
        'read_calibration_button_tooltip_text': 'Файл калибровки содержит информацию о калибровке параметров оборудования, необходимо сделать резервную копию! Рекомендуется хранить его всегда, для случая восстановления.',
        'write_calibration_button_tooltip_text': 'Записывайте файл калибровки только один раз после замены чипа или очистки данных EEPROM.',
        'read_config_button_tooltip_text': 'Файл конфигурации содержит настройки меню, символы загрузки, информацию о каналах и т. д. Резервное копирование не обязательно, если нет особых требований. Настройки меню для разных прошивок могут быть не универсальными.',
        'write_config_button_tooltip_text': 'Вы можете пропустить написание файла конфигурации, если это не нужно.',
        'write_font_conf_button_tooltip_text': 'Записать конфигурацию библиотеки шрифтов. Если автоматическая запись не используется, щелкните после выполнения записи библиотеки шрифтов.',
        'write_tone_options_button_tooltip_text': 'Записать t-tone параметры. Если автоматическая запись не используется, щелкните после выполнения записи библиотеки шрифтов.',
        'write_font_compressed_button_tooltip_text': 'Сжатая библиотека шрифтов GB2312, используется в losehu 118K, 123H, и последующих версиях.',
        'write_font_uncompressed_button_tooltip_text': 'Полная библиотека шрифтов GB2312, используется в losehu 118H и в более поздних версиях.',
        'write_font_old_button_tooltip_text': 'Используется для losehu 117 и ранних версий, старая библиотека шрифтов.',
        'write_pinyin_old_index_button_tooltip_text': '123 версия индекс Пиньинь. Если автоматическая запись не используется, щелкните после выполнения записи библиотеки шрифтов.',
        'write_pinyin_new_index_button_tooltip_text': '124 и поздние версиии индекс Пиньинь. Если автоматическая запись не используется, щелкните после выполнения записи библиотеки шрифтов.',
        'backup_eeprom_button_tooltip_text': 'Сохранить слепок EEPROM в файл. Используйте выпадающий список EEPROM чтобы выбрать необходимый объём для восстановления.',
        'restore_eeprom_button_tooltip_text': 'Восстановить данные в EEPROM из файла. Используйте выпадающий список EEPROM чтобы выбрать необходимый объём для восстановления.',
        'todo_button_tooltip_text': 'Скоро',
        'multiboot_button_tooltip_text': 'Конфигуратор загрузчика для нескольких прошивок',
        'language_combo_tooltip_text': 'Для смены языка перезапустите программу.'


    }
}
