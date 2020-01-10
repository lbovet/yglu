import pprint
import sys
import ruamel.yaml
import yaql

def load_yaml(yaml):
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as file:
            return yaml.load(file)
    else:
        return yaml.load(sys.stdin.read())

class ExpressionNode:
    def __init__(self, loader, node):
        self.expression = loader.construct_scalar(node)
    def eval(self, engine, scope):
        return engine(self.expression).evaluate(data=scope)

def expression_constructor(loader, node):
    return ExpressionNode(loader, node)


yaml = ruamel.yaml.YAML()
yaml.add_constructor(u'!=', expression_constructor)
yaml.allow_duplicate_keys = True

def eval_doc(doc):
    engine = yaql.factory.YaqlFactory().create()
    root = doc
    def eval(data):
        if isinstance(data, dict):
            result = dict()
            for k,v in data.items():
                result[k] = eval(v)
        elif isinstance(data, list) or isinstance(data, tuple):
            result = list()
            for v in data:
                result.append(eval(v))
        elif isinstance(data, ExpressionNode):
            result = data.eval(engine, root)
        else:
            result = data
        return result
    return eval(doc)

def main():
    yaml.dump(load_yaml(yaml), sys.stdout)

if __name__ == '__main__':
    main()
