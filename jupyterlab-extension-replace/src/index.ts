import {
  ILabShell,
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { circleIcon } from '@jupyterlab/ui-components';

import { Widget } from '@lumino/widgets';

/**
 * Initialization data for the @datalayer-examples/jupyterlab-logo extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: '@datalayer-examples/jupyterlab-logo:plugin',
  autoStart: true,
  requires: [ILabShell],
  activate: (app: JupyterFrontEnd, shell: ILabShell) => {
    console.log('JupyterLab extension @datalayer-examples/jupyterlab-logo is activated!');
    const logo = new Widget();
    circleIcon.element({
      container: logo.node,
      elementPosition: 'center',
      margin: '2px 2px 2px 8px',
      height: 'auto',
      width: '16px'
    });
    logo.id = 'jp-MainLogo';
    shell.add(logo, 'top', { rank: 0 });
    console.log('New JupyterLab logo added to top panel');
  }
};

export default extension;
