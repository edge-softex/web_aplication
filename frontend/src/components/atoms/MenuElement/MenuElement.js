import React from 'react';
import PropTypes from 'prop-types';
import { NavLink } from 'react-router-dom';

import './MenuElement.css';

function MenuElement(props) {
  const { children, link, title } = props;

  return (
    <NavLink
      to={link}
      className="menu-element_div-container"
    >
      {children}
      <p>{title}</p>
    </NavLink>
  );
}

MenuElement.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.object,
  ]).isRequired,
  link: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
};

export default MenuElement;
