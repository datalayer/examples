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
 * Initialization data for the jupyterlabextensions:react extension.
 */
const react: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlabextensions:react',
  autoStart: true,
  requires: [ICommandPalette, IMainMenu],
  activate: (
    app: JupyterFrontEnd,
    palette: ICommandPalette,
    mainMenu: IMainMenu
    ) => {

      console.log(
        '%cjupyterlabextensions:react is activated, Yeah!!!',
        'font-size: 16px'
      );

      const { commands, shell } = app;
      const menu = new Menu({ commands });  
      menu.title.label = 'Datalayer Examples';
      mainMenu.addMenu(menu, { rank: 80 });

      const sleep = (ms: number) => {
        return new Promise(resolve => setTimeout(resolve, ms));
      }

      async function asyncWait(message: string) {
        console.log('Taking a break...', message, new Date());
        await sleep(5000);
        console.log('Five seconds later, showing sleep in a loop...', message, new Date());
        for (let i = 0; i < 5; i++) {
          await sleep(5000);
          console.log(message, i, new Date());
        }
      }

      const promiseWait = (message: string): Promise<string> => {
        return new Promise((resolve, reject) => {
          console.log('Taking a break...', message, new Date(), new Date());
          sleep(5000).then(() => console.log('Waking up...', new Date()));
          console.log('Five seconds later, showing sleep in a loop...', message, new Date());
          for (let i = 0; i < 5; i++) {
            sleep(5000).then(() => console.log('Slept...', i, new Date()));
            console.log(message, i, new Date());
          }
          resolve('promiseWait function is resolved')
        })
      }

      function fetchGitHub() {
        fetch('https://api.github.com/users/echarles')
          .then(res => res.json())
          .then(json => console.log(json, new Date()));
        /*
        const date = Date.now();
        let currentDate = null;
        do {
          currentDate = Date.now();
        } while (currentDate - date < 5000);
        */
      }

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
      palette.addItem({ command: CommandIDs.react , category: 'Datalayer Examples' });
      menu.addItem({ command: CommandIDs.react });

     // Lumino.
     commands.addCommand(CommandIDs.lumino, {
      label: 'Open a Lumino Widget in a Tab',
      caption: 'Open a Lumino Widget in a Tab',
      execute: () => {
        promiseWait('Sleep Lumino with Promise').then((s) => console.log(s, new Date()));
        asyncWait('Sleep Lumino with Async');
        for (let i=0; i < 100; i++) fetchGitHub()
        console.log('--- Lumino');
        const widget = new LuminoCounter();
        shell.add(widget, 'main');
      }
    });
    palette.addItem({ command: CommandIDs.lumino, category: 'Datalayer Examples' });
    menu.addItem({ command: CommandIDs.lumino });

  }

};

export default react;
