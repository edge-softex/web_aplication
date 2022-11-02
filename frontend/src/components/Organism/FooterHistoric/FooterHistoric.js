import React from 'react';

import LisOfSmallButtonsFooter from '../../Molecules/ListOfSmallButtonsFooter/LisOfSmallButtonsFooter';

import './FooterHistoric.css';

function FooterHistoric() {
  return (
    <div className="FooterHistoric_div-container">
      <LisOfSmallButtonsFooter list={[1, 2, 3, 4, 5]} />
    </div>
  );
}

export default FooterHistoric;
