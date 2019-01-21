---
layout: post
title: reverse engineering crackme 1
---

Seeing as this is my first post, and I'm not entirely adjusted to writing blog-posts, I'll begin with an introduction.
I'm Unazed Spectaculum; I've been programming for six years with surplus, primarily in Python (as representative of the majority of the repositories on my GitHub), C (for a year) and x86{-64} (mainly studying documents like ABIs, learning about compiler theory and so forth in conjunction with assembly).
This post will be of theme to the blog (if I see a reason for it to continue), that is, reverse engineering, as I'm genuinely interested in it, and other subsidiary topics such as binary exploitation.

Furthermore, I digress into the focal point of this post, i.e., reversing a simple crackme sourced [here](https://github.com/LeoTindall/crackmes/blob/master/crackme01.c) with the goal of recreating the source code (with the certain optimizations applied by GCC).
Although it may seem slightly pointless to try and reverse engineer a binary whose source we have, even if we mayn't explicitly refer back to it, we will still have some notion of what it does and hence have an obvious advantage during reverse engineering; however, my perspective is not to necessarily try and correlate bits of assembly to bits of C, rather understand the optimizations and transformations applied by the compiler.

Now, to begin, allow me to give the C source-code:

```c
#include <stdio.h>
#include <string.h>

int main(int argc, char** argv) {

    if (argc != 2) {
        printf("Need exactly one argument.\n");
        return -1;
    }

    char* correct = "password1";

    if (strncmp(argv[1], correct, strlen(correct))) {
        printf("No, %s is not correct.\n", argv[1]);
        return 1;
    } else {
        printf("Yes, %s is correct!\n", argv[1]);
        return 0;
    }

}
```

As the purpose of this post is not to explain the C, I will move onto the disassembly produced on GNU/Linux Debian x86_64 krnl. 4.4.0, from the optimising GCC compiler with command `gcc -O3 -o crackme crackme.c`, and using the debugger `gdb`.

```
>gdb crackme
GNU gdb (Debian 7.12-6) 7.12.0.20161007-git
[...]
Reading symbols from crackme...(no debugging symbols found)...done.
(gdb) b main
Breakpoint 1 at 0x5c0
(gdb) r
Starting program: /home/unazed/crackme

Breakpoint 1, 0x00000000080005c0 in main ()
```

After running `disassemble` we are given the following output:

```assembly
   0x00000000080005c0 <+0>:     cmp    $0x2,%edi
   0x00000000080005c3 <+3>:     push   %rbx
   0x00000000080005c4 <+4>:     jne    0x8000614 <main+84>
   0x00000000080005c6 <+6>:     mov    0x8(%rsi),%rax
   0x00000000080005ca <+10>:    lea    0x22e(%rip),%rdi        # 0x80007ff
   0x00000000080005d1 <+17>:    mov    $0x9,%ecx
   0x00000000080005d6 <+22>:    mov    %rax,%rsi
   0x00000000080005d9 <+25>:    repz cmpsb %es:(%rdi),%ds:(%rsi)
   0x00000000080005db <+27>:    mov    %rax,%rsi
   0x00000000080005de <+30>:    seta   %bl
   0x00000000080005e1 <+33>:    setb   %dl
   0x00000000080005e4 <+36>:    sub    %edx,%ebx
   0x00000000080005e6 <+38>:    movsbl %bl,%ebx
   0x00000000080005e9 <+41>:    test   %ebx,%ebx
   0x00000000080005eb <+43>:    jne    0x80005ff <main+63>
   0x00000000080005ed <+45>:    lea    0x22d(%rip),%rdi        # 0x8000821
   0x00000000080005f4 <+52>:    xor    %eax,%eax
   0x00000000080005f6 <+54>:    callq  0x80005a0 <printf@plt>
   0x00000000080005fb <+59>:    mov    %ebx,%eax
   0x00000000080005fd <+61>:    pop    %rbx
   0x00000000080005fe <+62>:    retq
   0x00000000080005ff <+63>:    lea    0x203(%rip),%rdi        # 0x8000809
   0x0000000008000606 <+70>:    xor    %eax,%eax
   0x0000000008000608 <+72>:    mov    $0x1,%ebx
   0x000000000800060d <+77>:    callq  0x80005a0 <printf@plt>
   0x0000000008000612 <+82>:    jmp    0x80005fb <main+59>
   0x0000000008000614 <+84>:    lea    0x1c9(%rip),%rdi        # 0x80007e4
   0x000000000800061b <+91>:    or     $0xffffffff,%ebx
   0x000000000800061e <+94>:    callq  0x8000590 <puts@plt>
   0x0000000008000623 <+99>:    jmp    0x80005fb <main+59>
```

Note that, for this and any proceeding reversing posts I will (most likely) continue to use GAS/AT&T-flavoured assembly, it is not that I have any general preference over either Intel-flavoured nor AT&T-flavoured, it is simply at the ease of myself to use the latter.
Another thing to keep in mind whilst reading this is that the disassemblies will follow the LP64-model System V ABI conventions prescribed [here](https://github.com/hjl-tools/x86-psABI/wiki/X86-psABI) (under `x86-64 psABI`), that is, the first three integer parameters are passed in `%rdi`, `%rsi` and `%rbx` (and that is really all the preknowledge that is necessary for reversing this program).

Firstly, I'd like to begin with the analysis by substituting the right-hand hexadecimal addresses to their correspondent datum, this can be achieved by the GDB command `x/s <addr>` (to read strings at some `<addr>`), and so, allow me to provide these:

```
|    address  |            string              |
|-------------|--------------------------------|
| `0x80007ff` | `"password1"`                  |
| `0x8000821` | `"Yes, %s is correct!\n"`      |
| `0x8000809` | `"No, %s is not correct.\n"`   |
| `0x80007e4` | `"Need exactly one argument."` |
```

```assembly
   0x00000000080005c0 <+0>:     cmp    $0x2,%edi
   0x00000000080005c3 <+3>:     push   %rbx
   0x00000000080005c4 <+4>:     jne    0x8000614 <main+84>
```

To dive in, `+0` compares `argc` by `0x2` (recall `%[re]di` is `int argc` as defined by the CRT), hereafter preserves `%rbx` and given that the comparison was not truthy, jumps to `+84`, allow us to write parallel C code which resembles the control flow of the assembly that we observe:

```c
int
main (int argc, char **argv)
{
  if (argc != 2)
  {
    /* <...> */
  }
  /* <...> */
}
```

Now from here I'll lead to decompile everything at `+84` and to wherever it leads so that we can complete the if-clause, as we can intuitively presume that it will return from the program abruptly, as it is reached if `argc` is not equal to 2, i.e. there are not two arguments passed by the caller.

```assembly
   0x0000000008000614 <+84>:    lea    0x1c9(%rip),%rdi        # "Need exactly one argument."
   0x000000000800061b <+91>:    or     $0xffffffff,%ebx
   0x000000000800061e <+94>:    callq  0x8000590 <puts@plt>
   0x0000000008000623 <+99>:    jmp    0x80005fb <main+59>
```

We load the address of the right-hand string into the first-parameter slot of the proceeding `puts` call, hence performing `puts ("Need exactly one argument.");` and thereafter unconditionally jumping to `+59`.
*Note that `+91` simply places `0xffffffff` into `%ebx` using bitwise operations.*

```assembly
   0x00000000080005fb <+59>:    mov    %ebx,%eax
   0x00000000080005fd <+61>:    pop    %rbx
   0x00000000080005fe <+62>:    retq
```

Conclusively, we move the `0xffffffff` into `%eax` and return to the caller, effectively returning `-1` in two's complement (as the signature of the `main` function is defined `int main (int argc, char **argv, char **envp);` and `int` is a signed type.
In total these operations lead to the following C:

```c
int
main (int argc, char **argv)
{
  if (argc != 2)
  {
    puts ("Need exactly one argument.");
    return -1;
  }
  /* <...> */
}
```

Reverting back to the control flow, and passing the conditional jump with a falsey value we reach this:

```assembly
   0x00000000080005c6 <+6>:     mov    0x8(%rsi),%rax
   0x00000000080005ca <+10>:    lea    0x22e(%rip),%rdi        # "password1"
   0x00000000080005d1 <+17>:    mov    $0x9,%ecx
   0x00000000080005d6 <+22>:    mov    %rax,%rsi
   0x00000000080005d9 <+25>:    repz cmpsb %es:(%rdi),%ds:(%rsi)
   0x00000000080005db <+27>:    mov    %rax,%rsi
   0x00000000080005de <+30>:    seta   %bl
   0x00000000080005e1 <+33>:    setb   %dl
   0x00000000080005e4 <+36>:    sub    %edx,%ebx
   0x00000000080005e6 <+38>:    movsbl %bl,%ebx
   0x00000000080005e9 <+41>:    test   %ebx,%ebx
   0x00000000080005eb <+43>:    jne    0x80005ff <main+63>
```

`+6` moves `argv[1]` into `%rax` as `%rsi` contains `char **argv`, `%rdi` is populated with the address to the string `"password1"`, presumably we move `0x9` into `%ecx` as the length of the string `"password1"` is 9 characters, hereafter we move the `argv[1]` into `%rsi` for subsequent usage in the `+25` instruction which compares each byte of the respective strings until `%rcx` reaches 0. Finally, removing `argv[1]` into `%rsi` as it had been clobbered, and then setting the `%bl` and `%dl` registers with respect to the ZF/CF flags, to clarify the result we subtract the two bytes and test whether they are zero (equal), if not, jumping to `+63`, which follows:

**EDITORIAL NOTE:** `%bl` and `%dl` are only set if the strings are not equal at some part, that would mean that either one of them will be `1`, however not both, in the case they are equal both will be zero. The purpose of `+36` is actually unknown to me, it seems like the three instructions can be simplified down to `test %ebx,%edx`, `jnz 0x80005ff <main+63>`, refer to the end for a test on this.

```assembly
   0x00000000080005ff <+63>:    lea    0x203(%rip),%rdi        # "No, %s is not correct!\n"
   0x0000000008000606 <+70>:    xor    %eax,%eax
   0x0000000008000608 <+72>:    mov    $0x1,%ebx
   0x000000000800060d <+77>:    callq  0x80005a0 <printf@plt>
   0x0000000008000612 <+82>:    jmp    0x80005fb <main+59>
```

Where we simply `printf ("No, %s is not correct!\n", argv[1]);` after clearing `%eax` for the vector-count to `printf`, and thence `+72` for the near return-procedure branch to `+59`. To sum, we may glimpse at the original C source code and deduce that this is the compiler optimization done for the `strncmp` call (inlining), which is quite effective, nonetheless it would be pointless to reimplement the methodology used and instead we shall use the `strncmp` function:

**EDITORIAL NOTE:** `mov $0x1,%ebx` implies the `return 1;` directly after `+82`

```c
int
main (int argc, char **argv)
{
  if (argc != 2)
  {
    puts ("Need exactly one argument.");
    return -1;
  }
  if (strncmp(argv[1], "password1", 0x9))
  {
    printf ("No, %s is not correct!\n", argv[1]);
    return 1;
  }
}
```

And so, it would be sensical to assume that the `else` clause will simply be a `printf` of the other string, with a `return 0;` value, as unprogrammatic as it is to make assumptions like this, we may glimpse over the remaining code:

```assembly
   0x00000000080005ed <+45>:    lea    0x22d(%rip),%rdi        # "Yes, %s is correct!\n"
   0x00000000080005f4 <+52>:    xor    %eax,%eax
   0x00000000080005f6 <+54>:    callq  0x80005a0 <printf@plt>
   0x00000000080005fb <+59>:    mov    %ebx,%eax
   0x00000000080005fd <+61>:    pop    %rbx
   0x00000000080005fe <+62>:    retq
```

`+59` equates to `mov $0x0,%eax` due to the preceding clause of `jne <...>` which implies `%ebx` is 0, and hence we `return 0;` and our final C code becomes:

```c
int
main (int argc, char **argv)
{
  if (argc != 2)
  {
    puts ("Need exactly one argument.");
    return -1;
  }
  if (strncmp(argv[1], "password1", 0x9))
  {
    printf ("No, %s is not correct!\n", argv[1]);
    return 1;
  } else {
    printf ("Yes, %s is correct!\n", argv[1]);
    return 0;
  }
}
```

Now to test the optimization I suggested of `test %ebx,%edx` I will compile the program with `gcc -O3 -S crackme.c` and alter the assembly code, and recompile with `gcc -o crackme crackme.s`.
... yeah, it didn't work, it returns any input as correct, I leave it up to the reader to find out why.

Thanks for reading my first post.
