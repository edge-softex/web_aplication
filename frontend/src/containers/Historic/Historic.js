import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import getPvData from '../../store/actions/pvdataDataAction';
import getForecast from '../../store/actions/forecastDataAction';

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
  const [pages, setPages] = useState(1);
  const [elements, setElements] = useState(1);
  const [dataset, setDataset] = useState(1);
  const [table, setTable] = useState('pvdata');
  const pvData = useSelector((state) => state.pvdataHistory.pvData);
  const forecast = useSelector((state) => state.forecastHistory.forecast);

  useEffect(() => {
    if (table === 'pvdata') {
      dispatch(getPvData(actualPage, beginTime, endTime));
    } else if ((table === 'forecast')) {
      dispatch(getForecast(actualPage, beginTime, endTime));
    }
  }, [actualPage, beginTime, endTime, table]);

  useEffect(() => {
    if (table === 'pvdata') {
      setPages(pvData.pages);
      setElements(pvData.timestamp.length);
      setDataset(pvData.dataset);
    } else if ((table === 'forecast')) {
      setPages(forecast.pages);
      setElements(forecast.timestamp.length);
      setDataset(forecast.dataset);
    }
  }, [pvData, forecast, table]);

  return (
    <div className="historic-div">
      <div className="title_div-container">
        <Title>Histórico de Dados</Title>
      </div>
      <SearchCard
        pvData={pvData}
        forecast={forecast}
        onBeginTimeChange={setBeginTime}
        onEndTimeChange={setEndTime}
        setPage={setActualPage}
        changeTable={setTable}
      />
      <FooterHistoric
        setPage={setActualPage}
        pages={pages}
        historyPage={actualPage}
        elements={elements}
        dataset={dataset}
      />
    </div>
  );
}

export default Historic;
