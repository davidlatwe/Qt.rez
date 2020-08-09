
early = globals()["early"]  # lint helper


name = "Qt.py"

uuid = "repository.Qt.py"

description = "Minimal Python 2 & 3 shim around all Qt bindings - " \
              "PySide, PySide2, PyQt4 and PyQt5."


def __rmtree(path):
    import os
    import stat
    import shutil

    # handling read-only files in .git
    def del_rw(action, name, exc):
        os.chmod(name, stat.S_IWRITE)
        os.remove(name)

    shutil.rmtree(path, onerror=del_rw)


@early()
def __payload():
    import os
    import json
    import tempfile
    from subprocess import check_output, CalledProcessError

    if os.getenv("GIT_CLONED"):
        # Reuse data from previous clone
        data = json.loads(os.environ["GIT_CLONED"])
        return data

    url = "https://github.com/mottosso/Qt.py.git"

    tmpdir = tempfile.mkdtemp()
    tempdir = os.path.join(tmpdir, "Qt.py")
    try:
        check_output(["git", "clone", "--single-branch", url, tempdir])
        check_output(["git", "fetch", "--tags"], cwd=tempdir)
        commit = check_output(["git", "rev-list", "--tags", "--max-count=1"],
                              cwd=tempdir).strip().decode()
        tag = check_output(["git", "describe", "--tags", commit],
                           cwd=tempdir).strip().decode()
        check_output(["git", "checkout", tag], cwd=tempdir)

    except CalledProcessError:
        __rmtree(tempdir)
        raise

    data = {
        "repo": tempdir,
        "tag": tag,
    }
    # Avoid repeating in each variation build
    os.environ["GIT_CLONED"] = json.dumps(data)

    return data


@early()
def version():
    data = globals()["this"].__payload
    return data["tag"]


@early()
def authors():
    from subprocess import check_output

    data = globals()["this"].__payload
    repo = data["repo"]

    name_list = check_output(["git", "shortlog", "-sn"],
                             cwd=repo).strip().decode()
    contributors = [n.strip().split("\t", 1)[-1]
                    for n in name_list.split("\n")]
    contributors.append("davidlatwe")

    return contributors


@early()
def variants():
    import os
    from rez import packages

    bindings = [
        "PyQt5",
        "PySide2",
        "PyQt4",
        "PySide",
    ]
    variants_ = [
        [binding] for binding in bindings
        if packages.get_latest_package_from_string(binding)
    ]
    if not variants_:
        # cleanup
        data = globals()["this"].__payload
        __rmtree(data["repo"])

        raise Exception("No Qt binding package found.")

    os.environ["REZ_BUILD_VARIANT_COUNT"] = str(len(variants_))

    return variants_


build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]
    env.PYTHONPATH.prepend("{root}/payload")
