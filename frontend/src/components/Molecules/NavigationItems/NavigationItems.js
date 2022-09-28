import React from 'react';

import './NavigationItems.css';

const navigationItems = (props) => {
  let navItems = (
    <ul className="nav_list">
      <li>
        <p>
          Home
        </p>
      </li>
      <li>
        <p>Fault</p>
      </li>
      <li>
        <p>Vinicius Feitosa</p>
      </li>
    </ul>
  );

  return navItems;
};

export default navigationItems;
