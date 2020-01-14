[![Build Status](https://travis-ci.org/lbovet/yglu.svg?branch=master)](https://travis-ci.org/lbovet/yglu)
[![PyPI version](https://badge.fury.io/py/yglu.svg)](https://badge.fury.io/py/yglu)
# Yglu ᕄ

Yglu is [YAML](https://yaml.org/) enriched with an advanced expression language. Unlike usual text templating, Yglu relies on the YAML structure and leverages its typing features combined with the [YAQL](https://yaql.readthedocs.io/en/latest/) query language. 

This association enables templating and functional processing a bit like if YAML nodes where spreadsheet cells.

Yglu input documents are pure YAML using tags for computed nodes.

<table><tr>
<td width="440">
input
<pre lang="yaml">
a: 1
b: !? .a + 1  </pre>
</td>
<td width="440">
output
<pre lang="yaml">
a: 1
b: 2  </pre>
</td>
</tr></table>

See the [test samples](https://github.com/lbovet/yglu/tree/master/tests/samples) for more examples.

## Install

```
pip install yglu
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
| `!?`      | Evaluate an expression. The result can be a scalar, mapping or sequence. |
| `!-`      | Hide the node in the output but keep it accessible from expressions. When used with a scalar, it evaluates it as an expression. |
| `!()`     | Make the node reusable in expressions as a function. It is also hidden. |

## Expressions

Expressions are written in [YAQL](https://yaql.readthedocs.io/en/latest/).

They are evaluated in a context with the following predefined variables:

| **Variable**| **Description** |
|-----------|-----------------|
| `$_`      | Refers to the current document root. Can be ommitted at the beginning of the expression if it starts with a dot. |
| `$`       | Implicit arguments of functions. |
| `$env`    | Gives access to environment variables if $YGLU_ENABLE_ENV environment variable is set. |

## Built-in Functions

In addition to [standard YAQL operators](https://yaql.readthedocs.io/en/latest/standard_library.html#), Yglu defines the following functions:

| **Function**| **Description** |
|-----------|-----------------|
| `$import(filename)`  | Imports another document in the current node. |

## Planned Features

- Use expressions in mapping keys.
- Tag for merging mappings easily.
