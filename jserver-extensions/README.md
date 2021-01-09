[![Datalayer](https://raw.githubusercontent.com/datalayer/datalayer/main/res/logo/datalayer-25.svg?sanitize=true)](https://datalayer.io)

# Jupyter Server Simple Extension Example

```bash
yarn install && \
  yarn run build
```

```bash
pip install -e .
```

Ensure Jupyter Server is starting without any extension enabled.

```bash
# Run this command from a shell.
jupyter server
```

Browse the default home page, it should show a white page in your browser with the following content: `A Jupyter Server is running.`

```bash
# Jupyter Server default Home Page.
open http://localhost:8888
```

```bash
# Start the jupyter server activating simple_ext1 extension.
jupyter server --ServerApp.jpserver_extensions="{'simple_ext1': True}" --ServerApp.allow_origin=*
```

Now you can render `Extension 1` Server content in your browser.

```bash
# Home page as defined by default_url = '/default'.
open http://localhost:8888/simple_ext1/default
# HTML static page.
open http://localhost:8888/static/simple_ext1/home.html
open http://localhost:8888/static/simple_ext1/test.html
# Content from Handlers.
open http://localhost:8888/simple_ext1/params/test?var1=foo
# Content from Template.
open http://localhost:8888/simple_ext1/template1/test
# Content from Template with Typescript.
open http://localhost:8888/simple_ext1/typescript
# Error content.
open http://localhost:8888/simple_ext1/nope
# Redirect.
open http://localhost:8888/simple_ext1/redirect
# Favicon static content.
open http://localhost:8888/static/simple_ext1/favicon.ico
```

You can also start the server extension with python modules.

```bash
python -m simple_ext1
```

Start a Jupyter Server with a Node.js HTTP Server and send from a client a message via WebSocket.

```bash
# WebSocket Client <-> Jupyter WebSocket Server <-> HTTP Node.js Server
yarn server
...

WebSocket opened
PRODUCER: Event for URL ws://localhost:8888/simple_ext1/echo
WebSocket message: Hello Jupyter Server
URL /
'Params'
POST
Partial body: Hello Jupyter Server
Body: Hello Jupyter Server
{'text': 'Hello Jupyter Server'}
LISTENER: Got Message {"text":"Hello Jupyter Server"}
```