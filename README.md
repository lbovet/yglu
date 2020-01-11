[![Build Status](https://travis-ci.org/lbovet/yglu.svg?branch=master)](https://travis-ci.org/lbovet/yglu)
[![PyPI version](https://badge.fury.io/py/yglu.svg)](https://badge.fury.io/py/yglu)
# Yglu ᕄ

YAML enriched with an advanced expression language. Unlike usual text templating, Yglu relies on the YAML structure and leverage its typing features combined with the [YAQL](https://yaql.readthedocs.io/en/latest/) query language. 

This association enables templating and functional processing a bit like if YAML nodes where Excel cells.

Yglu input documents are pure YAML with tags for computed nodes.

<table><tr>
<td>
  input.yml
  <pre>
  a: 1
  b: $.a + 1
  </pre>
</td><td>
  output.yml
  <pre>
  a: 1
  b: 2
  </pre>
</td>
</tr></table>

See the [test samples](../tree/master/tests/samples) for more examples.

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
