import React from 'react';

import LisOfSmallButtonsFooter from '../../Molecules/ListOfSmallButtonsFooter/LisOfSmallButtonsFooter';
import DropDown from '../../atoms/DropDown/DropDown';

import './FooterHistoric.css';

function FooterHistoric() {
  return (
    <div className="FooterHistoric_div-container">
      <div className="FooterHistoric_div-rightContent">
        <DropDown
          options={[
            { value: 'teste1', name: 'nome1' },
            { value: 'teste2', name: 'nome2' },
            { value: 'teste3', name: 'nome3' },
          ]}
          width="60%"
          height={40}
          title="Escolher Tabela"
        />
        <p className="FooterHistoric_p-rightContent">de 150 registros</p>
      </div>
      <LisOfSmallButtonsFooter list={[1, 2, 3, 4, 5]} />
    </div>
  );
}

export default FooterHistoric;
