import React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { INotebookTracker, NotebookPanel, NotebookActions } from '@jupyterlab/notebook';
import { ICellFooter, Cell } from '@jupyterlab/cells';
import { ReadonlyPartialJSONObject } from '@lumino/coreutils';
import { CommandRegistry } from '@lumino/commands';
import { IEditorServices } from '@jupyterlab/codeeditor';

/**
 * The CSS classes added to the cell footer.
 */
const CELL_FOOTER_CLASS = 'jp-CellFooter';
const CELL_FOOTER_DIV_CLASS = 'ccb-cellFooterContainer';
const CELL_FOOTER_BUTTON_CLASS = 'ccb-cellFooterBtn';

/**
 * Extend default implementation of a cell footer.
 */
export class CellFooterWithButton extends ReactWidget implements ICellFooter {
  private readonly commands: CommandRegistry;
  /**
   * Construct a new cell footer.
   */
  constructor(commands: CommandRegistry) {
    super();
    this.commands = commands;
    this.addClass(CELL_FOOTER_CLASS);
  }
  render() {
    return (
      <div className={CELL_FOOTER_DIV_CLASS}>
        <button
          className={CELL_FOOTER_BUTTON_CLASS}
          onClick={event => {
            this.commands.execute('run-selected-codecell');
          }}
        >
          run
        </button>
      </div>
    );
  }
}

/**
 * Extend the default implementation of an `IContentFactory`.
 */
export class ContentFactoryWithFooterButton extends NotebookPanel.ContentFactory {
  private readonly commands: CommandRegistry;
  constructor(
    commands: CommandRegistry,
    options?: Cell.ContentFactory.IOptions | undefined
  ) {
    super(options);
    this.commands = commands;
  }
  /**
   * Create a new cell header for the parent widget.
   */
  createCellFooter(): ICellFooter {
    return new CellFooterWithButton(this.commands);
  }
}

/**
 * The footer button extension for the code cell.
 */
export const footerButtonExtension: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-cellcodebtn',
  autoStart: true,
  requires: [INotebookTracker],
  activate(
    app: JupyterFrontEnd,
    tracker: INotebookTracker
  ): Promise<void> {
    Promise.all([app.restored]).then(([params]) => {
      const { commands, shell } = app;
      function getCurrent(args: ReadonlyPartialJSONObject): NotebookPanel | null {
        const widget = tracker.currentWidget;
        const activate = args.activate !== false;
        if (activate && widget) {
          shell.activateById(widget.id);
        }
        return widget;
      }
      function isEnabled(): boolean {
        return (
          tracker.currentWidget !== null &&
          tracker.currentWidget === app.shell.currentWidget
        );
      }
      commands.addCommand('run-selected-codecell', {
        label: 'Run Cell',
        execute: args => {
          const current = getCurrent(args);
          if (current) {
            const { context, content } = current;
            NotebookActions.run(content, context.sessionContext);
            // current.content.mode = 'edit';
          }
        },
        isEnabled
      });
    });
    return Promise.resolve();
  }
}

/**
 * The notebook cell factory.
 */
export const cellFactory: JupyterFrontEndPlugin<NotebookPanel.IContentFactory> = {
  id: 'jupyterlab-cellcodebtn:factory',
  requires: [IEditorServices],
  provides: NotebookPanel.IContentFactory,
  autoStart: true,
  activate: (app: JupyterFrontEnd, editorServices: IEditorServices) => {
    console.log('JupyterLab extension jupyterlab-cellcodebtn overrides default nootebook content factory.');
    const { commands } = app;
    const editorFactory = editorServices.factoryService.newInlineEditor;
    return new ContentFactoryWithFooterButton(commands, { editorFactory });
  }
}

/**
 * Export this plugins as default.
 */
const codeCellButton: Array<JupyterFrontEndPlugin<any>> = [
  footerButtonExtension,
  cellFactory
];

export default codeCellButton;
