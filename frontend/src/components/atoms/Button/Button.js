import React from 'react';
import PropTypes from 'prop-types';

import './Button.css';

function Button(props) {
  const { children, onclick } = props;

  return <button type="button" className="Button_button-Button" onClick={onclick}>{children}</button>;
}

Button.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.object,
  ]).isRequired,
  onclick: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.object,
  ]).isRequired,
};

export default Button;
