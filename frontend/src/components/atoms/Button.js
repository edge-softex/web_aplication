import React from 'react';
import PropTypes from 'prop-types';

function Button(props) {
  const { children } = props;

  return <button type="button">{children}</button>;
}

Button.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.object,
  ]).isRequired,
};

export default Button;
