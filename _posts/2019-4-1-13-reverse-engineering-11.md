---
layout: post
title: reverse engineering 11
---

After a slight hiatus from the topic of reverse engineering, and computer science as a whole (more tended towards focusing on pure mathematics and my own education), I return with [this](https://crackmes.one/crackme/5ca0b3f833c5d4419da5567a) crackme, it is one made in C++ and I don't really want to use a decompiler since that's for skids (ref. to fundamental theorem of skid psychology [here](https://unazed.github.io/7-skid-psych-1/)).

```x86asm
   0x0000000008001195 <+0>:     push   %rbp
   0x0000000008001196 <+1>:     mov    %rsp,%rbp
   0x0000000008001199 <+4>:     sub    $0x10,%rsp
   0x000000000800119d <+8>:     lea    0xe61(%rip),%rsi        # 0x8002005
   0x00000000080011a4 <+15>:    lea    0x2fd5(%rip),%rdi        # 0x8004180 <_ZSt4cout@@GLIBCXX_3.4>
   0x00000000080011ab <+22>:    callq  0x8001050 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x00000000080011b0 <+27>:    mov    %rax,%rdx
   0x00000000080011b3 <+30>:    mov    0x2e16(%rip),%rax        # 0x8003fd0
   0x00000000080011ba <+37>:    mov    %rax,%rsi
   0x00000000080011bd <+40>:    mov    %rdx,%rdi
   0x00000000080011c0 <+43>:    callq  0x8001060 <_ZNSolsEPFRSoS_E@plt>
   0x00000000080011c5 <+48>:    callq  0x8001329 <_Z8get_codev>
   0x00000000080011ca <+53>:    mov    %rax,-0x10(%rbp)
   0x00000000080011ce <+57>:    lea    0x31eb(%rip),%rdi        # 0x80043c0 <code>
   0x00000000080011d5 <+64>:    callq  0x8001265 <_Z10check_codePi>
   0x00000000080011da <+69>:    xor    $0x1,%eax
   0x00000000080011dd <+72>:    test   %al,%al
   0x00000000080011df <+74>:    je     0x80011fe <main+105>
   0x00000000080011e1 <+76>:    lea    0xe38(%rip),%rsi        # 0x8002020
   0x00000000080011e8 <+83>:    lea    0x2f91(%rip),%rdi        # 0x8004180 <_ZSt4cout@@GLIBCXX_3.4>
   0x00000000080011ef <+90>:    callq  0x8001050 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x00000000080011f4 <+95>:    mov    $0x0,%edi
   0x00000000080011f9 <+100>:   callq  0x8001070 <exit@plt>
   0x00000000080011fe <+105>:   lea    0xe23(%rip),%rsi        # 0x8002028
   0x0000000008001205 <+112>:   lea    0x2f74(%rip),%rdi        # 0x8004180 <_ZSt4cout@@GLIBCXX_3.4>
   0x000000000800120c <+119>:   callq  0x8001050 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x0000000008001211 <+124>:   movl   $0x0,-0x4(%rbp)
   0x0000000008001218 <+131>:   cmpl   $0x3,-0x4(%rbp)
   0x000000000800121c <+135>:   jg     0x8001248 <main+179>
   0x000000000800121e <+137>:   mov    -0x4(%rbp),%eax
   0x0000000008001221 <+140>:   cltq
   0x0000000008001223 <+142>:   lea    0x0(,%rax,4),%rdx
   0x000000000800122b <+150>:   mov    -0x10(%rbp),%rax
   0x000000000800122f <+154>:   add    %rdx,%rax
   0x0000000008001232 <+157>:   mov    (%rax),%eax
   0x0000000008001234 <+159>:   mov    %eax,%esi
   0x0000000008001236 <+161>:   lea    0x2f43(%rip),%rdi        # 0x8004180 <_ZSt4cout@@GLIBCXX_3.4>
   0x000000000800123d <+168>:   callq  0x8001090 <_ZNSolsEi@plt>
   0x0000000008001242 <+173>:   addl   $0x1,-0x4(%rbp)
   0x0000000008001246 <+177>:   jmp    0x8001218 <main+131>
   0x0000000008001248 <+179>:   mov    0x2d81(%rip),%rax        # 0x8003fd0
   0x000000000800124f <+186>:   mov    %rax,%rsi
   0x0000000008001252 <+189>:   lea    0x2f27(%rip),%rdi        # 0x8004180 <_ZSt4cout@@GLIBCXX_3.4>
   0x0000000008001259 <+196>:   callq  0x8001060 <_ZNSolsEPFRSoS_E@plt>
   0x000000000800125e <+201>:   mov    $0x0,%eax
   0x0000000008001263 <+206>:   leaveq
   0x0000000008001264 <+207>:   retq
```

Now since I'm dealing with C++ the names are mangled for reasons of space optimization and probably some other obscure reasons, but one can unmask these mangled names by using `c++filt`, and so I shall do so:

```
[1]_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc
=> std::basic_ostream<char, std::char_traits<char> >& std::operator<< <std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&, char const*)


  _ZNSolsEPFRSoS_E
=> std::ostream::operator<<(std::ostream& (*)(std::ostream&))

  _Z8get_codev
=> get_code()

  _Z10check_codePi
=> check_code(int*)

  _ZSt4cout
=> std::cout

  _ZNSolsEi
=> std::basic_ostream<char, std::char_traits<char> >::operator<<(int)

[1] i assume this is for calling the `<<` operator over some given `std::basic_stream` with a C-string for the second parameter, also allowing for chaining as i learned as the return value is another stream so you can chain together `<<` operations instead of having them be individual
```

So, let's start somewhere:

```x86asm
   0x0000000008001195 <+0>:     push   %rbp
   0x0000000008001196 <+1>:     mov    %rsp,%rbp
   0x0000000008001199 <+4>:     sub    $0x10,%rsp
   0x000000000800119d <+8>:     lea    0xe61(%rip),%rsi        # 0x8002005
   0x00000000080011a4 <+15>:    lea    0x2fd5(%rip),%rdi        # 0x8004180 <_ZSt4cout@@GLIBCXX_3.4>
   0x00000000080011ab <+22>:    callq  0x8001050 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x00000000080011b0 <+27>:    mov    %rax,%rdx
   0x00000000080011b3 <+30>:    mov    0x2e16(%rip),%rax        # 0x8003fd0 [2]
   0x00000000080011ba <+37>:    mov    %rax,%rsi
   0x00000000080011bd <+40>:    mov    %rdx,%rdi
   0x00000000080011c0 <+43>:    callq  0x8001060 <std::ostream::operator<<(std::ostream& (*)(std::ostream&))@plt>
   0x00000000080011c5 <+48>:    callq  0x8001329 <_Z8get_codev>

[2] 0x8003fd0 is a pointer to a `std::basic_ostream<char, std::char_traits<char> >& std::endl<char, std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&)`
```

Equivalent to:

```c
int
main ()
{
  std::cout << "Please Enter The Passcode:" << std::endl;
  get_code ();
  /* ... */
}
```

As I've pointed out before in the `c++filt` table the seemingly extraneous or weird instructions `+30` to `+43` are utilizing the interchaining ability of the `<<` operator, now onto `get_code`:

```x86asm
   0x0000000008001329 <+0>:     push   %rbp
   0x000000000800132a <+1>:     mov    %rsp,%rbp
   0x000000000800132d <+4>:     sub    $0x10,%rsp
   0x0000000008001331 <+8>:     movl   $0x0,-0x4(%rbp)
   0x0000000008001338 <+15>:    cmpl   $0x3,-0x4(%rbp)
   0x000000000800133c <+19>:    jg     0x80013b2 <_Z8get_codev+137>
   0x000000000800133e <+21>:    lea    0xcf1(%rip),%rsi        # 0x8002036
   0x0000000008001345 <+28>:    lea    0x2e34(%rip),%rdi        # 0x8004180 <_ZSt4cout@@GLIBCXX_3.4>
   0x000000000800134c <+35>:    callq  0x8001050 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x0000000008001351 <+40>:    mov    %rax,%rdx
   0x0000000008001354 <+43>:    mov    -0x4(%rbp),%eax
   0x0000000008001357 <+46>:    add    $0x1,%eax
   0x000000000800135a <+49>:    mov    %eax,%esi
   0x000000000800135c <+51>:    mov    %rdx,%rdi
   0x000000000800135f <+54>:    callq  0x8001090 <_ZNSolsEi@plt>
   0x0000000008001364 <+59>:    lea    0xcd8(%rip),%rsi        # 0x8002043
   0x000000000800136b <+66>:    mov    %rax,%rdi
   0x000000000800136e <+69>:    callq  0x8001050 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x0000000008001373 <+74>:    mov    -0x4(%rbp),%eax
   0x0000000008001376 <+77>:    cltq
   0x0000000008001378 <+79>:    lea    0x0(,%rax,4),%rdx
   0x0000000008001380 <+87>:    lea    0x3039(%rip),%rax        # 0x80043c0 <code>
   0x0000000008001387 <+94>:    add    %rdx,%rax
   0x000000000800138a <+97>:    mov    %rax,%rsi
   0x000000000800138d <+100>:   lea    0x2f0c(%rip),%rdi        # 0x80042a0 <_ZSt3cin@@GLIBCXX_3.4>
   0x0000000008001394 <+107>:   callq  0x8001030 <_ZNSirsERi@plt>
   0x0000000008001399 <+112>:   lea    0xca6(%rip),%rsi        # 0x8002046
   0x00000000080013a0 <+119>:   lea    0x2dd9(%rip),%rdi        # 0x8004180 <_ZSt4cout@@GLIBCXX_3.4>
   0x00000000080013a7 <+126>:   callq  0x8001050 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x00000000080013ac <+131>:   addl   $0x1,-0x4(%rbp)
   0x00000000080013b0 <+135>:   jmp    0x8001338 <_Z8get_codev+15>
   0x00000000080013b2 <+137>:   lea    0x3007(%rip),%rax        # 0x80043c0 <code>
   0x00000000080013b9 <+144>:   leaveq
   0x00000000080013ba <+145>:   retq
```

`+8` to `+19` indicate that we are dealing with a for-loop (since `+131`), having already run the crackme it is helpful to pay note that at the surface of the program this function most likely will iterate four times, (hence the `jg` and not `jge`) and ask for a digit from the user:

```c
int code[4] = {0};
int[4]
get_code ()
{
  size_t iter;
  for (iter = 0; iter <= 3; ++iter)
    {
      std::cout << "Enter Digit " << iter + 1 << ": ";
      std::cin >> code[iter];
      std::cout << "\n";
    }
   return code;
}
```

Something more interesting about reading binary C++ is that the mangled names are genuinely useful in the case of manual type inference, like for example, the `code` variable being an array of four integers may have been `size_t` or any other qualifiable type as far as I'm concerned but the name: `_ZNSirsERi` gave it away, as it translates to `std::basic_istream<char, std::char_traits<char> >::operator>>(int&)` where the `int&` most likely suggests that `code` is an integer array, as `int&` is a reference to an integer, which is what is fed into the `code` variable as it is indexed 4-bytes at a time.

```x86asm
   0x00000000080011ca <+53>:    mov    %rax,-0x10(%rbp)
   0x00000000080011ce <+57>:    lea    0x31eb(%rip),%rdi        # 0x80043c0 <code>
   0x00000000080011d5 <+64>:    callq  0x8001265 <_Z10check_codePi>
   0x00000000080011da <+69>:    xor    $0x1,%eax
   0x00000000080011dd <+72>:    test   %al,%al
   0x00000000080011df <+74>:    je     0x80011fe <main+105>
   0x00000000080011e1 <+76>:    lea    0xe38(%rip),%rsi        # 0x8002020
   0x00000000080011e8 <+83>:    lea    0x2f91(%rip),%rdi        # 0x8004180 <_ZSt4cout@@GLIBCXX_3.4>
   0x00000000080011ef <+90>:    callq  0x8001050 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x00000000080011f4 <+95>:    mov    $0x0,%edi
   0x00000000080011f9 <+100>:   callq  0x8001070 <exit@plt>
```

Translates to:

```c
int
main ()
{
  std::cout << "Please Enter The Passcode:" << std::endl;
  int UNUSED[4] = get_code ();
  UNKNOWN ret = check_code (code);
  if (ret ^ 1)
    {
      std::cout << "\nWRONG\n";
      exit (0);
    }
  /* ... */
}
```

And following through:

```c
   0x00000000080011fe <+105>:   lea    0xe23(%rip),%rsi        # 0x8002028
   0x0000000008001205 <+112>:   lea    0x2f74(%rip),%rdi        # 0x8004180 <_ZSt4cout@@GLIBCXX_3.4>
   0x000000000800120c <+119>:   callq  0x8001050 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x0000000008001211 <+124>:   movl   $0x0,-0x4(%rbp)
   0x0000000008001218 <+131>:   cmpl   $0x3,-0x4(%rbp)
   0x000000000800121c <+135>:   jg     0x8001248 <main+179>
   0x000000000800121e <+137>:   mov    -0x4(%rbp),%eax
   0x0000000008001221 <+140>:   cltq
   0x0000000008001223 <+142>:   lea    0x0(,%rax,4),%rdx
   0x000000000800122b <+150>:   mov    -0x10(%rbp),%rax
   0x000000000800122f <+154>:   add    %rdx,%rax
   0x0000000008001232 <+157>:   mov    (%rax),%eax
   0x0000000008001234 <+159>:   mov    %eax,%esi
   0x0000000008001236 <+161>:   lea    0x2f43(%rip),%rdi        # 0x8004180 <_ZSt4cout@@GLIBCXX_3.4>
   0x000000000800123d <+168>:   callq  0x8001090 <_ZNSolsEi@plt>
   0x0000000008001242 <+173>:   addl   $0x1,-0x4(%rbp)
   0x0000000008001246 <+177>:   jmp    0x8001218 <main+131>
   0x0000000008001248 <+179>:   mov    0x2d81(%rip),%rax        # 0x8003fd0
   0x000000000800124f <+186>:   mov    %rax,%rsi
   0x0000000008001252 <+189>:   lea    0x2f27(%rip),%rdi        # 0x8004180 <_ZSt4cout@@GLIBCXX_3.4>
   0x0000000008001259 <+196>:   callq  0x8001060 <_ZNSolsEPFRSoS_E@plt>
   0x000000000800125e <+201>:   mov    $0x0,%eax
   0x0000000008001263 <+206>:   leaveq
   0x0000000008001264 <+207>:   retq
```

Gives:

```c
int
main ()
{
  std::cout << "Please Enter The Passcode:" << std::endl;
  int codes[4] = get_code ();
  UNKNOWN ret = check_code (code);
  if (ret ^ 1)
    {
      std::cout << "\nWRONG\n";
      exit (0);
    }
  std::cout << "\nYou Did it.\n"
  size_t iter;
  for (iter = 0; iter <= 3; ++iter)
    {
      std::cout << codes[iter];
    }
  std::cout << std::endl;
  return 0;
}
```

And so, it seems the only other relevant function to analyze is `check_code` (obviously):

```x86asm
   0x0000000008001265 <+0>:     push   %rbp
   0x0000000008001266 <+1>:     mov    %rsp,%rbp
   0x0000000008001269 <+4>:     push   %rbx
   0x000000000800126a <+5>:     sub    $0x18,%rsp
   0x000000000800126e <+9>:     mov    %rdi,-0x18(%rbp)
   0x0000000008001272 <+13>:    mov    -0x18(%rbp),%rax
   0x0000000008001276 <+17>:    mov    (%rax),%ebx
   0x0000000008001278 <+19>:    mov    $0xa,%esi
   0x000000000800127d <+24>:    lea    0x2dfc(%rip),%rdi        # 0x8004080 <p1>
   0x0000000008001284 <+31>:    callq  0x80013bb <_Z9get_digitPii>
   0x0000000008001289 <+36>:    cmp    %eax,%ebx
   0x000000000800128b <+38>:    setne  %al
   0x000000000800128e <+41>:    test   %al,%al
   0x0000000008001290 <+43>:    je     0x800129c <_Z10check_codePi+55>
   0x0000000008001292 <+45>:    mov    $0x0,%eax
   0x0000000008001297 <+50>:    jmpq   0x8001322 <_Z10check_codePi+189>
   0x000000000800129c <+55>:    mov    -0x18(%rbp),%rax
   0x00000000080012a0 <+59>:    add    $0x4,%rax
   0x00000000080012a4 <+63>:    mov    (%rax),%ebx
   0x00000000080012a6 <+65>:    mov    $0xa,%esi
   0x00000000080012ab <+70>:    lea    0x2e0e(%rip),%rdi        # 0x80040c0 <p2>
   0x00000000080012b2 <+77>:    callq  0x80013bb <_Z9get_digitPii>
   0x00000000080012b7 <+82>:    cmp    %eax,%ebx
   0x00000000080012b9 <+84>:    setne  %al
   0x00000000080012bc <+87>:    test   %al,%al
   0x00000000080012be <+89>:    je     0x80012c7 <_Z10check_codePi+98>
   0x00000000080012c0 <+91>:    mov    $0x0,%eax
   0x00000000080012c5 <+96>:    jmp    0x8001322 <_Z10check_codePi+189>
   0x00000000080012c7 <+98>:    mov    -0x18(%rbp),%rax
   0x00000000080012cb <+102>:   add    $0x8,%rax
   0x00000000080012cf <+106>:   mov    (%rax),%ebx
   0x00000000080012d1 <+108>:   mov    $0xa,%esi
   0x00000000080012d6 <+113>:   lea    0x2e23(%rip),%rdi        # 0x8004100 <p3>
   0x00000000080012dd <+120>:   callq  0x80013bb <_Z9get_digitPii>
   0x00000000080012e2 <+125>:   cmp    %eax,%ebx
   0x00000000080012e4 <+127>:   setne  %al
   0x00000000080012e7 <+130>:   test   %al,%al
   0x00000000080012e9 <+132>:   je     0x80012f2 <_Z10check_codePi+141>
   0x00000000080012eb <+134>:   mov    $0x0,%eax
   0x00000000080012f0 <+139>:   jmp    0x8001322 <_Z10check_codePi+189>
   0x00000000080012f2 <+141>:   mov    -0x18(%rbp),%rax
   0x00000000080012f6 <+145>:   add    $0xc,%rax
   0x00000000080012fa <+149>:   mov    (%rax),%ebx
   0x00000000080012fc <+151>:   mov    $0xa,%esi
   0x0000000008001301 <+156>:   lea    0x2e38(%rip),%rdi        # 0x8004140 <p4>
   0x0000000008001308 <+163>:   callq  0x80013bb <_Z9get_digitPii>
   0x000000000800130d <+168>:   cmp    %eax,%ebx
   0x000000000800130f <+170>:   setne  %al
   0x0000000008001312 <+173>:   test   %al,%al
   0x0000000008001314 <+175>:   je     0x800131d <_Z10check_codePi+184>
   0x0000000008001316 <+177>:   mov    $0x0,%eax
   0x000000000800131b <+182>:   jmp    0x8001322 <_Z10check_codePi+189>
   0x000000000800131d <+184>:   mov    $0x1,%eax
   0x0000000008001322 <+189>:   add    $0x18,%rsp
   0x0000000008001326 <+193>:   pop    %rbx
   0x0000000008001327 <+194>:   pop    %rbp
   0x0000000008001328 <+195>:   retq
```

Beginning with:

```x86asm
   0x0000000008001265 <+0>:     push   %rbp
   0x0000000008001266 <+1>:     mov    %rsp,%rbp
   0x0000000008001269 <+4>:     push   %rbx
   0x000000000800126a <+5>:     sub    $0x18,%rsp
   0x000000000800126e <+9>:     mov    %rdi,-0x18(%rbp)
   0x0000000008001272 <+13>:    mov    -0x18(%rbp),%rax
   0x0000000008001276 <+17>:    mov    (%rax),%ebx
   0x0000000008001278 <+19>:    mov    $0xa,%esi
   0x000000000800127d <+24>:    lea    0x2dfc(%rip),%rdi        # 0x8004080 <p1>
   0x0000000008001284 <+31>:    callq  0x80013bb <_Z9get_digitPii>
   0x0000000008001289 <+36>:    cmp    %eax,%ebx
   0x000000000800128b <+38>:    setne  %al
   0x000000000800128e <+41>:    test   %al,%al
   0x0000000008001290 <+43>:    je     0x800129c <_Z10check_codePi+55>
   0x0000000008001292 <+45>:    mov    $0x0,%eax
   0x0000000008001297 <+50>:    jmpq   0x8001322 <_Z10check_codePi+189>
```

Translates trivially to:

```c
UNKNOWN
check_code (int codes[4])
{
  if (codes[0] != get_digit (p1, 0xa))
    {
      return 1;
    }
  /* ... */
}
```

In fact, the function is quite easy:

```x86asm
   0x000000000800129c <+55>:    mov    -0x18(%rbp),%rax
   0x00000000080012a0 <+59>:    add    $0x4,%rax
   0x00000000080012a4 <+63>:    mov    (%rax),%ebx
   0x00000000080012a6 <+65>:    mov    $0xa,%esi
   0x00000000080012ab <+70>:    lea    0x2e0e(%rip),%rdi        # 0x80040c0 <p2>
   0x00000000080012b2 <+77>:    callq  0x80013bb <_Z9get_digitPii>
   0x00000000080012b7 <+82>:    cmp    %eax,%ebx
   0x00000000080012b9 <+84>:    setne  %al
   0x00000000080012bc <+87>:    test   %al,%al
   0x00000000080012be <+89>:    je     0x80012c7 <_Z10check_codePi+98>
   0x00000000080012c0 <+91>:    mov    $0x0,%eax
   0x00000000080012c5 <+96>:    jmp    0x8001322 <_Z10check_codePi+189>
   0x00000000080012c7 <+98>:    mov    -0x18(%rbp),%rax
   0x00000000080012cb <+102>:   add    $0x8,%rax
   0x00000000080012cf <+106>:   mov    (%rax),%ebx
   0x00000000080012d1 <+108>:   mov    $0xa,%esi
   0x00000000080012d6 <+113>:   lea    0x2e23(%rip),%rdi        # 0x8004100 <p3>
   0x00000000080012dd <+120>:   callq  0x80013bb <_Z9get_digitPii>
   0x00000000080012e2 <+125>:   cmp    %eax,%ebx
   0x00000000080012e4 <+127>:   setne  %al
   0x00000000080012e7 <+130>:   test   %al,%al
   0x00000000080012e9 <+132>:   je     0x80012f2 <_Z10check_codePi+141>
   0x00000000080012eb <+134>:   mov    $0x0,%eax
   0x00000000080012f0 <+139>:   jmp    0x8001322 <_Z10check_codePi+189>
   0x00000000080012f2 <+141>:   mov    -0x18(%rbp),%rax
   0x00000000080012f6 <+145>:   add    $0xc,%rax
   0x00000000080012fa <+149>:   mov    (%rax),%ebx
   0x00000000080012fc <+151>:   mov    $0xa,%esi
   0x0000000008001301 <+156>:   lea    0x2e38(%rip),%rdi        # 0x8004140 <p4>
   0x0000000008001308 <+163>:   callq  0x80013bb <_Z9get_digitPii>
   0x000000000800130d <+168>:   cmp    %eax,%ebx
   0x000000000800130f <+170>:   setne  %al
   0x0000000008001312 <+173>:   test   %al,%al
   0x0000000008001314 <+175>:   je     0x800131d <_Z10check_codePi+184>
   0x0000000008001316 <+177>:   mov    $0x0,%eax
   0x000000000800131b <+182>:   jmp    0x8001322 <_Z10check_codePi+189>
   0x000000000800131d <+184>:   mov    $0x1,%eax
   0x0000000008001322 <+189>:   add    $0x18,%rsp
   0x0000000008001326 <+193>:   pop    %rbx
   0x0000000008001327 <+194>:   pop    %rbp
   0x0000000008001328 <+195>:   retq
```

Gives:

```c
bool
check_code (int codes[4])
{
  if ((codes[0] != get_digit (p1, 0xa)) ||
      (codes[1] != get_digit (p2, 0xa)) ||
      (codes[2] != get_digit (p3, 0xa)) ||
      (codes[3] != get_digit (p4, 0xa)))
    {
      return 1;
    }
  return 0;
}
```

And so we can see the ultimate function we need is `get_digit`:

```x86asm
   0x00000000080013bb <+0>:     push   %rbp
   0x00000000080013bc <+1>:     mov    %rsp,%rbp
   0x00000000080013bf <+4>:     mov    %rdi,-0x18(%rbp)
   0x00000000080013c3 <+8>:     mov    %esi,-0x1c(%rbp)
   0x00000000080013c6 <+11>:    movl   $0x0,-0x4(%rbp)
   0x00000000080013cd <+18>:    movl   $0x0,-0x8(%rbp)
   0x00000000080013d4 <+25>:    movl   $0x0,-0xc(%rbp)
   0x00000000080013db <+32>:    mov    -0xc(%rbp),%eax
   0x00000000080013de <+35>:    cmp    -0x1c(%rbp),%eax
   0x00000000080013e1 <+38>:    jge    0x8001435 <_Z9get_digitPii+122>
   0x00000000080013e3 <+40>:    mov    -0xc(%rbp),%eax
   0x00000000080013e6 <+43>:    cltq
   0x00000000080013e8 <+45>:    lea    0x0(,%rax,4),%rdx
   0x00000000080013f0 <+53>:    mov    -0x18(%rbp),%rax
   0x00000000080013f4 <+57>:    add    %rdx,%rax
   0x00000000080013f7 <+60>:    mov    (%rax),%eax
   0x00000000080013f9 <+62>:    and    -0x4(%rbp),%eax
   0x00000000080013fc <+65>:    or     %eax,-0x8(%rbp)
   0x00000000080013ff <+68>:    mov    -0xc(%rbp),%eax
   0x0000000008001402 <+71>:    cltq
   0x0000000008001404 <+73>:    lea    0x0(,%rax,4),%rdx
   0x000000000800140c <+81>:    mov    -0x18(%rbp),%rax
   0x0000000008001410 <+85>:    add    %rdx,%rax
   0x0000000008001413 <+88>:    mov    (%rax),%eax
   0x0000000008001415 <+90>:    xor    %eax,-0x4(%rbp)
   0x0000000008001418 <+93>:    mov    -0x4(%rbp),%eax
   0x000000000800141b <+96>:    and    -0x8(%rbp),%eax
   0x000000000800141e <+99>:    not    %eax
   0x0000000008001420 <+101>:   mov    %eax,-0x10(%rbp)
   0x0000000008001423 <+104>:   mov    -0x10(%rbp),%eax
   0x0000000008001426 <+107>:   and    %eax,-0x4(%rbp)
   0x0000000008001429 <+110>:   mov    -0x10(%rbp),%eax
   0x000000000800142c <+113>:   and    %eax,-0x8(%rbp)
   0x000000000800142f <+116>:   addl   $0x1,-0xc(%rbp)
   0x0000000008001433 <+120>:   jmp    0x80013db <_Z9get_digitPii+32>
   0x0000000008001435 <+122>:   mov    -0x4(%rbp),%eax
   0x0000000008001438 <+125>:   pop    %rbp
   0x0000000008001439 <+126>:   retq
```

Feel like disassembling this? Me neither, we can just `set $rip` our way through the `check_code` function instead of trying to figure out what this does:

```
(gdb) print $eax
$1 = 3
[...]
(gdb) print $eax
$2 = 6
[...]
(gdb) print $eax
$3 = 7
[...]
(gdb) print $rax
$4 = 4
```

Et, voila:

```
>./crack3-by-D4RK_FL0W
Please Enter The Passcode:
Enter Digit 1: 3

Enter Digit 2: 6

Enter Digit 3: 7

Enter Digit 4: 4


You Did It.
3674
```

Thanks for reading.
