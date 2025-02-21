import serial
import keyboard
import time


# LCD commands for sending serial data -- corresponds to enum constants in arduino sketch
CLEAR = 0
SET_CURSOR = 1
PRINT = 2
WRITE = 3

# format for serial message consists of command and message data, which are seperated and marked using special chars
MESSAGE_START = '\r'
MESSAGE_END = '\n'

# key events
TOGGLE_KEYS = ['shift', 'right shift', 'caps lock']
MOVE_KEYS = ['up', 'down', 'left', 'right']

# NOTE: correct comm port should be used depending on user
port = serial.Serial(port='COM5', baudrate=9600)

# allow delay for arduino to reset
time.sleep(3)


# main program
def main():
    # NOTE: initiliaze LCD with correct columns and rows
    lcd = LCD(cols=16, rows=2) 

    while True:
        time.sleep(0.15)
        key = keyboard.read_key()

        match key:
            case key if key in TOGGLE_KEYS:
                continue
            case key if key in MOVE_KEYS:
                if key == 'up': lcd.move_up()
                if key == 'down': lcd.move_down()
                if key == 'left': lcd.move_left()
                if key == 'right': lcd.move_right() 
            case 'enter':
                lcd.enter()
            case 'backspace':
                lcd.delete()
            case key if len(key) == 1 or key == 'space':
                if key == 'space': 
                    key = ' '  

                lcd.write(key)
                lcd.get_cur_line()[lcd.pos_x] = key
                lcd.move_right()
            case _:
                # exit program
                lcd.clear()
                break

    port.close()


# class to handle most LCD and keyboard interface logic
class LCD:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.pos_x = 0
        self.pos_y = 0
        self.text = [[' '] * cols] # stores all lines of text displayed to LCD where each line is a list of chars
        self.line_num = 0 # current line number of stored text


    # access of current line of text
    def get_cur_line(self):
        return self.text[self.line_num]


    # functions for sending LCD commands and messages as serial data to arduino
    def clear(self):
        port.write(f'{CLEAR}{MESSAGE_START}{MESSAGE_END}'.encode())


    def set_cursor(self, posx, posy):
        port.write(f'{SET_CURSOR}{MESSAGE_START}{posx},{posy}{MESSAGE_END}'.encode())


    def print(self, text):
        port.write(f'{PRINT}{MESSAGE_START}{text}{MESSAGE_END}'.encode())


    def write(self, char):
        port.write(f'{WRITE}{MESSAGE_START}{char}{MESSAGE_END}'.encode())
    

    # delete previous char
    def delete(self):
        first_line_deleted = False
        
        # delete current line if empty
        if self.pos_x == 0 and ''.join(self.get_cur_line()).isspace():
            if self.line_num == 0: 
                first_line_deleted = True

            self.text.pop(self.line_num)
            self.text.append([' '] * self.cols) 

        self.move_left()

        if not first_line_deleted:
            self.get_cur_line().pop(self.pos_x)

        for _ in range(len(self.get_cur_line()), self.cols):
            self.get_cur_line().append(' ')

        self.set_cursor(0, self.pos_y)
        self.print(''.join(self.get_cur_line()))
        self.set_cursor(self.pos_x, self.pos_y)


    # 'enter' keystroke function
    def enter(self):
        new_line = self.get_cur_line()[self.pos_x:]
        new_line += [' '] * (self.cols - len(new_line))

        for x in range(self.pos_x, self.cols):
            self.get_cur_line()[x] = ' '

        self.pos_x = 0  
            
        self.text.insert(self.line_num + 1, new_line)
        self.move_down()


    # print all text stored from first_line to last_line by each row on LCD starting from lcd_row
    def update_display(self, first_line, last_line, lcd_row=0): 
        cur_line = first_line 

        while cur_line <= last_line and cur_line < len(self.text):
            self.set_cursor(0, lcd_row)
            self.print(''.join(self.text[cur_line]))

            cur_line +=1
            lcd_row += 1  

        self.set_cursor(self.pos_x, self.pos_y)


    # functions to move current position on LCD (i.e. by 1 col or 1 row)
    def move_left(self):
        self.pos_x -= 1

        if self.pos_x < 0:
            self.pos_x = self.cols - 1

            self.move_up()
        else:
            self.set_cursor(self.pos_x, self.pos_y)


    def move_right(self):
        self.pos_x += 1

        if self.pos_x >= self.cols:
            self.pos_x = 0
            
            self.move_down()
        else:
            self.set_cursor(self.pos_x, self.pos_y)


    def move_up(self):
        self.pos_y -= 1
        self.line_num -= 1

        if self.pos_y < 0:
            self.pos_y = 0

            if self.line_num < 0:
                self.pos_x = 0
                self.line_num = 0

        self.update_display(self.line_num, self.line_num + self.rows - 1)


    def move_down(self):
        self.pos_y += 1
        self.line_num += 1

        if self.pos_y >= self.rows:
            self.pos_y = self.rows - 1

        if (self.line_num >= len(self.text)):
            self.text.append([' '] * self.cols)

        self.update_display(self.line_num - self.rows + 1, self.line_num)


if __name__ == "__main__":
    main() 
    

