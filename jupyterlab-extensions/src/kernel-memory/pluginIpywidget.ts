import { Application, IPlugin } from '@lumino/application';
import { Widget } from '@lumino/widgets';
import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';

import * as widgetExports from './ipywidget';

import { MODULE_NAME, MODULE_VERSION } from './version';

import './../../style/system-monitor.css';

/**
 * The ipyresuse plugin.
 */
const ipyresusePlugin: IPlugin<Application<Widget>, void> = {
  id: 'jupyterlabextensions:ipywidget:kernelmemory',
  requires: [IJupyterWidgetRegistry],
  activate: activateWidgetExtension,
  autoStart: true
};

/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app: Application<Widget>, registry: IJupyterWidgetRegistry): void {
  registry.registerWidget({
    name: MODULE_NAME,
    version: MODULE_VERSION,
    exports: widgetExports,
  });
}

export default ipyresusePlugin;
