from collections import defaultdict


def test():
    repos_count_dict = defaultdict(int)
    repos_count_dict["x"] = 5
    repos_count_dict["y"] = 3
    repos_count_dict["z"] = 2

    k = repos_count_dict.keys()
    print(k)
    list(k).pop()
    print(k)


if __name__ == "__main__":
    test()
