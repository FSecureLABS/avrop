import intelhex
import sys
import os
import struct

"""
	Convert intel hex output from Atmel Studio to binary payloads for ROP.py
"""

args = sys.argv[1:]
if len(args) == 2:
	fin = args[0]
	fout = args[1]

	intelhex.hex2bin(fin, fout, None, None, None, None)

res = ''
with open(fout, 'r') as f:
	first = f.read(1)
	second = f.read(1)
	while second != '':
		res += second + first
		first = f.read(1)
		second = f.read(1)
		
with open(fout,'w') as fw:
	fw.write(res)