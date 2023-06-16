import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import getPvData from '../../store/actions/pvdataDataAction';

import Title from '../../components/atoms/Title/Title';
import SearchCard from '../../components/Molecules/SearchCard/SearchCard';
// import DropDown from '../../components/atoms/DropDown/DropDown';
import FooterHistoric from '../../components/Organism/FooterHistoric/FooterHistoric';

import './Historic.css';

function Historic() {
  const dispatch = useDispatch();
  const [actualPage, setActualPage] = useState(1);
  const pvData = useSelector((state) => state.pvdataHistory.pvData);

  useEffect(() => {
    dispatch(getPvData(actualPage));
  }, [actualPage]);

  return (
    <div className="historic-div">
      <div className="title_div-container">
        <Title>History</Title>
      </div>
      <SearchCard pvData={pvData} />
      <FooterHistoric
        setPage={setActualPage}
        pages={pvData.pages}
      />
    </div>
  );
}

export default Historic;
