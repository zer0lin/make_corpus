from github3 import login
from getpass import getpass
import pickle
import os
from py_repo import PyRepo
import time
import getopt
import sys


def login_github(username):
    password = getpass("GitHub password for {0}".format(username))
    g = login(username, password)
    return g


def new(repos, username, search_query, min_stars, language, limit, output_directory, db_file):
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
        if repo in repos:
            print("Skipping {0}, it has been cloned.".format(repo))
        else:
            try:
                repo.clone(output_directory)
                repos.append(repo)
                print("Cloned {0}".format(repo.details()))
                outfile = open(db_file, "wb")
                pickle.dump(repos, outfile)
                outfile.close()
            except Exception as e:
                print("Failed to clone {0} due to {1}".format(repo, e))


def create_repos(db_file):
    repos = []
    if os.path.exists(db_file):
        infile = open(db_file, "rb")
        repos = pickle.load(infile)
        infile.close()
    return repos


def recreate(repos, output_directory):
    for repo in repos:
        repo.checkout(output_directory)
        print("Checked out: {0}".format(repo.details()))


def give_download_hint():
    print("Usage:\n\tscraper.py [parameters]\n")

    print("Required Parameters:")
    print("\t-m --mode\t\t\t'new' to generate new corpus or 'recreate' to clone corpus from db_file")
    print("\t-o --out_dir\t\t\tDirectory into which repos are cloned")
    print("\t-d --db_file\t\t\tList of repos to clone in 'recreate' mode or save in 'new' mode")
    print("\t-u --username\t\tGitHub username")

    print()
    print("Optional Parameters:\n")
    print("\t-h --help\t\t\tShow this help")
    print("\t-n --limit\t\t\tNumber of repos to obtain in 'new' mode. DEFAULT 1000")
    print("\t-s --search\t\t\tSearch query used in 'new' mode. DEFAULT '<blank>'")
    print("\t-t --stars\t\t\tMinimum number of stars threshold. Used in 'new' mode to search. DEFAULT 100")
    print("\t-l --language\t\tRepo language, used in 'new' mode to search. DEFAULT 'python'")


def main(argv):
    mode = ""
    output_directory = ""
    db_file = ""
    username = ""
    limit = 1000
    search_query = ""
    min_stars = 100
    language = "python"

    try:
        opts, args = getopt.getopt(argv, "hlstnm:o:d:u:",
                                   ["mode=", "out_dir=", "db_file=", "user=", "limit=", "search=",
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
    if mode == "" or output_directory == "" or db_file == "" or username == "":
        give_download_hint()
        sys.exit(2)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    os.chdir(output_directory)
    repos = create_repos(db_file)

    if mode == "new":
        new(repos, username, search_query, min_stars, language, limit, output_directory, db_file)
    elif mode == "recreate":
        recreate(repos, output_directory)
    else:
        print("Mode parameter must be 'new' or 'recreate'")

    print("Done.")


if __name__ == "__main__":
    main(sys.argv[1:])

