import React from 'react';
import PropTypes from 'prop-types';

import './Card.css';

function Card(props) {
  const { children } = props;

  return (
    <div className="card_div-container">
      {children}
    </div>
  );
}

Card.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.object,
  ]).isRequired,
};

export default Card;
