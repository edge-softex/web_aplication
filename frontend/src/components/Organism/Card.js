import React from 'react';
import PropTypes from 'prop-types';

function Card(props) {
  const { children } = props;

  return (
    <div>
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
