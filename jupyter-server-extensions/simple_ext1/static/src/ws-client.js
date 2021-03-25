"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const ws_1 = __importDefault(require("ws"));
var ws = new ws_1.default('ws://localhost:8888/echo', '', {});
ws.onopen = function (event) {
    console.log('PRODUCER: Event for URL', event.target.url);
    ws.send('hello');
};
//# sourceMappingURL=ws-client.js.map