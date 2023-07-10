import React from 'react';

import './Logo.css';

import Title from '../Title/Title';
import MainLogo from '../../../assets/images/ufal.png';

function Logo() {
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <img
        src={MainLogo}
        alt="MainLogo"
        width="79px"
        height="100px"
      />
      <Title>Miniusina Solar Fotovoltaca</Title>
    </div>
  );
}

export default Logo;
