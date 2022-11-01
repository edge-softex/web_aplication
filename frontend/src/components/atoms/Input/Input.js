import React from 'react';
import PropTypes from 'prop-types';

import './Input.css';

function Input(props) {
  const {
    value, onChange, type, placeholder, title, width,
  } = props;

  return (
    <div style={{
      width,
    }}
    >
      <h3 className="h3_title-input">{title}</h3>
      <input
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="text_input"
      />
    </div>
  );
}

Input.defaultProps = {
  type: 'text',
  title: '',
};

Input.propTypes = {
  value: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  type: PropTypes.string,
  placeholder: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.object,
  ]).isRequired,
  title: PropTypes.string,
  width: PropTypes.oneOfType([
    PropTypes.number,
    PropTypes.string,
  ]).isRequired,
};

export default Input;
