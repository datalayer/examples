import {
  ILabShell,
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { circleIcon } from '@jupyterlab/ui-components';

import { Widget } from '@lumino/widgets';

const logo: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlabextensions:logo',
  autoStart: true,
  requires: [ILabShell],
  activate: (app: JupyterFrontEnd, shell: ILabShell) => {
    console.log('JupyterLab extension jupyterlabextensions:logo is activated!');
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
    console.log('The new logo is added');
  }
};

export default logo;
