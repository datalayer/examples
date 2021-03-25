[![Datalayer](https://raw.githubusercontent.com/datalayer/datalayer/main/res/logo/datalayer-25.svg?sanitize=true)](https://datalayer.io)

# JupyterLab Rendermime Examples

![](https://raw.githubusercontent.com/datalayer/examples/main/jupyterlab-rendermime-extensions/img/jupyterlab-rendermime-extensions.png "")

## Environment

```bash
conda deactivate && \
  conda remove -y --all -n jupyterlab-rendermime-extensions
# Create your conda environment.
conda create -y \
  -n jupyterlab-rendermime-extensions \
  python=3.8 \
  twine \
  nodejs=14.5.0 \
  yarn=1.22.5 \
  cookiecutter
conda activate jupyterlab-rendermime-extensions
pip install jupyter_packaging
```

```bash
# Install jupyterlab.
pip install jupyterlab==3.0.5
# ...or alternatively, clone and build jupyterlab from source.
git clone https://github.com/jupyterlab/jupyterlab --depth 1 -b master && \
  cd jupyterlab && \
  pip install -e . && \
  jupyter lab build && \
  cd ..
```

```bash
pip install ipywidgets==7.6.0
```

## Develop

```bash
# Create an extension skeleton with a cookiecutter.
cookiecutter \
  https://github.com/jupyterlab/mimerender-cookiecutter-ts \
  --config-file cookiecutter.yaml \
  --checkout jlab3 && \
cd jlab_rendermime_extensions
```

```bash
# Build the extension and link for dev in shell 1.
jupyter labextension develop --overwrite
```

```bash
# List extensions.
jupyter labextension list
pip list | grep jupyterlab-rendermime-extensions
```

```bash
# Run and watch extension in shell 1.
yarn watch
```

```bash
# Run and watch jupyterlab in shell 2.
# Look at the remote entry javascript, a webpack5 feature.
conda activate jupyterlab-rendermime-extensions && \
  jupyter lab \
    --watch \
    --ServerApp.token= \
    ./examples
```

```bash
# Only if you have build jupyterlab from source.
# Run and watch jupyterlab in shell 2.
# Look at the remote entry javascript, a webpack5 feature.
conda activate jupyterlab-rendermime-extensions && \
  jupyter lab \
    --watch \
    --dev-mode \
    --ServerApp.token= \
    --extensions-in-dev-mode \
    ./examples
```

## Build

```bash
# Generate sourcemaps.
jupyter labextension build --development=True .
jupyter lab build --minimize=False
```

```bash
# Do not generate sourcemaps.
jupyter labextension build .
jupyter lab build
```

## Publish

```bash
cd jlab_rendermime_extensions && \
  yarn build:lib && \
  npm publish --access public
```

```bash
cd jlab_rendermime_extensions && \
  pip install -e . && \
  python setup.py sdist bdist_wheel && \
  twine upload dist/*
```

## Use

```bash
conda deactivate && \
  conda remove -y --all -n jupyterlab-rendermime-extensions-user
# Create your conda environment.
conda create -y \
  -n jupyterlab-rendermime-extensions-user \
  python=3.8 \
  nodejs=14.5.0
conda activate jupyterlab-rendermime-extensions-user
pip install jupyterlab==3.0.5 ipywidgets==7.6.0
```

```bash
jupyter labextension list
# Check the Extension Manager.
jupyter lab --notebook-dir=~/notebooks
```

```bash
# https://pypi.org/project/jupyterlab-geojs/#history
pip search "jupyterlab extension"
pip search "JupyterLab3"
```

```bash
pip install @datalayer-examples/jupyterlab-rendermime-extensions
jupyter labextension list
jupyter lab --notebook-dir=~/notebooks
```

## Credits

This repository contains code taken from following sources:

- https://github.com/jupyterlab/scipy2019-jupyterlab-tutorial
- https://github.com/jupyterlab/benchmarks
- https://github.com/jupyterlab/jupyterlab-mp4

![](https://raw.githubusercontent.com/datalayer/examples/main/jupyterlab-rendermime-extensions/img/jupyterlab-rendermime-extensions-certificate.png "")

![](https://raw.githubusercontent.com/datalayer/examples/main/jupyterlab-rendermime-extensions/img/jupyterlab-rendermime-extensions-table.png "")
