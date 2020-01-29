
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

var report_errors;
CodeMirror.registerHelper("lint", "yaml", function (text, options) {
    return new Promise((resolve, reject) => {
        report_errors = resolve;
        setTimeout(() => resolve(problems), 500);
    })
});

var problems = []
var setErrors = (errors) => {
    problems = errors.map(err => ({
        from: CodeMirror.Pos(err.start.line, err.start.column),
        to: CodeMirror.Pos(err.end.line, err.end.column +
            (err.start.line == err.end.line &&
            err.start.column == err.end.column ? 1 : 0)),
        message: err.message,
        severity: "error"
    }))
    if (report_errors) {
        report_errors(problems);
    }
}

var input = CodeMirror(document.getElementById('input'), {
    mode: 'yglu',
    lint: true,
    gutters: ["CodeMirror-lint-markers"],
    theme: 'eclipse',
    lineNumbers: true,
    tabSize: 2,
    indentWithTabs: false
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
    gutters: ["CodeMirror-lint-markers"],
    lineNumbers: true,
    readOnly: true,
    cursorBlinkRate: -1
});

var process = () => {
    $('#output > .CodeMirror').addClass('disabled');
    $.post({
        url: 'https://lbovet.pythonanywhere.com/yglu/process',
        data: JSON.stringify({ doc: input.getDoc().getValue() }),
        contentType: 'application/json',
        dataType: 'json'
    }).then(res => {
        if (res.doc) {
            $('#output > .CodeMirror').removeClass('disabled')
            output.getDoc().setValue(res.doc);
            $('#error').text('');
            setErrors([])
        } else {
            if (res.errors && res.errors.length > 0)
                $('#error').text(res.errors[0].message);
            setErrors(res.errors || []);
        }
    })
}

var timer = 0
var debounce = fn => {
    clearTimeout(timer)
    timer = setTimeout(fn, 250)
}

input.on("changes", () => debounce(process));

$.get('samples.yaml').then(res => {
    res.split('---')
        .filter(doc => doc.trim())
        .map(doc => doc.split("\n"))
        .map(doc => $("#sample")
            .append($('<button>')
                .addClass("btn btn-outline-primary")
                .text((doc[0].trim() ? doc[0] : doc[1]).split(":")[1].trim())
                .click(() => input.doc.setValue(doc.slice(3).join("\n")))))
}).then(() => {
    $("#sample button").first().click();
    setTimeout(process,0);
});