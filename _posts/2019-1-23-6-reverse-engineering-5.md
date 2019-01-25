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

After a few days, thanks to the poster of the answer [here](https://reverseengineering.stackexchange.com/questions/20453/unknown-parameters-in-custom-signal-handler-on-linux) I have gotten nowhere, however, again thanks to the poster of that answer I now understand where I should look were I proficient enough to understand how to continue, since I didn't really trust (not that I disbelieved it, just skeptical due to different environments and possible differences) the answer, I took an attempt at finding the certain offset myself using `print (int)&(
(((struct ucontext_t*)(0))->member)`:

```
(gdb) ptype ucontext_t
type = struct ucontext {
    unsigned long uc_flags;
    struct ucontext *uc_link;
    stack_t uc_stack;
    mcontext_t uc_mcontext;
    __sigset_t uc_sigmask;
    struct _libc_fpstate __fpregs_mem;
}
(gdb) print (int)&(((struct ucontext*)(0))->uc_mcontext)
$5 = 40
(gdb) print (int)&(((struct ucontext*)(0))->uc_sigmask)
$6 = 296
(gdb) ptype mcontext_t
type = struct {
    gregset_t gregs;
    fpregset_t fpregs;
    unsigned long long __reserved1[8];
}
(gdb) print (int)&(((struct ucontext*)(0))->uc_mcontext.gregs)
$7 = 40
(gdb) print (int)&(((struct ucontext*)(0))->uc_mcontext.fpregs)
$8 = 224
```

As we can see, the offset is `168`, and offset `168` is within `gregs`, and so it must be offset `168 - 40` inside `gregs`, which is `gregs[128/8]` since `gregs` is a `long long[23]`, therefore it has to be at offset 16:

```
(gdb) ptype fpregset_t
type = struct _libc_fpstate {
    __uint16_t cwd;
    __uint16_t swd;
    __uint16_t ftw;
    __uint16_t fop;
    __uint64_t rip;
    __uint64_t rdp;
    __uint32_t mxcsr;
    __uint32_t mxcr_mask;
    struct _libc_fpxreg _st[8];
    struct _libc_xmmreg _xmm[16];
    __uint32_t padding[24];
} *
(gdb) ptype gregset_t
type = long long [23]
```

If only GDB was useful. Time to dig through `/usr/include` and use `grep`:

```c
/* Number of each register in the `gregset_t' array.  */
enum
{
  REG_R8 = 0,
# define REG_R8         REG_R8
  REG_R9,
# define REG_R9         REG_R9
  REG_R10,
# define REG_R10        REG_R10
  REG_R11,
# define REG_R11        REG_R11
  REG_R12,
# define REG_R12        REG_R12
  REG_R13,
# define REG_R13        REG_R13
  REG_R14,
# define REG_R14        REG_R14
  REG_R15,
# define REG_R15        REG_R15
  REG_RDI,
# define REG_RDI        REG_RDI
  REG_RSI,
# define REG_RSI        REG_RSI
  REG_RBP,
# define REG_RBP        REG_RBP
  REG_RBX,
# define REG_RBX        REG_RBX
  REG_RDX,
# define REG_RDX        REG_RDX
  REG_RAX,
# define REG_RAX        REG_RAX
  REG_RCX,
# define REG_RCX        REG_RCX
  REG_RSP,
# define REG_RSP        REG_RSP
  REG_RIP,
# define REG_RIP        REG_RIP
  REG_EFL,
# define REG_EFL        REG_EFL
  REG_CSGSFS,           /* Actually short cs, gs, fs, __pad0.  */
# define REG_CSGSFS     REG_CSGSFS
  REG_ERR,
# define REG_ERR        REG_ERR
  REG_TRAPNO,
# define REG_TRAPNO     REG_TRAPNO
  REG_OLDMASK,
# define REG_OLDMASK    REG_OLDMASK
  REG_CR2
# define REG_CR2        REG_CR2
};
```

Here are the `enum` and macro definitions for the `gregset_t` type, now let's take the register at the 17th offset:

```
  REG_RIP,
# define REG_RIP        REG_RIP
```

I'll point out that I made a horrible mistake of forgetting to 1-index the 16 and accidentally thought it was `REG_RSP`, thank god you didn't see that. There we go, thanks to the SO answer and now we're slightly a step closer, just now we need to fill in the rest of the fucking gaps!

```assembly
   0x0000000008001946:  mov    0xa8(%rdx),%rax
   0x000000000800194d:  lea    0x28(%rdx),%rsi
   0x0000000008001951:  lea    0x2(%rax),%rdi
   0x0000000008001955:  add    $0xe,%rax
   0x0000000008001959:  mov    %rax,0xa8(%rdx)
   0x0000000008001960:  jmpq   0x8001ee0
```

And we're back to this, except now we know `0xa8(%rdx)` = `REG_RIP`, i.e. the address of the instruction after `ud2`, now we can also derive `0x28(%rdx)` as the member at the `+40`th offset from `ucontext_t` which is simply the beginning of the `gregs` member, hence `%rsi` = `&(ucontext_t->mcontext_t.gregs)`, and `%rax` = `<addr. of instr after ud2>`, `%rdi` is `add %al,(%rax)` as `add (%rax),%al` is 2 bytes in length. `%rax += $0xe` makes `%rax` the instruction 12 bytes afterwards, which we can see here:

```assembly
   0x0000000008001190:  ud2
   0x0000000008001192:  add    (%rax),%al <=========\\ from here
   0x0000000008001194:  add    %al,(%rax)           ||
   0x0000000008001196:  add    %al,(%rax)           ||
   0x0000000008001198:  add    %al,(%rax)           ||
   0x000000000800119a:  or     %ecx,0xb0f0000(%rip) ||
   0x00000000080011a0:  add    (%rax),%al <=========// to here 
   0x00000000080011a2:  add    %al,(%rax)
   0x00000000080011a4:  add    %al,(%rax)
   0x00000000080011a6:  add    %al,(%rax)
   0x00000000080011a8:  and    $0x0,%al
   0x00000000080011aa:  or     %al,(%rax)
   0x00000000080011ac:  ud2
   0x00000000080011ae:  add    %al,(%rax)
   0x00000000080011b0:  add    %al,(%rax)
   0x00000000080011b2:  add    %al,(%rax)
   0x00000000080011b4:  add    %al,(%rax)
   0x00000000080011b6:  sub    (%rax),%al
   0x00000000080011b8:  add    %al,(%rax)
   0x00000000080011ba:  ud2
[...]
```

And, to be honest, these instructions are either hand-written, or very badly optimized, but we'll figure that out later.
`mov %rax,0xa8(%rdx)` moves the address of that `add (%rax),%al` into the old `%rip`, and finally we jump to `0x8001ee0`.

```assembly
   0x0000000008001ee0:  movzbl 0x8(%rdi),%edx
   0x0000000008001ee4:  lea    0x201195(%rip),%rax        # 0x8203080
   0x0000000008001eeb:  jmpq   *(%rax,%rdx,8)
```

`0x8(%rdi)` is the double-word at the address of the `add (%rax),%al` plus `0x8`, which is just `or %ecx,0xb0f0000(%rip)`, which is:

```
(gdb) x/d 0x000000000800119a
0x800119a:      9
```

Hence, at the first point, `%edx` = 9, `%rax` = `0x8203080`, and we jump to `[0x8203080 + %rdx * 8]`, which in the first case would be `[0x8203080 + 9 * 8]` which is `0x82030c8`:

```assembly
   0x00000000082030c8:  ficompl (%rdx)
   0x00000000082030ca:  add    %cl,(%rax)
   0x00000000082030cc:  add    %al,(%rax)
   0x00000000082030ce:  add    %al,(%rax)
   0x00000000082030d0:  cli
   0x00000000082030d1:  sbb    (%rax),%al
   0x00000000082030d3:  or     %al,(%rax)
[...]
```
`ficompl` is a part of the floating-point coprocessor instruction-set which translates to `ficomp` in non-AT&T (the flavour made it harder to find smh), now we have to look at the FPU stack, since `ficomp` compares the operand with `ST(0)`, it implies that there's something on the FPU stack, and that `%rdx` is a valid address

issues:
- `%rdx` is 9 in the first iteration
- the fpu stack should be empty
- it doesn't jump anywhere, it legit does a `cli` 4 instructions ahead ?????????

TBF
