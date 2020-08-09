
import os
import sys


def __rmtree(path):
    import os
    import stat
    import shutil

    # handling read-only files in .git
    def del_rw(action, name, exc):
        os.chmod(name, stat.S_IWRITE)
        os.remove(name)

    shutil.rmtree(path, onerror=del_rw)


def build(source_path, build_path, install_path, targets=None):
    import json
    import shutil

    targets = targets or []

    if "install" in targets:
        dst = install_path + "/payload"
    else:
        dst = build_path + "/payload"

    dst = os.path.normpath(dst)

    if os.path.isdir(dst):
        __rmtree(dst)
    os.makedirs(dst)

    data = json.loads(os.environ["GIT_CLONED"])

    shutil.copy2(os.path.join(data["repo"], "Qt.py"),
                 os.path.join(dst, "Qt.py"))

    index = int(os.environ["REZ_BUILD_VARIANT_INDEX"])
    last = int(os.environ["REZ_BUILD_VARIANT_COUNT"]) - 1
    if index == last:
        # last one, do cleanup
        __rmtree(data["repo"])


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
