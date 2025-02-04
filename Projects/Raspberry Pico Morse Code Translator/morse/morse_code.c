/**
 * The given template is a guideline for your coursework only.
 * You are free to edit/create any functions and variables.
 * You can add extra C files if required.
*/


#include <stdio.h>
#include <string.h>
#include <time.h>
#include "pico/stdlib.h"
#include "includes/seven_segment.h"

#define BUTTON_PIN			16	// Pin 21 (GPIO 16)

const char *morseAlphabet[26] = { // Morse code array corresponding to letters in the alphabet

    ".-"  ,     // A
    "-...",     // B
    "-.-.",     // C
    "-.." ,     // D
    "."   ,     // E
    "..-.",     // F
    "--." ,     // G
    "....",     // H
    ".."  ,     // I
    ".---",     // J
    "-.-" ,     // K
    ".-..",     // L
    "--"  ,     // M
    "-."  ,     // N
    "---" ,     // O
    ".--.",     // P
    "--.-",     // Q
    ".-." ,     // R
    "..." ,     // S
    "-"   ,     // T
    "..-" ,     // U
    "...-",     // V
    ".--" ,     // W
    "-..-",     // X
    "-.--",     // Y
    "--.."      // Z

};

const char alphabet[28] = { // alphabet

    'A',
    'B',
    'C',
    'D',
    'E',
    'F',
    'G',
    'H',
    'I',
    'J',
    'K',
    'L',
    'M',
    'N',
    'O',
    'P',
    'Q',
    'R',
    'S',
    'T',
    'U',
    'V',
    'W',
    'X',
    'Y',
    'Z',
    '8',
    '-'

};


void welcome() { // shows a welocme message in the serial monitor and displays the middle dash on the 7 segment display

    printf("Welcome!\nYou can start when the 7 segment display turns off.\n");
    seven_segment_show(27);
    sleep_ms(1000);
    seven_segment_off();
}

void displayEightError() { // displays an 8 on the 7 segment display

    printf("%c\n", '8');
    seven_segment_show(26);
    sleep_ms(500);
    seven_segment_off();
}

void decoder(char morseLetter[]){ // displays the corresponding letter on the 7 segment display
    
    bool checkExisting = false;

    for (int i = 0; i < 26; i++) { // loops through every string in morseAlphabet array
        if (strcmp(morseLetter, "") == 0) {
            checkExisting = true;
            break;
        }
        if (strcmp(morseLetter, morseAlphabet[i]) == 0) {
            printf("%c\n", alphabet[i]);
            seven_segment_show(i); // shows the letter corresponding to the provided morse code
            sleep_ms(500);
            seven_segment_off();
            checkExisting = true;
            break;
        }
    }

    if (!checkExisting) { // if no correlation, shows an error on the serial monitor and displayEightError()
        printf("Error - Morse Input Does Not Correlate To A Letter\n");
        displayEightError();
        
    }
}

char checkSignalInput(double timePressed) { // checks the input of the button

    double signalDuration = 0.25;
    double maxButtonDuration = 0.7;
    char signalType;

    if (timePressed > maxButtonDuration) {
        printf("Error - button pressed longer than 0.7 seconds\n");
        displayEightError();
        signalType = '8';
    }

    else {
        if (timePressed < signalDuration) { // Dot
            signalType = '.';
        }
        if (signalDuration <= timePressed) { // Dash
            signalType = '-';
        }
    }
    return signalType;
}

int main() {

    // Variable Declaration
    clock_t buttonDown;
    clock_t buttonUp;
    clock_t gapStart;
    clock_t currentGap;
    double timePressed;
    double timeNotPressed;
    char morseLetter[4] = "";
    bool gapTimeCheck = false;


    stdio_init_all();

    // Initialise the seven segment display.
    seven_segment_init();

    // Turn the seven segment display off when the program starts.
    seven_segment_off();

    // Initialize the button's GPIO pin.
    gpio_init(BUTTON_PIN);
    gpio_set_dir(BUTTON_PIN, GPIO_IN);
    gpio_pull_down(BUTTON_PIN); // Pull the button pin towards ground (with an internal pull-down resistor).

    welcome(); // Calls welcome function

    while (true) {

        if (gpio_get(BUTTON_PIN)) { // Button pressed
            seven_segment_show(27); // Displays middle dash on 7 segment display
            buttonDown = clock(); // Starts time when button is pressed
            while (gpio_get(BUTTON_PIN)) {
            
            }
            seven_segment_off();
            buttonUp = clock() - buttonDown; // Button released
            timePressed = ((double) buttonUp) / CLOCKS_PER_SEC; // Calculates the time button was pressed in seconds
            char signal = checkSignalInput(timePressed); // Input based on the time
            if (signal != '8') {
                strncat(morseLetter, &signal, 1); // Adds the input to the morse code message
            }

            gapTimeCheck = true; // Enables the time gap between button presses
            timeNotPressed = 0;
            gapStart = clock(); // Starts the gap time
            currentGap = clock();
        }
        if (gapTimeCheck) {
            currentGap = clock() - gapStart; // Current time of the gap
            timeNotPressed = ((double) currentGap) / CLOCKS_PER_SEC; // Calculates time of gap in seconds

            if (timeNotPressed > 0.4) { // Displays letter as the gap is over 0.4
                decoder(morseLetter); // Calls decoder function
                strcpy(morseLetter, ""); // Resets morseLetter string for the next letter
                gapTimeCheck = false; // Resets gapTimeCheck
            }
        }
    }
    return 0;


}





