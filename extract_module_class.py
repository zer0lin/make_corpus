import sys
import ast
import astunparse
from util import get_pretty_docstring, escape_control_string


def give_hint():
    """输入格式"""
    print('Format:', file=sys.stderr)
    print('out-module-descriptions-file out-module-metadata-file '
          'out-class-declarations-file out-class-descriptions-file out-class-metadata-file', file=sys.stderr)
    print('in-files-list', file=sys.stderr)
    sys.exit(-1)


def process_class(node, out_class_decl_fd, out_class_desc_fd, out_class_meta_fd, input_filename,
                  parent_class_lineno=-1):
    doc_str = ast.get_docstring(node)
    # 将ast还原为str
    # 做split后前2个元素是''，所以索引从0 1 2的2开始
    unparsed_list = astunparse.unparse(node).split('\n')
    # 获得decorator的数目
    n_classdef_decorator = len(node.decorator_list)
    unparsed_classdef = unparsed_list[2: 3 + n_classdef_decorator]
    pretty_docstring = get_pretty_docstring(doc_str) if doc_str is not None else "DCNA"
    classdef = " DCNL ".join([escape_control_string(line) for line in unparsed_classdef])
    meta_str = input_filename + " " + str(node.lineno) + " " + str(parent_class_lineno)
    print(pretty_docstring, file=out_class_desc_fd)
    print(classdef, file=out_class_decl_fd)
    print(meta_str, file=out_class_meta_fd)
    for inner_node in node.body:
        if isinstance(inner_node, ast.ClassDef):
            process_class(inner_node, out_class_decl_fd, out_class_desc_fd, out_class_meta_fd, input_filename,
                          node.lineno)


def process_module(in_fd, out_module_desc_fd, out_module_meta_fd, out_class_decl_fd, out_class_desc_fd,
                   out_class_meta_fd, input_filename):

    module_str = in_fd.read()
    try:
        module_ast = ast.parse(module_str)
    except SyntaxError:
        # Python3不兼容Python2的语法，若输入文件中包含Python2的语法，则会出现语法错误。直接结束。
        return
    doc_str = ast.get_docstring(module_ast)
    if doc_str is not None:
        pretty_docstring = get_pretty_docstring(doc_str)
        print(pretty_docstring, file=out_module_desc_fd)
    else:
        print("DCNA", file=out_module_desc_fd)
    meta_str = input_filename
    print(meta_str, file=out_module_meta_fd)
    for node in module_ast.body:
        if isinstance(node, ast.ClassDef):
            process_class(node, out_class_decl_fd, out_class_desc_fd, out_class_meta_fd, input_filename)


def workflow():
    if len(sys.argv) < 6:
        give_hint()
    module_description_filename = sys.argv[1]
    module_meta_filename = sys.argv[2]
    class_decl_filename = sys.argv[3]
    class_description_filename = sys.argv[4]
    class_meta_filename = sys.argv[5]

    # 注释上讲open返回的是一个stream，即创建了几个文件流
    module_description_fd = open(module_description_filename, "w", encoding="UTF-8")
    module_meta_fd = open(module_meta_filename, "w", encoding="UTF-8")
    class_decl_fd = open(class_decl_filename, "w", encoding="UTF-8")
    class_description_fd = open(class_description_filename, "w", encoding="UTF-8")
    class_meta_fd = open(class_meta_filename, "w", encoding="UTF-8")
    for line in sys.stdin:
        input_filename = line.strip()
        process_module(open(input_filename, encoding="UTF-8"), module_description_fd, module_meta_fd, class_decl_fd,
                       class_description_fd, class_meta_fd, input_filename)

    print('Done.')


if __name__ == '__main__':
    workflow()
