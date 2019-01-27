---
layout: post
title: reverse engineering crackme 7 & 8
---

Slightly changing up the format of this post as I'll be doing two crackmes, both of difficulty 1, one being `JustSee` [here](https://crackmes.one/crackme/5b81014933c5d41f5c6ba944) and the other called `WhiteRabbit` [here](https://crackmes.one/crackme/5c11e2f333c5d41e58e0057a):
I will begin with `JustSee`:

```assembly
   0x0000000000400686 <+0>:     push   %rbp
   0x0000000000400687 <+1>:     mov    %rsp,%rbp
   0x000000000040068a <+4>:     sub    $0x40,%rsp
   0x000000000040068e <+8>:     mov    %fs:0x28,%rax
   0x0000000000400697 <+17>:    mov    %rax,-0x8(%rbp)
   0x000000000040069b <+21>:    xor    %eax,%eax
   0x000000000040069d <+23>:    mov    $0x4007d4,%edi
   0x00000000004006a2 <+28>:    callq  0x400520 <puts@plt>
   0x00000000004006a7 <+33>:    mov    $0x4007dd,%edi
   0x00000000004006ac <+38>:    callq  0x400520 <puts@plt>
   0x00000000004006b1 <+43>:    mov    $0x4007ef,%edi
   0x00000000004006b6 <+48>:    mov    $0x0,%eax
   0x00000000004006bb <+53>:    callq  0x400540 <printf@plt>
   0x00000000004006c0 <+58>:    lea    -0x40(%rbp),%rax
   0x00000000004006c4 <+62>:    mov    %rax,%rsi
   0x00000000004006c7 <+65>:    mov    $0x4007fc,%edi
   0x00000000004006cc <+70>:    mov    $0x0,%eax
   0x00000000004006d1 <+75>:    callq  0x400570 <__isoc99_scanf@plt>
   0x00000000004006d6 <+80>:    movabs $0x7334457b67616c46,%rax
   0x00000000004006e0 <+90>:    mov    %rax,-0x20(%rbp)
   0x00000000004006e4 <+94>:    movabs $0x7d6c6c3468635f79,%rax
   0x00000000004006ee <+104>:   mov    %rax,-0x18(%rbp)
   0x00000000004006f2 <+108>:   movl   $0x0,-0x10(%rbp)
   0x00000000004006f9 <+115>:   lea    -0x20(%rbp),%rdx
   0x00000000004006fd <+119>:   lea    -0x40(%rbp),%rax
   0x0000000000400701 <+123>:   mov    %rdx,%rsi
   0x0000000000400704 <+126>:   mov    %rax,%rdi
   0x0000000000400707 <+129>:   callq  0x400560 <strcmp@plt>
   0x000000000040070c <+134>:   test   %eax,%eax
   0x000000000040070e <+136>:   jne    0x40071c <main+150>
   0x0000000000400710 <+138>:   mov    $0x4007ff,%edi
   0x0000000000400715 <+143>:   callq  0x400520 <puts@plt>
   0x000000000040071a <+148>:   jmp    0x400726 <main+160>
   0x000000000040071c <+150>:   mov    $0x400805,%edi
   0x0000000000400721 <+155>:   callq  0x400520 <puts@plt>
   0x0000000000400726 <+160>:   mov    $0x0,%eax
   0x000000000040072b <+165>:   mov    -0x8(%rbp),%rcx
   0x000000000040072f <+169>:   xor    %fs:0x28,%rcx
   0x0000000000400738 <+178>:   je     0x40073f <main+185>
   0x000000000040073a <+180>:   callq  0x400530 <__stack_chk_fail@plt>
   0x000000000040073f <+185>:   leaveq
   0x0000000000400740 <+186>:   retq
```

An interesting an unrelated thing which would be interesting to learn regards the lines, `+8:+21` and `+165:+180`, which are the stack canary checking procedures to ensure no stack overflows occur by using a stack cookie I presume and XORing it after the main procedure is finished. Although this is quite simple, `mov %fs:0x28,%rax` moves the canary value into `%rax`, and saves it at the lowest possible offset of the stack at `-0x8(%rbp)`, then at `+165` we reload the old value into `%rcx` and `xor` it against the actual canary value in `%fs:0x28`, if the values are not the same then `__stack_chk_fail` is called which alerts to the program that stack corruption has occurred, and hence performs necessary measures, otherwise it returns normally if they are the same.

Anyway, back onto the main part of the program, it is notable that this program uses absolute direct addressing opposed to traditional RIP-relative addressing:

```assembly
   0x000000000040069d <+23>:    mov    $0x4007d4,%edi
   0x00000000004006a2 <+28>:    callq  0x400520 <puts@plt>
   0x00000000004006a7 <+33>:    mov    $0x4007dd,%edi
   0x00000000004006ac <+38>:    callq  0x400520 <puts@plt>
   0x00000000004006b1 <+43>:    mov    $0x4007ef,%edi
   0x00000000004006b6 <+48>:    mov    $0x0,%eax
   0x00000000004006bb <+53>:    callq  0x400540 <printf@plt>
   0x00000000004006c0 <+58>:    lea    -0x40(%rbp),%rax
   0x00000000004006c4 <+62>:    mov    %rax,%rsi
   0x00000000004006c7 <+65>:    mov    $0x4007fc,%edi
   0x00000000004006cc <+70>:    mov    $0x0,%eax
   0x00000000004006d1 <+75>:    callq  0x400570 <__isoc99_scanf@plt>
```

Equivalent to:

```c
int
main (int argc, char **argv)
{
  char input[16];
  puts ("Hello ! ");
  puts ("Give Me Your Flag");
  printf ("Check Flag: ");
  scanf ("%s", &input);
  /* ... */
}
```

Continuing:

```assembly
   0x00000000004006d6 <+80>:    movabs $0x7334457b67616c46,%rax
   0x00000000004006e0 <+90>:    mov    %rax,-0x20(%rbp)
   0x00000000004006e4 <+94>:    movabs $0x7d6c6c3468635f79,%rax
   0x00000000004006ee <+104>:   mov    %rax,-0x18(%rbp)
   0x00000000004006f2 <+108>:   movl   $0x0,-0x10(%rbp)
   0x00000000004006f9 <+115>:   lea    -0x20(%rbp),%rdx
   0x00000000004006fd <+119>:   lea    -0x40(%rbp),%rax
   0x0000000000400701 <+123>:   mov    %rdx,%rsi
   0x0000000000400704 <+126>:   mov    %rax,%rdi
   0x0000000000400707 <+129>:   callq  0x400560 <strcmp@plt>
   0x000000000040070c <+134>:   test   %eax,%eax
   0x000000000040070e <+136>:   jne    0x40071c <main+150>
   0x0000000000400710 <+138>:   mov    $0x4007ff,%edi
   0x0000000000400715 <+143>:   callq  0x400520 <puts@plt>
   0x000000000040071a <+148>:   jmp    0x400726 <main+160>
   0x000000000040071c <+150>:   mov    $0x400805,%edi
   0x0000000000400721 <+155>:   callq  0x400520 <puts@plt>
```

I save time by doing `b *0x0000000000400707; x/s $rsi` gives `0x7ffffffee120: "Flag{E4sy_ch4ll}"`, although it is valuable understanding the `movabs` instruction and how the string even got there, so allow me to iterate line-by-line. `+80` moves `0x7334457b67616c46` into `-0x20(%rbp)` adjacent to `0x7d6c6c3468635f79` in `-0x18(%rbp)`, afterwards we load the first big constant into `%rdx` and the input buffer into `%rax`, doing a `strcmp (0x7d6c6c3468635f79, input)`, which would require noticing that due to the adjacency of the strings, and the fact that the input buffer is buffers, the buffer is actually: `0x7334457b67616c46` plus `0x7d6c6c3468635f79` which is just:

```py
>>> "\x73\x34\x45\x7b\x67\x61\x6c\x46"[::-1] + "\x7d\x6c\x6c\x34\x68\x63\x5f\x79"[::-1]
'Flag{E4sy_ch4ll}'
```

Anyway, just to verify:

```
>./just\ see Flag{E4sy_ch4ll}
Hello !
Give Me Your Flag
Check Flag: Flag{E4sy_ch4ll}
G00d
```

Now onto the `WhiteRabbit` challenge, here is the disassembly:

```assembly
   0x00000000000011d5 <+0>:     push   %rbp
   0x00000000000011d6 <+1>:     mov    %rsp,%rbp
   0x00000000000011d9 <+4>:     lea    0xe58(%rip),%rdi        # 0x2038
   0x00000000000011e0 <+11>:    callq  0x1030 <puts@plt>
   0x00000000000011e5 <+16>:    lea    0xe6c(%rip),%rdi        # 0x2058
   0x00000000000011ec <+23>:    mov    $0x0,%eax
   0x00000000000011f1 <+28>:    callq  0x1040 <printf@plt>
   0x00000000000011f6 <+33>:    lea    0xe63(%rip),%rdi        # 0x2060
   0x00000000000011fd <+40>:    callq  0x1030 <puts@plt>
   0x0000000000001202 <+45>:    mov    $0x0,%eax
   0x0000000000001207 <+50>:    pop    %rbp
   0x0000000000001208 <+51>:    retq
```

The strings are irrelevant, as there is no input, the point of this is to figure out the hidden function which is quite easy as it's named `secret`:

```assembly
   0x0000000000001145 <+0>:     push   %rbp
   0x0000000000001146 <+1>:     mov    %rsp,%rbp
   0x0000000000001149 <+4>:     sub    $0x10,%rsp
   0x000000000000114d <+8>:     movl   $0x5,-0x4(%rbp)
   0x0000000000001154 <+15>:    movl   $0x3,-0x8(%rbp)
   0x000000000000115b <+22>:    movl   $0x4,-0xc(%rbp)
   0x0000000000001162 <+29>:    movb   $0x73,-0xd(%rbp)
   0x0000000000001166 <+33>:    movb   $0x64,-0xe(%rbp)
   0x000000000000116a <+37>:    movb   $0x63,-0xf(%rbp)
   0x000000000000116e <+41>:    movsbl -0xd(%rbp),%r9d
   0x0000000000001173 <+46>:    mov    -0x4(%rbp),%eax
   0x0000000000001176 <+49>:    sub    -0xc(%rbp),%eax
   0x0000000000001179 <+52>:    mov    %eax,%r8d
   0x000000000000117c <+55>:    movsbl -0xe(%rbp),%edi
   0x0000000000001180 <+59>:    mov    -0x4(%rbp),%eax
   0x0000000000001183 <+62>:    sub    -0xc(%rbp),%eax
   0x0000000000001186 <+65>:    mov    %eax,%esi
   0x0000000000001188 <+67>:    movsbl -0xe(%rbp),%r10d
   0x000000000000118d <+72>:    movsbl -0xf(%rbp),%ecx
   0x0000000000001191 <+76>:    movsbl -0xd(%rbp),%edx
   0x0000000000001195 <+80>:    mov    -0x8(%rbp),%eax
   0x0000000000001198 <+83>:    pushq  $0x0
   0x000000000000119a <+85>:    pushq  $0x0
   0x000000000000119c <+87>:    push   %r9
   0x000000000000119e <+89>:    pushq  $0x0
   0x00000000000011a0 <+91>:    push   %r8
   0x00000000000011a2 <+93>:    mov    -0xc(%rbp),%r8d
   0x00000000000011a6 <+97>:    push   %r8
   0x00000000000011a8 <+99>:    mov    -0x8(%rbp),%r8d
   0x00000000000011ac <+103>:   push   %r8
   0x00000000000011ae <+105>:   pushq  $0x0
   0x00000000000011b0 <+107>:   push   %rdi
   0x00000000000011b1 <+108>:   push   %rsi
   0x00000000000011b2 <+109>:   mov    %r10d,%r9d
   0x00000000000011b5 <+112>:   mov    $0x0,%r8d
   0x00000000000011bb <+118>:   mov    %eax,%esi
   0x00000000000011bd <+120>:   lea    0xe44(%rip),%rdi        # 0x2008
   0x00000000000011c4 <+127>:   mov    $0x0,%eax
   0x00000000000011c9 <+132>:   callq  0x1040 <printf@plt>
   0x00000000000011ce <+137>:   add    $0x50,%rsp
   0x00000000000011d2 <+141>:   nop
   0x00000000000011d3 <+142>:   leaveq
   0x00000000000011d4 <+143>:   retq
```

Also no need to look at the strings, as we can `b *0x00000000000011d4` and `set $rip = 0x0000000000001145; c`:

```
(gdb) set $rip = 0x0000000008001145
(gdb) b *0x00000000080011d4
Breakpoint 5 at 0x80011d4
(gdb) c
Continuing.
flag{3sc0nd1d0_3h_M41s_G0st0S0}

Breakpoint 5, 0x00000000080011d4 in secret ()
```

Easy.

Thanks for reading.
