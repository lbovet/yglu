
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
var setErrors = (errors) =>
    problems = errors.map(err => ({
        from: CodeMirror.Pos(err.start.line, err.start.column),
        to: CodeMirror.Pos(err.end.line, err.end.column),
        message: err.message,
        severity: "error"
    }))
    if(report_errors) {
      report_errors(problems);
    }

var input = CodeMirror(document.getElementById('input'), {
    mode: 'yglu',
    lint: true,
    gutters: ["CodeMirror-lint-markers"],
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
          $('#error').text(res.errors[0].message);
          setErrors(res.errors);
      }
  })
}

var timer = 0
var debounce = fn => {
    clearTimeout(timer)
    timer = setTimeout(fn, 250)
}

$('.sample button').click(function() {
  doc = $(this).parent().children('.sample-document').text()
  input.doc.setValue(doc);
})

input.doc.setValue($('.sample-document').first().text());

input.on("changes", () => debounce(process));
process();