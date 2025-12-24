A non-insignificant quantity of branches across the decompilation appear dependent on two principal offsets into the `TEB->GdiTebBatch.Buffer`, at `+0x82` and `+0x106`. Comparisons against `qword`s supposedly stored at these offsets are performed against constant values, which appear to all share a similar numerical prefix--observe:

```c
if (gsbase->NtTib.Self->GdiTebBatch.Buffer[0x106].q == 0x2adeeacfe659f8ff)
if ( gsbase->NtTib.Self->GdiTebBatch.Buffer[0x82].q != 0x2adeefcf470df6ab)
```

These appear to be the only two values associated with these respective buffer positions. There appears to be no indication of where these two values are initialised, and educational resources are scarce on the TEB, let alone how to interpret these values.
Although, there is some semblance of hope in understanding [GDI batching](https://techshelps.github.io/MSDN/BUILDAPP/devdoc/live/pdapp/09high_69pv.htm): it is simply a way to store and execute a larger quantity of GDI commands, and this `GdiTebBatch.Buffer` stores these commands as `ULONG`s. However, in order for them to be processed by the system, the buffer must be flushed (through `GdiFlush`,) though this symbol does not seem to be transparently imported.

Heuristic analysis of these kinds of branches seems to determine that when the comparison (equality) evaluates false, i.e. `GdiTebBatch.Buffer[offs] != 0x...`, the proceeding branch is valid, otherwise it tends to exhibit nonsensical behaviour, but sometimes it may appear normal, as depicted below:

![[Pasted image 20251202141108.png]]

So, if we decide to believe that it is a guaranteed false evaluation, further backed by the fact that it never appears to be set explicitly in this binary database, and thus cannot become true at any point, then it would simply reduce to an opaque predicate. Otherwise, the way by which it is stored (assuming it is just hidden,) may reveal more about the state context of the program.
I believe it's unlikely that the latter is true, since it means that a lot of functions would depend on just two state variables (at both offsets in the buffer,) which would be exceedingly simple for how complex the application is; otherwise, they would have to be fundamental state variables that should be easy to infer from how they alter local function state.
It may be insightful to look into how GDI commands are structured, to perhaps gain insight into whether these two constants refer to concrete, recognised commands--although this is unlikely to prove meaningful.

![[Pasted image 20251203133218.png | center]]

Additionally, a similar opaque pattern is used on `glDispatchTable`, although this time it can be easily inferred that the compared values are invalid for the purpose of the table, as is described [here](https://www.geoffchappell.com/studies/windows/km/ntoskrnl/inc/api/pebteb/teb/index.htm):

> The `glDispatchTable` in version 3.51 is filled to capacity with pointers to functions [...]

And no instance of comparison lends itself to a valid function pointer, nor do we see any assignments into `glDispatchTable`, so we may assume all equality comparisons yield false.