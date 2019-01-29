---
layout: post
title: the amateur system v abi
---

In this post, for my own reference, I will explain and attempt to understand the concepts surveyed in the System V ABI for the AMD64 architecture maintained [here](https://github.com/hjl-tools/x86-psABI/wiki/X86-psABI). It is a document describing the conventions used for the Unix-like systems, i.e. defining certain data-types and their respective sizes, what registers are involved with what during function calls, defining the conventions taken by processes at initialization stages, etc.
In essence, it is the document you refer to whenever are confused about a certain subtlety about a program which is unrelated to the functionality itself, rather an intrinsic such as a stack alignment, or compiler optimization which seems ambiguous, although it is under good presumption of the ABI being followed.

The ABI, like many alike documents, is quite rigorous and thorough, laying out specific terms and definitions which are precise to their historic roots and generally strictly-followed in the conformant world of the operating system (typically)--and so, I will try to be as equivalently precise with my summarisations.

<h2> 3.1 <b>machine interface</b> </h2>

This chapter describes the concrete definitions for different currencies of measure in terms of primitive data-types, that is:

```
byte        =>   8 bits
twobyte     =>  16 bits
fourbyte    =>  32 bits
eightbyte   =>  64 bits
sixteenbyte => 128 bits
```

There is a reference made, which states that the Intel386 ABI (x86) defines an alternative:

```
halfword   => 16 bits
word       => 32 bits
doubleword => 64 bits
```

Stating that although this is said, most IA-32 documentation shifts the words down a bit into the following:

```
word            =>  16 bits
doubleword      =>  32 bits
quadword        =>  64 bits
double quadword => 128 bits
```

In the proceeding section `Fundamental Types`, the ABI defines the format for `__float128`, `long double`, `size_t`, the `NULL` pointer, `__int128` and booleans. `__float128` has a 15-bit exponent, and a 113-bit mantissa with an exponent bias of 16383. `long double` uses a 15-bit exponent, with a 64-bit mantissa and an explicit exponent bias (hence adding to 80-bits) of 16383. It is defined that the `long double` requires 16-bytes of storage, where the remainder 6-bytes are tail padding, although the `long double` itself can fit into 10-bytes, the contents of the padding is undefined.
The `NULL` pointer is defined as having the value 0, `__int128` is defined as being stored with little-endianness, `size_t` is defined as `unsigned long` for 64-bit environments and `unsigned int` for 32-bit environments (LP64 and ILP32). Booleans take up a byte in space, when in memory only the upper-bit is indicative of its truthiness, however when in a register any non-zero value is considered truthy.
Further on, the section describes that alignment is optional, and would only lead to slower data accesses, however in the cases of the types `__m128`, `__m256` and `__m512` the data must be aligned properly on a 16/32/64-byte boundary.

The next section describes the aspects of aggregate types, i.e. structures and unions, and defines that structures will take the alignment of their most strictly aligned member, and that each member will have the lowest available offset with the given alignment boundaries. It is said that the size of an object will also be a multiple of that object's alignment.
It is also noted that an array whose length exceeds 15 bytes, or is variably-lengthed, will have a 16-byte alignment, in the footnotes this is referenced to explain that it is to support the operation of SSE instructions over the array, and that the assumption that VLAs will most likely have a size over or equal to 16-bytes, therefore assuming a 16-byte alignment is logical.
Aggregate structures may require padding to meet to size and alignment standards, the contents of the padding is again undefined.

Moving onto bitfields ...

TBF
