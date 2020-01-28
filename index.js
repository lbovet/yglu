
CodeMirror.defineMode("yglu", function (config, parserConfig) {
    var ygluOverlay = {
        token: function (stream, state) {
            var ch;
            if (stream.match("!?") || stream.match("!-") || stream.match("!()") || stream.match("!if") || stream.match("!for")) {
                while ((ch = stream.next()) != null && ch != " ") { }
                return "keyword";
            }
            while (stream.next() != null && !stream.match("!", false)) { }
            return null;
        }
    };
    return CodeMirror.overlayMode(CodeMirror.getMode(config, parserConfig.backdrop || "yaml"), ygluOverlay);
});

var input = CodeMirror(document.getElementById('input'), {
    mode: 'yglu',
    theme: 'eclipse',
    lineNumbers: true,
    tabSize: 2,
    indentWithTabs: false,
    value: "a:\n  b: !? 1 + 2\n  c:\n  - !? hello + ' ' + str($_.a.b)",
})

input.setOption("extraKeys", {
    Tab: function (cm) {
        var spaces = Array(cm.getOption("indentUnit") + 1).join(" ");
        cm.replaceSelection(spaces);
    }
});

var output = CodeMirror(document.getElementById('output'), {
    mode: 'text/x-yaml',
    theme: 'eclipse',
    lineNumbers: true,
    readOnly: 'nocursor'
});

var process = () => $.post({
    url: 'https://lbovet.pythonanywhere.com/yglu/process',
    data: JSON.stringify({ doc: input.getDoc().getValue() }),
    contentType: 'application/json',
    dataType: 'json'
}).then(res => {
    if (res.doc) {
        $('#output > .CodeMirror').removeClass('disabled')
        output.getDoc().setValue(res.doc);
        $('#error').text('');
    } else {
        $('#output > .CodeMirror').addClass('disabled')
        $('#error').text(res.errors[0].message);
    }
})

var timer = 0
var debounce = fn => {
    clearTimeout(timer)
    timer = setTimeout(fn, 250)
}

input.on("changes", () => debounce(process));
process();