import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { JSONObject } from '@lumino/coreutils';

import { ITopBar } from '../topbar/topbar';

import { MemoryView, ResourceUsage } from './view'

import './../../style/system-monitor.css';

/**
 * The default refresh rate.
 */
const DEFAULT_REFRESH_RATE = 5000;

/**
 * The default memory label.
 */
const DEFAULT_MEMORY_LABEL = 'Mem: ';

/**
 * An interface for resource settings.
 */
interface IResourceSettings extends JSONObject {
  label: string;
}

/**
 * Initialization data for the jupyterlab-system-monitor extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlabextensions:kernel-memory',
  autoStart: true,
  requires: [ITopBar],
  optional: [ISettingRegistry],
  activate: async (
    app: JupyterFrontEnd,
    topBar: ITopBar,
    settingRegistry: ISettingRegistry
  ) => {
    let refreshRate = DEFAULT_REFRESH_RATE;
    let memoryLabel = DEFAULT_MEMORY_LABEL;

    if (settingRegistry) {
      const settings = await settingRegistry.load(extension.id);
      refreshRate = settings.get('refreshRate').composite as number;
      const memorySettings = settings.get('memory')
        .composite as IResourceSettings;
      memoryLabel = memorySettings.label;
    }
    const model = new ResourceUsage.Model({ refreshRate });
    await model.refresh();
    const memory = MemoryView.createMemoryView(model, memoryLabel);
    topBar.addItem('memory', memory);
  },
};

export default extension;
