---
layout: post
title: reverse engineering crackme 4
---

For this challenge, I've decided that I should leave this certain repository LeoTindall has made [here](https://github.com/LeoTindall/crackmes), and so I will be trying to reverse the final challenge located [here](https://github.com/LeoTindall/crackmes/blob/master/crackme08e.c), source:

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <cpuid.h>

void succeed(char* string) {
    printf("Yes, %s is correct!\n", string);
    exit(0);
}

void fail(char* string) {
    printf("No, %s is not correct.\n", string);
    exit(1);
}

void shift_int_to_char(int i, char* buff) {
    buff[0] = (i) & 0xFF;
    buff[1] = (i >> 8) & 0xFF;
    buff[2] = (i >> 16) & 0xFF;
    buff[3] = (i >> 24) & 0xFF;
}

int main(int argc, char** argv) {

    if (argc != 2) {
        printf("Need exactly one argument.\n");
        return -1;
    }

    unsigned int eax, ebx, ecx, edx;
    char* buff = malloc(sizeof(char) * 15);
    __get_cpuid(0, &eax, &ebx, &ecx, &edx);
    buff[0] = 'N';
    shift_int_to_char(ebx, buff + 1);
    shift_int_to_char(edx, buff + 5);
    shift_int_to_char(ecx, buff + 9);
    buff[13] = 'Q';
    buff[14] = '\0';
    
    int correct = (strcmp(buff, argv[1]) == 0);
    free(buff);

    if (correct) {
        succeed(argv[1]);
    } else {
        fail(argv[1]);
    }
}
```

Compiled, as usual, with `gcc -O3 -o crackme crackme.c`:

```assembly
   0x00000000080006e0 <+0>:     push   %r14
   0x00000000080006e2 <+2>:     push   %r13
   0x00000000080006e4 <+4>:     push   %r12
   0x00000000080006e6 <+6>:     push   %rbp
   0x00000000080006e7 <+7>:     push   %rbx
   0x00000000080006e8 <+8>:     sub    $0x10,%rsp
   0x00000000080006ec <+12>:    cmp    $0x2,%edi
   0x00000000080006ef <+15>:    je     0x800070f <main+47>
   0x00000000080006f1 <+17>:    lea    0x329(%rip),%rdi        # 0x8000a21
   0x00000000080006f8 <+24>:    callq  0x8000680 <puts@plt>
   0x00000000080006fd <+29>:    add    $0x10,%rsp
   0x0000000008000701 <+33>:    mov    $0xffffffff,%eax
   0x0000000008000706 <+38>:    pop    %rbx
   0x0000000008000707 <+39>:    pop    %rbp
   0x0000000008000708 <+40>:    pop    %r12
   0x000000000800070a <+42>:    pop    %r13
   0x000000000800070c <+44>:    pop    %r14
   0x000000000800070e <+46>:    retq
   0x000000000800070f <+47>:    mov    $0xf,%edi
   0x0000000008000714 <+52>:    mov    %rsi,0x8(%rsp)
   0x0000000008000719 <+57>:    callq  0x80006b0 <malloc@plt>
   0x000000000800071e <+62>:    xor    %edi,%edi
   0x0000000008000720 <+64>:    mov    %rax,%rbp
   0x0000000008000723 <+67>:    mov    0x8(%rsp),%rsi
   0x0000000008000728 <+72>:    mov    %edi,%eax
   0x000000000800072a <+74>:    cpuid
   0x000000000800072c <+76>:    test   %eax,%eax
   0x000000000800072e <+78>:    jne    0x80007c6 <main+230>
   0x0000000008000734 <+84>:    mov    %r14d,%eax
   0x0000000008000737 <+87>:    mov    %r12b,0x9(%rbp)
   0x000000000800073b <+91>:    mov    %r14b,0x1(%rbp)
   0x000000000800073f <+95>:    sar    $0x8,%eax
   0x0000000008000742 <+98>:    mov    %r13b,0x5(%rbp)
   0x0000000008000746 <+102>:   mov    %rbp,%rdi
   0x0000000008000749 <+105>:   mov    %al,0x2(%rbp)
   0x000000000800074c <+108>:   mov    %r14d,%eax
   0x000000000800074f <+111>:   shr    $0x18,%r14d
   0x0000000008000753 <+115>:   sar    $0x10,%eax
   0x0000000008000756 <+118>:   movb   $0x4e,0x0(%rbp)
   0x000000000800075a <+122>:   mov    %r14b,0x4(%rbp)
   0x000000000800075e <+126>:   mov    %al,0x3(%rbp)
   0x0000000008000761 <+129>:   mov    %r13d,%eax
   0x0000000008000764 <+132>:   movb   $0x51,0xd(%rbp)
   0x0000000008000768 <+136>:   sar    $0x8,%eax
   0x000000000800076b <+139>:   movb   $0x0,0xe(%rbp)
   0x000000000800076f <+143>:   mov    %al,0x6(%rbp)
   0x0000000008000772 <+146>:   mov    %r13d,%eax
   0x0000000008000775 <+149>:   shr    $0x18,%r13d
   0x0000000008000779 <+153>:   sar    $0x10,%eax
   0x000000000800077c <+156>:   mov    %r13b,0x8(%rbp)
   0x0000000008000780 <+160>:   mov    %al,0x7(%rbp)
   0x0000000008000783 <+163>:   mov    %r12d,%eax
   0x0000000008000786 <+166>:   sar    $0x8,%eax
   0x0000000008000789 <+169>:   mov    %al,0xa(%rbp)
   0x000000000800078c <+172>:   mov    %r12d,%eax
   0x000000000800078f <+175>:   shr    $0x18,%r12d
   0x0000000008000793 <+179>:   mov    %r12b,0xc(%rbp)
   0x0000000008000797 <+183>:   mov    0x8(%rsi),%r12
   0x000000000800079b <+187>:   sar    $0x10,%eax
   0x000000000800079e <+190>:   mov    %al,0xb(%rbp)
   0x00000000080007a1 <+193>:   mov    %r12,%rsi
   0x00000000080007a4 <+196>:   callq  0x80006a0 <strcmp@plt>
   0x00000000080007a9 <+201>:   mov    %rbp,%rdi
   0x00000000080007ac <+204>:   mov    %eax,%r13d
   0x00000000080007af <+207>:   callq  0x8000670 <free@plt>
   0x00000000080007b4 <+212>:   test   %r13d,%r13d
   0x00000000080007b7 <+215>:   mov    %r12,%rdi
   0x00000000080007ba <+218>:   jne    0x80007c1 <main+225>
   0x00000000080007bc <+220>:   callq  0x8000910 <succeed>
   0x00000000080007c1 <+225>:   callq  0x8000930 <fail>
   0x00000000080007c6 <+230>:   mov    %edi,%eax
   0x00000000080007c8 <+232>:   cpuid
   0x00000000080007ca <+234>:   mov    %ebx,%r14d
   0x00000000080007cd <+237>:   mov    %ecx,%r12d
   0x00000000080007d0 <+240>:   mov    %edx,%r13d
   0x00000000080007d3 <+243>:   jmpq   0x8000734 <main+84>
```

Strings:

```
|  address  |           string             |
|-----------|------------------------------|
| 0x8000a21 | "Need exactly one argument." |
```

As this is a bigger binary, I will read over the binary and pinpoint certain branch locations with immediate context, and make certain notes:

```
|   offset   |                      deduction                       |
|------------|------------------------------------------------------|
| <main+47>  | continuation after successful entry                  |
| <main+230> | initialization with `cpuid` and leads to `<main+84>` |
| <main+225> | fail procedure                                       |
| <main+84>  | primary logic, bunch of bitwise operations           |

NOTES:

The program only has two points of failure, one for the unexpected `argc` and one for after the primary logic check, at `+225 <fail>`
```

```assembly
   0x00000000080006e0 <+0>:     push   %r14
   0x00000000080006e2 <+2>:     push   %r13
   0x00000000080006e4 <+4>:     push   %r12
   0x00000000080006e6 <+6>:     push   %rbp
   0x00000000080006e7 <+7>:     push   %rbx
   0x00000000080006e8 <+8>:     sub    $0x10,%rsp
   0x00000000080006ec <+12>:    cmp    $0x2,%edi
   0x00000000080006ef <+15>:    je     0x800070f <main+47>
   0x00000000080006f1 <+17>:    lea    0x329(%rip),%rdi        # "Need exactly one argument."
   0x00000000080006f8 <+24>:    callq  0x8000680 <puts@plt>
   0x00000000080006fd <+29>:    add    $0x10,%rsp
   0x0000000008000701 <+33>:    mov    $0xffffffff,%eax
   0x0000000008000706 <+38>:    pop    %rbx
   0x0000000008000707 <+39>:    pop    %rbp
   0x0000000008000708 <+40>:    pop    %r12
   0x000000000800070a <+42>:    pop    %r13
   0x000000000800070c <+44>:    pop    %r14
   0x000000000800070e <+46>:    retq
```

Generic entry as is for previous crackmes:

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

Then:

```assembly
   0x000000000800070f <+47>:    mov    $0xf,%edi
   0x0000000008000714 <+52>:    mov    %rsi,0x8(%rsp)
   0x0000000008000719 <+57>:    callq  0x80006b0 <malloc@plt>
   0x000000000800071e <+62>:    xor    %edi,%edi
   0x0000000008000720 <+64>:    mov    %rax,%rbp
   0x0000000008000723 <+67>:    mov    0x8(%rsp),%rsi
   0x0000000008000728 <+72>:    mov    %edi,%eax
   0x000000000800072a <+74>:    cpuid
   0x000000000800072c <+76>:    test   %eax,%eax
   0x000000000800072e <+78>:    jne    0x80007c6 <main+230>
```

We save `argv` at `0x8(%rsp)`, allocate a 15 byte buffer at `%rbp` and call `cpuid` with a parameter of 0; therefore by (this table)[https://c9x.me/x86/html/file_module_x86_id_45.html] we can deduce that, `%eax` will contain something, `%ebx` will contain the four bytes `"Genu"`, `%ecx` will contain `"ntel"` and `%edx` will contain `"ineI"`.

We can cut the entire reversing short by setting a breakpoint on `+196` and doing an `i r` and getting the `%rdi` register, tracing it to the string and voila:

```
(gdb) b *0x00000000080007a4
Breakpoint 3 at 0x80007a4
(gdb) r arg
Starting program: /home/unazed/crackme arg

Breakpoint 3, 0x00000000080007a4 in main ()
(gdb) i r
[...]
rdi            0x8402010        138420240
[...]
(gdb) x/s 0x8402010
0x8402010:      "NGenuineIntelQ"
```

Afterwards, plugging in `"NGenuineIntelQ"` to see whether it works:

```
>./crackme "NGenuineIntelQ"
Yes, NGenuineIntelQ is correct!
```

Although this form of reverse engineering where you trace and pinpoint certain strings in the programs, breakpointing important calls like `strncmp`, etc., is useful in this context since I know that the program isn't malicious and hence not requiring of any more control-flow analysis, but in contexts where you have arbitrary code it is much better to analyse where the rest of the code leads and further decompile the program, as it is safer and more reliable.

Thanks for reading.
