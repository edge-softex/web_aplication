import React from 'react';
import PropTypes from 'prop-types';

import LisOfSmallButtonsFooter from '../../Molecules/ListOfSmallButtonsFooter/LisOfSmallButtonsFooter';
import DropDown from '../../atoms/DropDown/DropDown';

import './FooterHistoric.css';

function FooterHistoric(props) {
  const { pages, setPage } = props;

  const list = [];
  for (let i = 1; i <= pages; i += 1) {
    list.push(i);
  }

  // setPage(1);

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
      <LisOfSmallButtonsFooter list={list} setPage={setPage} />
    </div>
  );
}

FooterHistoric.propTypes = {
  setPage: PropTypes.func.isRequired,
  pages: PropTypes.number.isRequired,
};

export default FooterHistoric;
