[![Datalayer](https://raw.githubusercontent.com/datalayer/datalayer/main/res/logo/datalayer-25.svg?sanitize=true)](https://datalayer.io)

# JupyterLab Extension EXamples

## Environment

```bash
conda deactivate && \
  conda remove -y --all -n jupyterlabextensions
# Create your conda environment.
conda create -y \
  -n jupyterlabextensions \
  python=3.8 \
  twine \
  nodejs=14.5.0 \
  yarn=1.22.5
conda activate jupyterlabextensions
```

```bash
pip install jupyter_packaging
```

```bash
# Install jupyterlab.
pip install jupyterlab==3.1.0b0
# ...or alternatively, clone and build jupyterlab from source.
git clone https://github.com/jupyterlab/jupyterlab --depth 1 -b master && \
  cd jupyterlab && \
  pip install -e . && \
  jupyter lab build && \
  cd ..
```

```bash
pip install ipywidgets==8.0.0a5
```

## Develop

```bash
# Build the extension and link for dev in shell 1.
jupyter labextension develop --overwrite
```

```bash
# List extensions.
jupyter labextension list
pip list | grep jupyterlabextensions
```

```bash
# Run and watch the extension in shell 1.
yarn watch
```

```bash
# Run and watch jupyterlab in shell 2.
# Look at the remote entry javascript, a webpack5 feature.
conda activate jupyterlabextensions && \
  jupyter lab \
    --watch \
    --ServerApp.token= \
    --ServerApp.jpserver_extensions="{'jupyterlabextensions': True}" \
    ./examples
```

```bash
# If you have build jupyterlab from source.
# Run and watch jupyterlab in shell 2.
# Look at the remote entry javascript, a webpack5 feature.
conda activate jupyterlabextensions && \
  jupyter lab \
    --watch \
    --dev-mode \
    --ServerApp.token= \
    --ServerApp.jpserver_extensions="{'jupyterlabextensions': True}" \
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

## Disable

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

## Publish

```bash
cd jupyterlabextensions && \
  yarn build:lib && \
  npm publish --access public
```

```bash
cd jupyterlabextensions && \
  pip install -e . && \
  python setup.py sdist bdist_wheel && \
  twine upload dist/*
```

## Use a Published Release

```bash
conda deactivate && \
  conda remove -y --all -n jupyterlabextensions-user
# Create your conda environment.
conda create -y \
  -n jupyterlabextensions-user \
  python=3.8 \
  nodejs=14.5.0
conda activate jupyterlabextensions-user
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
pip install jupyterlabextensions
jupyter labextension list
jupyter lab --notebook-dir=~/notebooks
```

# Launch JupyterLab with a Theme

```bash
# See https://jupyterlab.readthedocs.io/en/stable/user/directories.html#overridesjson
cat << EOF >>~/.jupyter/lab/user-settings/overrides.json
{
  "@jupyterlab/apputils-extension:themes": {
    "theme": "JupyterLab Christmas"
  }
}
EOF
```

```bash
# Optionally.
mkdir -p ~/.jupyter/lab/user-settings/\@jupyterlab/apputils-extension && \
  CONF="{ \"theme\": \"JupyterLab Christmas\" }" && \
  cat > ~/.jupyter/lab/user-settings/\@jupyterlab/apputils-extension/themes.jupyterlab-settings  <<EOF
${CONF}
EOF
```

```bash
# JupyterLab will start with the defined theme.
jupyter lab
```

## TODO

- [ ] Update the Launcher page with something like e.g. https://github.com/fcollonval/jupyterlab-enhanced-launcher
- [ ] Strip down the variables.css to only the needed css?
- [ ] Bring more fancy ui like in https://github.com/timkpaine/jupyterlab_miami_nights: Search tool + neon billboard + Collapser + neon light + Scrollbar + FM-84's "Atlas" (compatible with webKit browsers) + A surprise in the presentation mode (Top menu --> View --> Presention mode)

## Credits

This folder contains souce code taken from following repositories under MIT-compatible license:

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

- https://github.com/jupyterlab/scipy2019-jupyterlab-tutorial
- https://github.com/jupyterlab/benchmarks
- https://github.com/jupyterlab/jupyterlab-mp4

![](https://raw.githubusercontent.com/datalayer-examples/jupyter-examples/main/jupyterlabextensions/img/jupyterlab-rendermime-extensions-certificate.png "")

![](https://raw.githubusercontent.com/datalayer-examples/jupyter-examples/main/jupyterlabextensions/img/jupyterlab-rendermime-extensions-table.png "")

- https://github.com/jupyterlab/scipy2019-jupyterlab-tutorial

![](https://raw.githubusercontent.com/datalayer/examples/main/jupyterlab-rendermime/img/jupyterlab-rendermime-certificate.png "")

- https://github.com/jupyterlab/benchmarks

![](https://raw.githubusercontent.com/datalayer/examples/main/jupyterlab-rendermime/img/jupyterlab-rendermime-table.png "")

- https://github.com/jtpio/jupyter-resource-usage
- https://github.com/jtpio/jupyterlab-system-monitor
