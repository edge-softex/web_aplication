import React from 'react';
import PropTypes from 'prop-types';

import './SystemStatus.css';

function SystemStatus(props) {
  const { status } = props;

  return (
    <div className="systemstatus_div-container">
      <div className="systemstatus_div-content">
        <div className={`systemstatus_div-ball ${status.trim()}`}> </div>
        <h3 className="systemstatus_h3">Fault</h3>
      </div>
      <div className="systemstatus_div-title">
        <p className="systemstatus_p-title">Status system</p>
      </div>
    </div>
  );
}

SystemStatus.defaultProps = {
  status: 'normaloperation',
};

SystemStatus.propTypes = {
  status: PropTypes.string,
};

export default SystemStatus;
