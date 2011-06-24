#include P16F627A.INC
	__CONFIG	_BODEN_OFF & _CP_OFF & _DATA_CP_OFF & _PWRTE_ON & _WDT_OFF & _LVP_OFF & _MCLRE_ON & _XT_OSC

	ORG		0
	GOTO	Start
		

;******************************************
;* Main Program                           *
;******************************************

Start
	; Configure PWM module
	BSF		STATUS, RP0		; switch to bank 1
	MOVLW	B'11111001'
	MOVWF	PR2				; set PR2 to 0xFF for the period (datasheet p67)
	BCF		TRISB, 3		; TRISB<3> must be cleared to make CCP1 pin an output
	BCF		STATUS, RP0		; switch to bank 0

	MOVLW	B'00111100'		; datasheet p63
	MOVWF	CCP1CON

	MOVLW	B'00000001'
	MOVWF	CCPR1L			; set the duty cycle
	BSF		T2CON, T2CKPS1	; set the prescalar to 1:16
	BSF		T2CON, TMR2ON	; Timer2 is on

	; Configure push buttons
	MOVLW	B'00000111'		; Disable Comparator module's
	MOVWF	CMCON

	BSF		STATUS, RP0		; switch to bank 1
	MOVLW	B'11111111'		; all RA ports are inputs
	MOVWF	TRISA	
	BCF		STATUS, RP0		; switch to bank 0

Loop
	BTFSC	PORTA, 0		; wait for switch 1 to be pressed
	CALL	Increase
	BTFSC	PORTA, 1
	CALL	Decrease
	GOTO	Loop

Increase
	RLF		CCPR1L, 1		; rotate
waitI
	BTFSC	PORTA, 0		; wait for switch 1 to be released
	GOTO	waitI
	RETURN

Decrease
	RRF		CCPR1L, 1
waitD
	BTFSC	PORTA, 1
	GOTO	waitD
	RETURN
	
	END