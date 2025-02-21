// this should work for standard LCDs wired to an arduino board
// the exact numbers and order of all pins connected to the arduino must be ensured when setting up the LCD

#include <LiquidCrystal.h>

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

// NOTE: initialize LCD with correct pin numbers
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

void setup() {
  lcd.begin(16, 2); // NOTE: set up LCD with correct columns and rows
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