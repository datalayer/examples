import {
  IFrame,
  ToolbarButton,
  ReactWidget,
  IWidgetTracker
} from "@jupyterlab/apputils";

import {
  ABCWidgetFactory,
  DocumentRegistry,
  DocumentWidget
} from "@jupyterlab/docregistry";

import { INotebookModel } from "@jupyterlab/notebook";

import { Token } from "@lumino/coreutils";

import { Signal } from "@lumino/signaling";

import React from "react";

/**
 * A class that tracks Preview widgets.
 */
export interface IPreviewTracker extends IWidgetTracker<Preview> {}

/**
 * The Preview tracker token.
 */
export const IPreviewTracker = new Token<IPreviewTracker>(
  "jupyterlabextensions:IPreviewTracker"
);

/**
 * The class name for a preview icon.
 */
export const PREVIEW_ICON_CLASS = "jp-MaterialIcon jp-PreviewIcon";

/**
 * A DocumentWidget that shows a preview in an IFrame.
 */
export class Preview extends DocumentWidget<IFrame, INotebookModel> {
  private _renderOnSave: boolean;

  /**
   * Instantiate a new Preview.
   * @param options The Preview instantiation options.
   */
  constructor(options: Preview.IOptions) {
    super({
      ...options,
      content: new IFrame({ sandbox: ["allow-same-origin", "allow-scripts"] })
    });

    const { getPreviewUrl, context, renderOnSave } = options;

    window.onmessage = (event: any) => {
      //console.log("EVENT: ", event);
      switch (event.data?.level) {
        case "debug":
          console.debug(...event.data?.msg);
          break;
        case "info":
          console.info(...event.data?.msg);
          break;
        case "warn":
          console.warn(...event.data?.msg);
          break;
        case "error":
          console.error(...event.data?.msg);
          break;
        default:
          console.log(event);
          break;
      }
    };

    this.content.url = getPreviewUrl(context.path);
    this.content.title.icon = PREVIEW_ICON_CLASS;

    this.renderOnSave = renderOnSave;

    context.pathChanged.connect(() => {
      this.content.url = getPreviewUrl(context.path);
    });

    const reloadButton = new ToolbarButton({
      iconClass: "jp-RefreshIcon",
      tooltip: "Reload Preview",
      onClick: () => {
        this.reload();
      }
    });

    const renderOnSaveCheckbox = ReactWidget.create(
      <label className="jp-Preview-renderOnSave">
        <input
          style={{ verticalAlign: "middle" }}
          name="renderOnSave"
          type="checkbox"
          defaultChecked={renderOnSave}
          onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
            this._renderOnSave = event.target.checked;
          }}
        />
        Render on Save
      </label>
    );

    this.toolbar.addItem("reload", reloadButton);

    if (context) {
      this.toolbar.addItem("renderOnSave", renderOnSaveCheckbox);
      void context.ready.then(() => {
        context.fileChanged.connect(() => {
          if (this.renderOnSave) {
            this.reload();
          }
        });
      });
    }

  }

  /**
   * Dispose the preview widget.
   */
  dispose() {
    if (this.isDisposed) {
      return;
    }
    super.dispose();
    Signal.clearData(this);
  }

  /**
   * Reload the preview.
   */
  reload() {
    const iframe = this.content.node.querySelector("iframe")!;
    if (iframe.contentWindow) {
      iframe.contentWindow.location.reload();
    }
  }

  /**
   * Get whether the preview reloads when the context is saved.
   */
  get renderOnSave(): boolean {
    return this._renderOnSave;
  }

  /**
   * Set whether the preview reloads when the context is saved.
   */
  set renderOnSave(renderOnSave: boolean) {
    this._renderOnSave = renderOnSave;
  }

}

/**
 * A namespace for Preview statics.
 */
export namespace Preview {
  /**
   * Instantiation options for `Preview`.
   */
  export interface IOptions
    extends DocumentWidget.IOptionsOptionalContent<IFrame, INotebookModel> {
    /**
     * The Preview URL function.
     */
    getPreviewUrl: (path: string) => string;

    /**
     * Whether to reload the preview on context saved.
     */
    renderOnSave?: boolean;
  }
}

export class PreviewFactory extends ABCWidgetFactory<Preview, INotebookModel> {
  public defaultRenderOnSave: boolean = false;

  constructor(
    private getPreviewUrl: (path: string) => string,
    options: DocumentRegistry.IWidgetFactoryOptions<Preview>
  ) {
    super(options);
  }

  protected createNewWidget(
    context: DocumentRegistry.IContext<INotebookModel>
  ): Preview {
    return new Preview({
      context,
      getPreviewUrl: this.getPreviewUrl,
      renderOnSave: this.defaultRenderOnSave
    });
  }

}
