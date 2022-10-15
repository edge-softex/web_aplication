import React from 'react';

// import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
// import { faCircleUser } from '@fortawesome/free-solid-svg-icons';

import MenuElement from '../../atoms/MenuElement/MenuElement';

import { ReactComponent as GraphSVG } from '../../../assets/images/graph.svg';
import { ReactComponent as HistSVG } from '../../../assets/images/historic.svg';
import { ReactComponent as SettingsSVG } from '../../../assets/images/settings.svg';

import './Menu.css';

function Menu() {
  return (
    <div className="menu_div-container">
      <MenuElement
        exact
        link="/dashboard"
        title="Dashboard"
      >
        <GraphSVG
          style={{ height: 25, width: 25 }}
        />
      </MenuElement>
      <MenuElement
        link="/history"
        title="History"
      >
        <HistSVG
          style={{ height: 25, width: 25 }}
        />
      </MenuElement>
      <MenuElement
        link="/settings"
        title="Settings"
      >
        <SettingsSVG
          style={{ height: 25, width: 25 }}
        />
      </MenuElement>
    </div>
  );
}

export default Menu;
