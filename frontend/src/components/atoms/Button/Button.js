import React from 'react';
import PropTypes from 'prop-types';

import './Button.css';

function Button(props) {
  const { children } = props;

  return <button type="button" className="Button_button-Button">{children}</button>;
}

Button.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.object,
  ]).isRequired,
};

export default Button;
