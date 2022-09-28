import React from 'react';
import PropTypes from 'prop-types';

import './Title.css';

function Title(props) {
  const { children } = props;

  return <h1 className="title_h1">{children}</h1>;
}

Title.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.object,
  ]).isRequired,
};

export default Title;
