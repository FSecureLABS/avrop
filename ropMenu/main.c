#include <avr/io.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <avr/pgmspace.h>
#include <avr/eeprom.h>

#include "main.h"
#include "uart.h"


int8_t notesdb[10][1000] EEMEM;

const char commands_text[] PROGMEM =
	"Possible commands:\r\n";

const char menu_message_start[] PROGMEM =
	"\tR\tRead Note\r\n"
	"\tA\tAdd Note\r\n";

extern unsigned char vm();

int main(void) {    

    uart_init();
	uart_flush();
               
    while(1) {
		int length;
		uart_puts("Welcome to my notes:\r\n");
		main_menu();
    }
    return 0;
}

void main_menu(){
	
	char command;
	
	uart_puts_p(&commands_text);
	uart_puts_p(&menu_message_start);	
	
	command = getCommand();

	if ((command == 'A') ||( command == 'a')) {
		addNoteMenu();
	}
	else if ((command == 'R') ||( command == 'r')) {
		readNoteMenu();
	}
	else{
		uart_puts("Please enter a correct command\r\n");
		main_menu();
	}
}

void addNoteMenu(){
	char note[1000]; // Should be big enough ;)
	int16_t length;
	int save;

	uart_puts("\r\nPlease enter the length of the note:\r\n");
	length = getNoteLength();

	uart_puts("\r\nPlease enter your note:\r\n");
	int16_t index = 0;
	while (index != length){
		note[index] = uart_get();
		uart_putc(note[index]);
		index++;
	}
	note[index+1] = 0x00;
	
	uart_puts("\r\nWould you like to save this note (y/N)?\r\n");
	save = uart_get();
	if (save == 'y' | save == 'Y'){
		saveNote(note);
	} 	
	else{
		uart_puts(note);
	}
}

void saveNote(char* note[]){
	char input;
	int8_t id;
	char *ptr;
	uart_puts("Select note ID (0-9)\r\n");
	input = uart_get();
	uart_putc(input);
	while (uart_get() != 0x0D){}
	id = strtol(input, &ptr, 10);
	uart_puts("\r\n");	
	
	uart_puts("Saving note\r\n");
	eeprom_write_block(note, &notesdb[id], 1000);
	return;
}

void readNoteMenu(){
	char input;
	int8_t id;
	char *ptr;
	char* note[1000];
	
	uart_puts("Select note ID to read (0-9)\r\n");
	input = uart_get();
	uart_putc(input);
	while (uart_get() != 0x0D){}
	input = strtol(input, &ptr, 10);
	id = strtol(input, &ptr, 10);
	uart_puts("\r\n");

	eeprom_read_block(&note, note[id], 1000);
	uart_puts(note);
	uart_puts("\r\n");

	return;
}

char getCommand(){
	char input;
	input = uart_get();
	uart_putc(input);
	while (uart_get() != 0x0D){}
	uart_puts("\r\n");
	
	return input;
}

int16_t getNoteLength(){
	int length;
	char input[5] = {0};
	int n; 
	char *ptr;
	n = 0;
	while (n < 4 & input[n-1] != 0x0D){
		input[n] = uart_get();	
		uart_putc(input[n]);
		n++;
	}
	if (input[n-1] != 0x0D){
		while (uart_get() != 0x0D){}
	}
	return strtol(input, &ptr, 10);
}