import React from 'react';

import NavigationItems from '../../Molecules/NavigationItems/NavigationItems';
import Logo from '../../atoms/Logo/Logo';
import './Navigation.css';

function Navigation() {
  return (
    <nav className="main_nav">
      <Logo />
      <NavigationItems />
    </nav>
  );
}

export default Navigation;
