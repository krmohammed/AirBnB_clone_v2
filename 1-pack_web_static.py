#!/usr/bin/python3
""" fabric script that generates a .tgz archive """
import os
from fabric.api import local
from datetime import datetime


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
        return filename
    else:
        return None
