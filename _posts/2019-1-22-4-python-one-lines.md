---
layout: post
title: python one liners (no semicolons)
---

Python, as you should know, is a versatile and flexible language, for this it suffers the well-debated repercussion of speed and performance. What goes on in this post is the complete inverse of performance-gaining, and should not be done at any point in your development, unless it is skid-quality code where you aren't expected to reach a certain bar of quality, then, by all means, go for it.

By most, it'd be considered entry-grade level obfuscation, by myself I'd consider it art; there is nothing quite like doing it proficiently, as it's a brain puzzles in most cases to even start thinking up ways of one-lining certain constructs. I would never (no pinky promises), and nor do I ever suggest that you should use this as obfuscation, unless, as mentioned before you don't expect anyone to really even open it up, let alone try and figure out what it does.
It is simply unstable, and for many of the methodologies you employ to make your coder harder to understand, there will still be trivial bypasses to circumvent your clever logic, as this is no different in reality from writing imperative code (as one-line programs are very majorly functional).

To begin, allow me to introduce the atoms of one-liners, that is, `globals()` and `locals()` (less `locals()` more `globals()` though), these are the dictionaries which dictate the variable namespaces of Python programs at, respectively, the `global` and `local` scopes (at the top-level and within functions), with these and the combined attributes of dictionaries such as `dict.__setitem__(k, v)` and `dict.__getitem__(k) -> v`, you can trivially understand the basis of a one-line program: a sequence of getter/setter calls, with arbitrary operations. And, to its core, that is the prime construct of one-lining, but your programs would be considered tasteless were they simply to be of this content.

Now, to sequence together these setter/getter calls we would prefer not to use semicolons (as that is not the topic), we would prefer to use something much more Pythonic (enough) and clean, something like lists and tuples; since you can group together calls in iterables. For example:

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

Of course we can condense this into one line by taking off the newlines proceeding the commas and last item, and it would still work. However for the case of this post I will continue using the prettified syntax as one-lines can grow exponentially complex.

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

This is an example of side-effects, note that putting this on one-line without changing anything except whitespace would be invalid no matter how, however the intent of this knowledge is to be applicable into concepts such as list comprehensions, for example:

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

Which will print the same results as the former code, except this form may be condensable into a one-line form. Note that I am not implying that for-loops are perfectly transformable into their one-line counterparts, as a counter-example would be as follows:

```py
for i in range(m, n):
  if i == j:
    break
  print(i)
```

How would you think, that you could implement this in one-line form (for any `m`, `n`, `i` and `j`)? Well, without using stdlib imports, here's how I'd do it:

```py
[print(i) for i in range(m, n) if i < j]
```

Easy, right? Now how would you implement this:

```py
for i in range(m, n):
  if i == j:
    print(i, j)
    break
  print(i)
```

A small change completely changes the resulting code, since in the first piece of code the fact it was simple was due to the fact that there was an empty terminating `if` clause, and due to this, there was no 'breaking procedure', unlike this code; therefore the only thing you had needed to do was simply check `i` against a condition, and not print it if it didn't meet a condition.
In this case, if it does meet the condition, you have to do something _and_ break the loop; here's how I'd do it:

```py
[
  (
    print(i, j),
    globals().__setitem__("_term", True)
  )
    if i == j else
  print(i)
  for i in (
    globals().__setitem__("_term", False),
    *range(m, n)
  )[1:]
  if not _term
]
```

Notice how I've increased my character count by nearly a factor of 5? It was due to the fact I had to implement the `_term` variable's initialization and the setting of it after `i == j`, although this is horrible to read, it is luckily the most general form of the for loop in this pattern:

```py
[
  (
    <breaking-clause>,
    globals().__setitem__("_term", True)
  )
    if <breaking-condition> else
  <continue>
  for <iterant> in (
    globals().__setitem__("_term", False),
    *<sequence>
  )
  if not _term
]
```

Equivalent to:

```py
for <iterant> in <sequence>:
  if <breaking-condition>:
    <breaking-clause>
    break
  <continue>
```

Although the for-loop has the `else` clause from itself, which is executed after the loop finishes normally, and can be implemented like this:

```py
(
  [
    (
      <breaking-clause>,
      globals().__setitem__("_term", True)
    )
      if <breaking-condition> else
    <continue>
    for <iterant> in (
      globals().__setitem__("_term", False),
      *<sequence>
    )
    if not _term
  ],
  <else-clause> if not _term else None
)
```

Equivalent to:

```py
for <iterant> in <sequence>:
  if <breaking-condition>:
    <breaking-clause>
    break
  <continue>
else:
  <else-clause>
```

Which is quite beautiful as it illustrates the for loop explicitly, using for loops and simple conditions (somewhat).

Moving onto `while` loops, this construct is equally as beautiful as it can be applied in many of the same ways as a for loop can be. Effectively, any construct can imitate any other construct with the given of `globals().__setitem__` and `globals().__getitem__` if you tried hard enough. Take an example of a while-loop here:

```py
variable = 5
while variable < 100:
  variable += variable ** .5
  print(f"variable={variable:.2f}")
```

A simple example, translated to:

```py
while (
  globals().__setitem__("variable", 5)
    if globals().get("variable", None) is None else
  globals().__setitem__("variable", variable + variable ** .5),
  print(f"variable={variable:.2f}"),
  variable < 100
)[-1]: pass
```

As tempted as someone may be to put the `print` outwith the while-conditional itself, it is _not_ the same as the former code given as it would run an iteration behind, although it is arguably more beautiful than having the `print` inside. The general structure that I define for any while-loop of the form:

```py
<pre-loop>
while <condition>:
  <while-clause>
```

Is generally convertible to:

```py
while (
  <pre-loop>,
  <condition>
)[-1]: pass
```

Now, an important note, is that occasionally you may use the while-clause itself to run code, and it is completely fine and I suggest doing so whenever possible because it is both beautiful and paradigmatic of one-lining; a simple `pass` seems slightly cheaty, rather you can also substitute it for such:

```py
while (
  globals().__setitem__("variable", 5)
    if globals().get("variable", None) is None else
  None,
  print(f"variable={variable:.2f}"),
  variable < 100
)[-1]: variable += variable ** .5
```

Or:

```py
while (
  [*(
    (
      globals().__setitem__("_variable", _variable + _variable ** .5),
      print(f"variable={_variable:.2f}"),
      _variable < 100
    ) for _ in range(1)
  )][0][-1]
    if globals().get("variable", None) is not None else
  (
    globals().__setitem__("_variable", 5),
    True
  )[1]
): variable = 5
```

The last one is a slight joke, although I do recommend that you try to understand why it works, but I'm simply alternating between what is in the while-clause, from `pass` to `variable += variable ** .5` to `variable = 5`, you may theoretically put anything there.

Now imagine while-loops with side-effects, although in actuality the previous two while loops both have side-effects and are impure, they're much more subtle, and I'd like to give an explicit example of a while loop with side effects:

```py
while (
    globals().__setitem__("n", globals().get("n", 1)),
    globals().__setitem__("n", n + 50),
    n < 100
  )[-1]:
  print(n) 
```

To amateurly prove that this has side-effects, run it through the Python interpreter twice, each time recording the `n` value, and seeing if it changes. If it does, it's impure, otherwise it's pure (unless it's based on a random probability). Moving onto making one-line while-loops, I'd like for the reader to recall to their C experiences (if any), and especially the fact that `while (1) {}` is equivalent to `for (;;) {}`, that is, a for-loop with no iterant, disposition nor condition.

```py
for:
  <for-clause>
```

There's no real good way to imitate while-loops as a take on for-loops in pure Python without using stdlib like in `itertools`, which is completely fine in one-lining, however pure Python is always good. Recursion will not get you far really, not further than the recursion limit on your system. Use `itertools.cycle` for infinite sequences of cycling data.

Exception handling is a bitch, here's an example of it from a socket-library that I made on my `python-one-liners` repository:

```py
(
  "receive_all",
  lambda self, ssize=4192, signal_timeout=2, _buffer=b"":
  (
    globals().__setitem__('_timeout',
      lambda time_, f, *args, **kwargs: (
        globals().__setitem__("signal", __import__("signal")),
        signal.signal(signal.SIGALRM, lambda _, frame: 0/0),
        signal.alarm(signal_timeout),
        f(*args, **kwargs),
        signal.alarm(0)
      )
    ),
    setvar(
      "_inner_receive_all",
      lambda self, ssize=4192, _buffer=b"": (
        exec(
          "def _autistic_receive_all(self, ssize=4192, _buffer=b''):\n\t"
            "try:"
              "return [_autistic_receive_all(self, ssize, _buffer+data) if data else _buffer for data in [self.socket.recv(ssize)]][0]\n\t"
            "except:"
              "return _buffer\n"
          "globals()['_autistic_receive_all'] = _autistic_receive_all"
        ),
        _autistic_receive_all
      )[1]
    ),
    _timeout(signal_timeout, _inner_receive_all(self), self, ssize)
  )
)
```

There is no other way (that I know of) to do it besides using `exec`. The most interesting thing there is the actual method I used for implementing a 'receive-all-data' method for a socket, using the UNIX signals and causing a `ZeroDivisionError` upon a certain timeout, hereafter unhanging the `self.socket.recv(ssize)` and returning back to the caller by the `return _buffer` which is quite genius if I say so for myself.

Lambdas are, in eyes of one-lining, simply a generalized sequence of array items (i.e. due to the parameters), with a return value. I use them to simplify certain pieces of code, such as above, the `setvar`, `_inner_receive_all` and `_timeout` which would be impossible to do without in that certain code.
You can technically use the `def` notation, but you wouldn't be able to use it to access any more than a regular `lambda` definition could.
Imports are achieved by `__import__`, classes are also one-lineable by using `type(<name>, <bases>, <var-dict>)` or `import types` and `types.ClassType` with the same parameters.

One-line etiquette is as follows:

- Don't use semicolons.
- Only use `exec` for exception-handling.
- If you're using it for obfuscation, the last thing that should be obfuscating it is the syntax, obfuscation comes from within the one-line's nature, if it doesn't, you aren't doing it well enough.
- Nobody likes boring code, encapsulate the stdlib, while/for-loops, lambdas, classes, multi-dimensional iteration, impure functionality, obscure control flow, anything and everything that isn't against one-line etiquette.
- Sneak in an `__import__("this")` somewhere inside the code, for purposes of irony.

Thanks for reading.
