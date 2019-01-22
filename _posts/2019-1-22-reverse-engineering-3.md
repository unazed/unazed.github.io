---
layout: post
title: reverse engineering crackme 2
---

In this post, I'll be reversing the crackme provided [here](https://github.com/LeoTindall/crackmes/blob/master/crackme07.c), source:

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>

#include <time.h>

#define PASSWORD "password1"
#define PASSLEN 9

void succeed() {
    printf("Access granted!\n");
    exit(0);
}

void fail() {
    printf("Access denied.\n");
    exit(1);
}

int cur_hour() {
    time_t rawtime;
    time(&rawtime);
    if (errno != 0) {
        printf("ERROR: Could not get time: %s", strerror(errno));
        return(-1);
    }
    struct tm *current_time = localtime(&rawtime);
    if (errno != 0) {
        printf("ERROR: Could not get time: %s", strerror(errno));
        return(-1);
    }
    return current_time->tm_hour;
}

int main(int argc, char** argv) {

    if (argc != 2) {
        printf("Need exactly one argument.\n");
        return -1;
    }

    int hour = cur_hour();
    char* input = argv[1];

    if (strncmp(input, PASSWORD, PASSLEN) != 0) {
        fail();
    }

    if (hour < 5 || hour > 6) {
        fail();
    }

    succeed();
}
```

```assembly
   0x0000000008000780 <+0>:     push   %rbx
   0x0000000008000781 <+1>:     sub    $0x10,%rsp
   0x0000000008000785 <+5>:     cmp    $0x2,%edi
   0x0000000008000788 <+8>:     je     0x80007a1 <main+33>
   0x000000000800078a <+10>:    lea    0x2f0(%rip),%rdi        # 0x8000a81
   0x0000000008000791 <+17>:    callq  0x8000720 <puts@plt>
   0x0000000008000796 <+22>:    add    $0x10,%rsp
   0x000000000800079a <+26>:    mov    $0xffffffff,%eax
   0x000000000800079f <+31>:    pop    %rbx
   0x00000000080007a0 <+32>:    retq
   0x00000000080007a1 <+33>:    xor    %eax,%eax
   0x00000000080007a3 <+35>:    mov    %rsi,0x8(%rsp)
   0x00000000080007a8 <+40>:    callq  0x8000960 <cur_hour>
   0x00000000080007ad <+45>:    mov    0x8(%rsp),%rsi
   0x00000000080007b2 <+50>:    mov    $0x9,%edx
   0x00000000080007b7 <+55>:    mov    %eax,%ebx
   0x00000000080007b9 <+57>:    mov    0x8(%rsi),%rdi
   0x00000000080007bd <+61>:    lea    0x2d8(%rip),%rsi        # 0x8000a9c
   0x00000000080007c4 <+68>:    callq  0x8000710 <strncmp@plt>
   0x00000000080007c9 <+73>:    test   %eax,%eax
   0x00000000080007cb <+75>:    mov    $0x0,%eax
   0x00000000080007d0 <+80>:    jne    0x80007da <main+90>
   0x00000000080007d2 <+82>:    sub    $0x5,%ebx
   0x00000000080007d5 <+85>:    cmp    $0x1,%ebx
   0x00000000080007d8 <+88>:    jbe    0x80007df <main+95>
   0x00000000080007da <+90>:    callq  0x8000940 <fail>
   0x00000000080007df <+95>:    callq  0x8000920 <succeed>
```

```
|  address  |           string             |
|-----------|------------------------------|
| 0x8000a81 | "Need exactly one argument." |
| 0x8000a9c | "password1"                  |
```

Beginning with:

```assembly
   0x0000000008000780 <+0>:     push   %rbx
   0x0000000008000781 <+1>:     sub    $0x10,%rsp
   0x0000000008000785 <+5>:     cmp    $0x2,%edi
   0x0000000008000788 <+8>:     je     0x80007a1 <main+33>
   0x000000000800078a <+10>:    lea    0x2f0(%rip),%rdi        # "Need exactly one argument."
   0x0000000008000791 <+17>:    callq  0x8000720 <puts@plt>
   0x0000000008000796 <+22>:    add    $0x10,%rsp
   0x000000000800079a <+26>:    mov    $0xffffffff,%eax
   0x000000000800079f <+31>:    pop    %rbx
   0x00000000080007a0 <+32>:    retq
```

Equivalent to the recurring pattern of:

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

At `+33`:

```assembly
   0x00000000080007a1 <+33>:    xor    %eax,%eax
   0x00000000080007a3 <+35>:    mov    %rsi,0x8(%rsp)
   0x00000000080007a8 <+40>:    callq  0x8000960 <cur_hour>
   0x00000000080007ad <+45>:    mov    0x8(%rsp),%rsi
   0x00000000080007b2 <+50>:    mov    $0x9,%edx
   0x00000000080007b7 <+55>:    mov    %eax,%ebx
   0x00000000080007b9 <+57>:    mov    0x8(%rsi),%rdi
   0x00000000080007bd <+61>:    lea    0x2d8(%rip),%rsi        # "password1"
   0x00000000080007c4 <+68>:    callq  0x8000710 <strncmp@plt>
   0x00000000080007c9 <+73>:    test   %eax,%eax
   0x00000000080007cb <+75>:    mov    $0x0,%eax
   0x00000000080007d0 <+80>:    jne    0x80007da <main+90>
   0x00000000080007d2 <+82>:    sub    $0x5,%ebx
   0x00000000080007d5 <+85>:    cmp    $0x1,%ebx
   0x00000000080007d8 <+88>:    jbe    0x80007df <main+95>
   0x00000000080007da <+90>:    callq  0x8000940 <fail>
   0x00000000080007df <+95>:    callq  0x8000920 <succeed>
```

We see usage of the local stackframe itself with `+35` moving `argv` into `0x8(%rsp)`, hereafter calling `cur_hour` and restoring the `%rsi` register, presumably as a way of preserving `%rsi` which is not preserved across function calls, i.e. `push %rsi; call ...; pop %rsi`, then we call `strncmp (argv[1], "password1", 0x9);`; given that its result is 'not equal', it calls `fail` otherwise we take `%ebx` which is just `%eax` from `+55`, which itself is the return value of `cur_hour ();`, we subtract 5 from it and compare it to 1, if `cur_hour () - 5 <= 1` then `succeed ();`, in another sense, `cur_hour() <= 6`, or otherwise `cur_hour () - 6 = 0` (as `jbe` is unsigned, it can't be less than 0 without overflowing), in another expanded sense we could expand `+85` to `cur_hour () - 5 - 1` = `cur_hour () - 6` implies ZF/CF are either set, that is, the condition is only met if `cur_hour () = 6` or `cur_hour () = 5` since `5 - 5 <= 1` = `0 <= 1` which is true, and `6 - 5 <= 1` is `1 <= 1` which is true.

Therefore we get the following C:

**EDITORIAL NOTE:** It's quite interesting to note that GCC didn't optimize the `strncmp` as it had done before in the first post, using a `repz cmpsb` loop.

```c
UNKNOWN cur_hour (void);
UNKNOWN fail (void);
UNKNOWN succeed (void);

int
main (int argc, char **argv)
{
  if (argc != 2)
  {
    puts ("Need exactly one argument.");
    return -1;
  }
  if (strncmp (argv[1], "password1", 0x9))
  {
    fail ();
  }
  if (5 <= cur_hour() <= 6)
  {
    succeed ();
  }
}
```

Now, allow us to analyse the `fail` function, which I presume will be the fastest:

```assembly
   0x0000000008000940 <+0>:     lea    0x10d(%rip),%rdi        # "Access denied."
   0x0000000008000947 <+7>:     sub    $0x8,%rsp
   0x000000000800094b <+11>:    callq  0x8000720 <puts@plt>
   0x0000000008000950 <+16>:    mov    $0x1,%edi
   0x0000000008000955 <+21>:    callq  0x8000750 <exit@plt>
```

Equivalent to:

```c
void
fail (void)
{
  puts ("Access denied.");
  exit (1);
}
```

And now, the `succeed` function:

```assembly
   0x0000000008000920 <+0>:     lea    0x11d(%rip),%rdi        # "Access granted!"
   0x0000000008000927 <+7>:     sub    $0x8,%rsp
   0x000000000800092b <+11>:    callq  0x8000720 <puts@plt>
   0x0000000008000930 <+16>:    xor    %edi,%edi
   0x0000000008000932 <+18>:    callq  0x8000750 <exit@plt>
```

Which is, similarly:

```c
void
succeed (void)
{
  puts ("Access granted!");
  exit (0);
}
```

And now, most likely the most difficult function, `cur_hour`:

```assembly
   0x0000000008000960 <+0>:     push   %rbp
   0x0000000008000961 <+1>:     push   %rbx
   0x0000000008000962 <+2>:     sub    $0x18,%rsp
   0x0000000008000966 <+6>:     lea    0x8(%rsp),%rbp
   0x000000000800096b <+11>:    mov    %rbp,%rdi
   0x000000000800096e <+14>:    callq  0x8000740 <time@plt>
   0x0000000008000973 <+19>:    callq  0x8000700 <__errno_location@plt>
   0x0000000008000978 <+24>:    mov    (%rax),%edi
   0x000000000800097a <+26>:    test   %edi,%edi
   0x000000000800097c <+28>:    jne    0x80009a0 <cur_hour+64>
   0x000000000800097e <+30>:    mov    %rax,%rbx
   0x0000000008000981 <+33>:    mov    %rbp,%rdi
   0x0000000008000984 <+36>:    callq  0x80006f0 <localtime@plt>
   0x0000000008000989 <+41>:    mov    (%rbx),%edi
   0x000000000800098b <+43>:    test   %edi,%edi
   0x000000000800098d <+45>:    jne    0x80009a0 <cur_hour+64>
   0x000000000800098f <+47>:    mov    0x8(%rax),%eax
   0x0000000008000992 <+50>:    add    $0x18,%rsp
   0x0000000008000996 <+54>:    pop    %rbx
   0x0000000008000997 <+55>:    pop    %rbp
   0x0000000008000998 <+56>:    retq
   0x0000000008000999 <+57>:    nopl   0x0(%rax)
   0x00000000080009a0 <+64>:    callq  0x8000760 <strerror@plt>
   0x00000000080009a5 <+69>:    lea    0xb7(%rip),%rdi        # "Access denied."
   0x00000000080009ac <+76>:    mov    %rax,%rsi
   0x00000000080009af <+79>:    xor    %eax,%eax
   0x00000000080009b1 <+81>:    callq  0x8000730 <printf@plt>
   0x00000000080009b6 <+86>:    mov    $0xffffffff,%eax
   0x00000000080009bb <+91>:    jmp    0x8000992 <cur_hour+50>
```

TBF
