from github3 import login
from getpass import getpass
import pickle
import os
from py_repo import PyRepo
import time
import getopt
import sys
import threading


def login_github(username):
    password = getpass("GitHub password for {0}".format(username))
    g = login(username, password)
    return g


def do_clone(output_directory):
    global repo_list_dict
    to_use_key = None
    while True:
        num = 0
        lock.acquire()
        for key, value in repo_list_dict.items():
            # false代表这个东西没有被下载
            if not value:
                to_use_key = key
                break
            else:
                num += 1
        if len(repo_list_dict) == num:
            lock.release()
            return
        else:
            repo_list_dict[to_use_key] = True
            lock.release()
            print("Cloned {0}".format(to_use_key.details()))
            try:
                to_use_key.clone(output_directory)
            except Exception as e:
                lock.acquire()
                print("Failed to clone {0} due to {1}".format(to_use_key, e))
                repo_list_dict[to_use_key] = False
                to_use_key.reject()
                lock.release()


def start_multi_thread(thread_num, output_directory):
    thread_list = []
    for i in range(thread_num):
        t = threading.Thread(target=do_clone, args=(output_directory, ))
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()


def new(repos, username, search_query, min_stars, language, limit, output_directory, db_file, thread_num):
    global repo_list_dict
    g = login_github(username)
    query = search_query + (" " if len(search_query) > 0 else "") + "stars:>" + str(min_stars) + " language:" + language
    search_result = g.search_repositories(query, number=limit, sort="forks")
    for result in search_result:
        name = result.repository.name
        full_name = result.repository.full_name
        description = result.repository.description
        clone_url = result.repository.clone_url
        num_stars = result.repository.watchers
        num_forks = result.repository.forks_count
        created_at = result.repository.created_at
        pushed_at = result.repository.pushed_at

        repo = PyRepo(name, full_name, description, clone_url, time.time(), num_stars, num_forks, created_at, pushed_at)
        repo_list_dict[repo] = False
        if repo in repos:
            print("Skipping {0}, it has been cloned.".format(repo))
        else:
            repos.append(repo)
            outfile = open(db_file, "wb")
            pickle.dump(repos, outfile)
            outfile.close()

    start_multi_thread(thread_num, output_directory)


def create_repos(db_file):
    repos = []
    if os.path.exists(db_file):
        infile = open(db_file, "rb")
        repos = pickle.load(infile)
        infile.close()
    return repos


def recreate(repos, output_directory, thread_num):
    for repo in repos:
        repo_list_dict[repo] = False
    start_multi_thread(thread_num, output_directory)


def give_download_hint():
    print("Usage:\n\tscraper.py [parameters]\n")

    print("Required Parameters:")
    print("\t-m --mode\t\t\t'new' to generate 'new' corpus or 'recreate' to clone corpus from db_file")
    print("\t-o --out_dir\t\t\tDirectory into which repos are cloned")
    print("\t-d --db_file\t\t\tList of repos to clone in 'recreate' mode or save in 'new' mode")
    print("\t-u --user\t\t\tGitHub username")

    print()
    print("Optional Parameters:\n")
    print("\t-h --help\t\t\tShow this help")
    print("\t-n --limit\t\t\tNumber of repos to obtain in 'new' mode. DEFAULT 1000")
    print("\t-r --thread_num\t\t\tNumber of thread number . DEFAULT 5")
    print("\t-s --search\t\t\tSearch query used in 'new' mode. DEFAULT '<blank>'")
    print("\t-t --stars\t\t\tMinimum number of stars threshold. Used in 'new' mode to search. DEFAULT 100")
    print("\t-l --language\t\t\tRepo language, used in 'new' mode to search. DEFAULT 'python'")


def main(argv):
    mode = ""
    output_directory = ""
    db_file = ""
    username = ""
    limit = 1000
    search_query = ""
    min_stars = 100
    language = "python"
    thread_num = 5

    try:
        opts, args = getopt.getopt(argv, "hlrstnm:o:d:u:",
                                   ["mode=", "out_dir=", "db_file=", "thread_num=", "user=", "limit=", "search=",
                                    "stars=", "language=", "help"])
    except getopt.GetoptError:
        give_download_hint()
        raise

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            give_download_hint()
            sys.exit()
        elif opt in ("-m", "--mode"):
            mode = arg
        elif opt in ("-o", "--out_dir"):
            output_directory = arg
        elif opt in ("-d", "--db_file"):
            db_file = arg
        elif opt in ("-u", "--user"):
            username = arg
        elif opt in ("-n", "--limit"):
            limit = int(arg)
        elif opt in ("-s", "--search"):
            search_query = arg
        elif opt in ("-t", "--stars"):
            min_stars = int(arg)
        elif opt in ("-l", "--language"):
            language = arg
        elif opt in ("-r", "--thread_num"):
            thread_num = int(arg)
    if mode == "" or output_directory == "" or db_file == "" or username == "":
        give_download_hint()
        sys.exit(2)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    os.chdir(output_directory)
    repos = create_repos(db_file)

    if mode == "new":
        new(repos, username, search_query, min_stars, language, limit, output_directory, db_file, thread_num)
    elif mode == "recreate":
        recreate(repos, output_directory, thread_num)
    else:
        print("Mode parameter must be 'new' or 'recreate'")

    print("Done.")


if __name__ == "__main__":
    lock = threading.Lock()
    repo_list_dict = {}
    main(sys.argv[1:])

