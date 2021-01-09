import {
  IDisposable
} from '@lumino/disposable';

import {
  JupyterFrontEnd, JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  ToolbarButton
} from '@jupyterlab/apputils';

import {
  DocumentRegistry
} from '@jupyterlab/docregistry';

import {
  NotebookPanel, INotebookModel
} from '@jupyterlab/notebook';

class RunAllCellsButtonExtension 
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {

  readonly app: JupyterFrontEnd;

  constructor(app: JupyterFrontEnd) {
    this.app = app;
  }

  createNew(panel: NotebookPanel, context: DocumentRegistry.IContext<INotebookModel>): IDisposable {
    // Create the on-click callback for the toolbar button.
    const runAllCells = () => {
      this.app.commands.execute('notebook:run-all-cells');
    };
    // Create the toolbar button.
    const button = new ToolbarButton({
      className: 'runAllCellsButton',      
      iconClass: 'fa fa-fast-forward',
      onClick: runAllCells,
      tooltip: 'Run All Cells'
    });
    // Add the toolbar button to the notebook.Ò
    panel.toolbar.insertItem(6, 'runAllCells', button);
    // The ToolbarButton class implements `IDisposable`, so the
    // button *is* the extension for the purposes of this method.
    return button;
  }
}

function activate(app: JupyterFrontEnd): void {
  let buttonExtension = new RunAllCellsButtonExtension(app);
  app.docRegistry.addWidgetExtension('Notebook', buttonExtension);
  app.contextMenu.addItem({
    selector: '.jp-Notebook',
    command: 'notebook:run-all-cells',
    rank: -0.5
  });
}

const runAll: JupyterFrontEndPlugin<void> = {
  id: 'runall-extension',
  autoStart: true,
  activate
};

export default runAll;
