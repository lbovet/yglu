""" Built-in functions  """

import os

from .builder import build
from .expression import Holder

base_dir = None


def import_definition(context, root):
    if hasattr(root, "doc") and hasattr(root.doc, "filepath") and root.doc.filepath:
        current_dir = os.path.dirname(root.doc.filepath)
    else:
        current_dir = os.getcwd()
    global base_dir
    if base_dir is None:
        base_dir = current_dir

    def import_function(filename):
        if os.path.isabs(filename):
            filepath = filename
        else:
            filepath = os.path.join(current_dir, filename)

        import_dirs = [base_dir]
        import_path = os.environ.get("YGLU_IMPORT_ALLOW")
        if import_path is not None:
            import_dirs.extend(import_path.split(os.pathsep))

        allow = False
        for dir in import_dirs:
            relative_path = os.path.relpath(filepath, start=dir)
            if not relative_path.startswith(os.pardir):
                allow = True
                break
        if not allow:
            raise Exception(
                """
                Import not allowed. Set $YGLU_IMPORT_ALLOW to allow
                import from other directories
                """
            )

        with open(filepath) as file:
            if hasattr(root, "doc"):
                errors = root.doc.errors
            else:
                errors = None
            result = build(file, filepath, errors)
            return Holder(result)

    context["$import"] = import_function


definitions = [import_definition]
