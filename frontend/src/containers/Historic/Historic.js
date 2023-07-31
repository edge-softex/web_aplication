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
  const [beginTime, setBeginTime] = useState('');
  const [endTime, setEndTime] = useState('');
  const pvData = useSelector((state) => state.pvdataHistory.pvData);

  useEffect(() => {
    dispatch(getPvData(actualPage, beginTime, endTime));
  }, [actualPage, beginTime, endTime]);

  return (
    <div className="historic-div">
      <div className="title_div-container">
        <Title>Histórico de Dados</Title>
      </div>
      <SearchCard
        pvData={pvData}
        onBeginTimeChange={setBeginTime}
        onEndTimeChange={setEndTime}
        setPage={setActualPage}
      />
      <FooterHistoric
        setPage={setActualPage}
        pages={pvData.pages}
        historyPage={actualPage}
      />
    </div>
  );
}

export default Historic;
