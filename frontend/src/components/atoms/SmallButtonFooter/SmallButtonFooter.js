import React from 'react';
import PropTypes from 'prop-types';

import './SmallButtonFooter.css';

function SmallButtonFooter(props) {
  const { children } = props;

  return (
    <button className="SmallButtonFooter_button-contanier" type="button">
      <p className="SmallButtonFooter_p-content">
        {children}
      </p>
    </button>
  );
}

SmallButtonFooter.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.object,
  ]).isRequired,
};

export default SmallButtonFooter;
