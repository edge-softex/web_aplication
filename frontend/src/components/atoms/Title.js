import React from 'react';
import PropTypes from 'prop-types';

function Title(props) {
  const { children } = props;

  return <p>{children}</p>;
}

Title.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.object,
  ]).isRequired,
};

export default Title;
