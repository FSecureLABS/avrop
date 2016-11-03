#include <avr/io.h>
#include <avr/pgmspace.h>

#include "uart.h"

#define F_CPU 16000000
#define BAUD 38400                             
#define BAUDRATE ((F_CPU)/(BAUD*16UL)-1)

void uart_init(){
	UBRR0H = ( BAUDRATE >> 8 );
	UBRR0L = BAUDRATE;
	UCSR0A = 0<<U2X0;
	UCSR0B = (1<<RXEN0)|(1<<TXEN0);
	UCSR0C = (2<<USBS0)|(3<<UCSZ00);
}

void uart_puts(char *str) {
	int i = 0;
	while(str[i] != '\0') {
		uart_putc(str[i]);
		i++;
	}
}

char uart_get() {
	
	while (!(UCSR0A & (1<<RXC0))) {} 
	return(UDR0); 
}

void uart_flush(){
	char dump;
	while (UCSR0A & (1<<RXC0)){
		dump = uart_get();
	}
}
void uart_putc(char data) {
    while (!(UCSR0A&(1<<UDRE0)));    
    UDR0 = data;    
}

void uart_puts_p(const char *str) {
    while(pgm_read_byte(str) != 0x00) { 
        uart_putc(pgm_read_byte(str++));
    }
}