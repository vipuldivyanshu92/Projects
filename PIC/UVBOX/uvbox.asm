	LIST   		P=PIC16F627
	#include 	<P16F627.INC>
	__CONFIG	_BODEN_OFF & _CP_OFF & _DATA_CP_OFF & _PWRTE_ON & _WDT_OFF & _LVP_OFF & _MCLRE_ON & _INTRC_OSC_NOCLKOUT

;********************************************
;* Set up the constants                     *
;********************************************
SRL_PORT	equ		PORTA	; Serial port in on port A
CLK_PIN		equ		1		; Clock pin is bit 0
DATA_PIN	equ		0		; Data pin is bit 1
; Seven segment display are active low
DIG0		equ		4		; right 7seg display
DIG1		equ		3		; mid 7seg display
DIG2		equ		2		; left 7seg display
; User defined storage space
SRL_DATA	equ		020h
COUNTER		equ		021h

;********************************************
;* Define reset vector and interrupt vector *
;********************************************
	ORG		000h
	GOTO	Start
	ORG		004h
	GOTO	Interrupt

;********************************************
;* Subroutines                              *
;********************************************

; Send subroutine, send content of W serially to port defined by SRL_PORT
; and pins defined by CLK_PIN and DATA_PIN, msb send first.
Send
	MOVWF	SRL_DATA
	MOVLW	8						; This needs to be repeated 8 times
	MOVWF	COUNTER
TXFER
	BCF		SRL_PORT, CLK_PIN		; Set the Clock low
	BCF		SRL_PORT, DATA_PIN		; Clear flag in both cases
	BTFSC	SRL_DATA, 7				; Check if bit need to be set
	BSF		SRL_PORT, DATA_PIN		; Set it if true
	BSF		SRL_PORT, CLK_PIN		; Set the Clock high
	RLF		SRL_DATA, 1				; Shift right data
	DECFSZ	COUNTER, 1				; Decrement and check if counter is 0
	GOTO	TXFER					; Loop while not 0
	RETURN
	
	
; 
; PWM cycle manipulation
Increase
	RLF		CCPR1L, 1		; rotate
WAITI
	BTFSC	PORTB, 0		; wait for switch 1 to be released
	GOTO	WAITI
	RETURN
;
; PWM cycle manipulation	
Decrease
	RRF		CCPR1L, 1
WAITD
	BTFSC	PORTB, 1
	GOTO	WAITD
	RETURN
	
;********************************************
;* Interrupt Subroutine                     *
;********************************************
Interrupt
	RETFIE

;********************************************
;* Main                                     *
;********************************************
Start
	; * Configure ports *
	; Disable Comparator module's
	MOVLW	B'00000111'
	MOVWF	CMCON
	
	; Configure port A for driving 7seg display
	MOVLW	B'00011100'		; 7 segment displays are active low
	MOVWF	PORTA
	
	BSF		STATUS, RP0		; Select bank 1
	; Configure 7Segment Display on port A
	MOVLW	B'11100000'		; RA4 to RA0 are outputs
	MOVWF	TRISA
	
	; Configure PWM on port B
	MOVLW	B'11111001'		
	MOVWF	PR2				; set PR2 to 0xFF for the period (datasheet p67)
	BCF		TRISB, 3		; TRISB<3> must be cleared to make CCP1 pin an output
	BSF		TRISB, 0		; RA0 is an input
	BSF		TRISB, 1		; RA1 is an input
	
	BCF		STATUS, RP0		; switch to bank 0
	
	; CCP1Z:CCP1Y PWM Lest Significant bits
	; CCP1M2:CCP1M0 Enable PWM mode
	MOVLW	B'00111100'		; datasheet p63
	MOVWF	CCP1CON

	MOVLW	B'00000001'
	MOVWF	CCPR1L			; set the duty cycle
	BSF		T2CON, T2CKPS1	; set the prescalar to 1:16
	BSF		T2CON, TMR2ON	; Timer2 is on
	
	; Send Test
	;pgfedcba
	MOVLW	B'11000001' ; write U
	CALL	Send
	BCF		SRL_PORT, DIG0
	
INFLOOP
	GOTO INFLOOP
	
	BTFSC	PORTB, 0		; wait for switch 1 to be pressed
	CALL	Increase
	BTFSC	PORTB, 1
	CALL	Decrease
	
	END
	