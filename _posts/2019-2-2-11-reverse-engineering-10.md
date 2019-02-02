---
layout: post
title: reverse engineering crackme 10
---

Although this is the tenth crackme, I don't intend to make it specialized as I don't see a point, it will be a traditional (recent) crackme located [here](https://crackmes.one/crackme/5c53840a33c5d475210bc6e9).
The user-defined entry point is located in `_start` opposed to the standard libc-defined `main`:

```assembly
   0x0000000000401000 <+0>:     mov    $0x1,%eax
   0x0000000000401005 <+5>:     mov    $0x1,%edi
   0x000000000040100a <+10>:    movabs $0x402000,%rsi
   0x0000000000401014 <+20>:    mov    $0x19,%edx
   0x0000000000401019 <+25>:    syscall
   0x000000000040101b <+27>:    mov    $0x0,%eax
   0x0000000000401020 <+32>:    mov    $0x0,%edi
   0x0000000000401025 <+37>:    movabs $0x402074,%rsi
   0x000000000040102f <+47>:    mov    $0x20,%edx
   0x0000000000401034 <+52>:    syscall
   0x0000000000401036 <+54>:    cmp    $0x0,%rax
   0x000000000040103a <+58>:    jl     0x401114 <_start.error>
   0x0000000000401040 <+64>:    mov    %rax,%r14
   0x0000000000401043 <+67>:    add    $0x6,%r14
   0x0000000000401047 <+71>:    mov    0x402019,%rax
   0x000000000040104f <+79>:    mov    %rax,0x402094
   0x0000000000401057 <+87>:    mov    0x402074,%rax
   0x000000000040105f <+95>:    mov    %rax,0x40209a
   0x0000000000401067 <+103>:   mov    $0x1,%eax
   0x000000000040106c <+108>:   mov    $0x1,%edi
   0x0000000000401071 <+113>:   movabs $0x402094,%rsi
   0x000000000040107b <+123>:   mov    %r14,%rdx
   0x000000000040107e <+126>:   syscall
   0x0000000000401080 <+128>:   mov    $0x1,%eax
   0x0000000000401085 <+133>:   mov    $0x1,%edi
   0x000000000040108a <+138>:   movabs $0x402020,%rsi
   0x0000000000401094 <+148>:   mov    $0x16,%edx
   0x0000000000401099 <+153>:   syscall
   0x000000000040109b <+155>:   mov    $0x0,%eax
   0x00000000004010a0 <+160>:   mov    $0x0,%edi
   0x00000000004010a5 <+165>:   movabs $0x402074,%rsi
   0x00000000004010af <+175>:   mov    $0x20,%edx
   0x00000000004010b4 <+180>:   syscall
   0x00000000004010b6 <+182>:   mov    %rax,%r15
   0x00000000004010b9 <+185>:   dec    %r15
```

Since, fuck tracing syscalls, I'll run `strace` over the program as I run it and pinpoint the corresponding system-calls:

```
execve("./hello", ["./hello"], [/* 13 vars */]) = 0
write(1, "Please enter your name: \0", 25) = 25
read(0, "a\n", 32)                      = 2
write(1, "Hello a\n", 8)                = 8
write(1, "Enter your Password: \0", 22) = 22
read(0, "b\n", 32)                      = 2
write(1, "Wrong Credentials, ", 24) = 24
exit(4202608)                           = ?
+++ exited with 112 +++
```

And so the prettified assembly:

```assembly
write(1, "Please enter your name: \0", 25)
%rax = read(0, 0x402074, 32)
   0x0000000000401036 <+54>:    cmp    $0x0,%rax
   0x000000000040103a <+58>:    jl     0x401114 <_start.error>
   0x0000000000401040 <+64>:    mov    %rax,%r14
   0x0000000000401043 <+67>:    add    $0x6,%r14
   0x0000000000401047 <+71>:    mov    0x402019,%rax
   0x000000000040104f <+79>:    mov    %rax,0x402094
   0x0000000000401057 <+87>:    mov    0x402074,%rax
   0x000000000040105f <+95>:    mov    %rax,0x40209a
   0x0000000000401067 <+103>:   mov    $0x1,%eax
   0x000000000040106c <+108>:   mov    $0x1,%edi
   0x0000000000401071 <+113>:   movabs $0x402094,%rsi
   0x000000000040107b <+123>:   mov    %r14,%rdx
   0x000000000040107e <+126>:   syscall
   0x0000000000401080 <+128>:   mov    $0x1,%eax
   0x0000000000401085 <+133>:   mov    $0x1,%edi
   0x000000000040108a <+138>:   movabs $0x402020,%rsi
   0x0000000000401094 <+148>:   mov    $0x16,%edx
   0x0000000000401099 <+153>:   syscall
   0x000000000040109b <+155>:   mov    $0x0,%eax
   0x00000000004010a0 <+160>:   mov    $0x0,%edi
   0x00000000004010a5 <+165>:   movabs $0x402074,%rsi
   0x00000000004010af <+175>:   mov    $0x20,%edx
   0x00000000004010b4 <+180>:   syscall
   0x00000000004010b6 <+182>:   mov    %rax,%r15
   0x00000000004010b9 <+185>:   dec    %r15
```

Where `_start.error` is actually mostly undetected by GDB and requires some manual input to disassemble the full function:

```assembly
   0x0000000000401114 <_start.error+0>: mov    %rax,0x402070
   0x000000000040111c <_start.exit+0>:  mov    $0x3c,%eax
   0x0000000000401121 <_start.exit+5>:  movabs $0x402070,%rdi
   0x000000000040112b <_start.exit+15>: syscall
```

Since it leads into the `_start.exit` function it appears, though this seems faulty since `_start.exit+0` immediately overwrites `%rax` as writing to `%eax` will clear the upper-half as defined by the Intel manual, also note the `read` syscall implementation as `ksys_read`:

```c
ssize_t ksys_read(unsigned int fd, char __user *buf, size_t count)
{
	struct fd f = fdget_pos(fd);
	ssize_t ret = -EBADF;

	if (f.file) {
		loff_t pos = file_pos_read(f.file);
		ret = vfs_read(f.file, buf, count, &pos);
		if (ret >= 0)
			file_pos_write(f.file, pos);
		fdput_pos(f);
	}
	return ret;
}
```

The `vfs_read` function is the lowest kernel-scope function for reading a file (AFAIK) as shown [here](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/fs/read_write.c#n437), its declaration is as such:

```c
ssize_t vfs_read(struct file *file, char __user *buf, size_t count, loff_t *pos);
```

It takes a `file` structure, the pointer to the user's out-buffer, how much to read and the offset from the beginning I presume is what the `pos` is: 

```c
ssize_t __vfs_read(struct file *file, char __user *buf, size_t count,
		   loff_t *pos)
{
	if (file->f_op->read)
		return file->f_op->read(file, buf, count, pos);
	else if (file->f_op->read_iter)
		return new_sync_read(file, buf, count, pos);
	else
		return -EINVAL;
}
```

Where `struct file` is defined as:

```c
struct file {
	union {
		struct llist_node	fu_llist;
		struct rcu_head 	fu_rcuhead;
	} f_u;
	struct path		f_path;
	struct inode		*f_inode;	/* cached value */
	const struct file_operations	*f_op;

	/*
	 * Protects f_ep_links, f_flags.
	 * Must not be taken from IRQ context.
	 */
	spinlock_t		f_lock;
	enum rw_hint		f_write_hint;
	atomic_long_t		f_count;
	unsigned int 		f_flags;
	fmode_t			f_mode;
	struct mutex		f_pos_lock;
	loff_t			f_pos;
	struct fown_struct	f_owner;
	const struct cred	*f_cred;
	struct file_ra_state	f_ra;

	u64			f_version;
#ifdef CONFIG_SECURITY
	void			*f_security;
#endif
	/* needed for tty driver, and maybe others */
	void			*private_data;

#ifdef CONFIG_EPOLL
	/* Used by fs/eventpoll.c to link all the hooks to this file */
	struct list_head	f_ep_links;
	struct list_head	f_tfile_llink;
#endif /* #ifdef CONFIG_EPOLL */
	struct address_space	*f_mapping;
	errseq_t		f_wb_err;
} __randomize_layout
  __attribute__((aligned(4)));	/* lest something weird decides that 2 is OK */
```

And the only relevant field is `const struct file_operations	*f_op;` which is defined as:

```c
struct file_operations {
	struct module *owner;
	loff_t (*llseek) (struct file *, loff_t, int);
	ssize_t (*read) (struct file *, char __user *, size_t, loff_t *);
	ssize_t (*write) (struct file *, const char __user *, size_t, loff_t *);
	ssize_t (*read_iter) (struct kiocb *, struct iov_iter *);
	ssize_t (*write_iter) (struct kiocb *, struct iov_iter *);
	int (*iterate) (struct file *, struct dir_context *);
	int (*iterate_shared) (struct file *, struct dir_context *);
	__poll_t (*poll) (struct file *, struct poll_table_struct *);
	long (*unlocked_ioctl) (struct file *, unsigned int, unsigned long);
	long (*compat_ioctl) (struct file *, unsigned int, unsigned long);
	int (*mmap) (struct file *, struct vm_area_struct *);
	unsigned long mmap_supported_flags;
	int (*open) (struct inode *, struct file *);
	int (*flush) (struct file *, fl_owner_t id);
	int (*release) (struct inode *, struct file *);
	int (*fsync) (struct file *, loff_t, loff_t, int datasync);
	int (*fasync) (int, struct file *, int);
	int (*lock) (struct file *, int, struct file_lock *);
	ssize_t (*sendpage) (struct file *, struct page *, int, size_t, loff_t *, int);
	unsigned long (*get_unmapped_area)(struct file *, unsigned long, unsigned long, unsigned long, unsigned long);
	int (*check_flags)(int);
	int (*flock) (struct file *, int, struct file_lock *);
	ssize_t (*splice_write)(struct pipe_inode_info *, struct file *, loff_t *, size_t, unsigned int);
	ssize_t (*splice_read)(struct file *, loff_t *, struct pipe_inode_info *, size_t, unsigned int);
	int (*setlease)(struct file *, long, struct file_lock **, void **);
	long (*fallocate)(struct file *file, int mode, loff_t offset,
			  loff_t len);
	void (*show_fdinfo)(struct seq_file *m, struct file *f);
#ifndef CONFIG_MMU
	unsigned (*mmap_capabilities)(struct file *);
#endif
	ssize_t (*copy_file_range)(struct file *, loff_t, struct file *,
			loff_t, size_t, unsigned int);
	loff_t (*remap_file_range)(struct file *file_in, loff_t pos_in,
				   struct file *file_out, loff_t pos_out,
				   loff_t len, unsigned int remap_flags);
	int (*fadvise)(struct file *, loff_t, loff_t, int);
} __randomize_layout;
```

And our relevant function prototype is: 

```c
ssize_t (*read) (struct file *, char __user *, size_t, loff_t *);
```

Which was quite a waste of time as we could've been able to derive this from the first call to the `file->f_op->read` but that's fine since now we need to delve into the implementation of this on the file structures that we're working with. Eventually, we get to the point where we have to figure out what `__fget_light` does, as it has to retrieve the corresponding file structure for the stdout/stdin file-descriptors:

```c
static unsigned long __fget_light(unsigned int fd, fmode_t mask)
{
	struct files_struct *files = current->files;
	struct file *file;

	if (atomic_read(&files->count) == 1) {
		file = __fcheck_files(files, fd);
		if (!file || unlikely(file->f_mode & mask))
			return 0;
		return (unsigned long)file;
	} else {
		file = __fget(fd, mask);
		if (!file)
			return 0;
		return FDPUT_FPUT | (unsigned long)file;
	}
}
```

And the `__to_fd` function:

```c
static inline struct fd __to_fd(unsigned long v)
{
	return (struct fd){(struct file *)(v & ~3),v & 3};
}
```

Which is much simpler, it uses the GNU extension where you may unpack multiple literals into a structure, otherwise zeroing the excess out, the we take some file-descriptor `v`, mask out the 2 LSBs, and put it in a `struct fd`:

```c
struct fd {
	struct file *file;
	unsigned int flags;
};
```

I.e., the `flags` is the lower 2 bits of the file-descriptor, and the `struct file` is equivalent to the structure given above, but with:

```c
struct llist_node {
	struct llist_node *next;
};
```

Or:

```c
struct callback_head {
	struct callback_head *next;
	void (*func)(struct callback_head *head);
} __attribute__((aligned(sizeof(void *))));
#define rcu_head callback_head
```

Where the structure generated is `struct callback_head` such that the `next` element of both aggregate structures is going to be the file-descriptor with the 2 LSBs cleared, so in terms of `stdin` = 1, and `stdout` = 0, I see that this really doesn't matter since all we get is simply a `struct fd` structure whose `file->next` member is `0` in both cases except the `flags` for `stdin` will have a set lower-bit, and `stdout` will not.

The `current` macro returns the following:

```c
#define current	((struct task_struct *) ia64_getreg(_IA64_REG_TP))
```

Where `ia64_getreg` is another macro:

```c
#define ia64_getreg			IA64_INTRINSIC_MACRO(getreg)
```

And `IA64_INTRINSIC_MACRO` is _another_ macro:

```c
#define IA64_INTRINSIC_MACRO(name)	ia64_native_ ## name
```

Which gives us another fucking macro `ia64_native_getreg` which is defined twice because the Linux kernel source is heavily obfuscated, and in general programmed very well!!!

```
arch/ia64/include/uapi/asm/gcc_intrin.h, line 62 (as a macro)
arch/ia64/include/uapi/asm/intel_intrin.h, line 19 (as a macro)
```

In `intel_intrin.h` it is defined as `#define ia64_native_getreg	__getReg`, and in `gcc_intrin.h` it is defined as: 

```c
#define ia64_native_getreg(regnum)						\
({										\
	__u64 ia64_intri_res;							\
										\
	switch (regnum) {							\
	case _IA64_REG_GP:							\
		asm volatile ("mov %0=gp" : "=r"(ia64_intri_res));		\
		break;								\
	case _IA64_REG_IP:							\
		asm volatile ("mov %0=ip" : "=r"(ia64_intri_res));		\
		break;								\
	case _IA64_REG_PSR:							\
		asm volatile ("mov %0=psr" : "=r"(ia64_intri_res));		\
		break;								\
	case _IA64_REG_TP:	/* for current() */				\
		ia64_intri_res = ia64_r13;					\
		break;								\
	case _IA64_REG_AR_KR0 ... _IA64_REG_AR_EC:				\
		asm volatile ("mov %0=ar%1" : "=r" (ia64_intri_res)		\
				      : "i"(regnum - _IA64_REG_AR_KR0));	\
		break;								\
	case _IA64_REG_CR_DCR ... _IA64_REG_CR_LRR1:				\
		asm volatile ("mov %0=cr%1" : "=r" (ia64_intri_res)		\
				      : "i" (regnum - _IA64_REG_CR_DCR));	\
		break;								\
	case _IA64_REG_SP:							\
		asm volatile ("mov %0=sp" : "=r" (ia64_intri_res));		\
		break;								\
	default:								\
		ia64_bad_param_for_getreg();					\
		break;								\
	}									\
	ia64_intri_res;								\
})
```

So finally, the last macro that we care about getting is `__getReg`, it appears that it isn't defined anywhere!!! because fuck shit bitch ass etc., so we Google it further and discover that the manual for the `Intel C++ Compiler for Linux` has more information on what it does [here](http://www.ehu.eus/sgi/ARCHIVOS/c_ug_lnx.pdf) on page 350:

`Gets the value from a hardware register based on the index passed in. Produces a corresponding mov = r instruction. Provides access to the following registers: See Register Names for getReg() and setReg(). ` Where the registers are defined on page 353 as some odd variety of registers that I have barely studied, there appears to be no GPRs like `%rax`, or `%rbp` which I am familiar with, rather some other names like:

```
_IA64_REG_AR_RSC 
_IA64_REG_AR_BSP 
_IA64_REG_AR_BSPSTORE 
_IA64_REG_AR_RNAT 
_IA64_REG_AR_FCR 
_IA64_REG_AR_EFLAG 
_IA64_REG_AR_CSD 
_IA64_REG_AR_SSD 
_IA64_REG_AR_CFLAG 
_IA64_REG_AR_FSR 
_IA64_REG_AR_FIR 
_IA64_REG_AR_FDR 
_IA64_REG_AR_CCV 
_IA64_REG_AR_UNAT 
_IA64_REG_AR_FPSR 
_IA64_REG_AR_ITC 
_IA64_REG_AR_PFS 
_IA64_REG_AR_LC
_IA64_REG_AR_EC
```

Of which, I recognize the `EFLAG`; you may think I'm diving into the Linux internals a bit too far, by a long stretch, but I disagree as I believe it is quite educational in order to FULLY understand the return value of `read`:

http://linuxcommand.org/lc3_man_pages/readh.html

```
    Exit Status:
    The return code is zero, unless end-of-file is encountered, read times out,
    or an invalid file descriptor is supplied as the argument to -u.
```

Yeah, it returns zero if it errors, alright onto the rest of the decompilation:

```assembly
write(1, "Please enter your name: \0", 25)
if (!read(0, 0x402074, 32))
{
  _start_error ();
}
   0x0000000000401040 <+64>:    mov    %rax,%r14
   0x0000000000401043 <+67>:    add    $0x6,%r14
   0x0000000000401047 <+71>:    mov    0x402019,%rax
   0x000000000040104f <+79>:    mov    %rax,0x402094
   0x0000000000401057 <+87>:    mov    0x402074,%rax
   0x000000000040105f <+95>:    mov    %rax,0x40209a
   0x0000000000401067 <+103>:   mov    $0x1,%eax
   0x000000000040106c <+108>:   mov    $0x1,%edi
   0x0000000000401071 <+113>:   movabs $0x402094,%rsi
   0x000000000040107b <+123>:   mov    %r14,%rdx
   0x000000000040107e <+126>:   syscall
   0x0000000000401080 <+128>:   mov    $0x1,%eax
   0x0000000000401085 <+133>:   mov    $0x1,%edi
   0x000000000040108a <+138>:   movabs $0x402020,%rsi
   0x0000000000401094 <+148>:   mov    $0x16,%edx
   0x0000000000401099 <+153>:   syscall
   0x000000000040109b <+155>:   mov    $0x0,%eax
   0x00000000004010a0 <+160>:   mov    $0x0,%edi
   0x00000000004010a5 <+165>:   movabs $0x402074,%rsi
   0x00000000004010af <+175>:   mov    $0x20,%edx
   0x00000000004010b4 <+180>:   syscall
   0x00000000004010b6 <+182>:   mov    %rax,%r15
   0x00000000004010b9 <+185>:   dec    %r15
```

Starting with:

```assembly
   0x0000000000401040 <+64>:    mov    %rax,%r14
   0x0000000000401043 <+67>:    add    $0x6,%r14
   0x0000000000401047 <+71>:    mov    0x402019,%rax
   0x000000000040104f <+79>:    mov    %rax,0x402094
   0x0000000000401057 <+87>:    mov    0x402074,%rax
   0x000000000040105f <+95>:    mov    %rax,0x40209a
   0x0000000000401067 <+103>:   mov    $0x1,%eax
   0x000000000040106c <+108>:   mov    $0x1,%edi
   0x0000000000401071 <+113>:   movabs $0x402094,%rsi
   0x000000000040107b <+123>:   mov    %r14,%rdx
   0x000000000040107e <+126>:   syscall
```

`%rax` is 0, we add 6 to it, having `%r14` = 6, afterwards moving `%rax` into `%ds:0x402094` which was odd at first since the `ds` is implicit, so we place `0` into some location `0x402094`, thereafter moving `0x402074` into `*0x40209a`

TBF
