---
layout: post
title: reverse engineering crackme 5
---

[This crackme can be found here](https://crackmes.one/crackme/5bc0fe0033c5d4110a29b296). Its level of difficulty is rated at a `3` which probably means I'll give up at some point, but there's no wrong in trying. In the case that I do give up, there is source-code which goes along with it, so I can simply look at it.
But for the duration of the decompilation, I will be blind to the source.

```assembly
.text:0000000000000FC0 main            proc near               ; DATA XREF: start+1D↓o
.text:0000000000000FC0                 push    rbp
.text:0000000000000FC1                 push    rbx
.text:0000000000000FC2                 mov     rbp, rsi
.text:0000000000000FC5                 mov     ebx, edi
.text:0000000000000FC7                 sub     rsp, 8
.text:0000000000000FCB                 call    sub_19C6
.text:0000000000000FD0                 test    al, al
.text:0000000000000FD2                 mov     edx, 1
.text:0000000000000FD7                 jz      short loc_1028
.text:0000000000000FD9                 call    sub_1965
.text:0000000000000FDE                 test    al, al
.text:0000000000000FE0                 mov     edx, 2
.text:0000000000000FE5                 jz      short loc_1028
.text:0000000000000FE7                 movsxd  rdi, ebx
.text:0000000000000FEA                 mov     rsi, rbp
.text:0000000000000FED                 call    sub_1190
.text:0000000000000FF2                 cmp     rax, 1
.text:0000000000000FF6                 lea     rdi, aWrong     ; "Wrong"
.text:0000000000000FFD                 jz      short loc_1021
.text:0000000000000FFF                 cmp     rax, 2
.text:0000000000001003                 lea     rdi, aHell86CrackmeP ; "[hell86 crackme] Please pass the flag a"...
.text:000000000000100A                 jz      short loc_1021
.text:000000000000100C                 test    rax, rax
.text:000000000000100F                 lea     rdi, aOk        ; "OK!"
.text:0000000000001016                 lea     rax, s          ; "You have encountered a bug"
.text:000000000000101D                 cmovnz  rdi, rax        ; s
.text:0000000000001021                 call    _puts
.text:0000000000001026                 xor     edx, edx
.text:0000000000001028                 mov     eax, edx
.text:000000000000102A                 pop     rdx
.text:000000000000102B                 pop     rbx
.text:000000000000102C                 pop     rbp
.text:000000000000102D                 retn
.text:000000000000102D main            endp
```

Note that I've changed from `gdb` to IDA, as, especially for this crackme, I need utility and functionality over a minimal interface (with respect to my ability, of course).
Here is the C source-code that I have decompiled (since I don't trust the Hex-Rays decompiler for shit):

```c
UNKNOWN sub_19C6 (void);
int sub_1190 (int argc, char **argv);

int
main (int argc, char **argv)
{
  UNKNOWN res_1 = sub_19C6 ();
  if (!res_1)
    {
      return 1;
    }

  UNKNOWN res_2 = sub_1965 (UNKNOWN);
  if (!res)
    {
      return 2;
    }

  int res_3 = sub_1190 (argc, argv);

  switch (res_3)
  {
    case (1):
      puts ("Wrong");
      break;
    case (2):
      puts ("[hell86 crackme] Please pass the flag as a command-line argument.");
      break;
    case (0):
      puts ("OK!");
      break;
    default:
      puts ("You have encountered a bug");
      break;
  }

  return 0;
}
```

And for the first function call, to `sub_19C6` I get the following, after deriving that it initializes some `sigaltstack` structure:

```c
_Bool init_sigaltstack (void)
{
  void *stack_base = malloc (8192);
  struct stack_t stackdata;
  
  if (!data)
    {
      return 0;
    }

  memset (stackdata, 0, sizeof (struct sigalstack));
  // inline opt.: rep stosd

  stackdata.ss_p = stack_base;
  if (!sigaltstack (&stackdata, NULL))
    {
      return 1;
    }
  free (stack_base);
  return 0;
}
```

A little bit deeper in, (after analyzing the second function call in `main` to a signal action register), here's the disassembly for the custom signal handler (as dumped from GDB, since I'm inconsistent):

```assembly
   0x0000000008001946:  mov    0xa8(%rdx),%rax
   0x000000000800194d:  lea    0x28(%rdx),%rsi
   0x0000000008001951:  lea    0x2(%rax),%rdi
   0x0000000008001955:  add    $0xe,%rax
   0x0000000008001959:  mov    %rax,0xa8(%rdx)
   0x0000000008001960:  jmpq   0x8001ee0
```

Which jumps to:

```assembly
   0x0000000008001ee0:  movzbl 0x8(%rdi),%edx
   0x0000000008001ee4:  lea    0x201195(%rip),%rax        # 0x8203080
   0x0000000008001eeb:  jmpq   *(%rax,%rdx,8)
```

And we are stuck at this jump, as it relies on `%rdx` whose value we don't have. Initially, I thought it was the `void *` parameter passed to signal handler, casted from `ucontext_t`, but `mov 0xa8(%rdx),%rax` invalidates this as there is no such offset `0xa8` in a `ucontext_t` structure--but it seems so much like a structure access, as `lea 0x2(%rax),%rdi` is done after, implying a pointer was dereferenced and now another structure within is being used for access.
By the first jump, the `0xa8`'th member in `%rdx` has become `%rax + $0xe` which is the `0x2`th member of the `0xa8`th member of `%rdx`, all plus `$0xe`.

The latter piece of assembly is most likely referencing an array, so we can check, if we set `%rdx` = 0, i.e. `jmp *(0x8203080 + 0 * 8)` = `jmp *(0x8203080)`. We arrive at the value `0x1a1f`, which honestly, I have no clue what this could be, perhaps after the calls are registered, just before the `ud2` this array will be populated with assembly.

```
(gdb) x/a 0x8203080
0x8203080:      0x8001a1f
(gdb) x/a 0x8203080+8
0x8203088:      0x8001a20
(gdb) x/a 0x8203080+8+8
0x8203090:      0x8001a39
(gdb) x/a 0x8203080+8+8+8
0x8203098:      0x8001a52
```

And, indeed, there are things! Functions, to be specific, perhaps we could take a guess and say `%rdx` = 4, since SIGILL=4 and therefore perhaps by chance we would be right:

```assembly
   0x0000000008001a6c:  movzbl 0xa(%rdi),%eax
   0x0000000008001a70:  movzbl 0x9(%rdi),%ecx
   0x0000000008001a74:  movzbl 0xb(%rdi),%edi
   0x0000000008001a78:  mov    (%rsi,%rax,8),%rax
   0x0000000008001a7c:  cqto
   0x0000000008001a7e:  idivq  (%rsi,%rdi,8)
   0x0000000008001a82:  mov    %rax,(%rsi,%rcx,8)
   0x0000000008001a86:  retq
```

This code repeats for all of the signals apparently (if they are even signals), and really I have no idea where to go further with this as I don't have exactly enough information about the registers. And, I crashed GDB by setting a breakpoint before the jump into the array and the signal handler's crashed so I can't CTRL+C or CTRL+Z out of it.

TBF
