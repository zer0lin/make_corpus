import sys
import numpy as np
from collections import defaultdict


def give_hint():
    print("Usage:", file=sys.stderr)
    print(sys.argv[0],
          "data-file metadata-file valid-size test-size out-repos-basename out-data-basename out-metadata-basename",
          file=sys.stderr)
    sys.exit(-1)


def pick_repos(repos, repos_count_dict, repos_mean_size, target_size):
    rv = []
    cur_size = 0
    while cur_size < target_size - 0.5 * repos_mean_size:
        repo = repos.pop()
        cur_size += repos_count_dict[repo]
        rv.append(repo)
    return rv


def write_repos(data, metadata, all_repos, repos, out_repos_fs, out_data_fs, out_metadata_fs):
    for repo in repos:
        print(repo, file=out_repos_fs)

    repo_set = set(repos)
    for i in range(len(all_repos)):
        if all_repos[i] in repo_set:
            print(data[i].strip(), file=out_data_fs)
            print(metadata[i].strip(), file=out_metadata_fs)


def workflow():
    if len(sys.argv) != 8:
        give_hint()
    np.random.seed(42)

    data_fs = open(sys.argv[1], encoding="UTF-8")
    metadata_fs = open(sys.argv[2], encoding="UTF-8")
    valid_size = int(sys.argv[3])
    test_size = int(sys.argv[4])

    # sys.argv[5] = out-repos-basename
    out_train_repos_fs = open(sys.argv[5] + ".train", "w", encoding="UTF-8")
    out_valid_repos_fs = open(sys.argv[5] + ".valid", "w", encoding="UTF-8")
    out_test_repos_fs = open(sys.argv[5] + ".test", "w", encoding="UTF-8")

    # sys.argv[6] = out-data-basename
    out_train_data_fs = open(sys.argv[6] + ".train", "w", encoding="UTF-8")
    out_valid_data_fs = open(sys.argv[6] + ".valid", "w", encoding="UTF-8")
    out_test_data_fs = open(sys.argv[6] + ".test", "w", encoding="UTF-8")

    out_train_metadata_fs = open(sys.argv[7] + ".train", "w", encoding="UTF-8")
    out_valid_metadata_fs = open(sys.argv[7] + ".valid", "w", encoding="UTF-8")
    out_test_metadata_fs = open(sys.argv[7] + ".test", "w", encoding="UTF-8")

    data = data_fs.readlines()
    metadata = metadata_fs.readlines()
    if len(metadata) - valid_size - test_size < 0:
        print("Error: not enough data.", file=sys.stderr)
        sys.exit(-1)

    src_files = [x.split()[0] for x in metadata]
    repos = ["/".join(x.split("/")[:3]) for x in src_files]
    repos_count_dict = defaultdict(int)
    for x in repos:
        repos_count_dict[x] = repos_count_dict[x] + 1
    repos_mean_size = np.mean(repos_count_dict.values())

    shuffle_uniq_repos = repos_count_dict.keys()
    np.random.shuffle(shuffle_uniq_repos)
    shuffle_uniq_repos_list = list(shuffle_uniq_repos)

    valid_repos = pick_repos(shuffle_uniq_repos_list, repos_count_dict, repos_mean_size, valid_size)
    test_repos = pick_repos(shuffle_uniq_repos_list, repos_count_dict, repos_mean_size, test_size)
    train_repos = shuffle_uniq_repos_list

    write_repos(data, metadata, repos, train_repos, out_train_repos_fs, out_train_data_fs, out_train_metadata_fs)
    write_repos(data, metadata, repos, valid_repos, out_valid_repos_fs, out_valid_data_fs, out_valid_metadata_fs)
    write_repos(data, metadata, repos, test_repos, out_test_repos_fs, out_test_data_fs, out_test_metadata_fs)


if __name__ == "__main__":
    workflow()
