import sys
import json


def give_hint():
    """输入格式"""
    print("Format:", file=sys.stderr)
    print("out-declarations-file out-descriptions-file out-bodies-file out-metadata-file", file=sys.stderr)
    print("out-all-file", file=sys.stderr)
    sys.exit(-1)


def process(func_decl_fd, description_fd, bodies_fd, meta_fd, out_all_fd):
    decl_list = func_decl_fd.read().split("\n")
    desc_list = description_fd.read().split("\n")
    bodies_list = bodies_fd.read().split("\n")
    meta_list = meta_fd.read().split("\n")
    list_len = len(decl_list) - 1
    print("[", file=out_all_fd)
    for i in range(0, list_len):
        temp_dict = {"decl": decl_list[i], "desc": desc_list[i], "body": bodies_list[i], "meta": meta_list[i]}
        temp_s = json.dumps(temp_dict, ensure_ascii=False)
        print(temp_s + ",", file=out_all_fd)
    print("]", file=out_all_fd)


def workflow():
    if len(sys.argv) < 6:
        give_hint()
    func_decl_filename = sys.argv[1]
    description_filename = sys.argv[2]
    bodies_filename = sys.argv[3]
    meta_filename = sys.argv[4]
    out_all_filename = sys.argv[5]
    func_decl_fd = open(func_decl_filename, "r", encoding="UTF-8")
    description_fd = open(description_filename, "r", encoding="UTF-8")
    bodies_fd = open(bodies_filename, "r", encoding="UTF-8")
    meta_fd = open(meta_filename, "r", encoding="UTF-8")
    out_all_fd = open(out_all_filename, "w", encoding="UTF-8")
    process(func_decl_fd, description_fd, bodies_fd, meta_fd, out_all_fd)


if __name__ == "__main__":
    workflow()
