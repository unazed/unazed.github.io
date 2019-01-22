---
layout: post
title: python one liners (without semicolons)
---

Python, as you should know, is a versatile and flexible language, for this it suffers the well-debated repercussion of speed and performance. What goes on in this post is the complete inverse of performance-gaining, and should not be done at any point in your development, unless it is skid-quality code where you aren't expected to reach a certain bar of quality, then, by all means, go for it.

By most, it'd be considered entry-grade level obfuscation, by myself I'd consider it art; there is nothing quite like doing it proficiently, as it's a brain puzzles in most cases to even start thinking up ways of one-lining certain constructs. I would never (no pinky promises), and nor do I ever suggest that you should use this as obfuscation, unless, as mentioned before you don't expect anyone to really even open it up, let alone try and figure out what it does in reality.
It is simply unstable, and many of the methodologies you employ to make your coder harder to understand, there will still be trivial bypasses to circumvent your clever logic, as this is no different in reality from writing imperative code (as one-line programs are very majorly functional).

To begin, allow me to introduce the atoms of one-liners, that is, `globals()` and `locals()` (less `locals()` more `globals()` though), these are the dictionaries which dictate the variable namespaces of Python programs at, respectively, the `global` and `local` scopes (at the top-level and within functions), with these and the combined attributes of dictionaries such as `dict.__setitem__(k, v)` and `dict.__getitem__(k) -> v`, you can trivially understand the basis of a one-line program: a sequence of getter/setter calls, with arbitrary operations. And, to its core, that is the prime construct of one-lining, but your programs would be considered tasteless were they simply to be of this content.

Now, to sequence together these setter/getter calls we would prefer not to use semicolons (as that is not the topic), we would prefer to use something much more Pythonic (enough) and clean (and usable), something like lists and tuples; since you can group together calls in iterables like these. For example:

```py
print([
  globals().__setitem__("a", 1),
  print(a + 1),
  globals().__getitem__("a")
][2] + 1)
```

Which simply: creates a global `a` initialized to 1, prints it, retrieves it and stores it in the 3rd index of the list. As Python evaluates everything inside-out we can make the assumption all of these calls will have a certain value upon reaching the encapsulating `print([...][2] + 1)`, obviously we can see that this would print `2` twice, which we may test:

```py
>>> print([
...   globals().__setitem__("a", 1),
...   print(a + 1),
...   globals().__getitem__("a")
... ][2] + 1)
2
2
```

Of course we can condense this into one line by taking off the newlines proceeding the commas and last item, and it would still obviously work. However for the case of this post I will continue using the prettified syntax as one-lines can grow exponentially complex.

Other important keywords include all of the general control-flow syntax, e.g.: `for`, `while`, `if`, `elif`, etc., it is important to realize that keywords that are generally used in ternary notation, or in embedded notation do not have to necessarily do so in order to achieve a functional one-line, take the example:

```py
for val in (
    globals().__setitem__("a", 1),
    globals().__getitem__("a"),
    globals().__setitem__("a", a + 1),
    globals().__getitem__("a")
  ):
  print(val)
```

What do you think this'd print? Take a second to follow the execution flow of the program. On the first iteration, we would get `None`, on the second, we'd get 1 due to the prior, on the third we'd get `None`, and then on the final iteration we would finally get a 2. Doesn't this goes besides the inside-out logic of the `print` that we'd seen previously?
Well, if you think about it, you'd arrive at a no (probably). The reason is, that everything _is_ evaluated, the difference between the individual `print` statement in the first example is that it was a constant-time operation which required no real logical thinking to figure out, whereas with for-loops you need to remember that everything is evaluated and everything is sequential.
By sequential I mean that, `globals().__setitem__("a", 1)` will, at that moment, set `a` to 1, afterwards the `globals().__getitem__("a")` will retrieve the value of `a` at that point, and so on, this loop is completely pure as well, that is, if you reran it multiple times it would not give you any other result other than `None`, 1, `None`, and 2. The effect of this purity is that you can deduce the full execution and result of the for-loop by simply looking at it and nothing other than itself, as we initialize `a` to 1 in the first line.

Iteration with side-effects is the more complex side of one-lining with iteration, unlike pure iteration, if the certain iteration is repeated via other iteration, it will have a different value, this is a very powerful idea in one-lining, take an example:

```py
for _ in range(2):
  for n in (
      globals().__setitem__("a",
        globals().get("k", 1)
      ),
      globals().__setitem__("k", 2),
      globals().__getitem__("a"),
      globals().__getitem__("k")
    ):
    print(n)
```

This is a trivial example of side-effects, note that putting this on one-line without changing anything except whitespace would be invalid no matter how, however the intent of this knowledge is to be applicable into concepts such as list comprehensions, for example:

```py
[
  [
    print(n)
    for n in (
        globals().__setitem__("a",
          globals().get("k", 1)
        ),
        globals().__setitem__("k", 2),
        globals().__getitem__("a"),
        globals().__getitem__("k")
      )
  ]
  for _ in range(2)
]
```

Which will print the same results as the former code, except this form may be condensable into a one-line form.

TBF
