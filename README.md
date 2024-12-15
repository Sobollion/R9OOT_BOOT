[![support me](https://img.shields.io/badge/Support%20me-CloudTips-blue)](https://pay.cloudtips.ru/p/c197b86d) [![readme ru](https://img.shields.io/badge/README%20%D0%BD%D0%B0%20%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%BE%D0%BC-214a57)](/README_RU.md)

# R9OOT_BOOT (UNFINISHED AND NOT TESTED YET)
Multibootloader configurator for UVK5/K6 based on Multiboot by LoseHu, BD8DFN and K5TOOLS by hank9999 

# Description of the multiboot
The multiloader consists of two loaders:

* The main bootloader (4KB) is flashed through the SWD interface using ST LINK and replaces the original Quansheng bootloader inside the flash memory of the radio microcontroller. When turned on with the "Menu" button held down, it loads the auxiliary bootloader from EEPROM into RAM and executes it there.

* The auxiliary bootloader (about 12KB) is stored in EEPROM memory. Contains a graphical interface for selecting firmware. It can erase the previous firmware from the microcontroller’s flash memory, read the next selected firmware from the EEPROM and write it instead of the previous one. It also contains the function of exchanging data via a serial port while it is in firmware selection mode (Menu+ON). And the forced firmware function (PTT+ON) (the dialogue with the PC does not work correctly, need to debug it later)

# Now there are 4 multiboot versions for different memory:

* 256 KiB - 3 firmwares with independent settings, channels and calibrations (REBORN with markings for BL24C256 32 KiB memory can also be installed)
* 512 KiB - 4 firmwares with independent settings, channels and calibrations\n(REBORN with markings for BL24C1024 128KiB and IJV version S can also be installed simultaneously)
* 512 KiB - 6 firmwares with independent settings, channels and calibrations (REBORN with markings for BL24C512 64 KiB memory can also be installed)
* 512 KiB - Standard LoseHu Multiboot for 4 firmware. The same settings will be used for all firmwares!

ATTENTION! Do not try to install firmware with EEPROM markup of more than 32 KiB for option 1 (3 firmware) and more than 64 KiB for option 3 (6 firmware). A full reset in such firmware will overwrite the auxiliary bootloader, which is also located in the EEPROM. But you can always roll back to the factory bootloader.

# Hardware upgrade
The modification consists of replacing the standard 64 Kilobit (8KiB) memory chip with a chip of increased capacity or a combination of two chips. Before starting hardware work, you need to decide what firmware you are going to use, since there are some subtleties, for example, the IJV(N) firmware requires fast memory (5ms).
But in general, all other firmwares are not demanding on memory speed and support all possible options.
Replacing the factory EEPROM memory chip (AT24CS64-SSHM) is possible for the following models in sop8 packages:
* BL24CM1A parc (128 KiB) speed 5ms
* M24M01-RP / M24M01-RMN6TP (128 KiB) speed 5ms
* BL24CM2A parc (256 KiB) speed 8ms
* M24M02-RD / M24M02-DRMN6TP (256KiB) speed 10ms
* M24M02-WT / M24M02-DWMN3TP/K (256KiB) speed 5ms - the best option

The chips have pins A1, A2/E1, E2 for addressing. Thus, it is possible to connect up to 4 chips with a volume of 1M (128 KiB) or up to two chips with a volume of 2M (256 KiB) to the i2c bus.
# Description of the multiboot configurator program
In the header there is a FAQ button and a block of basic operations with EEPROM; they were borrowed from the hank9999 and BG4IST program.

In the main body of the program there are 4 independent tabs for different multi-loaders. These tabs have a different number of cells, the first 3, the second 4, the third 6 and the fourth 4. 
You can load 3 files into each cell: firmware, configuration and calibrations.
This is done only for convenience, so that you can initially quickly configure the assembly as you need. But this does not mean that every time you have to change configurations or calibrations through this program. 
Files selected in cells are saved in temporary folders for subsequent assembly.

On the right side there is an output block, where you can save the assembly to a file or load it into the radio. Or preload a previously saved file to replace firmware or configurations in it. 

Configurations and calibrations can be edited as usual, without the need to configure the EEPROM with this program each time

At the very bottom there is a block of firmware for the main bootloader, there are only two buttons, flash it and roll back to the factory bootloader.
# Guide to action:
Initial installation:

* Make a hardware modification - replace the EEPROM memory with 256 or 512 KiB.
* Using any usual method, flash special firmware from LoseHu to configure EEPROM of all sizes. You can find it in release archive, `LoseHu firmware for first EEPROM load.bin` (its special difference is black rectangles instead of numbers, due to the lack of fonts).
* Configure the auxiliary bootloader and write the selected option with the necessary firmware and settings to EEPROM. Press the red button to write to EEPROM.
* Disassemble the station, connect ST LINK to the SWD interface and flash the main bootloader from the same program tab where you configured the auxiliary one.

# If you already have the multiboot:
You don't need to do all of the above. You can immediately proceed to the third point; you can configure the EEPROM by connecting the radio in the firmware selection menu mode (Menu+ON). Point 4 is also not needed, since you already have the required main bootloader flashed.
# Unbricking:
If something goes wrong, don't panic, in 99.9% of cases you can roll back the main bootloader to the factory one.

* Disassemble the station, connect ST LINK to the SWD interface (with PTT or Menu pressed) 
* Flash the factory bootloader (yellow button below) from any tab of the program. 
* You can either start installing the multiboot from the beginning, or flash any firmware.


# Soon.
Loading and editing function. It will be useful if you just want to change one firmware in your assembly (for example, a new version has been released), you will need: 
Save EEPROM by selecting your chip size.
In the configurator window, click the preload EEPROM button, the cells will be updated and show where they are occupied and where they are free.
Load the firmware into the desired cell.
Save or write EEPROM to the radio as usual (red or green button).

# Disclaimer:

* **I am not responsible**
* Radios may be bricked during the flashing process, and I am not responsible for this.
* I do not assume any legal responsibility. This project is open source; you are free to use it, but you must be responsible for your actions.

# This development exists thanks to LoseHu
Donation QR code:

[![Donation QR code](https://github.com/losehu/uv-k5-firmware-chinese/blob/main/payment/show.png)](https://losehu.github.io/payment-codes/)
