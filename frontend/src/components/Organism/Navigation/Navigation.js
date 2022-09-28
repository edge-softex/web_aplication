import React from 'react';

import NavigationItems from '../../Molecules/NavigationItems/NavigationItems';
import './Navigation.css';

const navigation = (props) => (
  <nav className="main_nav">
    <h1>Logo</h1>
    <NavigationItems />
  </nav>
);

export default navigation;
