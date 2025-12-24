Prior to my last expedition into the binary, and my untimely departure upon encountering how obscurely system calls appeared to be invoked, I am glad to see that they don't appear to have changed much since in methodology, observe:

```c
int64_t r11 = *data_7ffc380f13d8
uint32_t rdx = zx.d(r11.w)
int32_t r8_3 = (((rdx ^ 0x38f5a4d4) << 2) * rdx + 0x1c296cb0) ^ 0x38f5a4d4
uint32_t rax = zx.d((r11 u>> 0x20).w)
int32_t r10_1 = rol.d(r8_3, 0x1b)
int32_t r14_2 = (r11.d u>> 0x10) * rol.d(r8_3 + rax, 0x1b)
int32_t r10_2 = r10_1 * r14_2

if (
	zx.q(
		(not.d(0x5bfddd16 * *(arg2 + 0x418)) ^ 0xc0d9cf6d
	) * 0x58cdbd1f)
	< zx.q(not.d(rol.d(0x5e21c6b, arg3)))
)
	r10_2 = r14_2 + r10_1

int32_t r10_3 = r10_2 ^ r8_3
int32_t r9_8 = rol.d(r10_3, 0x15) ^ ((rdx ^ r10_3) * rax) ^ r10_3
uint64_t rcx_10 = zx.q(rol.d(r9_8, 0x1b)) ^ zx.q(rol.d(rax - r9_8, 2) * (r11 u>> 0x30).d) ^ zx.q(r9_8)
*(arg2 + 0x980) = rcx_10
*((0xc091ec38 ^ rcx_10) + sx.q(not.d(ror.d(0x86086c4, (*(arg2 + 0x308)).b)) + (*(arg2 + 0xfe0)).d) + &data_7ffc38116ef7)
void* arg_30 = arg2 + 0x32c
int32_t arg_28 = 0
int64_t rcx_14 = syscall(arg1, 4, 3, arg2 + 0x9d0)
```

The largest problem, as before, being the first line:

```c
mov     r8, qword [rel data]
mov     r9, qword [r8]
```

Since, at the point of being dumped, the data stored at that location resembles this pattern:

![[Pasted image 20251202161614.png | center]]

Which, all besides the occasional `0x1e472d7c_XXX`, is prefixed with `0xdb9b0_XXXXXXXXX`, this may serve to be useful in pattern-matching, but for the moment meaningless.