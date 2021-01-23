import { ReactWidget } from '@jupyterlab/apputils';

import React, { useState } from 'react';

import { getRandomInt } from './utils';

/**
 * React component for a counter.
 *
 * @returns The React component
 */
const CounterComponent = (props: {animate: boolean}): JSX.Element => {
  const [counter, setCounter] = useState(0);
  const [increment, setIncrement] = useState(0);
  increment
  const doIncrement = () => {
    const inc = getRandomInt(10000);
    setIncrement(inc);
    setCounter(counter + inc);
  }
  return (
    <div>
      {
        <div>
          <p>You earned {counter}!</p>
          <button
            onClick={() => { doIncrement() }}
          >
            Increment
          </button>
        </div>
      }
    </div>
  );
}

/**
 * A React Counter Widget that wraps a CounterComponent.
 */
class ReactCounter extends ReactWidget {
  private animate: boolean;
  /**
   * Constructs a new CounterWidget.
   */
  constructor(animate: boolean) {
    super();
    this.animate = animate;
    this.addClass('jp-Datalayer-React');
  }
  protected render(): JSX.Element {
    return <CounterComponent 
      animate={this.animate}
    />;
  }
}

export default ReactCounter;
