import React from 'react';
import PropTypes from 'prop-types';

import './Button.css';

function Button(props) {
  const { children, onClick } = props;

  return <button type="button" className="Button_button-Button" onClick={onClick}>{children}</button>;
}

Button.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.object,
  ]).isRequired,
  onClick: PropTypes.func.isRequired,
};

export default Button;
