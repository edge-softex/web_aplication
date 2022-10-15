import React from 'react';
import PropTypes from 'prop-types';

import './CardTitle.css';

function CardTitle(props) {
  const { children } = props;

  return (
    <h2 className="cardTitle_h2">{children}</h2>
  );
}

CardTitle.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.object,
  ]).isRequired,
};

export default CardTitle;
