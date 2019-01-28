---
layout: post
title: reverse engineering crackme 9
---

Slightly digressing to seemingly harder crackmes, this time, [jumpjumpjump](https://crackmes.one/crackme/5c1a939633c5d41e58e005d1):

```assembly
   0x00000000080011ca <+0>:     push   %rbp
   0x00000000080011cb <+1>:     mov    %rsp,%rbp
   0x00000000080011ce <+4>:     push   %rbx
   0x00000000080011cf <+5>:     sub    $0x88,%rsp
   0x00000000080011d6 <+12>:    movl   $0x0,-0x14(%rbp)
   0x00000000080011dd <+19>:    lea    0xe24(%rip),%rdi        # 0x8002008
   0x00000000080011e4 <+26>:    callq  0x8001040 <puts@plt>
   0x00000000080011e9 <+31>:    mov    0x2e60(%rip),%rdx        # 0x8004050 <stdin@@GLIBC_2.2.5>
   0x00000000080011f0 <+38>:    lea    -0x90(%rbp),%rax
   0x00000000080011f7 <+45>:    mov    $0x64,%esi
   0x00000000080011fc <+50>:    mov    %rax,%rdi
   0x00000000080011ff <+53>:    callq  0x8001070 <fgets@plt>
   0x0000000008001204 <+58>:    lea    -0x90(%rbp),%rax
   0x000000000800120b <+65>:    mov    %rax,%rdi
   0x000000000800120e <+68>:    callq  0x8001050 <strlen@plt>
   0x0000000008001213 <+73>:    cmp    $0xb,%rax
   0x0000000008001217 <+77>:    jbe    0x800122f <main+101>
   0x0000000008001219 <+79>:    lea    0xe00(%rip),%rdi        # 0x8002020
   0x0000000008001220 <+86>:    callq  0x8001040 <puts@plt>
   0x0000000008001225 <+91>:    mov    $0x0,%eax
   0x000000000800122a <+96>:    jmpq   0x80012e2 <main+280>
   0x000000000800122f <+101>:   movl   $0x0,-0x18(%rbp)
   0x0000000008001236 <+108>:   jmp    0x800124f <main+133>
   0x0000000008001238 <+110>:   mov    -0x18(%rbp),%eax
   0x000000000800123b <+113>:   cltq
   0x000000000800123d <+115>:   movzbl -0x90(%rbp,%rax,1),%eax
   0x0000000008001245 <+123>:   movsbl %al,%eax
   0x0000000008001248 <+126>:   add    %eax,-0x14(%rbp)
   0x000000000800124b <+129>:   addl   $0x1,-0x18(%rbp)
   0x000000000800124f <+133>:   mov    -0x18(%rbp),%eax
   0x0000000008001252 <+136>:   movslq %eax,%rbx
   0x0000000008001255 <+139>:   lea    -0x90(%rbp),%rax
   0x000000000800125c <+146>:   mov    %rax,%rdi
   0x000000000800125f <+149>:   callq  0x8001050 <strlen@plt>
   0x0000000008001264 <+154>:   cmp    %rax,%rbx
   0x0000000008001267 <+157>:   jb     0x8001238 <main+110>
   0x0000000008001269 <+159>:   cmpl   $0x3e8,-0x14(%rbp)
   0x0000000008001270 <+166>:   jne    0x80012d1 <main+263>
   0x0000000008001272 <+168>:   mov    $0x0,%eax
   0x0000000008001277 <+173>:   callq  0x8001175 <strcat_str>
   0x000000000800127c <+178>:   mov    %rax,-0x20(%rbp)
   0x0000000008001280 <+182>:   lea    0xdbd(%rip),%rdi        # 0x8002044
   0x0000000008001287 <+189>:   mov    $0x0,%eax
   0x000000000800128c <+194>:   callq  0x8001060 <printf@plt>
   0x0000000008001291 <+199>:   movl   $0x0,-0x18(%rbp)
   0x0000000008001298 <+206>:   jmp    0x80012b8 <main+238>
   0x000000000800129a <+208>:   mov    -0x18(%rbp),%eax
   0x000000000800129d <+211>:   movslq %eax,%rdx
   0x00000000080012a0 <+214>:   mov    -0x20(%rbp),%rax
   0x00000000080012a4 <+218>:   add    %rdx,%rax
   0x00000000080012a7 <+221>:   movzbl (%rax),%eax
   0x00000000080012aa <+224>:   movsbl %al,%eax
   0x00000000080012ad <+227>:   mov    %eax,%edi
   0x00000000080012af <+229>:   callq  0x8001030 <putchar@plt>
   0x00000000080012b4 <+234>:   addl   $0x1,-0x18(%rbp)
   0x00000000080012b8 <+238>:   cmpl   $0x9,-0x18(%rbp)
   0x00000000080012bc <+242>:   jle    0x800129a <main+208>
   0x00000000080012be <+244>:   lea    0xd8d(%rip),%rdi        # 0x8002052
   0x00000000080012c5 <+251>:   callq  0x8001040 <puts@plt>
   0x00000000080012ca <+256>:   mov    $0x0,%eax
   0x00000000080012cf <+261>:   jmp    0x80012e2 <main+280>
   0x00000000080012d1 <+263>:   lea    0xd7c(%rip),%rdi        # 0x8002054
   0x00000000080012d8 <+270>:   callq  0x8001040 <puts@plt>
   0x00000000080012dd <+275>:   mov    $0x0,%eax
   0x00000000080012e2 <+280>:   add    $0x88,%rsp
   0x00000000080012e9 <+287>:   pop    %rbx
   0x00000000080012ea <+288>:   pop    %rbp
   0x00000000080012eb <+289>:   retq
```

Beginning with:

```assembly
   0x00000000080011ca <+0>:     push   %rbp
   0x00000000080011cb <+1>:     mov    %rsp,%rbp
   0x00000000080011ce <+4>:     push   %rbx
   0x00000000080011cf <+5>:     sub    $0x88,%rsp
   0x00000000080011d6 <+12>:    movl   $0x0,-0x14(%rbp)
   0x00000000080011dd <+19>:    lea    0xe24(%rip),%rdi        # 0x8002008
   0x00000000080011e4 <+26>:    callq  0x8001040 <puts@plt>
   0x00000000080011e9 <+31>:    mov    0x2e60(%rip),%rdx        # 0x8004050 <stdin@@GLIBC_2.2.5>
   0x00000000080011f0 <+38>:    lea    -0x90(%rbp),%rax
   0x00000000080011f7 <+45>:    mov    $0x64,%esi
   0x00000000080011fc <+50>:    mov    %rax,%rdi
   0x00000000080011ff <+53>:    callq  0x8001070 <fgets@plt>
   0x0000000008001204 <+58>:    lea    -0x90(%rbp),%rax
   0x000000000800120b <+65>:    mov    %rax,%rdi
   0x000000000800120e <+68>:    callq  0x8001050 <strlen@plt>
   0x0000000008001213 <+73>:    cmp    $0xb,%rax
   0x0000000008001217 <+77>:    jbe    0x800122f <main+101>
```

Translates to:

```c
int
main (int argc, char **argv)
{
  char buffer[100]; // -0x90(%rbp)
  puts ("enter the magic string");
  fgets (buffer, 0x64, stdin);
  if (strlen (buffer) > 11)
    {
      puts ("too long...sorry no flag for you!!!");
      return 0;
    }
  /* <...> */  
}
```

Hereafter:

```assembly
   0x0000000008001238 <+110>:   mov    -0x18(%rbp),%eax
   0x000000000800123b <+113>:   cltq
   0x000000000800123d <+115>:   movzbl -0x90(%rbp,%rax,1),%eax
   0x0000000008001245 <+123>:   movsbl %al,%eax
   0x0000000008001248 <+126>:   add    %eax,-0x14(%rbp)
   0x000000000800124b <+129>:   addl   $0x1,-0x18(%rbp)
   0x000000000800124f <+133>:   mov    -0x18(%rbp),%eax
   0x0000000008001252 <+136>:   movslq %eax,%rbx
   0x0000000008001255 <+139>:   lea    -0x90(%rbp),%rax
   0x000000000800125c <+146>:   mov    %rax,%rdi
   0x000000000800125f <+149>:   callq  0x8001050 <strlen@plt>
   0x0000000008001264 <+154>:   cmp    %rax,%rbx
   0x0000000008001267 <+157>:   jb     0x8001238 <main+110>
   0x0000000008001269 <+159>:   cmpl   $0x3e8,-0x14(%rbp)
   0x0000000008001270 <+166>:   jne    0x80012d1 <main+263>
   0x0000000008001272 <+168>:   mov    $0x0,%eax
   0x0000000008001277 <+173>:   callq  0x8001175 <strcat_str>
```

`-0x14(%rbp)` contains the accumulated ASCII characters, `-0x18(%rbp)` is the iterating index, thereafter we call `strlen (buffer);` and compare it against `%rbx` which is the iterable, and restarts the loop if `i < strlen (buffer)`, otherwise it compares the accumulated ASCII to `0x3e8` and fails if it is not equal, otherwise calling `strcat_str`

Equivalent to:

```c
int
main (int argc, char **argv)
{
  char buffer[100]; // -0x90(%rbp)
  puts ("enter the magic string");
  fgets (buffer, 0x64, stdin);
  if (strlen (buffer) > 11)
    {
      puts ("too long...sorry no flag for you!!!");
      return 0;
    }
  int acc;
  int idx;
  for (acc = 0, idx = 0; idx < strlen (buffer); ++idx)
    {
      acc += buffer[idx];
    }
  if (acc != 0x3e8)
    {
      puts ("wrong string\nNo flag for you.");
      return 0;
    }
  strcat_str ();  // nulladic (?)
}
```

Now let's take a look at `strcat_str` because I have no idea whether it returns anything or has parameters:

```assembly
   0x0000000008001175 <+0>:     push   %rbp
   0x0000000008001176 <+1>:     mov    %rsp,%rbp
   0x0000000008001179 <+4>:     movb   $0x21,0x2ee0(%rip)        # 0x8004060 <f.2605>
   0x0000000008001180 <+11>:    movl   $0x1,-0x4(%rbp)
   0x0000000008001187 <+18>:    jmp    0x80011bb <strcat_str+70>
   0x0000000008001189 <+20>:    mov    -0x4(%rbp),%eax
   0x000000000800118c <+23>:    sub    $0x1,%eax
   0x000000000800118f <+26>:    cltq
   0x0000000008001191 <+28>:    lea    0x2ec8(%rip),%rdx        # 0x8004060 <f.2605>
   0x0000000008001198 <+35>:    movzbl (%rax,%rdx,1),%eax
   0x000000000800119c <+39>:    mov    %eax,%edx
   0x000000000800119e <+41>:    mov    -0x4(%rbp),%eax
   0x00000000080011a1 <+44>:    add    %edx,%eax
   0x00000000080011a3 <+46>:    add    $0x1,%eax
   0x00000000080011a6 <+49>:    mov    %eax,%ecx
   0x00000000080011a8 <+51>:    mov    -0x4(%rbp),%eax
   0x00000000080011ab <+54>:    cltq
   0x00000000080011ad <+56>:    lea    0x2eac(%rip),%rdx        # 0x8004060 <f.2605>
   0x00000000080011b4 <+63>:    mov    %cl,(%rax,%rdx,1)
   0x00000000080011b7 <+66>:    addl   $0x1,-0x4(%rbp)
   0x00000000080011bb <+70>:    cmpl   $0x9,-0x4(%rbp)
   0x00000000080011bf <+74>:    jle    0x8001189 <strcat_str+20>
   0x00000000080011c1 <+76>:    lea    0x2e98(%rip),%rax        # 0x8004060 <f.2605>
   0x00000000080011c8 <+83>:    pop    %rbp
   0x00000000080011c9 <+84>:    retq
```

So let's take a look, we initialize `f.2605` to `0x21`, move `0x1` to some `-0x4(%rbp)`, afterwards jumping to a comparison indicating a while-loop, there is a comparison on `+70` comparing `-0x4(%rbp)` by 9 and hereafter restarting the loop if `-0x4(%rbp) <= 0x9`, otherwise returning the pointer to the variable `f.2605`, the main loop is as follows:

```assembly
   0x0000000008001189 <+20>:    mov    -0x4(%rbp),%eax
   0x000000000800118c <+23>:    sub    $0x1,%eax
   0x000000000800118f <+26>:    cltq
   0x0000000008001191 <+28>:    lea    0x2ec8(%rip),%rdx        # 0x8004060 <f.2605>
   0x0000000008001198 <+35>:    movzbl (%rax,%rdx,1),%eax
   0x000000000800119c <+39>:    mov    %eax,%edx
   0x000000000800119e <+41>:    mov    -0x4(%rbp),%eax
   0x00000000080011a1 <+44>:    add    %edx,%eax
   0x00000000080011a3 <+46>:    add    $0x1,%eax
   0x00000000080011a6 <+49>:    mov    %eax,%ecx
   0x00000000080011a8 <+51>:    mov    -0x4(%rbp),%eax
   0x00000000080011ab <+54>:    cltq
   0x00000000080011ad <+56>:    lea    0x2eac(%rip),%rdx        # 0x8004060 <f.2605>
   0x00000000080011b4 <+63>:    mov    %cl,(%rax,%rdx,1)
   0x00000000080011b7 <+66>:    addl   $0x1,-0x4(%rbp)
```

Translates to the following C code:

```c
char f_2605[9];

char *
strcat_str (void) // ?
{
  f_2605[0] = '!'; // (char)0x21
  
  int idx = 1;
  while (idx <= 9)
    {
      f_2065[idx] = f_2605[idx - 1] + idx + 1;
      ++idx;
    }
  return f_2605;
}
```

Quite confusing control flow as it makes no intuitive sense, but yeah, let's run this through a Python interpeter:

```py
>>> def strcat_str():
...   string = "!"
...   idx = 1
...   while idx <= 9:
...     string += chr(ord(string[idx - 1]) + idx + 1)
...     idx += 1
...   return string
...
>>> strcat_str()
'!#&*/5<DMW'
```

And in the C code this is encapsulated with `"flag is flag{...}"`, originally I set the `$rip` to after the jump to the return and this returned the same value, but I didn't think it was correct and so thought it was dependent on the input, but it seems that it is not, and so we have our flag `flag{!#&*/5<DMW}`, an example of correct input would be acquired by a sequence of characters of length 5 to 10 (inclusive) which sum to 990, (0x3e8 is 1000, but you need to include the newline which is 0xa):

```assembly
$4.4 DESKTOP-AVEP851@unazed ~ 0
>./rev03
enter the magic string
cccccccccc
flag is flag{!#&*/5<DMW}
```

Thanks for reading.


