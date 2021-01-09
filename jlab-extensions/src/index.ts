import autoCreate from './auto-create';
import cellFlash from './cell-flash';
import codeCellButton from './codecell-btn';
import contextMenu from './context-menu';
import execTime from './exec-time';
import nbMetadata from './nb-metadata';
import preview from './preview';
import pythonFile from './python-file';
import react from './react';
import recents from './recents';
import runAll from './run-all';
import themeToggle from './theme-toggle';
import topBar from './topbar';

import '../style/index.css';

export default [
    autoCreate,
    cellFlash,
    ...codeCellButton,
    contextMenu,
    execTime,
    nbMetadata,
    pythonFile,
    preview,
    react,
    recents,
    runAll,
    themeToggle,
    topBar,
];
