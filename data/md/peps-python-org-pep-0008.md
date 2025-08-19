One of Guido’s key insights is that code is read much more often than
it is written. The guidelines provided here are intended to improve
the readability of code and make it consistent across the wide
spectrum of Python code. As [PEP 20](../pep-0020/ "PEP 20 – The Zen of Python") says, “Readability counts”.

A style guide is about consistency. Consistency with this style guide
is important. Consistency within a project is more important.
Consistency within one module or function is the most important.

However, know when to be inconsistent – sometimes style guide
recommendations just aren’t applicable. When in doubt, use your best
judgment. Look at other examples and decide what looks best. And
don’t hesitate to ask!

In particular: do not break backwards compatibility just to comply with
this PEP!

Some other good reasons to ignore a particular guideline:

1. When applying the guideline would make the code less readable, even
   for someone who is used to reading code that follows this PEP.
2. To be consistent with surrounding code that also breaks it (maybe
   for historic reasons) – although this is also an opportunity to
   clean up someone else’s mess (in true XP style).
3. Because the code in question predates the introduction of the
   guideline and there is no other reason to be modifying that code.
4. When the code needs to remain compatible with older versions of
   Python that don’t support the feature recommended by the style guide.

Use 4 spaces per indentation level.

Continuation lines should align wrapped elements either vertically
using Python’s implicit line joining inside parentheses, brackets and
braces, or using a *hanging indent* . When using a hanging
indent the following should be considered; there should be no
arguments on the first line and further indentation should be used to
clearly distinguish itself as a continuation line:

```
# Correct:

# Aligned with opening delimiter.
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

# Add 4 spaces (an extra level of indentation) to distinguish arguments from the rest.
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)

# Hanging indents should add a level.
foo = long_function_name(
    var_one, var_two,
    var_three, var_four)
```

```
# Wrong:

# Arguments on first line forbidden when not using vertical alignment.
foo = long_function_name(var_one, var_two,
    var_three, var_four)

# Further indentation required as indentation is not distinguishable.
def long_function_name(
    var_one, var_two, var_three,
    var_four):
    print(var_one)
```

The 4-space rule is optional for continuation lines.

Optional:

```
# Hanging indents *may* be indented to other than 4 spaces.
foo = long_function_name(
  var_one, var_two,
  var_three, var_four)
```

When the conditional part of an `if`-statement is long enough to require
that it be written across multiple lines, it’s worth noting that the
combination of a two character keyword (i.e. `if`), plus a single space,
plus an opening parenthesis creates a natural 4-space indent for the
subsequent lines of the multiline conditional. This can produce a visual
conflict with the indented suite of code nested inside the `if`-statement,
which would also naturally be indented to 4 spaces. This PEP takes no
explicit position on how (or whether) to further visually distinguish such
conditional lines from the nested suite inside the `if`-statement.
Acceptable options in this situation include, but are not limited to:

```
# No extra indentation.
if (this_is_one_thing and
    that_is_another_thing):
    do_something()

# Add a comment, which will provide some distinction in editors
# supporting syntax highlighting.
if (this_is_one_thing and
    that_is_another_thing):
    # Since both conditions are true, we can frobnicate.
    do_something()

# Add some extra indentation on the conditional continuation line.
if (this_is_one_thing
        and that_is_another_thing):
    do_something()
```

(Also see the discussion of whether to break before or after binary
operators below.)

The closing brace/bracket/parenthesis on multiline constructs may
either line up under the first non-whitespace character of the last
line of list, as in:

```
my_list = [
    1, 2, 3,
    4, 5, 6,
    ]
result = some_function_that_takes_arguments(
    'a', 'b', 'c',
    'd', 'e', 'f',
    )
```

or it may be lined up under the first character of the line that
starts the multiline construct, as in:

```
my_list = [
    1, 2, 3,
    4, 5, 6,
]
result = some_function_that_takes_arguments(
    'a', 'b', 'c',
    'd', 'e', 'f',
)
```

Spaces are the preferred indentation method.

Tabs should be used solely to remain consistent with code that is
already indented with tabs.

Python disallows mixing tabs and spaces for indentation.

Limit all lines to a maximum of 79 characters.

For flowing long blocks of text with fewer structural restrictions
(docstrings or comments), the line length should be limited to 72
characters.

Limiting the required editor window width makes it possible to have
several files open side by side, and works well when using code
review tools that present the two versions in adjacent columns.

The default wrapping in most tools disrupts the visual structure of the
code, making it more difficult to understand. The limits are chosen to
avoid wrapping in editors with the window width set to 80, even
if the tool places a marker glyph in the final column when wrapping
lines. Some web based tools may not offer dynamic line wrapping at all.

Some teams strongly prefer a longer line length. For code maintained
exclusively or primarily by a team that can reach agreement on this
issue, it is okay to increase the line length limit up to 99 characters,
provided that comments and docstrings are still wrapped at 72
characters.

The Python standard library is conservative and requires limiting
lines to 79 characters (and docstrings/comments to 72).

The preferred way of wrapping long lines is by using Python’s implied
line continuation inside parentheses, brackets and braces. Long lines
can be broken over multiple lines by wrapping expressions in
parentheses. These should be used in preference to using a backslash
for line continuation.

Backslashes may still be appropriate at times. For example, long,
multiple `with`-statements could not use implicit continuation
before Python 3.10, so backslashes were acceptable for that case:

```
with open('/path/to/some/file/you/want/to/read') as file_1, \
     open('/path/to/some/file/being/written', 'w') as file_2:
    file_2.write(file_1.read())
```

(See the previous discussion on [multiline if-statements](#multiline-if-statements) for further
thoughts on the indentation of such multiline `with`-statements.)

Another such case is with `assert` statements.

Make sure to indent the continued line appropriately.

For decades the recommended style was to break after binary operators.
But this can hurt readability in two ways: the operators tend to get
scattered across different columns on the screen, and each operator is
moved away from its operand and onto the previous line. Here, the eye
has to do extra work to tell which items are added and which are
subtracted:

```
# Wrong:
# operators sit far away from their operands
income = (gross_wages +
          taxable_interest +
          (dividends - qualified_dividends) -
          ira_deduction -
          student_loan_interest)
```

To solve this readability problem, mathematicians and their publishers
follow the opposite convention. Donald Knuth explains the traditional
rule in his *Computers and Typesetting* series: “Although formulas
within a paragraph always break after binary operations and relations,
displayed formulas always break before binary operations” .

Following the tradition from mathematics usually results in more
readable code:

```
# Correct:
# easy to match operators with operands
income = (gross_wages
          + taxable_interest
          + (dividends - qualified_dividends)
          - ira_deduction
          - student_loan_interest)
```

In Python code, it is permissible to break before or after a binary
operator, as long as the convention is consistent locally. For new
code Knuth’s style is suggested.

Surround top-level function and class definitions with two blank
lines.

Method definitions inside a class are surrounded by a single blank
line.

Extra blank lines may be used (sparingly) to separate groups of
related functions. Blank lines may be omitted between a bunch of
related one-liners (e.g. a set of dummy implementations).

Use blank lines in functions, sparingly, to indicate logical sections.

Python accepts the control-L (i.e. ^L) form feed character as
whitespace; many tools treat these characters as page separators, so
you may use them to separate pages of related sections of your file.
Note, some editors and web-based code viewers may not recognize
control-L as a form feed and will show another glyph in its place.

Code in the core Python distribution should always use UTF-8, and should not
have an encoding declaration.

In the standard library, non-UTF-8 encodings should be used only for
test purposes. Use non-ASCII characters sparingly, preferably only to
denote places and human names. If using non-ASCII characters as data,
avoid noisy Unicode characters like z̯̯͡a̧͎̺l̡͓̫g̹̲o̡̼̘ and byte order
marks.

All identifiers in the Python standard library MUST use ASCII-only
identifiers, and SHOULD use English words wherever feasible (in many
cases, abbreviations and technical terms are used which aren’t
English).

Open source projects with a global audience are encouraged to adopt a
similar policy.

* Imports should usually be on separate lines:

  ```
  # Correct:
  import os
  import sys
  ```

  It’s okay to say this though:

  ```
  # Correct:
  from subprocess import Popen, PIPE
  ```
* Imports are always put at the top of the file, just after any module
  comments and docstrings, and before module globals and constants.

  Imports should be grouped in the following order:

  1. Standard library imports.
  2. Related third party imports.
  3. Local application/library specific imports.

  You should put a blank line between each group of imports.
* Absolute imports are recommended, as they are usually more readable
  and tend to be better behaved (or at least give better error
  messages) if the import system is incorrectly configured (such as
  when a directory inside a package ends up on `sys.path`):

  ```
  import mypkg.sibling
  from mypkg import sibling
  from mypkg.sibling import example
  ```

  However, explicit relative imports are an acceptable alternative to
  absolute imports, especially when dealing with complex package layouts
  where using absolute imports would be unnecessarily verbose:

  ```
  from . import sibling
  from .sibling import example
  ```

  Standard library code should avoid complex package layouts and always
  use absolute imports.
* When importing a class from a class-containing module, it’s usually
  okay to spell this:

  ```
  from myclass import MyClass
  from foo.bar.yourclass import YourClass
  ```

  If this spelling causes local name clashes, then spell them explicitly:

  ```
  import myclass
  import foo.bar.yourclass
  ```

  and use `myclass.MyClass` and `foo.bar.yourclass.YourClass`.
* Wildcard imports (`from <module> import *`) should be avoided, as
  they make it unclear which names are present in the namespace,
  confusing both readers and many automated tools. There is one
  defensible use case for a wildcard import, which is to republish an
  internal interface as part of a public API (for example, overwriting
  a pure Python implementation of an interface with the definitions
  from an optional accelerator module and exactly which definitions
  will be overwritten isn’t known in advance).

  When republishing names this way, the guidelines below regarding
  public and internal interfaces still apply.

Module level “dunders” (i.e. names with two leading and two trailing
underscores) such as `__all__`, `__author__`, `__version__`,
etc. should be placed after the module docstring but before any import
statements *except* `from __future__` imports. Python mandates that
future-imports must appear in the module before any other code except
docstrings:

```
"""This is the example module.

This module does stuff.
"""

from __future__ import barry_as_FLUFL

__all__ = ['a', 'b', 'c']
__version__ = '0.1'
__author__ = 'Cardinal Biggles'

import os
import sys
```

The naming conventions of Python’s library are a bit of a mess, so
we’ll never get this completely consistent – nevertheless, here are
the currently recommended naming standards. New modules and packages
(including third party frameworks) should be written to these
standards, but where an existing library has a different style,
internal consistency is preferred.

Names that are visible to the user as public parts of the API should
follow conventions that reflect usage rather than implementation.

There are a lot of different naming styles. It helps to be able to
recognize what naming style is being used, independently from what
they are used for.

The following naming styles are commonly distinguished:

There’s also the style of using a short unique prefix to group related
names together. This is not used much in Python, but it is mentioned
for completeness. For example, the `os.stat()` function returns a
tuple whose items traditionally have names like `st_mode`,
`st_size`, `st_mtime` and so on. (This is done to emphasize the
correspondence with the fields of the POSIX system call struct, which
helps programmers familiar with that.)

The X11 library uses a leading X for all its public functions. In
Python, this style is generally deemed unnecessary because attribute
and method names are prefixed with an object, and function names are
prefixed with a module name.

In addition, the following special forms using leading or trailing
underscores are recognized (these can generally be combined with any
case convention):

* `_single_leading_underscore`: weak “internal use” indicator.
  E.g. `from M import *` does not import objects whose names start
  with an underscore.
* `single_trailing_underscore_`: used by convention to avoid
  conflicts with Python keyword, e.g. :

  ```
  tkinter.Toplevel(master, class_='ClassName')
  ```
* `__double_leading_underscore`: when naming a class attribute,
  invokes name mangling (inside class FooBar, `__boo` becomes
  `_FooBar__boo`; see below).
* `__double_leading_and_trailing_underscore__`: “magic” objects or
  attributes that live in user-controlled namespaces.
  E.g. `__init__`, `__import__` or `__file__`. Never invent
  such names; only use them as documented.

Never use the characters ‘l’ (lowercase letter el), ‘O’ (uppercase
letter oh), or ‘I’ (uppercase letter eye) as single character variable
names.

In some fonts, these characters are indistinguishable from the
numerals one and zero. When tempted to use ‘l’, use ‘L’ instead.

Identifiers used in the standard library must be ASCII compatible
as described in the
[policy section](../pep-3131/#policy-specification "PEP 3131 – Supporting Non-ASCII Identifiers § Policy Specification")
of [PEP 3131](../pep-3131/ "PEP 3131 – Supporting Non-ASCII Identifiers").

Modules should have short, all-lowercase names. Underscores can be
used in the module name if it improves readability. Python packages
should also have short, all-lowercase names, although the use of
underscores is discouraged.

When an extension module written in C or C++ has an accompanying
Python module that provides a higher level (e.g. more object oriented)
interface, the C/C++ module has a leading underscore
(e.g. `_socket`).

Class names should normally use the CapWords convention.

The naming convention for functions may be used instead in cases where
the interface is documented and used primarily as a callable.

Note that there is a separate convention for builtin names: most builtin
names are single words (or two words run together), with the CapWords
convention used only for exception names and builtin constants.

Names of type variables introduced in [PEP 484](../pep-0484/ "PEP 484 – Type Hints") should normally use CapWords
preferring short names: `T`, `AnyStr`, `Num`. It is recommended to add
suffixes `_co` or `_contra` to the variables used to declare covariant
or contravariant behavior correspondingly:

```
from typing import TypeVar

VT_co = TypeVar('VT_co', covariant=True)
KT_contra = TypeVar('KT_contra', contravariant=True)
```

Because exceptions should be classes, the class naming convention
applies here. However, you should use the suffix “Error” on your
exception names (if the exception actually is an error).

(Let’s hope that these variables are meant for use inside one module
only.) The conventions are about the same as those for functions.

Modules that are designed for use via `from M import *` should use
the `__all__` mechanism to prevent exporting globals, or use the
older convention of prefixing such globals with an underscore (which
you might want to do to indicate these globals are “module
non-public”).

Function names should be lowercase, with words separated by
underscores as necessary to improve readability.

Variable names follow the same convention as function names.

mixedCase is allowed only in contexts where that’s already the
prevailing style (e.g. threading.py), to retain backwards
compatibility.

Always use `self` for the first argument to instance methods.

Always use `cls` for the first argument to class methods.

If a function argument’s name clashes with a reserved keyword, it is
generally better to append a single trailing underscore rather than
use an abbreviation or spelling corruption. Thus `class_` is better
than `clss`. (Perhaps better is to avoid such clashes by using a
synonym.)

Use the function naming rules: lowercase with words separated by
underscores as necessary to improve readability.

Use one leading underscore only for non-public methods and instance
variables.

To avoid name clashes with subclasses, use two leading underscores to
invoke Python’s name mangling rules.

Python mangles these names with the class name: if class Foo has an
attribute named `__a`, it cannot be accessed by `Foo.__a`. (An
insistent user could still gain access by calling `Foo._Foo__a`.)
Generally, double leading underscores should be used only to avoid
name conflicts with attributes in classes designed to be subclassed.

Note: there is some controversy about the use of \_\_names (see below).

Constants are usually defined on a module level and written in all
capital letters with underscores separating words. Examples include
`MAX_OVERFLOW` and `TOTAL`.

Always decide whether a class’s methods and instance variables
(collectively: “attributes”) should be public or non-public. If in
doubt, choose non-public; it’s easier to make it public later than to
make a public attribute non-public.

Public attributes are those that you expect unrelated clients of your
class to use, with your commitment to avoid backwards incompatible
changes. Non-public attributes are those that are not intended to be
used by third parties; you make no guarantees that non-public
attributes won’t change or even be removed.

We don’t use the term “private” here, since no attribute is really
private in Python (without a generally unnecessary amount of work).

Another category of attributes are those that are part of the
“subclass API” (often called “protected” in other languages). Some
classes are designed to be inherited from, either to extend or modify
aspects of the class’s behavior. When designing such a class, take
care to make explicit decisions about which attributes are public,
which are part of the subclass API, and which are truly only to be
used by your base class.

With this in mind, here are the Pythonic guidelines:

* Public attributes should have no leading underscores.
* If your public attribute name collides with a reserved keyword,
  append a single trailing underscore to your attribute name. This is
  preferable to an abbreviation or corrupted spelling. (However,
  notwithstanding this rule, ‘cls’ is the preferred spelling for any
  variable or argument which is known to be a class, especially the
  first argument to a class method.)

  Note 1: See the argument name recommendation above for class methods.
* For simple public data attributes, it is best to expose just the
  attribute name, without complicated accessor/mutator methods. Keep
  in mind that Python provides an easy path to future enhancement,
  should you find that a simple data attribute needs to grow
  functional behavior. In that case, use properties to hide
  functional implementation behind simple data attribute access
  syntax.

  Note 1: Try to keep the functional behavior side-effect free,
  although side-effects such as caching are generally fine.

  Note 2: Avoid using properties for computationally expensive
  operations; the attribute notation makes the caller believe that
  access is (relatively) cheap.
* If your class is intended to be subclassed, and you have attributes
  that you do not want subclasses to use, consider naming them with
  double leading underscores and no trailing underscores. This
  invokes Python’s name mangling algorithm, where the name of the
  class is mangled into the attribute name. This helps avoid
  attribute name collisions should subclasses inadvertently contain
  attributes with the same name.

  Note 1: Note that only the simple class name is used in the mangled
  name, so if a subclass chooses both the same class name and attribute
  name, you can still get name collisions.

  Note 2: Name mangling can make certain uses, such as debugging and
  `__getattr__()`, less convenient. However the name mangling
  algorithm is well documented and easy to perform manually.

  Note 3: Not everyone likes name mangling. Try to balance the
  need to avoid accidental name clashes with potential use by
  advanced callers.

Any backwards compatibility guarantees apply only to public interfaces.
Accordingly, it is important that users be able to clearly distinguish
between public and internal interfaces.

Documented interfaces are considered public, unless the documentation
explicitly declares them to be provisional or internal interfaces exempt
from the usual backwards compatibility guarantees. All undocumented
interfaces should be assumed to be internal.

To better support introspection, modules should explicitly declare the
names in their public API using the `__all__` attribute. Setting
`__all__` to an empty list indicates that the module has no public API.

Even with `__all__` set appropriately, internal interfaces (packages,
modules, classes, functions, attributes or other names) should still be
prefixed with a single leading underscore.

An interface is also considered internal if any containing namespace
(package, module or class) is considered internal.

Imported names should always be considered an implementation detail.
Other modules must not rely on indirect access to such imported names
unless they are an explicitly documented part of the containing module’s
API, such as `os.path` or a package’s `__init__` module that exposes
functionality from submodules.