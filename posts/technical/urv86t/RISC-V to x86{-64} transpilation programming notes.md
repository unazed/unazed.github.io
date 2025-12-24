# Architectural notes
- RV32/64I (*I* for base *integer* ISA) has 32 general purpose registers, not including `pc`, denoted as `x0` to `x31`. `x0` is a null-register which is always zeroed.
- RV32/64E (*E* for base integer *embedded* ISA) has half the count, at 16 GPRs.
- The different instruction formats are constructed somewhat-aligned to the R-type format; observe:

![[Pasted image 20251003220539.png | center]]

R-type contains fundamental fields which exist at their position in each subsequent format, unless replaced with an immediate specifier. The immediate specifiers (such as `imm[19:12]`) appear scrambled, but their indices correlate with similar indications in prior, i.e. J-type's `imm[10:1]` is contained within I-type's `imm[11:0]`, and similarly for other types except the U-type format, which represents the upper half of an immediate.
Keep in mind this is a hardware-level optimisation to minimise fan-out, as it preserves the ability to carry-through logic lines (?) across different formats since they share fields at the same positions. Same reasoning applied to the fundamental `rd`/`rs*`/etc. fields.
- `XLEN` refers to the integer register width (either 32 or 64 bits,) unrelated to word size, which is 32 bits regardless.
# Programming notes
- Emulation state should store a reference to GPRs with the consideration that there may be 16 or 32
- For making a generic instruction base `struct`, the only reasonably optimal solution is creating a union across the different formats, enabling access semantics as `insn.j.imm__19_12`. Separating the formats into different `struct`s may complicate type genericity further down the line.