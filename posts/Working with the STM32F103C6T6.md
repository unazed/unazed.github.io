---
title: Working with the STM32F103C6T6
author: Mindaugas Taujanskas
abstract:
---
## Motivation

Getting into embedded systems has always seemed a daunting task for myself, even after so many years of relatively low-level development and reverse engineering on Intel x86/x64 platforms. I decided to start with purchasing four STM32 microcomputer units (MCU) for a fairly inexpensive price, just under the assumption that I may break something more than once.

I've had very little experience working with ARM-based systems, so to begin my task of constructing, debugging, and extending an elementary firmware (whose functionality I haven't even really ascertained yet,) it feels as a shot in the deep dark to undertake this exercise. Nonetheless, like many other untethered ambitions I've pursued, I will try my best to achieve something of value, especially as this project exposes the veil between electronics and system development that I have wanted to pierce early into my hobbyist career.

## Why this particular MCU?

Initially: no reason.

The STM32F10x series start from low-power cost-effective, and range up to devices which support more components and bandwidth in terms of flash and memory. In the case of my MCU, the difference between the STM32F103Cxxx variants appears to be increasing flash/memory capacity.
Even the lowest end MCU in this family would be fine. To the benefit of, and for the purpose of learning, an increasingly constrained environment is ideal for learning how to optimise and manage resources.
## Where do I even start?

Aside from purchasing the relevant goodies (an ST-Link to interface with the MCU,) the first step was understanding what I would even need to begin actualising my code from thought into fruition. Usually, I'd download the native GCC toolchain (with MSYS32 on Windows), install a text editor, create my folder structure, a `main` file outputting "Hello, world!" to the user, a `Makefile` to organise the compilation, and be happy.
Unfortunately, and as one would expect, only one of these steps is adjacent to the embedded-equivalent--that being which you may still install any text editor of your choosing.

My conception of the workflow was initially:

1. Develop your primary source files
2. Cross-compile the sources for ARM (Cortex-M3 in the case of STM32F1xx)
3. Link it against a linker-file which places it appropriately according to the MCU's memory mapping
4. Flash it using whichever tools the ST-Link provides
5. If necessary, debug it with the ST-Link--or preferably the toolchain's GDB via remote connection

So far, it seems to be fairly accurate disregarding some pedantic details. Cross-compilation is performed through `arm-none-eabi-gcc`, whose architecture is specified by the `CFLAGS` as `-mcpu=cortex-m3`. The linking stage can be utterly simplified to simply indicating where the flash and memory sections are located and their lengths, and then subsequently placing the typical `.text`, `.data` and `.bss` sections, with the special addition of placing an interrupt service routine table (ISR) at the root of the flash storage, and also indicating where the `.stack` starts.

```
ENTRY(vector_table)

MEMORY
{
  FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 32K
  RAM   (rwx): ORIGIN = 0x20000000, LENGTH = 10K
}

SECTIONS
{
  .isr_vector : {
    KEEP(*(.isr_vector))
  } > FLASH

  .text : {
    *(.text*)
    *(.rodata*)
  } > FLASH

  .data : {
    *(.data*)
  } > RAM AT > FLASH

  .bss : {
    *(.bss*)
    *(COMMON)
  } > RAM

  .stack : {
    *(.stack)
  } > RAM
}
```
## Interim note regarding resources

- The reference manual: [RM0008](https://www.st.com/resource/en/reference_manual/rm0008-stm32f101xx-stm32f102xx-stm32f103xx-stm32f105xx-and-stm32f107xx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf). Priceless in understanding essentially everything about the operation and layout of the MCU.
- The programming manual: [PM0056](https://www.st.com/resource/en/programming_manual/pm0056-stm32f10xxx20xxx21xxxl1xxxx-cortexm3-programming-manual-stmicroelectronics.pdf). Extensive information on the instruction set, essentially just the ARM Cortex-M3 programming manual, but likely with relevant considerations for the specific MCU.
- The application notes: [AN2606](https://www.st.com/resource/en/application_note/an2606-introduction-to-system-memory-boot-mode-on-stm32-mcus-stmicroelectronics.pdf). Relevant to understanding how to configure your MCU to select between the (typically?) pre-installed bootloader stored in read-only memory, and yours stored at `0x0800_000`. My MCU notably came with a shunt across both `BOOT0` and `BOOT1` pins to `GND`, which means that it will begin executing from the flash root by default, this may be different from other suppliers.
- The [AAPCS](https://web.eecs.umich.edu/~prabal/teaching/resources/eecs373/ARM-AAPCS-EABI-v2.08.pdf): supplementary documentation and reading to further understand how the ARM architecture expects things to be done. Elaborates on calling conventions, broader code/data alignment constraints, etc.
- The [preliminary datasheet](https://www.alldatasheet.com/datasheet-pdf/download/201595/STMICROELECTRONICS/STM32F103C6T6.html): semi-important to understand what operating conditions your MCU will work under, and its lifespan. Section (5.3.9) (Table 24) indicates the minimum endurance cycles before flash memory faults may occur, though given at extremal conditions.

## What does anything in that linker script mean?

I've never actually gone out of my way to learn linker-script, since I've only ever had to read it, and it's fairly self-explanatory when read, but seems to get endlessly complex as constraints grow. I had a few questions when reading the file:

1. Does the `>` in the `<section> : { ... } > <region>` grammar mean to append that section ahead of any previous sections? Are there any implicit alignment constraints? If no to the former question, can the linker reorder sections as it sees fit?
2. Is the `<section>` token just the identifier for the group of sections expounded immediately after, could I just do `.blah-blah { *(.text*) } > FLASH`, and have it be equivalent?
3. Why is `.isr_vector` notated with `KEEP`, but `.stack` isn't?
4. What is `COMMON`? Is this a linker-defined constant for compiler-specific sections that might exist, like for DWARF or such?
5. What does `.data { ... } > RAM AT > FLASH` mean? Are we copying the data section between both RAM and flash? If so, why?
6. Does the `ENTRY(vector_table)` really matter--won't the MCU begin executing at `0x0800_0000` regardless?

And then, subsequent research to answer these questions:

1. It's apparently not technically *appending*, but more-so just indicating which section belongs to which memory-region, although the linker will respect the precedence of sections as they appear in the script. Implicit alignments are known by the cross-compiler, as they are typically set out by the AAPCS, however specific alignments for DMA will likely have to be explicitly annotated.
2. I had a crucial misunderstanding of the syntax's purpose. The first `.text` indicates the resultant section from which all object files will collate their sections into, if they happen to have sections that match the proceeding `.text*` wildcard. The first asterisk in `*(.text*)` simply means to consider *all* object files, whereas `test.o(.text)` would only look at `test.o`.
   Furthermore, wildcards on these filenames are not supported as they are with section names.
3. In the current context, we need to `KEEP` `.isr_vector` because, although it may have no references at link-time (it is typically just referred to by hardware when an interrupt occurs), we do not want it to be pruned or altered in any way whatsoever, as it would simply cause undefined behaviour.
   `.stack` is a more peculiar case, since it doesn't necessarily need to be defined as a section, as it simply refers to an address in RAM, and it is made known to the processor by virtue of being the first entry in the ISR, and thus given that the address is properly aligned, all further operations on `sp` will perform as expected.
   However, I feel as though the `_estack` (and `_sstack`) symbols are missing, which would simply help make the definition globally available to the program, instead of requiring a header-definition.
4. `COMMON` is apparently a relic of practice long-gone. In essence, it seems to just be a `.bss` per-file equivalent, which is then collected into the resultant `.bss` section. It seems to just exist for the sole purpose of enabling legacy behaviour, where variable definitions lacking `extern` can still be resolved to an external symbol, as they're resolved through looking at each object file's `COMMON` sections (?)
5. This syntax is abhorrently confusing at first, but it essentially just means `VMA <-loaded- LMA`, where VMA and LMA mean virtual/loaded memory address.
   This mindset felt a little tricky for me to get out of, but remember when you flash your program, it is permanent, and flash memory will retain it indefinitely, but RAM will not. *However*, because flash is expensive to read from/write to, you should act as if it's read-only (further togglable by R/W protections on the chip,) and so, what if you have global variables that you want to always keep, but also have the capability to change? You need to store their static initialised value in flash (the LMA), and then copy it to RAM (the VMA) each time you reset the MCU.
   So, the statement is telling the linker that the variable will be initialised (if it has a value) in flash, and then will be copied by the entry routine (or at least any time before it's accessed) to RAM, and so any time a translation unit refers to the variable, ensure the VMA is used.
6. `ENTRY` doesn't appear to have any consequence on how the resultant binary is generated by the `objcopy`, as the "loading" stage is handled by the MCU, and it may be omitted.

Furthermore, the permissions indicated on memory regions seem to just be cosmetic, although they may prevent certain (obscure?) link-time issues, and obviously increase semantic clarity to the reader.

## Why do we even load at 0x0800_0000?

I found it a little disorienting trying to understand the STM32 memory map and boot configuration, solely because it states two different things across two different manuals, namely from the PM0056:

	On system reset, the vector table is fixed at address 0x0000 0000.
	Privileged software can write to the VTOR to relocate the vector table start 
	address to a different memory location, in the range 0x0000 0080 to 0x3FFF FF80

And then the RM0008 further states:

	[...] the main Flash memory is aliased in the boot memory space (0x0000 0000), 
	but still accessible from its original memory space (0x800 0000). In other 
	words, the Flash memory contents can be accessed starting from address
	0x0000 0000 or 0x800 0000

This was confusing to begin with, and seemed like unneeded complexity, but the reason appears to stem from the fact that the MCU specifically has multiple boot modes, whose bootloaders must reside in different areas of memory (either SRAM or flash;) and so, the processor needs a way to alias two different memory addresses to a single one.
Once the processor loads the reset handler at `0x0000 0004`, aliased to either `0x2000 0004` or `0x0800 0004` the handler will then continue to work in their respective memory regions.

## Okay, how do we prepare the processor in our code?

The linker does a lot of the simpler grunt-work of ensuring static data will be where it needs to be in flash in order to be processed by the MCU, we just need to ensure that we follow up on our promises which we made to the linker; i.e., zero-initialising the `.bss` section, and copying over the `.data` section into SRAM.
We must do this in the reset handler, since this is essentially the equivalent of Linux's `_start`, where we have nothing but a blank-slate of a CRT yet to initialise:

```c
#include <stdint-gcc.h>

extern uint32_t _sdata, _edata, _sidata;
extern uint32_t _szero, _ezero;
extern uint32_t _estack;

__attribute__((noreturn))
void isr_reset_handler (void);

_Bool isr_reset_completed = 0;

__attribute__(( section(".isr_vector") ))
const uint32_t isr_vector[] = {
  (uint32_t)&_estack,
  (uint32_t)isr_reset_handler
};

void
isr_reset_handler (void)
{
  uint32_t *lma_sdata = &_sidata,
           *vma_sdata = &_sdata;

  while (vma_sdata < &_edata)
    *vma_sdata++ = *lma_sdata++;

  for (uint32_t* szero = &_szero; szero < &_ezero; ++szero)
    *szero = 0;

  isr_reset_completed = 1;

  while (1);
}
```

Note that the linker script was mildly revised to more verbosely comply with alignments, and to export section demarcation symbols. Further note the `_sidata` symbol which confused me initially when I was wondering if the `_sdata`/`_edata` symbols for the section we want to relocate to SRAM referred to the VMA or LMA addresses. They refer to the former, and so one needs to add an additional `_sidata = LOADADDR(.data);` in order to grab the LMA.

I added the `isr_reset_completed` global to verify that the `.data` section was appropriately relocated, to which GDB proved me wrong:

```c
isr_reset_handler () at src/handler.c:17
17        while (vma_sdata < &_edata)
(gdb) c
Continuing.
Program received signal SIGINT, Interrupt.
isr_reset_handler () at src/handler.c:25
25        while (1);
(gdb) printf "%d\n", isr_reset_completed
1
(gdb) printf ".data: %x -> %x\n", &_sdata, &_edata
.data: 20000000 -> 20000000
(gdb) printf ".bss: %x -> %x\n", &_szero, &_ezero
.bss: 20000000 -> 20000004
```

Woops, since I zero-initialised it, the linker automatically placed it in `.bss`. Changing it to a `uint8_t` and setting the default value to anything but 0 does however demonstrate that the linker places it in `.data` as we would expect.

So far, we've prepared the simplest part of the processor, however, I want my MCU to write something nice and kind to me.

## Receiving messages from the MCU

So, there were two ways in which I was considering implementing this:

1. Universal synchronous/asynchronous receiver/transmitter (USART)
2. Semi-hosting

My idea of USART is that it's essentially just a communication bridge between the MCU and any peripheral which supports the protocol.
All MCUs in the STM32F103xx family support USART, but they would likely require a physical serial interface across the appropriate pins, of which, there are three potential interfaces (`USART1` to `USART3`.) This can be achieved by soldering the GPIO header onto the MCU, connecting a USB-to-TTL adapter (like [this](https://www.aliexpress.com/item/1005003536455256.html)), and then configuring the COM driver host-side to display data.

At the moment, this isn't an option while the adapter ships from mainland China, so the simplest route is option (2): semi-hosting. This is more generally applicable to any ARM targets(?), and it involves passing-through system calls from the target to host through debugging breakpoints (or the `SVC` supervisor call instruction), which is recognised by OpenOCD, and then appropriately handled host-side; returning the result into the correct register once the system call is completed.

I've simply created a separate `io.c/h` file-pair, and defined the `trace_print` function:

```c
#include <stdio.h>

#ifdef ARM_SEMIHOSTED
  extern void initialise_monitor_handles (void);
#endif

void io_init (void);
int trace_print (const char* const s);

int
trace_print (const char* const s)
{
#ifdef ARM_SEMIHOSTED
  return puts (s);
#else
  int len = 0;
  for (; s[len]; ++len);
  return len;
#endif
}

void
io_init (void)
{
#ifdef ARM_SEMIHOSTED
  initialise_monitor_handles ();
#endif
}
```

`initialise_monitor_handles` is provided by the `rdimon` library, which must be linked against, as well as removing `-nostartfiles` so that we can link against the CRT with `-lc`.
Then, we can add a new `Makefile` rule:

```
debug: build/firmware.elf
  openocd -f interface/stlink.cfg -f target/stm32f1x.cfg \
    -c "init" \
    -c "reset halt" \
    -c "arm semihosting enable" \
    -c "resume"
```

And so, we have semi-hosting configured. Let us introduce the MCU to our host:

```c
void
isr_reset_handler (void)
{
  uint32_t *lma_sdata = &_sidata,
           *vma_sdata = &_sdata;

  while (vma_sdata < &_edata)
    *vma_sdata++ = *lma_sdata++;

  for (uint32_t* szero = &_szero; szero < &_ezero; ++szero)
    *szero = 0;

  io_init ();
  main ();

  while (1);
}

void
main (void)
{
  trace_print ("hello from the stm32 :)");
}
```

Running `make debug` after `make flash`:

```
$ make debug
/c/msys64/mingw64/bin/openocd -f interface/stlink.cfg -f target/stm32f1x.cfg \
  -c "init" \
  -c "reset halt" \
  -c "arm semihosting enable" \
  -c "resume"
Open On-Chip Debugger 0.12.0 (2025-06-13) [https://github.com/sysprogs/openocd]
...
[stm32f1x.cpu] halted due to breakpoint, current mode: Thread
xPSR: 0x01000000 pc: 0x08001a0c msp: 0x20000fb8
semihosting is enabled
Info : Listening on port 6666 for tcl connections
Info : Listening on port 4444 for telnet connections
hello from the stm32 :)
```

Voila: our first embedded hello world.

Note that semi-hosting is apparently uncommon to use for debugging, primarily due to the performance loss, which makes sense. I felt the consequences when I tried to use `printf` with a format specifier, and suddenly `objcopy` failed because trying to populate the `.data` section caused the `FLASH` memory region to exceed its 32KB size.
Obviously, there are bound to be space-efficient solutions, whether in terms of a leaner standard library, or by writing thin interfaces over the `SYS_WRITE` system call.

Ideally, I hope to write my own driver for the USB-TTL adapter, so that I can gain experience in dealing with peripheral state.

## Triggering software interrupts

So, looking through the vector table in the reference manual, what I was interested in is creating software interrupts (SWI) so I can get a taste of how IRQ handlers are executed and return. The most important register here is the `EXTI` (from the external interrupt/event controller), and specifically `EXTI.SWIER` (software-interrupt event register,) which is a 20-bit field (masked by `EXTI.IMR`) that allows you to trigger interrupts, which must then be correspondingly cleared in `EXTI.PR` by the IRQ handler.
What was weird was that there's neither a catch-all IRQ dispatcher, nor just a per-line IRQ handler for these SWIs--there's a mix of both:

- `+0x58 EXTI0` to `+0x68 EXTI4` map five individual lines
- `+0x9C EXTI9_5` and `+0xE0 EXTI15_10` map the next five lines into a grouped IRQ handler

And there's no mapping for the remaining 4 lines (the 20th bit has reserved functionality,) so we can only register 16 IRQ handlers.

Anyways, for a proof of concept, we can just unmask the first bit in the IMR, set it high in the SWIER and register our `EXTI0` IRQ handler, right?
Apparently not--we also have to enable IRQ in the nested vectored interrupt controller (NVIC).

### Quick aside on representing some of the structures in C

The ARM specification system structure groupings are slightly contrary to how the CMSIS header implements them. My primary gripe was with understanding why, for example, `SCB.ACTLR` was spaced so far behind the next field `SCB.CPUID`, but then `ICTR`, which is listed under the technical reference manual as a field of the NVIC, is adjacent to `ACTLR`, which itself has nothing to do with the NVIC.
There's likely a decent explanation from the hardware perspective, but reading the [CMSIS](https://github.com/ARM-software/CMSIS_5/blob/develop/CMSIS/Core/Include/core_cm3.h) implementation indicates that they separate those two registers entirely into a structure called `SCnSCB` (System Controls not in the System Control Block.)

## Enabling SWIs in the NVIC

Moving forward, we need to modify the correct NVIC interrupt set-enable registers (ISER) in order to enable the corresponding interrupt. There are 8 ISERs, each mapping 32 interrupts, although our device only supports up to 60. The `EXTI0` line has interrupt position 6, so we're looking to toggle bit 6 of `ISER[0]`.
Then, we want to tell the processor to process any interrupts on line 0 by unmasking it in the `IMR`, and then finally queue the event by setting the respective line bit in `SWIER`:

```c
volatile uint8_t irq_called = 0;
  
DEFN_ISR_ROUTINE(isr_irq_exti0)
{
  trace_print ("we're in the EXTI0 IRQ routine!");
  irq_called = 1;
  REG_EXTI->pr |= 1 << 0;
}

DEFN_ISR_ROUTINE(isr_reset)
{
  ...
  main ();

  while (1)
  {
    if (irq_called)
    {
      trace_print ("we returned to isr_reset!");
      irq_called = 0;
    }
  }
}

void
main (void)
{
  trace_print ("enabling interrupts");
  asm volatile ( "cpsie i" );

  trace_print ("configuring ISER, IMR and SWIER");
  REG_NVIC->iser[0] |= 1 << 6;
  REG_EXTI->imr |= 1 << 0;

  trace_print ("SWI should trigger soon")
  REG_EXTI->swier |= 1 << 0;
}
```

And tada! It seems to have worked as expected. The code appears to run with or without the `cpsie i`, since interrupts are enabled by default, but naturally it will not function without them enabled.

Initially nothing I tried worked; I went through a large deal of trouble scouring over the ARM specification, relating it to the STM32 manual, and diagnosing why the interrupt handler didn't seem to get called no matter what--and although the solution was trivial, it reminded me of the horror of having to work in an environment where nobody nor nothing will tell you that you messed something up, and will just remain silently broken (I wrote the wrong NVIC address.)

For better or for worse, here are some vital reference addresses for the STM32F103xx low-density family of MCUs:

```c
#define BND_BASE_EXTI   (0x40010400)
#define BND_BASE_SCB    (0xE000ED00)
#define BND_BASE_SCnSCB (0xE000E000)
#define BND_BASE_NVIC   (0xE000E100)
#define BND_BASE_RCC    (0x40021000)
#define BND_BASE_AFIO   (0x40010000)
```

## What about system calls?

They're simpler in principle, since they're just handled by the processor without need for any configuration, aside from needing a system call handler to function. The `SVC #imm` instruction causes an exception, which stores the state onto stack and execution is transferred to the handler.

After an hour or so of mindless and both shameless copying since I don't have a good grasp on ARM assembly, I've inevitably come to the age old conclusion that it's never as simple as it ever seems. Since the processor just pushes the context information onto the stack, you need to recover the instruction pointer and grab the system call number from the instruction, which is fairly trivial since apparently ARM Thumb mode doesn't have that complicated instruction encoding, but one quickly comes to the conclusion it's better off writing the function in inline assembly, because otherwise you need to rely on the compiler not generating its own stack-frame and muddling your offsets.

```c
__attribute__(( naked ))
DEFN_ISR_ROUTINE(isr_svc_call)
{
    asm volatile
    (
      "tst lr, #4\n"
      "ite eq\n"
      "mrseq r0, msp\n"
      "mrsne r0, psp\n"
  
      "ldr r1, [r0, #24]\n"
      "ldrh r2, [r1, #-2]\n"
      "and r1, r2, #0xFF\n"
  
      "push {lr}\n"
      "mov r2, r0\n"
      "mov r0, r1\n"
      "mov r1, r2\n"
      "bl isr_fwd_svc_call\n"
      "pop {lr}\n"
  
      "bx lr\n"
      ::: "memory"
    );
}
```

There are four main stages of the assembly:

1. Test to see if we're using the main system stack or a specific program stack: choose the correct one to forward
2. Retrieve the instruction pointer and extract the immediate byte
3. Save our link-register, prepare and  pass the two parameters `(uin8_t svc_number, void* stack_frame)` to pass into `isr_fwd_svc_call`
4. Restore state, and tell the processor we're done, so that it can do its magic to get us back to the normal flow of execution

Upon observing `lr`, it seems to be a negative signed value `0xfffffff9` which upon researching is identified as `EXC_RETURN`, which tells the processor to perform a set of special operations instead of just outright placing execution back to `lr`, i.e. restoring the context from stack and using the stored `lr`.

And so, we can begin creating our own implementation of system calls which opens innumerable doors into how we can separate user-space from privileged-space, implement I/O, memory management, all the boring sounding stuff.

## What's next?

In my former years I'd always enjoyed the idea of writing a fully integrated bootloader/kernel/user-space, but the idea doesn't quite ring out to me when working with MCUs, since they're a more ideal, standardised environment which doesn't feel like it would contribute to the crux of what OS development envelopes.
On the other hand, and as unbelievable as it seems, I haven't even begun touching upon the complicated parts of embedded development. Experiencing the unique debugging experience and problems that come with working in a constrained environment is what sparks the joy in embedded development for myself. However, reading complex datasheets, reference manuals, and being limited by my physical access to components is certainly a unique experience which feels much more industrious than any issue I've had in software development.