# JupyterHub configuration
#
## If you update this file, do not forget to delete the `jupyterhub_data` volume before restarting the jupyterhub service:
##
##     docker volume rm jupyterhub_jupyterhub_data
##
## or, if you changed the COMPOSE_PROJECT_NAME to <name>:
##
##    docker volume rm <name>_jupyterhub_data
##

import os

## Generic
c.JupyterHub.admin_access = True
c.Spawner.default_url = '/lab'

# LDAP authentication
c.JupyterHub.authenticator_class = 'ldapauthenticator.LDAPAuthenticator'
c.LDAPAuthenticator.server_address = '161.97.161.11'
c.LDAPAuthenticator.bind_dn_template = ["uid={username},cn=users,cn=accounts,dc=mim,dc=lan"]
# Restricting to a group doesn't work, don't know why:
# c.LDAPAuthenticator.allowed_groups = ["cn=jupyterhub-buka,cn=groups,cn=accounts,dc=mim,dc=lan"]
c.LDAPAuthenticator.use_ssl = True
c.LDAPAuthenticator.allow_nested_groups = True

## Docker spawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = os.environ['DOCKER_JUPYTER_CONTAINER']
c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.image_whitelist = {
    "deepdetect-gpu (Tensorflow+PyTorch)": "jolibrain/jupyter-dd-notebook-gpu",
    "tensorflow-2-gpu (Tensorflow 2.0)": "d4n1el/tensorflow-2-notebook-gpu",
    "datascience-gpu (Python+Julia+R)": "d4n1el/datascience-notebook-gpu",
    "tensorflow-cpu (Tensorflow)": "jupyter/tensorflow-notebook",
    "datascience-cpu (Python+Julia+R)": "jupyter/datascience-notebook",
}

# See https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py
c.JupyterHub.hub_ip = os.environ['HUB_IP']
c.JupyterHub.shutdown_on_logout = True
c.LDAPAuthenticator.admin_users = {'arturkiwa'}

c.ResourceUseDisplay.mem_limit = 4294967296
c.ResourceUseDisplay.track_cpu_percent = True
c.ResourceUseDisplay.cpu_limit = 2

# user data persistence
# see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }
#c.DockerSpawner.extra_host_config = { '--gpus': 'all', }

# Other stuff
c.Spawner.cpu_limit = 2
c.Spawner.mem_limit = '10G'


## Services
#c.JupyterHub.services = [
#    {
#        'name': 'cull_idle',
#        'admin': True,
#        'command': 'python /srv/jupyterhub/cull_idle_servers.py --timeout=3600'.split(),
#    },
#]
