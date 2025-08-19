```
const map = new Map();

map.set("a", 1);
map.set("b", 2);
map.set("c", 3);

console.log(map.get("a"));
// Expected output: 1

map.set("a", 97);

console.log(map.get("a"));
// Expected output: 97

console.log(map.size);
// Expected output: 3

map.delete("b");

console.log(map.size);
// Expected output: 2
```

`Map` objects are collections of key-value pairs. A key in the `Map` **may only occur once**; it is unique in the `Map`'s collection. A `Map` object is iterated by key-value pairs â a [`for...of`](/en-US/docs/Web/JavaScript/Reference/Statements/for...of) loop returns a 2-member array of `[key, value]` for each iteration. Iteration happens in *insertion order*, which corresponds to the order in which each key-value pair was first inserted into the map by the [`set()`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/set) method (that is, there wasn't a key with the same value already in the map when `set()` was called).

The specification requires maps to be implemented "that, on average, provide access times that are sublinear on the number of elements in the collection". Therefore, it could be represented internally as a hash table (with O(1) lookup), a search tree (with O(log(N)) lookup), or any other data structure, as long as the complexity is better than O(N).

Value equality is based on the [SameValueZero](/en-US/docs/Web/JavaScript/Guide/Equality_comparisons_and_sameness#same-value-zero_equality) algorithm. (It used to use [SameValue](/en-US/docs/Web/JavaScript/Guide/Equality_comparisons_and_sameness#same-value_equality_using_object.is), which treated `0` and `-0` as different. Check [browser compatibility](#browser_compatibility).) This means [`NaN`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/NaN) is considered the same as `NaN` (even though `NaN !== NaN`) and all other values are considered equal according to the semantics of the `===` operator.

[`Object`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object) is similar to `Map`âboth let you set keys to
values, retrieve those values, delete keys, and detect whether something is
stored at a key. For this reason (and because there were no built-in
alternatives), `Object` has been used as `Map` historically.

However, there are important differences that make `Map` preferable in some
cases:

|  | Map | Object |
| --- | --- | --- |
| Accidental Keys | A `Map` does not contain any keys by default. It only contains what is explicitly put into it. | An `Object` has a prototype, so it contains default keys that could collide with your own keys if you're not careful. |
| Security | A `Map` is safe to use with user-provided keys and values. | Setting user-provided key-value pairs on an `Object` may allow an attacker to override the object's prototype, which can lead to [object injection attacks](https://github.com/eslint-community/eslint-plugin-security/blob/main/docs/the-dangers-of-square-bracket-notation.md). Like the accidental keys issue, this can also be mitigated by using a `null`-prototype object. |
| Key Types | A `Map`'s keys can be any value (including functions, objects, or any primitive). | The keys of an `Object` must be either a [`String`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/String) or a [`Symbol`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol). |
| Key Order | The keys in `Map` are ordered in a straightforward way: A `Map` object iterates entries, keys, and values in the order of entry insertion. | Although the keys of an ordinary `Object` are ordered now, this was not always the case, and the order is complex. As a result, it's best not to rely on property order.  The order was first defined for own properties only in ECMAScript 2015; ECMAScript 2020 defines order for inherited properties as well. But note that no single mechanism iterates **all** of an object's properties; the various mechanisms each include different subsets of properties. ([`for-in`](/en-US/docs/Web/JavaScript/Reference/Statements/for...in) includes only enumerable string-keyed properties; [`Object.keys`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/keys) includes only own, enumerable, string-keyed properties; [`Object.getOwnPropertyNames`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/getOwnPropertyNames) includes own, string-keyed properties even if non-enumerable; [`Object.getOwnPropertySymbols`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/getOwnPropertySymbols) does the same for just `Symbol`-keyed properties, etc.) |
| Size | The number of items in a `Map` is easily retrieved from its [`size`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/size) property. | Determining the number of items in an `Object` is more roundabout and less efficient. A common way to do it is through the [`length`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/length) of the array returned from [`Object.keys()`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/keys). |
| Iteration | A `Map` is an [iterable](/en-US/docs/Web/JavaScript/Reference/Iteration_protocols), so it can be directly iterated. | `Object` does not implement an [iteration protocol](/en-US/docs/Web/JavaScript/Reference/Iteration_protocols#the_iterable_protocol), and so objects are not directly iterable using the JavaScript [for...of](/en-US/docs/Web/JavaScript/Reference/Statements/for...of) statement (by default).  **Note:**   * An object can implement the iteration protocol, or you can get an   iterable for an object using [`Object.keys`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/keys) or [`Object.entries`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/entries). * The   [for...in](/en-US/docs/Web/JavaScript/Reference/Statements/for...in)   statement allows you to iterate over the   *enumerable* properties of an object. |
| Performance | Performs better in scenarios involving frequent additions and removals of key-value pairs. | Not optimized for frequent additions and removals of key-value pairs. |
| Serialization and parsing | No native support for serialization or parsing.  (But you can build your own serialization and parsing support for `Map` by using [`JSON.stringify()`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify) with its *replacer* argument, and by using [`JSON.parse()`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse) with its *reviver* argument. See the Stack Overflow question [How do you JSON.stringify an ES6 Map?](https://stackoverflow.com/q/29085197/)). | Native support for serialization from [`Object`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object) to JSON, using [`JSON.stringify()`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify).  Native support for parsing from JSON to [`Object`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object), using [`JSON.parse()`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse). |

Setting Object properties works for Map objects as well, and can cause
considerable confusion.

Therefore, this appears to work in a way:

```
const wrongMap = new Map();
wrongMap["bla"] = "blaa";
wrongMap["bla2"] = "blaaa2";

console.log(wrongMap); // Map { bla: 'blaa', bla2: 'blaaa2' }
```

But that way of setting a property does not interact with the Map data
structure. It uses the feature of the generic object. The value of 'bla' is not
stored in the Map for queries. Other operations on the data fail:

```
wrongMap.has("bla"); // false
wrongMap.delete("bla"); // false
console.log(wrongMap); // Map { bla: 'blaa', bla2: 'blaaa2' }
```

The correct usage for storing data in the Map is through the `set(key, value)`
method.

```
const contacts = new Map();
contacts.set("Jessie", { phone: "213-555-1234", address: "123 N 1st Ave" });
contacts.has("Jessie"); // true
contacts.get("Hilary"); // undefined
contacts.set("Hilary", { phone: "617-555-4321", address: "321 S 2nd St" });
contacts.get("Jessie"); // {phone: "213-555-1234", address: "123 N 1st Ave"}
contacts.delete("Raymond"); // false
contacts.delete("Jessie"); // true
console.log(contacts.size); // 1
```

**Browser `Map`-like objects** (or "maplike objects") are [Web API](/en-US/docs/Web/API) interfaces that behave in many ways like a `Map`.

Just like `Map`, entries can be iterated in the same order that they were added to the object.
`Map`-like objects and `Map` also have properties and methods that share the same name and behavior.
However unlike `Map` they only allow specific predefined types for the keys and values of each entry.

The allowed types are set in the specification IDL definition.
For example, [`RTCStatsReport`](/en-US/docs/Web/API/RTCStatsReport) is a `Map`-like object that must use strings for keys and objects for values.
This is defined in the specification IDL below:

```
interface RTCStatsReport {
  readonly maplike<DOMString, object>;
};
```

`Map`-like objects are either read-only or read-writable (see the `readonly` keyword in the IDL above).

The methods and properties have the same behavior as the equivalent entities in `Map`, except for the restriction on the types of the keys and values.

The following are examples of read-only `Map`-like browser objects:

[`Map()`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/Map)
:   Creates a new `Map` object.

[`Map[Symbol.species]`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/Symbol.species)
:   The constructor function that is used to create derived objects.

[`Map.groupBy()`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/groupBy)
:   Groups the elements of a given iterable using the values returned by a provided callback function. The final returned `Map` uses the unique values from the test function as keys, which can be used to get the array of elements in each group.

These properties are defined on `Map.prototype` and shared by all `Map` instances.

[`Map.prototype.constructor`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/constructor)
:   The constructor function that created the instance object. For `Map` instances, the initial value is the [`Map`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/Map) constructor.

[`Map.prototype.size`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/size)
:   Returns the number of key/value pairs in the `Map` object.

[`Map.prototype[Symbol.toStringTag]`](#map.prototypesymbol.tostringtag)
:   The initial value of the [`[Symbol.toStringTag]`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol/toStringTag) property is the string `"Map"`. This property is used in [`Object.prototype.toString()`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/toString).

[`Map.prototype.clear()`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/clear)
:   Removes all key-value pairs from the `Map` object.

[`Map.prototype.delete()`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/delete)
:   Returns `true` if an element in the `Map` object existed and has been
    removed, or `false` if the element does not exist. `map.has(key)`
    will return `false` afterwards.

[`Map.prototype.entries()`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/entries)
:   Returns a new Iterator object that contains a two-member array of `[key, value]` for each element in the `Map` object in insertion order.

[`Map.prototype.forEach()`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/forEach)
:   Calls `callbackFn` once for each key-value pair present in the `Map` object, in insertion order. If a `thisArg` parameter is provided to `forEach`, it will be used as the `this` value for each callback.

[`Map.prototype.get()`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/get)
:   Returns the value associated to the passed key, or `undefined` if there is none.

[`Map.prototype.has()`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/has)
:   Returns a boolean indicating whether a value has been associated with the passed key in the `Map` object or not.

[`Map.prototype.keys()`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/keys)
:   Returns a new Iterator object that contains the keys for each element in the `Map` object in insertion order.

[`Map.prototype.set()`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/set)
:   Sets the value for the passed key in the `Map` object. Returns the `Map` object.

[`Map.prototype.values()`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/values)
:   Returns a new Iterator object that contains the values for each element in the `Map` object in insertion order.

[`Map.prototype[Symbol.iterator]()`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/Symbol.iterator)
:   Returns a new Iterator object that contains a two-member array of `[key, value]` for each element in the `Map` object in insertion order.

```
const myMap = new Map();

const keyString = "a string";
const keyObj = {};
const keyFunc = () => {};

// setting the values
myMap.set(keyString, "value associated with 'a string'");
myMap.set(keyObj, "value associated with keyObj");
myMap.set(keyFunc, "value associated with keyFunc");

console.log(myMap.size); // 3

// getting the values
console.log(myMap.get(keyString)); // "value associated with 'a string'"
console.log(myMap.get(keyObj)); // "value associated with keyObj"
console.log(myMap.get(keyFunc)); // "value associated with keyFunc"

console.log(myMap.get("a string")); // "value associated with 'a string'", because keyString === 'a string'
console.log(myMap.get({})); // undefined, because keyObj !== {}
console.log(myMap.get(() => {})); // undefined, because keyFunc !== () => {}
```

[`NaN`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/NaN) can also be used as a key. Even though every `NaN` is
not equal to itself (`NaN !== NaN` is true), the following example works because
`NaN`s are indistinguishable from each other:

```
const myMap = new Map();
myMap.set(NaN, "not a number");

myMap.get(NaN);
// "not a number"

const otherNaN = Number("foo");
myMap.get(otherNaN);
// "not a number"
```

Maps can be iterated using a `for...of` loop:

```
const myMap = new Map();
myMap.set(0, "zero");
myMap.set(1, "one");

for (const [key, value] of myMap) {
  console.log(`${key} = ${value}`);
}
// 0 = zero
// 1 = one

for (const key of myMap.keys()) {
  console.log(key);
}
// 0
// 1

for (const value of myMap.values()) {
  console.log(value);
}
// zero
// one

for (const [key, value] of myMap.entries()) {
  console.log(`${key} = ${value}`);
}
// 0 = zero
// 1 = one
```

Maps can be iterated using the
[`forEach()`](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/forEach) method:

```
myMap.forEach((value, key) => {
  console.log(`${key} = ${value}`);
});
// 0 = zero
// 1 = one
```

```
const kvArray = [
  ["key1", "value1"],
  ["key2", "value2"],
];

// Use the regular Map constructor to transform a 2D key-value Array into a map
const myMap = new Map(kvArray);

console.log(myMap.get("key1")); // "value1"

// Use Array.from() to transform a map into a 2D key-value Array
console.log(Array.from(myMap)); // Will show you exactly the same Array as kvArray

// A succinct way to do the same, using the spread syntax
console.log([...myMap]);

// Or use the keys() or values() iterators, and convert them to an array
console.log(Array.from(myMap.keys())); // ["key1", "key2"]
```

Just like `Array`s, `Map`s can be cloned:

```
const original = new Map([[1, "one"]]);

const clone = new Map(original);

console.log(clone.get(1)); // one
console.log(original === clone); // false (useful for shallow comparison)
```

**Note:**
Keep in mind that *the data itself* is not cloned. In other words, it is only a [shallow copy](/en-US/docs/Glossary/Shallow_copy) of the `Map`.

Maps can be merged, maintaining key uniqueness:

```
const first = new Map([
  [1, "one"],
  [2, "two"],
  [3, "three"],
]);

const second = new Map([
  [1, "uno"],
  [2, "dos"],
]);

// Merge two maps. The last repeated key wins.
// Spread syntax essentially converts a Map to an Array
const merged = new Map([...first, ...second]);

console.log(merged.get(1)); // uno
console.log(merged.get(2)); // dos
console.log(merged.get(3)); // three
```

Maps can be merged with Arrays, too:

```
const first = new Map([
  [1, "one"],
  [2, "two"],
  [3, "three"],
]);

const second = new Map([
  [1, "uno"],
  [2, "dos"],
]);

// Merge maps with an array. The last repeated key wins.
const merged = new Map([...first, ...second, [1, "un"]]);

console.log(merged.get(1)); // un
console.log(merged.get(2)); // dos
console.log(merged.get(3)); // three
```