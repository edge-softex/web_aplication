import React from 'react';

import './Logo.css';

import { ReactComponent as MainLogo } from '../../../assets/images/logo.svg';

function Logo() {
  return (
    <div>
      <MainLogo
        style={{ height: 46.6, width: 64 }}
      />
    </div>
  );
}

export default Logo;
