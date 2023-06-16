import React from 'react';
import PropTypes from 'prop-types';

import './SmallButtonFooter.css';

function SmallButtonFooter(props) {
  const { children, onClick } = props;

  return (
    <button className="SmallButtonFooter_button-contanier" type="button" onClick={onClick}>
      {children}
    </button>
  );
}

SmallButtonFooter.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.object,
    PropTypes.number,
  ]).isRequired,
  onClick: PropTypes.func.isRequired,
};

export default SmallButtonFooter;
