[![Datalayer](https://raw.githubusercontent.com/datalayer/datalayer/main/res/logo/datalayer-25.svg?sanitize=true)](https://datalayer.io)

# Docker with JupyterLab 3 Extensions

This repository contains a Docker based demo of `JupyterLab` running on `Jupyter Server`:

- JupyterLab is now a [Jupyter Server extension](https://jupyter-server.readthedocs.io/en/latest/developers/extensions.html).
- [NbClassic](https://github.com/Zsailer/nbclassic) provides a shim for configuration and generates warning for deprecated NotebookApp configuration usage and ensures backwards compatibility of existings notebook server extensions.

JupyterLab is built from source and we add the following extensions:

- jupyterlab extension example https://github.com/jupyterlab/extension-examples/blob/3.0/advanced/server-extension/README.md
- jupyterlab git https://github.com/jupyter/nbdime/pull/551 + https://github.com/jupyterlab/jupyterlab-git/pull/818
- jupyterlab voila https://github.com/voila-dashboards/voila/pull/732

## Build the Docker Image

```bash
# Use it with Docker.
make build
```

Some details when building the docker image (you can see the [`@jupyterlab-examples/server-extension` notebook extension being activated and usable](https://github.com/jupyterlab/extension-examples/blob/master/advanced/server-extension/README.md)).

```
 ---> Running in f4ee6660637c
Package                       Version             Location
----------------------------- ------------------- --------------------------------------------------------------------
jlab-ext-example              0.1.0               /home/jovyan/jupyterlab-extension-examples/advanced/server-extension
jupyter-server                0.3.0               /home/jovyan/jupyter_server
jupyterlab                    3.0.0a0             /home/jovyan/jupyterlab
jupyterlab-server             1.1.5               /home/jovyan/jupyterlab-server
nbclassic                     0.1                 /home/jovyan/nbclassic
notebook                      6.0.3
Removing intermediate container f4ee6660637c
 ---> f7b14ceebfd8
Step 13/19 : RUN jupyter serverextension list
 ---> Running in 52c3c878b19c
Removing intermediate container 52c3c878b19c
 ---> 25700b73ae7a
Step 14/19 : RUN jupyter server extension list
 ---> Running in fa4b1ab2ce85
Removing intermediate container fa4b1ab2ce85
 ---> 8e7bb57e53bd
Step 15/19 : RUN jupyter labextension list
 ---> Running in 0dd77b1e5669
   app dir: /opt/conda/share/jupyter/lab
        @jupyterlab-examples/server-extension v0.1.0 enabled OK*
JupyterLab v3.0.0a0
Known labextensions:
   local extensions:
        @jupyterlab-examples/server-extension: /home/jovyan/jupyterlab-extension-examples/advanced/server-extension
Removing intermediate container 0dd77b1e5669
 ---> 216397488a21
```

## Start

```bash
# Use it with Docker.
make start
open http://localhost:8888
```

```bash
# Stop and remove the Docker container.
make stop
make rm
```

## NbClassic Shim

```bash
# Inspect the logs in another terminal.
make logs
# You can see warning created by nbclassic for the deprecated configuration like:
# [LabApp] WARNING | 'token' has moved from NotebookApp to ServerApp. This config will be passed to ServerApp. Be sure to update your config before our next release.
# [LabApp] WARNING | 'password' has moved from LabApp to ServerApp. Be sure to update your config before our next release.
```

## Notebook Extensions Backwards Compatibility

![server extension example](./img/server-extension.png)
