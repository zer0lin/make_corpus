import sys
import ast
import astunparse
from util import inplace_escape_spaces_in_strings, get_pretty_docstring, escape_control_string, reduce_ident


def give_hint():
    """输入格式"""
    print('Format:', file=sys.stderr)
    print('out-declarations-file out-descriptions-file out-bodies-file', file=sys.stderr)
    print('in-files-list', file=sys.stderr)
    sys.exit(-1)


def process_function(node, out_func_decl_fd, out_description_fd, out_bodies_fd):
    """提取函数节点中的函数定义，函数描述（docstring），函数体

    :param node: 函数节点
    :param out_func_decl_fd: 输出函数定义的流
    :param out_description_fd: 输出函数描述的流
    :param out_bodies_fd: 输出函数体的流
    :return:
    """
    doc_str = ast.get_docstring(node)
    if doc_str is None:
        return
    # 处理字符串中的转义字符
    inplace_escape_spaces_in_strings(node)
    # 将ast还原为str
    # 做split后前2个元素是''，所以索引从0 1 2的2开始
    unparsed_list = astunparse.unparse(node).split('\n')
    # 获得decorator的数目
    n_funcdef_decorator = len(node.decorator_list)
    unparsed_funcdef = unparsed_list[2: 3 + n_funcdef_decorator]
    unparsed_body = unparsed_list[1 + 3 + n_funcdef_decorator:]
    pretty_docstring = get_pretty_docstring(doc_str)
    funcdef = " DCNL ".join([escape_control_string(line) for line in unparsed_funcdef])
    processed_body = []
    if len(unparsed_body) > 10:
        return
    for line in unparsed_body:
        if line == "":
            continue
        line = escape_control_string(line)
        line = reduce_ident(line, ident_separator=" DCSP ")
        processed_body.append(line)
    processed_body_str = " DCNL".join(processed_body)
    if (pretty_docstring == "") or (processed_body_str == "") or (funcdef == ""):
        return
    print(pretty_docstring, file=out_description_fd)
    print(processed_body_str, file=out_bodies_fd)
    print(funcdef, file=out_func_decl_fd)


def process_module(in_fd, out_func_decl_fd, out_description_fd, out_bodies_fd):
    """提取输入模块中的函数定义，函数描述（docstring），函数体

    :param in_fd: 输入文件的流
    :param out_func_decl_fd: 输出函数定义的流
    :param out_description_fd: 输出函数描述的流
    :param out_bodies_fd: 输出函数体的流
    :return:
    """
    try:
        module_str = in_fd.read()
    except UnicodeDecodeError:
        return
    try:
        module_ast = ast.parse(module_str)
    except SyntaxError:
        # Python3不兼容Python2的语法，若输入文件中包含Python2的语法，则会出现语法错误。直接结束。
        return
    for node in module_ast.body:
        if isinstance(node, ast.FunctionDef):
            process_function(node, out_func_decl_fd, out_description_fd, out_bodies_fd)


def workflow():
    if len(sys.argv) < 4:
        give_hint()
    func_decl_filename = sys.argv[1]
    description_filename = sys.argv[2]
    bodies_filename = sys.argv[3]
    # 注释上讲open返回的是一个stream，即创建了几个文件流
    func_decl_fd = open(func_decl_filename, "w", encoding="UTF-8")
    description_fd = open(description_filename, "w", encoding="UTF-8")
    bodies_fd = open(bodies_filename, "w", encoding="UTF-8")
    for line in sys.stdin:
        input_filename = line.strip()
        try:
            process_module(open(input_filename, encoding="UTF-8"), func_decl_fd, description_fd, bodies_fd)
        except OSError:
            continue
    print('Done.')


if __name__ == '__main__':
    workflow()
