import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import axios from 'axios';
import { API_URL } from '../../../network';
import getPvData from '../../../store/actions/pvdataDataAction';

import Input from '../../atoms/Input/Input';
import Button from '../../atoms/Button/Button';
import DropDown from '../../atoms/DropDown/DropDown';
import './SearchCard.css';
import { ReactComponent as CloudSVG } from '../../../assets/images/cloud.svg';
// import { ReactComponent as SearchSVG } from '../../../assets/images/search.svg';

const fileDownload = require('js-file-download');

function downloadFile() {
  axios({
    url: `${API_URL}/pvdata/downloadhistory/`,
    method: 'GET',
    responseType: 'blob',
  }).then((response) => {
    fileDownload(response.data, 'pvdata.csv');
  });
}

function SearchCard() {
  const pvData = useSelector((state) => state.pvdataHistory.pvData);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(getPvData());
  }, []);

  // useEffect(() => {
  //   const interval = setInterval(() => {
  //     dispatch(getPvData());
  //     console.log(pvData);
  //   }, 5000);
  //   return () => clearInterval(interval);
  // }, []);

  const rows = [];
  for (let i = 0; i < pvData.timestamp.length; i += 1) {
    rows.push(
      <div className="list_div-element">
        <div className="element_div-content">{pvData.timestamp[i]}</div>
        <div className="element_div-content">{pvData.temperature_pv[i]}</div>
        <div className="element_div-content">{pvData.temperature_amb[i]}</div>
        <div className="element_div-content">{pvData.irradiance[i]}</div>
        <div className="element_div-content">{pvData.power_avg[i]}</div>
      </div>,
    );
  }

  return (
    <div className="searchcard_div-container">
      <div className="head_div">
        <div className="head_div-left">
          <DropDown
            options={[
              { value: 'teste1', name: 'nome1' },
              { value: 'teste2', name: 'nome2' },
              { value: 'teste3', name: 'nome3' },
            ]}
            width="100%"
            height={48}
            title="Escolher Tabela"
          />
        </div>
        <div className="head_div-right">
          <Input
            title="Data e hora inicial"
            width="30%"
            type="date"
          />
          <Input
            title="Data e hora final"
            width="30%"
            type="date"
          />
          <Button
            onclick={() => downloadFile()}
          >
            {' '}
            <CloudSVG />
            {' '}
            Download CSV
          </Button>
        </div>
      </div>
      <div className="searchcard_div-body">
        <div className="list_div-container">
          <div className="listtitle_div-element">
            <div className="elementtitle_div-content">
              <p>Timestamp</p>
            </div>
            <div className="elementtitle_div-content">
              <p>PV Temperature</p>
            </div>
            <div className="elementtitle_div-content">
              <p>Ambient temperature</p>
            </div>
            <div className="elementtitle_div-content">
              <p>Irrandiance</p>
            </div>
            <div className="elementtitle_div-content">
              <p>Power avr</p>
            </div>
          </div>
          {rows}
        </div>
      </div>
    </div>
  );
}

export default SearchCard;
