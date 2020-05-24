```gdb
(gdb) r < /tmp/stack5
Starting program: /opt/protostar/bin/stack5 < /tmp/stack5

Breakpoint 1, 0x080483da in main (argc=Cannot access memory at address 0x4242424a
) at stack5/stack5.c:11
11	in stack5/stack5.c
(gdb) x/40wx 0xbffffc60
0xbffffc60:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffffc70:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffffc80:	0x90909090	0x90909090	0x90909090	0xcc909090
0xbffffc90:	0xcccccccc	0xcccccccc	0xcccccccc	0xcccccccc
0xbffffca0:	0xcccccccc	0xcccccccc	0x42424242	0xbffffc79
0xbffffcb0:	0x00000000	0xbffffd54	0xbffffd5c	0xb7fe1848
0xbffffcc0:	0xbffffd10	0xffffffff	0xb7ffeff4	0x08048232
0xbffffcd0:	0x00000001	0xbffffd10	0xb7ff0626	0xb7fffab0
0xbffffce0:	0xb7fe1b28	0xb7fd7ff4	0x00000000	0x00000000
0xbffffcf0:	0xbffffd28	0xb5713bf5	0x9f302de5	0x00000000
(gdb) info registers
eax            0xbffffc60	-1073742752
ecx            0xbffffc60	-1073742752
edx            0xb7fd9334	-1208118476
ebx            0xb7fd7ff4	-1208123404
esp            0xbffffcac	0xbffffcac
ebp            0x42424242	0x42424242
esi            0x0	0
edi            0x0	0
eip            0x80483da	0x80483da <main+22>
eflags         0x200246	[ PF ZF IF ID ]
cs             0x73	115
ss             0x7b	123
ds             0x7b	123
es             0x7b	123
fs             0x0	0
gs             0x33	51
(gdb) si
Cannot access memory at address 0x42424246
(gdb)
0xbffffc7a in ?? ()
(gdb)
0xbffffc7b in ?? ()
(gdb)
0xbffffc7c in ?? ()
(gdb)
0xbffffc7d in ?? ()
(gdb)
0xbffffc7e in ?? ()
(gdb)
0xbffffc7f in ?? ()
(gdb)
0xbffffc80 in ?? ()
(gdb)
0xbffffc81 in ?? ()
(gdb)
0xbffffc82 in ?? ()
(gdb)
0xbffffc83 in ?? ()
(gdb)
0xbffffc84 in ?? ()
(gdb)
0xbffffc85 in ?? ()
(gdb)
0xbffffc86 in ?? ()
(gdb)
0xbffffc87 in ?? ()
(gdb)
0xbffffc88 in ?? ()
(gdb)
0xbffffc89 in ?? ()
(gdb)
0xbffffc8a in ?? ()
(gdb)
0xbffffc8b in ?? ()
(gdb)
0xbffffc8c in ?? ()
(gdb)
0xbffffc8d in ?? ()
(gdb)
0xbffffc8e in ?? ()
(gdb)
0xbffffc8f in ?? ()
(gdb)
0xbffffc90 in ?? ()
(gdb)
0xbffffc91 in ?? ()
(gdb)
0xbffffc92 in ?? ()
(gdb)
0xbffffc93 in ?? ()
(gdb)
0xbffffc94 in ?? ()
(gdb) c
Continuing.

Program received signal SIGTRAP, Trace/breakpoint trap.
0xbffffc95 in ?? ()
(gdb)
Continuing.

Program received signal SIGTRAP, Trace/breakpoint trap.
0xbffffc96 in ?? ()
(gdb)
Continuing.

Program received signal SIGTRAP, Trace/breakpoint trap.
0xbffffc97 in ?? ()
(gdb)
Continuing.

Program received signal SIGTRAP, Trace/breakpoint trap.
0xbffffc98 in ?? ()
(gdb)
Continuing.

Program received signal SIGTRAP, Trace/breakpoint trap.
0xbffffc99 in ?? ()
(gdb)
Continuing.

Program received signal SIGTRAP, Trace/breakpoint trap.
0xbffffc9a in ?? ()
(gdb)
Continuing.

Program received signal SIGTRAP, Trace/breakpoint trap.
0xbffffc9b in ?? ()
(gdb) x/40wx 0xbffffc60
0xbffffc60:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffffc70:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffffc80:	0x90909090	0x90909090	0x90909090	0xcc909090
0xbffffc90:	0xcccccccc	0xcccccccc	0xcccccccc	0xcccccccc
0xbffffca0:	0xcccccccc	0xcccccccc	0x42424242	0xbffffc79
0xbffffcb0:	0x00000000	0xbffffd54	0xbffffd5c	0xb7fe1848
0xbffffcc0:	0xbffffd10	0xffffffff	0xb7ffeff4	0x08048232
0xbffffcd0:	0x00000001	0xbffffd10	0xb7ff0626	0xb7fffab0
0xbffffce0:	0xb7fe1b28	0xb7fd7ff4	0x00000000	0x00000000
0xbffffcf0:	0xbffffd28	0xb5713bf5	0x9f302de5	0x00000000
(gdb)
```

- Why does it start executing from c95 and not from c8e ???