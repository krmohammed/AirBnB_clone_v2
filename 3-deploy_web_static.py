#!/usr/bin/python3
""" a fabric script that creates and distributes an archive to your web servers """
import os
from fabric.operations import local
from fabric.api import env, put, run
from datetime import datetime


env.user = "ubuntu"
env.hosts = ['35.153.57.28', '34.232.71.62']


def do_pack():
    """
    generates .tgz file from the contents of the web_static folder
    """
    if not os.path.exists("versions"):
        os.makedirs("versions")

    now = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "versions/web_static_{}.tgz".format(now)

    tgz_file = local("tar -cvzf {} web_static".format(filename))

    if tgz_file.succeeded:
        return tgz_file
    else:
        return None


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
        filename.split(".")[0] + "/"
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


def deploy():
    """
    creates and distributes an archive to your web servers
    """
    tzg_file = do_pack()

    if not tzg_file:
        return False
    return do_deploy(tzg_file)
