import React from 'react';

import './UnderConstruction.css';

import MainLogo from '../../../assets/images/underconstruction.png';

function Logo() {
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <p>Em construção</p>
      <img
        src={MainLogo}
        alt="UnderConstruction"
        width="120px"
        height="120px"
      />
    </div>
  );
}

export default Logo;
