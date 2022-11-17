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
    unity,
    showData,
    showForecast,
  } = props;

  let dataValue = null;
  if (showData) {
    dataValue = <Consumption type="current" unity={unity}>{data.toFixed(2)}</Consumption>;
  }

  let forecastValue = null;
  if (showForecast) {
    forecastValue = <Consumption type="forecast" unity={unity}>{forecast.toFixed(2)}</Consumption>;
  }

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
          { dataValue }
          { forecastValue }
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
  data: PropTypes.number,
  forecast: PropTypes.number,
  unity: PropTypes.string,
  showData: PropTypes.bool,
  showForecast: PropTypes.bool,
};

Card.defaultProps = {
  data: 0,
  forecast: 0,
  unity: 'None',
  showData: true,
  showForecast: true,
};

export default Card;
