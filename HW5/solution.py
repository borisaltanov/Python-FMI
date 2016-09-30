from collections import defaultdict
import re
import ast


class CodeError(ast.NodeVisitor):
    GATES = [ast.If, ast.For, ast.While, ast.Break,
             ast.Try, ast.ExceptHandler, ast.With, ast.withitem]

    def __init__(self, code):
        self.error_list = defaultdict(list)
        self.code = code
        self.ast_tree = ast.parse(code)

    def line_length(self, line_length=79):
        for i, line in enumerate(self.code.splitlines()):
            if len(line) > line_length:
                self.error_list[i + 1].append(
                    'line too long ({} > {})'.format(len(line), line_length))

    def trailing_whitespace(self, forbid_trailing_whitespace=True):
        if forbid_trailing_whitespace is False:
            return
        for i, line in enumerate(self.code.splitlines()):
            if re.search(r'[ \t]+$', line):
                self.error_list[i + 1].append('trailing whitespace')

    def forbid_semicolons(self, forbid=True):
        if not forbid:
            return
        for i, line in enumerate(self.code.splitlines()):
            line = re.sub(r'([\'\"]).*?\1', '', line)
            if ';' in line:
                self.error_list[i + 1].append(
                    'multiple expressions on the same line')

    def visit_FunctionDef(self, node):
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.generic_visit(node)

    def lines_in_function_help(self, node, length=0):
        parsed = ast.parse(node)
        length = len(node.body)
        for element in ast.iter_child_nodes(parsed):
            if type(element) in self.GATES:
                length += self.lines_in_function_help(element)

        return length

    def lines_in_function(self, code, max_lines=None):
        if max_lines is None:
            return
        for node in ast.walk(code):
            if isinstance(node, ast.FunctionDef):
                length = self.lines_in_function_help(node)
                if length > max_lines:
                    self.error_list[node.lineno].append(
                        'method with too many lines ({} > {})'.format(
                            length, max_lines))

    def methods_in_class(self, code, max_methods=None):
        if max_methods is None:
            return
        for node in ast.walk(code):
            if isinstance(node, ast.ClassDef):
                methods = 0
                for method in node.body:
                    if isinstance(method, ast.FunctionDef):
                        methods += 1
                if methods > max_methods:
                    self.error_list[node.lineno].append(
                        'too many methods in class({} > {})'.format(
                            methods, max_methods))

    def arguments_in_function(self, code, max_arity=None):
        if max_arity is None:
            return
        parsed = ast.parse(code)
        for node in ast.walk(parsed):
            if isinstance(node, (ast.FunctionDef)):
                args = len(node.args.args)
                if args > max_arity:
                    self.error_list[node.lineno].append(
                        'too many arguments({} > {})'.format(args, max_arity))

    def nesting_help(self, node, depths, depth=0):
        depth += 1
        for element in node.body:
            if hasattr(element, 'lineno'):
                depths[element.lineno] = depth
            if type(element) in self.GATES:
                self.nesting_help(element, depths, depth)

        return depths

    def nesting(self, code, max_nesting=None):
        if max_nesting is None:
            return
        for node in ast.walk(code):
            if isinstance(node, ast.FunctionDef):
                depths = {}
                self.nesting_help(node, depths)
                for key, value in depths.items():
                    if value > max_nesting:
                        self.error_list[key].append(
                            'nesting too deep ({} > {})'.format(
                                value, max_nesting))

    def indentation(self, node, depths, depth=0, indentation_size=4):
        if not hasattr(node, 'body'):
            return depth
        for element in node.body:
            if hasattr(element, 'lineno') and hasattr(element, 'col_offset'):
                if element.lineno in depths:
                    if element.col_offset < depths[element.lineno]:
                        depths[element.lineno] = element.col_offset
                if element.lineno not in depths:
                    depths[element.lineno] = element.col_offset
                if depth * indentation_size != element.col_offset and \
                        element.col_offset in depths.values():
                    self.error_list[element.lineno].append(
                        'indentation is {} instead of {}'.format(
                            element.col_offset, depth * indentation_size))
            if type(element) in self.GATES or \
                    isinstance(element, ast.FunctionDef) or \
                    isinstance(element, ast.ClassDef):
                self.indentation(element, depths, depth + 1)


def critic(code, **rules):
    code_err = CodeError(code)
    code_err.line_length(rules.get('line_length', 79))
    code_err.forbid_semicolons(rules.get('forbid_semicolons', True))
    code_err.nesting(code_err.ast_tree, rules.get('max_nesting', None))
    code_err.indentation(code_err.ast_tree, dict(), 0,
                         rules.get('indentation_size', 4))
    code_err.methods_in_class(
        code_err.ast_tree, rules.get('methods_per_class', None))
    code_err.arguments_in_function(
        code_err.ast_tree, rules.get('max_arity', None))
    code_err.trailing_whitespace(rules.get('forbid_trailing_whitespace', True))
    code_err.lines_in_function(
        code_err.ast_tree, rules.get('max_lines_per_function', None))

    error_list = code_err.error_list
    return error_list


cir = '''class A:
    def foo(self, a):
        with file('SDasd'):
            print(a)
            if a == 0:
                a = "mega dulgiq shiban string bete ujasno e dulug eehsssssssssssssss"
                return 0
        return a

    def bar(self, b):
        print(b)

    def unpleasant_one():
        for x in ["smiling", "girl"]:
            for y in ["cool", "long beard", "boy"]:
                if x == 'girl' and y == 'long beard':
                    print("А {} {}!".format(y, x))

def ffs(a):
    print(a)

class B:
    class N:
        def __init__(self):
            print("INIT")

        def n(s):
            if(s):
                return s
            print("damn")

        def h(f):
            pass

    def b():
        def nested():
            print("Nested")
            return 1
        for _ in range(10):
            print("SDADA")

    def g():
        pass

def ffs(a):
    print(a)
'''

pir = '''def neuf_tam(s, t, f, u):
   def nemanachin():
       a_ne = 2
   ugly_ident = 3
   return ugly_ident
'''

print(critic(cir, methods_per_class = 2))
