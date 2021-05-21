[![Datalayer](https://raw.githubusercontent.com/datalayer/datalayer/main/res/logo/datalayer-25.svg?sanitize=true)](https://datalayer.io)

# JupyterLab Simple Extension Example

## Environment

```bash
conda deactivate && \
  conda remove -y --all -n jupyterlab-extension-replace
# Create your conda environment.
conda create -y \
  -n jupyterlab-extension-replace \
  python=3.8 \
  twine \
  nodejs=14.5.0 \
  yarn=1.22.5 \
  cookiecutter
conda activate jupyterlab-extension-replace
pip install jupyter_packaging
```

```bash
# Install jupyterlab.
pip install jupyterlab==3.1.0a5
# ...or alternatively, clone and build jupyterlab from source.
git clone https://github.com/jupyterlab/jupyterlab --depth 1 -b master && \
  cd jupyterlab && \
  pip install -e . && \
  jupyter lab build && \
  cd ..
```

```bash
pip install ipywidgets==8.0.0a4
```

## Deactivate

```bash
# Reade https://jupyterlab.readthedocs.io/en/stable/extension/extension_dev.html#disabledextensions
# https://github.com/jupyterlab/jupyterlab/blob/d6c3857ac6ff27811f49fd63fcd529b763024f1f/packages/application-extension/src/index.tsx#L956-L972
jupyter labextension disable @jupyterlab/application-extension:logo
cat $(dirname $(which jupyter))/../etc/jupyter/labconfig/page_config.json
```

You can also deactivate a complete extension or a specific plugin with a definition in `package.json`.

```json
...
  "jupyterlab": {
    ...
    "disabledExtensions": [
      "@jupyterlab/application-extension:logo"
    ],
    ...
  }
...
```

## Develop

```bash
# Create an extension skeleton with a cookiecutter.
cookiecutter \
  https://github.com/jupyterlab/extension-cookiecutter-ts \
  --config-file cookiecutter.yaml
cd jupyterlab_logo
```

```bash
# Build the extension and link for dev in shell 1.
jupyter labextension develop --overwrite
```

```bash
# List extensions.
jupyter labextension list
pip list | grep jupyterlab-logo
```

```bash
# Run and watch the extension in shell 1.
yarn watch
```

```bash
# Run and watch jupyterlab in shell 2.
# Look at the remote entry javascript, a webpack5 feature.
conda activate jupyterlab-extension-replace && \
  jupyter lab \
    --watch \
    --ServerApp.token=
```

```bash
# Only if you have build jupyterlab from source.
# Run and watch jupyterlab in shell 2.
# Look at the remote entry javascript, a webpack5 feature.
conda activate jupyterlab-extension-replace && \
  jupyter lab \
    --watch \
    --dev-mode \
    --ServerApp.token= \
    --ServerApp.jpserver_extensions="{'jupyterlab-logo': True}" \
    --extensions-in-dev-mode 
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
cd jupyterlab_extensions && \
  yarn build:lib && \
  npm publish --access public
```

```bash
cd jupyterlab_extensions && \
  pip install -e . && \
  python setup.py sdist bdist_wheel && \
  twine upload dist/*
```

## Use

```bash
conda deactivate && \
  conda remove -y --all -n jupyterlab-extension-replace-user
# Create your conda environment.
conda create -y \
  -n jupyterlab-extension-replace-user \
  python=3.8 \
  nodejs=14.5.0
conda activate jupyterlab-extension-replace-user
pip install --pre jupyterlab==3.0.5
```

```bash
pip install jupyterlab_widgets==1.0.0a6
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
pip install @datalayer-examples/jupyterlab-extension-replace
jupyter labextension list
jupyter lab --notebook-dir=~/notebooks
```

## Credits

This folder contains code taken from following sources:

- https://github.com/deshaw/jupyterlab-execute-time
- https://github.com/ibqn/jupyterlab-codecellbtn
- https://github.com/jtpio/jupyterlab-cell-flash
- https://github.com/jtpio/jupyterlab-python-file
- https://github.com/jtpio/jupyterlab-theme-toggle
- https://github.com/jtpio/jupyterlab-topbar
- https://github.com/jupyterlab/extension-examples
- https://github.com/nersc/jupyterlab-recents
- https://github.com/voila-dashboards/voila
- https://github.com/yuvipanda/jupyterlab-nbmetadata
