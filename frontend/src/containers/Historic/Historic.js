import React from 'react';

import Title from '../../components/atoms/Title/Title';
import SearchCard from '../../components/Molecules/SearchCard/SearchCard';
// import DropDown from '../../components/atoms/DropDown/DropDown';
import FooterHistoric from '../../components/Organism/FooterHistoric/FooterHistoric';

import './Historic.css';

function Historic() {
  return (
    <div className="historic-div">
      <div className="title_div-container">
        <Title>History</Title>
      </div>
      <SearchCard />
      <FooterHistoric />
    </div>
  );
}

export default Historic;
