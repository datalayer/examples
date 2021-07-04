import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the @datalayer-examples/jupyterlab-extensions extension.
 */
const christmasTheme: JupyterFrontEndPlugin<void> = {
  id: '@datalayer-examples/jupyterlab-extensions',
  requires: [IThemeManager],
  autoStart: true,
  activate: (app: JupyterFrontEnd, themeManager: IThemeManager) => {
    console.log('JupyterLab extension @datalayer-examples/jupyterlab-extensions is activated!');
    const style = '@datalayer-examples/jupyterlab-extensions/index.css';
    themeManager.register({
      name: 'JupyterLab Christmas',
      isLight: true,
      load: () => themeManager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default christmasTheme;
