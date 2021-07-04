import { JupyterFrontEnd, JupyterFrontEndPlugin } from "@jupyterlab/application";
import { IDocumentManager } from '@jupyterlab/docmanager';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { INotebookTracker } from '@jupyterlab/notebook';

const architecture: JupyterFrontEndPlugin<void> = {
  id: "jupyterlabestensions-architecture:plugin",
  autoStart: true,
  requires: [ IDocumentManager, INotebookTracker],
  activate: (
    app: JupyterFrontEnd,
    docManager: IDocumentManager,
    notebookTracker: INotebookTracker
  ) => {
    const fileTypes = docManager.registry.fileTypes();
    let ft: DocumentRegistry.IFileType;
    while (ft = fileTypes.next()) {
      console.log('fileType', ft, ft.mimeTypes, docManager.registry.defaultWidgetFactory('test.' + ft.extensions[0]));      
    }
    const modelFactories = docManager.registry.modelFactories();
    let mf: DocumentRegistry.IModelFactory<any>;
    while (mf = modelFactories.next()) {
      console.log('modelFactory', mf);
    }
    const widgetFactories = docManager.registry.widgetFactories();
    let wf: DocumentRegistry.WidgetFactory;
    while (wf = widgetFactories.next()) {
      console.log('widgetFactory', wf, wf.fileTypes);
      const widgetExtensions = docManager.registry.widgetExtensions(wf.name);
      let we: DocumentRegistry.WidgetExtension;
      while (we = widgetExtensions.next()) {
        console.log('--- widgetExtension', we);
      }
    }
  }

};

export default architecture;
