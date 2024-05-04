#!/usr/bin/python3
""" a Fabric script that distributes an archive to your web servers """
import os
from fabric.api import env, put, run


env.user = "ubuntu"
env.hosts = ['35.153.57.28', '34.232.71.62']


def do_deploy(archive_path):
    """distributes an archive to your web servers

    Args:
        archive_path (str): path to archive file
    """
    if not os.path.exists(archive_path):
        return False

    # upload the archive file to /tmp/ directory
    put(archive_path, "/tmp/")

    # extraction of archive file
    filename = os.path.basename(archive_path)
    to_release = "/data/web_static/releases/" + \
            filename.split(".").[0] + "/"
    run("mkdir -p {}".format(to_release))
    run("tar -xzf /tmp/{} -C {}".format(filename, to_release))

    # deleting archive file
    run("rm /tmp/{}".format(filename))

    # move extracted files to to_release and delete
    run("mv {}web_static/* {}".format(to_release, to_release))
    run("rm -rf {}web_static".format(to_release))

    # deletion and creation of symbolic link
    ln_path = "/data/web_static/current"
    run("rm -rf {}".format(ln_path))
    run("ln -s {} {}".format(to_release, ln_path))

    print("New version deployed!")
    return True
