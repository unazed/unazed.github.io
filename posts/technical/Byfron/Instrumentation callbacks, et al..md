The instrumentation callback is fairly standard:

```c
push    r10 {ic_return_address}
push    rax {__saved_rax}
pushfq   {flags}
push    rbx {__saved_rbx}
mov     rbx, rsp {__saved_rbx}
lea     rax, [rel instrumentation_callback]
cmp     rcx, rax
cmove   rcx, r10
lea     r10, [rsp-0xc0 {var_e0}]
and     r10 {var_e0}, 0xfffffffffffffff0
mov     rsp, r10
cld     
mov     qword [rsp+0xb0 {target_address_1}], rcx
mov     qword [rsp+0xa8 {__saved_rdx}], rdx
mov     qword [rsp+0xa0 {__saved_r8}], r8
mov     qword [rsp+0x98 {__saved_r9}], r9
mov     qword [rsp+0x90 {__saved_r11}], r11
movaps  xmmword [rsp+0x80 {__saved_zmm0}], xmm0
movaps  xmmword [rsp+0x70 {__saved_zmm1}], xmm1
movaps  xmmword [rsp+0x60 {__saved_zmm2}], xmm2
movaps  xmmword [rsp+0x50 {__saved_zmm3}], xmm3
movaps  xmmword [rsp+0x40 {__saved_zmm4}], xmm4
movaps  xmmword [rsp+0x30 {__saved_zmm5}], xmm5
mov     rcx, qword [rbx+0x18 {ic_return_address}]
call    ic_to_LdrInitThunk_or_UserApcDispatch
mov     qword [rbx+0x18 {var_8}], rax
mov     rcx, qword [rsp+0xb0 {target_address_1}]
mov     rdx, qword [rsp+0xa8 {__saved_rdx}]
mov     r8, qword [rsp+0xa0 {__saved_r8}]
mov     r9, qword [rsp+0x98 {__saved_r9}]
mov     r11, qword [rsp+0x90 {__saved_r11}]
movaps  xmm0, xmmword [rsp+0x80 {__saved_zmm0}]
movaps  xmm1, xmmword [rsp+0x70 {__saved_zmm1}]
movaps  xmm2, xmmword [rsp+0x60 {__saved_zmm2}]
movaps  xmm3, xmmword [rsp+0x50 {__saved_zmm3}]
movaps  xmm4, xmmword [rsp+0x40 {__saved_zmm4}]
movaps  xmm5, xmmword [rsp+0x30 {__saved_zmm5}]
mov     rsp, rbx
pop     rbx {__saved_rbx}
popfq   
pop     rax {__saved_rax}
pop     r10 {var_8}
jmp     r10
```

Which simply boils down to:

```c
void
instrumentation_callback (
	uint64_t* target /* rcx */, uint64_t* return_rip /* r10 */)
{
	if (target == instrumentation_callback)
		target = return_rip;
	__jump (ic_to_LdrInitThunk_or_UserApcDispatch (return_rip));
}
```

Then, the proceeding function essentially switches against `return_rip` to determine which function was called, and act based on that:

```c
void
ic_to_LdrInitThunk_or_UserApcDispatch (uint64_t* return_rip /* rcx */)
{
	switch (return_rip)
	{
		case &LdrInitializeThunk:
			__clearTrap ();
			return &ic_LdrInitializeThunk;
		case &KiUserApcDispatcher:
			return &ic_KiUserApcDispatcher;
	}
	/* these functions not matched, read below */
}
```

Essentially injecting its own intermediate functionality for either Windows function, if neither function is matched, then it continues as such:

```c
if (!__teb->ExceptionList)
{
	if (return_rip == &KiUserExceptionDispatcher)
		return &ic_KiUserApcDispatcher;
	__clearTrap ();
	return /* `return_rip`, unmodified */;
}
```