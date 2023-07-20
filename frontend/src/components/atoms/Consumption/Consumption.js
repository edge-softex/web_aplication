import React from 'react';
import PropTypes from 'prop-types';

import './Consumption.css';

function Consumption(props) {
  const { children, type, unity } = props;

  return (
    <div className="consumption_div-container">
      <h3 className={`consumption_h2 ${type}`}>{`${children} ${unity}`}</h3>
      <h3 className="consumption_h3-type">{type === 'current' ? 'Medição' : 'Previsão'}</h3>
    </div>
  );
}

Consumption.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.object,
  ]).isRequired,
  type: PropTypes.string.isRequired,
  unity: PropTypes.string.isRequired,
};

export default Consumption;
