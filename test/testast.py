import ast
import astunparse


def do_print():
    pass


def test():
    in_fd = open("./auth.py")
    module_str = in_fd.read()
    # print(module_str)
    module_ast = ast.parse(module_str)
    for node in module_ast.body:
        if isinstance(node, ast.FunctionDef):
            print(astunparse.unparse(node).split('\n'))

    in_fd.close()


if __name__ == '__main__':
    test()
