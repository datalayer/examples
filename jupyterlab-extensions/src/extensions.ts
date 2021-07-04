import architecture from './architecture';
import autoCreate from './auto-create';
import cellFlash from './cell-flash';
import christmasTheme from './christmas-theme';
import codeCellButton from './codecell-btn';
import contextMenu from './context-menu';
import execTime from './exec-time';
import logo from './logo';
import nbMetadata from './nb-metadata';
import preview from './preview';
import pythonFile from './python-file';
import kernelMemory from './kernel-memory/plugin';
import ipyresusePlugin from './kernel-memory/pluginIpywidget';
import react from './react';
import recents from './recents';
import runAll from './run-all';
import themeToggle from './theme-toggle';
import server from './server';
import topBar from './topbar';

import '../style/index.css';

export default [
    architecture,
    autoCreate,
    cellFlash,
    christmasTheme,
    ...codeCellButton,
    contextMenu,
    execTime,
    logo,
    nbMetadata,
    pythonFile,
    kernelMemory,
    ipyresusePlugin,
    preview,
    react,
    recents,
    runAll,
    server,
    themeToggle,
    topBar,
];
