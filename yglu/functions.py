''' Built-in functions  '''

import os
from .builder import build

def import_definition(context, root):
    if hasattr(root, 'doc') and  hasattr(root.doc, 'filepath') and root.doc.filepath:
        dir = os.path.dirname(root.doc.filepath)
    else:
        dir = os.getcwd()

    def import_function(filename):
        if os.path.isabs(filename):
            filepath = filename
        else:
            filepath = os.path.join(dir, filename)
        with open(filepath) as file:
            result = build(file, filename)[0]
            return result

    context['$import'] = import_function

definitions = [import_definition]
