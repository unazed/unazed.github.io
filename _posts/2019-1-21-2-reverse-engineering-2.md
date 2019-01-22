---
layout: post
title: reverse engineering crackme 2
---

Utmost to learning is the ability of comprehension; practical knowledge is not attainable without theoretical foundation, babies don't learn to walk due to a fact that their brain 'told' them to, it was due to the visual sight and 'studying' (in a sense of that word) of others, the application of walking is hence unachievable without the theory behind walking. Although there may be little theory to walking, as it seems to yourself, it seems a monumental strife to those with underdeveloped bones, and brains which cannot fluidly register the muscle movements required to invoke 'walking'.

This may generalize to all fields of study, such as, however not limited to, reverse engineering; in the sense that, you may not feel it within your bones to be able to yet reverse any sort of program, that or you may feel bored or as if it were a _menial_ endeavor to some extent, rather requiring more time and patience (which is true, however not always). But, note that if you spend enough time around reverse engineers, and people of related study (e.g. binary exploitation or `pwn`, embedded systems development, etc.) you'll eventually get to gripes with understanding the passion and tinder behind the whole profession.

Personally, I do it because I have time and I don't have other things to do; plus it mixes into my general passion of programming and development, although it seems like reverse engineering is on a contrary to these, it is nonetheless simply problem solving.
For example: you are given some certain binary and you're asked to make it not do this certain thing which is an obstacle in terms of further regression of the binary back into its original source-code, whether it is an anti-debugging feature preventing certain dynamic analysis from progressing, or an unknown payload which could incur unknown side-effects. The end goal will always be reached by methodology of problem-solving, no matter to what quality, as for a succinct solution needs not always be the most efficient, unless there are problems that arise from such an effect.

Back to the topic at hand, a few notes which can be derived from the previous post are that optimizations at the highest level require much more consideration (from my perspective as an amateur reverse engineer) when being interpreted, although I presume as you become more fluent within reverse engineering GCC-optimized programs you will be able to spot out certain patterns of assembly correlating with a certain inline optimization, but as someone with no real experience it simply seems as a time-take from the process of reversing (especially so when it is documented, as to explain each sequence of instructions).
Another note is that a simple mistake in your writeup can be quite devestating, although thankfully the crackme I'd done was very small in size, a slight mistake that I'd made in addressing the correct strings (a mismatch) forced me to reconsider and rewrite two paragraphs (to which I still feel somewhat suspicious about). And, the final note, is that sometimes, although I understand what a sequence of instructions may do, I cannot understand for what reason there was not a certain other optimization made to reduce the size perhaps and I'm left wondering whether the optimizing compiler misoptimized something, or I simply don't understand the ISA well enough.

The crackme which I will be reversing in this post can be found [here](https://github.com/LeoTindall/crackmes/blob/master/crackme04.c):

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define CORRECT_LEN 16
#define CORRECT_SUM 1762

int main(int argc, char** argv) {

    char correct = 0;

    if (argc != 2) {
        printf("Need exactly one argument.\n");
        return -1;
    }

    int i = 0;
    int sum = 0;
    while (argv[1][i] != 0) {
        sum += argv[1][i];
        i++;
    }

    correct = (i == CORRECT_LEN) && (sum == CORRECT_SUM);

    if (correct) {
        printf("Yes, %s is correct!\n", argv[1]);
        return 0;
    } else {
        printf("No, %s is not correct.\n", argv[1]);
        return 1;
    }
}
```

I will be compiling this with `gcc -O3 -o crackme crackme.c` and using `gdb` with the same operating system mentioned in the last post.

```assembly
   0x00000000080005c0 <+0>:     sub    $0x8,%rsp
   0x00000000080005c4 <+4>:     cmp    $0x2,%edi
   0x00000000080005c7 <+7>:     jne    0x8000626 <main+102>
   0x00000000080005c9 <+9>:     mov    0x8(%rsi),%rsi
   0x00000000080005cd <+13>:    xor    %ecx,%ecx
   0x00000000080005cf <+15>:    mov    $0x1,%edx
   0x00000000080005d4 <+20>:    movsbl (%rsi),%eax
   0x00000000080005d7 <+23>:    test   %al,%al
   0x00000000080005d9 <+25>:    je     0x800060e <main+78>
   0x00000000080005db <+27>:    nopl   0x0(%rax,%rax,1)
   0x00000000080005e0 <+32>:    mov    %edx,%edi
   0x00000000080005e2 <+34>:    add    $0x1,%rdx
   0x00000000080005e6 <+38>:    add    %eax,%ecx
   0x00000000080005e8 <+40>:    movsbl -0x1(%rsi,%rdx,1),%eax
   0x00000000080005ed <+45>:    test   %al,%al
   0x00000000080005ef <+47>:    jne    0x80005e0 <main+32>
   0x00000000080005f1 <+49>:    cmp    $0x10,%edi
   0x00000000080005f4 <+52>:    jne    0x800060e <main+78>
   0x00000000080005f6 <+54>:    cmp    $0x6e2,%ecx
   0x00000000080005fc <+60>:    jne    0x800060e <main+78>
   0x00000000080005fe <+62>:    lea    0x20a(%rip),%rdi        # 0x800080f
   0x0000000008000605 <+69>:    callq  0x80005a0 <printf@plt>
   0x000000000800060a <+74>:    xor    %eax,%eax
   0x000000000800060c <+76>:    jmp    0x8000621 <main+97>
   0x000000000800060e <+78>:    lea    0x20f(%rip),%rdi        # 0x8000824
   0x0000000008000615 <+85>:    xor    %eax,%eax
   0x0000000008000617 <+87>:    callq  0x80005a0 <printf@plt>
   0x000000000800061c <+92>:    mov    $0x1,%eax
   0x0000000008000621 <+97>:    add    $0x8,%rsp
   0x0000000008000625 <+101>:   retq
   0x0000000008000626 <+102>:   lea    0x1c7(%rip),%rdi        # 0x80007f4
   0x000000000800062d <+109>:   callq  0x8000590 <puts@plt>
   0x0000000008000632 <+114>:   or     $0xffffffff,%eax
   0x0000000008000635 <+117>:   jmp    0x8000621 <main+97>
```

To begin, allow me to make the address to string mapping:

```
|  address  |           string             |
|-----------|------------------------------|
| 0x800080f | "Yes, %s is correct!\n"      |
| 0x8000824 | "No, %s is not correct.\n"   |
| 0x80007f4 | "Need exactly one argument." |
```

And to begin:

```assembly
   0x00000000080005c0 <+0>:     sub    $0x8,%rsp
   0x00000000080005c4 <+4>:     cmp    $0x2,%edi
   0x00000000080005c7 <+7>:     jne    0x8000626 <main+102>
   [...]
   0x0000000008000626 <+102>:   lea    0x1c7(%rip),%rdi        # "Need exactly one argument."
   0x000000000800062d <+109>:   callq  0x8000590 <puts@plt>
   0x0000000008000632 <+114>:   or     $0xffffffff,%eax
   0x0000000008000635 <+117>:   jmp    0x8000621 <main+97>
   [...]
   0x0000000008000621 <+97>:    add    $0x8,%rsp
   0x0000000008000625 <+101>:   retq
```

Trivially, we may deduce that this is simply:

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

And to move on:

```assembly
   0x00000000080005c9 <+9>:     mov    0x8(%rsi),%rsi
   0x00000000080005cd <+13>:    xor    %ecx,%ecx
   0x00000000080005cf <+15>:    mov    $0x1,%edx
   0x00000000080005d4 <+20>:    movsbl (%rsi),%eax
   0x00000000080005d7 <+23>:    test   %al,%al
   0x00000000080005d9 <+25>:    je     0x800060e <main+78>
```

`%rsi` becomes `argv[1]`, clear `%ecx`, set `%edx` to 1, move `argv[1][0]` to `%eax` with sign extension, thereafter testing if the character is `\0` and jumping to `+78` which we could assume is a fail procedure.

```assembly
   0x000000000800060e <+78>:    lea    0x20f(%rip),%rdi        # "No, %s is not correct.\n"
   0x0000000008000615 <+85>:    xor    %eax,%eax
   0x0000000008000617 <+87>:    callq  0x80005a0 <printf@plt>
   0x000000000800061c <+92>:    mov    $0x1,%eax
   0x0000000008000621 <+97>:    add    $0x8,%rsp
   0x0000000008000625 <+101>:   retq
```

And that it is, equivalent to `printf ("No, %s is not correct.\n", argv[1]);`, `return 1;`, otherwise we go to `+32`:

```c
int
main (int argc, char **argv)
{
  if (argc != 2)
  {
    puts ("Need exactly one argument.");
    return -1;
  }
  if (!argv[1][0])
  {
    printf ("No, %s is not correct.\n", argv[1]);
    return 1;
  }
  /* <...> */
}
```

```assembly
   0x00000000080005e0 <+32>:    mov    %edx,%edi
   0x00000000080005e2 <+34>:    add    $0x1,%rdx
   0x00000000080005e6 <+38>:    add    %eax,%ecx
   0x00000000080005e8 <+40>:    movsbl -0x1(%rsi,%rdx,1),%eax
   0x00000000080005ed <+45>:    test   %al,%al
   0x00000000080005ef <+47>:    jne    0x80005e0 <main+32>
   0x00000000080005f1 <+49>:    cmp    $0x10,%edi
   0x00000000080005f4 <+52>:    jne    0x800060e <main+78>
   0x00000000080005f6 <+54>:    cmp    $0x6e2,%ecx
   0x00000000080005fc <+60>:    jne    0x800060e <main+78>
   0x00000000080005fe <+62>:    lea    0x20a(%rip),%rdi        # "Yes, %s is correct!\n"
   0x0000000008000605 <+69>:    callq  0x80005a0 <printf@plt>
   0x000000000800060a <+74>:    xor    %eax,%eax
   0x000000000800060c <+76>:    jmp    0x8000621 <main+97>
```

Before we go into analysing this, recall: `%ecx` = 0 and `%edx` = 1 (before the loop is iterated), `+97` is a return proc., `+78` is a fail proc., `%eax` is the first character, and `+32` is the start. `+40` is equivalent to moving the sign-extended version of `-0x1(%rsi + %rdx)` into `%eax`, where `%rsi` is `argv[1]` and `%edx` is an increasing amount as deduced from `+34`, therefore `-0x1(argv[1] + %edx)` is essentially `argv[1][%edx - 1]` for ever-increasing values of `%edx`, so `%eax` contains each consecutive byte of the `argv[1]` string, then we test the character by itself, if it's not zero then we restart the loop (note: `%ecx` accumulates the characters).
From this perspective it actually appears that there is a possible buffer overrun given that `argv[1]` is not a C-string, therefore running into undefined memory, which is most likely why it also could run forever given that the character is never `\0`.
Finally, if the character is zero, it compares the string's length to 16 (due to `+32` moving the string's length into `%edi`), presumably jumps to a fail procedure if it is not equal, otherwise also compares the accumulator `%ecx` to `0x6e2`, and if equal then `printf ("Yes, %s is correct!\n", argv[1]);`.

Now to construct this assembly back into C, we can represent it as a do-while loop:

```c
int
main (int argc, char **argv)
{
  if (argc != 2)
    {
      puts ("Need exactly one argument.");
      return -1;
    }
  if (!argv[1][0])
    {
      printf ("No, %s is not correct.\n", argv[1]);
      return 1;
    }
  size_t acc = 0;
  size_t length = 0;

  do
    {
      acc += argv[1][length++];
    }
  while (argv[1][length]);

  if (length != 16)
    {
      printf ("No, %s is not correct.\n", argv[1]);
      return 1;
    }
  if (acc == 0x6e2)
    {
      printf ("Yes, %s is correct!\n", argv[1]);
      return 0;
    }
}
```

Which, finally functions as intended.

See you in the next post.
