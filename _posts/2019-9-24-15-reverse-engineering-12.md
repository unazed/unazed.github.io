---
layout: post
title: reverse engineering crackme 12
---

I don't expect myself to be any better than I last was, in my 11th crackme, because I have been focusing on my college and senior studies at highschool, but I'm curious as to what skills I indirectly developed through my having to study Baby Rudin, therein having to go through crying and spending hours solving seemingly trivial propositions and understanding shortly explained theorems.

Nonetheless, I start with [Baphomet](https://crackmes.one/crackme/5d7e154333c5d46f00e2c470). As I disassemble the `main` function I find that it is 320 lines of assembly long, so I believe I should be in for some fun.

```x86asm
   0x00005555555547ea <+0>:	push   %rbp
   0x00005555555547eb <+1>:	mov    %rsp,%rbp
   0x00005555555547ee <+4>:	push   %rbx
   0x00005555555547ef <+5>:	sub    $0x4c8,%rsp
   0x00005555555547f6 <+12>:	mov    %edi,-0x4c4(%rbp)
   0x00005555555547fc <+18>:	mov    %rsi,-0x4d0(%rbp)
   0x0000555555554803 <+25>:	mov    %fs:0x28,%rax
   0x000055555555480c <+34>:	mov    %rax,-0x18(%rbp)
   0x0000555555554810 <+38>:	xor    %eax,%eax
   0x0000555555554812 <+40>:	lea    0x62f(%rip),%rdi        # 0x555555554e48
   0x0000555555554819 <+47>:	callq  0x555555554670 <puts@plt>
   0x000055555555481e <+52>:	movl   $0x0,-0x4b0(%rbp)
   0x0000555555554828 <+62>:	movl   $0x89,-0x490(%rbp)
   0x0000555555554832 <+72>:	movl   $0xbb,-0x48c(%rbp)
   0x000055555555483c <+82>:	movl   $0x800,-0x488(%rbp)
   0x0000555555554846 <+92>:	movl   $0x0,-0x484(%rbp)
   0x0000555555554850 <+102>:	movl   $0x0,-0x4ac(%rbp)
   0x000055555555485a <+112>:	movl   $0x0,-0x4a8(%rbp)
   0x0000555555554864 <+122>:	lea    0xaec(%rip),%rdi        # 0x555555555357
   0x000055555555486b <+129>:	callq  0x555555554670 <puts@plt>
   0x0000555555554870 <+134>:	lea    0xb01(%rip),%rdi        # 0x555555555378
   0x0000555555554877 <+141>:	callq  0x555555554670 <puts@plt>
   0x000055555555487c <+146>:	lea    0xb3d(%rip),%rdi        # 0x5555555553c0
   0x0000555555554883 <+153>:	callq  0x555555554670 <puts@plt>
   0x0000555555554888 <+158>:	lea    0xb9c(%rip),%rdi        # 0x55555555542b
   0x000055555555488f <+165>:	mov    $0x0,%eax
   0x0000555555554894 <+170>:	callq  0x5555555546a0 <printf@plt>
   0x0000555555554899 <+175>:	lea    -0x170(%rbp),%rax
   0x00005555555548a0 <+182>:	mov    %rax,%rsi
   0x00005555555548a3 <+185>:	lea    0xb95(%rip),%rdi        # 0x55555555543f
   0x00005555555548aa <+192>:	mov    $0x0,%eax
   0x00005555555548af <+197>:	callq  0x5555555546b0 <__isoc99_scanf@plt>
   0x00005555555548b4 <+202>:	movl   $0x0,-0x4b4(%rbp)
   0x00005555555548be <+212>:	jmpq   0x555555554965 <main+379>
   0x00005555555548c3 <+217>:	mov    -0x4b4(%rbp),%eax
   0x00005555555548c9 <+223>:	cltq   
   0x00005555555548cb <+225>:	movzbl -0x170(%rbp,%rax,1),%eax
   0x00005555555548d3 <+233>:	movsbl %al,%eax
   0x00005555555548d6 <+236>:	mov    %eax,-0x484(%rbp)
   0x00005555555548dc <+242>:	mov    -0x484(%rbp),%eax
   0x00005555555548e2 <+248>:	mov    %eax,-0x4ac(%rbp)
   0x00005555555548e8 <+254>:	movl   $0x0,-0x4b0(%rbp)
   0x00005555555548f2 <+264>:	jmp    0x55555555491f <main+309>
   0x00005555555548f4 <+266>:	mov    -0x490(%rbp),%eax
   0x00005555555548fa <+272>:	imul   -0x4ac(%rbp),%eax
   0x0000555555554901 <+279>:	mov    %eax,%edx
   0x0000555555554903 <+281>:	mov    -0x48c(%rbp),%eax
   0x0000555555554909 <+287>:	add    %edx,%eax
   0x000055555555490b <+289>:	cltd   
   0x000055555555490c <+290>:	idivl  -0x488(%rbp)
   0x0000555555554912 <+296>:	mov    %edx,-0x4ac(%rbp)
   0x0000555555554918 <+302>:	addl   $0x1,-0x4b0(%rbp)
   0x000055555555491f <+309>:	mov    -0x4b4(%rbp),%eax
   0x0000555555554925 <+315>:	cltq   
   0x0000555555554927 <+317>:	movzbl -0x170(%rbp,%rax,1),%eax
   0x000055555555492f <+325>:	movsbl %al,%eax
   0x0000555555554932 <+328>:	add    $0x4a,%eax
   0x0000555555554935 <+331>:	cmp    %eax,-0x4b0(%rbp)
   0x000055555555493b <+337>:	jl     0x5555555548f4 <main+266>
   0x000055555555493d <+339>:	mov    -0x4ac(%rbp),%eax
   0x0000555555554943 <+345>:	imul   $0x29a,%eax,%edx
   0x0000555555554949 <+351>:	mov    -0x4ac(%rbp),%eax
   0x000055555555494f <+357>:	imul   $0x29a,%eax,%eax
   0x0000555555554955 <+363>:	imul   %edx,%eax
   0x0000555555554958 <+366>:	add    %eax,-0x4a8(%rbp)
   0x000055555555495e <+372>:	addl   $0x1,-0x4b4(%rbp)
   0x0000555555554965 <+379>:	mov    -0x4b4(%rbp),%eax
   0x000055555555496b <+385>:	movslq %eax,%rbx
   0x000055555555496e <+388>:	lea    -0x170(%rbp),%rax
   0x0000555555554975 <+395>:	mov    %rax,%rdi
   0x0000555555554978 <+398>:	callq  0x555555554680 <strlen@plt>
   0x000055555555497d <+403>:	cmp    %rax,%rbx
   0x0000555555554980 <+406>:	jb     0x5555555548c3 <main+217>
   0x0000555555554986 <+412>:	movl   $0x0,-0x4b4(%rbp)
   0x0000555555554990 <+422>:	jmpq   0x555555554a27 <main+573>
   0x0000555555554995 <+427>:	movl   $0x0,-0x4b0(%rbp)
   0x000055555555499f <+437>:	jmp    0x555555554a17 <main+557>
   0x00005555555549a1 <+439>:	mov    -0x4b0(%rbp),%eax
   0x00005555555549a7 <+445>:	and    $0x1,%eax
   0x00005555555549aa <+448>:	test   %eax,%eax
   0x00005555555549ac <+450>:	je     0x5555555549e0 <main+502>
   0x00005555555549ae <+452>:	mov    -0x4b0(%rbp),%eax
   0x00005555555549b4 <+458>:	movslq %eax,%rcx
   0x00005555555549b7 <+461>:	mov    -0x4b4(%rbp),%eax
   0x00005555555549bd <+467>:	movslq %eax,%rdx
   0x00005555555549c0 <+470>:	mov    %rdx,%rax
   0x00005555555549c3 <+473>:	shl    $0x3,%rax
   0x00005555555549c7 <+477>:	add    %rdx,%rax
   0x00005555555549ca <+480>:	add    %rax,%rax
   0x00005555555549cd <+483>:	add    %rdx,%rax
   0x00005555555549d0 <+486>:	add    %rcx,%rax
   0x00005555555549d3 <+489>:	movl   $0x1,-0x480(%rbp,%rax,4)
   0x00005555555549de <+500>:	jmp    0x555555554a10 <main+550>
   0x00005555555549e0 <+502>:	mov    -0x4b0(%rbp),%eax
   0x00005555555549e6 <+508>:	movslq %eax,%rcx
   0x00005555555549e9 <+511>:	mov    -0x4b4(%rbp),%eax
   0x00005555555549ef <+517>:	movslq %eax,%rdx
   0x00005555555549f2 <+520>:	mov    %rdx,%rax
   0x00005555555549f5 <+523>:	shl    $0x3,%rax
   0x00005555555549f9 <+527>:	add    %rdx,%rax
   0x00005555555549fc <+530>:	add    %rax,%rax
   0x00005555555549ff <+533>:	add    %rdx,%rax
   0x0000555555554a02 <+536>:	add    %rcx,%rax
   0x0000555555554a05 <+539>:	movl   $0x0,-0x480(%rbp,%rax,4)
   0x0000555555554a10 <+550>:	addl   $0x1,-0x4b0(%rbp)
   0x0000555555554a17 <+557>:	cmpl   $0x12,-0x4b0(%rbp)
   0x0000555555554a1e <+564>:	jle    0x5555555549a1 <main+439>
   0x0000555555554a20 <+566>:	addl   $0x1,-0x4b4(%rbp)
   0x0000555555554a27 <+573>:	cmpl   $0x9,-0x4b4(%rbp)
   0x0000555555554a2e <+580>:	jle    0x555555554995 <main+427>
   0x0000555555554a34 <+586>:	mov    -0x4a8(%rbp),%edx
   0x0000555555554a3a <+592>:	lea    -0x17f(%rbp),%rax
   0x0000555555554a41 <+599>:	lea    0x9fa(%rip),%rsi        # 0x555555555442
   0x0000555555554a48 <+606>:	mov    %rax,%rdi
   0x0000555555554a4b <+609>:	mov    $0x0,%eax
   0x0000555555554a50 <+614>:	callq  0x5555555546c0 <sprintf@plt>
   0x0000555555554a55 <+619>:	movl   $0x0,-0x4a4(%rbp)
   0x0000555555554a5f <+629>:	movl   $0x1,-0x4b0(%rbp)
   0x0000555555554a69 <+639>:	jmpq   0x555555554b07 <main+797>
   0x0000555555554a6e <+644>:	cmpl   $0x11,-0x4b0(%rbp)
   0x0000555555554a75 <+651>:	je     0x555555554ab9 <main+719>
   0x0000555555554a77 <+653>:	mov    -0x4a4(%rbp),%eax
   0x0000555555554a7d <+659>:	cltq   
   0x0000555555554a7f <+661>:	movzbl -0x17f(%rbp,%rax,1),%eax
   0x0000555555554a87 <+669>:	movsbl %al,%eax
   0x0000555555554a8a <+672>:	lea    -0x30(%rax),%edx
   0x0000555555554a8d <+675>:	mov    -0x4b0(%rbp),%eax
   0x0000555555554a93 <+681>:	movslq %eax,%rcx
   0x0000555555554a96 <+684>:	movslq %edx,%rdx
   0x0000555555554a99 <+687>:	mov    %rdx,%rax
   0x0000555555554a9c <+690>:	shl    $0x3,%rax
   0x0000555555554aa0 <+694>:	add    %rdx,%rax
   0x0000555555554aa3 <+697>:	add    %rax,%rax
   0x0000555555554aa6 <+700>:	add    %rdx,%rax
   0x0000555555554aa9 <+703>:	add    %rcx,%rax
   0x0000555555554aac <+706>:	movl   $0x0,-0x480(%rbp,%rax,4)
   0x0000555555554ab7 <+717>:	jmp    0x555555554af9 <main+783>
   0x0000555555554ab9 <+719>:	mov    -0x4a4(%rbp),%eax
   0x0000555555554abf <+725>:	cltq   
   0x0000555555554ac1 <+727>:	movzbl -0x17f(%rbp,%rax,1),%eax
   0x0000555555554ac9 <+735>:	movsbl %al,%eax
   0x0000555555554acc <+738>:	lea    -0x30(%rax),%edx
   0x0000555555554acf <+741>:	mov    -0x4b0(%rbp),%eax
   0x0000555555554ad5 <+747>:	movslq %eax,%rcx
   0x0000555555554ad8 <+750>:	movslq %edx,%rdx
   0x0000555555554adb <+753>:	mov    %rdx,%rax
   0x0000555555554ade <+756>:	shl    $0x3,%rax
   0x0000555555554ae2 <+760>:	add    %rdx,%rax
   0x0000555555554ae5 <+763>:	add    %rax,%rax
   0x0000555555554ae8 <+766>:	add    %rdx,%rax
   0x0000555555554aeb <+769>:	add    %rcx,%rax
   0x0000555555554aee <+772>:	movl   $0x2,-0x480(%rbp,%rax,4)
   0x0000555555554af9 <+783>:	addl   $0x1,-0x4a4(%rbp)
   0x0000555555554b00 <+790>:	addl   $0x2,-0x4b0(%rbp)
   0x0000555555554b07 <+797>:	cmpl   $0x12,-0x4b0(%rbp)
   0x0000555555554b0e <+804>:	jle    0x555555554a6e <main+644>
   0x0000555555554b14 <+810>:	lea    0x92d(%rip),%rdi        # 0x555555555448
   0x0000555555554b1b <+817>:	mov    $0x0,%eax
   0x0000555555554b20 <+822>:	callq  0x5555555546a0 <printf@plt>
   0x0000555555554b25 <+827>:	lea    -0x150(%rbp),%rax
   0x0000555555554b2c <+834>:	mov    %rax,%rsi
   0x0000555555554b2f <+837>:	lea    0x909(%rip),%rdi        # 0x55555555543f
   0x0000555555554b36 <+844>:	mov    $0x0,%eax
   0x0000555555554b3b <+849>:	callq  0x5555555546b0 <__isoc99_scanf@plt>
   0x0000555555554b40 <+854>:	movl   $0x0,-0x4a0(%rbp)
   0x0000555555554b4a <+864>:	movl   $0x0,-0x49c(%rbp)
   0x0000555555554b54 <+874>:	movl   $0x0,-0x498(%rbp)
   0x0000555555554b5e <+884>:	movl   $0x0,-0x494(%rbp)
   0x0000555555554b68 <+894>:	movl   $0x0,-0x494(%rbp)
   0x0000555555554b72 <+904>:	jmpq   0x555555554d49 <main+1375>
   0x0000555555554b77 <+909>:	mov    -0x494(%rbp),%eax
   0x0000555555554b7d <+915>:	cltq   
   0x0000555555554b7f <+917>:	movzbl -0x150(%rbp,%rax,1),%eax
   0x0000555555554b87 <+925>:	cmp    $0x55,%al
   0x0000555555554b89 <+927>:	jne    0x555555554be0 <main+1014>
   0x0000555555554b8b <+929>:	mov    -0x4a0(%rbp),%eax
   0x0000555555554b91 <+935>:	sub    $0x1,%eax
   0x0000555555554b94 <+938>:	test   %eax,%eax
   0x0000555555554b96 <+940>:	js     0x555555554d08 <main+1310>
   0x0000555555554b9c <+946>:	mov    -0x4a0(%rbp),%eax
   0x0000555555554ba2 <+952>:	lea    -0x1(%rax),%edx
   0x0000555555554ba5 <+955>:	mov    -0x49c(%rbp),%eax
   0x0000555555554bab <+961>:	movslq %eax,%rcx
   0x0000555555554bae <+964>:	movslq %edx,%rdx
   0x0000555555554bb1 <+967>:	mov    %rdx,%rax
   0x0000555555554bb4 <+970>:	shl    $0x3,%rax
   0x0000555555554bb8 <+974>:	add    %rdx,%rax
   0x0000555555554bbb <+977>:	add    %rax,%rax
   0x0000555555554bbe <+980>:	add    %rdx,%rax
   0x0000555555554bc1 <+983>:	add    %rcx,%rax
   0x0000555555554bc4 <+986>:	mov    -0x480(%rbp,%rax,4),%eax
   0x0000555555554bcb <+993>:	cmp    $0x1,%eax
   0x0000555555554bce <+996>:	je     0x555555554d08 <main+1310>
   0x0000555555554bd4 <+1002>:	subl   $0x1,-0x4a0(%rbp)
   0x0000555555554bdb <+1009>:	jmpq   0x555555554d08 <main+1310>
   0x0000555555554be0 <+1014>:	mov    -0x494(%rbp),%eax
   0x0000555555554be6 <+1020>:	cltq   
   0x0000555555554be8 <+1022>:	movzbl -0x150(%rbp,%rax,1),%eax
   0x0000555555554bf0 <+1030>:	cmp    $0x44,%al
   0x0000555555554bf2 <+1032>:	jne    0x555555554c4a <main+1120>
   0x0000555555554bf4 <+1034>:	mov    -0x4a0(%rbp),%eax
   0x0000555555554bfa <+1040>:	add    $0x1,%eax
   0x0000555555554bfd <+1043>:	cmp    $0x12,%eax
   0x0000555555554c00 <+1046>:	jg     0x555555554d08 <main+1310>
   0x0000555555554c06 <+1052>:	mov    -0x4a0(%rbp),%eax
   0x0000555555554c0c <+1058>:	lea    0x1(%rax),%edx
   0x0000555555554c0f <+1061>:	mov    -0x49c(%rbp),%eax
   0x0000555555554c15 <+1067>:	movslq %eax,%rcx
   0x0000555555554c18 <+1070>:	movslq %edx,%rdx
   0x0000555555554c1b <+1073>:	mov    %rdx,%rax
   0x0000555555554c1e <+1076>:	shl    $0x3,%rax
   0x0000555555554c22 <+1080>:	add    %rdx,%rax
   0x0000555555554c25 <+1083>:	add    %rax,%rax
   0x0000555555554c28 <+1086>:	add    %rdx,%rax
   0x0000555555554c2b <+1089>:	add    %rcx,%rax
   0x0000555555554c2e <+1092>:	mov    -0x480(%rbp,%rax,4),%eax
   0x0000555555554c35 <+1099>:	cmp    $0x1,%eax
   0x0000555555554c38 <+1102>:	je     0x555555554d08 <main+1310>
   0x0000555555554c3e <+1108>:	addl   $0x1,-0x4a0(%rbp)
   0x0000555555554c45 <+1115>:	jmpq   0x555555554d08 <main+1310>
   0x0000555555554c4a <+1120>:	mov    -0x494(%rbp),%eax
   0x0000555555554c50 <+1126>:	cltq   
   0x0000555555554c52 <+1128>:	movzbl -0x150(%rbp,%rax,1),%eax
   0x0000555555554c5a <+1136>:	cmp    $0x4c,%al
   0x0000555555554c5c <+1138>:	jne    0x555555554cac <main+1218>
   0x0000555555554c5e <+1140>:	mov    -0x49c(%rbp),%eax
   0x0000555555554c64 <+1146>:	sub    $0x1,%eax
   0x0000555555554c67 <+1149>:	test   %eax,%eax
   0x0000555555554c69 <+1151>:	js     0x555555554d08 <main+1310>
   0x0000555555554c6f <+1157>:	mov    -0x49c(%rbp),%eax
   0x0000555555554c75 <+1163>:	sub    $0x1,%eax
   0x0000555555554c78 <+1166>:	movslq %eax,%rcx
   0x0000555555554c7b <+1169>:	mov    -0x4a0(%rbp),%eax
   0x0000555555554c81 <+1175>:	movslq %eax,%rdx
   0x0000555555554c84 <+1178>:	mov    %rdx,%rax
   0x0000555555554c87 <+1181>:	shl    $0x3,%rax
   0x0000555555554c8b <+1185>:	add    %rdx,%rax
   0x0000555555554c8e <+1188>:	add    %rax,%rax
   0x0000555555554c91 <+1191>:	add    %rdx,%rax
   0x0000555555554c94 <+1194>:	add    %rcx,%rax
   0x0000555555554c97 <+1197>:	mov    -0x480(%rbp,%rax,4),%eax
   0x0000555555554c9e <+1204>:	cmp    $0x1,%eax
   0x0000555555554ca1 <+1207>:	je     0x555555554d08 <main+1310>
   0x0000555555554ca3 <+1209>:	subl   $0x1,-0x49c(%rbp)
   0x0000555555554caa <+1216>:	jmp    0x555555554d08 <main+1310>
   0x0000555555554cac <+1218>:	mov    -0x494(%rbp),%eax
   0x0000555555554cb2 <+1224>:	cltq   
   0x0000555555554cb4 <+1226>:	movzbl -0x150(%rbp,%rax,1),%eax
   0x0000555555554cbc <+1234>:	cmp    $0x52,%al
   0x0000555555554cbe <+1236>:	jne    0x555555554d08 <main+1310>
   0x0000555555554cc0 <+1238>:	mov    -0x49c(%rbp),%eax
   0x0000555555554cc6 <+1244>:	add    $0x1,%eax
   0x0000555555554cc9 <+1247>:	test   %eax,%eax
   0x0000555555554ccb <+1249>:	js     0x555555554d08 <main+1310>
   0x0000555555554ccd <+1251>:	mov    -0x49c(%rbp),%eax
   0x0000555555554cd3 <+1257>:	add    $0x1,%eax
   0x0000555555554cd6 <+1260>:	movslq %eax,%rcx
   0x0000555555554cd9 <+1263>:	mov    -0x4a0(%rbp),%eax
   0x0000555555554cdf <+1269>:	movslq %eax,%rdx
   0x0000555555554ce2 <+1272>:	mov    %rdx,%rax
   0x0000555555554ce5 <+1275>:	shl    $0x3,%rax
   0x0000555555554ce9 <+1279>:	add    %rdx,%rax
   0x0000555555554cec <+1282>:	add    %rax,%rax
   0x0000555555554cef <+1285>:	add    %rdx,%rax
   0x0000555555554cf2 <+1288>:	add    %rcx,%rax
   0x0000555555554cf5 <+1291>:	mov    -0x480(%rbp,%rax,4),%eax
   0x0000555555554cfc <+1298>:	cmp    $0x1,%eax
   0x0000555555554cff <+1301>:	je     0x555555554d08 <main+1310>
   0x0000555555554d01 <+1303>:	addl   $0x1,-0x49c(%rbp)
   0x0000555555554d08 <+1310>:	mov    -0x49c(%rbp),%eax
   0x0000555555554d0e <+1316>:	movslq %eax,%rcx
   0x0000555555554d11 <+1319>:	mov    -0x4a0(%rbp),%eax
   0x0000555555554d17 <+1325>:	movslq %eax,%rdx
   0x0000555555554d1a <+1328>:	mov    %rdx,%rax
   0x0000555555554d1d <+1331>:	shl    $0x3,%rax
   0x0000555555554d21 <+1335>:	add    %rdx,%rax
   0x0000555555554d24 <+1338>:	add    %rax,%rax
   0x0000555555554d27 <+1341>:	add    %rdx,%rax
   0x0000555555554d2a <+1344>:	add    %rcx,%rax
   0x0000555555554d2d <+1347>:	mov    -0x480(%rbp,%rax,4),%eax
   0x0000555555554d34 <+1354>:	cmp    $0x2,%eax
   0x0000555555554d37 <+1357>:	jne    0x555555554d42 <main+1368>
   0x0000555555554d39 <+1359>:	addl   $0x1,-0x498(%rbp)
   0x0000555555554d40 <+1366>:	jmp    0x555555554d6a <main+1408>
   0x0000555555554d42 <+1368>:	addl   $0x1,-0x494(%rbp)
   0x0000555555554d49 <+1375>:	mov    -0x494(%rbp),%eax
   0x0000555555554d4f <+1381>:	movslq %eax,%rbx
   0x0000555555554d52 <+1384>:	lea    -0x150(%rbp),%rax
   0x0000555555554d59 <+1391>:	mov    %rax,%rdi
   0x0000555555554d5c <+1394>:	callq  0x555555554680 <strlen@plt>
   0x0000555555554d61 <+1399>:	cmp    %rax,%rbx
   0x0000555555554d64 <+1402>:	jb     0x555555554b77 <main+909>
   0x0000555555554d6a <+1408>:	cmpl   $0x0,-0x498(%rbp)
   0x0000555555554d71 <+1415>:	je     0x555555554d8d <main+1443>
   0x0000555555554d73 <+1417>:	lea    0x6f6(%rip),%rdi        # 0x555555555470
   0x0000555555554d7a <+1424>:	callq  0x555555554670 <puts@plt>
   0x0000555555554d7f <+1429>:	lea    0x774(%rip),%rdi        # 0x5555555554fa
   0x0000555555554d86 <+1436>:	callq  0x555555554670 <puts@plt>
   0x0000555555554d8b <+1441>:	jmp    0x555555554d99 <main+1455>
   0x0000555555554d8d <+1443>:	lea    0x77c(%rip),%rdi        # 0x555555555510
   0x0000555555554d94 <+1450>:	callq  0x555555554670 <puts@plt>
   0x0000555555554d99 <+1455>:	mov    $0x0,%eax
   0x0000555555554d9e <+1460>:	mov    -0x18(%rbp),%rsi
   0x0000555555554da2 <+1464>:	xor    %fs:0x28,%rsi
   0x0000555555554dab <+1473>:	je     0x555555554db2 <main+1480>
   0x0000555555554dad <+1475>:	callq  0x555555554690 <__stack_chk_fail@plt>
   0x0000555555554db2 <+1480>:	add    $0x4c8,%rsp
   0x0000555555554db9 <+1487>:	pop    %rbx
   0x0000555555554dba <+1488>:	pop    %rbp
   0x0000555555554dbb <+1489>:	retq  
```

I start by, per usual, segmenting the assembly into apparently logical chunks, which would represent an understandable chunk of the original source:

```x86asm
   0x00005555555547ea <+0>:	push   %rbp
   0x00005555555547eb <+1>:	mov    %rsp,%rbp
   0x00005555555547ee <+4>:	push   %rbx
   0x00005555555547ef <+5>:	sub    $0x4c8,%rsp
   0x00005555555547f6 <+12>:	mov    %edi,-0x4c4(%rbp)
   0x00005555555547fc <+18>:	mov    %rsi,-0x4d0(%rbp)
   0x0000555555554803 <+25>:	mov    %fs:0x28,%rax
   0x000055555555480c <+34>:	mov    %rax,-0x18(%rbp)
   0x0000555555554810 <+38>:	xor    %eax,%eax
   0x0000555555554812 <+40>:	lea    0x62f(%rip),%rdi        # 0x555555554e48
   0x0000555555554819 <+47>:	callq  0x555555554670 <puts@plt>
   0x000055555555481e <+52>:	movl   $0x0,-0x4b0(%rbp)
   0x0000555555554828 <+62>:	movl   $0x89,-0x490(%rbp)
   0x0000555555554832 <+72>:	movl   $0xbb,-0x48c(%rbp)
   0x000055555555483c <+82>:	movl   $0x800,-0x488(%rbp)
   0x0000555555554846 <+92>:	movl   $0x0,-0x484(%rbp)
   0x0000555555554850 <+102>:	movl   $0x0,-0x4ac(%rbp)
   0x000055555555485a <+112>:	movl   $0x0,-0x4a8(%rbp)
   0x0000555555554864 <+122>:	lea    0xaec(%rip),%rdi        # 0x555555555357
   0x000055555555486b <+129>:	callq  0x555555554670 <puts@plt>
   0x0000555555554870 <+134>:	lea    0xb01(%rip),%rdi        # 0x555555555378
   0x0000555555554877 <+141>:	callq  0x555555554670 <puts@plt>
   0x000055555555487c <+146>:	lea    0xb3d(%rip),%rdi        # 0x5555555553c0
   0x0000555555554883 <+153>:	callq  0x555555554670 <puts@plt>
```

The `sub $0x4c8, %rsp` honestly gives me a preemptive caution, if this function is allocating this much local variable space, then either you have a huge variable scope, or relatively small amount of floating point/vector types, which is scary either way.
Regardless, this translates to the following:

```c
int
main (
  int argc,         /* -0x4c4(%rbp) */
  char** argv   /* -0x4d0(%rbp) */
  )
{
  int unk_1 = 0x89;     /*  -0x490(%rbp) */
  int unk_2 = 0xbb;     /* -0x48c(%rbp) */
  int unk_3 = 0x800;    /* -0x488(%rbp) */
  int unk_4 = 0x0;        /* -0x4a8(%rbp) */
  puts (star);    /* (char *)0x555555554e48 */
  puts ("YOU REALLY THINK THAT SACRIFICE A GOAT IS ENOUGH TO JOIN OUR CULT ?");
  puts ("MOUAHAHAHAHAH YOU MUST FIND THE WAY TO FREE BAPHOMET IF YOU WANT TO BECOME ONE OF HIS CHILDREN GOOD LUCK !");
  /* ... */;
}
```

So, nothing that hard to begin with, I continue:

```x86asm
   0x0000555555554888 <+158>:	lea    0xb9c(%rip),%rdi        # 0x55555555542b
   0x000055555555488f <+165>:	mov    $0x0,%eax
   0x0000555555554894 <+170>:	callq  0x5555555546a0 <printf@plt>
   0x0000555555554899 <+175>:	lea    -0x170(%rbp),%rax
   0x00005555555548a0 <+182>:	mov    %rax,%rsi
   0x00005555555548a3 <+185>:	lea    0xb95(%rip),%rdi        # 0x55555555543f
   0x00005555555548aa <+192>:	mov    $0x0,%eax
   0x00005555555548af <+197>:	callq  0x5555555546b0 <__isoc99_scanf@plt>
   0x00005555555548b4 <+202>:	movl   $0x0,-0x4b4(%rbp)
   0x00005555555548be <+212>:	jmpq   0x555555554965 <main+379>
   0x00005555555548c3 <+217>:	mov    -0x4b4(%rbp),%eax
   0x00005555555548c9 <+223>:	cltq   
   0x00005555555548cb <+225>:	movzbl -0x170(%rbp,%rax,1),%eax
   0x00005555555548d3 <+233>:	movsbl %al,%eax
   0x00005555555548d6 <+236>:	mov    %eax,-0x484(%rbp)
   0x00005555555548dc <+242>:	mov    -0x484(%rbp),%eax
   0x00005555555548e2 <+248>:	mov    %eax,-0x4ac(%rbp)
   0x00005555555548e8 <+254>:	movl   $0x0,-0x4b0(%rbp)
   0x00005555555548f2 <+264>:	jmp    0x55555555491f <main+309>
   0x00005555555548f4 <+266>:	mov    -0x490(%rbp),%eax
   0x00005555555548fa <+272>:	imul   -0x4ac(%rbp),%eax
   0x0000555555554901 <+279>:	mov    %eax,%edx
   0x0000555555554903 <+281>:	mov    -0x48c(%rbp),%eax
   0x0000555555554909 <+287>:	add    %edx,%eax
   0x000055555555490b <+289>:	cltd   
   0x000055555555490c <+290>:	idivl  -0x488(%rbp)
   0x0000555555554912 <+296>:	mov    %edx,-0x4ac(%rbp)
   0x0000555555554918 <+302>:	addl   $0x1,-0x4b0(%rbp)
   0x000055555555491f <+309>:	mov    -0x4b4(%rbp),%eax
   0x0000555555554925 <+315>:	cltq   
   0x0000555555554927 <+317>:	movzbl -0x170(%rbp,%rax,1),%eax
   0x000055555555492f <+325>:	movsbl %al,%eax
   0x0000555555554932 <+328>:	add    $0x4a,%eax
   0x0000555555554935 <+331>:	cmp    %eax,-0x4b0(%rbp)
   0x000055555555493b <+337>:	jl     0x5555555548f4 <main+266>
   0x000055555555493d <+339>:	mov    -0x4ac(%rbp),%eax
   0x0000555555554943 <+345>:	imul   $0x29a,%eax,%edx
   0x0000555555554949 <+351>:	mov    -0x4ac(%rbp),%eax
   0x000055555555494f <+357>:	imul   $0x29a,%eax,%eax
   0x0000555555554955 <+363>:	imul   %edx,%eax
   0x0000555555554958 <+366>:	add    %eax,-0x4a8(%rbp)
   0x000055555555495e <+372>:	addl   $0x1,-0x4b4(%rbp)
   0x0000555555554965 <+379>:	mov    -0x4b4(%rbp),%eax
   0x000055555555496b <+385>:	movslq %eax,%rbx
   0x000055555555496e <+388>:	lea    -0x170(%rbp),%rax
   0x0000555555554975 <+395>:	mov    %rax,%rdi
   0x0000555555554978 <+398>:	callq  0x555555554680 <strlen@plt>
   0x000055555555497d <+403>:	cmp    %rax,%rbx
   0x0000555555554980 <+406>:	jb     0x5555555548c3 <main+217>
   0x0000555555554986 <+412>:	movl   $0x0,-0x4b4(%rbp)
   0x0000555555554990 <+422>:	jmpq   0x555555554a27 <main+573>
```

Translates to:

```c
int
main (
  int argc,         /* -0x4c4(%rbp) */
  char** argv   /* -0x4d0(%rbp) */
  )
{
  char name[64];   /* -0x170(%rbp), guessed length */
  int var_1 = 0;       /* -0x4b4(%rbp) */
  int unk_1 = 0x89;     /*  -0x490(%rbp) */
  int unk_2 = 0xbb;     /* -0x48c(%rbp) */
  int unk_3 = 0x800;    /* -0x488(%rbp) */
  int unk_4 = 0x0;        /* -0x4a8(%rbp) */
  puts (star);    /* (char *)0x555555554e48 */
  puts ("YOU REALLY THINK THAT SACRIFICE A GOAT IS ENOUGH TO JOIN OUR CULT ?");
  puts ("MOUAHAHAHAHAH YOU MUST FIND THE WAY TO FREE BAPHOMET IF YOU WANT TO BECOME ONE OF HIS CHILDREN GOOD LUCK !");
  printf ("TELL US YOUR NAME: ");
  scanf ("%s", &name);
  while (var_1 < strlen (name))
    {
      char chr = name[var_1];   /* -0x484(%rbp) */
      char chr_copy = name[var_1];    /* -0x4ac(%rbp) ?? */
      int var_2 = 0;    /* -0x4b0(%rbp) */
      while (1)
        {
          if (var_2  < name[var_1] + 0x4a)
            {
              chr_copy = unk_2 + chr_copy  * unk_1) % unk_3;
              var_2++;
              continue;
            }
          unk_4 += (chr_copy  * 0x29a) * (chr_copy * 0x29a);
          var_1++;
          break;
        }
    }
    var_1 = 0;
    /* ... */
}
```

There is most likely a compact reduction of this that can be applied, but I do not see it immediately; I am, however, starting to see some of the essence behind the code, perhaps `unk_4` is some component of hashing (since `chr_copy = unk_2 + chr_copy * unk_1) % unk_3` is lossy), so `unk_4` may be considered a key. The reason for the duplicate `chr`, `chr_copy` variables is still unsure to me, as `chr` is not used in the proceeding logic, it is only mentioned at `+242`, which corresponds to our `char chr = name[var_1];`, and immediately after which also corresponds to the `char chr_copy = name[var_1];` which is more precisely `char chr_copy = chr;`. Perhaps it wil be more obvious later. I continue:

```x86asm
   0x0000555555554986 <+412>:	movl   $0x0,-0x4b4(%rbp)
   0x0000555555554990 <+422>:	jmpq   0x555555554a27 <main+573>
   0x0000555555554995 <+427>:	movl   $0x0,-0x4b0(%rbp)
   0x000055555555499f <+437>:	jmp    0x555555554a17 <main+557>
   0x00005555555549a1 <+439>:	mov    -0x4b0(%rbp),%eax
   0x00005555555549a7 <+445>:	and    $0x1,%eax
   0x00005555555549aa <+448>:	test   %eax,%eax
   0x00005555555549ac <+450>:	je     0x5555555549e0 <main+502>
   0x00005555555549ae <+452>:	mov    -0x4b0(%rbp),%eax
   0x00005555555549b4 <+458>:	movslq %eax,%rcx
   0x00005555555549b7 <+461>:	mov    -0x4b4(%rbp),%eax
   0x00005555555549bd <+467>:	movslq %eax,%rdx
   0x00005555555549c0 <+470>:	mov    %rdx,%rax
   0x00005555555549c3 <+473>:	shl    $0x3,%rax
   0x00005555555549c7 <+477>:	add    %rdx,%rax
   0x00005555555549ca <+480>:	add    %rax,%rax
   0x00005555555549cd <+483>:	add    %rdx,%rax
   0x00005555555549d0 <+486>:	add    %rcx,%rax
   0x00005555555549d3 <+489>:	movl   $0x1,-0x480(%rbp,%rax,4)
   0x00005555555549de <+500>:	jmp    0x555555554a10 <main+550>
   0x00005555555549e0 <+502>:	mov    -0x4b0(%rbp),%eax
   0x00005555555549e6 <+508>:	movslq %eax,%rcx
   0x00005555555549e9 <+511>:	mov    -0x4b4(%rbp),%eax
   0x00005555555549ef <+517>:	movslq %eax,%rdx
   0x00005555555549f2 <+520>:	mov    %rdx,%rax
   0x00005555555549f5 <+523>:	shl    $0x3,%rax
   0x00005555555549f9 <+527>:	add    %rdx,%rax
   0x00005555555549fc <+530>:	add    %rax,%rax
   0x00005555555549ff <+533>:	add    %rdx,%rax
   0x0000555555554a02 <+536>:	add    %rcx,%rax
   0x0000555555554a05 <+539>:	movl   $0x0,-0x480(%rbp,%rax,4)
   0x0000555555554a10 <+550>:	addl   $0x1,-0x4b0(%rbp)
   0x0000555555554a17 <+557>:	cmpl   $0x12,-0x4b0(%rbp)
   0x0000555555554a1e <+564>:	jle    0x5555555549a1 <main+439>
   0x0000555555554a20 <+566>:	addl   $0x1,-0x4b4(%rbp)
   0x0000555555554a27 <+573>:	cmpl   $0x9,-0x4b4(%rbp)
   0x0000555555554a2e <+580>:	jle    0x555555554995 <main+427>
```

Corresponding to:

```c
int
main (
  int argc,         /* -0x4c4(%rbp) */
  char** argv   /* -0x4d0(%rbp) */
  )
{
  char name[64];   /* -0x170(%rbp), guessed length */
  int var_1 = 0;       /* -0x4b4(%rbp) */
  int unk_1 = 0x89;     /*  -0x490(%rbp) */
  int unk_2 = 0xbb;     /* -0x48c(%rbp) */
  int unk_3 = 0x800;    /* -0x488(%rbp) */
  int unk_4 = 0x0;        /* -0x4a8(%rbp) */
  puts (star);    /* (char *)0x555555554e48 */
  puts ("YOU REALLY THINK THAT SACRIFICE A GOAT IS ENOUGH TO JOIN OUR CULT ?");
  puts ("MOUAHAHAHAHAH YOU MUST FIND THE WAY TO FREE BAPHOMET IF YOU WANT TO BECOME ONE OF HIS CHILDREN GOOD LUCK !");
  printf ("TELL US YOUR NAME: ");
  scanf ("%s", &name);
  while (var_1 < strlen (name))
    {
      char chr = name[var_1];   /* -0x484(%rbp) */
      char chr_copy = name[var_1];    /* -0x4ac(%rbp) ?? */
      int var_2 = 0;    /* -0x4b0(%rbp) */
      int arr_1[0xbe];  /* -0x480(%rbp) */
      while (1)
        {
          if (var_2  < name[var_1] + 0x4a)
            {
              chr_copy = unk_2 + chr_copy  * unk_1) % unk_3;
              var_2++;
              continue;
            }
          unk_4 += (chr_copy  * 0x29a) * (chr_copy * 0x29a);
          var_1++;
          break;
        }
    }
    var_1 = 0;
    while (var_1 <= 0x9)
      {
        var_2 = 0;
        while (var_2 <= 0x12)
          {
            int old_var_1;
            if (var_2 & 0x1 == 0)
              {
                old_var_1 = var_1
                var_1 <<= 0x3;
                var_1 += old_var_1;
                var_1 += var_1;
                var_1 += old_var_1;
                var_1 += var_2;
                arr_1[var_1] = 1;   /* ?? */
              }
            else
              {
                old_var_1 = var_1;
                var_1 <<= 0x3;
                var_1 += old_var_1;
                var_1 += var_1;
                var_1 += old_var_1;
                var_1 += var_2;
                arr_1[var_1] = 0;   /* ?? */
              }
            var_2++;
          }
        var_1++;
      }
      /* ... */
}
```

One remark about this disassembly and logic pertains to both cases of `arr_1[var_1] = 0/1`, since it seems to me that `var_1` can become very large, as suppose `var_1 == 0x9`, and `var_2 == 0x12` (edges of both while-loops), then we would take the first condition, as `0x12 & 0x1 == 0`, so, `old_var_1 == 0x9`, then:

```py
>>> old_var_1 = 0x9
>>> var_1 = 0x9
>>> var_2 = 0x12
>>> var_1 <<= 0x3
>>> var_1 += old_var_1
>>> var_1 += var_1
>>> var_1 += old_var_1
>>> var_1 += var_2
>>> var_1 += var_12
>>> var_1
189
```

So, we'd be accessing the `190`th element of `arr_1`, which entails 760 bytes of stack-space, which should theoretically indicate that there shouldn't exist stack items in the range `[-0x188, -0x480](%rbp)`, which from a glance seems to hold true, as the first stack variable that I could find which bordered this range was `-0x150(%rbp)` on `+827`, and `-0x484(%rbp)` at `+82`. So we may be content with that this array is 190 (0xbe) elements big.

TBF
