import React from 'react';
import PropTypes from 'prop-types';

import './Consumption.css';

function Consumption(props) {
  const { children, type } = props;

  return (
    <div className="consumption_div-container">
      <h2 className={`consumption_h2 ${type}`}>{`${children} Wh`}</h2>
      <h3 className="consumption_h3-type">{type === 'current' ? 'Current consumption' : 'Current forecast'}</h3>
    </div>
  );
}

Consumption.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.object,
  ]).isRequired,
  type: PropTypes.string.isRequired,
};

export default Consumption;
