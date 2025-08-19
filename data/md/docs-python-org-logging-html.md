This page contains tutorial information. For links to reference information and a
logging cookbook, please see [Other resources](#tutorial-ref-links).

## Basic Logging Tutorial

Logging is a means of tracking events that happen when some software runs. The
softwareâs developer adds logging calls to their code to indicate that certain
events have occurred. An event is described by a descriptive message which can
optionally contain variable data (i.e. data that is potentially different for
each occurrence of the event). Events also have an importance which the
developer ascribes to the event; the importance can also be called the *level*
or *severity*.

### When to use logging

You can access logging functionality by creating a logger via `logger =
getLogger(__name__)`, and then calling the loggerâs [`debug()`](../library/logging.html#logging.Logger.debug "logging.Logger.debug"),
[`info()`](../library/logging.html#logging.Logger.info "logging.Logger.info"), [`warning()`](../library/logging.html#logging.Logger.warning "logging.Logger.warning"), [`error()`](../library/logging.html#logging.Logger.error "logging.Logger.error") and
[`critical()`](../library/logging.html#logging.Logger.critical "logging.Logger.critical") methods. To determine when to use logging, and to see
which logger methods to use when, see the table below. It states, for each of a
set of common tasks, the best tool to use for that task.

| Task you want to perform | The best tool for the task |
| --- | --- |
| Display console output for ordinary usage of a command line script or program | [`print()`](../library/functions.html#print "print") |
| Report events that occur during normal operation of a program (e.g. for status monitoring or fault investigation) | A loggerâs [`info()`](../library/logging.html#logging.Logger.info "logging.Logger.info") (or [`debug()`](../library/logging.html#logging.Logger.debug "logging.Logger.debug") method for very detailed output for diagnostic purposes) |
| Issue a warning regarding a particular runtime event | [`warnings.warn()`](../library/warnings.html#warnings.warn "warnings.warn") in library code if the issue is avoidable and the client application should be modified to eliminate the warning  A loggerâs [`warning()`](../library/logging.html#logging.Logger.warning "logging.Logger.warning") method if there is nothing the client application can do about the situation, but the event should still be noted |
| Report an error regarding a particular runtime event | Raise an exception |
| Report suppression of an error without raising an exception (e.g. error handler in a long-running server process) | A loggerâs [`error()`](../library/logging.html#logging.Logger.error "logging.Logger.error"), [`exception()`](../library/logging.html#logging.Logger.exception "logging.Logger.exception") or [`critical()`](../library/logging.html#logging.Logger.critical "logging.Logger.critical") method as appropriate for the specific error and application domain |

The logger methods are named after the level or severity of the events
they are used to track. The standard levels and their applicability are
described below (in increasing order of severity):

| Level | When itâs used |
| --- | --- |
| `DEBUG` | Detailed information, typically of interest only when diagnosing problems. |
| `INFO` | Confirmation that things are working as expected. |
| `WARNING` | An indication that something unexpected happened, or indicative of some problem in the near future (e.g. âdisk space lowâ). The software is still working as expected. |
| `ERROR` | Due to a more serious problem, the software has not been able to perform some function. |
| `CRITICAL` | A serious error, indicating that the program itself may be unable to continue running. |

The default level is `WARNING`, which means that only events of this severity and higher
will be tracked, unless the logging package is configured to do otherwise.

Events that are tracked can be handled in different ways. The simplest way of
handling tracked events is to print them to the console. Another common way
is to write them to a disk file.

### A simple example

A very simple example is:

```
import logging
logging.warning('Watch out!')  # will print a message to the console
logging.info('I told you so')  # will not print anything
```

If you type these lines into a script and run it, youâll see:

printed out on the console. The `INFO` message doesnât appear because the
default level is `WARNING`. The printed message includes the indication of the
level and the description of the event provided in the logging call, i.e.
âWatch out!â. The actual output can be formatted quite flexibly if you need
that; formatting options will also be explained later.

Notice that in this example, we use functions directly on the `logging`
module, like `logging.debug`, rather than creating a logger and calling
functions on it. These functions operation on the root logger, but can be useful
as they will call [`basicConfig()`](../library/logging.html#logging.basicConfig "logging.basicConfig") for you if it has not been called yet, like in
this example. In larger programs youâll usually want to control the logging
configuration explicitly however - so for that reason as well as others, itâs
better to create loggers and call their methods.

### Logging to a file

A very common situation is that of recording logging events in a file, so letâs
look at that next. Be sure to try the following in a newly started Python
interpreter, and donât just continue from the session described above:

```
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logger.debug('This message should go to the log file')
logger.info('So should this')
logger.warning('And this, too')
logger.error('And non-ASCII stuff, too, like Ãresund and MalmÃ¶')
```

Changed in version 3.9: The *encoding* argument was added. In earlier Python versions, or if not
specified, the encoding used is the default value used by [`open()`](../library/functions.html#open "open"). While
not shown in the above example, an *errors* argument can also now be passed,
which determines how encoding errors are handled. For available values and
the default, see the documentation for [`open()`](../library/functions.html#open "open").

And now if we open the file and look at what we have, we should find the log
messages:

```
DEBUG:__main__:This message should go to the log file
INFO:__main__:So should this
WARNING:__main__:And this, too
ERROR:__main__:And non-ASCII stuff, too, like Ãresund and MalmÃ¶
```

This example also shows how you can set the logging level which acts as the
threshold for tracking. In this case, because we set the threshold to
`DEBUG`, all of the messages were printed.

If you want to set the logging level from a command-line option such as:

and you have the value of the parameter passed for `--log` in some variable
*loglevel*, you can use:

```
getattr(logging, loglevel.upper())
```

to get the value which youâll pass to [`basicConfig()`](../library/logging.html#logging.basicConfig "logging.basicConfig") via the *level*
argument. You may want to error check any user input value, perhaps as in the
following example:

```
# assuming loglevel is bound to the string value obtained from the
# command line argument. Convert to upper case to allow the user to
# specify --log=DEBUG or --log=debug
numeric_level = getattr(logging, loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(level=numeric_level, ...)
```

The call to [`basicConfig()`](../library/logging.html#logging.basicConfig "logging.basicConfig") should come *before* any calls to a loggerâs
methods such as [`debug()`](../library/logging.html#logging.Logger.debug "logging.Logger.debug"), [`info()`](../library/logging.html#logging.Logger.info "logging.Logger.info"), etc. Otherwise,
that logging event may not be handled in the desired manner.

If you run the above script several times, the messages from successive runs
are appended to the file *example.log*. If you want each run to start afresh,
not remembering the messages from earlier runs, you can specify the *filemode*
argument, by changing the call in the above example to:

```
logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)
```

The output will be the same as before, but the log file is no longer appended
to, so the messages from earlier runs are lost.

### Logging variable data

To log variable data, use a format string for the event description message and
append the variable data as arguments. For example:

```
import logging
logging.warning('%s before you %s', 'Look', 'leap!')
```

will display:

```
WARNING:root:Look before you leap!
```

As you can see, merging of variable data into the event description message
uses the old, %-style of string formatting. This is for backwards
compatibility: the logging package pre-dates newer formatting options such as
[`str.format()`](../library/stdtypes.html#str.format "str.format") and [`string.Template`](../library/string.html#string.Template "string.Template"). These newer formatting
options *are* supported, but exploring them is outside the scope of this
tutorial: see [Using particular formatting styles throughout your application](logging-cookbook.html#formatting-styles) for more information.

### Changing the format of displayed messages

To change the format which is used to display messages, you need to
specify the format you want to use:

```
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.debug('This message should appear on the console')
logging.info('So should this')
logging.warning('And this, too')
```

which would print:

```
DEBUG:This message should appear on the console
INFO:So should this
WARNING:And this, too
```

Notice that the ârootâ which appeared in earlier examples has disappeared. For
a full set of things that can appear in format strings, you can refer to the
documentation for [LogRecord attributes](../library/logging.html#logrecord-attributes), but for simple usage, you just
need the *levelname* (severity), *message* (event description, including
variable data) and perhaps to display when the event occurred. This is
described in the next section.

### Displaying the date/time in messages

To display the date and time of an event, you would place â%(asctime)sâ in
your format string:

```
import logging
logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is when this event was logged.')
```

which should print something like this:

```
2010-12-12 11:41:42,612 is when this event was logged.
```

The default format for date/time display (shown above) is like ISO8601 or
[**RFC 3339**](https://datatracker.ietf.org/doc/html/rfc3339.html). If you need more control over the formatting of the date/time, provide
a *datefmt* argument to `basicConfig`, as in this example:

```
import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.warning('is when this event was logged.')
```

which would display something like this:

```
12/12/2010 11:46:36 AM is when this event was logged.
```

The format of the *datefmt* argument is the same as supported by
[`time.strftime()`](../library/time.html#time.strftime "time.strftime").

### Next Steps

That concludes the basic tutorial. It should be enough to get you up and
running with logging. Thereâs a lot more that the logging package offers, but
to get the best out of it, youâll need to invest a little more of your time in
reading the following sections. If youâre ready for that, grab some of your
favourite beverage and carry on.

If your logging needs are simple, then use the above examples to incorporate
logging into your own scripts, and if you run into problems or donât understand
something, please post a question in the Help category of the [Python
discussion forum](https://discuss.python.org/c/help/7) and you should receive
help before too long.

Still here? You can carry on reading the next few sections, which provide a
slightly more advanced/in-depth tutorial than the basic one above. After that,
you can take a look at the [Logging Cookbook](logging-cookbook.html#logging-cookbook).

## Advanced Logging Tutorial

The logging library takes a modular approach and offers several categories
of components: loggers, handlers, filters, and formatters.

* Loggers expose the interface that application code directly uses.
* Handlers send the log records (created by loggers) to the appropriate
  destination.
* Filters provide a finer grained facility for determining which log records
  to output.
* Formatters specify the layout of log records in the final output.

Log event information is passed between loggers, handlers, filters and
formatters in a [`LogRecord`](../library/logging.html#logging.LogRecord "logging.LogRecord") instance.

Logging is performed by calling methods on instances of the [`Logger`](../library/logging.html#logging.Logger "logging.Logger")
class (hereafter called *loggers*). Each instance has a name, and they are
conceptually arranged in a namespace hierarchy using dots (periods) as
separators. For example, a logger named âscanâ is the parent of loggers
âscan.textâ, âscan.htmlâ and âscan.pdfâ. Logger names can be anything you want,
and indicate the area of an application in which a logged message originates.

A good convention to use when naming loggers is to use a module-level logger,
in each module which uses logging, named as follows:

```
logger = logging.getLogger(__name__)
```

This means that logger names track the package/module hierarchy, and itâs
intuitively obvious where events are logged just from the logger name.

The root of the hierarchy of loggers is called the root logger. Thatâs the
logger used by the functions [`debug()`](../library/logging.html#logging.debug "logging.debug"), [`info()`](../library/logging.html#logging.info "logging.info"), [`warning()`](../library/logging.html#logging.warning "logging.warning"),
[`error()`](../library/logging.html#logging.error "logging.error") and [`critical()`](../library/logging.html#logging.critical "logging.critical"), which just call the same-named method of
the root logger. The functions and the methods have the same signatures. The
root loggerâs name is printed as ârootâ in the logged output.

It is, of course, possible to log messages to different destinations. Support
is included in the package for writing log messages to files, HTTP GET/POST
locations, email via SMTP, generic sockets, queues, or OS-specific logging
mechanisms such as syslog or the Windows NT event log. Destinations are served
by *handler* classes. You can create your own log destination class if
you have special requirements not met by any of the built-in handler classes.

By default, no destination is set for any logging messages. You can specify
a destination (such as console or file) by using [`basicConfig()`](../library/logging.html#logging.basicConfig "logging.basicConfig") as in the
tutorial examples. If you call the functions [`debug()`](../library/logging.html#logging.debug "logging.debug"), [`info()`](../library/logging.html#logging.info "logging.info"),
[`warning()`](../library/logging.html#logging.warning "logging.warning"), [`error()`](../library/logging.html#logging.error "logging.error") and [`critical()`](../library/logging.html#logging.critical "logging.critical"), they will check to see
if no destination is set; and if one is not set, they will set a destination
of the console (`sys.stderr`) and a default format for the displayed
message before delegating to the root logger to do the actual message output.

The default format set by [`basicConfig()`](../library/logging.html#logging.basicConfig "logging.basicConfig") for messages is:

```
severity:logger name:message
```

You can change this by passing a format string to [`basicConfig()`](../library/logging.html#logging.basicConfig "logging.basicConfig") with the
*format* keyword argument. For all options regarding how a format string is
constructed, see [Formatter Objects](../library/logging.html#formatter-objects).

### Logging Flow

The flow of log event information in loggers and handlers is illustrated in the
following diagram.

Logger flow



Create
LogRecord









Logging call in user
code, e.g.

logger.info(...)







Stop



Does a filter attached
to logger reject the
record?







Pass record to
handlers of
current logger



Is propagate true for
current logger?



Is there a parent
logger?



Set current
logger to parent



At least one handler
in hierarchy?



Use
lastResort
handler



Handler enabled for
level of record?



Does a filter attached
to handler reject the
record?



Stop



Emit (includes formatting)

Handler flow



Logger enabled for
level of call?





























































No

Yes

Yes

No

No

Yes

Yes

No

No

Yes




No







Yes

No




Yes

Record passed
to handler

### Loggers

[`Logger`](../library/logging.html#logging.Logger "logging.Logger") objects have a threefold job. First, they expose several
methods to application code so that applications can log messages at runtime.
Second, logger objects determine which log messages to act upon based upon
severity (the default filtering facility) or filter objects. Third, logger
objects pass along relevant log messages to all interested log handlers.

The most widely used methods on logger objects fall into two categories:
configuration and message sending.

These are the most common configuration methods:

* [`Logger.setLevel()`](../library/logging.html#logging.Logger.setLevel "logging.Logger.setLevel") specifies the lowest-severity log message a logger
  will handle, where debug is the lowest built-in severity level and critical
  is the highest built-in severity. For example, if the severity level is
  INFO, the logger will handle only INFO, WARNING, ERROR, and CRITICAL messages
  and will ignore DEBUG messages.
* [`Logger.addHandler()`](../library/logging.html#logging.Logger.addHandler "logging.Logger.addHandler") and [`Logger.removeHandler()`](../library/logging.html#logging.Logger.removeHandler "logging.Logger.removeHandler") add and remove
  handler objects from the logger object. Handlers are covered in more detail
  in [Handlers](#handler-basic).
* [`Logger.addFilter()`](../library/logging.html#logging.Logger.addFilter "logging.Logger.addFilter") and [`Logger.removeFilter()`](../library/logging.html#logging.Logger.removeFilter "logging.Logger.removeFilter") add and remove filter
  objects from the logger object. Filters are covered in more detail in
  [Filter Objects](../library/logging.html#filter).

You donât need to always call these methods on every logger you create. See the
last two paragraphs in this section.

With the logger object configured, the following methods create log messages:

* [`Logger.debug()`](../library/logging.html#logging.Logger.debug "logging.Logger.debug"), [`Logger.info()`](../library/logging.html#logging.Logger.info "logging.Logger.info"), [`Logger.warning()`](../library/logging.html#logging.Logger.warning "logging.Logger.warning"),
  [`Logger.error()`](../library/logging.html#logging.Logger.error "logging.Logger.error"), and [`Logger.critical()`](../library/logging.html#logging.Logger.critical "logging.Logger.critical") all create log records with
  a message and a level that corresponds to their respective method names. The
  message is actually a format string, which may contain the standard string
  substitution syntax of `%s`, `%d`, `%f`, and so on. The
  rest of their arguments is a list of objects that correspond with the
  substitution fields in the message. With regard to `**kwargs`, the
  logging methods care only about a keyword of `exc_info` and use it to
  determine whether to log exception information.
* [`Logger.exception()`](../library/logging.html#logging.Logger.exception "logging.Logger.exception") creates a log message similar to
  [`Logger.error()`](../library/logging.html#logging.Logger.error "logging.Logger.error"). The difference is that [`Logger.exception()`](../library/logging.html#logging.Logger.exception "logging.Logger.exception") dumps a
  stack trace along with it. Call this method only from an exception handler.
* [`Logger.log()`](../library/logging.html#logging.Logger.log "logging.Logger.log") takes a log level as an explicit argument. This is a
  little more verbose for logging messages than using the log level convenience
  methods listed above, but this is how to log at custom log levels.

[`getLogger()`](../library/logging.html#logging.getLogger "logging.getLogger") returns a reference to a logger instance with the specified
name if it is provided, or `root` if not. The names are period-separated
hierarchical structures. Multiple calls to [`getLogger()`](../library/logging.html#logging.getLogger "logging.getLogger") with the same name
will return a reference to the same logger object. Loggers that are further
down in the hierarchical list are children of loggers higher up in the list.
For example, given a logger with a name of `foo`, loggers with names of
`foo.bar`, `foo.bar.baz`, and `foo.bam` are all descendants of `foo`.

Loggers have a concept of *effective level*. If a level is not explicitly set
on a logger, the level of its parent is used instead as its effective level.
If the parent has no explicit level set, *its* parent is examined, and so on -
all ancestors are searched until an explicitly set level is found. The root
logger always has an explicit level set (`WARNING` by default). When deciding
whether to process an event, the effective level of the logger is used to
determine whether the event is passed to the loggerâs handlers.

Child loggers propagate messages up to the handlers associated with their
ancestor loggers. Because of this, it is unnecessary to define and configure
handlers for all the loggers an application uses. It is sufficient to
configure handlers for a top-level logger and create child loggers as needed.
(You can, however, turn off propagation by setting the *propagate*
attribute of a logger to `False`.)

### Handlers

[`Handler`](../library/logging.html#logging.Handler "logging.Handler") objects are responsible for dispatching the
appropriate log messages (based on the log messagesâ severity) to the handlerâs
specified destination. [`Logger`](../library/logging.html#logging.Logger "logging.Logger") objects can add zero or more handler
objects to themselves with an [`addHandler()`](../library/logging.html#logging.Logger.addHandler "logging.Logger.addHandler") method. As an example
scenario, an application may want to send all log messages to a log file, all
log messages of error or higher to stdout, and all messages of critical to an
email address. This scenario requires three individual handlers where each
handler is responsible for sending messages of a specific severity to a specific
location.

The standard library includes quite a few handler types (see
[Useful Handlers](#useful-handlers)); the tutorials use mainly [`StreamHandler`](../library/logging.handlers.html#logging.StreamHandler "logging.StreamHandler") and
[`FileHandler`](../library/logging.handlers.html#logging.FileHandler "logging.FileHandler") in its examples.

There are very few methods in a handler for application developers to concern
themselves with. The only handler methods that seem relevant for application
developers who are using the built-in handler objects (that is, not creating
custom handlers) are the following configuration methods:

* The [`setLevel()`](../library/logging.html#logging.Handler.setLevel "logging.Handler.setLevel") method, just as in logger objects, specifies the
  lowest severity that will be dispatched to the appropriate destination. Why
  are there two [`setLevel()`](../library/logging.html#logging.Handler.setLevel "logging.Handler.setLevel") methods? The level set in the logger
  determines which severity of messages it will pass to its handlers. The level
  set in each handler determines which messages that handler will send on.
* [`setFormatter()`](../library/logging.html#logging.Handler.setFormatter "logging.Handler.setFormatter") selects a Formatter object for this handler to
  use.
* [`addFilter()`](../library/logging.html#logging.Handler.addFilter "logging.Handler.addFilter") and [`removeFilter()`](../library/logging.html#logging.Handler.removeFilter "logging.Handler.removeFilter") respectively
  configure and deconfigure filter objects on handlers.

Application code should not directly instantiate and use instances of
[`Handler`](../library/logging.html#logging.Handler "logging.Handler"). Instead, the [`Handler`](../library/logging.html#logging.Handler "logging.Handler") class is a base class that
defines the interface that all handlers should have and establishes some
default behavior that child classes can use (or override).

### Formatters

Formatter objects configure the final order, structure, and contents of the log
message. Unlike the base [`logging.Handler`](../library/logging.html#logging.Handler "logging.Handler") class, application code may
instantiate formatter classes, although you could likely subclass the formatter
if your application needs special behavior. The constructor takes three
optional arguments â a message format string, a date format string and a style
indicator.

logging.Formatter.\_\_init\_\_(*fmt=None*, *datefmt=None*, *style='%'*)

If there is no message format string, the default is to use the
raw message. If there is no date format string, the default date format is:

with the milliseconds tacked on at the end. The `style` is one of `'%'`,
`'{'`, or `'$'`. If one of these is not specified, then `'%'` will be used.

If the `style` is `'%'`, the message format string uses
`%(<dictionary key>)s` styled string substitution; the possible keys are
documented in [LogRecord attributes](../library/logging.html#logrecord-attributes). If the style is `'{'`, the message
format string is assumed to be compatible with [`str.format()`](../library/stdtypes.html#str.format "str.format") (using
keyword arguments), while if the style is `'$'` then the message format string
should conform to what is expected by [`string.Template.substitute()`](../library/string.html#string.Template.substitute "string.Template.substitute").

Changed in version 3.2: Added the `style` parameter.

The following message format string will log the time in a human-readable
format, the severity of the message, and the contents of the message, in that
order:

```
'%(asctime)s - %(levelname)s - %(message)s'
```

Formatters use a user-configurable function to convert the creation time of a
record to a tuple. By default, [`time.localtime()`](../library/time.html#time.localtime "time.localtime") is used; to change this
for a particular formatter instance, set the `converter` attribute of the
instance to a function with the same signature as [`time.localtime()`](../library/time.html#time.localtime "time.localtime") or
[`time.gmtime()`](../library/time.html#time.gmtime "time.gmtime"). To change it for all formatters, for example if you want
all logging times to be shown in GMT, set the `converter` attribute in the
Formatter class (to `time.gmtime` for GMT display).

### Configuring Logging

Programmers can configure logging in three ways:

1. Creating loggers, handlers, and formatters explicitly using Python
   code that calls the configuration methods listed above.
2. Creating a logging config file and reading it using the [`fileConfig()`](../library/logging.config.html#logging.config.fileConfig "logging.config.fileConfig")
   function.
3. Creating a dictionary of configuration information and passing it
   to the [`dictConfig()`](../library/logging.config.html#logging.config.dictConfig "logging.config.dictConfig") function.

For the reference documentation on the last two options, see
[Configuration functions](../library/logging.config.html#logging-config-api). The following example configures a very simple
logger, a console handler, and a simple formatter using Python code:

```
import logging

# create logger
logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')
```

Running this module from the command line produces the following output:

```
$ python simple_logging_module.py
2005-03-19 15:10:26,618 - simple_example - DEBUG - debug message
2005-03-19 15:10:26,620 - simple_example - INFO - info message
2005-03-19 15:10:26,695 - simple_example - WARNING - warn message
2005-03-19 15:10:26,697 - simple_example - ERROR - error message
2005-03-19 15:10:26,773 - simple_example - CRITICAL - critical message
```

The following Python module creates a logger, handler, and formatter nearly
identical to those in the example listed above, with the only difference being
the names of the objects:

```
import logging
import logging.config

logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('simpleExample')

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')
```

Here is the logging.conf file:

```
[loggers]
keys=root,simpleExample

[handlers]
keys=consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_simpleExample]
level=DEBUG
handlers=consoleHandler
qualname=simpleExample
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

The output is nearly identical to that of the non-config-file-based example:

```
$ python simple_logging_config.py
2005-03-19 15:38:55,977 - simpleExample - DEBUG - debug message
2005-03-19 15:38:55,979 - simpleExample - INFO - info message
2005-03-19 15:38:56,054 - simpleExample - WARNING - warn message
2005-03-19 15:38:56,055 - simpleExample - ERROR - error message
2005-03-19 15:38:56,130 - simpleExample - CRITICAL - critical message
```

You can see that the config file approach has a few advantages over the Python
code approach, mainly separation of configuration and code and the ability of
noncoders to easily modify the logging properties.

Warning

The [`fileConfig()`](../library/logging.config.html#logging.config.fileConfig "logging.config.fileConfig") function takes a default parameter,
`disable_existing_loggers`, which defaults to `True` for reasons of
backward compatibility. This may or may not be what you want, since it
will cause any non-root loggers existing before the [`fileConfig()`](../library/logging.config.html#logging.config.fileConfig "logging.config.fileConfig")
call to be disabled unless they (or an ancestor) are explicitly named in
the configuration. Please refer to the reference documentation for more
information, and specify `False` for this parameter if you wish.

The dictionary passed to [`dictConfig()`](../library/logging.config.html#logging.config.dictConfig "logging.config.dictConfig") can also specify a Boolean
value with key `disable_existing_loggers`, which if not specified
explicitly in the dictionary also defaults to being interpreted as
`True`. This leads to the logger-disabling behaviour described above,
which may not be what you want - in which case, provide the key
explicitly with a value of `False`.

Note that the class names referenced in config files need to be either relative
to the logging module, or absolute values which can be resolved using normal
import mechanisms. Thus, you could use either
[`WatchedFileHandler`](../library/logging.handlers.html#logging.handlers.WatchedFileHandler "logging.handlers.WatchedFileHandler") (relative to the logging module) or
`mypackage.mymodule.MyHandler` (for a class defined in package `mypackage`
and module `mymodule`, where `mypackage` is available on the Python import
path).

In Python 3.2, a new means of configuring logging has been introduced, using
dictionaries to hold configuration information. This provides a superset of the
functionality of the config-file-based approach outlined above, and is the
recommended configuration method for new applications and deployments. Because
a Python dictionary is used to hold configuration information, and since you
can populate that dictionary using different means, you have more options for
configuration. For example, you can use a configuration file in JSON format,
or, if you have access to YAML processing functionality, a file in YAML
format, to populate the configuration dictionary. Or, of course, you can
construct the dictionary in Python code, receive it in pickled form over a
socket, or use whatever approach makes sense for your application.

Hereâs an example of the same configuration as above, in YAML format for
the new dictionary-based approach:

```
version: 1
formatters:
  simple:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: simple
    stream: ext://sys.stdout
loggers:
  simpleExample:
    level: DEBUG
    handlers: [console]
    propagate: no
root:
  level: DEBUG
  handlers: [console]
```

For more information about logging using a dictionary, see
[Configuration functions](../library/logging.config.html#logging-config-api).

### What happens if no configuration is provided

If no logging configuration is provided, it is possible to have a situation
where a logging event needs to be output, but no handlers can be found to
output the event.

The event is output using a âhandler of last resortâ, stored in
[`lastResort`](../library/logging.html#logging.lastResort "logging.lastResort"). This internal handler is not associated with any
logger, and acts like a [`StreamHandler`](../library/logging.handlers.html#logging.StreamHandler "logging.StreamHandler") which writes the
event description message to the current value of `sys.stderr` (therefore
respecting any redirections which may be in effect). No formatting is
done on the message - just the bare event description message is printed.
The handlerâs level is set to `WARNING`, so all events at this and
greater severities will be output.

Changed in version 3.2: For versions of Python prior to 3.2, the behaviour is as follows:

* If [`raiseExceptions`](../library/logging.html#logging.raiseExceptions "logging.raiseExceptions") is `False` (production mode), the event is
  silently dropped.
* If [`raiseExceptions`](../library/logging.html#logging.raiseExceptions "logging.raiseExceptions") is `True` (development mode), a message
  âNo handlers could be found for logger X.Y.Zâ is printed once.

To obtain the pre-3.2 behaviour,
[`lastResort`](../library/logging.html#logging.lastResort "logging.lastResort") can be set to `None`.

### Configuring Logging for a Library

When developing a library which uses logging, you should take care to
document how the library uses logging - for example, the names of loggers
used. Some consideration also needs to be given to its logging configuration.
If the using application does not use logging, and library code makes logging
calls, then (as described in the previous section) events of severity
`WARNING` and greater will be printed to `sys.stderr`. This is regarded as
the best default behaviour.

If for some reason you *donât* want these messages printed in the absence of
any logging configuration, you can attach a do-nothing handler to the top-level
logger for your library. This avoids the message being printed, since a handler
will always be found for the libraryâs events: it just doesnât produce any
output. If the library user configures logging for application use, presumably
that configuration will add some handlers, and if levels are suitably
configured then logging calls made in library code will send output to those
handlers, as normal.

A do-nothing handler is included in the logging package:
[`NullHandler`](../library/logging.handlers.html#logging.NullHandler "logging.NullHandler") (since Python 3.1). An instance of this handler
could be added to the top-level logger of the logging namespace used by the
library (*if* you want to prevent your libraryâs logged events being output to
`sys.stderr` in the absence of logging configuration). If all logging by a
library *foo* is done using loggers with names matching âfoo.xâ, âfoo.x.yâ,
etc. then the code:

```
import logging
logging.getLogger('foo').addHandler(logging.NullHandler())
```

should have the desired effect. If an organisation produces a number of
libraries, then the logger name specified can be âorgname.fooâ rather than
just âfooâ.

Note

It is strongly advised that you *do not log to the root logger*
in your library. Instead, use a logger with a unique and easily
identifiable name, such as the `__name__` for your libraryâs top-level package
or module. Logging to the root logger will make it difficult or impossible for
the application developer to configure the logging verbosity or handlers of
your library as they wish.

Note

It is strongly advised that you *do not add any handlers other
than* [`NullHandler`](../library/logging.handlers.html#logging.NullHandler "logging.NullHandler") *to your libraryâs loggers*. This is
because the configuration of handlers is the prerogative of the application
developer who uses your library. The application developer knows their
target audience and what handlers are most appropriate for their
application: if you add handlers âunder the hoodâ, you might well interfere
with their ability to carry out unit tests and deliver logs which suit their
requirements.

## Logging Levels

The numeric values of logging levels are given in the following table. These are
primarily of interest if you want to define your own levels, and need them to
have specific values relative to the predefined levels. If you define a level
with the same numeric value, it overwrites the predefined value; the predefined
name is lost.

| Level | Numeric value |
| --- | --- |
| `CRITICAL` | 50 |
| `ERROR` | 40 |
| `WARNING` | 30 |
| `INFO` | 20 |
| `DEBUG` | 10 |
| `NOTSET` | 0 |

Levels can also be associated with loggers, being set either by the developer or
through loading a saved logging configuration. When a logging method is called
on a logger, the logger compares its own level with the level associated with
the method call. If the loggerâs level is higher than the method callâs, no
logging message is actually generated. This is the basic mechanism controlling
the verbosity of logging output.

Logging messages are encoded as instances of the [`LogRecord`](../library/logging.html#logging.LogRecord "logging.LogRecord")
class. When a logger decides to actually log an event, a
[`LogRecord`](../library/logging.html#logging.LogRecord "logging.LogRecord") instance is created from the logging message.

Logging messages are subjected to a dispatch mechanism through the use of
*handlers*, which are instances of subclasses of the [`Handler`](../library/logging.html#logging.Handler "logging.Handler")
class. Handlers are responsible for ensuring that a logged message (in the form
of a [`LogRecord`](../library/logging.html#logging.LogRecord "logging.LogRecord")) ends up in a particular location (or set of locations)
which is useful for the target audience for that message (such as end users,
support desk staff, system administrators, developers). Handlers are passed
[`LogRecord`](../library/logging.html#logging.LogRecord "logging.LogRecord") instances intended for particular destinations. Each logger
can have zero, one or more handlers associated with it (via the
[`addHandler()`](../library/logging.html#logging.Logger.addHandler "logging.Logger.addHandler") method of [`Logger`](../library/logging.html#logging.Logger "logging.Logger")). In addition to any
handlers directly associated with a logger, *all handlers associated with all
ancestors of the logger* are called to dispatch the message (unless the
*propagate* flag for a logger is set to a false value, at which point the
passing to ancestor handlers stops).

Just as for loggers, handlers can have levels associated with them. A handlerâs
level acts as a filter in the same way as a loggerâs level does. If a handler
decides to actually dispatch an event, the [`emit()`](../library/logging.html#logging.Handler.emit "logging.Handler.emit") method is used
to send the message to its destination. Most user-defined subclasses of
[`Handler`](../library/logging.html#logging.Handler "logging.Handler") will need to override this [`emit()`](../library/logging.html#logging.Handler.emit "logging.Handler.emit").

### Custom Levels

Defining your own levels is possible, but should not be necessary, as the
existing levels have been chosen on the basis of practical experience.
However, if you are convinced that you need custom levels, great care should
be exercised when doing this, and it is possibly *a very bad idea to define
custom levels if you are developing a library*. Thatâs because if multiple
library authors all define their own custom levels, there is a chance that
the logging output from such multiple libraries used together will be
difficult for the using developer to control and/or interpret, because a
given numeric value might mean different things for different libraries.