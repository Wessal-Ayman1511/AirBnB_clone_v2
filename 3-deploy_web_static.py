#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers.
Usage: fab -f 3-deploy_web_static.py deploy -i ~/.ssh/id_rsa -u ubuntu
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir

# Set up the remote servers
env.hosts = ['54.236.56.171', '52.90.14.249']

def do_pack():
    """Generates a .tgz archive from the web_static folder."""
    try:
        # Create a timestamp for the archive file name
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Check if the versions directory exists, create it if not
        if not isdir("versions"):
            local("mkdir versions")
        
        # Define the archive file name and path
        file_name = "versions/web_static_{}.tgz".format(date)
        
        # Create the .tgz archive of the web_static folder
        local("tar -cvzf {} web_static".format(file_name))
        
        return file_name
    except Exception as e:
        # Print error message and return None if something goes wrong
        print(f"Error in do_pack: {e}")
        return None

def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not exists(archive_path):
        return False
    
    try:
        # Extract the file name and name without extension
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        
        # Upload the archive to the remote server's /tmp/ directory
        put(archive_path, '/tmp/')
        
        # Create the release directory on the remote server
        run('mkdir -p {}{}/'.format(path, no_ext))
        
        # Uncompress the archive to the release directory
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        
        # Remove the archive from the /tmp/ directory
        run('rm /tmp/{}'.format(file_n))
        
        # Move contents from web_static to the release directory
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        
        # Remove the now empty web_static directory
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        
        # Remove the old symbolic link
        run('rm -rf /data/web_static/current')
        
        # Create a new symbolic link pointing to the new release
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        
        return True
    except Exception as e:
        # Print error message and return False if something goes wrong
        print(f"Error in do_deploy: {e}")
        return False

def deploy():
    """Creates and distributes an archive to the web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
