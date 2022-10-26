import React from 'react';

import Title from '../../components/atoms/Title/Title';
import SearchCard from '../../components/Molecules/SearchCard/SearchCard';
import DropDown from '../../components/atoms/DropDown/DropDown';

import './Historic.css';

function Historic() {
  return (
    <div className="historic-div">
      <div className="title_div-container">
        <Title>History</Title>
      </div>
      <div className="dropdown_div-historic">
        <DropDown
          options={[
            { value: 'teste1', name: 'nome1' },
            { value: 'teste2', name: 'nome2' },
          ]}
          width="35%"
          title="Escolher Tabela"
        />
      </div>
      <SearchCard />
    </div>
  );
}

export default Historic;
