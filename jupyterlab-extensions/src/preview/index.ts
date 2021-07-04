import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
  ILayoutRestorer
} from "@jupyterlab/application";

import {
  ICommandPalette,
  WidgetTracker,
  ToolbarButton
} from "@jupyterlab/apputils";

import { ISettingRegistry } from "@jupyterlab/settingregistry";

import { DocumentRegistry } from "@jupyterlab/docregistry";

import { IMainMenu } from "@jupyterlab/mainmenu";

import {
  INotebookTracker,
  NotebookPanel,
  INotebookModel
} from "@jupyterlab/notebook";

import { CommandRegistry } from "@lumino/commands";

import { ReadonlyJSONObject } from "@lumino/coreutils";

import { IDisposable } from "@lumino/disposable";

import {
  PREVIEW_ICON_CLASS,
  Preview,
  IPreviewTracker,
  PreviewFactory
} from "./preview";

/**
 * The command IDs used by the plugin.
 */
export namespace CommandIDs {
  export const previewRender = "notebook:render-with-preview";
  export const previewOpen = "notebook:open-with-preview";
}

/**
 * A notebook widget extension that adds a preview preview button to the toolbar.
 */
class PreviewRenderButton
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {

  private _commands: CommandRegistry;

  /**
   * Instantiate a new PreviewRenderButton.
   * @param commands The command registry.
   */
  constructor(commands: CommandRegistry) {
    this._commands = commands;
  }

  /**
   * Create a new extension object.
   */
  createNew(panel: NotebookPanel): IDisposable {
    const button = new ToolbarButton({
      className: "previewRender",
      tooltip: "Render with Preview",
      iconClass: PREVIEW_ICON_CLASS,
      onClick: () => {
        this._commands.execute(CommandIDs.previewRender);
      }
    });
    panel.toolbar.insertAfter("cellType", "previewRender", button);
    return button;
  }

}

/**
 * Initialization data for the jupyterlab-preview extension.
 */
const preview: JupyterFrontEndPlugin<IPreviewTracker> = {
  id: "jupyterlabextensions:plugin",
  autoStart: true,
  requires: [INotebookTracker],
  optional: [ICommandPalette, ILayoutRestorer, IMainMenu, ISettingRegistry],
  provides: IPreviewTracker,
  activate: (
    app: JupyterFrontEnd,
    notebookTracker: INotebookTracker,
    palette: ICommandPalette | null,
    restorer: ILayoutRestorer | null,
    menu: IMainMenu | null,
    settingRegistry: ISettingRegistry | null
  ) => {

    const { commands, docRegistry } = app;

    // Create a widget tracker for Previews.
    const tracker = new WidgetTracker<Preview>({
      namespace: "preview-preview"
    });

    if (restorer) {
      restorer.restore(tracker, {
        command: "docmanager:open",
        args: panel => ({
          path: panel.context.path,
          factory: previewFactory.name
        }),
        name: panel => panel.context.path,
        when: app.serviceManager.ready
      });
    }

    function getCurrent(args: ReadonlyJSONObject): NotebookPanel | null {
      const widget = notebookTracker.currentWidget;
      const activate = args["activate"] !== false;
      if (activate && widget) {
        app.shell.activateById(widget.id);
      }
      return widget;
    }

    function isEnabled(): boolean {
      return (
        notebookTracker.currentWidget !== null &&
        notebookTracker.currentWidget === app.shell.currentWidget
      );
    }

    function getPreviewUrl(path: string): string {
//      const baseUrl = PageConfig.getBaseUrl();
//      return `${baseUrl}preview/render/${path}`;
      return "/"
    }

    const previewFactory = new PreviewFactory(getPreviewUrl, {
      name: "preview",
      fileTypes: ["notebook"],
      modelName: "notebook"
    });

    previewFactory.widgetCreated.connect((sender, widget) => {
      // Notify the widget tracker if restore data needs to update.
      widget.context.pathChanged.connect(() => {
        void tracker.save(widget);
      });
      // Add the notebook panel to the tracker.
      void tracker.add(widget);
    });

    const updateSettings = (settings: ISettingRegistry.ISettings): void => {
      previewFactory.defaultRenderOnSave = settings.get("renderOnSave")
        .composite as boolean;
    };

    if (settingRegistry) {
      Promise.all([settingRegistry.load(preview.id), app.restored])
        .then(([settings]) => {
          updateSettings(settings);
          settings.changed.connect(updateSettings);    
        })
        .catch((reason: Error) => {
          console.error(reason.message);
        });
    }

    app.docRegistry.addWidgetFactory(previewFactory);

    commands.addCommand(CommandIDs.previewRender, {
      label: "Render Notebook with Preview",
      execute: async args => {
        const current = getCurrent(args);
        let context: DocumentRegistry.IContext<INotebookModel>;
        if (current) {
          context = current.context;
          await context.save();
          commands.execute("docmanager:open", {
            path: context.path,
            factory: "preview",
            options: {
              mode: "split-right"
            }
          });
        }
      },
      isEnabled
    });

    commands.addCommand(CommandIDs.previewOpen, {
      label: "Open with Preview in New Browser Tab",
      execute: async args => {
        const current = getCurrent(args);
        if (!current) {
          return;
        }
        await current.context.save();
        const previewUrl = getPreviewUrl(current.context.path);
        window.open(previewUrl);
      },
      isEnabled
    });

    if (palette) {
      const category = "Notebook Operations";
      [CommandIDs.previewRender, CommandIDs.previewOpen].forEach(command => {
        palette.addItem({ command, category });
      });
    }

    if (menu) {
      menu.viewMenu.addGroup(
        [
          {
            command: CommandIDs.previewRender
          },
          {
            command: CommandIDs.previewOpen
          }
        ],
        1000
      );
    }

    const previewButton = new PreviewRenderButton(commands);

    docRegistry.addWidgetExtension("Notebook", previewButton);

    return tracker;

  }

};

export default preview;
