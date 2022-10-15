import React from 'react';
import PropTypes from 'prop-types';

import CardTitle from '../../../atoms/CardTitle/CardTitle';
import Consumption from '../../../atoms/Consumption/Consumption';

import './Card.css';

function Card(props) {
  const {
    children,
    width,
    height,
    title,
  } = props;

  return (
    <div className="card_div-container" style={{ width, height }}>
      <div className="card_div-head">
        <div className="card_div-title">
          <CardTitle>{title}</CardTitle>
        </div>
        <div className="card_div-consumption">
          <Consumption type="current">60</Consumption>
          <Consumption type="forecast">300</Consumption>
        </div>
      </div>
      <div className="card_div-body">
        {children}
      </div>
    </div>
  );
}

Card.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.object,
  ]).isRequired,
  width: PropTypes.number.isRequired,
  height: PropTypes.number.isRequired,
  title: PropTypes.string.isRequired,
};

export default Card;
