## 3.1. Objects, values and types

*Objects* are Pythonâs abstraction for data. All data in a Python program
is represented by objects or by relations between objects. (In a sense, and in
conformance to Von Neumannâs model of a âstored program computerâ, code is also
represented by objects.)

Every object has an identity, a type and a value. An objectâs *identity* never
changes once it has been created; you may think of it as the objectâs address in
memory. The [`is`](expressions.html#is) operator compares the identity of two objects; the
[`id()`](../library/functions.html#id "id") function returns an integer representing its identity.

**CPython implementation detail:** For CPython, `id(x)` is the memory address where `x` is stored.

An objectâs type determines the operations that the object supports (e.g., âdoes
it have a length?â) and also defines the possible values for objects of that
type. The [`type()`](../library/functions.html#type "type") function returns an objectâs type (which is an object
itself). Like its identity, an objectâs *type* is also unchangeable.

The *value* of some objects can change. Objects whose value can
change are said to be *mutable*; objects whose value is unchangeable once they
are created are called *immutable*. (The value of an immutable container object
that contains a reference to a mutable object can change when the latterâs value
is changed; however the container is still considered immutable, because the
collection of objects it contains cannot be changed. So, immutability is not
strictly the same as having an unchangeable value, it is more subtle.) An
objectâs mutability is determined by its type; for instance, numbers, strings
and tuples are immutable, while dictionaries and lists are mutable.

Objects are never explicitly destroyed; however, when they become unreachable
they may be garbage-collected. An implementation is allowed to postpone garbage
collection or omit it altogether â it is a matter of implementation quality
how garbage collection is implemented, as long as no objects are collected that
are still reachable.

**CPython implementation detail:** CPython currently uses a reference-counting scheme with (optional) delayed
detection of cyclically linked garbage, which collects most objects as soon
as they become unreachable, but is not guaranteed to collect garbage
containing circular references. See the documentation of the [`gc`](../library/gc.html#module-gc "gc: Interface to the cycle-detecting garbage collector.")
module for information on controlling the collection of cyclic garbage.
Other implementations act differently and CPython may change.
Do not depend on immediate finalization of objects when they become
unreachable (so you should always close files explicitly).

Note that the use of the implementationâs tracing or debugging facilities may
keep objects alive that would normally be collectable. Also note that catching
an exception with a [`try`](compound_stmts.html#try)â¦[`except`](compound_stmts.html#except) statement may keep
objects alive.

Some objects contain references to âexternalâ resources such as open files or
windows. It is understood that these resources are freed when the object is
garbage-collected, but since garbage collection is not guaranteed to happen,
such objects also provide an explicit way to release the external resource,
usually a `close()` method. Programs are strongly recommended to explicitly
close such objects. The [`try`](compound_stmts.html#try)â¦[`finally`](compound_stmts.html#finally) statement
and the [`with`](compound_stmts.html#with) statement provide convenient ways to do this.

Some objects contain references to other objects; these are called *containers*.
Examples of containers are tuples, lists and dictionaries. The references are
part of a containerâs value. In most cases, when we talk about the value of a
container, we imply the values, not the identities of the contained objects;
however, when we talk about the mutability of a container, only the identities
of the immediately contained objects are implied. So, if an immutable container
(like a tuple) contains a reference to a mutable object, its value changes if
that mutable object is changed.

Types affect almost all aspects of object behavior. Even the importance of
object identity is affected in some sense: for immutable types, operations that
compute new values may actually return a reference to any existing object with
the same type and value, while for mutable objects this is not allowed.
For example, after `a = 1; b = 1`, *a* and *b* may or may not refer to
the same object with the value one, depending on the implementation.
This is because [`int`](../library/functions.html#int "int") is an immutable type, so the reference to `1`
can be reused. This behaviour depends on the implementation used, so should
not be relied upon, but is something to be aware of when making use of object
identity tests.
However, after `c = []; d = []`, *c* and *d* are guaranteed to refer to two
different, unique, newly created empty lists. (Note that `e = f = []` assigns
the *same* object to both *e* and *f*.)

## 3.2. The standard type hierarchy

Below is a list of the types that are built into Python. Extension modules
(written in C, Java, or other languages, depending on the implementation) can
define additional types. Future versions of Python may add types to the type
hierarchy (e.g., rational numbers, efficiently stored arrays of integers, etc.),
although such additions will often be provided via the standard library instead.

Some of the type descriptions below contain a paragraph listing âspecial
attributes.â These are attributes that provide access to the implementation and
are not intended for general use. Their definition may change in the future.

### 3.2.1. None

This type has a single value. There is a single object with this value. This
object is accessed through the built-in name `None`. It is used to signify the
absence of a value in many situations, e.g., it is returned from functions that
donât explicitly return anything. Its truth value is false.

### 3.2.2. NotImplemented

This type has a single value. There is a single object with this value. This
object is accessed through the built-in name [`NotImplemented`](../library/constants.html#NotImplemented "NotImplemented"). Numeric methods
and rich comparison methods should return this value if they do not implement the
operation for the operands provided. (The interpreter will then try the
reflected operation, or some other fallback, depending on the operator.) It
should not be evaluated in a boolean context.

See
[Implementing the arithmetic operations](../library/numbers.html#implementing-the-arithmetic-operations)
for more details.

Changed in version 3.9: Evaluating [`NotImplemented`](../library/constants.html#NotImplemented "NotImplemented") in a boolean context is deprecated. While
it currently evaluates as true, it will emit a [`DeprecationWarning`](../library/exceptions.html#DeprecationWarning "DeprecationWarning").
It will raise a [`TypeError`](../library/exceptions.html#TypeError "TypeError") in a future version of Python.

### 3.2.3. Ellipsis

This type has a single value. There is a single object with this value. This
object is accessed through the literal `...` or the built-in name
`Ellipsis`. Its truth value is true.

These are created by numeric literals and returned as results by arithmetic
operators and arithmetic built-in functions. Numeric objects are immutable;
once created their value never changes. Python numbers are of course strongly
related to mathematical numbers, but subject to the limitations of numerical
representation in computers.

The string representations of the numeric classes, computed by
[`__repr__()`](#object.__repr__ "object.__repr__") and [`__str__()`](#object.__str__ "object.__str__"), have the following
properties:

* They are valid numeric literals which, when passed to their
  class constructor, produce an object having the value of the
  original numeric.
* The representation is in base 10, when possible.
* Leading zeros, possibly excepting a single zero before a
  decimal point, are not shown.
* Trailing zeros, possibly excepting a single zero after a
  decimal point, are not shown.
* A sign is shown only when the number is negative.

Python distinguishes between integers, floating-point numbers, and complex
numbers:

These represent elements from the mathematical set of integers (positive and
negative).

Note

The rules for integer representation are intended to give the most meaningful
interpretation of shift and mask operations involving negative integers.

There are two types of integers:

Integers ([`int`](../library/functions.html#int "int"))
:   These represent numbers in an unlimited range, subject to available (virtual)
    memory only. For the purpose of shift and mask operations, a binary
    representation is assumed, and negative numbers are represented in a variant of
    2âs complement which gives the illusion of an infinite string of sign bits
    extending to the left.

Booleans ([`bool`](../library/functions.html#bool "bool"))
:   These represent the truth values False and True. The two objects representing
    the values `False` and `True` are the only Boolean objects. The Boolean type is a
    subtype of the integer type, and Boolean values behave like the values 0 and 1,
    respectively, in almost all contexts, the exception being that when converted to
    a string, the strings `"False"` or `"True"` are returned, respectively.

These represent machine-level double precision floating-point numbers. You are
at the mercy of the underlying machine architecture (and C or Java
implementation) for the accepted range and handling of overflow. Python does not
support single-precision floating-point numbers; the savings in processor and
memory usage that are usually the reason for using these are dwarfed by the
overhead of using objects in Python, so there is no reason to complicate the
language with two kinds of floating-point numbers.

These represent complex numbers as a pair of machine-level double precision
floating-point numbers. The same caveats apply as for floating-point numbers.
The real and imaginary parts of a complex number `z` can be retrieved through
the read-only attributes `z.real` and `z.imag`.

### 3.2.5. Sequences

These represent finite ordered sets indexed by non-negative numbers. The
built-in function [`len()`](../library/functions.html#len "len") returns the number of items of a sequence. When
the length of a sequence is *n*, the index set contains the numbers 0, 1,
â¦, *n*-1. Item *i* of sequence *a* is selected by `a[i]`. Some sequences,
including built-in sequences, interpret negative subscripts by adding the
sequence length. For example, `a[-2]` equals `a[n-2]`, the second to last
item of sequence a with length `n`.

Sequences also support slicing: `a[i:j]` selects all items with index *k* such
that *i* `<=` *k* `<` *j*. When used as an expression, a slice is a
sequence of the same type. The comment above about negative indexes also applies
to negative slice positions.

Some sequences also support âextended slicingâ with a third âstepâ parameter:
`a[i:j:k]` selects all items of *a* with index *x* where `x = i + n*k`, *n*
`>=` `0` and *i* `<=` *x* `<` *j*.

Sequences are distinguished according to their mutability:

#### 3.2.5.1. Immutable sequences

An object of an immutable sequence type cannot change once it is created. (If
the object contains references to other objects, these other objects may be
mutable and may be changed; however, the collection of objects directly
referenced by an immutable object cannot change.)

The following types are immutable sequences:

Strings
:   A string is a sequence of values that represent Unicode code points.
    All the code points in the range `U+0000 - U+10FFFF` can be
    represented in a string. Python doesnât have a char type;
    instead, every code point in the string is represented as a string
    object with length `1`. The built-in function [`ord()`](../library/functions.html#ord "ord")
    converts a code point from its string form to an integer in the
    range `0 - 10FFFF`; [`chr()`](../library/functions.html#chr "chr") converts an integer in the range
    `0 - 10FFFF` to the corresponding length `1` string object.
    [`str.encode()`](../library/stdtypes.html#str.encode "str.encode") can be used to convert a [`str`](../library/stdtypes.html#str "str") to
    [`bytes`](../library/stdtypes.html#bytes "bytes") using the given text encoding, and
    [`bytes.decode()`](../library/stdtypes.html#bytes.decode "bytes.decode") can be used to achieve the opposite.

Tuples
:   The items of a tuple are arbitrary Python objects. Tuples of two or
    more items are formed by comma-separated lists of expressions. A tuple
    of one item (a âsingletonâ) can be formed by affixing a comma to an
    expression (an expression by itself does not create a tuple, since
    parentheses must be usable for grouping of expressions). An empty
    tuple can be formed by an empty pair of parentheses.

Bytes
:   A bytes object is an immutable array. The items are 8-bit bytes,
    represented by integers in the range 0 <= x < 256. Bytes literals
    (like `b'abc'`) and the built-in [`bytes()`](../library/stdtypes.html#bytes "bytes") constructor
    can be used to create bytes objects. Also, bytes objects can be
    decoded to strings via the [`decode()`](../library/stdtypes.html#bytes.decode "bytes.decode") method.

#### 3.2.5.2. Mutable sequences

Mutable sequences can be changed after they are created. The subscription and
slicing notations can be used as the target of assignment and [`del`](simple_stmts.html#del)
(delete) statements.

Note

The [`collections`](../library/collections.html#module-collections "collections: Container datatypes") and [`array`](../library/array.html#module-array "array: Space efficient arrays of uniformly typed numeric values.") module provide
additional examples of mutable sequence types.

There are currently two intrinsic mutable sequence types:

Lists
:   The items of a list are arbitrary Python objects. Lists are formed by
    placing a comma-separated list of expressions in square brackets. (Note
    that there are no special cases needed to form lists of length 0 or 1.)

Byte Arrays
:   A bytearray object is a mutable array. They are created by the built-in
    [`bytearray()`](../library/stdtypes.html#bytearray "bytearray") constructor. Aside from being mutable
    (and hence unhashable), byte arrays otherwise provide the same interface
    and functionality as immutable [`bytes`](../library/stdtypes.html#bytes "bytes") objects.

### 3.2.6. Set types

These represent unordered, finite sets of unique, immutable objects. As such,
they cannot be indexed by any subscript. However, they can be iterated over, and
the built-in function [`len()`](../library/functions.html#len "len") returns the number of items in a set. Common
uses for sets are fast membership testing, removing duplicates from a sequence,
and computing mathematical operations such as intersection, union, difference,
and symmetric difference.

For set elements, the same immutability rules apply as for dictionary keys. Note
that numeric types obey the normal rules for numeric comparison: if two numbers
compare equal (e.g., `1` and `1.0`), only one of them can be contained in a
set.

There are currently two intrinsic set types:

Sets
:   These represent a mutable set. They are created by the built-in [`set()`](../library/stdtypes.html#set "set")
    constructor and can be modified afterwards by several methods, such as
    `add()`.

Frozen sets
:   These represent an immutable set. They are created by the built-in
    [`frozenset()`](../library/stdtypes.html#frozenset "frozenset") constructor. As a frozenset is immutable and
    [hashable](../glossary.html#term-hashable), it can be used again as an element of another set, or as
    a dictionary key.

### 3.2.7. Mappings

These represent finite sets of objects indexed by arbitrary index sets. The
subscript notation `a[k]` selects the item indexed by `k` from the mapping
`a`; this can be used in expressions and as the target of assignments or
[`del`](simple_stmts.html#del) statements. The built-in function [`len()`](../library/functions.html#len "len") returns the number
of items in a mapping.

There is currently a single intrinsic mapping type:

#### 3.2.7.1. Dictionaries

These represent finite sets of objects indexed by nearly arbitrary values. The
only types of values not acceptable as keys are values containing lists or
dictionaries or other mutable types that are compared by value rather than by
object identity, the reason being that the efficient implementation of
dictionaries requires a keyâs hash value to remain constant. Numeric types used
for keys obey the normal rules for numeric comparison: if two numbers compare
equal (e.g., `1` and `1.0`) then they can be used interchangeably to index
the same dictionary entry.

Dictionaries preserve insertion order, meaning that keys will be produced
in the same order they were added sequentially over the dictionary.
Replacing an existing key does not change the order, however removing a key
and re-inserting it will add it to the end instead of keeping its old place.

Dictionaries are mutable; they can be created by the `{}` notation (see
section [Dictionary displays](expressions.html#dict)).

The extension modules [`dbm.ndbm`](../library/dbm.html#module-dbm.ndbm "dbm.ndbm: The New Database Manager (Unix)") and [`dbm.gnu`](../library/dbm.html#module-dbm.gnu "dbm.gnu: GNU database manager (Unix)") provide
additional examples of mapping types, as does the [`collections`](../library/collections.html#module-collections "collections: Container datatypes")
module.

Changed in version 3.7: Dictionaries did not preserve insertion order in versions of Python before 3.6.
In CPython 3.6, insertion order was preserved, but it was considered
an implementation detail at that time rather than a language guarantee.

### 3.2.8. Callable types

These are the types to which the function call operation (see section
[Calls](expressions.html#calls)) can be applied:

#### 3.2.8.1. User-defined functions

A user-defined function object is created by a function definition (see
section [Function definitions](compound_stmts.html#function)). It should be called with an argument list
containing the same number of items as the functionâs formal parameter
list.

##### 3.2.8.1.1. Special read-only attributes

| Attribute | Meaning |
| --- | --- |
| function.\_\_globals\_\_ | A reference to the [`dictionary`](../library/stdtypes.html#dict "dict") that holds the functionâs [global variables](executionmodel.html#naming) â the global namespace of the module in which the function was defined. |
| function.\_\_closure\_\_ | `None` or a [`tuple`](../library/stdtypes.html#tuple "tuple") of cells that contain bindings for the names specified in the [`co_freevars`](#codeobject.co_freevars "codeobject.co_freevars") attribute of the functionâs [`code object`](#function.__code__ "function.__code__").  A cell object has the attribute `cell_contents`. This can be used to get the value of the cell, as well as set the value. |

##### 3.2.8.1.2. Special writable attributes

Most of these attributes check the type of the assigned value:

| Attribute | Meaning |
| --- | --- |
| function.\_\_doc\_\_ | The functionâs documentation string, or `None` if unavailable. |
| function.\_\_name\_\_ | The functionâs name. See also: [`__name__ attributes`](../library/stdtypes.html#definition.__name__ "definition.__name__"). |
| function.\_\_qualname\_\_ | The functionâs [qualified name](../glossary.html#term-qualified-name). See also: [`__qualname__ attributes`](../library/stdtypes.html#definition.__qualname__ "definition.__qualname__"). |
| function.\_\_module\_\_ | The name of the module the function was defined in, or `None` if unavailable. |
| function.\_\_defaults\_\_ | A [`tuple`](../library/stdtypes.html#tuple "tuple") containing default [parameter](../glossary.html#term-parameter) values for those parameters that have defaults, or `None` if no parameters have a default value. |
| function.\_\_code\_\_ | The [code object](#code-objects) representing the compiled function body. |
| function.\_\_dict\_\_ | The namespace supporting arbitrary function attributes. See also: [`__dict__ attributes`](#object.__dict__ "object.__dict__"). |
| function.\_\_annotations\_\_ | A [`dictionary`](../library/stdtypes.html#dict "dict") containing annotations of [parameters](../glossary.html#term-parameter). The keys of the dictionary are the parameter names, and `'return'` for the return annotation, if provided. See also: [Annotations Best Practices](../howto/annotations.html#annotations-howto). |
| function.\_\_kwdefaults\_\_ | A [`dictionary`](../library/stdtypes.html#dict "dict") containing defaults for keyword-only [parameters](../glossary.html#term-parameter). |
| function.\_\_type\_params\_\_ | A [`tuple`](../library/stdtypes.html#tuple "tuple") containing the [type parameters](compound_stmts.html#type-params) of a [generic function](compound_stmts.html#generic-functions). |

Function objects also support getting and setting arbitrary attributes, which
can be used, for example, to attach metadata to functions. Regular attribute
dot-notation is used to get and set such attributes.

**CPython implementation detail:** CPythonâs current implementation only supports function attributes
on user-defined functions. Function attributes on
[built-in functions](#builtin-functions) may be supported in the
future.

Additional information about a functionâs definition can be retrieved from its
[code object](#code-objects)
(accessible via the [`__code__`](#function.__code__ "function.__code__") attribute).

#### 3.2.8.2. Instance methods

An instance method object combines a class, a class instance and any
callable object (normally a user-defined function).

Special read-only attributes:

|  |  |
| --- | --- |
| method.\_\_self\_\_ | Refers to the class instance object to which the method is [bound](#method-binding) |
| method.\_\_func\_\_ | Refers to the original [function object](#user-defined-funcs) |
| method.\_\_doc\_\_ | The methodâs documentation (same as [`method.__func__.__doc__`](#function.__doc__ "function.__doc__")). A [`string`](../library/stdtypes.html#str "str") if the original function had a docstring, else `None`. |
| method.\_\_name\_\_ | The name of the method (same as [`method.__func__.__name__`](#function.__name__ "function.__name__")) |
| method.\_\_module\_\_ | The name of the module the method was defined in, or `None` if unavailable. |

Methods also support accessing (but not setting) the arbitrary function
attributes on the underlying [function object](#user-defined-funcs).

User-defined method objects may be created when getting an attribute of a
class (perhaps via an instance of that class), if that attribute is a
user-defined [function object](#user-defined-funcs) or a
[`classmethod`](../library/functions.html#classmethod "classmethod") object.

When an instance method object is created by retrieving a user-defined
[function object](#user-defined-funcs) from a class via one of its
instances, its [`__self__`](#method.__self__ "method.__self__") attribute is the instance, and the
method object is said to be *bound*. The new methodâs [`__func__`](#method.__func__ "method.__func__")
attribute is the original function object.

When an instance method object is created by retrieving a [`classmethod`](../library/functions.html#classmethod "classmethod")
object from a class or instance, its [`__self__`](#method.__self__ "method.__self__") attribute is the
class itself, and its [`__func__`](#method.__func__ "method.__func__") attribute is the function object
underlying the class method.

When an instance method object is called, the underlying function
([`__func__`](#method.__func__ "method.__func__")) is called, inserting the class instance
([`__self__`](#method.__self__ "method.__self__")) in front of the argument list. For instance, when
`C` is a class which contains a definition for a function
`f()`, and `x` is an instance of `C`, calling `x.f(1)` is
equivalent to calling `C.f(x, 1)`.

When an instance method object is derived from a [`classmethod`](../library/functions.html#classmethod "classmethod") object, the
âclass instanceâ stored in [`__self__`](#method.__self__ "method.__self__") will actually be the class
itself, so that calling either `x.f(1)` or `C.f(1)` is equivalent to
calling `f(C,1)` where `f` is the underlying function.

It is important to note that user-defined functions
which are attributes of a class instance are not converted to bound
methods; this *only* happens when the function is an attribute of the
class.

#### 3.2.8.3. Generator functions

A function or method which uses the [`yield`](simple_stmts.html#yield) statement (see section
[The yield statement](simple_stmts.html#yield)) is called a *generator function*. Such a function, when
called, always returns an [iterator](../glossary.html#term-iterator) object which can be used to
execute the body of the function: calling the iteratorâs
[`iterator.__next__()`](../library/stdtypes.html#iterator.__next__ "iterator.__next__") method will cause the function to execute until
it provides a value using the `yield` statement. When the
function executes a [`return`](simple_stmts.html#return) statement or falls off the end, a
[`StopIteration`](../library/exceptions.html#StopIteration "StopIteration") exception is raised and the iterator will have
reached the end of the set of values to be returned.

#### 3.2.8.5. Asynchronous generator functions

A function or method which is defined using [`async def`](compound_stmts.html#async-def) and
which uses the [`yield`](simple_stmts.html#yield) statement is called a
*asynchronous generator function*. Such a function, when called,
returns an [asynchronous iterator](../glossary.html#term-asynchronous-iterator) object which can be used in an
[`async for`](compound_stmts.html#async-for) statement to execute the body of the function.

Calling the asynchronous iteratorâs
[`aiterator.__anext__`](#object.__anext__ "object.__anext__") method
will return an [awaitable](../glossary.html#term-awaitable) which when awaited
will execute until it provides a value using the [`yield`](simple_stmts.html#yield)
expression. When the function executes an empty [`return`](simple_stmts.html#return)
statement or falls off the end, a [`StopAsyncIteration`](../library/exceptions.html#StopAsyncIteration "StopAsyncIteration") exception
is raised and the asynchronous iterator will have reached the end of
the set of values to be yielded.

#### 3.2.8.6. Built-in functions

A built-in function object is a wrapper around a C function. Examples of
built-in functions are [`len()`](../library/functions.html#len "len") and [`math.sin()`](../library/math.html#math.sin "math.sin") ([`math`](../library/math.html#module-math "math: Mathematical functions (sin() etc.).") is a
standard built-in module). The number and type of the arguments are
determined by the C function. Special read-only attributes:

* `__doc__` is the functionâs documentation string, or `None` if
  unavailable. See [`function.__doc__`](#function.__doc__ "function.__doc__").
* `__name__` is the functionâs name. See [`function.__name__`](#function.__name__ "function.__name__").
* `__self__` is set to `None` (but see the next item).
* `__module__` is the name of
  the module the function was defined in or `None` if unavailable.
  See [`function.__module__`](#function.__module__ "function.__module__").

#### 3.2.8.7. Built-in methods

This is really a different disguise of a built-in function, this time containing
an object passed to the C function as an implicit extra argument. An example of
a built-in method is `alist.append()`, assuming *alist* is a list object. In
this case, the special read-only attribute `__self__` is set to the object
denoted by *alist*. (The attribute has the same semantics as it does with
[`other instance methods`](#method.__self__ "method.__self__").)

#### 3.2.8.8. Classes

Classes are callable. These objects normally act as factories for new
instances of themselves, but variations are possible for class types that
override [`__new__()`](#object.__new__ "object.__new__"). The arguments of the call are passed to
`__new__()` and, in the typical case, to [`__init__()`](#object.__init__ "object.__init__") to
initialize the new instance.

#### 3.2.8.9. Class Instances

Instances of arbitrary classes can be made callable by defining a
[`__call__()`](#object.__call__ "object.__call__") method in their class.

### 3.2.9. Modules

Modules are a basic organizational unit of Python code, and are created by
the [import system](import.html#importsystem) as invoked either by the
[`import`](simple_stmts.html#import) statement, or by calling
functions such as [`importlib.import_module()`](../library/importlib.html#importlib.import_module "importlib.import_module") and built-in
[`__import__()`](../library/functions.html#import__ "__import__"). A module object has a namespace implemented by a
[`dictionary`](../library/stdtypes.html#dict "dict") object (this is the dictionary referenced by the
[`__globals__`](#function.__globals__ "function.__globals__")
attribute of functions defined in the module). Attribute references are
translated to lookups in this dictionary, e.g., `m.x` is equivalent to
`m.__dict__["x"]`. A module object does not contain the code object used
to initialize the module (since it isnât needed once the initialization is
done).

Attribute assignment updates the moduleâs namespace dictionary, e.g.,
`m.x = 1` is equivalent to `m.__dict__["x"] = 1`.

#### 3.2.9.2. Other writable attributes on module objects

As well as the import-related attributes listed above, module objects also have
the following writable attributes:

module.\_\_doc\_\_
:   The moduleâs documentation string, or `None` if unavailable.
    See also: [`__doc__ attributes`](../library/stdtypes.html#definition.__doc__ "definition.__doc__").

module.\_\_annotations\_\_
:   A dictionary containing
    [variable annotations](../glossary.html#term-variable-annotation) collected during module
    body execution. For best practices on working with [`__annotations__`](#module.__annotations__ "module.__annotations__"),
    please see [Annotations Best Practices](../howto/annotations.html#annotations-howto).

#### 3.2.9.3. Module dictionaries

Module objects also have the following special read-only attribute:

module.\_\_dict\_\_
:   The moduleâs namespace as a dictionary object. Uniquely among the attributes
    listed here, `__dict__` cannot be accessed as a global variable from
    within a module; it can only be accessed as an attribute on module objects.

    **CPython implementation detail:** Because of the way CPython clears module dictionaries, the module
    dictionary will be cleared when the module falls out of scope even if the
    dictionary still has live references. To avoid this, copy the dictionary
    or keep the module around while using its dictionary directly.

### 3.2.10. Custom classes

Custom class types are typically created by class definitions (see section
[Class definitions](compound_stmts.html#class)). A class has a namespace implemented by a dictionary object.
Class attribute references are translated to lookups in this dictionary, e.g.,
`C.x` is translated to `C.__dict__["x"]` (although there are a number of
hooks which allow for other means of locating attributes). When the attribute
name is not found there, the attribute search continues in the base classes.
This search of the base classes uses the C3 method resolution order which
behaves correctly even in the presence of âdiamondâ inheritance structures
where there are multiple inheritance paths leading back to a common ancestor.
Additional details on the C3 MRO used by Python can be found at
[The Python 2.3 Method Resolution Order](../howto/mro.html#python-2-3-mro).

When a class attribute reference (for class `C`, say) would yield a
class method object, it is transformed into an instance method object whose
[`__self__`](#method.__self__ "method.__self__") attribute is `C`.
When it would yield a [`staticmethod`](../library/functions.html#staticmethod "staticmethod") object,
it is transformed into the object wrapped by the static method
object. See section [Implementing Descriptors](#descriptors) for another way in which attributes
retrieved from a class may differ from those actually contained in its
[`__dict__`](#object.__dict__ "object.__dict__").

Class attribute assignments update the classâs dictionary, never the dictionary
of a base class.

A class object can be called (see above) to yield a class instance (see below).

#### 3.2.10.1. Special attributes

| Attribute | Meaning |
| --- | --- |
| type.\_\_name\_\_ | The classâs name. See also: [`__name__ attributes`](../library/stdtypes.html#definition.__name__ "definition.__name__"). |
| type.\_\_qualname\_\_ | The classâs [qualified name](../glossary.html#term-qualified-name). See also: [`__qualname__ attributes`](../library/stdtypes.html#definition.__qualname__ "definition.__qualname__"). |
| type.\_\_module\_\_ | The name of the module in which the class was defined. |
| type.\_\_dict\_\_ | A [`mapping proxy`](../library/types.html#types.MappingProxyType "types.MappingProxyType") providing a read-only view of the classâs namespace. See also: [`__dict__ attributes`](#object.__dict__ "object.__dict__"). |
| type.\_\_bases\_\_ | A [`tuple`](../library/stdtypes.html#tuple "tuple") containing the classâs bases. In most cases, for a class defined as `class X(A, B, C)`, `X.__bases__` will be exactly equal to `(A, B, C)`. |
| type.\_\_doc\_\_ | The classâs documentation string, or `None` if undefined. Not inherited by subclasses. |
| type.\_\_annotations\_\_ | A dictionary containing [variable annotations](../glossary.html#term-variable-annotation) collected during class body execution. For best practices on working with `__annotations__`, please see [Annotations Best Practices](../howto/annotations.html#annotations-howto).  Caution  Accessing the `__annotations__` attribute of a class object directly may yield incorrect results in the presence of metaclasses. In addition, the attribute may not exist for some classes. Use [`inspect.get_annotations()`](../library/inspect.html#inspect.get_annotations "inspect.get_annotations") to retrieve class annotations safely. |
| type.\_\_type\_params\_\_ | A [`tuple`](../library/stdtypes.html#tuple "tuple") containing the [type parameters](compound_stmts.html#type-params) of a [generic class](compound_stmts.html#generic-classes). |
| type.\_\_static\_attributes\_\_ | A [`tuple`](../library/stdtypes.html#tuple "tuple") containing names of attributes of this class which are assigned through `self.X` from any function in its body. |
| type.\_\_firstlineno\_\_ | The line number of the first line of the class definition, including decorators. Setting the `__module__` attribute removes the `__firstlineno__` item from the typeâs dictionary. |
| type.\_\_mro\_\_ | The [`tuple`](../library/stdtypes.html#tuple "tuple") of classes that are considered when looking for base classes during method resolution. |

#### 3.2.10.2. Special methods

In addition to the special attributes described above, all Python classes also
have the following two methods available:

type.mro()
:   This method can be overridden by a metaclass to customize the method
    resolution order for its instances. It is called at class instantiation,
    and its result is stored in [`__mro__`](#type.__mro__ "type.__mro__").

type.\_\_subclasses\_\_()
:   Each class keeps a list of weak references to its immediate subclasses. This
    method returns a list of all those references still alive. The list is in
    definition order. Example:

    ```
    >>> class A: pass
    >>> class B(A): pass
    >>> A.__subclasses__()
    [<class 'B'>]
    ```

### 3.2.11. Class instances

A class instance is created by calling a class object (see above). A class
instance has a namespace implemented as a dictionary which is the first place
in which attribute references are searched. When an attribute is not found
there, and the instanceâs class has an attribute by that name, the search
continues with the class attributes. If a class attribute is found that is a
user-defined function object, it is transformed into an instance method
object whose [`__self__`](#method.__self__ "method.__self__") attribute is the instance. Static method and
class method objects are also transformed; see above under âClassesâ. See
section [Implementing Descriptors](#descriptors) for another way in which attributes of a class
retrieved via its instances may differ from the objects actually stored in
the classâs [`__dict__`](#object.__dict__ "object.__dict__"). If no class attribute is found, and the
objectâs class has a [`__getattr__()`](#object.__getattr__ "object.__getattr__") method, that is called to satisfy
the lookup.

Attribute assignments and deletions update the instanceâs dictionary, never a
classâs dictionary. If the class has a [`__setattr__()`](#object.__setattr__ "object.__setattr__") or
[`__delattr__()`](#object.__delattr__ "object.__delattr__") method, this is called instead of updating the instance
dictionary directly.

Class instances can pretend to be numbers, sequences, or mappings if they have
methods with certain special names. See section [Special method names](#specialnames).

#### 3.2.11.1. Special attributes

object.\_\_class\_\_
:   The class to which a class instance belongs.

object.\_\_dict\_\_
:   A dictionary or other mapping object used to store an objectâs (writable)
    attributes. Not all instances have a `__dict__` attribute; see the
    section on [\_\_slots\_\_](#slots) for more details.

### 3.2.12. I/O objects (also known as file objects)

A [file object](../glossary.html#term-file-object) represents an open file. Various shortcuts are
available to create file objects: the [`open()`](../library/functions.html#open "open") built-in function, and
also [`os.popen()`](../library/os.html#os.popen "os.popen"), [`os.fdopen()`](../library/os.html#os.fdopen "os.fdopen"), and the
[`makefile()`](../library/socket.html#socket.socket.makefile "socket.socket.makefile") method of socket objects (and perhaps by
other functions or methods provided by extension modules).

The objects `sys.stdin`, `sys.stdout` and `sys.stderr` are
initialized to file objects corresponding to the interpreterâs standard
input, output and error streams; they are all open in text mode and
therefore follow the interface defined by the [`io.TextIOBase`](../library/io.html#io.TextIOBase "io.TextIOBase")
abstract class.

### 3.2.13. Internal types

A few types used internally by the interpreter are exposed to the user. Their
definitions may change with future versions of the interpreter, but they are
mentioned here for completeness.

#### 3.2.13.1. Code objects

Code objects represent *byte-compiled* executable Python code, or [bytecode](../glossary.html#term-bytecode).
The difference between a code object and a function object is that the function
object contains an explicit reference to the functionâs globals (the module in
which it was defined), while a code object contains no context; also the default
argument values are stored in the function object, not in the code object
(because they represent values calculated at run-time). Unlike function
objects, code objects are immutable and contain no references (directly or
indirectly) to mutable objects.

##### 3.2.13.1.1. Special read-only attributes

|  |  |
| --- | --- |
| codeobject.co\_name | The function name |
| codeobject.co\_qualname | The fully qualified function name |
| codeobject.co\_argcount | The total number of positional [parameters](../glossary.html#term-parameter) (including positional-only parameters and parameters with default values) that the function has |
| codeobject.co\_posonlyargcount | The number of positional-only [parameters](../glossary.html#term-parameter) (including arguments with default values) that the function has |
| codeobject.co\_kwonlyargcount | The number of keyword-only [parameters](../glossary.html#term-parameter) (including arguments with default values) that the function has |
| codeobject.co\_nlocals | The number of [local variables](executionmodel.html#naming) used by the function (including parameters) |
| codeobject.co\_varnames | A [`tuple`](../library/stdtypes.html#tuple "tuple") containing the names of the local variables in the function (starting with the parameter names) |
| codeobject.co\_cellvars | A [`tuple`](../library/stdtypes.html#tuple "tuple") containing the names of [local variables](executionmodel.html#naming) that are referenced from at least one [nested scope](../glossary.html#term-nested-scope) inside the function |
| codeobject.co\_freevars | A [`tuple`](../library/stdtypes.html#tuple "tuple") containing the names of [free (closure) variables](../glossary.html#term-closure-variable) that a [nested scope](../glossary.html#term-nested-scope) references in an outer scope. See also [`function.__closure__`](#function.__closure__ "function.__closure__").  Note: references to global and builtin names are *not* included. |
| codeobject.co\_code | A string representing the sequence of [bytecode](../glossary.html#term-bytecode) instructions in the function |
| codeobject.co\_consts | A [`tuple`](../library/stdtypes.html#tuple "tuple") containing the literals used by the [bytecode](../glossary.html#term-bytecode) in the function |
| codeobject.co\_names | A [`tuple`](../library/stdtypes.html#tuple "tuple") containing the names used by the [bytecode](../glossary.html#term-bytecode) in the function |
| codeobject.co\_filename | The name of the file from which the code was compiled |
| codeobject.co\_firstlineno | The line number of the first line of the function |
| codeobject.co\_lnotab | A string encoding the mapping from [bytecode](../glossary.html#term-bytecode) offsets to line numbers. For details, see the source code of the interpreter.  Deprecated since version 3.12: This attribute of code objects is deprecated, and may be removed in Python 3.15. |
| codeobject.co\_stacksize | The required stack size of the code object |
| codeobject.co\_flags | An [`integer`](../library/functions.html#int "int") encoding a number of flags for the interpreter. |

The following flag bits are defined for [`co_flags`](#codeobject.co_flags "codeobject.co_flags"):
bit `0x04` is set if
the function uses the `*arguments` syntax to accept an arbitrary number of
positional arguments; bit `0x08` is set if the function uses the
`**keywords` syntax to accept arbitrary keyword arguments; bit `0x20` is set
if the function is a generator. See [Code Objects Bit Flags](../library/inspect.html#inspect-module-co-flags) for details
on the semantics of each flags that might be present.

Future feature declarations (for example, `from __future__ import division`) also use bits
in [`co_flags`](#codeobject.co_flags "codeobject.co_flags") to indicate whether a code object was compiled with a
particular feature enabled. See [`compiler_flag`](../library/__future__.html#future__._Feature.compiler_flag "__future__._Feature.compiler_flag").

Other bits in [`co_flags`](#codeobject.co_flags "codeobject.co_flags") are reserved for internal use.

If a code object represents a function, the first item in
[`co_consts`](#codeobject.co_consts "codeobject.co_consts") is
the documentation string of the function, or `None` if undefined.

##### 3.2.13.1.2. Methods on code objects

codeobject.co\_positions()
:   Returns an iterable over the source code positions of each [bytecode](../glossary.html#term-bytecode)
    instruction in the code object.

    The iterator returns [`tuple`](../library/stdtypes.html#tuple "tuple")s containing the `(start_line, end_line,
    start_column, end_column)`. The *i-th* tuple corresponds to the
    position of the source code that compiled to the *i-th* code unit.
    Column information is 0-indexed utf-8 byte offsets on the given source
    line.

    This positional information can be missing. A non-exhaustive lists of
    cases where this may happen:

    * Running the interpreter with [`-X`](../using/cmdline.html#cmdoption-X) `no_debug_ranges`.
    * Loading a pyc file compiled while using [`-X`](../using/cmdline.html#cmdoption-X) `no_debug_ranges`.
    * Position tuples corresponding to artificial instructions.
    * Line and column numbers that canât be represented due to
      implementation specific limitations.

    When this occurs, some or all of the tuple elements can be
    [`None`](../library/constants.html#None "None").

    Note

    This feature requires storing column positions in code objects which may
    result in a small increase of disk usage of compiled Python files or
    interpreter memory usage. To avoid storing the extra information and/or
    deactivate printing the extra traceback information, the
    [`-X`](../using/cmdline.html#cmdoption-X) `no_debug_ranges` command line flag or the [`PYTHONNODEBUGRANGES`](../using/cmdline.html#envvar-PYTHONNODEBUGRANGES)
    environment variable can be used.

codeobject.co\_lines()
:   Returns an iterator that yields information about successive ranges of
    [bytecode](../glossary.html#term-bytecode)s. Each item yielded is a `(start, end, lineno)`
    [`tuple`](../library/stdtypes.html#tuple "tuple"):

    * `start` (an [`int`](../library/functions.html#int "int")) represents the offset (inclusive) of the start
      of the [bytecode](../glossary.html#term-bytecode) range
    * `end` (an [`int`](../library/functions.html#int "int")) represents the offset (exclusive) of the end of
      the [bytecode](../glossary.html#term-bytecode) range
    * `lineno` is an [`int`](../library/functions.html#int "int") representing the line number of the
      [bytecode](../glossary.html#term-bytecode) range, or `None` if the bytecodes in the given range
      have no line number

    The items yielded will have the following properties:

    * The first range yielded will have a `start` of 0.
    * The `(start, end)` ranges will be non-decreasing and consecutive. That
      is, for any pair of [`tuple`](../library/stdtypes.html#tuple "tuple")s, the `start` of the second will be
      equal to the `end` of the first.
    * No range will be backwards: `end >= start` for all triples.
    * The last [`tuple`](../library/stdtypes.html#tuple "tuple") yielded will have `end` equal to the size of the
      [bytecode](../glossary.html#term-bytecode).

    Zero-width ranges, where `start == end`, are allowed. Zero-width ranges
    are used for lines that are present in the source code, but have been
    eliminated by the [bytecode](../glossary.html#term-bytecode) compiler.

    See also

    [**PEP 626**](https://peps.python.org/pep-0626/) - Precise line numbers for debugging and other tools.
    :   The PEP that introduced the `co_lines()` method.

codeobject.replace(*\*\*kwargs*)
:   Return a copy of the code object with new values for the specified fields.

    Code objects are also supported by the generic function [`copy.replace()`](../library/copy.html#copy.replace "copy.replace").

#### 3.2.13.2. Frame objects

Frame objects represent execution frames. They may occur in
[traceback objects](#traceback-objects),
and are also passed to registered trace functions.

##### 3.2.13.2.1. Special read-only attributes

|  |  |
| --- | --- |
| frame.f\_back | Points to the previous stack frame (towards the caller), or `None` if this is the bottom stack frame |
| frame.f\_code | The [code object](#code-objects) being executed in this frame. Accessing this attribute raises an [auditing event](../library/sys.html#auditing) `object.__getattr__` with arguments `obj` and `"f_code"`. |
| frame.f\_locals | The mapping used by the frame to look up [local variables](executionmodel.html#naming). If the frame refers to an [optimized scope](../glossary.html#term-optimized-scope), this may return a write-through proxy object.  Changed in version 3.13: Return a proxy for optimized scopes. |
| frame.f\_globals | The dictionary used by the frame to look up [global variables](executionmodel.html#naming) |
| frame.f\_builtins | The dictionary used by the frame to look up [built-in (intrinsic) names](executionmodel.html#naming) |
| frame.f\_lasti | The âprecise instructionâ of the frame object (this is an index into the [bytecode](../glossary.html#term-bytecode) string of the [code object](#code-objects)) |

##### 3.2.13.2.2. Special writable attributes

|  |  |
| --- | --- |
| frame.f\_trace | If not `None`, this is a function called for various events during code execution (this is used by debuggers). Normally an event is triggered for each new source line (see [`f_trace_lines`](#frame.f_trace_lines "frame.f_trace_lines")). |
| frame.f\_trace\_lines | Set this attribute to [`False`](../library/constants.html#False "False") to disable triggering a tracing event for each source line. |
| frame.f\_trace\_opcodes | Set this attribute to [`True`](../library/constants.html#True "True") to allow per-opcode events to be requested. Note that this may lead to undefined interpreter behaviour if exceptions raised by the trace function escape to the function being traced. |
| frame.f\_lineno | The current line number of the frame â writing to this from within a trace function jumps to the given line (only for the bottom-most frame). A debugger can implement a Jump command (aka Set Next Statement) by writing to this attribute. |

##### 3.2.13.2.3. Frame object methods

Frame objects support one method:

frame.clear()
:   This method clears all references to [local variables](executionmodel.html#naming) held by the
    frame. Also, if the frame belonged to a [generator](../glossary.html#term-generator), the generator
    is finalized. This helps break reference cycles involving frame
    objects (for example when catching an [exception](../library/exceptions.html#bltin-exceptions)
    and storing its [traceback](#traceback-objects) for later use).

    [`RuntimeError`](../library/exceptions.html#RuntimeError "RuntimeError") is raised if the frame is currently executing
    or suspended.

    Changed in version 3.13: Attempting to clear a suspended frame raises [`RuntimeError`](../library/exceptions.html#RuntimeError "RuntimeError")
    (as has always been the case for executing frames).

#### 3.2.13.3. Traceback objects

Traceback objects represent the stack trace of an [exception](../tutorial/errors.html#tut-errors).
A traceback object
is implicitly created when an exception occurs, and may also be explicitly
created by calling [`types.TracebackType`](../library/types.html#types.TracebackType "types.TracebackType").

Changed in version 3.7: Traceback objects can now be explicitly instantiated from Python code.

For implicitly created tracebacks, when the search for an exception handler
unwinds the execution stack, at each unwound level a traceback object is
inserted in front of the current traceback. When an exception handler is
entered, the stack trace is made available to the program. (See section
[The try statement](compound_stmts.html#try).) It is accessible as the third item of the
tuple returned by [`sys.exc_info()`](../library/sys.html#sys.exc_info "sys.exc_info"), and as the
[`__traceback__`](../library/exceptions.html#BaseException.__traceback__ "BaseException.__traceback__") attribute
of the caught exception.

When the program contains no suitable
handler, the stack trace is written (nicely formatted) to the standard error
stream; if the interpreter is interactive, it is also made available to the user
as [`sys.last_traceback`](../library/sys.html#sys.last_traceback "sys.last_traceback").

For explicitly created tracebacks, it is up to the creator of the traceback
to determine how the [`tb_next`](#traceback.tb_next "traceback.tb_next") attributes should be linked to
form a full stack trace.

Special read-only attributes:

|  |  |
| --- | --- |
| traceback.tb\_frame | Points to the execution [frame](#frame-objects) of the current level.  Accessing this attribute raises an [auditing event](../library/sys.html#auditing) `object.__getattr__` with arguments `obj` and `"tb_frame"`. |
| traceback.tb\_lineno | Gives the line number where the exception occurred |
| traceback.tb\_lasti | Indicates the âprecise instructionâ. |

The line number and last instruction in the traceback may differ from the
line number of its [frame object](#frame-objects) if the exception
occurred in a
[`try`](compound_stmts.html#try) statement with no matching except clause or with a
[`finally`](compound_stmts.html#finally) clause.

traceback.tb\_next
:   The special writable attribute `tb_next` is the next level in the
    stack trace (towards the frame where the exception occurred), or `None` if
    there is no next level.

    Changed in version 3.7: This attribute is now writable

#### 3.2.13.4. Slice objects

Slice objects are used to represent slices for
[`__getitem__()`](#object.__getitem__ "object.__getitem__")
methods. They are also created by the built-in [`slice()`](../library/functions.html#slice "slice") function.

Special read-only attributes: [`start`](../library/functions.html#slice.start "slice.start") is the lower bound;
[`stop`](../library/functions.html#slice.stop "slice.stop") is the upper bound; [`step`](../library/functions.html#slice.step "slice.step") is the step
value; each is `None` if omitted. These attributes can have any type.

Slice objects support one method:

slice.indices(*self*, *length*)
:   This method takes a single integer argument *length* and computes
    information about the slice that the slice object would describe if
    applied to a sequence of *length* items. It returns a tuple of three
    integers; respectively these are the *start* and *stop* indices and the
    *step* or stride length of the slice. Missing or out-of-bounds indices
    are handled in a manner consistent with regular slices.

#### 3.2.13.5. Static method objects

Static method objects provide a way of defeating the transformation of function
objects to method objects described above. A static method object is a wrapper
around any other object, usually a user-defined method object. When a static
method object is retrieved from a class or a class instance, the object actually
returned is the wrapped object, which is not subject to any further
transformation. Static method objects are also callable. Static method
objects are created by the built-in [`staticmethod()`](../library/functions.html#staticmethod "staticmethod") constructor.

#### 3.2.13.6. Class method objects

A class method object, like a static method object, is a wrapper around another
object that alters the way in which that object is retrieved from classes and
class instances. The behaviour of class method objects upon such retrieval is
described above, under [âinstance methodsâ](#instance-methods). Class method objects are created
by the built-in [`classmethod()`](../library/functions.html#classmethod "classmethod") constructor.

## 3.3. Special method names

A class can implement certain operations that are invoked by special syntax
(such as arithmetic operations or subscripting and slicing) by defining methods
with special names. This is Pythonâs approach to *operator overloading*,
allowing classes to define their own behavior with respect to language
operators. For instance, if a class defines a method named
[`__getitem__()`](#object.__getitem__ "object.__getitem__"),
and `x` is an instance of this class, then `x[i]` is roughly equivalent
to `type(x).__getitem__(x, i)`. Except where mentioned, attempts to execute an
operation raise an exception when no appropriate method is defined (typically
[`AttributeError`](../library/exceptions.html#AttributeError "AttributeError") or [`TypeError`](../library/exceptions.html#TypeError "TypeError")).

Setting a special method to `None` indicates that the corresponding
operation is not available. For example, if a class sets
[`__iter__()`](#object.__iter__ "object.__iter__") to `None`, the class is not iterable, so calling
[`iter()`](../library/functions.html#iter "iter") on its instances will raise a [`TypeError`](../library/exceptions.html#TypeError "TypeError") (without
falling back to [`__getitem__()`](#object.__getitem__ "object.__getitem__")).

When implementing a class that emulates any built-in type, it is important that
the emulation only be implemented to the degree that it makes sense for the
object being modelled. For example, some sequences may work well with retrieval
of individual elements, but extracting a slice may not make sense. (One example
of this is the `NodeList` interface in the W3Câs Document
Object Model.)

### 3.3.1. Basic customization

object.\_\_new\_\_(*cls*[, *...*])
:   Called to create a new instance of class *cls*. [`__new__()`](#object.__new__ "object.__new__") is a static
    method (special-cased so you need not declare it as such) that takes the class
    of which an instance was requested as its first argument. The remaining
    arguments are those passed to the object constructor expression (the call to the
    class). The return value of [`__new__()`](#object.__new__ "object.__new__") should be the new object instance
    (usually an instance of *cls*).

    Typical implementations create a new instance of the class by invoking the
    superclassâs [`__new__()`](#object.__new__ "object.__new__") method using `super().__new__(cls[, ...])`
    with appropriate arguments and then modifying the newly created instance
    as necessary before returning it.

    If [`__new__()`](#object.__new__ "object.__new__") is invoked during object construction and it returns an
    instance of *cls*, then the new instanceâs [`__init__()`](#object.__init__ "object.__init__") method
    will be invoked like `__init__(self[, ...])`, where *self* is the new instance
    and the remaining arguments are the same as were passed to the object constructor.

    If [`__new__()`](#object.__new__ "object.__new__") does not return an instance of *cls*, then the new instanceâs
    [`__init__()`](#object.__init__ "object.__init__") method will not be invoked.

    [`__new__()`](#object.__new__ "object.__new__") is intended mainly to allow subclasses of immutable types (like
    int, str, or tuple) to customize instance creation. It is also commonly
    overridden in custom metaclasses in order to customize class creation.

object.\_\_init\_\_(*self*[, *...*])
:   Called after the instance has been created (by [`__new__()`](#object.__new__ "object.__new__")), but before
    it is returned to the caller. The arguments are those passed to the
    class constructor expression. If a base class has an [`__init__()`](#object.__init__ "object.__init__")
    method, the derived classâs [`__init__()`](#object.__init__ "object.__init__") method, if any, must explicitly
    call it to ensure proper initialization of the base class part of the
    instance; for example: `super().__init__([args...])`.

    Because [`__new__()`](#object.__new__ "object.__new__") and [`__init__()`](#object.__init__ "object.__init__") work together in constructing
    objects ([`__new__()`](#object.__new__ "object.__new__") to create it, and [`__init__()`](#object.__init__ "object.__init__") to customize it),
    no non-`None` value may be returned by [`__init__()`](#object.__init__ "object.__init__"); doing so will
    cause a [`TypeError`](../library/exceptions.html#TypeError "TypeError") to be raised at runtime.

object.\_\_del\_\_(*self*)
:   Called when the instance is about to be destroyed. This is also called a
    finalizer or (improperly) a destructor. If a base class has a
    [`__del__()`](#object.__del__ "object.__del__") method, the derived classâs [`__del__()`](#object.__del__ "object.__del__") method,
    if any, must explicitly call it to ensure proper deletion of the base
    class part of the instance.

    It is possible (though not recommended!) for the [`__del__()`](#object.__del__ "object.__del__") method
    to postpone destruction of the instance by creating a new reference to
    it. This is called object *resurrection*. It is implementation-dependent
    whether [`__del__()`](#object.__del__ "object.__del__") is called a second time when a resurrected object
    is about to be destroyed; the current [CPython](../glossary.html#term-CPython) implementation
    only calls it once.

    It is not guaranteed that [`__del__()`](#object.__del__ "object.__del__") methods are called for objects
    that still exist when the interpreter exits.
    [`weakref.finalize`](../library/weakref.html#weakref.finalize "weakref.finalize") provides a straightforward way to register
    a cleanup function to be called when an object is garbage collected.

    Note

    `del x` doesnât directly call `x.__del__()` â the former decrements
    the reference count for `x` by one, and the latter is only called when
    `x`âs reference count reaches zero.

    **CPython implementation detail:** It is possible for a reference cycle to prevent the reference count
    of an object from going to zero. In this case, the cycle will be
    later detected and deleted by the [cyclic garbage collector](../glossary.html#term-garbage-collection). A common cause of reference cycles is when
    an exception has been caught in a local variable. The frameâs
    locals then reference the exception, which references its own
    traceback, which references the locals of all frames caught in the
    traceback.

    See also

    Documentation for the [`gc`](../library/gc.html#module-gc "gc: Interface to the cycle-detecting garbage collector.") module.

    Warning

    Due to the precarious circumstances under which [`__del__()`](#object.__del__ "object.__del__") methods are
    invoked, exceptions that occur during their execution are ignored, and a warning
    is printed to `sys.stderr` instead. In particular:

    * [`__del__()`](#object.__del__ "object.__del__") can be invoked when arbitrary code is being executed,
      including from any arbitrary thread. If [`__del__()`](#object.__del__ "object.__del__") needs to take
      a lock or invoke any other blocking resource, it may deadlock as
      the resource may already be taken by the code that gets interrupted
      to execute [`__del__()`](#object.__del__ "object.__del__").
    * [`__del__()`](#object.__del__ "object.__del__") can be executed during interpreter shutdown. As a
      consequence, the global variables it needs to access (including other
      modules) may already have been deleted or set to `None`. Python
      guarantees that globals whose name begins with a single underscore
      are deleted from their module before other globals are deleted; if
      no other references to such globals exist, this may help in assuring
      that imported modules are still available at the time when the
      [`__del__()`](#object.__del__ "object.__del__") method is called.

object.\_\_repr\_\_(*self*)
:   Called by the [`repr()`](../library/functions.html#repr "repr") built-in function to compute the âofficialâ string
    representation of an object. If at all possible, this should look like a
    valid Python expression that could be used to recreate an object with the
    same value (given an appropriate environment). If this is not possible, a
    string of the form `<...some useful description...>` should be returned.
    The return value must be a string object. If a class defines [`__repr__()`](#object.__repr__ "object.__repr__")
    but not [`__str__()`](#object.__str__ "object.__str__"), then [`__repr__()`](#object.__repr__ "object.__repr__") is also used when an
    âinformalâ string representation of instances of that class is required.

    This is typically used for debugging, so it is important that the representation
    is information-rich and unambiguous. A default implementation is provided by the
    [`object`](../library/functions.html#object "object") class itself.

object.\_\_str\_\_(*self*)
:   Called by [`str(object)`](../library/stdtypes.html#str "str"), the default [`__format__()`](#object.__format__ "object.__format__") implementation,
    and the built-in function [`print()`](../library/functions.html#print "print"), to compute the âinformalâ or nicely
    printable string representation of an object. The return value must be a
    [str](../library/stdtypes.html#textseq) object.

    This method differs from [`object.__repr__()`](#object.__repr__ "object.__repr__") in that there is no
    expectation that [`__str__()`](#object.__str__ "object.__str__") return a valid Python expression: a more
    convenient or concise representation can be used.

    The default implementation defined by the built-in type [`object`](../library/functions.html#object "object")
    calls [`object.__repr__()`](#object.__repr__ "object.__repr__").

object.\_\_bytes\_\_(*self*)
:   Called by [bytes](../library/functions.html#func-bytes) to compute a byte-string representation
    of an object. This should return a [`bytes`](../library/stdtypes.html#bytes "bytes") object. The [`object`](../library/functions.html#object "object")
    class itself does not provide this method.

object.\_\_format\_\_(*self*, *format\_spec*)
:   Called by the [`format()`](../library/functions.html#format "format") built-in function,
    and by extension, evaluation of [formatted string literals](lexical_analysis.html#f-strings) and the [`str.format()`](../library/stdtypes.html#str.format "str.format") method, to produce a âformattedâ
    string representation of an object. The *format\_spec* argument is
    a string that contains a description of the formatting options desired.
    The interpretation of the *format\_spec* argument is up to the type
    implementing [`__format__()`](#object.__format__ "object.__format__"), however most classes will either
    delegate formatting to one of the built-in types, or use a similar
    formatting option syntax.

    See [Format Specification Mini-Language](../library/string.html#formatspec) for a description of the standard formatting syntax.

    The return value must be a string object.

    The default implementation by the [`object`](../library/functions.html#object "object") class should be given
    an empty *format\_spec* string. It delegates to [`__str__()`](#object.__str__ "object.__str__").

    Changed in version 3.4: The \_\_format\_\_ method of `object` itself raises a [`TypeError`](../library/exceptions.html#TypeError "TypeError")
    if passed any non-empty string.

    Changed in version 3.7: `object.__format__(x, '')` is now equivalent to `str(x)` rather
    than `format(str(x), '')`.

object.\_\_lt\_\_(*self*, *other*)

object.\_\_le\_\_(*self*, *other*)

object.\_\_eq\_\_(*self*, *other*)

object.\_\_ne\_\_(*self*, *other*)

object.\_\_gt\_\_(*self*, *other*)

object.\_\_ge\_\_(*self*, *other*)
:   These are the so-called ârich comparisonâ methods. The correspondence between
    operator symbols and method names is as follows: `x<y` calls `x.__lt__(y)`,
    `x<=y` calls `x.__le__(y)`, `x==y` calls `x.__eq__(y)`, `x!=y` calls
    `x.__ne__(y)`, `x>y` calls `x.__gt__(y)`, and `x>=y` calls
    `x.__ge__(y)`.

    A rich comparison method may return the singleton [`NotImplemented`](../library/constants.html#NotImplemented "NotImplemented") if it does
    not implement the operation for a given pair of arguments. By convention,
    `False` and `True` are returned for a successful comparison. However, these
    methods can return any value, so if the comparison operator is used in a Boolean
    context (e.g., in the condition of an `if` statement), Python will call
    [`bool()`](../library/functions.html#bool "bool") on the value to determine if the result is true or false.

    By default, `object` implements [`__eq__()`](#object.__eq__ "object.__eq__") by using `is`, returning
    [`NotImplemented`](../library/constants.html#NotImplemented "NotImplemented") in the case of a false comparison:
    `True if x is y else NotImplemented`. For [`__ne__()`](#object.__ne__ "object.__ne__"), by default it
    delegates to [`__eq__()`](#object.__eq__ "object.__eq__") and inverts the result unless it is
    `NotImplemented`. There are no other implied relationships among the
    comparison operators or default implementations; for example, the truth of
    `(x<y or x==y)` does not imply `x<=y`. To automatically generate ordering
    operations from a single root operation, see [`functools.total_ordering()`](../library/functools.html#functools.total_ordering "functools.total_ordering").

    By default, the [`object`](../library/functions.html#object "object") class provides implementations consistent
    with [Value comparisons](expressions.html#expressions-value-comparisons): equality compares according to
    object identity, and order comparisons raise [`TypeError`](../library/exceptions.html#TypeError "TypeError"). Each default
    method may generate these results directly, but may also return
    [`NotImplemented`](../library/constants.html#NotImplemented "NotImplemented").

    See the paragraph on [`__hash__()`](#object.__hash__ "object.__hash__") for
    some important notes on creating [hashable](../glossary.html#term-hashable) objects which support
    custom comparison operations and are usable as dictionary keys.

    There are no swapped-argument versions of these methods (to be used when the
    left argument does not support the operation but the right argument does);
    rather, [`__lt__()`](#object.__lt__ "object.__lt__") and [`__gt__()`](#object.__gt__ "object.__gt__") are each otherâs reflection,
    [`__le__()`](#object.__le__ "object.__le__") and [`__ge__()`](#object.__ge__ "object.__ge__") are each otherâs reflection, and
    [`__eq__()`](#object.__eq__ "object.__eq__") and [`__ne__()`](#object.__ne__ "object.__ne__") are their own reflection.
    If the operands are of different types, and the right operandâs type is
    a direct or indirect subclass of the left operandâs type,
    the reflected method of the right operand has priority, otherwise
    the left operandâs method has priority. Virtual subclassing is
    not considered.

    When no appropriate method returns any value other than [`NotImplemented`](../library/constants.html#NotImplemented "NotImplemented"), the
    `==` and `!=` operators will fall back to `is` and `is not`, respectively.

object.\_\_hash\_\_(*self*)
:   Called by built-in function [`hash()`](../library/functions.html#hash "hash") and for operations on members of
    hashed collections including [`set`](../library/stdtypes.html#set "set"), [`frozenset`](../library/stdtypes.html#frozenset "frozenset"), and
    [`dict`](../library/stdtypes.html#dict "dict"). The `__hash__()` method should return an integer. The only required
    property is that objects which compare equal have the same hash value; it is
    advised to mix together the hash values of the components of the object that
    also play a part in comparison of objects by packing them into a tuple and
    hashing the tuple. Example:

    ```
    def __hash__(self):
        return hash((self.name, self.nick, self.color))
    ```

    Note

    [`hash()`](../library/functions.html#hash "hash") truncates the value returned from an objectâs custom
    [`__hash__()`](#object.__hash__ "object.__hash__") method to the size of a [`Py_ssize_t`](../c-api/intro.html#c.Py_ssize_t "Py_ssize_t"). This is
    typically 8 bytes on 64-bit builds and 4 bytes on 32-bit builds. If an
    objectâs [`__hash__()`](#object.__hash__ "object.__hash__") must interoperate on builds of different bit
    sizes, be sure to check the width on all supported builds. An easy way
    to do this is with
    `python -c "import sys; print(sys.hash_info.width)"`.

    If a class does not define an [`__eq__()`](#object.__eq__ "object.__eq__") method it should not define a
    [`__hash__()`](#object.__hash__ "object.__hash__") operation either; if it defines [`__eq__()`](#object.__eq__ "object.__eq__") but not
    [`__hash__()`](#object.__hash__ "object.__hash__"), its instances will not be usable as items in hashable
    collections. If a class defines mutable objects and implements an
    [`__eq__()`](#object.__eq__ "object.__eq__") method, it should not implement [`__hash__()`](#object.__hash__ "object.__hash__"), since the
    implementation of [hashable](../glossary.html#term-hashable) collections requires that a keyâs hash value is
    immutable (if the objectâs hash value changes, it will be in the wrong hash
    bucket).

    User-defined classes have [`__eq__()`](#object.__eq__ "object.__eq__") and [`__hash__()`](#object.__hash__ "object.__hash__") methods
    by default (inherited from the [`object`](../library/functions.html#object "object") class); with them, all objects compare
    unequal (except with themselves) and `x.__hash__()` returns an appropriate
    value such that `x == y` implies both that `x is y` and `hash(x) == hash(y)`.

    A class that overrides [`__eq__()`](#object.__eq__ "object.__eq__") and does not define [`__hash__()`](#object.__hash__ "object.__hash__")
    will have its [`__hash__()`](#object.__hash__ "object.__hash__") implicitly set to `None`. When the
    [`__hash__()`](#object.__hash__ "object.__hash__") method of a class is `None`, instances of the class will
    raise an appropriate [`TypeError`](../library/exceptions.html#TypeError "TypeError") when a program attempts to retrieve
    their hash value, and will also be correctly identified as unhashable when
    checking `isinstance(obj, collections.abc.Hashable)`.

    If a class that overrides [`__eq__()`](#object.__eq__ "object.__eq__") needs to retain the implementation
    of [`__hash__()`](#object.__hash__ "object.__hash__") from a parent class, the interpreter must be told this
    explicitly by setting `__hash__ = <ParentClass>.__hash__`.

    If a class that does not override [`__eq__()`](#object.__eq__ "object.__eq__") wishes to suppress hash
    support, it should include `__hash__ = None` in the class definition.
    A class which defines its own [`__hash__()`](#object.__hash__ "object.__hash__") that explicitly raises
    a [`TypeError`](../library/exceptions.html#TypeError "TypeError") would be incorrectly identified as hashable by
    an `isinstance(obj, collections.abc.Hashable)` call.

    Note

    By default, the [`__hash__()`](#object.__hash__ "object.__hash__") values of str and bytes objects are
    âsaltedâ with an unpredictable random value. Although they
    remain constant within an individual Python process, they are not
    predictable between repeated invocations of Python.

    This is intended to provide protection against a denial-of-service caused
    by carefully chosen inputs that exploit the worst case performance of a
    dict insertion, *O*(*n*2) complexity. See
    <http://ocert.org/advisories/ocert-2011-003.html> for details.

    Changing hash values affects the iteration order of sets.
    Python has never made guarantees about this ordering
    (and it typically varies between 32-bit and 64-bit builds).

    See also [`PYTHONHASHSEED`](../using/cmdline.html#envvar-PYTHONHASHSEED).

    Changed in version 3.3: Hash randomization is enabled by default.

object.\_\_bool\_\_(*self*)
:   Called to implement truth value testing and the built-in operation
    `bool()`; should return `False` or `True`. When this method is not
    defined, [`__len__()`](#object.__len__ "object.__len__") is called, if it is defined, and the object is
    considered true if its result is nonzero. If a class defines neither
    `__len__()` nor `__bool__()` (which is true of the [`object`](../library/functions.html#object "object")
    class itself), all its instances are considered true.

### 3.3.2. Customizing attribute access

The following methods can be defined to customize the meaning of attribute
access (use of, assignment to, or deletion of `x.name`) for class instances.

object.\_\_getattr\_\_(*self*, *name*)
:   Called when the default attribute access fails with an [`AttributeError`](../library/exceptions.html#AttributeError "AttributeError")
    (either [`__getattribute__()`](#object.__getattribute__ "object.__getattribute__") raises an [`AttributeError`](../library/exceptions.html#AttributeError "AttributeError") because
    *name* is not an instance attribute or an attribute in the class tree
    for `self`; or [`__get__()`](#object.__get__ "object.__get__") of a *name* property raises
    [`AttributeError`](../library/exceptions.html#AttributeError "AttributeError")). This method should either return the (computed)
    attribute value or raise an [`AttributeError`](../library/exceptions.html#AttributeError "AttributeError") exception.
    The [`object`](../library/functions.html#object "object") class itself does not provide this method.

    Note that if the attribute is found through the normal mechanism,
    [`__getattr__()`](#object.__getattr__ "object.__getattr__") is not called. (This is an intentional asymmetry between
    [`__getattr__()`](#object.__getattr__ "object.__getattr__") and [`__setattr__()`](#object.__setattr__ "object.__setattr__").) This is done both for efficiency
    reasons and because otherwise [`__getattr__()`](#object.__getattr__ "object.__getattr__") would have no way to access
    other attributes of the instance. Note that at least for instance variables,
    you can take total control by not inserting any values in the instance attribute
    dictionary (but instead inserting them in another object). See the
    [`__getattribute__()`](#object.__getattribute__ "object.__getattribute__") method below for a way to actually get total control
    over attribute access.

object.\_\_getattribute\_\_(*self*, *name*)
:   Called unconditionally to implement attribute accesses for instances of the
    class. If the class also defines [`__getattr__()`](#object.__getattr__ "object.__getattr__"), the latter will not be
    called unless [`__getattribute__()`](#object.__getattribute__ "object.__getattribute__") either calls it explicitly or raises an
    [`AttributeError`](../library/exceptions.html#AttributeError "AttributeError"). This method should return the (computed) attribute value
    or raise an [`AttributeError`](../library/exceptions.html#AttributeError "AttributeError") exception. In order to avoid infinite
    recursion in this method, its implementation should always call the base class
    method with the same name to access any attributes it needs, for example,
    `object.__getattribute__(self, name)`.

    For certain sensitive attribute accesses, raises an
    [auditing event](../library/sys.html#auditing) `object.__getattr__` with arguments
    `obj` and `name`.

object.\_\_setattr\_\_(*self*, *name*, *value*)
:   Called when an attribute assignment is attempted. This is called instead of
    the normal mechanism (i.e. store the value in the instance dictionary).
    *name* is the attribute name, *value* is the value to be assigned to it.

    If [`__setattr__()`](#object.__setattr__ "object.__setattr__") wants to assign to an instance attribute, it should
    call the base class method with the same name, for example,
    `object.__setattr__(self, name, value)`.

    For certain sensitive attribute assignments, raises an
    [auditing event](../library/sys.html#auditing) `object.__setattr__` with arguments
    `obj`, `name`, `value`.

object.\_\_delattr\_\_(*self*, *name*)
:   Like [`__setattr__()`](#object.__setattr__ "object.__setattr__") but for attribute deletion instead of assignment. This
    should only be implemented if `del obj.name` is meaningful for the object.

    For certain sensitive attribute deletions, raises an
    [auditing event](../library/sys.html#auditing) `object.__delattr__` with arguments
    `obj` and `name`.

object.\_\_dir\_\_(*self*)
:   Called when [`dir()`](../library/functions.html#dir "dir") is called on the object. An iterable must be
    returned. [`dir()`](../library/functions.html#dir "dir") converts the returned iterable to a list and sorts it.

#### 3.3.2.1. Customizing module attribute access

Special names `__getattr__` and `__dir__` can be also used to customize
access to module attributes. The `__getattr__` function at the module level
should accept one argument which is the name of an attribute and return the
computed value or raise an [`AttributeError`](../library/exceptions.html#AttributeError "AttributeError"). If an attribute is
not found on a module object through the normal lookup, i.e.
[`object.__getattribute__()`](#object.__getattribute__ "object.__getattribute__"), then `__getattr__` is searched in
the module `__dict__` before raising an [`AttributeError`](../library/exceptions.html#AttributeError "AttributeError"). If found,
it is called with the attribute name and the result is returned.

The `__dir__` function should accept no arguments, and return an iterable of
strings that represents the names accessible on module. If present, this
function overrides the standard [`dir()`](../library/functions.html#dir "dir") search on a module.

For a more fine grained customization of the module behavior (setting
attributes, properties, etc.), one can set the `__class__` attribute of
a module object to a subclass of [`types.ModuleType`](../library/types.html#types.ModuleType "types.ModuleType"). For example:

```
import sys
from types import ModuleType

class VerboseModule(ModuleType):
    def __repr__(self):
        return f'Verbose {self.__name__}'

    def __setattr__(self, attr, value):
        print(f'Setting {attr}...')
        super().__setattr__(attr, value)

sys.modules[__name__].__class__ = VerboseModule
```

Note

Defining module `__getattr__` and setting module `__class__` only
affect lookups made using the attribute access syntax â directly accessing
the module globals (whether by code within the module, or via a reference
to the moduleâs globals dictionary) is unaffected.

Changed in version 3.5: `__class__` module attribute is now writable.

Added in version 3.7: `__getattr__` and `__dir__` module attributes.

See also

[**PEP 562**](https://peps.python.org/pep-0562/) - Module \_\_getattr\_\_ and \_\_dir\_\_
:   Describes the `__getattr__` and `__dir__` functions on modules.

#### 3.3.2.2. Implementing Descriptors

The following methods only apply when an instance of the class containing the
method (a so-called *descriptor* class) appears in an *owner* class (the
descriptor must be in either the ownerâs class dictionary or in the class
dictionary for one of its parents). In the examples below, âthe attributeâ
refers to the attribute whose name is the key of the property in the owner
classâ [`__dict__`](#object.__dict__ "object.__dict__"). The [`object`](../library/functions.html#object "object") class itself does not
implement any of these protocols.

object.\_\_get\_\_(*self*, *instance*, *owner=None*)
:   Called to get the attribute of the owner class (class attribute access) or
    of an instance of that class (instance attribute access). The optional
    *owner* argument is the owner class, while *instance* is the instance that
    the attribute was accessed through, or `None` when the attribute is
    accessed through the *owner*.

    This method should return the computed attribute value or raise an
    [`AttributeError`](../library/exceptions.html#AttributeError "AttributeError") exception.

    [**PEP 252**](https://peps.python.org/pep-0252/) specifies that [`__get__()`](#object.__get__ "object.__get__") is callable with one or two
    arguments. Pythonâs own built-in descriptors support this specification;
    however, it is likely that some third-party tools have descriptors
    that require both arguments. Pythonâs own [`__getattribute__()`](#object.__getattribute__ "object.__getattribute__")
    implementation always passes in both arguments whether they are required
    or not.

object.\_\_set\_\_(*self*, *instance*, *value*)
:   Called to set the attribute on an instance *instance* of the owner class to a
    new value, *value*.

    Note, adding [`__set__()`](#object.__set__ "object.__set__") or [`__delete__()`](#object.__delete__ "object.__delete__") changes the kind of
    descriptor to a âdata descriptorâ. See [Invoking Descriptors](#descriptor-invocation) for
    more details.

object.\_\_delete\_\_(*self*, *instance*)
:   Called to delete the attribute on an instance *instance* of the owner class.

Instances of descriptors may also have the `__objclass__` attribute
present:

object.\_\_objclass\_\_
:   The attribute `__objclass__` is interpreted by the [`inspect`](../library/inspect.html#module-inspect "inspect: Extract information and source code from live objects.") module
    as specifying the class where this object was defined (setting this
    appropriately can assist in runtime introspection of dynamic class attributes).
    For callables, it may indicate that an instance of the given type (or a
    subclass) is expected or required as the first positional argument (for example,
    CPython sets this attribute for unbound methods that are implemented in C).

#### 3.3.2.3. Invoking Descriptors

In general, a descriptor is an object attribute with âbinding behaviorâ, one
whose attribute access has been overridden by methods in the descriptor
protocol: [`__get__()`](#object.__get__ "object.__get__"), [`__set__()`](#object.__set__ "object.__set__"), and
[`__delete__()`](#object.__delete__ "object.__delete__"). If any of
those methods are defined for an object, it is said to be a descriptor.

The default behavior for attribute access is to get, set, or delete the
attribute from an objectâs dictionary. For instance, `a.x` has a lookup chain
starting with `a.__dict__['x']`, then `type(a).__dict__['x']`, and
continuing through the base classes of `type(a)` excluding metaclasses.

However, if the looked-up value is an object defining one of the descriptor
methods, then Python may override the default behavior and invoke the descriptor
method instead. Where this occurs in the precedence chain depends on which
descriptor methods were defined and how they were called.

The starting point for descriptor invocation is a binding, `a.x`. How the
arguments are assembled depends on `a`:

Direct Call
:   The simplest and least common call is when user code directly invokes a
    descriptor method: `x.__get__(a)`.

Instance Binding
:   If binding to an object instance, `a.x` is transformed into the call:
    `type(a).__dict__['x'].__get__(a, type(a))`.

Class Binding
:   If binding to a class, `A.x` is transformed into the call:
    `A.__dict__['x'].__get__(None, A)`.

Super Binding
:   A dotted lookup such as `super(A, a).x` searches
    `a.__class__.__mro__` for a base class `B` following `A` and then
    returns `B.__dict__['x'].__get__(a, A)`. If not a descriptor, `x` is
    returned unchanged.

For instance bindings, the precedence of descriptor invocation depends on
which descriptor methods are defined. A descriptor can define any combination
of [`__get__()`](#object.__get__ "object.__get__"), [`__set__()`](#object.__set__ "object.__set__") and
[`__delete__()`](#object.__delete__ "object.__delete__"). If it does not
define `__get__()`, then accessing the attribute will return the descriptor
object itself unless there is a value in the objectâs instance dictionary. If
the descriptor defines `__set__()` and/or `__delete__()`, it is a data
descriptor; if it defines neither, it is a non-data descriptor. Normally, data
descriptors define both `__get__()` and `__set__()`, while non-data
descriptors have just the `__get__()` method. Data descriptors with
`__get__()` and `__set__()` (and/or `__delete__()`) defined
always override a redefinition in an
instance dictionary. In contrast, non-data descriptors can be overridden by
instances.

Python methods (including those decorated with
[`@staticmethod`](../library/functions.html#staticmethod "staticmethod") and [`@classmethod`](../library/functions.html#classmethod "classmethod")) are
implemented as non-data descriptors. Accordingly, instances can redefine and
override methods. This allows individual instances to acquire behaviors that
differ from other instances of the same class.

The [`property()`](../library/functions.html#property "property") function is implemented as a data descriptor. Accordingly,
instances cannot override the behavior of a property.

#### 3.3.2.4. \_\_slots\_\_

*\_\_slots\_\_* allow us to explicitly declare data members (like
properties) and deny the creation of [`__dict__`](#object.__dict__ "object.__dict__") and *\_\_weakref\_\_*
(unless explicitly declared in *\_\_slots\_\_* or available in a parent.)

The space saved over using [`__dict__`](#object.__dict__ "object.__dict__") can be significant.
Attribute lookup speed can be significantly improved as well.

object.\_\_slots\_\_
:   This class variable can be assigned a string, iterable, or sequence of
    strings with variable names used by instances. *\_\_slots\_\_* reserves space
    for the declared variables and prevents the automatic creation of
    [`__dict__`](#object.__dict__ "object.__dict__")
    and *\_\_weakref\_\_* for each instance.

Notes on using *\_\_slots\_\_*:

* When inheriting from a class without *\_\_slots\_\_*, the
  [`__dict__`](#object.__dict__ "object.__dict__") and
  *\_\_weakref\_\_* attribute of the instances will always be accessible.
* Without a [`__dict__`](#object.__dict__ "object.__dict__") variable, instances cannot be assigned new
  variables not
  listed in the *\_\_slots\_\_* definition. Attempts to assign to an unlisted
  variable name raises [`AttributeError`](../library/exceptions.html#AttributeError "AttributeError"). If dynamic assignment of new
  variables is desired, then add `'__dict__'` to the sequence of strings in
  the *\_\_slots\_\_* declaration.
* Without a *\_\_weakref\_\_* variable for each instance, classes defining
  *\_\_slots\_\_* do not support [`weak references`](../library/weakref.html#module-weakref "weakref: Support for weak references and weak dictionaries.") to its instances.
  If weak reference
  support is needed, then add `'__weakref__'` to the sequence of strings in the
  *\_\_slots\_\_* declaration.
* *\_\_slots\_\_* are implemented at the class level by creating [descriptors](#descriptors)
  for each variable name. As a result, class attributes
  cannot be used to set default values for instance variables defined by
  *\_\_slots\_\_*; otherwise, the class attribute would overwrite the descriptor
  assignment.
* The action of a *\_\_slots\_\_* declaration is not limited to the class
  where it is defined. *\_\_slots\_\_* declared in parents are available in
  child classes. However, instances of a child subclass will get a
  [`__dict__`](#object.__dict__ "object.__dict__") and *\_\_weakref\_\_* unless the subclass also defines
  *\_\_slots\_\_* (which should only contain names of any *additional* slots).
* If a class defines a slot also defined in a base class, the instance variable
  defined by the base class slot is inaccessible (except by retrieving its
  descriptor directly from the base class). This renders the meaning of the
  program undefined. In the future, a check may be added to prevent this.
* [`TypeError`](../library/exceptions.html#TypeError "TypeError") will be raised if nonempty *\_\_slots\_\_* are defined for a
  class derived from a
  [`"variable-length" built-in type`](../c-api/typeobj.html#c.PyTypeObject.tp_itemsize "PyTypeObject.tp_itemsize") such as
  [`int`](../library/functions.html#int "int"), [`bytes`](../library/stdtypes.html#bytes "bytes"), and [`tuple`](../library/stdtypes.html#tuple "tuple").
* Any non-string [iterable](../glossary.html#term-iterable) may be assigned to *\_\_slots\_\_*.
* If a [`dictionary`](../library/stdtypes.html#dict "dict") is used to assign *\_\_slots\_\_*, the dictionary
  keys will be used as the slot names. The values of the dictionary can be used
  to provide per-attribute docstrings that will be recognised by
  [`inspect.getdoc()`](../library/inspect.html#inspect.getdoc "inspect.getdoc") and displayed in the output of [`help()`](../library/functions.html#help "help").
* [`__class__`](#object.__class__ "object.__class__") assignment works only if both classes have the
  same *\_\_slots\_\_*.
* [Multiple inheritance](../tutorial/classes.html#tut-multiple) with multiple slotted parent
  classes can be used,
  but only one parent is allowed to have attributes created by slots
  (the other bases must have empty slot layouts) - violations raise
  [`TypeError`](../library/exceptions.html#TypeError "TypeError").
* If an [iterator](../glossary.html#term-iterator) is used for *\_\_slots\_\_* then a [descriptor](../glossary.html#term-descriptor) is
  created for each
  of the iteratorâs values. However, the *\_\_slots\_\_* attribute will be an empty
  iterator.

### 3.3.3. Customizing class creation

Whenever a class inherits from another class, [`__init_subclass__()`](#object.__init_subclass__ "object.__init_subclass__") is
called on the parent class. This way, it is possible to write classes which
change the behavior of subclasses. This is closely related to class
decorators, but where class decorators only affect the specific class theyâre
applied to, `__init_subclass__` solely applies to future subclasses of the
class defining the method.

*classmethod* object.\_\_init\_subclass\_\_(*cls*)
:   This method is called whenever the containing class is subclassed.
    *cls* is then the new subclass. If defined as a normal instance method,
    this method is implicitly converted to a class method.

    Keyword arguments which are given to a new class are passed to
    the parent classâs `__init_subclass__`. For compatibility with
    other classes using `__init_subclass__`, one should take out the
    needed keyword arguments and pass the others over to the base
    class, as in:

    ```
    class Philosopher:
        def __init_subclass__(cls, /, default_name, **kwargs):
            super().__init_subclass__(**kwargs)
            cls.default_name = default_name

    class AustralianPhilosopher(Philosopher, default_name="Bruce"):
        pass
    ```

    The default implementation `object.__init_subclass__` does
    nothing, but raises an error if it is called with any arguments.

    Note

    The metaclass hint `metaclass` is consumed by the rest of the type
    machinery, and is never passed to `__init_subclass__` implementations.
    The actual metaclass (rather than the explicit hint) can be accessed as
    `type(cls)`.

When a class is created, `type.__new__()` scans the class variables
and makes callbacks to those with a [`__set_name__()`](#object.__set_name__ "object.__set_name__") hook.

object.\_\_set\_name\_\_(*self*, *owner*, *name*)
:   Automatically called at the time the owning class *owner* is
    created. The object has been assigned to *name* in that class:

    ```
    class A:
        x = C()  # Automatically calls: x.__set_name__(A, 'x')
    ```

    If the class variable is assigned after the class is created,
    [`__set_name__()`](#object.__set_name__ "object.__set_name__") will not be called automatically.
    If needed, [`__set_name__()`](#object.__set_name__ "object.__set_name__") can be called directly:

    ```
    class A:
       pass

    c = C()
    A.x = c                  # The hook is not called
    c.__set_name__(A, 'x')   # Manually invoke the hook
    ```

    See [Creating the class object](#class-object-creation) for more details.

#### 3.3.3.2. Resolving MRO entries

object.\_\_mro\_entries\_\_(*self*, *bases*)
:   If a base that appears in a class definition is not an instance of
    [`type`](../library/functions.html#type "type"), then an `__mro_entries__()` method is searched on the base.
    If an `__mro_entries__()` method is found, the base is substituted with the
    result of a call to `__mro_entries__()` when creating the class.
    The method is called with the original bases tuple
    passed to the *bases* parameter, and must return a tuple
    of classes that will be used instead of the base. The returned tuple may be
    empty: in these cases, the original base is ignored.

#### 3.3.3.4. Preparing the class namespace

Once the appropriate metaclass has been identified, then the class namespace
is prepared. If the metaclass has a `__prepare__` attribute, it is called
as `namespace = metaclass.__prepare__(name, bases, **kwds)` (where the
additional keyword arguments, if any, come from the class definition). The
`__prepare__` method should be implemented as a
[`classmethod`](../library/functions.html#classmethod "classmethod"). The
namespace returned by `__prepare__` is passed in to `__new__`, but when
the final class object is created the namespace is copied into a new `dict`.

If the metaclass has no `__prepare__` attribute, then the class namespace
is initialised as an empty ordered mapping.

See also

[**PEP 3115**](https://peps.python.org/pep-3115/) - Metaclasses in Python 3000
:   Introduced the `__prepare__` namespace hook

#### 3.3.3.5. Executing the class body

The class body is executed (approximately) as
`exec(body, globals(), namespace)`. The key difference from a normal
call to [`exec()`](../library/functions.html#exec "exec") is that lexical scoping allows the class body (including
any methods) to reference names from the current and outer scopes when the
class definition occurs inside a function.

However, even when the class definition occurs inside the function, methods
defined inside the class still cannot see names defined at the class scope.
Class variables must be accessed through the first parameter of instance or
class methods, or through the implicit lexically scoped `__class__` reference
described in the next section.

#### 3.3.3.6. Creating the class object

Once the class namespace has been populated by executing the class body,
the class object is created by calling
`metaclass(name, bases, namespace, **kwds)` (the additional keywords
passed here are the same as those passed to `__prepare__`).

This class object is the one that will be referenced by the zero-argument
form of [`super()`](../library/functions.html#super "super"). `__class__` is an implicit closure reference
created by the compiler if any methods in a class body refer to either
`__class__` or `super`. This allows the zero argument form of
[`super()`](../library/functions.html#super "super") to correctly identify the class being defined based on
lexical scoping, while the class or instance that was used to make the
current call is identified based on the first argument passed to the method.

**CPython implementation detail:** In CPython 3.6 and later, the `__class__` cell is passed to the metaclass
as a `__classcell__` entry in the class namespace. If present, this must
be propagated up to the `type.__new__` call in order for the class to be
initialised correctly.
Failing to do so will result in a [`RuntimeError`](../library/exceptions.html#RuntimeError "RuntimeError") in Python 3.8.

When using the default metaclass [`type`](../library/functions.html#type "type"), or any metaclass that ultimately
calls `type.__new__`, the following additional customization steps are
invoked after creating the class object:

1. The `type.__new__` method collects all of the attributes in the class
   namespace that define a [`__set_name__()`](#object.__set_name__ "object.__set_name__") method;
2. Those `__set_name__` methods are called with the class
   being defined and the assigned name of that particular attribute;
3. The [`__init_subclass__()`](#object.__init_subclass__ "object.__init_subclass__") hook is called on the
   immediate parent of the new class in its method resolution order.

After the class object is created, it is passed to the class decorators
included in the class definition (if any) and the resulting object is bound
in the local namespace as the defined class.

When a new class is created by `type.__new__`, the object provided as the
namespace parameter is copied to a new ordered mapping and the original
object is discarded. The new copy is wrapped in a read-only proxy, which
becomes the [`__dict__`](#type.__dict__ "type.__dict__") attribute of the class object.

See also

[**PEP 3135**](https://peps.python.org/pep-3135/) - New super
:   Describes the implicit `__class__` closure reference

### 3.3.4. Customizing instance and subclass checks

The following methods are used to override the default behavior of the
[`isinstance()`](../library/functions.html#isinstance "isinstance") and [`issubclass()`](../library/functions.html#issubclass "issubclass") built-in functions.

In particular, the metaclass [`abc.ABCMeta`](../library/abc.html#abc.ABCMeta "abc.ABCMeta") implements these methods in
order to allow the addition of Abstract Base Classes (ABCs) as âvirtual base
classesâ to any class or type (including built-in types), including other
ABCs.

type.\_\_instancecheck\_\_(*self*, *instance*)
:   Return true if *instance* should be considered a (direct or indirect)
    instance of *class*. If defined, called to implement `isinstance(instance,
    class)`.

type.\_\_subclasscheck\_\_(*self*, *subclass*)
:   Return true if *subclass* should be considered a (direct or indirect)
    subclass of *class*. If defined, called to implement `issubclass(subclass,
    class)`.

Note that these methods are looked up on the type (metaclass) of a class. They
cannot be defined as class methods in the actual class. This is consistent with
the lookup of special methods that are called on instances, only in this
case the instance is itself a class.

### 3.3.5. Emulating generic types

When using [type annotations](../glossary.html#term-annotation), it is often useful to
*parameterize* a [generic type](../glossary.html#term-generic-type) using Pythonâs square-brackets notation.
For example, the annotation `list[int]` might be used to signify a
[`list`](../library/stdtypes.html#list "list") in which all the elements are of type [`int`](../library/functions.html#int "int").

See also

[**PEP 484**](https://peps.python.org/pep-0484/) - Type Hints
:   Introducing Pythonâs framework for type annotations

[Generic Alias Types](../library/stdtypes.html#types-genericalias)
:   Documentation for objects representing parameterized generic classes

[Generics](../library/typing.html#generics), [user-defined generics](../library/typing.html#user-defined-generics) and [`typing.Generic`](../library/typing.html#typing.Generic "typing.Generic")
:   Documentation on how to implement generic classes that can be
    parameterized at runtime and understood by static type-checkers.

A class can *generally* only be parameterized if it defines the special
class method `__class_getitem__()`.

*classmethod* object.\_\_class\_getitem\_\_(*cls*, *key*)
:   Return an object representing the specialization of a generic class
    by type arguments found in *key*.

    When defined on a class, `__class_getitem__()` is automatically a class
    method. As such, there is no need for it to be decorated with
    [`@classmethod`](../library/functions.html#classmethod "classmethod") when it is defined.

#### 3.3.5.1. The purpose of *\_\_class\_getitem\_\_*

The purpose of [`__class_getitem__()`](#object.__class_getitem__ "object.__class_getitem__") is to allow runtime
parameterization of standard-library generic classes in order to more easily
apply [type hints](../glossary.html#term-type-hint) to these classes.

To implement custom generic classes that can be parameterized at runtime and
understood by static type-checkers, users should either inherit from a standard
library class that already implements [`__class_getitem__()`](#object.__class_getitem__ "object.__class_getitem__"), or
inherit from [`typing.Generic`](../library/typing.html#typing.Generic "typing.Generic"), which has its own implementation of
`__class_getitem__()`.

Custom implementations of [`__class_getitem__()`](#object.__class_getitem__ "object.__class_getitem__") on classes defined
outside of the standard library may not be understood by third-party
type-checkers such as mypy. Using `__class_getitem__()` on any class for
purposes other than type hinting is discouraged.

#### 3.3.5.2. *\_\_class\_getitem\_\_* versus *\_\_getitem\_\_*

Usually, the [subscription](expressions.html#subscriptions) of an object using square
brackets will call the [`__getitem__()`](#object.__getitem__ "object.__getitem__") instance method defined on
the objectâs class. However, if the object being subscribed is itself a class,
the class method [`__class_getitem__()`](#object.__class_getitem__ "object.__class_getitem__") may be called instead.
`__class_getitem__()` should return a [GenericAlias](../library/stdtypes.html#types-genericalias)
object if it is properly defined.

Presented with the [expression](../glossary.html#term-expression) `obj[x]`, the Python interpreter
follows something like the following process to decide whether
[`__getitem__()`](#object.__getitem__ "object.__getitem__") or [`__class_getitem__()`](#object.__class_getitem__ "object.__class_getitem__") should be
called:

```
from inspect import isclass

def subscribe(obj, x):
    """Return the result of the expression 'obj[x]'"""

    class_of_obj = type(obj)

    # If the class of obj defines __getitem__,
    # call class_of_obj.__getitem__(obj, x)
    if hasattr(class_of_obj, '__getitem__'):
        return class_of_obj.__getitem__(obj, x)

    # Else, if obj is a class and defines __class_getitem__,
    # call obj.__class_getitem__(x)
    elif isclass(obj) and hasattr(obj, '__class_getitem__'):
        return obj.__class_getitem__(x)

    # Else, raise an exception
    else:
        raise TypeError(
            f"'{class_of_obj.__name__}' object is not subscriptable"
        )
```

In Python, all classes are themselves instances of other classes. The class of
a class is known as that classâs [metaclass](../glossary.html#term-metaclass), and most classes have the
[`type`](../library/functions.html#type "type") class as their metaclass. [`type`](../library/functions.html#type "type") does not define
[`__getitem__()`](#object.__getitem__ "object.__getitem__"), meaning that expressions such as `list[int]`,
`dict[str, float]` and `tuple[str, bytes]` all result in
[`__class_getitem__()`](#object.__class_getitem__ "object.__class_getitem__") being called:

```
>>> # list has class "type" as its metaclass, like most classes:
>>> type(list)
<class 'type'>
>>> type(dict) == type(list) == type(tuple) == type(str) == type(bytes)
True
>>> # "list[int]" calls "list.__class_getitem__(int)"
>>> list[int]
list[int]
>>> # list.__class_getitem__ returns a GenericAlias object:
>>> type(list[int])
<class 'types.GenericAlias'>
```

However, if a class has a custom metaclass that defines
[`__getitem__()`](#object.__getitem__ "object.__getitem__"), subscribing the class may result in different
behaviour. An example of this can be found in the [`enum`](../library/enum.html#module-enum "enum: Implementation of an enumeration class.") module:

```
>>> from enum import Enum
>>> class Menu(Enum):
...     """A breakfast menu"""
...     SPAM = 'spam'
...     BACON = 'bacon'
...
>>> # Enum classes have a custom metaclass:
>>> type(Menu)
<class 'enum.EnumMeta'>
>>> # EnumMeta defines __getitem__,
>>> # so __class_getitem__ is not called,
>>> # and the result is not a GenericAlias object:
>>> Menu['SPAM']
<Menu.SPAM: 'spam'>
>>> type(Menu['SPAM'])
<enum 'Menu'>
```

### 3.3.6. Emulating callable objects

object.\_\_call\_\_(*self*[, *args...*])
:   Called when the instance is âcalledâ as a function; if this method is defined,
    `x(arg1, arg2, ...)` roughly translates to `type(x).__call__(x, arg1, ...)`.
    The [`object`](../library/functions.html#object "object") class itself does not provide this method.

### 3.3.7. Emulating container types

The following methods can be defined to implement container objects. None of them
are provided by the [`object`](../library/functions.html#object "object") class itself. Containers usually are
[sequences](../glossary.html#term-sequence) (such as [`lists`](../library/stdtypes.html#list "list") or
[`tuples`](../library/stdtypes.html#tuple "tuple")) or [mappings](../glossary.html#term-mapping) (like
[dictionaries](../glossary.html#term-dictionary)),
but can represent other containers as well. The first set of methods is used
either to emulate a sequence or to emulate a mapping; the difference is that for
a sequence, the allowable keys should be the integers *k* for which `0 <= k <
N` where *N* is the length of the sequence, or [`slice`](../library/functions.html#slice "slice") objects, which define a
range of items. It is also recommended that mappings provide the methods
`keys()`, `values()`, `items()`, `get()`, `clear()`,
`setdefault()`, `pop()`, `popitem()`, `copy()`, and
`update()` behaving similar to those for Pythonâs standard [`dictionary`](../library/stdtypes.html#dict "dict")
objects. The [`collections.abc`](../library/collections.abc.html#module-collections.abc "collections.abc: Abstract base classes for containers") module provides a
[`MutableMapping`](../library/collections.abc.html#collections.abc.MutableMapping "collections.abc.MutableMapping")
[abstract base class](../glossary.html#term-abstract-base-class) to help create those methods from a base set of
[`__getitem__()`](#object.__getitem__ "object.__getitem__"), [`__setitem__()`](#object.__setitem__ "object.__setitem__"),
[`__delitem__()`](#object.__delitem__ "object.__delitem__"), and `keys()`.
Mutable sequences should provide methods `append()`, `count()`,
`index()`, `extend()`, `insert()`, `pop()`, `remove()`,
`reverse()` and `sort()`, like Python standard [`list`](../library/stdtypes.html#list "list")
objects. Finally,
sequence types should implement addition (meaning concatenation) and
multiplication (meaning repetition) by defining the methods
[`__add__()`](#object.__add__ "object.__add__"), [`__radd__()`](#object.__radd__ "object.__radd__"), [`__iadd__()`](#object.__iadd__ "object.__iadd__"),
[`__mul__()`](#object.__mul__ "object.__mul__"), [`__rmul__()`](#object.__rmul__ "object.__rmul__") and [`__imul__()`](#object.__imul__ "object.__imul__")
described below; they should not define other numerical
operators. It is recommended that both mappings and sequences implement the
[`__contains__()`](#object.__contains__ "object.__contains__") method to allow efficient use of the `in`
operator; for
mappings, `in` should search the mappingâs keys; for sequences, it should
search through the values. It is further recommended that both mappings and
sequences implement the [`__iter__()`](#object.__iter__ "object.__iter__") method to allow efficient iteration
through the container; for mappings, `__iter__()` should iterate
through the objectâs keys; for sequences, it should iterate through the values.

object.\_\_len\_\_(*self*)
:   Called to implement the built-in function [`len()`](../library/functions.html#len "len"). Should return the length
    of the object, an integer `>=` 0. Also, an object that doesnât define a
    [`__bool__()`](#object.__bool__ "object.__bool__") method and whose `__len__()` method returns zero is
    considered to be false in a Boolean context.

    **CPython implementation detail:** In CPython, the length is required to be at most [`sys.maxsize`](../library/sys.html#sys.maxsize "sys.maxsize").
    If the length is larger than `sys.maxsize` some features (such as
    [`len()`](../library/functions.html#len "len")) may raise [`OverflowError`](../library/exceptions.html#OverflowError "OverflowError"). To prevent raising
    `OverflowError` by truth value testing, an object must define a
    [`__bool__()`](#object.__bool__ "object.__bool__") method.

object.\_\_length\_hint\_\_(*self*)
:   Called to implement [`operator.length_hint()`](../library/operator.html#operator.length_hint "operator.length_hint"). Should return an estimated
    length for the object (which may be greater or less than the actual length).
    The length must be an integer `>=` 0. The return value may also be
    [`NotImplemented`](../library/constants.html#NotImplemented "NotImplemented"), which is treated the same as if the
    `__length_hint__` method didnât exist at all. This method is purely an
    optimization and is never required for correctness.

Note

Slicing is done exclusively with the following three methods. A call like

is translated to

and so forth. Missing slice items are always filled in with `None`.

object.\_\_getitem\_\_(*self*, *key*)
:   Called to implement evaluation of `self[key]`. For [sequence](../glossary.html#term-sequence) types,
    the accepted keys should be integers. Optionally, they may support
    [`slice`](../library/functions.html#slice "slice") objects as well. Negative index support is also optional.
    If *key* is
    of an inappropriate type, [`TypeError`](../library/exceptions.html#TypeError "TypeError") may be raised; if *key* is a value
    outside the set of indexes for the sequence (after any special
    interpretation of negative values), [`IndexError`](../library/exceptions.html#IndexError "IndexError") should be raised. For
    [mapping](../glossary.html#term-mapping) types, if *key* is missing (not in the container),
    [`KeyError`](../library/exceptions.html#KeyError "KeyError") should be raised.

    Note

    [`for`](compound_stmts.html#for) loops expect that an [`IndexError`](../library/exceptions.html#IndexError "IndexError") will be raised for
    illegal indexes to allow proper detection of the end of the sequence.

object.\_\_setitem\_\_(*self*, *key*, *value*)
:   Called to implement assignment to `self[key]`. Same note as for
    [`__getitem__()`](#object.__getitem__ "object.__getitem__"). This should only be implemented for mappings if the
    objects support changes to the values for keys, or if new keys can be added, or
    for sequences if elements can be replaced. The same exceptions should be raised
    for improper *key* values as for the [`__getitem__()`](#object.__getitem__ "object.__getitem__") method.

object.\_\_delitem\_\_(*self*, *key*)
:   Called to implement deletion of `self[key]`. Same note as for
    [`__getitem__()`](#object.__getitem__ "object.__getitem__"). This should only be implemented for mappings if the
    objects support removal of keys, or for sequences if elements can be removed
    from the sequence. The same exceptions should be raised for improper *key*
    values as for the [`__getitem__()`](#object.__getitem__ "object.__getitem__") method.

object.\_\_missing\_\_(*self*, *key*)
:   Called by [`dict`](../library/stdtypes.html#dict "dict").[`__getitem__()`](#object.__getitem__ "object.__getitem__") to implement `self[key]` for dict subclasses
    when key is not in the dictionary.

object.\_\_iter\_\_(*self*)
:   This method is called when an [iterator](../glossary.html#term-iterator) is required for a container.
    This method should return a new iterator object that can iterate over all the
    objects in the container. For mappings, it should iterate over the keys of
    the container.

object.\_\_reversed\_\_(*self*)
:   Called (if present) by the [`reversed()`](../library/functions.html#reversed "reversed") built-in to implement
    reverse iteration. It should return a new iterator object that iterates
    over all the objects in the container in reverse order.

    If the [`__reversed__()`](#object.__reversed__ "object.__reversed__") method is not provided, the [`reversed()`](../library/functions.html#reversed "reversed")
    built-in will fall back to using the sequence protocol ([`__len__()`](#object.__len__ "object.__len__") and
    [`__getitem__()`](#object.__getitem__ "object.__getitem__")). Objects that support the sequence protocol should
    only provide [`__reversed__()`](#object.__reversed__ "object.__reversed__") if they can provide an implementation
    that is more efficient than the one provided by [`reversed()`](../library/functions.html#reversed "reversed").

The membership test operators ([`in`](expressions.html#in) and [`not in`](expressions.html#not-in)) are normally
implemented as an iteration through a container. However, container objects can
supply the following special method with a more efficient implementation, which
also does not require the object be iterable.

object.\_\_contains\_\_(*self*, *item*)
:   Called to implement membership test operators. Should return true if *item*
    is in *self*, false otherwise. For mapping objects, this should consider the
    keys of the mapping rather than the values or the key-item pairs.

    For objects that donât define [`__contains__()`](#object.__contains__ "object.__contains__"), the membership test first
    tries iteration via [`__iter__()`](#object.__iter__ "object.__iter__"), then the old sequence iteration
    protocol via [`__getitem__()`](#object.__getitem__ "object.__getitem__"), see [this section in the language
    reference](expressions.html#membership-test-details).

### 3.3.8. Emulating numeric types

The following methods can be defined to emulate numeric objects. Methods
corresponding to operations that are not supported by the particular kind of
number implemented (e.g., bitwise operations for non-integral numbers) should be
left undefined.

object.\_\_add\_\_(*self*, *other*)

object.\_\_sub\_\_(*self*, *other*)

object.\_\_mul\_\_(*self*, *other*)

object.\_\_matmul\_\_(*self*, *other*)

object.\_\_truediv\_\_(*self*, *other*)

object.\_\_floordiv\_\_(*self*, *other*)

object.\_\_mod\_\_(*self*, *other*)

object.\_\_divmod\_\_(*self*, *other*)

object.\_\_pow\_\_(*self*, *other*[, *modulo*])

object.\_\_lshift\_\_(*self*, *other*)

object.\_\_rshift\_\_(*self*, *other*)

object.\_\_and\_\_(*self*, *other*)

object.\_\_xor\_\_(*self*, *other*)

object.\_\_or\_\_(*self*, *other*)
:   These methods are called to implement the binary arithmetic operations
    (`+`, `-`, `*`, `@`, `/`, `//`, `%`, [`divmod()`](../library/functions.html#divmod "divmod"),
    [`pow()`](../library/functions.html#pow "pow"), `**`, `<<`, `>>`, `&`, `^`, `|`). For instance, to
    evaluate the expression `x + y`, where *x* is an instance of a class that
    has an [`__add__()`](#object.__add__ "object.__add__") method, `type(x).__add__(x, y)` is called. The
    [`__divmod__()`](#object.__divmod__ "object.__divmod__") method should be the equivalent to using
    [`__floordiv__()`](#object.__floordiv__ "object.__floordiv__") and [`__mod__()`](#object.__mod__ "object.__mod__"); it should not be related to
    [`__truediv__()`](#object.__truediv__ "object.__truediv__"). Note that [`__pow__()`](#object.__pow__ "object.__pow__") should be defined to accept
    an optional third argument if the ternary version of the built-in [`pow()`](../library/functions.html#pow "pow")
    function is to be supported.

    If one of those methods does not support the operation with the supplied
    arguments, it should return [`NotImplemented`](../library/constants.html#NotImplemented "NotImplemented").

object.\_\_radd\_\_(*self*, *other*)

object.\_\_rsub\_\_(*self*, *other*)

object.\_\_rmul\_\_(*self*, *other*)

object.\_\_rmatmul\_\_(*self*, *other*)

object.\_\_rtruediv\_\_(*self*, *other*)

object.\_\_rfloordiv\_\_(*self*, *other*)

object.\_\_rmod\_\_(*self*, *other*)

object.\_\_rdivmod\_\_(*self*, *other*)

object.\_\_rpow\_\_(*self*, *other*[, *modulo*])

object.\_\_rlshift\_\_(*self*, *other*)

object.\_\_rrshift\_\_(*self*, *other*)

object.\_\_rand\_\_(*self*, *other*)

object.\_\_rxor\_\_(*self*, *other*)

object.\_\_ror\_\_(*self*, *other*)
:   These methods are called to implement the binary arithmetic operations
    (`+`, `-`, `*`, `@`, `/`, `//`, `%`, [`divmod()`](../library/functions.html#divmod "divmod"),
    [`pow()`](../library/functions.html#pow "pow"), `**`, `<<`, `>>`, `&`, `^`, `|`) with reflected
    (swapped) operands. These functions are only called if the left operand does
    not support the corresponding operation and the operands are of different
    types. For instance, to evaluate the expression `x - y`, where *y* is
    an instance of a class that has an [`__rsub__()`](#object.__rsub__ "object.__rsub__") method,
    `type(y).__rsub__(y, x)` is called if `type(x).__sub__(x, y)` returns
    [`NotImplemented`](../library/constants.html#NotImplemented "NotImplemented").

    Note that ternary [`pow()`](../library/functions.html#pow "pow") will not try calling [`__rpow__()`](#object.__rpow__ "object.__rpow__") (the
    coercion rules would become too complicated).

    Note

    If the right operandâs type is a subclass of the left operandâs type and
    that subclass provides a different implementation of the reflected method
    for the operation, this method will be called before the left operandâs
    non-reflected method. This behavior allows subclasses to override their
    ancestorsâ operations.

object.\_\_iadd\_\_(*self*, *other*)

object.\_\_isub\_\_(*self*, *other*)

object.\_\_imul\_\_(*self*, *other*)

object.\_\_imatmul\_\_(*self*, *other*)

object.\_\_itruediv\_\_(*self*, *other*)

object.\_\_ifloordiv\_\_(*self*, *other*)

object.\_\_imod\_\_(*self*, *other*)

object.\_\_ipow\_\_(*self*, *other*[, *modulo*])

object.\_\_ilshift\_\_(*self*, *other*)

object.\_\_irshift\_\_(*self*, *other*)

object.\_\_iand\_\_(*self*, *other*)

object.\_\_ixor\_\_(*self*, *other*)

object.\_\_ior\_\_(*self*, *other*)
:   These methods are called to implement the augmented arithmetic assignments
    (`+=`, `-=`, `*=`, `@=`, `/=`, `//=`, `%=`, `**=`, `<<=`,
    `>>=`, `&=`, `^=`, `|=`). These methods should attempt to do the
    operation in-place (modifying *self*) and return the result (which could be,
    but does not have to be, *self*). If a specific method is not defined, or if
    that method returns [`NotImplemented`](../library/constants.html#NotImplemented "NotImplemented"), the
    augmented assignment falls back to the normal methods. For instance, if *x*
    is an instance of a class with an [`__iadd__()`](#object.__iadd__ "object.__iadd__") method, `x += y` is
    equivalent to `x = x.__iadd__(y)` . If [`__iadd__()`](#object.__iadd__ "object.__iadd__") does not exist, or if `x.__iadd__(y)`
    returns `NotImplemented`, `x.__add__(y)` and
    `y.__radd__(x)` are considered, as with the evaluation of `x + y`. In
    certain situations, augmented assignment can result in unexpected errors (see
    [Why does a\_tuple[i] += [âitemâ] raise an exception when the addition works?](../faq/programming.html#faq-augmented-assignment-tuple-error)), but this behavior is in fact
    part of the data model.

object.\_\_neg\_\_(*self*)

object.\_\_pos\_\_(*self*)

object.\_\_abs\_\_(*self*)

object.\_\_invert\_\_(*self*)
:   Called to implement the unary arithmetic operations (`-`, `+`, [`abs()`](../library/functions.html#abs "abs")
    and `~`).

object.\_\_complex\_\_(*self*)

object.\_\_int\_\_(*self*)

object.\_\_float\_\_(*self*)
:   Called to implement the built-in functions [`complex()`](../library/functions.html#complex "complex"),
    [`int()`](../library/functions.html#int "int") and [`float()`](../library/functions.html#float "float"). Should return a value
    of the appropriate type.

object.\_\_index\_\_(*self*)
:   Called to implement [`operator.index()`](../library/operator.html#operator.index "operator.index"), and whenever Python needs to
    losslessly convert the numeric object to an integer object (such as in
    slicing, or in the built-in [`bin()`](../library/functions.html#bin "bin"), [`hex()`](../library/functions.html#hex "hex") and [`oct()`](../library/functions.html#oct "oct")
    functions). Presence of this method indicates that the numeric object is
    an integer type. Must return an integer.

    If [`__int__()`](#object.__int__ "object.__int__"), [`__float__()`](#object.__float__ "object.__float__") and [`__complex__()`](#object.__complex__ "object.__complex__") are not
    defined then corresponding built-in functions [`int()`](../library/functions.html#int "int"), [`float()`](../library/functions.html#float "float")
    and [`complex()`](../library/functions.html#complex "complex") fall back to [`__index__()`](#object.__index__ "object.__index__").

object.\_\_round\_\_(*self*[, *ndigits*])

object.\_\_trunc\_\_(*self*)

object.\_\_floor\_\_(*self*)

object.\_\_ceil\_\_(*self*)
:   Called to implement the built-in function [`round()`](../library/functions.html#round "round") and [`math`](../library/math.html#module-math "math: Mathematical functions (sin() etc.).")
    functions [`trunc()`](../library/math.html#math.trunc "math.trunc"), [`floor()`](../library/math.html#math.floor "math.floor") and [`ceil()`](../library/math.html#math.ceil "math.ceil").
    Unless *ndigits* is passed to `__round__()` all these methods should
    return the value of the object truncated to an [`Integral`](../library/numbers.html#numbers.Integral "numbers.Integral")
    (typically an [`int`](../library/functions.html#int "int")).

    The built-in function [`int()`](../library/functions.html#int "int") falls back to [`__trunc__()`](#object.__trunc__ "object.__trunc__") if neither
    [`__int__()`](#object.__int__ "object.__int__") nor [`__index__()`](#object.__index__ "object.__index__") is defined.

### 3.3.9. With Statement Context Managers

A *context manager* is an object that defines the runtime context to be
established when executing a [`with`](compound_stmts.html#with) statement. The context manager
handles the entry into, and the exit from, the desired runtime context for the
execution of the block of code. Context managers are normally invoked using the
`with` statement (described in section [The with statement](compound_stmts.html#with)), but can also be
used by directly invoking their methods.

Typical uses of context managers include saving and restoring various kinds of
global state, locking and unlocking resources, closing opened files, etc.

For more information on context managers, see [Context Manager Types](../library/stdtypes.html#typecontextmanager).
The [`object`](../library/functions.html#object "object") class itself does not provide the context manager methods.

object.\_\_enter\_\_(*self*)
:   Enter the runtime context related to this object. The [`with`](compound_stmts.html#with) statement
    will bind this methodâs return value to the target(s) specified in the
    `as` clause of the statement, if any.

object.\_\_exit\_\_(*self*, *exc\_type*, *exc\_value*, *traceback*)
:   Exit the runtime context related to this object. The parameters describe the
    exception that caused the context to be exited. If the context was exited
    without an exception, all three arguments will be [`None`](../library/constants.html#None "None").

    If an exception is supplied, and the method wishes to suppress the exception
    (i.e., prevent it from being propagated), it should return a true value.
    Otherwise, the exception will be processed normally upon exit from this method.

    Note that [`__exit__()`](#object.__exit__ "object.__exit__") methods should not reraise the passed-in exception;
    this is the callerâs responsibility.

See also

[**PEP 343**](https://peps.python.org/pep-0343/) - The âwithâ statement
:   The specification, background, and examples for the Python [`with`](compound_stmts.html#with)
    statement.

### 3.3.10. Customizing positional arguments in class pattern matching

When using a class name in a pattern, positional arguments in the pattern are not
allowed by default, i.e. `case MyClass(x, y)` is typically invalid without special
support in `MyClass`. To be able to use that kind of pattern, the class needs to
define a *\_\_match\_args\_\_* attribute.

object.\_\_match\_args\_\_
:   This class variable can be assigned a tuple of strings. When this class is
    used in a class pattern with positional arguments, each positional argument will
    be converted into a keyword argument, using the corresponding value in
    *\_\_match\_args\_\_* as the keyword. The absence of this attribute is equivalent to
    setting it to `()`.

For example, if `MyClass.__match_args__` is `("left", "center", "right")` that means
that `case MyClass(x, y)` is equivalent to `case MyClass(left=x, center=y)`. Note
that the number of arguments in the pattern must be smaller than or equal to the number
of elements in *\_\_match\_args\_\_*; if it is larger, the pattern match attempt will raise
a [`TypeError`](../library/exceptions.html#TypeError "TypeError").

See also

[**PEP 634**](https://peps.python.org/pep-0634/) - Structural Pattern Matching
:   The specification for the Python `match` statement.

### 3.3.11. Emulating buffer types

The [buffer protocol](../c-api/buffer.html#bufferobjects) provides a way for Python
objects to expose efficient access to a low-level memory array. This protocol
is implemented by builtin types such as [`bytes`](../library/stdtypes.html#bytes "bytes") and [`memoryview`](../library/stdtypes.html#memoryview "memoryview"),
and third-party libraries may define additional buffer types.

While buffer types are usually implemented in C, it is also possible to
implement the protocol in Python.

object.\_\_buffer\_\_(*self*, *flags*)
:   Called when a buffer is requested from *self* (for example, by the
    [`memoryview`](../library/stdtypes.html#memoryview "memoryview") constructor). The *flags* argument is an integer
    representing the kind of buffer requested, affecting for example whether
    the returned buffer is read-only or writable. [`inspect.BufferFlags`](../library/inspect.html#inspect.BufferFlags "inspect.BufferFlags")
    provides a convenient way to interpret the flags. The method must return
    a [`memoryview`](../library/stdtypes.html#memoryview "memoryview") object.

object.\_\_release\_buffer\_\_(*self*, *buffer*)
:   Called when a buffer is no longer needed. The *buffer* argument is a
    [`memoryview`](../library/stdtypes.html#memoryview "memoryview") object that was previously returned by
    [`__buffer__()`](#object.__buffer__ "object.__buffer__"). The method must release any resources associated
    with the buffer. This method should return `None`.
    Buffer objects that do not need to perform any cleanup are not required
    to implement this method.

See also

[**PEP 688**](https://peps.python.org/pep-0688/) - Making the buffer protocol accessible in Python
:   Introduces the Python `__buffer__` and `__release_buffer__` methods.

[`collections.abc.Buffer`](../library/collections.abc.html#collections.abc.Buffer "collections.abc.Buffer")
:   ABC for buffer types.

### 3.3.12. Special method lookup

For custom classes, implicit invocations of special methods are only guaranteed
to work correctly if defined on an objectâs type, not in the objectâs instance
dictionary. That behaviour is the reason why the following code raises an
exception:

```
>>> class C:
...     pass
...
>>> c = C()
>>> c.__len__ = lambda: 5
>>> len(c)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: object of type 'C' has no len()
```

The rationale behind this behaviour lies with a number of special methods such
as [`__hash__()`](#object.__hash__ "object.__hash__") and [`__repr__()`](#object.__repr__ "object.__repr__") that are implemented
by all objects,
including type objects. If the implicit lookup of these methods used the
conventional lookup process, they would fail when invoked on the type object
itself:

```
>>> 1 .__hash__() == hash(1)
True
>>> int.__hash__() == hash(int)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: descriptor '__hash__' of 'int' object needs an argument
```

Incorrectly attempting to invoke an unbound method of a class in this way is
sometimes referred to as âmetaclass confusionâ, and is avoided by bypassing
the instance when looking up special methods:

```
>>> type(1).__hash__(1) == hash(1)
True
>>> type(int).__hash__(int) == hash(int)
True
```

In addition to bypassing any instance attributes in the interest of
correctness, implicit special method lookup generally also bypasses the
[`__getattribute__()`](#object.__getattribute__ "object.__getattribute__") method even of the objectâs metaclass:

```
>>> class Meta(type):
...     def __getattribute__(*args):
...         print("Metaclass getattribute invoked")
...         return type.__getattribute__(*args)
...
>>> class C(object, metaclass=Meta):
...     def __len__(self):
...         return 10
...     def __getattribute__(*args):
...         print("Class getattribute invoked")
...         return object.__getattribute__(*args)
...
>>> c = C()
>>> c.__len__()                 # Explicit lookup via instance
Class getattribute invoked
10
>>> type(c).__len__(c)          # Explicit lookup via type
Metaclass getattribute invoked
10
>>> len(c)                      # Implicit lookup
10
```

Bypassing the [`__getattribute__()`](#object.__getattribute__ "object.__getattribute__") machinery in this fashion
provides significant scope for speed optimisations within the
interpreter, at the cost of some flexibility in the handling of
special methods (the special method *must* be set on the class
object itself in order to be consistently invoked by the interpreter).