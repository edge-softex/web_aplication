import React from 'react';
import PropTypes from 'prop-types';

import CardTitle from '../../atoms/CardTitle/CardTitle';
import Consumption from '../../atoms/Consumption/Consumption';

import './Card.css';

function Card(props) {
  const {
    children,
    minWidth,
    width,
    height,
    title,
    data,
    forecast,
  } = props;

  return (
    <div
      className="card_div-container"
      style={{
        minWidth,
        width,
        height,
      }}
    >
      <div className="card_div-head">
        <div className="card_div-title">
          <CardTitle>{title}</CardTitle>
        </div>
        <div className="card_div-consumption">
          <Consumption type="current">{data.toFixed(2)}</Consumption>
          <Consumption type="forecast">{forecast.toFixed(2)}</Consumption>
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
  minWidth: PropTypes.number.isRequired,
  width: PropTypes.oneOfType([
    PropTypes.number,
    PropTypes.string,
  ]).isRequired,
  height: PropTypes.number.isRequired,
  title: PropTypes.string.isRequired,
  data: PropTypes.number.isRequired,
  forecast: PropTypes.number.isRequired,
};

export default Card;
