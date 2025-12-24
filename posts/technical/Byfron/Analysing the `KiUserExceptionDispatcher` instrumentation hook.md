A fundamental stack memory structure is referenced relative to `rbp`, `0x2368 (9064)` bytes large. It is the local variable space for the function, and it significantly padded with garbage values and opaque predicate determinates. We can assume that the first parameters of this function are identical to the real `KiUserExceptionDispatcher` function, thus:

```c
void hook_KiUserExceptionDispatcher (PEXCEPTION_RECORD exc_record, PCONTEXT exc_context)
```

Passed in `rcx`/`rdx` respectively, per the standard Windows calling convention. Note that decompilation has been significantly cleaned through eliminating simple opaque predicates and renamed data references. The first order of business:

```c
uint64_t table_1_index_2 = zx.q(table_1_index)
char r8 = rol.b((&table_1)[table_1_index_2][0], 5)
table_1_bytes__dllBase:0.b = table_1_xor[0] ^ r8
table_1_bytes__dllBase:1.b =
rol.b(table_1[1 + (table_1_index_2 << 3)], 5) ^ table_1_xor[1][0]
char r8_2 = table_1[2 + (table_1_index_2 << 3)]
table_1_bytes__dllBase:2.b = rol.b(r8_2, 5) ^ table_1_xor[2][0]
table_1_bytes__dllBase:3.b =
rol.b(table_1[3 + (table_1_index_2 << 3)], 5) ^ table_1_xor[3][0]
char r12_1 = table_1_xor[4][0]
table_1_bytes__dllBase:4.b =
rol.b(table_1[4 + (table_1_index_2 << 3)], 5) ^ r12_1
table_1_bytes__dllBase:5.b =
rol.b(table_1[5 + (table_1_index_2 << 3)], 5) ^ table_1_xor[5][0]
uint64_t table_1_byte_6_rol_1
table_1_byte_6_rol_1.b = rol.b(table_1[6 + (table_1_index_2 << 3)], 5)
table_1_bytes__dllBase:6.b = table_1_xor[6][0] ^ table_1_byte_6_rol_1.b
char r13_1 = rol.b(table_1[7 + (table_1_index_2 << 3)], 5)
table_1_bytes__dllBase:7.b = table_1_xor[7][0] ^ r13_1
if (exc_context u< table_1_bytes__dllBase)
{ ... }
```

The disassembly is mildly more obfuscated, and given that we can assume `table_1_index` is always `0x1` (as no cross-references indicate it is overwritten, unlike other indices introduced later), then the real address of `table_1` is `0x7ffc3813224a` (the `lea` has a constant-offset of `0x11`.)  `table_1_xor` consists entirely of zeros, therefore this is just a transmutation cipher, which we can decode:

```c
#include <stdio.h>
#include <inttypes.h>
#include <stdlib.h>
#include <stdint.h>

static uint8_t table_1[8] = {
        0x00, 0x00, 0x70, 0xc1,
        0xe7, 0xfb, 0x00, 0x00
};

int
main (void)
{
        uint8_t bytes[8] = { 0 };
        for (uint8_t i = 0; i < 8; ++i)
                bytes[i] = rotl8 (table_1[i], 5);
        printf ("bytes.q=0x%" PRIx64 "\n", *(uint64_t *)bytes);
        return EXIT_SUCCESS;
}
```

Yields `0x7ffc380e0000`: the base address of the module, so we may begin to anticipate that an upper bound will come. So far, we have the following:

```c
void
hook_KiUserExceptionDispatcher (PEXCEPTION_RECORD exc_record, PCONTEXT exc_context)
{
	uint8_t module_base[8];
	for (uint8_t i = 0; i < sizeof (table_1); ++i)
		module_base[i] = rotl8 (table_1[i], 5);
	if (exc_context < *(uint64_t *)module_base)
	{
		/* ... */
	}
}
```

So, we're checking if the pointer to the exception's context is outside of the module's bounds: does this make sense? Yes, if the allocation was made on the heap/stack, of which the stack would seem to be the most typical case. Moving forward:

```c
if (exc_context u< table_1_bytes__dllBase)
{
check_context_in_stack_bounds:
	if (exc_context_1 u>= Self->NtTib.StackLimit)
		_0x18_if_ctx_valid_else_0x8 = 0x18
	
	if (exc_context_1 u>= Self->NtTib.StackLimit
			&& exc_context_1 u< Self->NtTib.StackBase)
		goto exit_check_context_in_stack_bounds
	
	table_1_bytes__dllBase.d = 0x7d309f99
}
else
{
	uint64_t table_2_index_1 = zx.q(table_2_index)
	table_2_bytes__dllEnd:0.b = ror.b(not.b((&table_2)[table_2_index_1][0]), 1)
	table_2_bytes__dllEnd:1.b = ror.b(not.b((&table_2)[1][table_2_index_1][0]), 1)
	table_2_bytes__dllEnd:2.b = ror.b(not.b((&table_2)[2][table_2_index_1][0]), 1)
	table_2_bytes__dllEnd:3.b = ror.b(not.b((&table_2)[3][table_2_index_1][0]), 1)
	table_2_bytes__dllEnd:4.b = ror.b(not.b((&table_2)[4][table_2_index_1][0]), 1)
	table_2_bytes__dllEnd:5.b = ror.b(not.b((&table_2)[5][table_2_index_1][0]), 1)
	table_2_bytes__dllEnd:6.b = ror.b(not.b((&table_2)[6][table_2_index_1][0]), 1)
	table_2_bytes__dllEnd:7.b = ror.b(not.b((&table_2)[7][table_2_index_1][0]), 1)
	_0x18_if_ctx_valid_else_0x8 = 8
	
	if (exc_context_1 u>= table_2_bytes__dllEnd)
		goto check_context_in_stack_bounds
}
exit_check_context_in_stack_bounds:
```

Applying a similar methodology for `table_2`, we discover that it is the end of the module at `0x7ffc392b0000`, so we may simplify the branches to this:

```c
if (exc_context < dllBase || exc_context >= dllEnd)
{
	uint64_t is_context_valid = 0x8;
	if (exc_context >= NtTib.StackLimit)
	{
		is_context_valid = 0x18;
		if (exc_context < NtTib.StackBase)
			goto exit;
	}
}
```

Now, note that when cross-referencing how `is_context_valid` is used in later portions of the decompilation, it seems to be mostly meaningless to execution, however it does incur side-effects that are meaningful, i.e.:

![[Pasted image 20251204094321.png | center]]

Which in either case of a valid exception context, refers to `0x2e92` or `0x4883`--not that it is stored. Regardless, this dereferences valid memory so it has no cause for concern regarding access violations, and since we are the exception dispatcher, we (probably) wouldn't want to invoke any further exceptions on trapped page accesses or similar, so we may likely treat this as benign.
This begs the question, what is the state differential when the context is out of bounds versus otherwise? 