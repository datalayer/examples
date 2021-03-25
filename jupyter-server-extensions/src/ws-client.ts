import WebSocket from 'ws';

var ws = new WebSocket('ws://localhost:8888/simple_ext1/echo', '', {});

ws.onmessage = function(m) {
    console.log('LISTENER: Got Message', m.data);
}

ws.onopen = function (event: any) {
    console.log('PRODUCER: Event for URL', event.target.url);
    ws.send('Hello Jupyter Server');
};
