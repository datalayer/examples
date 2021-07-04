import React from 'react';
import { render } from "react-dom";
import { DOMWidgetModel, DOMWidgetView, ISerializers } from "@jupyter-widgets/base";
import { ResourceUsage } from './view/index'
import { MemoryViewComponent } from './view/memoryView'
import { MODULE_NAME, MODULE_VERSION } from "./version";

const DEFAULT_REFRESH_RATE = 2147483646;
const DEFAULT_MEMORY_LABEL = 'Mem: ';
// const DEFAULT_CPU_LABEL = 'CPU: ';
 
export class KernelMemoryUsageModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: KernelMemoryUsageModel.model_name,
      _model_module: KernelMemoryUsageModel.model_module,
      _model_module_version: KernelMemoryUsageModel.model_module_version,
      _view_name: KernelMemoryUsageModel.view_name,
      _view_module: KernelMemoryUsageModel.view_module,
      _view_module_version: KernelMemoryUsageModel.view_module_version,
      _current: 0,
      limit: 0,
      label: "Mem:",
      _percentage: null as any,
      _values: [] as any,
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers
  };

  static model_name = "KernelMemoryUsageModel";
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = "KernelMemoryUsageView"; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

interface IMemoryComponentState {
  label: string;
  text: string;
  values: number[];
  percentage: number | null;
}

class MemoryComponent extends React.Component<{model : any}, IMemoryComponentState> {
  private resourceUsageModel: ResourceUsage.Model;

  constructor(props: any) {
    super(props);
    this.state = {
      label: "",
      text: "",
      values: [],
      percentage: null
    };
    this.resourceUsageModel = new ResourceUsage.Model({ refreshRate: DEFAULT_REFRESH_RATE });
    /*
//    await this.resourceUsageModel.refresh();
    this.resourceUsageModel.refresh();
    */
    /*
    if (this.model.cpuAvailable) {
      const cpu = CpuView.createCpuView(this.model, DEFAULT_CPU_LABEL);
      topBar.addItem('cpu', cpu);
    }
    */
  }

  componentDidMount = () => {
    const { model } = this.props;
    model.on('change', () => {
      this.resourceUsageModel.update(model);  
      this.setState({
        label: model.get('label'),
        text: model.get('_text'),
        values: model.get('_values'),
        percentage: model.get('_percentage'),
      })
    })
  }

  componentWillUnmount = () => {
    const { model } = this.props;
    model.off();
  }

  render() {
    return (
      <>
        <MemoryViewComponent
          model={this.resourceUsageModel}
          label={DEFAULT_MEMORY_LABEL}
          {...this.state}
        />
      </>
    );
  }
}

export class KernelMemoryUsageView extends DOMWidgetView {
  initialize() {
    render(<MemoryComponent model={this.model}/>, this.el)
  }
}
