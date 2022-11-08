import React from 'react';

import SystemStatus from '../../atoms/SystemStatus/SystemStatus';
import UserAvatar from '../../atoms/userAvatar/UserAvatar';

import './NavigationItems.css';

function NavigationItems() {
  return (
    <ul className="nav_list">
      <li>
        <SystemStatus status="fault" />
      </li>
      <li>
        <UserAvatar name="Vinicius Feitosa" />
      </li>
    </ul>
  );
}

export default NavigationItems;
