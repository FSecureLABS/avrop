.global vm
vm_init:
	;get the start of the 'code' it is pointed at by the first virtual register vr0
	pop YH
	pop YL
	ld XH, Y+
	ld XL, Y
	ret

	;save stack pointer
	in r10, 0x3D
	in r11, 0x3E
	ret

	;stack piv
	pop r11
	pop r10
	out 0x3E, r11
	out 0x3D, r10
	ret

vm_loop :
	;mov ebx, [esi] Read address of virtual index register
	ld YH, X+
	ld YL, X+
	ret

	;mov ebx, [ebx] Read virtual index register
	ld ZH, Y+
	ld ZL, Y
	ret

	;add ebx, [esi+2] Compute source address
	ld YH, X+
	ld YL, X+
	ret

	add ZL, YL
	adc ZH, YH
	ret

	;mov ebx, [ebx] Read data from source address (8 bits)
	ld r24, Z
	ret

	;mov [edx], ebx Write (only write 8 bits)
	st Z, r24
	ret

end: