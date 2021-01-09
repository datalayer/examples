import {
  JupyterFrontEnd, 
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ICommandPalette } from '@jupyterlab/apputils';

import { MainAreaWidget } from '@jupyterlab/apputils';

import { IMainMenu } from '@jupyterlab/mainmenu';

import { Menu } from '@lumino/widgets';

import LuminoCounter from './LuminoCounter';

import CounterWidget from './ReactCounter';

/**
 * The command IDs used by the extension.
 */
namespace CommandIDs {
  export const lumino = 'jupyterlab-examples:open-lumino-tab';
  export const react = 'jupyterlab-examples:open-react-tab';
}

/**
 * Initialization data for the @datalayer-examples/jlab-extensions:react extension.
 */
const react: JupyterFrontEndPlugin<void> = {
  id: '@datalayer-examples/jlab-extensions:react',
  autoStart: true,
  requires: [ICommandPalette, IMainMenu],
  activate: (
    app: JupyterFrontEnd,
    palette: ICommandPalette,
    mainMenu: IMainMenu
    ) => {

      console.log(
        '%cJupyterLab extension @datalayer-examples/jlab-extensions:react is activated, Yeah!!!',
        'font-size: 30px'
      );

      const { commands, shell } = app;
      const menu = new Menu({ commands });  
      menu.title.label = 'React Examples';
      mainMenu.addMenu(menu, { rank: 80 });

      // Lumino.
      commands.addCommand(CommandIDs.lumino, {
        label: 'Open a Lumino Widget in a Tab',
        caption: 'Open a Lumino Widget in a Tab',
        execute: () => {
          const widget = new LuminoCounter();
          shell.add(widget, 'main');
        }
      });
      palette.addItem({ command: CommandIDs.lumino, category: 'React Examples' });
      menu.addItem({ command: CommandIDs.lumino });

      // React.
      commands.addCommand(CommandIDs.react, {
        label: 'Open a React Widget in a Tab',
        caption: 'Open a React Widget in a Tab',
        execute: () => {
          const content = new CounterWidget(true);
          const widget = new MainAreaWidget<CounterWidget>({ content });
          widget.title.label = 'React';
          app.shell.add(widget, 'main');
        }
      });
      palette.addItem({ command: CommandIDs.react , category: 'React Examples' });
      menu.addItem({ command: CommandIDs.react });

    }

};

export default react;
