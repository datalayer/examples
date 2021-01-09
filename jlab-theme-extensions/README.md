[![Datalayer](https://raw.githubusercontent.com/datalayer/datalayer/main/res/logo/datalayer-25.svg?sanitize=true)](https://datalayer.io)

# JupyterLab Theme Examples

## Environment

```bash
conda deactivate && \
  conda remove -y --all -n jlab-theme-extensions
# Create your conda environment.
conda create -y \
  -n jlab-theme-extensions \
  python=3.8 \
  twine \
  nodejs=14.5.0 \
  yarn=1.22.5 \
  cookiecutter
conda activate jlab-theme-extensions
pip install jupyter_packaging
```

```bash
# Install jupyterlab.
pip install jupyterlab==3.0.1
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
  https://github.com/jupyterlab/extension-cookiecutter-ts \
  --config-file cookiecutter.yaml \
  --checkout master && \
cd jlab_theme_extensions
```

```bash
# Build the extension and link for dev in shell 1.
cd jlab_theme_extensions && \
  jupyter labextension develop --overwrite
```

```bash
# List extensions.
jupyter labextension list
pip list | grep jlab-theme-extensions
```

```bash
# Run and watch extension in shell 1.
yarn watch
```

```bash
# Run and watch jupyterlab in shell 2.
# Look at the remote entry javascript, a webpack5 feature.
#    --dev-mode \ # you can use dev-mode is you have installed from source
conda activate jlab-theme-extensions && \
  jupyter lab \
    --watch \
    --ServerApp.token=
```

```bash
# Only if you have build jupyterlab from source.
# Run and watch jupyterlab in shell 2.
# Look at the remote entry javascript, a webpack5 feature.
#    --dev-mode \ # you can use dev-mode is you have installed from source
conda activate jupyterlab-extension-examples && \
  jupyter lab \
    --watch \
    --dev-mode
    --ServerApp.token= \
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
cd jlab_theme_extensions && \
  yarn build:lib && \
  npm publish --access public
```

```bash
cd jlab_theme_extensions && \
  pip install -e . && \
  python setup.py sdist bdist_wheel && \
  twine upload dist/*
```

## Use

```bash
conda deactivate && \
  conda remove -y --all -n jlab-theme-extensions-user
# Create your conda environment.
conda create -y \
  -n jlab-theme-extensions-user \
  python=3.8 \
  nodejs=14.5.0
conda activate jlab-theme-extensions-user
pip install --pre jupyterlab==3.0.0rc6
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
pip install @datalayer-examples/jupyterlab-rendermime
jupyter labextension list
jupyter lab --notebook-dir=~/notebooks
```

# How to launch jupyter lab with a defined theme?

```bash
mkdir -p ~/.jupyter/lab/user-settings/\@jupyterlab/apputils-extension && \
  CONF="{ \"theme\": \"JupyterLab Christmas\" }" && \
  cat > ~/.jupyter/lab/user-settings/\@jupyterlab/apputils-extension/themes.jupyterlab-settings  <<EOF
${CONF}
EOF
jupyter lab
```

## TODO

Update the Launcher page with something like e.g. https://github.com/fcollonval/jlab-enhanced-launcher
Strip down the variables.css to only the needed css?
Bring more fancy ui like in https://github.com/timkpaine/jupyterlab_miami_nights: Search tool + neon billboard + Collapser + neon light + Scrollbar + FM-84's "Atlas" (compatible with webKit browsers) + A surprise in the presentation mode (Top menu --> View --> Presention mode)

## Credits

> Taken from https://github.com/jupyterlab/scipy2019-jupyterlab-tutorial

![](https://raw.githubusercontent.com/datalayer/examples/main/jupyterlab-rendermime/img/jupyterlab-rendermime-certificate.png "")

> Taken from https://github.com/jupyterlab/benchmarks

![](https://raw.githubusercontent.com/datalayer/examples/main/jupyterlab-rendermime/img/jupyterlab-rendermime-table.png "")
