import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from "@jupyterlab/application";

import { IDocumentManager } from '@jupyterlab/docmanager';

import { INotebookTracker } from "@jupyterlab/notebook";

/**
 * Initialization for the autoCreate extension.
 */
const autoCreate: JupyterFrontEndPlugin<void> = {
  id: "@datalayer-examples/auto-create",
  autoStart: true,
  requires: [INotebookTracker, IDocumentManager],
  activate: (
    app: JupyterFrontEnd,
    notebookTracker: INotebookTracker,
    docManager: IDocumentManager,
  ) => {
    const notebook = docManager.createNew('tmp.ipynb', 'notebook')
    app.shell.add(notebook, 'main')
  }

};

export default autoCreate;
