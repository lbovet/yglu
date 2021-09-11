from yglu.main import ErrorList

from .utils import process, process_all


def test_empty_expression():
    input = "key1: !?"
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert "unexpected end of statement" in message
        assert "line 1, column 9" in message


def test_parse_error():
    input = "key1: !? 12."
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert "unexpected end of statement" in message
        assert "line 1, column 10" in message


def test_lexical_error():
    input = "key1: !? $_^.bla\n"
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert "illegal character" in message
        assert "line 1, column 12" in message


def test_key_error():
    input = "key1: !? $_.b\n"
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert "key not found" in message
        assert "line 1, column 10" in message


def test_key_error_invisible():
    input = "key1: !- $_.b\n"
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert "key not found" in message
        assert "line 1, column 10" in message


def test_key_error_shortcut():
    input = "key1: !? .b\n"
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert "key not found" in message
        assert "line 1, column 10" in message


def test_parse_error_trailing():
    input = "key1: !? $_.b c\n"
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert "Parse error" in message
        assert "line 1, column 15" in message


def test_parser_error_trailing_shortcut():
    input = "key1: !? .b c\n"
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert "Parse error" in message
        assert "line 1, column 13" in message


def test_key_error_space():
    input = "key1: !?   .b\n"
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert "key not found" in message
        assert "line 1, column 12" in message


def test_circular_reference():
    input = """
        a: !? .b
        b: !? .c
        c: !? .a
        """
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert "circular" in message
        assert "line 1, column 7" in message


def test_import_error():
    input = 'a: !? $import("filenotfound")'
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert "No such file" in message
        assert "line 1, column 7" in message


def test_null_key():
    input = "!? null: 1"
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert "mapping key is null" in message
        assert "line 1, column 4" in message


def test_empty_for_loop():
    input = """
        ? !for '[1,2,3]'
        :
        """
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert "object is not callable" in message
        assert "line 1, column 1" in message


def test_non_scalar_expression():
    input = """
        a: !?
            asd: 2
        """
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert "expected a scalar node" in message
        assert "line 1, column 4" in message


def test_if_key_error():
    input = """
        !if .a:
            a: 1
        """
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert len(message.split("\n")) == 3
        assert "key not found" in message
        assert "line 1, column 5" in message


def test_for_key_error():
    input = """
        !for .a: !()
            a: 1
        """
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        assert len(message.split("\n")) == 3
        assert "key not found" in message
        assert "line 1, column 6" in message


def test_single_errors():
    input = """
        a: !? .b
        """
    errors = ErrorList()
    next(process_all(input, None, errors))
    assert len(errors) == 1
    assert "key not found" in str(errors[0])


def test_muliple_errors():
    input = """
        a: !? .b
        b: !? .c
        """
    errors = ErrorList()
    next(process_all(input, None, errors))
    assert len(errors) == 2
    assert "key not found" in str(errors[0])
    assert "error in referenced node" in str(errors[1])


def test_no_line_format():
    input = "key1: !?"
    try:
        process(input)
        assert False
    except Exception as e:
        message = str(e)
        lines = message.splitlines()
        assert len(lines) == 3
        assert "unexpected end of statement" in lines[0]
        assert "line 1, column 9" in lines[1]


def test_line_format():
    input = "key1: !?"
    try:
        process(input, "/dummy/file/path.yml")
        assert False
    except Exception as e:
        message = str(e)
        lines = message.splitlines()
        assert len(lines) == 3
        assert "/dummy/file/path.yml:1:9:" in lines[0]
        assert "unexpected end of statement" in lines[1]


def test_error_in_multiline_expression():
    input = """
        key1: !? 111111111111111111111111
            + 2 ssss
                x bla
            """
    try:
        process(input)
        assert False
    except Exception as e:
        assert e.start_mark().line == 0
        assert e.start_mark().column == 6
        assert e.end_mark().line == 2
        assert e.end_mark().column == 13
