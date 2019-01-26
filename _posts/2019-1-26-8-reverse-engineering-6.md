---
layout: post
title: reverse engineering crackme 6
---

As rebound to the previous crackme which had in me complete intellectual disarray, I will be doing the crackme (here)[https://crackmes.one/crackme/5c2acb8933c5d46a3882b8d4], rated at difficulty 1, if I'm not able to finish this then the RE gods shan't have mercy on me.

```assembly
   0x0000000008001226 <+0>:     push   %rbp
   0x0000000008001227 <+1>:     mov    %rsp,%rbp
   0x000000000800122a <+4>:     sub    $0x10,%rsp
   0x000000000800122e <+8>:     mov    %edi,-0x4(%rbp)
   0x0000000008001231 <+11>:    mov    %rsi,-0x10(%rbp)
   0x0000000008001235 <+15>:    cmpl   $0x2,-0x4(%rbp)
   0x0000000008001239 <+19>:    je     0x800124a <main+36>
   0x000000000800123b <+21>:    mov    -0x10(%rbp),%rax
   0x000000000800123f <+25>:    mov    (%rax),%rax
   0x0000000008001242 <+28>:    mov    %rax,%rdi
   0x0000000008001245 <+31>:    callq  0x8001169 <usage>
   0x000000000800124a <+36>:    mov    -0x10(%rbp),%rax
   0x000000000800124e <+40>:    add    $0x8,%rax
   0x0000000008001252 <+44>:    mov    (%rax),%rax
   0x0000000008001255 <+47>:    mov    %rax,%rdi
   0x0000000008001258 <+50>:    callq  0x8001197 <checkSerial>
   0x000000000800125d <+55>:    test   %eax,%eax
   0x000000000800125f <+57>:    jne    0x8001274 <main+78>
   0x0000000008001261 <+59>:    lea    0xda9(%rip),%rdi        # 0x8002011
   0x0000000008001268 <+66>:    callq  0x8001030 <puts@plt>
   0x000000000800126d <+71>:    mov    $0x0,%eax
   0x0000000008001272 <+76>:    jmp    0x8001285 <main+95>
   0x0000000008001274 <+78>:    lea    0xda2(%rip),%rdi        # 0x800201d
   0x000000000800127b <+85>:    callq  0x8001030 <puts@plt>
   0x0000000008001280 <+90>:    mov    $0xffffffff,%eax
   0x0000000008001285 <+95>:    leaveq
   0x0000000008001286 <+96>:    retq
```

Looks as if it weren't optimized at all during compilation due to the standard `push %rbp; mov %rsp,%rbp; ...; leaveq; retq` instructions, and the binary doesn't seem stripped at all, due to the names of the functions still being there, this should be relatively easy.

```assembly
   0x0000000008001226 <+0>:     push   %rbp
   0x0000000008001227 <+1>:     mov    %rsp,%rbp
   0x000000000800122a <+4>:     sub    $0x10,%rsp
   0x000000000800122e <+8>:     mov    %edi,-0x4(%rbp)
   0x0000000008001231 <+11>:    mov    %rsi,-0x10(%rbp)
   0x0000000008001235 <+15>:    cmpl   $0x2,-0x4(%rbp)
   0x0000000008001239 <+19>:    je     0x800124a <main+36>
   0x000000000800123b <+21>:    mov    -0x10(%rbp),%rax
   0x000000000800123f <+25>:    mov    (%rax),%rax
   0x0000000008001242 <+28>:    mov    %rax,%rdi
   0x0000000008001245 <+31>:    callq  0x8001169 <usage>
```

`-0x4(%rbp)` = `argc` and `-0x10(%rbp) = `agv`, if two arguments aren't passed then `usage (argv[0]);`

```assembly
   0x0000000008001169 <+0>:     push   %rbp
   0x000000000800116a <+1>:     mov    %rsp,%rbp
   0x000000000800116d <+4>:     sub    $0x10,%rsp
   0x0000000008001171 <+8>:     mov    %rdi,-0x8(%rbp)
   0x0000000008001175 <+12>:    mov    -0x8(%rbp),%rax
   0x0000000008001179 <+16>:    mov    %rax,%rsi
   0x000000000800117c <+19>:    lea    0xe81(%rip),%rdi        # "%s [SERIAL]\n"
   0x0000000008001183 <+26>:    mov    $0x0,%eax
   0x0000000008001188 <+31>:    callq  0x8001050 <printf@plt>
   0x000000000800118d <+36>:    mov    $0xffffffff,%edi
   0x0000000008001192 <+41>:    callq  0x8001060 <exit@plt>
```

Makes the C as follows:

```c
void
usage (const char *filename)
{
  printf ("%s [SERIAL]\n", filename);
  exit (-1);
}

int
main (int argc, char **argv)
{
  if (argc != 2)
    {
      usage (argv[0]);
    }
  /* <...> */
}
```

Afterwards:

```assembly
   0x000000000800124a <+36>:    mov    -0x10(%rbp),%rax
   0x000000000800124e <+40>:    add    $0x8,%rax
   0x0000000008001252 <+44>:    mov    (%rax),%rax
   0x0000000008001255 <+47>:    mov    %rax,%rdi
   0x0000000008001258 <+50>:    callq  0x8001197 <checkSerial>
   0x000000000800125d <+55>:    test   %eax,%eax
   0x000000000800125f <+57>:    jne    0x8001274 <main+78>
   0x0000000008001261 <+59>:    lea    0xda9(%rip),%rdi        # "Good Serial"
   0x0000000008001268 <+66>:    callq  0x8001030 <puts@plt>
   0x000000000800126d <+71>:    mov    $0x0,%eax
   0x0000000008001272 <+76>:    jmp    0x8001285 <main+95>
   0x0000000008001274 <+78>:    lea    0xda2(%rip),%rdi        # "Bad Serial"
   0x000000000800127b <+85>:    callq  0x8001030 <puts@plt>
   0x0000000008001280 <+90>:    mov    $0xffffffff,%eax
   0x0000000008001285 <+95>:    leaveq
   0x0000000008001286 <+96>:    retq
```

Translates to:

```c
void
usage (const char *filename)
{
  printf ("%s [SERIAL]\n", filename);
  exit (-1);
}

int
main (int argc, char **argv)
{
  if (argc != 2)
    {
      usage (argv[0]);
    }
  bool result = checkSerial (argv[1]);
  if (result)
    {
      puts ("Good Serial");
      return 0;
    }
  puts ("Bad Serial");
  return -1;
}
```

Then, the more interesting `checkSerial` function is as follows:

```assembly
   0x0000000008001197 <+0>:     push   %rbp                                        
   0x0000000008001198 <+1>:     mov    %rsp,%rbp                                   
   0x000000000800119b <+4>:     push   %rbx                                        
   0x000000000800119c <+5>:     sub    $0x28,%rsp                                  
   0x00000000080011a0 <+9>:     mov    %rdi,-0x28(%rbp)                            
   0x00000000080011a4 <+13>:    mov    -0x28(%rbp),%rax                            
   0x00000000080011a8 <+17>:    mov    %rax,%rdi                                   
   0x00000000080011ab <+20>:    callq  0x8001040 <strlen@plt>                      
   0x00000000080011b0 <+25>:    cmp    $0x10,%rax                                  
   0x00000000080011b4 <+29>:    je     0x80011bd <checkSerial+38>                  
   0x00000000080011b6 <+31>:    mov    $0xffffffff,%eax                            
   0x00000000080011bb <+36>:    jmp    0x800121f <checkSerial+136>                 
   0x00000000080011bd <+38>:    movl   $0x0,-0x14(%rbp)                            
   0x00000000080011c4 <+45>:    jmp    0x8001203 <checkSerial+108>                 
   0x00000000080011c6 <+47>:    mov    -0x14(%rbp),%eax                            
   0x00000000080011c9 <+50>:    movslq %eax,%rdx                                   
   0x00000000080011cc <+53>:    mov    -0x28(%rbp),%rax                            
   0x00000000080011d0 <+57>:    add    %rdx,%rax                                   
   0x00000000080011d3 <+60>:    movzbl (%rax),%eax                                 
   0x00000000080011d6 <+63>:    movsbl %al,%edx                                    
   0x00000000080011d9 <+66>:    mov    -0x14(%rbp),%eax                            
   0x00000000080011dc <+69>:    cltq                                               
   0x00000000080011de <+71>:    lea    0x1(%rax),%rcx                              
   0x00000000080011e2 <+75>:    mov    -0x28(%rbp),%rax                            
   0x00000000080011e6 <+79>:    add    %rcx,%rax                                   
   0x00000000080011e9 <+82>:    movzbl (%rax),%eax                                 
   0x00000000080011ec <+85>:    movsbl %al,%eax                                    
   0x00000000080011ef <+88>:    sub    %eax,%edx                                   
   0x00000000080011f1 <+90>:    mov    %edx,%eax                                   
   0x00000000080011f3 <+92>:    cmp    $0xffffffff,%eax                            
   0x00000000080011f6 <+95>:    je     0x80011ff <checkSerial+104>                 
   0x00000000080011f8 <+97>:    mov    $0xffffffff,%eax                            
   0x00000000080011fd <+102>:   jmp    0x800121f <checkSerial+136>                 
   0x00000000080011ff <+104>:   addl   $0x2,-0x14(%rbp)                            
   0x0000000008001203 <+108>:   mov    -0x14(%rbp),%eax                            
   0x0000000008001206 <+111>:   movslq %eax,%rbx                                   
   0x0000000008001209 <+114>:   mov    -0x28(%rbp),%rax                            
   0x000000000800120d <+118>:   mov    %rax,%rdi                                   
   0x0000000008001210 <+121>:   callq  0x8001040 <strlen@plt>                                                 
   0x0000000008001215 <+126>:   cmp    %rax,%rbx                                   
   0x0000000008001218 <+129>:   jb     0x80011c6 <checkSerial+47>                  
   0x000000000800121a <+131>:   mov    $0x0,%eax                                   
   0x000000000800121f <+136>:   add    $0x28,%rsp                                  
   0x0000000008001223 <+140>:   pop    %rbx                                        
   0x0000000008001224 <+141>:   pop    %rbp                                        
   0x0000000008001225 <+142>:   retq                                               
```

Recall, `%rdi` = `argv[1]`:

```assembly
   0x0000000008001197 <+0>:     push   %rbp                                        
   0x0000000008001198 <+1>:     mov    %rsp,%rbp                                   
   0x000000000800119b <+4>:     push   %rbx                                        
   0x000000000800119c <+5>:     sub    $0x28,%rsp                                  
   0x00000000080011a0 <+9>:     mov    %rdi,-0x28(%rbp)                            
   0x00000000080011a4 <+13>:    mov    -0x28(%rbp),%rax                            
   0x00000000080011a8 <+17>:    mov    %rax,%rdi                                   
   0x00000000080011ab <+20>:    callq  0x8001040 <strlen@plt>                      
   0x00000000080011b0 <+25>:    cmp    $0x10,%rax                                  
   0x00000000080011b4 <+29>:    je     0x80011bd <checkSerial+38>                  
   0x00000000080011b6 <+31>:    mov    $0xffffffff,%eax                            
   0x00000000080011bb <+36>:    jmp    0x800121f <checkSerial+136>  
```

And so we have:

```c
bool
checkSerial (const char *input)
{
  if (strlen (input) != 0x10)
    {
      return -1;
    }
  /* <...> */
}
```

Then:

```assembly
   0x00000000080011bd <+38>:    movl   $0x0,-0x14(%rbp)                            
   0x00000000080011c4 <+45>:    jmp    0x8001203 <checkSerial+108>   
...
   0x0000000008001203 <+108>:   mov    -0x14(%rbp),%eax                            
   0x0000000008001206 <+111>:   movslq %eax,%rbx                                   
   0x0000000008001209 <+114>:   mov    -0x28(%rbp),%rax                            
   0x000000000800120d <+118>:   mov    %rax,%rdi                                   
   0x0000000008001210 <+121>:   callq  0x8001040 <strlen@plt>                                                 
   0x0000000008001215 <+126>:   cmp    %rax,%rbx                                   
   0x0000000008001218 <+129>:   jb     0x80011c6 <checkSerial+47>                  
   0x000000000800121a <+131>:   mov    $0x0,%eax                                   
   0x000000000800121f <+136>:   add    $0x28,%rsp                                  
   0x0000000008001223 <+140>:   pop    %rbx                                        
   0x0000000008001224 <+141>:   pop    %rbp                                        
   0x0000000008001225 <+142>:   retq     
```

This is indicative of a while-loop, revolving around that `%rbx - %rax < 0`, i.e. `%rbx < %rax`, given that `%rax` is `strlen (argv[1])` and `%rbx` which is `0` to begin with then `0 < 16` (since upon first iteration the serial has to be 16 characters).

```assembly
   0x00000000080011c6 <+47>:    mov    -0x14(%rbp),%eax                            
   0x00000000080011c9 <+50>:    movslq %eax,%rdx                                   
   0x00000000080011cc <+53>:    mov    -0x28(%rbp),%rax                            
   0x00000000080011d0 <+57>:    add    %rdx,%rax                                   
   0x00000000080011d3 <+60>:    movzbl (%rax),%eax                                 
   0x00000000080011d6 <+63>:    movsbl %al,%edx                                    
   0x00000000080011d9 <+66>:    mov    -0x14(%rbp),%eax                            
   0x00000000080011dc <+69>:    cltq                                               
   0x00000000080011de <+71>:    lea    0x1(%rax),%rcx                              
   0x00000000080011e2 <+75>:    mov    -0x28(%rbp),%rax                            
   0x00000000080011e6 <+79>:    add    %rcx,%rax                                   
   0x00000000080011e9 <+82>:    movzbl (%rax),%eax                                 
   0x00000000080011ec <+85>:    movsbl %al,%eax                                    
   0x00000000080011ef <+88>:    sub    %eax,%edx                                   
   0x00000000080011f1 <+90>:    mov    %edx,%eax                                   
   0x00000000080011f3 <+92>:    cmp    $0xffffffff,%eax                            
   0x00000000080011f6 <+95>:    je     0x80011ff <checkSerial+104>                 
   0x00000000080011f8 <+97>:    mov    $0xffffffff,%eax                            
   0x00000000080011fd <+102>:   jmp    0x800121f <checkSerial+136>                 
   0x00000000080011ff <+104>:   addl   $0x2,-0x14(%rbp)                            
   0x0000000008001203 <+108>:   mov    -0x14(%rbp),%eax                            
   0x0000000008001206 <+111>:   movslq %eax,%rbx    
```

Note `+136` is the return, `+108` is the condition.

```assembly
   0x00000000080011c6 <+47>:    mov    -0x14(%rbp),%eax                            
   0x00000000080011c9 <+50>:    movslq %eax,%rdx                                   
   0x00000000080011cc <+53>:    mov    -0x28(%rbp),%rax                            
   0x00000000080011d0 <+57>:    add    %rdx,%rax                                   
   0x00000000080011d3 <+60>:    movzbl (%rax),%eax                                 
   0x00000000080011d6 <+63>:    movsbl %al,%edx                                    
   0x00000000080011d9 <+66>:    mov    -0x14(%rbp),%eax                            
   0x00000000080011dc <+69>:    cltq   
```

`+57` gets the `%rdx`th byte of `argv[1]`, so `%rax` = `(argv[1] + %rdx)`, afterwards having `%edx` be that certain byte, i.e. `%edx` = `argv[1][%rdx]`:

```assembly
   0x00000000080011de <+71>:    lea    0x1(%rax),%rcx                              
   0x00000000080011e2 <+75>:    mov    -0x28(%rbp),%rax                            
   0x00000000080011e6 <+79>:    add    %rcx,%rax                                   
   0x00000000080011e9 <+82>:    movzbl (%rax),%eax                                 
   0x00000000080011ec <+85>:    movsbl %al,%eax                                    
   0x00000000080011ef <+88>:    sub    %eax,%edx                                   
   0x00000000080011f1 <+90>:    mov    %edx,%eax                                   
   0x00000000080011f3 <+92>:    cmp    $0xffffffff,%eax                            
   0x00000000080011f6 <+95>:    je     0x80011ff <checkSerial+104>                 
   0x00000000080011f8 <+97>:    mov    $0xffffffff,%eax                            
   0x00000000080011fd <+102>:   jmp    0x800121f <checkSerial+136>  
   0x00000000080011ff <+104>:   addl   $0x2,-0x14(%rbp)   
```

Afterwards, we load `%rcx` with `-0x14(%rbp) + 1`, set `%rax` to `argv[1]` again, so we have `%eax` = `argv[1][%rcx]`, afterwards we subtract the two bytes `argv[1][k]` and `argv[1][k+1]`, compare if the difference between them is `-1`, if so, rerun the condition, otherwise, exit.

```c
bool
checkSerial (const char *input)
{
  if (strlen (input) != 0x10)
    {
      return -1;
    }
  int acc = 0;
  while (acc < strlen (input))
    {
      int diff = input[acc] - input[acc + 1];
      if (diff != -1)
        {
          return -1;
        }
      acc += 2;
    }
  return 0;
}
```

By this, we have the solution, we need a string of characters such that a character at some position `2k` with ordinal `2k_c` must also imply `2(k + 1)` has ordinal `2k_c + 1`, therefore a simple string such as `"abababababababab"` or `"abcdefghijklmnop'` would work:

**EDITORIAL NOTE:** The positions are of a factor of `2` due to the line `acc += 2;`

```
$4.4 DESKTOP-AVEP851@unazed ~ 255
>./SimpleKeyGen abcdefghijklmnop
Good Serial
$4.4 DESKTOP-AVEP851@unazed ~ 0
>./SimpleKeyGen abababababababab
Good Serial
```

Which it does.

Thanks for reading.
