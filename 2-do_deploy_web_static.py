#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['54.236.56.171', '	52.90.14.249']


def do_deploy(archive_path): #versions/web_static_20170315003959.tgz
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1] #web_static_20170315003959.tgz
        no_ext = file_n.split(".")[0] #web_static_20170315003959
        path = "/data/web_static/releases/" #where i will put data in server
        put(archive_path, '/tmp/') #Upload Archive to /tmp/ on remote server
        run('mkdir -p {}{}/'.format(path, no_ext)) #Create Release Directory /data/web_static/releases/web_static_20170315003959
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext)) #Uncompress the Archive to /data/web_static/releases/web_static_20170315003959
        run('rm /tmp/{}'.format(file_n)) # Remove Archive from /tmp/
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext)) #Move Contents of web_static
        run('rm -rf {}{}/web_static'.format(path, no_ext)) #Remove Empty web_static Directory
        run('rm -rf /data/web_static/current') #Remove Old Symbolic Link
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext)) #Create New Symbolic Link
        return True
    except:
        return False
