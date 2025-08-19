All file system operations have synchronous, callback, and promise-based
forms, and are accessible using both CommonJS syntax and ES6 Modules (ESM).

### Promises API[#](#promises-api)

The `fs/promises` API provides asynchronous file system methods that return
promises.

The promise APIs use the underlying Node.js threadpool to perform file
system operations off the event loop thread. These operations are not
synchronized or threadsafe. Care must be taken when performing multiple
concurrent modifications on the same file or data corruption may occur.

#### Class: `FileHandle`[#](#class-filehandle)

Added in: v10.0.0

A [<FileHandle>](fs.html#class-filehandle) object is an object wrapper for a numeric file descriptor.

Instances of the [<FileHandle>](fs.html#class-filehandle) object are created by the `fsPromises.open()`
method.

All [<FileHandle>](fs.html#class-filehandle) objects are [<EventEmitter>](events.html#class-eventemitter)s.

If a [<FileHandle>](fs.html#class-filehandle) is not closed using the `filehandle.close()` method, it will
try to automatically close the file descriptor and emit a process warning,
helping to prevent memory leaks. Please do not rely on this behavior because
it can be unreliable and the file may not be closed. Instead, always explicitly
close [<FileHandle>](fs.html#class-filehandle)s. Node.js may change this behavior in the future.

##### Event: `'close'`[#](#event-close)

Added in: v15.4.0

The `'close'` event is emitted when the [<FileHandle>](fs.html#class-filehandle) has been closed and can no
longer be used.

##### `filehandle.chmod(mode)`[#](#filehandlechmodmode)

Added in: v10.0.0

* `mode` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) the file mode bit mask.
* Returns: [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) Fulfills with `undefined` upon success.

Modifies the permissions on the file. See [`chmod(2)`](http://man7.org/linux/man-pages/man2/chmod.2.html).

##### `filehandle.chown(uid, gid)`[#](#filehandlechownuid-gid)

Added in: v10.0.0

* `uid` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) The file's new owner's user id.
* `gid` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) The file's new group's group id.
* Returns: [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) Fulfills with `undefined` upon success.

Changes the ownership of the file. A wrapper for [`chown(2)`](http://man7.org/linux/man-pages/man2/chown.2.html).

##### `filehandle.close()`[#](#filehandleclose)

Added in: v10.0.0

* Returns: [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) Fulfills with `undefined` upon success.

Closes the file handle after waiting for any pending operation on the handle to
complete.

```
import { open } from 'node:fs/promises';

let filehandle;
try {
  filehandle = await open('thefile.txt', 'r');
} finally {
  await filehandle?.close();
} copy
```

##### `filehandle.createReadStream([options])`[#](#filehandlecreatereadstreamoptions)

Added in: v16.11.0

`options` can include `start` and `end` values to read a range of bytes from
the file instead of the entire file. Both `start` and `end` are inclusive and
start counting at 0, allowed values are in the
[0, [`Number.MAX_SAFE_INTEGER`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER)] range. If `start` is
omitted or `undefined`, `filehandle.createReadStream()` reads sequentially from
the current file position. The `encoding` can be any one of those accepted by
[<Buffer>](buffer.html#class-buffer).

If the `FileHandle` points to a character device that only supports blocking
reads (such as keyboard or sound card), read operations do not finish until data
is available. This can prevent the process from exiting and the stream from
closing naturally.

By default, the stream will emit a `'close'` event after it has been
destroyed. Set the `emitClose` option to `false` to change this behavior.

```
import { open } from 'node:fs/promises';

const fd = await open('/dev/input/event0');

const stream = fd.createReadStream();
setTimeout(() => {
  stream.close(); 
  
  
  
  
  
  stream.push(null);
  stream.read(0);
}, 100); copy
```

If `autoClose` is false, then the file descriptor won't be closed, even if
there's an error. It is the application's responsibility to close it and make
sure there's no file descriptor leak. If `autoClose` is set to true (default
behavior), on `'error'` or `'end'` the file descriptor will be closed
automatically.

An example to read the last 10 bytes of a file which is 100 bytes long:

```
import { open } from 'node:fs/promises';

const fd = await open('sample.txt');
fd.createReadStream({ start: 90, end: 99 }); copy
```

##### `filehandle.createWriteStream([options])`[#](#filehandlecreatewritestreamoptions)

`options` may also include a `start` option to allow writing data at some
position past the beginning of the file, allowed values are in the
[0, [`Number.MAX_SAFE_INTEGER`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER)] range. Modifying a file rather than
replacing it may require the `flags` `open` option to be set to `r+` rather than
the default `r`. The `encoding` can be any one of those accepted by [<Buffer>](buffer.html#class-buffer).

If `autoClose` is set to true (default behavior) on `'error'` or `'finish'`
the file descriptor will be closed automatically. If `autoClose` is false,
then the file descriptor won't be closed, even if there's an error.
It is the application's responsibility to close it and make sure there's no
file descriptor leak.

By default, the stream will emit a `'close'` event after it has been
destroyed. Set the `emitClose` option to `false` to change this behavior.

##### `filehandle.datasync()`[#](#filehandledatasync)

Added in: v10.0.0

* Returns: [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) Fulfills with `undefined` upon success.

Forces all currently queued I/O operations associated with the file to the
operating system's synchronized I/O completion state. Refer to the POSIX
[`fdatasync(2)`](http://man7.org/linux/man-pages/man2/fdatasync.2.html) documentation for details.

Unlike `filehandle.sync` this method does not flush modified metadata.

##### `filehandle.fd`[#](#filehandlefd)

Added in: v10.0.0

##### `filehandle.read(buffer, offset, length, position)`[#](#filehandlereadbuffer-offset-length-position)

* `buffer` [<Buffer>](buffer.html#class-buffer) | [<TypedArray>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray) | [<DataView>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView) A buffer that will be filled with the
  file data read.
* `offset` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) The location in the buffer at which to start filling.
  **Default:** `0`
* `length` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) The number of bytes to read. **Default:**
  `buffer.byteLength - offset`
* `position` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) | [<bigint>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt) | [<null>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Null_type) The location where to begin reading data
  from the file. If `null` or `-1`, data will be read from the current file
  position, and the position will be updated. If `position` is a non-negative
  integer, the current file position will remain unchanged.
  **Default:**: `null`
* Returns: [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) Fulfills upon success with an object with two properties:

Reads data from the file and stores that in the given buffer.

If the file is not modified concurrently, the end-of-file is reached when the
number of bytes read is zero.

##### `filehandle.read([options])`[#](#filehandlereadoptions)

* `options` [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)
  + `buffer` [<Buffer>](buffer.html#class-buffer) | [<TypedArray>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray) | [<DataView>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView) A buffer that will be filled with the
    file data read. **Default:** `Buffer.alloc(16384)`
  + `offset` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) The location in the buffer at which to start filling.
    **Default:** `0`
  + `length` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) The number of bytes to read. **Default:**
    `buffer.byteLength - offset`
  + `position` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) | [<bigint>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt) | [<null>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Null_type) The location where to begin reading data
    from the file. If `null` or `-1`, data will be read from the current file
    position, and the position will be updated. If `position` is a non-negative
    integer, the current file position will remain unchanged.
    **Default:**: `null`
* Returns: [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) Fulfills upon success with an object with two properties:

Reads data from the file and stores that in the given buffer.

If the file is not modified concurrently, the end-of-file is reached when the
number of bytes read is zero.

##### `filehandle.read(buffer[, options])`[#](#filehandlereadbuffer-options)

* `buffer` [<Buffer>](buffer.html#class-buffer) | [<TypedArray>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray) | [<DataView>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView) A buffer that will be filled with the
  file data read.
* `options` [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)
  + `offset` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) The location in the buffer at which to start filling.
    **Default:** `0`
  + `length` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) The number of bytes to read. **Default:**
    `buffer.byteLength - offset`
  + `position` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) | [<bigint>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt) | [<null>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Null_type) The location where to begin reading data
    from the file. If `null` or `-1`, data will be read from the current file
    position, and the position will be updated. If `position` is a non-negative
    integer, the current file position will remain unchanged.
    **Default:**: `null`
* Returns: [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) Fulfills upon success with an object with two properties:

Reads data from the file and stores that in the given buffer.

If the file is not modified concurrently, the end-of-file is reached when the
number of bytes read is zero.

##### `filehandle.readableWebStream([options])`[#](#filehandlereadablewebstreamoptions)

Returns a byte-oriented `ReadableStream` that may be used to read the file's
contents.

An error will be thrown if this method is called more than once or is called
after the `FileHandle` is closed or closing.

```
import {
  open,
} from 'node:fs/promises';

const file = await open('./some/file/to/read');

for await (const chunk of file.readableWebStream())
  console.log(chunk);

await file.close();const {
  open,
} = require('node:fs/promises');

(async () => {
  const file = await open('./some/file/to/read');

  for await (const chunk of file.readableWebStream())
    console.log(chunk);

  await file.close();
})();copy
```

While the `ReadableStream` will read the file to completion, it will not
close the `FileHandle` automatically. User code must still call the
`fileHandle.close()` method.

##### `filehandle.readFile(options)`[#](#filehandlereadfileoptions)

Added in: v10.0.0

* `options` [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object) | [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type)
* Returns: [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) Fulfills upon a successful read with the contents of the
  file. If no encoding is specified (using `options.encoding`), the data is
  returned as a [<Buffer>](buffer.html#class-buffer) object. Otherwise, the data will be a string.

Asynchronously reads the entire contents of a file.

If `options` is a string, then it specifies the `encoding`.

The [<FileHandle>](fs.html#class-filehandle) has to support reading.

If one or more `filehandle.read()` calls are made on a file handle and then a
`filehandle.readFile()` call is made, the data will be read from the current
position till the end of the file. It doesn't always read from the beginning
of the file.

##### `filehandle.readv(buffers[, position])`[#](#filehandlereadvbuffers-position)

Added in: v13.13.0, v12.17.0

* `buffers` [<Buffer[]>](buffer.html#class-buffer) | [<TypedArray[]>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray) | [<DataView[]>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView)
* `position` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) | [<null>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Null_type) The offset from the beginning of the file where
  the data should be read from. If `position` is not a `number`, the data will
  be read from the current position. **Default:** `null`
* Returns: [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) Fulfills upon success an object containing two properties:

Read from a file and write to an array of [<ArrayBufferView>](https://developer.mozilla.org/en-US/docs/Web/API/ArrayBufferView)s

##### `filehandle.stat([options])`[#](#filehandlestatoptions)

##### `filehandle.sync()`[#](#filehandlesync)

Added in: v10.0.0

* Returns: [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) Fulfills with `undefined` upon success.

Request that all data for the open file descriptor is flushed to the storage
device. The specific implementation is operating system and device specific.
Refer to the POSIX [`fsync(2)`](http://man7.org/linux/man-pages/man2/fsync.2.html) documentation for more detail.

##### `filehandle.truncate(len)`[#](#filehandletruncatelen)

Added in: v10.0.0

Truncates the file.

If the file was larger than `len` bytes, only the first `len` bytes will be
retained in the file.

The following example retains only the first four bytes of the file:

```
import { open } from 'node:fs/promises';

let filehandle = null;
try {
  filehandle = await open('temp.txt', 'r+');
  await filehandle.truncate(4);
} finally {
  await filehandle?.close();
} copy
```

If the file previously was shorter than `len` bytes, it is extended, and the
extended part is filled with null bytes (`'\0'`):

If `len` is negative then `0` will be used.

##### `filehandle.utimes(atime, mtime)`[#](#filehandleutimesatime-mtime)

Added in: v10.0.0

Change the file system timestamps of the object referenced by the [<FileHandle>](fs.html#class-filehandle)
then fulfills the promise with no arguments upon success.

##### `filehandle.write(buffer, offset[, length[, position]])`[#](#filehandlewritebuffer-offset-length-position)

* `buffer` [<Buffer>](buffer.html#class-buffer) | [<TypedArray>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray) | [<DataView>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView)
* `offset` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) The start position from within `buffer` where the data
  to write begins.
* `length` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) The number of bytes from `buffer` to write. **Default:**
  `buffer.byteLength - offset`
* `position` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) | [<null>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Null_type) The offset from the beginning of the file where the
  data from `buffer` should be written. If `position` is not a `number`,
  the data will be written at the current position. See the POSIX [`pwrite(2)`](http://man7.org/linux/man-pages/man2/pwrite.2.html)
  documentation for more detail. **Default:** `null`
* Returns: [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)

Write `buffer` to the file.

The promise is fulfilled with an object containing two properties:

It is unsafe to use `filehandle.write()` multiple times on the same file
without waiting for the promise to be fulfilled (or rejected). For this
scenario, use [`filehandle.createWriteStream()`](#filehandlecreatewritestreamoptions).

On Linux, positional writes do not work when the file is opened in append mode.
The kernel ignores the position argument and always appends the data to
the end of the file.

##### `filehandle.write(buffer[, options])`[#](#filehandlewritebuffer-options)

Added in: v18.3.0, v16.17.0

Write `buffer` to the file.

Similar to the above `filehandle.write` function, this version takes an
optional `options` object. If no `options` object is specified, it will
default with the above values.

##### `filehandle.write(string[, position[, encoding]])`[#](#filehandlewritestring-position-encoding)

* `string` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type)
* `position` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) | [<null>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Null_type) The offset from the beginning of the file where the
  data from `string` should be written. If `position` is not a `number` the
  data will be written at the current position. See the POSIX [`pwrite(2)`](http://man7.org/linux/man-pages/man2/pwrite.2.html)
  documentation for more detail. **Default:** `null`
* `encoding` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) The expected string encoding. **Default:** `'utf8'`
* Returns: [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)

Write `string` to the file. If `string` is not a string, the promise is
rejected with an error.

The promise is fulfilled with an object containing two properties:

* `bytesWritten` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) the number of bytes written
* `buffer` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) a reference to the `string` written.

It is unsafe to use `filehandle.write()` multiple times on the same file
without waiting for the promise to be fulfilled (or rejected). For this
scenario, use [`filehandle.createWriteStream()`](#filehandlecreatewritestreamoptions).

On Linux, positional writes do not work when the file is opened in append mode.
The kernel ignores the position argument and always appends the data to
the end of the file.

##### `filehandle.writeFile(data, options)`[#](#filehandlewritefiledata-options)

Asynchronously writes data to a file, replacing the file if it already exists.
`data` can be a string, a buffer, an [<AsyncIterable>](https://tc39.github.io/ecma262/#sec-asynciterable-interface), or an [<Iterable>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Iteration_protocols#The_iterable_protocol) object.
The promise is fulfilled with no arguments upon success.

If `options` is a string, then it specifies the `encoding`.

The [<FileHandle>](fs.html#class-filehandle) has to support writing.

It is unsafe to use `filehandle.writeFile()` multiple times on the same file
without waiting for the promise to be fulfilled (or rejected).

If one or more `filehandle.write()` calls are made on a file handle and then a
`filehandle.writeFile()` call is made, the data will be written from the
current position till the end of the file. It doesn't always write from the
beginning of the file.

##### `filehandle.writev(buffers[, position])`[#](#filehandlewritevbuffers-position)

Added in: v12.9.0

Write an array of [<ArrayBufferView>](https://developer.mozilla.org/en-US/docs/Web/API/ArrayBufferView)s to the file.

The promise is fulfilled with an object containing a two properties:

It is unsafe to call `writev()` multiple times on the same file without waiting
for the promise to be fulfilled (or rejected).

On Linux, positional writes don't work when the file is opened in append mode.
The kernel ignores the position argument and always appends the data to
the end of the file.

##### `filehandle[Symbol.asyncDispose]()`[#](#filehandlesymbolasyncdispose)

Calls `filehandle.close()` and returns a promise that fulfills when the
filehandle is closed.

#### `fsPromises.access(path[, mode])`[#](#fspromisesaccesspath-mode)

Added in: v10.0.0

Tests a user's permissions for the file or directory specified by `path`.
The `mode` argument is an optional integer that specifies the accessibility
checks to be performed. `mode` should be either the value `fs.constants.F_OK`
or a mask consisting of the bitwise OR of any of `fs.constants.R_OK`,
`fs.constants.W_OK`, and `fs.constants.X_OK` (e.g.
`fs.constants.W_OK | fs.constants.R_OK`). Check [File access constants](#file-access-constants) for
possible values of `mode`.

If the accessibility check is successful, the promise is fulfilled with no
value. If any of the accessibility checks fail, the promise is rejected
with an [<Error>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error) object. The following example checks if the file
`/etc/passwd` can be read and written by the current process.

```
import { access, constants } from 'node:fs/promises';

try {
  await access('/etc/passwd', constants.R_OK | constants.W_OK);
  console.log('can access');
} catch {
  console.error('cannot access');
} copy
```

Using `fsPromises.access()` to check for the accessibility of a file before
calling `fsPromises.open()` is not recommended. Doing so introduces a race
condition, since other processes may change the file's state between the two
calls. Instead, user code should open/read/write the file directly and handle
the error raised if the file is not accessible.

#### `fsPromises.appendFile(path, data[, options])`[#](#fspromisesappendfilepath-data-options)

Asynchronously append data to a file, creating the file if it does not yet
exist. `data` can be a string or a [<Buffer>](buffer.html#class-buffer).

If `options` is a string, then it specifies the `encoding`.

The `mode` option only affects the newly created file. See [`fs.open()`](#fsopenpath-flags-mode-callback)
for more details.

The `path` may be specified as a [<FileHandle>](fs.html#class-filehandle) that has been opened
for appending (using `fsPromises.open()`).

#### `fsPromises.chmod(path, mode)`[#](#fspromiseschmodpath-mode)

Added in: v10.0.0

Changes the permissions of a file.

#### `fsPromises.chown(path, uid, gid)`[#](#fspromiseschownpath-uid-gid)

Added in: v10.0.0

Changes the ownership of a file.

#### `fsPromises.copyFile(src, dest[, mode])`[#](#fspromisescopyfilesrc-dest-mode)

* `src` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) | [<Buffer>](buffer.html#class-buffer) | [<URL>](url.html#the-whatwg-url-api) source filename to copy
* `dest` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) | [<Buffer>](buffer.html#class-buffer) | [<URL>](url.html#the-whatwg-url-api) destination filename of the copy operation
* `mode` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) Optional modifiers that specify the behavior of the copy
  operation. It is possible to create a mask consisting of the bitwise OR of
  two or more values (e.g.
  `fs.constants.COPYFILE_EXCL | fs.constants.COPYFILE_FICLONE`)
  **Default:** `0`.
  + `fs.constants.COPYFILE_EXCL`: The copy operation will fail if `dest`
    already exists.
  + `fs.constants.COPYFILE_FICLONE`: The copy operation will attempt to create
    a copy-on-write reflink. If the platform does not support copy-on-write,
    then a fallback copy mechanism is used.
  + `fs.constants.COPYFILE_FICLONE_FORCE`: The copy operation will attempt to
    create a copy-on-write reflink. If the platform does not support
    copy-on-write, then the operation will fail.
* Returns: [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) Fulfills with `undefined` upon success.

Asynchronously copies `src` to `dest`. By default, `dest` is overwritten if it
already exists.

No guarantees are made about the atomicity of the copy operation. If an
error occurs after the destination file has been opened for writing, an attempt
will be made to remove the destination.

```
import { copyFile, constants } from 'node:fs/promises';

try {
  await copyFile('source.txt', 'destination.txt');
  console.log('source.txt was copied to destination.txt');
} catch {
  console.error('The file could not be copied');
}


try {
  await copyFile('source.txt', 'destination.txt', constants.COPYFILE_EXCL);
  console.log('source.txt was copied to destination.txt');
} catch {
  console.error('The file could not be copied');
} copy
```

#### `fsPromises.cp(src, dest[, options])`[#](#fspromisescpsrc-dest-options)

* `src` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) | [<URL>](url.html#the-whatwg-url-api) source path to copy.
* `dest` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) | [<URL>](url.html#the-whatwg-url-api) destination path to copy to.
* `options` [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)
  + `dereference` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) dereference symlinks. **Default:** `false`.
  + `errorOnExist` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) when `force` is `false`, and the destination
    exists, throw an error. **Default:** `false`.
  + `filter` [<Function>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function) Function to filter copied files/directories. Return
    `true` to copy the item, `false` to ignore it. When ignoring a directory,
    all of its contents will be skipped as well. Can also return a `Promise`
    that resolves to `true` or `false` **Default:** `undefined`.
    - `src` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) source path to copy.
    - `dest` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) destination path to copy to.
    - Returns: [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) | [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) A value that is coercible to `boolean` or
      a `Promise` that fulfils with such value.
  + `force` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) overwrite existing file or directory. The copy
    operation will ignore errors if you set this to false and the destination
    exists. Use the `errorOnExist` option to change this behavior.
    **Default:** `true`.
  + `mode` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) modifiers for copy operation. **Default:** `0`.
    See `mode` flag of [`fsPromises.copyFile()`](#fspromisescopyfilesrc-dest-mode).
  + `preserveTimestamps` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) When `true` timestamps from `src` will
    be preserved. **Default:** `false`.
  + `recursive` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) copy directories recursively **Default:** `false`
  + `verbatimSymlinks` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) When `true`, path resolution for symlinks will
    be skipped. **Default:** `false`
* Returns: [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) Fulfills with `undefined` upon success.

Asynchronously copies the entire directory structure from `src` to `dest`,
including subdirectories and files.

When copying a directory to another directory, globs are not supported and
behavior is similar to `cp dir1/ dir2/`.

#### `fsPromises.lchmod(path, mode)`[#](#fspromiseslchmodpath-mode)

Deprecated since: v10.0.0

Changes the permissions on a symbolic link.

This method is only implemented on macOS.

#### `fsPromises.lchown(path, uid, gid)`[#](#fspromiseslchownpath-uid-gid)

Changes the ownership on a symbolic link.

#### `fsPromises.lutimes(path, atime, mtime)`[#](#fspromiseslutimespath-atime-mtime)

Added in: v14.5.0, v12.19.0

Changes the access and modification times of a file in the same way as
[`fsPromises.utimes()`](#fspromisesutimespath-atime-mtime), with the difference that if the path refers to a
symbolic link, then the link is not dereferenced: instead, the timestamps of
the symbolic link itself are changed.

#### `fsPromises.link(existingPath, newPath)`[#](#fspromiseslinkexistingpath-newpath)

Added in: v10.0.0

Creates a new link from the `existingPath` to the `newPath`. See the POSIX
[`link(2)`](http://man7.org/linux/man-pages/man2/link.2.html) documentation for more detail.

#### `fsPromises.lstat(path[, options])`[#](#fspromiseslstatpath-options)

Equivalent to [`fsPromises.stat()`](#fspromisesstatpath-options) unless `path` refers to a symbolic link,
in which case the link itself is stat-ed, not the file that it refers to.
Refer to the POSIX [`lstat(2)`](http://man7.org/linux/man-pages/man2/lstat.2.html) document for more detail.

#### `fsPromises.mkdir(path[, options])`[#](#fspromisesmkdirpath-options)

Added in: v10.0.0

Asynchronously creates a directory.

The optional `options` argument can be an integer specifying `mode` (permission
and sticky bits), or an object with a `mode` property and a `recursive`
property indicating whether parent directories should be created. Calling
`fsPromises.mkdir()` when `path` is a directory that exists results in a
rejection only when `recursive` is false.

```
import { mkdir } from 'node:fs/promises';

try {
  const projectFolder = new URL('./test/project/', import.meta.url);
  const createDir = await mkdir(projectFolder, { recursive: true });

  console.log(`created ${createDir}`);
} catch (err) {
  console.error(err.message);
}const { mkdir } = require('node:fs/promises');
const { join } = require('node:path');

async function makeDirectory() {
  const projectFolder = join(__dirname, 'test', 'project');
  const dirCreation = await mkdir(projectFolder, { recursive: true });

  console.log(dirCreation);
  return dirCreation;
}

makeDirectory().catch(console.error);copy
```

#### `fsPromises.mkdtemp(prefix[, options])`[#](#fspromisesmkdtempprefix-options)

Creates a unique temporary directory. A unique directory name is generated by
appending six random characters to the end of the provided `prefix`. Due to
platform inconsistencies, avoid trailing `X` characters in `prefix`. Some
platforms, notably the BSDs, can return more than six random characters, and
replace trailing `X` characters in `prefix` with random characters.

The optional `options` argument can be a string specifying an encoding, or an
object with an `encoding` property specifying the character encoding to use.

```
import { mkdtemp } from 'node:fs/promises';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

try {
  await mkdtemp(join(tmpdir(), 'foo-'));
} catch (err) {
  console.error(err);
} copy
```

The `fsPromises.mkdtemp()` method will append the six randomly selected
characters directly to the `prefix` string. For instance, given a directory
`/tmp`, if the intention is to create a temporary directory *within* `/tmp`, the
`prefix` must end with a trailing platform-specific path separator
(`require('node:path').sep`).

#### `fsPromises.mkdtempDisposable(prefix[, options])`[#](#fspromisesmkdtempdisposableprefix-options)

Added in: v24.4.0

The resulting Promise holds an async-disposable object whose `path` property
holds the created directory path. When the object is disposed, the directory
and its contents will be removed asynchronously if it still exists. If the
directory cannot be deleted, disposal will throw an error. The object has an
async `remove()` method which will perform the same task.

Both this function and the disposal function on the resulting object are
async, so it should be used with `await` + `await using` as in
`await using dir = await fsPromises.mkdtempDisposable('prefix')`.

For detailed information, see the documentation of [`fsPromises.mkdtemp()`](#fspromisesmkdtempprefix-options).

The optional `options` argument can be a string specifying an encoding, or an
object with an `encoding` property specifying the character encoding to use.

#### `fsPromises.open(path, flags[, mode])`[#](#fspromisesopenpath-flags-mode)

Opens a [<FileHandle>](fs.html#class-filehandle).

Refer to the POSIX [`open(2)`](http://man7.org/linux/man-pages/man2/open.2.html) documentation for more detail.

Some characters (`< > : " / \ | ? *`) are reserved under Windows as documented
by [Naming Files, Paths, and Namespaces](https://docs.microsoft.com/en-us/windows/desktop/FileIO/naming-a-file). Under NTFS, if the filename contains
a colon, Node.js will open a file system stream, as described by
[this MSDN page](https://docs.microsoft.com/en-us/windows/desktop/FileIO/using-streams).

#### `fsPromises.opendir(path[, options])`[#](#fspromisesopendirpath-options)

Asynchronously open a directory for iterative scanning. See the POSIX
[`opendir(3)`](http://man7.org/linux/man-pages/man3/opendir.3.html) documentation for more detail.

Creates an [<fs.Dir>](fs.html#class-fsdir), which contains all further functions for reading from
and cleaning up the directory.

The `encoding` option sets the encoding for the `path` while opening the
directory and subsequent read operations.

Example using async iteration:

```
import { opendir } from 'node:fs/promises';

try {
  const dir = await opendir('./');
  for await (const dirent of dir)
    console.log(dirent.name);
} catch (err) {
  console.error(err);
} copy
```

When using the async iterator, the [<fs.Dir>](fs.html#class-fsdir) object will be automatically
closed after the iterator exits.

#### `fsPromises.readdir(path[, options])`[#](#fspromisesreaddirpath-options)

* `path` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) | [<Buffer>](buffer.html#class-buffer) | [<URL>](url.html#the-whatwg-url-api)
* `options` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) | [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)
  + `encoding` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) **Default:** `'utf8'`
  + `withFileTypes` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) **Default:** `false`
  + `recursive` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) If `true`, reads the contents of a directory
    recursively. In recursive mode, it will list all files, sub files, and
    directories. **Default:** `false`.
* Returns: [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) Fulfills with an array of the names of the files in
  the directory excluding `'.'` and `'..'`.

Reads the contents of a directory.

The optional `options` argument can be a string specifying an encoding, or an
object with an `encoding` property specifying the character encoding to use for
the filenames. If the `encoding` is set to `'buffer'`, the filenames returned
will be passed as [<Buffer>](buffer.html#class-buffer) objects.

If `options.withFileTypes` is set to `true`, the returned array will contain
[<fs.Dirent>](fs.html#class-fsdirent) objects.

```
import { readdir } from 'node:fs/promises';

try {
  const files = await readdir(path);
  for (const file of files)
    console.log(file);
} catch (err) {
  console.error(err);
} copy
```

#### `fsPromises.readFile(path[, options])`[#](#fspromisesreadfilepath-options)

Asynchronously reads the entire contents of a file.

If no encoding is specified (using `options.encoding`), the data is returned
as a [<Buffer>](buffer.html#class-buffer) object. Otherwise, the data will be a string.

If `options` is a string, then it specifies the encoding.

When the `path` is a directory, the behavior of `fsPromises.readFile()` is
platform-specific. On macOS, Linux, and Windows, the promise will be rejected
with an error. On FreeBSD, a representation of the directory's contents will be
returned.

An example of reading a `package.json` file located in the same directory of the
running code:

```
import { readFile } from 'node:fs/promises';
try {
  const filePath = new URL('./package.json', import.meta.url);
  const contents = await readFile(filePath, { encoding: 'utf8' });
  console.log(contents);
} catch (err) {
  console.error(err.message);
}const { readFile } = require('node:fs/promises');
const { resolve } = require('node:path');
async function logFile() {
  try {
    const filePath = resolve('./package.json');
    const contents = await readFile(filePath, { encoding: 'utf8' });
    console.log(contents);
  } catch (err) {
    console.error(err.message);
  }
}
logFile();copy
```

It is possible to abort an ongoing `readFile` using an [<AbortSignal>](globals.html#class-abortsignal). If a
request is aborted the promise returned is rejected with an `AbortError`:

```
import { readFile } from 'node:fs/promises';

try {
  const controller = new AbortController();
  const { signal } = controller;
  const promise = readFile(fileName, { signal });

  
  controller.abort();

  await promise;
} catch (err) {
  
  console.error(err);
} copy
```

Aborting an ongoing request does not abort individual operating
system requests but rather the internal buffering `fs.readFile` performs.

Any specified [<FileHandle>](fs.html#class-filehandle) has to support reading.

#### `fsPromises.readlink(path[, options])`[#](#fspromisesreadlinkpath-options)

Added in: v10.0.0

Reads the contents of the symbolic link referred to by `path`. See the POSIX
[`readlink(2)`](http://man7.org/linux/man-pages/man2/readlink.2.html) documentation for more detail. The promise is fulfilled with the
`linkString` upon success.

The optional `options` argument can be a string specifying an encoding, or an
object with an `encoding` property specifying the character encoding to use for
the link path returned. If the `encoding` is set to `'buffer'`, the link path
returned will be passed as a [<Buffer>](buffer.html#class-buffer) object.

#### `fsPromises.realpath(path[, options])`[#](#fspromisesrealpathpath-options)

Added in: v10.0.0

Determines the actual location of `path` using the same semantics as the
`fs.realpath.native()` function.

Only paths that can be converted to UTF8 strings are supported.

The optional `options` argument can be a string specifying an encoding, or an
object with an `encoding` property specifying the character encoding to use for
the path. If the `encoding` is set to `'buffer'`, the path returned will be
passed as a [<Buffer>](buffer.html#class-buffer) object.

On Linux, when Node.js is linked against musl libc, the procfs file system must
be mounted on `/proc` in order for this function to work. Glibc does not have
this restriction.

#### `fsPromises.rename(oldPath, newPath)`[#](#fspromisesrenameoldpath-newpath)

Added in: v10.0.0

Renames `oldPath` to `newPath`.

#### `fsPromises.rmdir(path[, options])`[#](#fspromisesrmdirpath-options)

* `path` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) | [<Buffer>](buffer.html#class-buffer) | [<URL>](url.html#the-whatwg-url-api)
* `options` [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)
  + `maxRetries` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) If an `EBUSY`, `EMFILE`, `ENFILE`, `ENOTEMPTY`, or
    `EPERM` error is encountered, Node.js retries the operation with a linear
    backoff wait of `retryDelay` milliseconds longer on each try. This option
    represents the number of retries. This option is ignored if the `recursive`
    option is not `true`. **Default:** `0`.
  + `recursive` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) If `true`, perform a recursive directory removal. In
    recursive mode, operations are retried on failure. **Default:** `false`.
    **Deprecated.**
  + `retryDelay` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) The amount of time in milliseconds to wait between
    retries. This option is ignored if the `recursive` option is not `true`.
    **Default:** `100`.
* Returns: [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) Fulfills with `undefined` upon success.

Removes the directory identified by `path`.

Using `fsPromises.rmdir()` on a file (not a directory) results in the
promise being rejected with an `ENOENT` error on Windows and an `ENOTDIR`
error on POSIX.

To get a behavior similar to the `rm -rf` Unix command, use
[`fsPromises.rm()`](#fspromisesrmpath-options) with options `{ recursive: true, force: true }`.

#### `fsPromises.rm(path[, options])`[#](#fspromisesrmpath-options)

Added in: v14.14.0

* `path` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) | [<Buffer>](buffer.html#class-buffer) | [<URL>](url.html#the-whatwg-url-api)
* `options` [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)
  + `force` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) When `true`, exceptions will be ignored if `path` does
    not exist. **Default:** `false`.
  + `maxRetries` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) If an `EBUSY`, `EMFILE`, `ENFILE`, `ENOTEMPTY`, or
    `EPERM` error is encountered, Node.js will retry the operation with a linear
    backoff wait of `retryDelay` milliseconds longer on each try. This option
    represents the number of retries. This option is ignored if the `recursive`
    option is not `true`. **Default:** `0`.
  + `recursive` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) If `true`, perform a recursive directory removal. In
    recursive mode operations are retried on failure. **Default:** `false`.
  + `retryDelay` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) The amount of time in milliseconds to wait between
    retries. This option is ignored if the `recursive` option is not `true`.
    **Default:** `100`.
* Returns: [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) Fulfills with `undefined` upon success.

Removes files and directories (modeled on the standard POSIX `rm` utility).

#### `fsPromises.stat(path[, options])`[#](#fspromisesstatpath-options)

#### `fsPromises.statfs(path[, options])`[#](#fspromisesstatfspath-options)

Added in: v19.6.0, v18.15.0

#### `fsPromises.symlink(target, path[, type])`[#](#fspromisessymlinktarget-path-type)

Creates a symbolic link.

The `type` argument is only used on Windows platforms and can be one of `'dir'`,
`'file'`, or `'junction'`. If the `type` argument is `null`, Node.js will
autodetect `target` type and use `'file'` or `'dir'`. If the `target` does not
exist, `'file'` will be used. Windows junction points require the destination
path to be absolute. When using `'junction'`, the `target` argument will
automatically be normalized to absolute path. Junction points on NTFS volumes
can only point to directories.

#### `fsPromises.truncate(path[, len])`[#](#fspromisestruncatepath-len)

Added in: v10.0.0

Truncates (shortens or extends the length) of the content at `path` to `len`
bytes.

#### `fsPromises.unlink(path)`[#](#fspromisesunlinkpath)

Added in: v10.0.0

If `path` refers to a symbolic link, then the link is removed without affecting
the file or directory to which that link refers. If the `path` refers to a file
path that is not a symbolic link, the file is deleted. See the POSIX [`unlink(2)`](http://man7.org/linux/man-pages/man2/unlink.2.html)
documentation for more detail.

#### `fsPromises.utimes(path, atime, mtime)`[#](#fspromisesutimespath-atime-mtime)

Added in: v10.0.0

Change the file system timestamps of the object referenced by `path`.

The `atime` and `mtime` arguments follow these rules:

* Values can be either numbers representing Unix epoch time, `Date`s, or a
  numeric string like `'123456789.0'`.
* If the value can not be converted to a number, or is `NaN`, `Infinity`, or
  `-Infinity`, an `Error` will be thrown.

#### `fsPromises.watch(filename[, options])`[#](#fspromiseswatchfilename-options)

Added in: v15.9.0, v14.18.0

* `filename` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) | [<Buffer>](buffer.html#class-buffer) | [<URL>](url.html#the-whatwg-url-api)
* `options` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) | [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)
  + `persistent` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) Indicates whether the process should continue to run
    as long as files are being watched. **Default:** `true`.
  + `recursive` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) Indicates whether all subdirectories should be
    watched, or only the current directory. This applies when a directory is
    specified, and only on supported platforms (See [caveats](#caveats)). **Default:**
    `false`.
  + `encoding` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) Specifies the character encoding to be used for the
    filename passed to the listener. **Default:** `'utf8'`.
  + `signal` [<AbortSignal>](globals.html#class-abortsignal) An [<AbortSignal>](globals.html#class-abortsignal) used to signal when the watcher
    should stop.
  + `maxQueue` [<number>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) Specifies the number of events to queue between iterations
    of the [<AsyncIterator>](https://tc39.github.io/ecma262/#sec-asynciterator-interface) returned. **Default:** `2048`.
  + `overflow` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) Either `'ignore'` or `'throw'` when there are more events to be
    queued than `maxQueue` allows. `'ignore'` means overflow events are dropped and a
    warning is emitted, while `'throw'` means to throw an exception. **Default:** `'ignore'`.
* Returns: [<AsyncIterator>](https://tc39.github.io/ecma262/#sec-asynciterator-interface) of objects with the properties:

Returns an async iterator that watches for changes on `filename`, where `filename`
is either a file or a directory.

```
const { watch } = require('node:fs/promises');

const ac = new AbortController();
const { signal } = ac;
setTimeout(() => ac.abort(), 10000);

(async () => {
  try {
    const watcher = watch(__filename, { signal });
    for await (const event of watcher)
      console.log(event);
  } catch (err) {
    if (err.name === 'AbortError')
      return;
    throw err;
  }
})(); copy
```

On most platforms, `'rename'` is emitted whenever a filename appears or
disappears in the directory.

All the [caveats](#caveats) for `fs.watch()` also apply to `fsPromises.watch()`.

#### `fsPromises.writeFile(file, data[, options])`[#](#fspromiseswritefilefile-data-options)

Asynchronously writes data to a file, replacing the file if it already exists.
`data` can be a string, a buffer, an [<AsyncIterable>](https://tc39.github.io/ecma262/#sec-asynciterable-interface), or an [<Iterable>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Iteration_protocols#The_iterable_protocol) object.

The `encoding` option is ignored if `data` is a buffer.

If `options` is a string, then it specifies the encoding.

The `mode` option only affects the newly created file. See [`fs.open()`](#fsopenpath-flags-mode-callback)
for more details.

Any specified [<FileHandle>](fs.html#class-filehandle) has to support writing.

It is unsafe to use `fsPromises.writeFile()` multiple times on the same file
without waiting for the promise to be settled.

Similarly to `fsPromises.readFile` - `fsPromises.writeFile` is a convenience
method that performs multiple `write` calls internally to write the buffer
passed to it. For performance sensitive code consider using
[`fs.createWriteStream()`](#fscreatewritestreampath-options) or [`filehandle.createWriteStream()`](#filehandlecreatewritestreamoptions).

It is possible to use an [<AbortSignal>](globals.html#class-abortsignal) to cancel an `fsPromises.writeFile()`.
Cancelation is "best effort", and some amount of data is likely still
to be written.

```
import { writeFile } from 'node:fs/promises';
import { Buffer } from 'node:buffer';

try {
  const controller = new AbortController();
  const { signal } = controller;
  const data = new Uint8Array(Buffer.from('Hello Node.js'));
  const promise = writeFile('message.txt', data, { signal });

  
  controller.abort();

  await promise;
} catch (err) {
  
  console.error(err);
} copy
```

Aborting an ongoing request does not abort individual operating
system requests but rather the internal buffering `fs.writeFile` performs.

#### `fsPromises.constants`[#](#fspromisesconstants)

Added in: v18.4.0, v16.17.0

Returns an object containing commonly used constants for file system
operations. The object is the same as `fs.constants`. See [FS constants](#fs-constants)
for more details.

### Callback API[#](#callback-api)

The callback APIs perform all operations asynchronously, without blocking the
event loop, then invoke a callback function upon completion or error.

The callback APIs use the underlying Node.js threadpool to perform file
system operations off the event loop thread. These operations are not
synchronized or threadsafe. Care must be taken when performing multiple
concurrent modifications on the same file or data corruption may occur.

#### `fs.access(path[, mode], callback)`[#](#fsaccesspath-mode-callback)

Tests a user's permissions for the file or directory specified by `path`.
The `mode` argument is an optional integer that specifies the accessibility
checks to be performed. `mode` should be either the value `fs.constants.F_OK`
or a mask consisting of the bitwise OR of any of `fs.constants.R_OK`,
`fs.constants.W_OK`, and `fs.constants.X_OK` (e.g.
`fs.constants.W_OK | fs.constants.R_OK`). Check [File access constants](#file-access-constants) for
possible values of `mode`.

The final argument, `callback`, is a callback function that is invoked with
a possible error argument. If any of the accessibility checks fail, the error
argument will be an `Error` object. The following examples check if
`package.json` exists, and if it is readable or writable.

```
import { access, constants } from 'node:fs';

const file = 'package.json';


access(file, constants.F_OK, (err) => {
  console.log(`${file} ${err ? 'does not exist' : 'exists'}`);
});


access(file, constants.R_OK, (err) => {
  console.log(`${file} ${err ? 'is not readable' : 'is readable'}`);
});


access(file, constants.W_OK, (err) => {
  console.log(`${file} ${err ? 'is not writable' : 'is writable'}`);
});


access(file, constants.R_OK | constants.W_OK, (err) => {
  console.log(`${file} ${err ? 'is not' : 'is'} readable and writable`);
}); copy
```

Do not use `fs.access()` to check for the accessibility of a file before calling
`fs.open()`, `fs.readFile()`, or `fs.writeFile()`. Doing
so introduces a race condition, since other processes may change the file's
state between the two calls. Instead, user code should open/read/write the
file directly and handle the error raised if the file is not accessible.

**write (NOT RECOMMENDED)**

```
import { access, open, close } from 'node:fs';

access('myfile', (err) => {
  if (!err) {
    console.error('myfile already exists');
    return;
  }

  open('myfile', 'wx', (err, fd) => {
    if (err) throw err;

    try {
      writeMyData(fd);
    } finally {
      close(fd, (err) => {
        if (err) throw err;
      });
    }
  });
}); copy
```

**write (RECOMMENDED)**

```
import { open, close } from 'node:fs';

open('myfile', 'wx', (err, fd) => {
  if (err) {
    if (err.code === 'EEXIST') {
      console.error('myfile already exists');
      return;
    }

    throw err;
  }

  try {
    writeMyData(fd);
  } finally {
    close(fd, (err) => {
      if (err) throw err;
    });
  }
}); copy
```

**read (NOT RECOMMENDED)**

```
import { access, open, close } from 'node:fs';
access('myfile', (err) => {
  if (err) {
    if (err.code === 'ENOENT') {
      console.error('myfile does not exist');
      return;
    }

    throw err;
  }

  open('myfile', 'r', (err, fd) => {
    if (err) throw err;

    try {
      readMyData(fd);
    } finally {
      close(fd, (err) => {
        if (err) throw err;
      });
    }
  });
}); copy
```

**read (RECOMMENDED)**

```
import { open, close } from 'node:fs';

open('myfile', 'r', (err, fd) => {
  if (err) {
    if (err.code === 'ENOENT') {
      console.error('myfile does not exist');
      return;
    }

    throw err;
  }

  try {
    readMyData(fd);
  } finally {
    close(fd, (err) => {
      if (err) throw err;
    });
  }
}); copy
```

The "not recommended" examples above check for accessibility and then use the
file; the "recommended" examples are better because they use the file directly
and handle the error, if any.

In general, check for the accessibility of a file only if the file will not be
used directly, for example when its accessibility is a signal from another
process.

On Windows, access-control policies (ACLs) on a directory may limit access to
a file or directory. The `fs.access()` function, however, does not check the
ACL and therefore may report that a path is accessible even if the ACL restricts
the user from reading or writing to it.

#### `fs.appendFile(path, data[, options], callback)`[#](#fsappendfilepath-data-options-callback)

Asynchronously append data to a file, creating the file if it does not yet
exist. `data` can be a string or a [<Buffer>](buffer.html#class-buffer).

The `mode` option only affects the newly created file. See [`fs.open()`](#fsopenpath-flags-mode-callback)
for more details.

```
import { appendFile } from 'node:fs';

appendFile('message.txt', 'data to append', (err) => {
  if (err) throw err;
  console.log('The "data to append" was appended to file!');
}); copy
```

If `options` is a string, then it specifies the encoding:

```
import { appendFile } from 'node:fs';

appendFile('message.txt', 'data to append', 'utf8', callback); copy
```

The `path` may be specified as a numeric file descriptor that has been opened
for appending (using `fs.open()` or `fs.openSync()`). The file descriptor will
not be closed automatically.

```
import { open, close, appendFile } from 'node:fs';

function closeFd(fd) {
  close(fd, (err) => {
    if (err) throw err;
  });
}

open('message.txt', 'a', (err, fd) => {
  if (err) throw err;

  try {
    appendFile(fd, 'data to append', 'utf8', (err) => {
      closeFd(fd);
      if (err) throw err;
    });
  } catch (err) {
    closeFd(fd);
    throw err;
  }
}); copy
```

#### `fs.chmod(path, mode, callback)`[#](#fschmodpath-mode-callback)

Asynchronously changes the permissions of a file. No arguments other than a
possible exception are given to the completion callback.

See the POSIX [`chmod(2)`](http://man7.org/linux/man-pages/man2/chmod.2.html) documentation for more detail.

```
import { chmod } from 'node:fs';

chmod('my_file.txt', 0o775, (err) => {
  if (err) throw err;
  console.log('The permissions for file "my_file.txt" have been changed!');
}); copy
```

##### File modes[#](#file-modes)

The `mode` argument used in both the `fs.chmod()` and `fs.chmodSync()`
methods is a numeric bitmask created using a logical OR of the following
constants:

| Constant | Octal | Description |
| --- | --- | --- |
| `fs.constants.S_IRUSR` | `0o400` | read by owner |
| `fs.constants.S_IWUSR` | `0o200` | write by owner |
| `fs.constants.S_IXUSR` | `0o100` | execute/search by owner |
| `fs.constants.S_IRGRP` | `0o40` | read by group |
| `fs.constants.S_IWGRP` | `0o20` | write by group |
| `fs.constants.S_IXGRP` | `0o10` | execute/search by group |
| `fs.constants.S_IROTH` | `0o4` | read by others |
| `fs.constants.S_IWOTH` | `0o2` | write by others |
| `fs.constants.S_IXOTH` | `0o1` | execute/search by others |

An easier method of constructing the `mode` is to use a sequence of three
octal digits (e.g. `765`). The left-most digit (`7` in the example), specifies
the permissions for the file owner. The middle digit (`6` in the example),
specifies permissions for the group. The right-most digit (`5` in the example),
specifies the permissions for others.

| Number | Description |
| --- | --- |
| `7` | read, write, and execute |
| `6` | read and write |
| `5` | read and execute |
| `4` | read only |
| `3` | write and execute |
| `2` | write only |
| `1` | execute only |
| `0` | no permission |

For example, the octal value `0o765` means:

* The owner may read, write, and execute the file.
* The group may read and write the file.
* Others may read and execute the file.

When using raw numbers where file modes are expected, any value larger than
`0o777` may result in platform-specific behaviors that are not supported to work
consistently. Therefore constants like `S_ISVTX`, `S_ISGID`, or `S_ISUID` are
not exposed in `fs.constants`.

Caveats: on Windows only the write permission can be changed, and the
distinction among the permissions of group, owner, or others is not
implemented.

#### `fs.chown(path, uid, gid, callback)`[#](#fschownpath-uid-gid-callback)

Asynchronously changes owner and group of a file. No arguments other than a
possible exception are given to the completion callback.

See the POSIX [`chown(2)`](http://man7.org/linux/man-pages/man2/chown.2.html) documentation for more detail.

#### `fs.close(fd[, callback])`[#](#fsclosefd-callback)

Closes the file descriptor. No arguments other than a possible exception are
given to the completion callback.

Calling `fs.close()` on any file descriptor (`fd`) that is currently in use
through any other `fs` operation may lead to undefined behavior.

See the POSIX [`close(2)`](http://man7.org/linux/man-pages/man2/close.2.html) documentation for more detail.

#### `fs.copyFile(src, dest[, mode], callback)`[#](#fscopyfilesrc-dest-mode-callback)

Asynchronously copies `src` to `dest`. By default, `dest` is overwritten if it
already exists. No arguments other than a possible exception are given to the
callback function. Node.js makes no guarantees about the atomicity of the copy
operation. If an error occurs after the destination file has been opened for
writing, Node.js will attempt to remove the destination.

`mode` is an optional integer that specifies the behavior
of the copy operation. It is possible to create a mask consisting of the bitwise
OR of two or more values (e.g.
`fs.constants.COPYFILE_EXCL | fs.constants.COPYFILE_FICLONE`).

* `fs.constants.COPYFILE_EXCL`: The copy operation will fail if `dest` already
  exists.
* `fs.constants.COPYFILE_FICLONE`: The copy operation will attempt to create a
  copy-on-write reflink. If the platform does not support copy-on-write, then a
  fallback copy mechanism is used.
* `fs.constants.COPYFILE_FICLONE_FORCE`: The copy operation will attempt to
  create a copy-on-write reflink. If the platform does not support
  copy-on-write, then the operation will fail.

```
import { copyFile, constants } from 'node:fs';

function callback(err) {
  if (err) throw err;
  console.log('source.txt was copied to destination.txt');
}


copyFile('source.txt', 'destination.txt', callback);


copyFile('source.txt', 'destination.txt', constants.COPYFILE_EXCL, callback); copy
```

#### `fs.cp(src, dest[, options], callback)`[#](#fscpsrc-dest-options-callback)

* `src` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) | [<URL>](url.html#the-whatwg-url-api) source path to copy.
* `dest` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) | [<URL>](url.html#the-whatwg-url-api) destination path to copy to.
* `options` [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)
  + `dereference` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) dereference symlinks. **Default:** `false`.
  + `errorOnExist` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) when `force` is `false`, and the destination
    exists, throw an error. **Default:** `false`.
  + `filter` [<Function>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function) Function to filter copied files/directories. Return
    `true` to copy the item, `false` to ignore it. When ignoring a directory,
    all of its contents will be skipped as well. Can also return a `Promise`
    that resolves to `true` or `false` **Default:** `undefined`.
    - `src` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) source path to copy.
    - `dest` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) destination path to copy to.
    - Returns: [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) | [<Promise>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) A value that is coercible to `boolean` or
      a `Promise` that fulfils with such value.
  + `force` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) overwrite existing file or directory. The copy
    operation will ignore errors if you set this to false and the destination
    exists. Use the `errorOnExist` option to change this behavior.
    **Default:** `true`.
  + `mode` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) modifiers for copy operation. **Default:** `0`.
    See `mode` flag of [`fs.copyFile()`](#fscopyfilesrc-dest-mode-callback).
  + `preserveTimestamps` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) When `true` timestamps from `src` will
    be preserved. **Default:** `false`.
  + `recursive` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) copy directories recursively **Default:** `false`
  + `verbatimSymlinks` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) When `true`, path resolution for symlinks will
    be skipped. **Default:** `false`
* `callback` [<Function>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function)

Asynchronously copies the entire directory structure from `src` to `dest`,
including subdirectories and files.

When copying a directory to another directory, globs are not supported and
behavior is similar to `cp dir1/ dir2/`.

#### `fs.createReadStream(path[, options])`[#](#fscreatereadstreampath-options)

`options` can include `start` and `end` values to read a range of bytes from
the file instead of the entire file. Both `start` and `end` are inclusive and
start counting at 0, allowed values are in the
[0, [`Number.MAX_SAFE_INTEGER`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER)] range. If `fd` is specified and `start` is
omitted or `undefined`, `fs.createReadStream()` reads sequentially from the
current file position. The `encoding` can be any one of those accepted by
[<Buffer>](buffer.html#class-buffer).

If `fd` is specified, `ReadStream` will ignore the `path` argument and will use
the specified file descriptor. This means that no `'open'` event will be
emitted. `fd` should be blocking; non-blocking `fd`s should be passed to
[<net.Socket>](net.html#class-netsocket).

If `fd` points to a character device that only supports blocking reads
(such as keyboard or sound card), read operations do not finish until data is
available. This can prevent the process from exiting and the stream from
closing naturally.

By default, the stream will emit a `'close'` event after it has been
destroyed. Set the `emitClose` option to `false` to change this behavior.

By providing the `fs` option, it is possible to override the corresponding `fs`
implementations for `open`, `read`, and `close`. When providing the `fs` option,
an override for `read` is required. If no `fd` is provided, an override for
`open` is also required. If `autoClose` is `true`, an override for `close` is
also required.

```
import { createReadStream } from 'node:fs';


const stream = createReadStream('/dev/input/event0');
setTimeout(() => {
  stream.close(); 
  
  
  
  
  
  stream.push(null);
  stream.read(0);
}, 100); copy
```

If `autoClose` is false, then the file descriptor won't be closed, even if
there's an error. It is the application's responsibility to close it and make
sure there's no file descriptor leak. If `autoClose` is set to true (default
behavior), on `'error'` or `'end'` the file descriptor will be closed
automatically.

`mode` sets the file mode (permission and sticky bits), but only if the
file was created.

An example to read the last 10 bytes of a file which is 100 bytes long:

```
import { createReadStream } from 'node:fs';

createReadStream('sample.txt', { start: 90, end: 99 }); copy
```

If `options` is a string, then it specifies the encoding.

#### `fs.createWriteStream(path[, options])`[#](#fscreatewritestreampath-options)

`options` may also include a `start` option to allow writing data at some
position past the beginning of the file, allowed values are in the
[0, [`Number.MAX_SAFE_INTEGER`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER)] range. Modifying a file rather than
replacing it may require the `flags` option to be set to `r+` rather than the
default `w`. The `encoding` can be any one of those accepted by [<Buffer>](buffer.html#class-buffer).

If `autoClose` is set to true (default behavior) on `'error'` or `'finish'`
the file descriptor will be closed automatically. If `autoClose` is false,
then the file descriptor won't be closed, even if there's an error.
It is the application's responsibility to close it and make sure there's no
file descriptor leak.

By default, the stream will emit a `'close'` event after it has been
destroyed. Set the `emitClose` option to `false` to change this behavior.

By providing the `fs` option it is possible to override the corresponding `fs`
implementations for `open`, `write`, `writev`, and `close`. Overriding `write()`
without `writev()` can reduce performance as some optimizations (`_writev()`)
will be disabled. When providing the `fs` option, overrides for at least one of
`write` and `writev` are required. If no `fd` option is supplied, an override
for `open` is also required. If `autoClose` is `true`, an override for `close`
is also required.

Like [<fs.ReadStream>](fs.html#class-fsreadstream), if `fd` is specified, [<fs.WriteStream>](fs.html#class-fswritestream) will ignore the
`path` argument and will use the specified file descriptor. This means that no
`'open'` event will be emitted. `fd` should be blocking; non-blocking `fd`s
should be passed to [<net.Socket>](net.html#class-netsocket).

If `options` is a string, then it specifies the encoding.

#### `fs.exists(path, callback)`[#](#fsexistspath-callback)

Test whether or not the element at the given `path` exists by checking with the file system.
Then call the `callback` argument with either true or false:

```
import { exists } from 'node:fs';

exists('/etc/passwd', (e) => {
  console.log(e ? 'it exists' : 'no passwd!');
}); copy
```

**The parameters for this callback are not consistent with other Node.js
callbacks.** Normally, the first parameter to a Node.js callback is an `err`
parameter, optionally followed by other parameters. The `fs.exists()` callback
has only one boolean parameter. This is one reason `fs.access()` is recommended
instead of `fs.exists()`.

If `path` is a symbolic link, it is followed. Thus, if `path` exists but points
to a non-existent element, the callback will receive the value `false`.

Using `fs.exists()` to check for the existence of a file before calling
`fs.open()`, `fs.readFile()`, or `fs.writeFile()` is not recommended. Doing
so introduces a race condition, since other processes may change the file's
state between the two calls. Instead, user code should open/read/write the
file directly and handle the error raised if the file does not exist.

**write (NOT RECOMMENDED)**

```
import { exists, open, close } from 'node:fs';

exists('myfile', (e) => {
  if (e) {
    console.error('myfile already exists');
  } else {
    open('myfile', 'wx', (err, fd) => {
      if (err) throw err;

      try {
        writeMyData(fd);
      } finally {
        close(fd, (err) => {
          if (err) throw err;
        });
      }
    });
  }
}); copy
```

**write (RECOMMENDED)**

```
import { open, close } from 'node:fs';
open('myfile', 'wx', (err, fd) => {
  if (err) {
    if (err.code === 'EEXIST') {
      console.error('myfile already exists');
      return;
    }

    throw err;
  }

  try {
    writeMyData(fd);
  } finally {
    close(fd, (err) => {
      if (err) throw err;
    });
  }
}); copy
```

**read (NOT RECOMMENDED)**

```
import { open, close, exists } from 'node:fs';

exists('myfile', (e) => {
  if (e) {
    open('myfile', 'r', (err, fd) => {
      if (err) throw err;

      try {
        readMyData(fd);
      } finally {
        close(fd, (err) => {
          if (err) throw err;
        });
      }
    });
  } else {
    console.error('myfile does not exist');
  }
}); copy
```

**read (RECOMMENDED)**

```
import { open, close } from 'node:fs';

open('myfile', 'r', (err, fd) => {
  if (err) {
    if (err.code === 'ENOENT') {
      console.error('myfile does not exist');
      return;
    }

    throw err;
  }

  try {
    readMyData(fd);
  } finally {
    close(fd, (err) => {
      if (err) throw err;
    });
  }
}); copy
```

The "not recommended" examples above check for existence and then use the
file; the "recommended" examples are better because they use the file directly
and handle the error, if any.

In general, check for the existence of a file only if the file won't be
used directly, for example when its existence is a signal from another
process.

#### `fs.fchmod(fd, mode, callback)`[#](#fsfchmodfd-mode-callback)

Sets the permissions on the file. No arguments other than a possible exception
are given to the completion callback.

See the POSIX [`fchmod(2)`](http://man7.org/linux/man-pages/man2/fchmod.2.html) documentation for more detail.

#### `fs.fchown(fd, uid, gid, callback)`[#](#fsfchownfd-uid-gid-callback)

Sets the owner of the file. No arguments other than a possible exception are
given to the completion callback.

See the POSIX [`fchown(2)`](http://man7.org/linux/man-pages/man2/fchown.2.html) documentation for more detail.

#### `fs.fdatasync(fd, callback)`[#](#fsfdatasyncfd-callback)

Forces all currently queued I/O operations associated with the file to the
operating system's synchronized I/O completion state. Refer to the POSIX
[`fdatasync(2)`](http://man7.org/linux/man-pages/man2/fdatasync.2.html) documentation for details. No arguments other than a possible
exception are given to the completion callback.

#### `fs.fstat(fd[, options], callback)`[#](#fsfstatfd-options-callback)

Invokes the callback with the [<fs.Stats>](fs.html#class-fsstats) for the file descriptor.

See the POSIX [`fstat(2)`](http://man7.org/linux/man-pages/man2/fstat.2.html) documentation for more detail.

#### `fs.fsync(fd, callback)`[#](#fsfsyncfd-callback)

Request that all data for the open file descriptor is flushed to the storage
device. The specific implementation is operating system and device specific.
Refer to the POSIX [`fsync(2)`](http://man7.org/linux/man-pages/man2/fsync.2.html) documentation for more detail. No arguments other
than a possible exception are given to the completion callback.

#### `fs.ftruncate(fd[, len], callback)`[#](#fsftruncatefd-len-callback)

Truncates the file descriptor. No arguments other than a possible exception are
given to the completion callback.

See the POSIX [`ftruncate(2)`](http://man7.org/linux/man-pages/man2/ftruncate.2.html) documentation for more detail.

If the file referred to by the file descriptor was larger than `len` bytes, only
the first `len` bytes will be retained in the file.

For example, the following program retains only the first four bytes of the
file:

```
import { open, close, ftruncate } from 'node:fs';

function closeFd(fd) {
  close(fd, (err) => {
    if (err) throw err;
  });
}

open('temp.txt', 'r+', (err, fd) => {
  if (err) throw err;

  try {
    ftruncate(fd, 4, (err) => {
      closeFd(fd);
      if (err) throw err;
    });
  } catch (err) {
    closeFd(fd);
    if (err) throw err;
  }
}); copy
```

If the file previously was shorter than `len` bytes, it is extended, and the
extended part is filled with null bytes (`'\0'`):

If `len` is negative then `0` will be used.

#### `fs.futimes(fd, atime, mtime, callback)`[#](#fsfutimesfd-atime-mtime-callback)

Change the file system timestamps of the object referenced by the supplied file
descriptor. See [`fs.utimes()`](#fsutimespath-atime-mtime-callback).

#### `fs.lchmod(path, mode, callback)`[#](#fslchmodpath-mode-callback)

Changes the permissions on a symbolic link. No arguments other than a possible
exception are given to the completion callback.

This method is only implemented on macOS.

See the POSIX [`lchmod(2)`](https://www.freebsd.org/cgi/man.cgi?query=lchmod&sektion=2) documentation for more detail.

#### `fs.lchown(path, uid, gid, callback)`[#](#fslchownpath-uid-gid-callback)

Set the owner of the symbolic link. No arguments other than a possible
exception are given to the completion callback.

See the POSIX [`lchown(2)`](http://man7.org/linux/man-pages/man2/lchown.2.html) documentation for more detail.

#### `fs.lutimes(path, atime, mtime, callback)`[#](#fslutimespath-atime-mtime-callback)

Changes the access and modification times of a file in the same way as
[`fs.utimes()`](#fsutimespath-atime-mtime-callback), with the difference that if the path refers to a symbolic
link, then the link is not dereferenced: instead, the timestamps of the
symbolic link itself are changed.

No arguments other than a possible exception are given to the completion
callback.

#### `fs.link(existingPath, newPath, callback)`[#](#fslinkexistingpath-newpath-callback)

Creates a new link from the `existingPath` to the `newPath`. See the POSIX
[`link(2)`](http://man7.org/linux/man-pages/man2/link.2.html) documentation for more detail. No arguments other than a possible
exception are given to the completion callback.

#### `fs.lstat(path[, options], callback)`[#](#fslstatpath-options-callback)

Retrieves the [<fs.Stats>](fs.html#class-fsstats) for the symbolic link referred to by the path.
The callback gets two arguments `(err, stats)` where `stats` is a [<fs.Stats>](fs.html#class-fsstats)
object. `lstat()` is identical to `stat()`, except that if `path` is a symbolic
link, then the link itself is stat-ed, not the file that it refers to.

See the POSIX [`lstat(2)`](http://man7.org/linux/man-pages/man2/lstat.2.html) documentation for more details.

#### `fs.mkdir(path[, options], callback)`[#](#fsmkdirpath-options-callback)

Asynchronously creates a directory.

The callback is given a possible exception and, if `recursive` is `true`, the
first directory path created, `(err[, path])`.
`path` can still be `undefined` when `recursive` is `true`, if no directory was
created (for instance, if it was previously created).

The optional `options` argument can be an integer specifying `mode` (permission
and sticky bits), or an object with a `mode` property and a `recursive`
property indicating whether parent directories should be created. Calling
`fs.mkdir()` when `path` is a directory that exists results in an error only
when `recursive` is false. If `recursive` is false and the directory exists,
an `EEXIST` error occurs.

```
import { mkdir } from 'node:fs';


mkdir('./tmp/a/apple', { recursive: true }, (err) => {
  if (err) throw err;
}); copy
```

On Windows, using `fs.mkdir()` on the root directory even with recursion will
result in an error:

```
import { mkdir } from 'node:fs';

mkdir('/', { recursive: true }, (err) => {
  
}); copy
```

See the POSIX [`mkdir(2)`](http://man7.org/linux/man-pages/man2/mkdir.2.html) documentation for more details.

#### `fs.mkdtemp(prefix[, options], callback)`[#](#fsmkdtempprefix-options-callback)

Creates a unique temporary directory.

Generates six random characters to be appended behind a required
`prefix` to create a unique temporary directory. Due to platform
inconsistencies, avoid trailing `X` characters in `prefix`. Some platforms,
notably the BSDs, can return more than six random characters, and replace
trailing `X` characters in `prefix` with random characters.

The created directory path is passed as a string to the callback's second
parameter.

The optional `options` argument can be a string specifying an encoding, or an
object with an `encoding` property specifying the character encoding to use.

```
import { mkdtemp } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

mkdtemp(join(tmpdir(), 'foo-'), (err, directory) => {
  if (err) throw err;
  console.log(directory);
  
}); copy
```

The `fs.mkdtemp()` method will append the six randomly selected characters
directly to the `prefix` string. For instance, given a directory `/tmp`, if the
intention is to create a temporary directory *within* `/tmp`, the `prefix`
must end with a trailing platform-specific path separator
(`require('node:path').sep`).

```
import { tmpdir } from 'node:os';
import { mkdtemp } from 'node:fs';


const tmpDir = tmpdir();


mkdtemp(tmpDir, (err, directory) => {
  if (err) throw err;
  console.log(directory);
  
  
  
});


import { sep } from 'node:path';
mkdtemp(`${tmpDir}${sep}`, (err, directory) => {
  if (err) throw err;
  console.log(directory);
  
  
  
}); copy
```

#### `fs.open(path[, flags[, mode]], callback)`[#](#fsopenpath-flags-mode-callback)

Asynchronous file open. See the POSIX [`open(2)`](http://man7.org/linux/man-pages/man2/open.2.html) documentation for more details.

`mode` sets the file mode (permission and sticky bits), but only if the file was
created. On Windows, only the write permission can be manipulated; see
[`fs.chmod()`](#fschmodpath-mode-callback).

The callback gets two arguments `(err, fd)`.

Some characters (`< > : " / \ | ? *`) are reserved under Windows as documented
by [Naming Files, Paths, and Namespaces](https://docs.microsoft.com/en-us/windows/desktop/FileIO/naming-a-file). Under NTFS, if the filename contains
a colon, Node.js will open a file system stream, as described by
[this MSDN page](https://docs.microsoft.com/en-us/windows/desktop/FileIO/using-streams).

Functions based on `fs.open()` exhibit this behavior as well:
`fs.writeFile()`, `fs.readFile()`, etc.

#### `fs.opendir(path[, options], callback)`[#](#fsopendirpath-options-callback)

Asynchronously open a directory. See the POSIX [`opendir(3)`](http://man7.org/linux/man-pages/man3/opendir.3.html) documentation for
more details.

Creates an [<fs.Dir>](fs.html#class-fsdir), which contains all further functions for reading from
and cleaning up the directory.

The `encoding` option sets the encoding for the `path` while opening the
directory and subsequent read operations.

#### `fs.read(fd, buffer, offset, length, position, callback)`[#](#fsreadfd-buffer-offset-length-position-callback)

* `fd` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type)
* `buffer` [<Buffer>](buffer.html#class-buffer) | [<TypedArray>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray) | [<DataView>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView) The buffer that the data will be
  written to.
* `offset` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) The position in `buffer` to write the data to.
* `length` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) The number of bytes to read.
* `position` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) | [<bigint>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt) | [<null>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Null_type) Specifies where to begin reading from in the
  file. If `position` is `null` or `-1` , data will be read from the current
  file position, and the file position will be updated. If `position` is
  a non-negative integer, the file position will be unchanged.
* `callback` [<Function>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function)

Read data from the file specified by `fd`.

The callback is given the three arguments, `(err, bytesRead, buffer)`.

If the file is not modified concurrently, the end-of-file is reached when the
number of bytes read is zero.

If this method is invoked as its [`util.promisify()`](util.html#utilpromisifyoriginal)ed version, it returns
a promise for an `Object` with `bytesRead` and `buffer` properties.

The `fs.read()` method reads data from the file specified
by the file descriptor (`fd`).
The `length` argument indicates the maximum number
of bytes that Node.js
will attempt to read from the kernel.
However, the actual number of bytes read (`bytesRead`) can be lower
than the specified `length` for various reasons.

For example:

* If the file is shorter than the specified `length`, `bytesRead`
  will be set to the actual number of bytes read.
* If the file encounters EOF (End of File) before the buffer could
  be filled, Node.js will read all available bytes until EOF is encountered,
  and the `bytesRead` parameter in the callback will indicate
  the actual number of bytes read, which may be less than the specified `length`.
* If the file is on a slow network `filesystem`
  or encounters any other issue during reading,
  `bytesRead` can be lower than the specified `length`.

Therefore, when using `fs.read()`, it's important to
check the `bytesRead` value to
determine how many bytes were actually read from the file.
Depending on your application
logic, you may need to handle cases where `bytesRead`
is lower than the specified `length`,
such as by wrapping the read call in a loop if you require
a minimum amount of bytes.

This behavior is similar to the POSIX `preadv2` function.

#### `fs.read(fd[, options], callback)`[#](#fsreadfd-options-callback)

Similar to the [`fs.read()`](#fsreadfd-buffer-offset-length-position-callback) function, this version takes an optional
`options` object. If no `options` object is specified, it will default with the
above values.

#### `fs.read(fd, buffer[, options], callback)`[#](#fsreadfd-buffer-options-callback)

Added in: v18.2.0, v16.17.0

Similar to the [`fs.read()`](#fsreadfd-buffer-offset-length-position-callback) function, this version takes an optional
`options` object. If no `options` object is specified, it will default with the
above values.

#### `fs.readdir(path[, options], callback)`[#](#fsreaddirpath-options-callback)

Reads the contents of a directory. The callback gets two arguments `(err, files)`
where `files` is an array of the names of the files in the directory excluding
`'.'` and `'..'`.

See the POSIX [`readdir(3)`](http://man7.org/linux/man-pages/man3/readdir.3.html) documentation for more details.

The optional `options` argument can be a string specifying an encoding, or an
object with an `encoding` property specifying the character encoding to use for
the filenames passed to the callback. If the `encoding` is set to `'buffer'`,
the filenames returned will be passed as [<Buffer>](buffer.html#class-buffer) objects.

If `options.withFileTypes` is set to `true`, the `files` array will contain
[<fs.Dirent>](fs.html#class-fsdirent) objects.

#### `fs.readFile(path[, options], callback)`[#](#fsreadfilepath-options-callback)

Asynchronously reads the entire contents of a file.

```
import { readFile } from 'node:fs';

readFile('/etc/passwd', (err, data) => {
  if (err) throw err;
  console.log(data);
}); copy
```

The callback is passed two arguments `(err, data)`, where `data` is the
contents of the file.

If no encoding is specified, then the raw buffer is returned.

If `options` is a string, then it specifies the encoding:

```
import { readFile } from 'node:fs';

readFile('/etc/passwd', 'utf8', callback); copy
```

When the path is a directory, the behavior of `fs.readFile()` and
[`fs.readFileSync()`](#fsreadfilesyncpath-options) is platform-specific. On macOS, Linux, and Windows, an
error will be returned. On FreeBSD, a representation of the directory's contents
will be returned.

```
import { readFile } from 'node:fs';


readFile('<directory>', (err, data) => {
  
});


readFile('<directory>', (err, data) => {
  
}); copy
```

It is possible to abort an ongoing request using an `AbortSignal`. If a
request is aborted the callback is called with an `AbortError`:

```
import { readFile } from 'node:fs';

const controller = new AbortController();
const signal = controller.signal;
readFile(fileInfo[0].name, { signal }, (err, buf) => {
  
});

controller.abort(); copy
```

The `fs.readFile()` function buffers the entire file. To minimize memory costs,
when possible prefer streaming via `fs.createReadStream()`.

Aborting an ongoing request does not abort individual operating
system requests but rather the internal buffering `fs.readFile` performs.

##### File descriptors[#](#file-descriptors)

1. Any specified file descriptor has to support reading.
2. If a file descriptor is specified as the `path`, it will not be closed
   automatically.
3. The reading will begin at the current position. For example, if the file
   already had `'Hello World'` and six bytes are read with the file descriptor,
   the call to `fs.readFile()` with the same file descriptor, would give
   `'World'`, rather than `'Hello World'`.

##### Performance Considerations[#](#performance-considerations)

The `fs.readFile()` method asynchronously reads the contents of a file into
memory one chunk at a time, allowing the event loop to turn between each chunk.
This allows the read operation to have less impact on other activity that may
be using the underlying libuv thread pool but means that it will take longer
to read a complete file into memory.

The additional read overhead can vary broadly on different systems and depends
on the type of file being read. If the file type is not a regular file (a pipe
for instance) and Node.js is unable to determine an actual file size, each read
operation will load on 64 KiB of data. For regular files, each read will process
512 KiB of data.

For applications that require as-fast-as-possible reading of file contents, it
is better to use `fs.read()` directly and for application code to manage
reading the full contents of the file itself.

The Node.js GitHub issue [#25741](https://github.com/nodejs/node/issues/25741) provides more information and a detailed
analysis on the performance of `fs.readFile()` for multiple file sizes in
different Node.js versions.

#### `fs.readlink(path[, options], callback)`[#](#fsreadlinkpath-options-callback)

Reads the contents of the symbolic link referred to by `path`. The callback gets
two arguments `(err, linkString)`.

See the POSIX [`readlink(2)`](http://man7.org/linux/man-pages/man2/readlink.2.html) documentation for more details.

The optional `options` argument can be a string specifying an encoding, or an
object with an `encoding` property specifying the character encoding to use for
the link path passed to the callback. If the `encoding` is set to `'buffer'`,
the link path returned will be passed as a [<Buffer>](buffer.html#class-buffer) object.

#### `fs.readv(fd, buffers[, position], callback)`[#](#fsreadvfd-buffers-position-callback)

Read from a file specified by `fd` and write to an array of `ArrayBufferView`s
using `readv()`.

`position` is the offset from the beginning of the file from where data
should be read. If `typeof position !== 'number'`, the data will be read
from the current position.

The callback will be given three arguments: `err`, `bytesRead`, and
`buffers`. `bytesRead` is how many bytes were read from the file.

If this method is invoked as its [`util.promisify()`](util.html#utilpromisifyoriginal)ed version, it returns
a promise for an `Object` with `bytesRead` and `buffers` properties.

#### `fs.realpath(path[, options], callback)`[#](#fsrealpathpath-options-callback)

Asynchronously computes the canonical pathname by resolving `.`, `..`, and
symbolic links.

A canonical pathname is not necessarily unique. Hard links and bind mounts can
expose a file system entity through many pathnames.

This function behaves like [`realpath(3)`](http://man7.org/linux/man-pages/man3/realpath.3.html), with some exceptions:

1. No case conversion is performed on case-insensitive file systems.
2. The maximum number of symbolic links is platform-independent and generally
   (much) higher than what the native [`realpath(3)`](http://man7.org/linux/man-pages/man3/realpath.3.html) implementation supports.

The `callback` gets two arguments `(err, resolvedPath)`. May use `process.cwd`
to resolve relative paths.

Only paths that can be converted to UTF8 strings are supported.

The optional `options` argument can be a string specifying an encoding, or an
object with an `encoding` property specifying the character encoding to use for
the path passed to the callback. If the `encoding` is set to `'buffer'`,
the path returned will be passed as a [<Buffer>](buffer.html#class-buffer) object.

If `path` resolves to a socket or a pipe, the function will return a system
dependent name for that object.

A path that does not exist results in an ENOENT error.
`error.path` is the absolute file path.

#### `fs.realpath.native(path[, options], callback)`[#](#fsrealpathnativepath-options-callback)

Asynchronous [`realpath(3)`](http://man7.org/linux/man-pages/man3/realpath.3.html).

The `callback` gets two arguments `(err, resolvedPath)`.

Only paths that can be converted to UTF8 strings are supported.

The optional `options` argument can be a string specifying an encoding, or an
object with an `encoding` property specifying the character encoding to use for
the path passed to the callback. If the `encoding` is set to `'buffer'`,
the path returned will be passed as a [<Buffer>](buffer.html#class-buffer) object.

On Linux, when Node.js is linked against musl libc, the procfs file system must
be mounted on `/proc` in order for this function to work. Glibc does not have
this restriction.

#### `fs.rename(oldPath, newPath, callback)`[#](#fsrenameoldpath-newpath-callback)

Asynchronously rename file at `oldPath` to the pathname provided
as `newPath`. In the case that `newPath` already exists, it will
be overwritten. If there is a directory at `newPath`, an error will
be raised instead. No arguments other than a possible exception are
given to the completion callback.

See also: [`rename(2)`](http://man7.org/linux/man-pages/man2/rename.2.html).

```
import { rename } from 'node:fs';

rename('oldFile.txt', 'newFile.txt', (err) => {
  if (err) throw err;
  console.log('Rename complete!');
}); copy
```

#### `fs.rmdir(path[, options], callback)`[#](#fsrmdirpath-options-callback)

* `path` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) | [<Buffer>](buffer.html#class-buffer) | [<URL>](url.html#the-whatwg-url-api)
* `options` [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)
  + `maxRetries` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) If an `EBUSY`, `EMFILE`, `ENFILE`, `ENOTEMPTY`, or
    `EPERM` error is encountered, Node.js retries the operation with a linear
    backoff wait of `retryDelay` milliseconds longer on each try. This option
    represents the number of retries. This option is ignored if the `recursive`
    option is not `true`. **Default:** `0`.
  + `recursive` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) If `true`, perform a recursive directory removal. In
    recursive mode, operations are retried on failure. **Default:** `false`.
    **Deprecated.**
  + `retryDelay` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) The amount of time in milliseconds to wait between
    retries. This option is ignored if the `recursive` option is not `true`.
    **Default:** `100`.
* `callback` [<Function>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function)

Asynchronous [`rmdir(2)`](http://man7.org/linux/man-pages/man2/rmdir.2.html). No arguments other than a possible exception are given
to the completion callback.

Using `fs.rmdir()` on a file (not a directory) results in an `ENOENT` error on
Windows and an `ENOTDIR` error on POSIX.

To get a behavior similar to the `rm -rf` Unix command, use [`fs.rm()`](#fsrmpath-options-callback)
with options `{ recursive: true, force: true }`.

#### `fs.rm(path[, options], callback)`[#](#fsrmpath-options-callback)

* `path` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) | [<Buffer>](buffer.html#class-buffer) | [<URL>](url.html#the-whatwg-url-api)
* `options` [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)
  + `force` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) When `true`, exceptions will be ignored if `path` does
    not exist. **Default:** `false`.
  + `maxRetries` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) If an `EBUSY`, `EMFILE`, `ENFILE`, `ENOTEMPTY`, or
    `EPERM` error is encountered, Node.js will retry the operation with a linear
    backoff wait of `retryDelay` milliseconds longer on each try. This option
    represents the number of retries. This option is ignored if the `recursive`
    option is not `true`. **Default:** `0`.
  + `recursive` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) If `true`, perform a recursive removal. In
    recursive mode operations are retried on failure. **Default:** `false`.
  + `retryDelay` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) The amount of time in milliseconds to wait between
    retries. This option is ignored if the `recursive` option is not `true`.
    **Default:** `100`.
* `callback` [<Function>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function)

Asynchronously removes files and directories (modeled on the standard POSIX `rm`
utility). No arguments other than a possible exception are given to the
completion callback.

#### `fs.stat(path[, options], callback)`[#](#fsstatpath-options-callback)

Asynchronous [`stat(2)`](http://man7.org/linux/man-pages/man2/stat.2.html). The callback gets two arguments `(err, stats)` where
`stats` is an [<fs.Stats>](fs.html#class-fsstats) object.

In case of an error, the `err.code` will be one of [Common System Errors](errors.html#common-system-errors).

[`fs.stat()`](#fsstatpath-options-callback) follows symbolic links. Use [`fs.lstat()`](#fslstatpath-options-callback) to look at the
links themselves.

Using `fs.stat()` to check for the existence of a file before calling
`fs.open()`, `fs.readFile()`, or `fs.writeFile()` is not recommended.
Instead, user code should open/read/write the file directly and handle the
error raised if the file is not available.

To check if a file exists without manipulating it afterwards, [`fs.access()`](#fsaccesspath-mode-callback)
is recommended.

For example, given the following directory structure:

```
- txtDir
-- file.txt
- app.js copy
```

The next program will check for the stats of the given paths:

```
import { stat } from 'node:fs';

const pathsToCheck = ['./txtDir', './txtDir/file.txt'];

for (let i = 0; i < pathsToCheck.length; i++) {
  stat(pathsToCheck[i], (err, stats) => {
    console.log(stats.isDirectory());
    console.log(stats);
  });
} copy
```

The resulting output will resemble:

```
true
Stats {
  dev: 16777220,
  mode: 16877,
  nlink: 3,
  uid: 501,
  gid: 20,
  rdev: 0,
  blksize: 4096,
  ino: 14214262,
  size: 96,
  blocks: 0,
  atimeMs: 1561174653071.963,
  mtimeMs: 1561174614583.3518,
  ctimeMs: 1561174626623.5366,
  birthtimeMs: 1561174126937.2893,
  atime: 2019-06-22T03:37:33.072Z,
  mtime: 2019-06-22T03:36:54.583Z,
  ctime: 2019-06-22T03:37:06.624Z,
  birthtime: 2019-06-22T03:28:46.937Z
}
false
Stats {
  dev: 16777220,
  mode: 33188,
  nlink: 1,
  uid: 501,
  gid: 20,
  rdev: 0,
  blksize: 4096,
  ino: 14214074,
  size: 8,
  blocks: 8,
  atimeMs: 1561174616618.8555,
  mtimeMs: 1561174614584,
  ctimeMs: 1561174614583.8145,
  birthtimeMs: 1561174007710.7478,
  atime: 2019-06-22T03:36:56.619Z,
  mtime: 2019-06-22T03:36:54.584Z,
  ctime: 2019-06-22T03:36:54.584Z,
  birthtime: 2019-06-22T03:26:47.711Z
} copy
```

#### `fs.statfs(path[, options], callback)`[#](#fsstatfspath-options-callback)

Added in: v19.6.0, v18.15.0

Asynchronous [`statfs(2)`](http://man7.org/linux/man-pages/man2/statfs.2.html). Returns information about the mounted file system which
contains `path`. The callback gets two arguments `(err, stats)` where `stats`
is an [<fs.StatFs>](fs.html#class-fsstatfs) object.

In case of an error, the `err.code` will be one of [Common System Errors](errors.html#common-system-errors).

#### `fs.symlink(target, path[, type], callback)`[#](#fssymlinktarget-path-type-callback)

Creates the link called `path` pointing to `target`. No arguments other than a
possible exception are given to the completion callback.

See the POSIX [`symlink(2)`](http://man7.org/linux/man-pages/man2/symlink.2.html) documentation for more details.

The `type` argument is only available on Windows and ignored on other platforms.
It can be set to `'dir'`, `'file'`, or `'junction'`. If the `type` argument is
`null`, Node.js will autodetect `target` type and use `'file'` or `'dir'`.
If the `target` does not exist, `'file'` will be used. Windows junction points
require the destination path to be absolute. When using `'junction'`, the
`target` argument will automatically be normalized to absolute path. Junction
points on NTFS volumes can only point to directories.

Relative targets are relative to the link's parent directory.

```
import { symlink } from 'node:fs';

symlink('./mew', './mewtwo', callback); copy
```

The above example creates a symbolic link `mewtwo` which points to `mew` in the
same directory:

```
$ tree .
.
├── mew
└── mewtwo -> ./mew copy
```

#### `fs.truncate(path[, len], callback)`[#](#fstruncatepath-len-callback)

Truncates the file. No arguments other than a possible exception are
given to the completion callback. A file descriptor can also be passed as the
first argument. In this case, `fs.ftruncate()` is called.

```
import { truncate } from 'node:fs';

truncate('path/file.txt', (err) => {
  if (err) throw err;
  console.log('path/file.txt was truncated');
});const { truncate } = require('node:fs');

truncate('path/file.txt', (err) => {
  if (err) throw err;
  console.log('path/file.txt was truncated');
});copy
```

Passing a file descriptor is deprecated and may result in an error being thrown
in the future.

See the POSIX [`truncate(2)`](http://man7.org/linux/man-pages/man2/truncate.2.html) documentation for more details.

#### `fs.unlink(path, callback)`[#](#fsunlinkpath-callback)

Asynchronously removes a file or symbolic link. No arguments other than a
possible exception are given to the completion callback.

```
import { unlink } from 'node:fs';

unlink('path/file.txt', (err) => {
  if (err) throw err;
  console.log('path/file.txt was deleted');
}); copy
```

`fs.unlink()` will not work on a directory, empty or otherwise. To remove a
directory, use [`fs.rmdir()`](#fsrmdirpath-options-callback).

See the POSIX [`unlink(2)`](http://man7.org/linux/man-pages/man2/unlink.2.html) documentation for more details.

#### `fs.unwatchFile(filename[, listener])`[#](#fsunwatchfilefilename-listener)

Added in: v0.1.31

Stop watching for changes on `filename`. If `listener` is specified, only that
particular listener is removed. Otherwise, *all* listeners are removed,
effectively stopping watching of `filename`.

Calling `fs.unwatchFile()` with a filename that is not being watched is a
no-op, not an error.

Using [`fs.watch()`](#fswatchfilename-options-listener) is more efficient than `fs.watchFile()` and
`fs.unwatchFile()`. `fs.watch()` should be used instead of `fs.watchFile()`
and `fs.unwatchFile()` when possible.

#### `fs.utimes(path, atime, mtime, callback)`[#](#fsutimespath-atime-mtime-callback)

Change the file system timestamps of the object referenced by `path`.

The `atime` and `mtime` arguments follow these rules:

* Values can be either numbers representing Unix epoch time in seconds,
  `Date`s, or a numeric string like `'123456789.0'`.
* If the value can not be converted to a number, or is `NaN`, `Infinity`, or
  `-Infinity`, an `Error` will be thrown.

#### `fs.watch(filename[, options][, listener])`[#](#fswatchfilename-options-listener)

* `filename` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) | [<Buffer>](buffer.html#class-buffer) | [<URL>](url.html#the-whatwg-url-api)
* `options` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) | [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)
  + `persistent` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) Indicates whether the process should continue to run
    as long as files are being watched. **Default:** `true`.
  + `recursive` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) Indicates whether all subdirectories should be
    watched, or only the current directory. This applies when a directory is
    specified, and only on supported platforms (See [caveats](#caveats)). **Default:**
    `false`.
  + `encoding` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) Specifies the character encoding to be used for the
    filename passed to the listener. **Default:** `'utf8'`.
  + `signal` [<AbortSignal>](globals.html#class-abortsignal) allows closing the watcher with an AbortSignal.
* `listener` [<Function>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function) | [<undefined>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Undefined_type) **Default:** `undefined`
* Returns: [<fs.FSWatcher>](fs.html#class-fsfswatcher)

Watch for changes on `filename`, where `filename` is either a file or a
directory.

The second argument is optional. If `options` is provided as a string, it
specifies the `encoding`. Otherwise `options` should be passed as an object.

The listener callback gets two arguments `(eventType, filename)`. `eventType`
is either `'rename'` or `'change'`, and `filename` is the name of the file
which triggered the event.

On most platforms, `'rename'` is emitted whenever a filename appears or
disappears in the directory.

The listener callback is attached to the `'change'` event fired by
[<fs.FSWatcher>](fs.html#class-fsfswatcher), but it is not the same thing as the `'change'` value of
`eventType`.

If a `signal` is passed, aborting the corresponding AbortController will close
the returned [<fs.FSWatcher>](fs.html#class-fsfswatcher).

##### Caveats[#](#caveats)

The `fs.watch` API is not 100% consistent across platforms, and is
unavailable in some situations.

On Windows, no events will be emitted if the watched directory is moved or
renamed. An `EPERM` error is reported when the watched directory is deleted.

The `fs.watch` API does not provide any protection with respect
to malicious actions on the file system. For example, on Windows it is
implemented by monitoring changes in a directory versus specific files. This
allows substitution of a file and fs reporting changes on the new file
with the same filename.

###### Availability[#](#availability)

This feature depends on the underlying operating system providing a way
to be notified of file system changes.

* On Linux systems, this uses [`inotify(7)`](https://man7.org/linux/man-pages/man7/inotify.7.html).
* On BSD systems, this uses [`kqueue(2)`](https://www.freebsd.org/cgi/man.cgi?query=kqueue&sektion=2).
* On macOS, this uses [`kqueue(2)`](https://www.freebsd.org/cgi/man.cgi?query=kqueue&sektion=2) for files and [`FSEvents`](https://developer.apple.com/documentation/coreservices/file_system_events) for
  directories.
* On SunOS systems (including Solaris and SmartOS), this uses [`event ports`](https://illumos.org/man/port_create).
* On Windows systems, this feature depends on [`ReadDirectoryChangesW`](https://docs.microsoft.com/en-us/windows/desktop/api/winbase/nf-winbase-readdirectorychangesw).
* On AIX systems, this feature depends on [`AHAFS`](https://developer.ibm.com/articles/au-aix_event_infrastructure/), which must be enabled.
* On IBM i systems, this feature is not supported.

If the underlying functionality is not available for some reason, then
`fs.watch()` will not be able to function and may throw an exception.
For example, watching files or directories can be unreliable, and in some
cases impossible, on network file systems (NFS, SMB, etc) or host file systems
when using virtualization software such as Vagrant or Docker.

It is still possible to use `fs.watchFile()`, which uses stat polling, but
this method is slower and less reliable.

###### Inodes[#](#inodes)

On Linux and macOS systems, `fs.watch()` resolves the path to an [inode](https://en.wikipedia.org/wiki/Inode) and
watches the inode. If the watched path is deleted and recreated, it is assigned
a new inode. The watch will emit an event for the delete but will continue
watching the *original* inode. Events for the new inode will not be emitted.
This is expected behavior.

AIX files retain the same inode for the lifetime of a file. Saving and closing a
watched file on AIX will result in two notifications (one for adding new
content, and one for truncation).

###### Filename argument[#](#filename-argument)

Providing `filename` argument in the callback is only supported on Linux,
macOS, Windows, and AIX. Even on supported platforms, `filename` is not always
guaranteed to be provided. Therefore, don't assume that `filename` argument is
always provided in the callback, and have some fallback logic if it is `null`.

```
import { watch } from 'node:fs';
watch('somedir', (eventType, filename) => {
  console.log(`event type is: ${eventType}`);
  if (filename) {
    console.log(`filename provided: ${filename}`);
  } else {
    console.log('filename not provided');
  }
}); copy
```

#### `fs.watchFile(filename[, options], listener)`[#](#fswatchfilefilename-options-listener)

Watch for changes on `filename`. The callback `listener` will be called each
time the file is accessed.

The `options` argument may be omitted. If provided, it should be an object. The
`options` object may contain a boolean named `persistent` that indicates
whether the process should continue to run as long as files are being watched.
The `options` object may specify an `interval` property indicating how often the
target should be polled in milliseconds.

The `listener` gets two arguments the current stat object and the previous
stat object:

```
import { watchFile } from 'node:fs';

watchFile('message.text', (curr, prev) => {
  console.log(`the current mtime is: ${curr.mtime}`);
  console.log(`the previous mtime was: ${prev.mtime}`);
}); copy
```

These stat objects are instances of `fs.Stat`. If the `bigint` option is `true`,
the numeric values in these objects are specified as `BigInt`s.

To be notified when the file was modified, not just accessed, it is necessary
to compare `curr.mtimeMs` and `prev.mtimeMs`.

When an `fs.watchFile` operation results in an `ENOENT` error, it
will invoke the listener once, with all the fields zeroed (or, for dates, the
Unix Epoch). If the file is created later on, the listener will be called
again, with the latest stat objects. This is a change in functionality since
v0.10.

Using [`fs.watch()`](#fswatchfilename-options-listener) is more efficient than `fs.watchFile` and
`fs.unwatchFile`. `fs.watch` should be used instead of `fs.watchFile` and
`fs.unwatchFile` when possible.

When a file being watched by `fs.watchFile()` disappears and reappears,
then the contents of `previous` in the second callback event (the file's
reappearance) will be the same as the contents of `previous` in the first
callback event (its disappearance).

This happens when:

* the file is deleted, followed by a restore
* the file is renamed and then renamed a second time back to its original name

#### `fs.write(fd, buffer, offset[, length[, position]], callback)`[#](#fswritefd-buffer-offset-length-position-callback)

Write `buffer` to the file specified by `fd`.

`offset` determines the part of the buffer to be written, and `length` is
an integer specifying the number of bytes to write.

`position` refers to the offset from the beginning of the file where this data
should be written. If `typeof position !== 'number'`, the data will be written
at the current position. See [`pwrite(2)`](http://man7.org/linux/man-pages/man2/pwrite.2.html).

The callback will be given three arguments `(err, bytesWritten, buffer)` where
`bytesWritten` specifies how many *bytes* were written from `buffer`.

If this method is invoked as its [`util.promisify()`](util.html#utilpromisifyoriginal)ed version, it returns
a promise for an `Object` with `bytesWritten` and `buffer` properties.

It is unsafe to use `fs.write()` multiple times on the same file without waiting
for the callback. For this scenario, [`fs.createWriteStream()`](#fscreatewritestreampath-options) is
recommended.

On Linux, positional writes don't work when the file is opened in append mode.
The kernel ignores the position argument and always appends the data to
the end of the file.

#### `fs.write(fd, buffer[, options], callback)`[#](#fswritefd-buffer-options-callback)

Added in: v18.3.0, v16.17.0

Write `buffer` to the file specified by `fd`.

Similar to the above `fs.write` function, this version takes an
optional `options` object. If no `options` object is specified, it will
default with the above values.

#### `fs.write(fd, string[, position[, encoding]], callback)`[#](#fswritefd-string-position-encoding-callback)

Write `string` to the file specified by `fd`. If `string` is not a string,
an exception is thrown.

`position` refers to the offset from the beginning of the file where this data
should be written. If `typeof position !== 'number'` the data will be written at
the current position. See [`pwrite(2)`](http://man7.org/linux/man-pages/man2/pwrite.2.html).

`encoding` is the expected string encoding.

The callback will receive the arguments `(err, written, string)` where `written`
specifies how many *bytes* the passed string required to be written. Bytes
written is not necessarily the same as string characters written. See
[`Buffer.byteLength`](buffer.html#static-method-bufferbytelengthstring-encoding).

It is unsafe to use `fs.write()` multiple times on the same file without waiting
for the callback. For this scenario, [`fs.createWriteStream()`](#fscreatewritestreampath-options) is
recommended.

On Linux, positional writes don't work when the file is opened in append mode.
The kernel ignores the position argument and always appends the data to
the end of the file.

On Windows, if the file descriptor is connected to the console (e.g. `fd == 1`
or `stdout`) a string containing non-ASCII characters will not be rendered
properly by default, regardless of the encoding used.
It is possible to configure the console to render UTF-8 properly by changing the
active codepage with the `chcp 65001` command. See the [chcp](https://ss64.com/nt/chcp.html) docs for more
details.

#### `fs.writeFile(file, data[, options], callback)`[#](#fswritefilefile-data-options-callback)

When `file` is a filename, asynchronously writes data to the file, replacing the
file if it already exists. `data` can be a string or a buffer.

When `file` is a file descriptor, the behavior is similar to calling
`fs.write()` directly (which is recommended). See the notes below on using
a file descriptor.

The `encoding` option is ignored if `data` is a buffer.

The `mode` option only affects the newly created file. See [`fs.open()`](#fsopenpath-flags-mode-callback)
for more details.

```
import { writeFile } from 'node:fs';
import { Buffer } from 'node:buffer';

const data = new Uint8Array(Buffer.from('Hello Node.js'));
writeFile('message.txt', data, (err) => {
  if (err) throw err;
  console.log('The file has been saved!');
}); copy
```

If `options` is a string, then it specifies the encoding:

```
import { writeFile } from 'node:fs';

writeFile('message.txt', 'Hello Node.js', 'utf8', callback); copy
```

It is unsafe to use `fs.writeFile()` multiple times on the same file without
waiting for the callback. For this scenario, [`fs.createWriteStream()`](#fscreatewritestreampath-options) is
recommended.

Similarly to `fs.readFile` - `fs.writeFile` is a convenience method that
performs multiple `write` calls internally to write the buffer passed to it.
For performance sensitive code consider using [`fs.createWriteStream()`](#fscreatewritestreampath-options).

It is possible to use an [<AbortSignal>](globals.html#class-abortsignal) to cancel an `fs.writeFile()`.
Cancelation is "best effort", and some amount of data is likely still
to be written.

```
import { writeFile } from 'node:fs';
import { Buffer } from 'node:buffer';

const controller = new AbortController();
const { signal } = controller;
const data = new Uint8Array(Buffer.from('Hello Node.js'));
writeFile('message.txt', data, { signal }, (err) => {
  
});

controller.abort(); copy
```

Aborting an ongoing request does not abort individual operating
system requests but rather the internal buffering `fs.writeFile` performs.

##### Using `fs.writeFile()` with file descriptors[#](#using-fswritefile-with-file-descriptors)

When `file` is a file descriptor, the behavior is almost identical to directly
calling `fs.write()` like:

```
import { write } from 'node:fs';
import { Buffer } from 'node:buffer';

write(fd, Buffer.from(data, options.encoding), callback); copy
```

The difference from directly calling `fs.write()` is that under some unusual
conditions, `fs.write()` might write only part of the buffer and need to be
retried to write the remaining data, whereas `fs.writeFile()` retries until
the data is entirely written (or an error occurs).

The implications of this are a common source of confusion. In
the file descriptor case, the file is not replaced! The data is not necessarily
written to the beginning of the file, and the file's original data may remain
before and/or after the newly written data.

For example, if `fs.writeFile()` is called twice in a row, first to write the
string `'Hello'`, then to write the string `', World'`, the file would contain
`'Hello, World'`, and might contain some of the file's original data (depending
on the size of the original file, and the position of the file descriptor). If
a file name had been used instead of a descriptor, the file would be guaranteed
to contain only `', World'`.

#### `fs.writev(fd, buffers[, position], callback)`[#](#fswritevfd-buffers-position-callback)

Write an array of `ArrayBufferView`s to the file specified by `fd` using
`writev()`.

`position` is the offset from the beginning of the file where this data
should be written. If `typeof position !== 'number'`, the data will be written
at the current position.

The callback will be given three arguments: `err`, `bytesWritten`, and
`buffers`. `bytesWritten` is how many bytes were written from `buffers`.

If this method is [`util.promisify()`](util.html#utilpromisifyoriginal)ed, it returns a promise for an
`Object` with `bytesWritten` and `buffers` properties.

It is unsafe to use `fs.writev()` multiple times on the same file without
waiting for the callback. For this scenario, use [`fs.createWriteStream()`](#fscreatewritestreampath-options).

On Linux, positional writes don't work when the file is opened in append mode.
The kernel ignores the position argument and always appends the data to
the end of the file.

### Synchronous API[#](#synchronous-api)

The synchronous APIs perform all operations synchronously, blocking the
event loop until the operation completes or fails.

#### `fs.accessSync(path[, mode])`[#](#fsaccesssyncpath-mode)

Synchronously tests a user's permissions for the file or directory specified
by `path`. The `mode` argument is an optional integer that specifies the
accessibility checks to be performed. `mode` should be either the value
`fs.constants.F_OK` or a mask consisting of the bitwise OR of any of
`fs.constants.R_OK`, `fs.constants.W_OK`, and `fs.constants.X_OK` (e.g.
`fs.constants.W_OK | fs.constants.R_OK`). Check [File access constants](#file-access-constants) for
possible values of `mode`.

If any of the accessibility checks fail, an `Error` will be thrown. Otherwise,
the method will return `undefined`.

```
import { accessSync, constants } from 'node:fs';

try {
  accessSync('etc/passwd', constants.R_OK | constants.W_OK);
  console.log('can read/write');
} catch (err) {
  console.error('no access!');
} copy
```

#### `fs.appendFileSync(path, data[, options])`[#](#fsappendfilesyncpath-data-options)

Synchronously append data to a file, creating the file if it does not yet
exist. `data` can be a string or a [<Buffer>](buffer.html#class-buffer).

The `mode` option only affects the newly created file. See [`fs.open()`](#fsopenpath-flags-mode-callback)
for more details.

```
import { appendFileSync } from 'node:fs';

try {
  appendFileSync('message.txt', 'data to append');
  console.log('The "data to append" was appended to file!');
} catch (err) {
  
} copy
```

If `options` is a string, then it specifies the encoding:

```
import { appendFileSync } from 'node:fs';

appendFileSync('message.txt', 'data to append', 'utf8'); copy
```

The `path` may be specified as a numeric file descriptor that has been opened
for appending (using `fs.open()` or `fs.openSync()`). The file descriptor will
not be closed automatically.

```
import { openSync, closeSync, appendFileSync } from 'node:fs';

let fd;

try {
  fd = openSync('message.txt', 'a');
  appendFileSync(fd, 'data to append', 'utf8');
} catch (err) {
  
} finally {
  if (fd !== undefined)
    closeSync(fd);
} copy
```

#### `fs.chmodSync(path, mode)`[#](#fschmodsyncpath-mode)

For detailed information, see the documentation of the asynchronous version of
this API: [`fs.chmod()`](#fschmodpath-mode-callback).

See the POSIX [`chmod(2)`](http://man7.org/linux/man-pages/man2/chmod.2.html) documentation for more detail.

#### `fs.chownSync(path, uid, gid)`[#](#fschownsyncpath-uid-gid)

Synchronously changes owner and group of a file. Returns `undefined`.
This is the synchronous version of [`fs.chown()`](#fschownpath-uid-gid-callback).

See the POSIX [`chown(2)`](http://man7.org/linux/man-pages/man2/chown.2.html) documentation for more detail.

#### `fs.closeSync(fd)`[#](#fsclosesyncfd)

Added in: v0.1.21

Closes the file descriptor. Returns `undefined`.

Calling `fs.closeSync()` on any file descriptor (`fd`) that is currently in use
through any other `fs` operation may lead to undefined behavior.

See the POSIX [`close(2)`](http://man7.org/linux/man-pages/man2/close.2.html) documentation for more detail.

#### `fs.copyFileSync(src, dest[, mode])`[#](#fscopyfilesyncsrc-dest-mode)

Synchronously copies `src` to `dest`. By default, `dest` is overwritten if it
already exists. Returns `undefined`. Node.js makes no guarantees about the
atomicity of the copy operation. If an error occurs after the destination file
has been opened for writing, Node.js will attempt to remove the destination.

`mode` is an optional integer that specifies the behavior
of the copy operation. It is possible to create a mask consisting of the bitwise
OR of two or more values (e.g.
`fs.constants.COPYFILE_EXCL | fs.constants.COPYFILE_FICLONE`).

* `fs.constants.COPYFILE_EXCL`: The copy operation will fail if `dest` already
  exists.
* `fs.constants.COPYFILE_FICLONE`: The copy operation will attempt to create a
  copy-on-write reflink. If the platform does not support copy-on-write, then a
  fallback copy mechanism is used.
* `fs.constants.COPYFILE_FICLONE_FORCE`: The copy operation will attempt to
  create a copy-on-write reflink. If the platform does not support
  copy-on-write, then the operation will fail.

```
import { copyFileSync, constants } from 'node:fs';


copyFileSync('source.txt', 'destination.txt');
console.log('source.txt was copied to destination.txt');


copyFileSync('source.txt', 'destination.txt', constants.COPYFILE_EXCL); copy
```

#### `fs.cpSync(src, dest[, options])`[#](#fscpsyncsrc-dest-options)

* `src` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) | [<URL>](url.html#the-whatwg-url-api) source path to copy.
* `dest` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) | [<URL>](url.html#the-whatwg-url-api) destination path to copy to.
* `options` [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)
  + `dereference` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) dereference symlinks. **Default:** `false`.
  + `errorOnExist` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) when `force` is `false`, and the destination
    exists, throw an error. **Default:** `false`.
  + `filter` [<Function>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function) Function to filter copied files/directories. Return
    `true` to copy the item, `false` to ignore it. When ignoring a directory,
    all of its contents will be skipped as well. **Default:** `undefined`
    - `src` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) source path to copy.
    - `dest` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) destination path to copy to.
    - Returns: [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) Any non-`Promise` value that is coercible
      to `boolean`.
  + `force` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) overwrite existing file or directory. The copy
    operation will ignore errors if you set this to false and the destination
    exists. Use the `errorOnExist` option to change this behavior.
    **Default:** `true`.
  + `mode` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) modifiers for copy operation. **Default:** `0`.
    See `mode` flag of [`fs.copyFileSync()`](#fscopyfilesyncsrc-dest-mode).
  + `preserveTimestamps` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) When `true` timestamps from `src` will
    be preserved. **Default:** `false`.
  + `recursive` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) copy directories recursively **Default:** `false`
  + `verbatimSymlinks` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) When `true`, path resolution for symlinks will
    be skipped. **Default:** `false`

Synchronously copies the entire directory structure from `src` to `dest`,
including subdirectories and files.

When copying a directory to another directory, globs are not supported and
behavior is similar to `cp dir1/ dir2/`.

#### `fs.existsSync(path)`[#](#fsexistssyncpath)

Returns `true` if the path exists, `false` otherwise.

For detailed information, see the documentation of the asynchronous version of
this API: [`fs.exists()`](#fsexistspath-callback).

`fs.exists()` is deprecated, but `fs.existsSync()` is not. The `callback`
parameter to `fs.exists()` accepts parameters that are inconsistent with other
Node.js callbacks. `fs.existsSync()` does not use a callback.

```
import { existsSync } from 'node:fs';

if (existsSync('/etc/passwd'))
  console.log('The path exists.'); copy
```

#### `fs.fchmodSync(fd, mode)`[#](#fsfchmodsyncfd-mode)

Added in: v0.4.7

Sets the permissions on the file. Returns `undefined`.

See the POSIX [`fchmod(2)`](http://man7.org/linux/man-pages/man2/fchmod.2.html) documentation for more detail.

#### `fs.fchownSync(fd, uid, gid)`[#](#fsfchownsyncfd-uid-gid)

Added in: v0.4.7

Sets the owner of the file. Returns `undefined`.

See the POSIX [`fchown(2)`](http://man7.org/linux/man-pages/man2/fchown.2.html) documentation for more detail.

#### `fs.fdatasyncSync(fd)`[#](#fsfdatasyncsyncfd)

Added in: v0.1.96

Forces all currently queued I/O operations associated with the file to the
operating system's synchronized I/O completion state. Refer to the POSIX
[`fdatasync(2)`](http://man7.org/linux/man-pages/man2/fdatasync.2.html) documentation for details. Returns `undefined`.

#### `fs.fstatSync(fd[, options])`[#](#fsfstatsyncfd-options)

Retrieves the [<fs.Stats>](fs.html#class-fsstats) for the file descriptor.

See the POSIX [`fstat(2)`](http://man7.org/linux/man-pages/man2/fstat.2.html) documentation for more detail.

#### `fs.fsyncSync(fd)`[#](#fsfsyncsyncfd)

Added in: v0.1.96

Request that all data for the open file descriptor is flushed to the storage
device. The specific implementation is operating system and device specific.
Refer to the POSIX [`fsync(2)`](http://man7.org/linux/man-pages/man2/fsync.2.html) documentation for more detail. Returns `undefined`.

#### `fs.ftruncateSync(fd[, len])`[#](#fsftruncatesyncfd-len)

Added in: v0.8.6

Truncates the file descriptor. Returns `undefined`.

For detailed information, see the documentation of the asynchronous version of
this API: [`fs.ftruncate()`](#fsftruncatefd-len-callback).

#### `fs.futimesSync(fd, atime, mtime)`[#](#fsfutimessyncfd-atime-mtime)

Synchronous version of [`fs.futimes()`](#fsfutimesfd-atime-mtime-callback). Returns `undefined`.

#### `fs.lchmodSync(path, mode)`[#](#fslchmodsyncpath-mode)

Deprecated since: v0.4.7

Changes the permissions on a symbolic link. Returns `undefined`.

This method is only implemented on macOS.

See the POSIX [`lchmod(2)`](https://www.freebsd.org/cgi/man.cgi?query=lchmod&sektion=2) documentation for more detail.

#### `fs.lchownSync(path, uid, gid)`[#](#fslchownsyncpath-uid-gid)

Set the owner for the path. Returns `undefined`.

See the POSIX [`lchown(2)`](http://man7.org/linux/man-pages/man2/lchown.2.html) documentation for more details.

#### `fs.lutimesSync(path, atime, mtime)`[#](#fslutimessyncpath-atime-mtime)

Added in: v14.5.0, v12.19.0

Change the file system timestamps of the symbolic link referenced by `path`.
Returns `undefined`, or throws an exception when parameters are incorrect or
the operation fails. This is the synchronous version of [`fs.lutimes()`](#fslutimespath-atime-mtime-callback).

#### `fs.linkSync(existingPath, newPath)`[#](#fslinksyncexistingpath-newpath)

Creates a new link from the `existingPath` to the `newPath`. See the POSIX
[`link(2)`](http://man7.org/linux/man-pages/man2/link.2.html) documentation for more detail. Returns `undefined`.

#### `fs.lstatSync(path[, options])`[#](#fslstatsyncpath-options)

Retrieves the [<fs.Stats>](fs.html#class-fsstats) for the symbolic link referred to by `path`.

See the POSIX [`lstat(2)`](http://man7.org/linux/man-pages/man2/lstat.2.html) documentation for more details.

#### `fs.mkdirSync(path[, options])`[#](#fsmkdirsyncpath-options)

Synchronously creates a directory. Returns `undefined`, or if `recursive` is
`true`, the first directory path created.
This is the synchronous version of [`fs.mkdir()`](#fsmkdirpath-options-callback).

See the POSIX [`mkdir(2)`](http://man7.org/linux/man-pages/man2/mkdir.2.html) documentation for more details.

#### `fs.mkdtempSync(prefix[, options])`[#](#fsmkdtempsyncprefix-options)

Returns the created directory path.

For detailed information, see the documentation of the asynchronous version of
this API: [`fs.mkdtemp()`](#fsmkdtempprefix-options-callback).

The optional `options` argument can be a string specifying an encoding, or an
object with an `encoding` property specifying the character encoding to use.

#### `fs.mkdtempDisposableSync(prefix[, options])`[#](#fsmkdtempdisposablesyncprefix-options)

Added in: v24.4.0

Returns a disposable object whose `path` property holds the created directory
path. When the object is disposed, the directory and its contents will be
removed if it still exists. If the directory cannot be deleted, disposal will
throw an error. The object has a `remove()` method which will perform the same
task.

For detailed information, see the documentation of [`fs.mkdtemp()`](#fsmkdtempprefix-options-callback).

There is no callback-based version of this API because it is designed for use
with the `using` syntax.

The optional `options` argument can be a string specifying an encoding, or an
object with an `encoding` property specifying the character encoding to use.

#### `fs.opendirSync(path[, options])`[#](#fsopendirsyncpath-options)

Synchronously open a directory. See [`opendir(3)`](http://man7.org/linux/man-pages/man3/opendir.3.html).

Creates an [<fs.Dir>](fs.html#class-fsdir), which contains all further functions for reading from
and cleaning up the directory.

The `encoding` option sets the encoding for the `path` while opening the
directory and subsequent read operations.

#### `fs.openSync(path[, flags[, mode]])`[#](#fsopensyncpath-flags-mode)

Returns an integer representing the file descriptor.

For detailed information, see the documentation of the asynchronous version of
this API: [`fs.open()`](#fsopenpath-flags-mode-callback).

#### `fs.readdirSync(path[, options])`[#](#fsreaddirsyncpath-options)

Reads the contents of the directory.

See the POSIX [`readdir(3)`](http://man7.org/linux/man-pages/man3/readdir.3.html) documentation for more details.

The optional `options` argument can be a string specifying an encoding, or an
object with an `encoding` property specifying the character encoding to use for
the filenames returned. If the `encoding` is set to `'buffer'`,
the filenames returned will be passed as [<Buffer>](buffer.html#class-buffer) objects.

If `options.withFileTypes` is set to `true`, the result will contain
[<fs.Dirent>](fs.html#class-fsdirent) objects.

#### `fs.readFileSync(path[, options])`[#](#fsreadfilesyncpath-options)

Returns the contents of the `path`.

For detailed information, see the documentation of the asynchronous version of
this API: [`fs.readFile()`](#fsreadfilepath-options-callback).

If the `encoding` option is specified then this function returns a
string. Otherwise it returns a buffer.

Similar to [`fs.readFile()`](#fsreadfilepath-options-callback), when the path is a directory, the behavior of
`fs.readFileSync()` is platform-specific.

```
import { readFileSync } from 'node:fs';


readFileSync('<directory>');



readFileSync('<directory>');  copy
```

#### `fs.readlinkSync(path[, options])`[#](#fsreadlinksyncpath-options)

Returns the symbolic link's string value.

See the POSIX [`readlink(2)`](http://man7.org/linux/man-pages/man2/readlink.2.html) documentation for more details.

The optional `options` argument can be a string specifying an encoding, or an
object with an `encoding` property specifying the character encoding to use for
the link path returned. If the `encoding` is set to `'buffer'`,
the link path returned will be passed as a [<Buffer>](buffer.html#class-buffer) object.

#### `fs.readSync(fd, buffer, offset, length[, position])`[#](#fsreadsyncfd-buffer-offset-length-position)

Returns the number of `bytesRead`.

For detailed information, see the documentation of the asynchronous version of
this API: [`fs.read()`](#fsreadfd-buffer-offset-length-position-callback).

#### `fs.readSync(fd, buffer[, options])`[#](#fsreadsyncfd-buffer-options)

Returns the number of `bytesRead`.

Similar to the above `fs.readSync` function, this version takes an optional `options` object.
If no `options` object is specified, it will default with the above values.

For detailed information, see the documentation of the asynchronous version of
this API: [`fs.read()`](#fsreadfd-buffer-offset-length-position-callback).

#### `fs.readvSync(fd, buffers[, position])`[#](#fsreadvsyncfd-buffers-position)

Added in: v13.13.0, v12.17.0

For detailed information, see the documentation of the asynchronous version of
this API: [`fs.readv()`](#fsreadvfd-buffers-position-callback).

#### `fs.realpathSync(path[, options])`[#](#fsrealpathsyncpath-options)

Returns the resolved pathname.

For detailed information, see the documentation of the asynchronous version of
this API: [`fs.realpath()`](#fsrealpathpath-options-callback).

#### `fs.realpathSync.native(path[, options])`[#](#fsrealpathsyncnativepath-options)

Added in: v9.2.0

Synchronous [`realpath(3)`](http://man7.org/linux/man-pages/man3/realpath.3.html).

Only paths that can be converted to UTF8 strings are supported.

The optional `options` argument can be a string specifying an encoding, or an
object with an `encoding` property specifying the character encoding to use for
the path returned. If the `encoding` is set to `'buffer'`,
the path returned will be passed as a [<Buffer>](buffer.html#class-buffer) object.

On Linux, when Node.js is linked against musl libc, the procfs file system must
be mounted on `/proc` in order for this function to work. Glibc does not have
this restriction.

#### `fs.renameSync(oldPath, newPath)`[#](#fsrenamesyncoldpath-newpath)

Renames the file from `oldPath` to `newPath`. Returns `undefined`.

See the POSIX [`rename(2)`](http://man7.org/linux/man-pages/man2/rename.2.html) documentation for more details.

#### `fs.rmdirSync(path[, options])`[#](#fsrmdirsyncpath-options)

* `path` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) | [<Buffer>](buffer.html#class-buffer) | [<URL>](url.html#the-whatwg-url-api)
* `options` [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)
  + `maxRetries` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) If an `EBUSY`, `EMFILE`, `ENFILE`, `ENOTEMPTY`, or
    `EPERM` error is encountered, Node.js retries the operation with a linear
    backoff wait of `retryDelay` milliseconds longer on each try. This option
    represents the number of retries. This option is ignored if the `recursive`
    option is not `true`. **Default:** `0`.
  + `recursive` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) If `true`, perform a recursive directory removal. In
    recursive mode, operations are retried on failure. **Default:** `false`.
    **Deprecated.**
  + `retryDelay` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) The amount of time in milliseconds to wait between
    retries. This option is ignored if the `recursive` option is not `true`.
    **Default:** `100`.

Synchronous [`rmdir(2)`](http://man7.org/linux/man-pages/man2/rmdir.2.html). Returns `undefined`.

Using `fs.rmdirSync()` on a file (not a directory) results in an `ENOENT` error
on Windows and an `ENOTDIR` error on POSIX.

To get a behavior similar to the `rm -rf` Unix command, use [`fs.rmSync()`](#fsrmsyncpath-options)
with options `{ recursive: true, force: true }`.

#### `fs.rmSync(path[, options])`[#](#fsrmsyncpath-options)

* `path` [<string>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#String_type) | [<Buffer>](buffer.html#class-buffer) | [<URL>](url.html#the-whatwg-url-api)
* `options` [<Object>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)
  + `force` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) When `true`, exceptions will be ignored if `path` does
    not exist. **Default:** `false`.
  + `maxRetries` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) If an `EBUSY`, `EMFILE`, `ENFILE`, `ENOTEMPTY`, or
    `EPERM` error is encountered, Node.js will retry the operation with a linear
    backoff wait of `retryDelay` milliseconds longer on each try. This option
    represents the number of retries. This option is ignored if the `recursive`
    option is not `true`. **Default:** `0`.
  + `recursive` [<boolean>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Boolean_type) If `true`, perform a recursive directory removal. In
    recursive mode operations are retried on failure. **Default:** `false`.
  + `retryDelay` [<integer>](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Number_type) The amount of time in milliseconds to wait between
    retries. This option is ignored if the `recursive` option is not `true`.
    **Default:** `100`.

Synchronously removes files and directories (modeled on the standard POSIX `rm`
utility). Returns `undefined`.

#### `fs.statSync(path[, options])`[#](#fsstatsyncpath-options)

Retrieves the [<fs.Stats>](fs.html#class-fsstats) for the path.

#### `fs.statfsSync(path[, options])`[#](#fsstatfssyncpath-options)

Added in: v19.6.0, v18.15.0

Synchronous [`statfs(2)`](http://man7.org/linux/man-pages/man2/statfs.2.html). Returns information about the mounted file system which
contains `path`.

In case of an error, the `err.code` will be one of [Common System Errors](errors.html#common-system-errors).

#### `fs.symlinkSync(target, path[, type])`[#](#fssymlinksynctarget-path-type)

For detailed information, see the documentation of the asynchronous version of
this API: [`fs.symlink()`](#fssymlinktarget-path-type-callback).

#### `fs.truncateSync(path[, len])`[#](#fstruncatesyncpath-len)

Added in: v0.8.6

Truncates the file. Returns `undefined`. A file descriptor can also be
passed as the first argument. In this case, `fs.ftruncateSync()` is called.

Passing a file descriptor is deprecated and may result in an error being thrown
in the future.

#### `fs.unlinkSync(path)`[#](#fsunlinksyncpath)

Synchronous [`unlink(2)`](http://man7.org/linux/man-pages/man2/unlink.2.html). Returns `undefined`.

#### `fs.utimesSync(path, atime, mtime)`[#](#fsutimessyncpath-atime-mtime)

For detailed information, see the documentation of the asynchronous version of
this API: [`fs.utimes()`](#fsutimespath-atime-mtime-callback).

#### `fs.writeFileSync(file, data[, options])`[#](#fswritefilesyncfile-data-options)

The `mode` option only affects the newly created file. See [`fs.open()`](#fsopenpath-flags-mode-callback)
for more details.

For detailed information, see the documentation of the asynchronous version of
this API: [`fs.writeFile()`](#fswritefilefile-data-options-callback).

#### `fs.writeSync(fd, buffer, offset[, length[, position]])`[#](#fswritesyncfd-buffer-offset-length-position)

For detailed information, see the documentation of the asynchronous version of
this API: [`fs.write(fd, buffer...)`](#fswritefd-buffer-offset-length-position-callback).

#### `fs.writeSync(fd, buffer[, options])`[#](#fswritesyncfd-buffer-options)

Added in: v18.3.0, v16.17.0

For detailed information, see the documentation of the asynchronous version of
this API: [`fs.write(fd, buffer...)`](#fswritefd-buffer-offset-length-position-callback).

#### `fs.writeSync(fd, string[, position[, encoding]])`[#](#fswritesyncfd-string-position-encoding)

For detailed information, see the documentation of the asynchronous version of
this API: [`fs.write(fd, string...)`](#fswritefd-string-position-encoding-callback).

#### `fs.writevSync(fd, buffers[, position])`[#](#fswritevsyncfd-buffers-position)

Added in: v12.9.0

For detailed information, see the documentation of the asynchronous version of
this API: [`fs.writev()`](#fswritevfd-buffers-position-callback).