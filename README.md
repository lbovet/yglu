---
title: yglu ReadMe
---

# Yglu ᕄ !?

[![Build Status](https://travis-ci.org/lbovet/yglu.svg?branch=master)](https://travis-ci.org/lbovet/yglu)
[![PyPI version](https://badge.fury.io/py/yglu.svg)](https://badge.fury.io/py/yglu)

<p align="center"><b><a href="https://yglu.io/">* Try Yglu Online *</a></b></p>


Yglu is [YAML](https://yaml.org/) augmented with an advanced expression language. Unlike usual text templating, Yglu relies on the YAML structure and leverages its tag system combined with the [YAQL](https://yaql.readthedocs.io/en/latest/) query language.

This association enables templating and functional processing a bit like if YAML nodes were spreadsheet cells.

Yglu input documents are pure and valid YAML using [tags](https://yaml.org/spec/1.2/spec.html#id2784064) for computed nodes.

<table><tr>
<td width="440">
input
<pre lang="yaml">
a: 1
b: !? .a + 1
!if .b = 2:
  c: 3  </pre>
</td>
<td width="440">
output
<pre lang="yaml">
a: 1
b: 2
c: 3
 </pre>
</td>
</tr></table>

<table><tr>
<td width="440">
input
<pre lang="yaml">
names: !-
  - 'nginx:1.16'
  - 'node:13.6'
  - 'couchbase:9.3'
image: !()
  !? $.split(':')[0]:
    version: !? $.split(':')[1]
images: !?
  $_.names
    .select(($_.image)($))
    .aggregate($1.mergeWith($2), {})</pre>
</td>
<td width="440">
output
<pre lang="yaml">
images:
  nginx:
    version: '1.16'
  node:
    version: '13.6'
  couchbase:
    version: '9.3'
    &nbsp;
    &nbsp;
    &nbsp;
    &nbsp;  </pre>
</td>
</tr></table>

In the example above, the `names` sequence is hidden, `image` is a function (like a template block) and `images` is an expression which iterates through all names, applies the image function to each one and aggregates the individual results by merging them together as a mapping.

As such an operation is often needed, Yglu provides a `!for` tag for merging a sequence iterated over a function:

<table><tr>
<td width="440">
input
<pre lang="yaml">
names: !-
  - 'nginx:1.16'
  - 'node:13.6'
  - 'couchbase:9.3'
images:
  !for .names: !()
    !? $.split(':')[0]:
      version: !? $.split(':')[1]</pre>
</td>
<td width="440">
output
<pre lang="yaml">
images:
  nginx:
    version: '1.16'
  node:
    version: '13.6'
  couchbase:
    version: '9.3'
    &nbsp;</pre>
</td>
</tr></table>

See the test [samples](https://github.com/lbovet/yglu/tree/master/tests/samples) for more examples.

<p align="center"><b><a href="https://yglu.io/">* Try Yglu Online *</a></b></p>

## Install

```
pip3 install yglu
```

## Run

```
Usage: yglu [options] [<filename>]

Options:
  -v - -version          Print version and exit.
  -h - -help             Print help and exit.
```

## Tags

Tags specify an alteration of the document structure.

| **Tag**&nbsp;&nbsp;&nbsp;| **Description** |
|-----------|-----------------|
| `!?`      | Evaluate an expression. The result can be a scalar, mapping or sequence. Can also be used in mapping keys. |
| `!-`      | Hide the node in the output but keep it accessible from expressions. Can be an expression. |
| `!()`     | Make the node reusable in expressions as a function. |
| `!if`     | Conditional merge. See [if.yml](https://github.com/lbovet/yglu/tree/master/tests/samples/if.yml). |
| `!for`    | Merge the results of a function applied to all items of a sequence . See [for.yml](https://github.com/lbovet/yglu/tree/master/tests/samples/for.yml). |
| `!apply`  | Apply a function or function block to a block. See [function.yml](https://github.com/lbovet/yglu/tree/master/tests/samples/function.yml). |


## Expressions

Expressions are written in [YAQL](https://yaql.readthedocs.io/en/latest/).

They are evaluated in a context with the following variables defined:

| **Variable**| **Description** |
|-------------|-----------------|
| `$_`        | Refers to the current document root. Can be omitted at the beginning of the expression if it starts with a dot. |
| `$`         | Implicit argument of functions. |
| `$env`      | Gives access to environment variables. Disabled by default. Set the `$YGLU_ENABLE_ENV` environment variable to enable this feature. |
| `$this`     | Refers to the current function block node in order to access its children nodes. See [function.yml](https://github.com/lbovet/yglu/tree/master/tests/samples/function.yml) |

## Built-in Functions

In addition to the [standard YAQL library](https://yaql.readthedocs.io/en/latest/standard_library.html#), Yglu defines the following functions:

| **Function**         | **Description** |
|----------------------|-----------------|
| `$import(filename)`  | Imports another document in the current node. By default, it is only permitted to import files from within the directory hierarchy of the input file. Set `$YGLU_IMPORT_ALLOW` to a list of permitted directories. |
