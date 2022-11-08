import React from 'react';
import PropTypes from 'prop-types';

import Navigation from '../../components/Organism/Navigation/Navigation';
import Menu from '../../components/Organism/Menu/Menu';

import './Layout.css';

function Layout(props) {
  const { children } = props;

  return (
    <div className="main-page_layout">
      <Navigation />
      <div className="main-page_layout-body">
        <Menu />
        {children}
      </div>
    </div>
  );
}

Layout.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.object,
  ]).isRequired,
};

export default Layout;
