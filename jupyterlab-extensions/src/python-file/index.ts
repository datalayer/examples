import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ICommandPalette } from '@jupyterlab/apputils';

import { ILauncher } from '@jupyterlab/launcher';

import { IFileBrowserFactory } from '@jupyterlab/filebrowser';

import { IMainMenu } from '@jupyterlab/mainmenu';

const FACTORY = 'Editor';

const ICON_CLASS = 'jp-PythonIcon';

const PALETTE_CATEGORY = 'Text Editor';

namespace CommandIDs {
  export const createNew = 'fileeditor:create-new-python-file';
}

const pythonFile: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-python-file',
  autoStart: true,
  optional: [IFileBrowserFactory, ILauncher, IMainMenu, ICommandPalette],
  activate: (
    app: JupyterFrontEnd,
    browserFactory: IFileBrowserFactory | null,
    launcher: ILauncher | null,
    menu: IMainMenu | null,
    palette: ICommandPalette
  ) => {
    const { commands, contextMenu } = app;
    const command = CommandIDs.createNew;
    commands.addCommand(command, {
      label: args =>
        args['isPalette'] || args['isContextMenu']
          ? 'New Python File'
          : 'Python File',
      caption: 'Create a new Python file',
      iconClass: args => (args['isPalette'] ? '' : ICON_CLASS),
      execute: async args => {
        const cwd =
          args['cwd'] ?? browserFactory?.defaultBrowser.model.path ?? undefined;
        const model = await commands.execute('docmanager:new-untitled', {
          path: cwd,
          type: 'file',
          ext: 'py'
        });
        return commands.execute('docmanager:open', {
          path: model.path,
          factory: FACTORY
        });
      }
    });
    // Add to the file browser context menu.
    const selectorContent = '.jp-DirListing-content';
    contextMenu.addItem({
      command,
      args: { isContextMenu: true },
      selector: selectorContent,
      rank: 3
    });
    // Add to the launcher.
    if (launcher) {
      launcher.add({
        command,
        category: 'Other',
        rank: 1
      });
    }
    // Add to the palette.
    if (palette) {
      palette.addItem({
        command,
        args: { isPalette: true },
        category: PALETTE_CATEGORY
      });
    }
    // Add to the menu.
    if (menu) {
      menu.fileMenu.newMenu.addGroup([{ command }], 30);
    }
  }
}

export default pythonFile;
