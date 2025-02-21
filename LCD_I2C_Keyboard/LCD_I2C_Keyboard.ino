// this should work for LCDs connected to an arduino using the I2C interface

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// LCD commands for receiving serial data
enum {
  CLEAR,
  SET_CURSOR,
  PRINT,
  WRITE
};

// message markers for receiving serial data
const char startOfMsg[] = "\r";
const char endOfMsg[] = "\n";

// store incoming serial data and flag for state of data receival
char incomingData[32];
boolean recvSuccess = false;
// store parsed command and message for displaying to LCD
int lcdCommand;
char lcdMessage[32];

// NOTE: initialize LCD with correct I2C address and columns and rows
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.cursor();
  lcd.blink();
  Serial.begin(9600);
}

void loop() {
  recvData();

  if (recvSuccess == true) {
    parseData();
    displayMessage();
    
    recvSuccess = false; // set flag to false to prevent looping over code
  }
}

void recvData() {
  // receive each char from incoming serial data and store in char array
  static byte i = 0;
  char c;
  
  while (Serial.available() > 0 && recvSuccess == false) {
    c = Serial.read();

      if (c != endOfMsg[0]) {
        incomingData[i] = c;
        i++;
      } else {
        incomingData[i] = '\0';
        i = 0;
        recvSuccess = true;
      }
  }
}

void parseData() {
  // parse command from data and convert to corresponding enum int
  char *ptr = strtok(incomingData, startOfMsg);
  lcdCommand = atoi(ptr);
  // parse main message from data
  ptr = strtok(NULL, startOfMsg);
  strcpy(lcdMessage, ptr);
}

void displayMessage() {
  switch (lcdCommand) {
    case CLEAR: {
      lcd.clear();
      break;
    }
    case SET_CURSOR: {
      // parse new x and y position from message
      char *ptr = strtok(lcdMessage, ",");
      int posX = atoi(ptr);
      
      ptr = strtok(NULL, ",");
      int posY = atoi(ptr);

      lcd.setCursor(posX, posY);
      break;
    }
    case PRINT: {
      lcd.print(lcdMessage);
      break;
    }
    case WRITE: {
      lcd.write(lcdMessage[0]);
      break;
    }
  }
}