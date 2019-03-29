import ast


def inplace_escape_spaces_in_strings(node):
    """处理转义字符"""
    if isinstance(node, ast.Str):
        node.s = node.s                         \
            .replace("DCQS", "DCQSDCQS")        \
            .replace(" DCSP ", " DCQSDCSP ")    \
            .replace(" DCTB ", " DCQSDCTB ")    \
            .replace(" ", " DCSP ")             \
            .replace("\t", " DCTB ")
    else:
        for child in ast.iter_child_nodes(node):
            inplace_escape_spaces_in_strings(child)


def get_pretty_docstring(doc_str):
    """整理docstring"""
    doc_str = doc_str.replace("DCQT", "DCQTDCQT").replace("DCNL", "DCQTDCNL")
    doc_str = doc_str.replace("'", "\\'")
    rv_list = []
    for line in doc_str.split('\n'):
        line = line.strip()
        # 如果这一行为空或者都是空字符
        if line == "" or (not any([c.isalnum() for c in line])):
            continue
        rv_list.append(line)
    unevaluated_pretty_docstring = "'" + " DCNL ".join(rv_list) + "'"
    return unevaluated_pretty_docstring


def escape_control_string(line):
    """转义控制字符"""
    return line.replace("DCQT", "DCQTDCQT").replace("DCNL", "DCQTDCNL")


def reduce_ident(line, ident_separator=" "):
    """压缩分隔符，就是缩进区分代码段的那个"""
    line = line.rstrip()
    line_all_stripped = line.lstrip()
    # 计算左边多少个空格，默认缩进分隔符4个空格
    n_space = len(line) - len(line_all_stripped)
    n_ident = n_space // 4
    return (ident_separator * n_ident) + line_all_stripped
