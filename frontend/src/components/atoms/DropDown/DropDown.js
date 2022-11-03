import React from 'react';
import PropTypes from 'prop-types';

import './DropDown.css';

function DropDown(props) {
  const {
    options, width, title, height,
  } = props;

  return (
    <div style={{
      width,
    }}
    >
      <h3 className="h3_dropdown-title">{title}</h3>
      <select
        style={{
          height,
        }}
        className="select_dropdown"
      >
        {options.map((option) => (
          <option
            value={option.value}
            className="option_dropdown"
          >
            {option.name}
          </option>
        ))}
      </select>
    </div>
  );
}

DropDown.propTypes = {
  options: PropTypes.arrayOf(PropTypes.shape({
    value: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
  })).isRequired,
  width: PropTypes.oneOfType([
    PropTypes.number,
    PropTypes.string,
  ]).isRequired,
  height: PropTypes.oneOfType([
    PropTypes.number,
    PropTypes.string,
  ]).isRequired,
  title: PropTypes.string.isRequired,
};

export default DropDown;
