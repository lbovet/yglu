[![Build Status](https://travis-ci.org/lbovet/yglu.svg?branch=master)](https://travis-ci.org/lbovet/yglu)
[![PyPI version](https://badge.fury.io/py/yglu.svg)](https://badge.fury.io/py/yglu)
# Yglu ᕄ

Yglu [YAML](https://yaml.org/) enriched with an advanced expression language. Unlike usual text templating, Yglu relies on the YAML structure and leverage its typing features combined with the [YAQL](https://yaql.readthedocs.io/en/latest/) query language. 

This association enables templating and functional processing a bit like if YAML nodes where spreadsheet cells.

Yglu input documents are pure YAML using tags for computed nodes.

<table><tr>
<td width="440">
input
<pre lang="yaml">
a: 1
b: ?! $.a + 1  </pre>
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

Tags specify an alteration of the structure of the document.

| **Tag**&nbsp;&nbsp;&nbsp;| **Description** |
|-----------|-----------------|
| `!?`     | Replace the node value with the result of an expression |
| `!-`      | Hide the node in the output but keep it accessible from expressions. If the node value is a string, it is replaced with the result of the expression. |
| `!()`  | Make the node reusable in expressions as a function. It is also hidden. *Will be available in version 1.1* |

## Expressions

Expressions are written in [YAQL](https://yaql.readthedocs.io/en/latest/).

They receive a context with predefined variables.

| **Variable**| **Description** |
|-----------|-----------------|
| `$`     | Refers to the document root, or implicit argument in function blocks. |
| `$_`      | Always refers to the document root. So that the root is accessible from functions. *Will be available in version 1.1* |

