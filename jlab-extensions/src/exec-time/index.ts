import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  INotebookTracker,
  INotebookModel,
  NotebookPanel
} from '@jupyterlab/notebook';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { DocumentRegistry } from '@jupyterlab/docregistry';

import ExecuteTimeWidget from './ExecuteTimeWidget';

class ExecuteTimeWidgetExtension implements DocumentRegistry.WidgetExtension {
  private _settingRegistry: ISettingRegistry;
  constructor(settingRegistry: ISettingRegistry) {
    this._settingRegistry = settingRegistry;
  }
  // We get a notebook panel because of addWidgetExtension('Notebook', ...) below.
  createNew(
    panel: NotebookPanel,
    context: DocumentRegistry.IContext<INotebookModel>
  ) {
    return new ExecuteTimeWidget(panel, this._settingRegistry);
  }
}

/**
 * Initialization data for the extension.
 */
const execTime: JupyterFrontEndPlugin<void> = {
  id: 'exec-time',
  autoStart: true,
  requires: [INotebookTracker, ISettingRegistry],
  activate: (
    app: JupyterFrontEnd,
    notebookTracker: INotebookTracker,
    settingRegistry: ISettingRegistry
  ) => {
    // We need notebookTracker to ensure correct injection order.
    app.docRegistry.addWidgetExtension(
      'notebook',
      new ExecuteTimeWidgetExtension(settingRegistry)
    );
  }
};

export default execTime;
