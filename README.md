# Arduino LCD w/ keyboard detection

Uses python and serial input to allow an Arduino board wired to a compatible LCD to receive keystrokes from the computer's keyboard and display them on the LCD.

## Requirements

the python script requires installing both the [pyserial](https://github.com/pyserial/pyserial) and [keyboard](https://github.com/boppreh/keyboard) packages or with the requirements file: `pip install -r requirements.txt`

either the [LiquidCrystal](https://github.com/arduino-libraries/LiquidCrystal) or [LiquidCrystal_I2C](https://github.com/johnrickman/LiquidCrystal_I2C) library is needed depending on how the LCD is wired to the board, both can also be installed through the Arduino IDE.

## Usage

upload the required arduino sketch (`LCD_Keyboard.ino` or `LCD_I2C_Keyboard.ino`) to the board and then run the python file: `python main.py`

## Important notes

-   the arrow keys can be used to move the cursor around the LCD
-   pressing a key for a single character simply overwrites the current character
-   likewise, pressing spacebar will only write a whitespace character and will not shift the rest to the right
-   pressing backspace / deleting a character will only shift to the left characters in the current line, and will delete the current line if it is empty
-   only a few keystroke functions have been added
-   some characters may not be displayed properly

some unexpected behaviour exists because implementing key presses to work in a traditional manner was too complicated and/or because it would otherwise compromise the ability to easily and freely write to the limited dimensions of the LCD without greatly affecting other characters and rows.

## Thanks

this was my first project working with an Arduino board and environment, so [this tutorial](https://forum.arduino.cc/t/serial-input-basics-updated/382007) really helped me make receiving serial data work. A good part of the code in the arduino program is taken from it.
