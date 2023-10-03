import React, { useState } from 'react';
import PropTypes from 'prop-types';

import axios from 'axios';
import { API_URL, API_TOKEN } from '../../network';

import Input from '../../atoms/Input/Input';
import Button from '../../atoms/Button/Button';
import DropDown from '../../atoms/DropDown/DropDown';
import './SearchCard.css';
import { ReactComponent as CloudSVG } from '../../../assets/images/cloud.svg';
// import { ReactComponent as SearchSVG } from '../../../assets/images/search.svg';

const fileDownload = require('js-file-download');

let defaultEndDate = new Date();
defaultEndDate.setHours(defaultEndDate.getHours() - 3);
let defaultInitDate = new Date(defaultEndDate.valueOf());
defaultInitDate.setDate(defaultEndDate.getDate() - 1);
[defaultInitDate] = defaultInitDate.toJSON().split('.');
[defaultEndDate] = defaultEndDate.toJSON().split('.');

let downloadUrl = `${API_URL}/pvdata/downloadhistory/`;
let downloadFilter = '';
let fileName = 'pvdata.csv';

const regex = /\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d/g;

function downloadFile() {
  axios({
    url: `${downloadUrl}${downloadFilter}`,
    method: 'GET',
    responseType: 'blob',
    headers: {
      'ngrok-skip-browser-warning': 'true',
      'Bypass-Tunnel-Reminder': 'true',
      Authorization: `Token ${API_TOKEN}`,
    },
  }).then((response) => {
    fileDownload(response.data, fileName);
  });
}

function setDownloadURL(table) {
  if (table === 'pvdata') {
    downloadUrl = `${API_URL}/pvdata/downloadhistory/`;
    fileName = 'pvdata.csv';
  }
  if (table === 'forecast') {
    downloadUrl = `${API_URL}/powerforecast/downloadhistory/`;
    fileName = 'pvforecast.csv';
  }
}

function SearchCard(props) {
  const {
    pvData,
    forecast,
    onBeginTimeChange,
    onEndTimeChange,
    setPage,
    changeTable,
  } = props;
  const [table, setTable] = useState('pvdata');

  const rows = [];

  if (table === 'pvdata') {
    rows.push(
      <div className="listtitle_div-element">
        <div className="elementtitle_div-content">
          <p>Data/Hora</p>
        </div>
        <div className="elementtitle_div-content">
          <p>Temperatura PV</p>
        </div>
        <div className="elementtitle_div-content">
          <p>Temperatura Ambiente</p>
        </div>
        <div className="elementtitle_div-content">
          <p>Irrandiância</p>
        </div>
        <div className="elementtitle_div-content">
          <p>Potência Média</p>
        </div>
      </div>,
    );

    for (let i = 0; i < pvData.timestamp.length; i += 1) {
      rows.push(
        <div className="list_div-element" key={i}>
          <div className="element_div-content">{pvData.timestamp[i]}</div>
          <div className="element_div-content">{pvData.temperature_pv[i]}</div>
          <div className="element_div-content">{pvData.temperature_amb[i]}</div>
          <div className="element_div-content">{pvData.irradiance[i]}</div>
          <div className="element_div-content">{pvData.power_avg[i]}</div>
        </div>,
      );
    }
  } else if (table === 'forecast') {
    rows.push(
      <div className="listtitle_div-element">
        <div className="elementtitle_div-content">
          <p>Data/Hora</p>
        </div>
        <div className="elementtitle_div-content">
          <p>Pot. medida</p>
        </div>
        <div className="elementtitle_div-content">
          <p>Prev. T+1m</p>
        </div>
        <div className="elementtitle_div-content">
          <p>Prev. T+2m</p>
        </div>
        <div className="elementtitle_div-content">
          <p>Prev. T+3m</p>
        </div>
        <div className="elementtitle_div-content">
          <p>Prev. T+4m</p>
        </div>
        <div className="elementtitle_div-content">
          <p>Prev. T+5m</p>
        </div>
      </div>,
    );

    for (let i = 0; i < forecast.timestamp.length; i += 1) {
      rows.push(
        <div className="list_div-element" key={i}>
          <div className="element_div-content">{forecast.timestamp[i]}</div>
          <div className="element_div-content">{forecast.power_avg[i]}</div>
          <div className="element_div-content">{forecast.t1[i]}</div>
          <div className="element_div-content">{forecast.t2[i]}</div>
          <div className="element_div-content">{forecast.t3[i]}</div>
          <div className="element_div-content">{forecast.t4[i]}</div>
          <div className="element_div-content">{forecast.t5[i]}</div>
        </div>,
      );
    }
  }

  return (
    <div className="searchcard_div-container">
      <div className="head_div">
        <div className="head_div-left">
          <DropDown
            options={[
              { value: 'pvdata', name: 'Dados monitorados' },
              { value: 'forecast', name: 'Previsão de geração' },
            ]}
            width="80%"
            height={48}
            title="Escolher Tabela"
            onChange={(e) => {
              setTable(e.target.value);
              changeTable(e.target.value);
              setPage(1);
              setDownloadURL(e.target.value);
            }}
          />
        </div>
        <div className="head_div-right">
          <Input
            title="Data e hora iniciais"
            width="30%"
            type="datetime-local"
            placeholder="Data e Hora iniciais"
            value={defaultInitDate}
            onChange={(e) => {
              defaultInitDate = e.target.value;
              if (e.target.value.match(regex) && (e.target.value.length <= 19)) {
                onBeginTimeChange(`${e.target.value}.0-03:00`);
                setPage(1);
                downloadFilter = `?time_begin=${defaultInitDate}.0-03:00&time_end=${defaultEndDate}.0-03:00`;
              }
            }}
          />
          <Input
            title="Data e hora finais"
            width="30%"
            type="datetime-local"
            placeholder="Data e hora finais"
            value={defaultEndDate}
            onChange={(e) => {
              defaultEndDate = e.target.value;
              if (e.target.value.match(regex) && (e.target.value.length <= 19)) {
                onEndTimeChange(`${e.target.value}.0-03:00`);
                setPage(1);
                downloadFilter = `?time_begin=${defaultInitDate}.0-03:00&time_end=${defaultEndDate}.0-03:00`;
              }
            }}
          />
          <Button
            onClick={() => downloadFile()}
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
          {rows}
        </div>
      </div>
    </div>
  );
}

SearchCard.propTypes = {
  pvData: PropTypes.shape({
    pages: PropTypes.number,
    dataset: PropTypes.number,
    timestamp: PropTypes.arrayOf(PropTypes.string),
    irradiance: PropTypes.arrayOf(PropTypes.number),
    temperature_pv: PropTypes.arrayOf(PropTypes.number),
    temperature_amb: PropTypes.arrayOf(PropTypes.number),
    humidity: PropTypes.arrayOf(PropTypes.number),
    wind_speed: PropTypes.arrayOf(PropTypes.number),
    wind_direction: PropTypes.arrayOf(PropTypes.string),
    rain: PropTypes.arrayOf(PropTypes.number),
    open_circuit_voltage: PropTypes.arrayOf(PropTypes.number),
    short_circuit_current: PropTypes.arrayOf(PropTypes.number),
    power_avg: PropTypes.arrayOf(PropTypes.number),
  }).isRequired,
  forecast: PropTypes.shape({
    pages: PropTypes.number,
    dataset: PropTypes.number,
    timestamp: PropTypes.arrayOf(PropTypes.string),
    power_avg: PropTypes.arrayOf(PropTypes.number),
    t1: PropTypes.arrayOf(PropTypes.number),
    t2: PropTypes.arrayOf(PropTypes.number),
    t3: PropTypes.arrayOf(PropTypes.number),
    t4: PropTypes.arrayOf(PropTypes.number),
    t5: PropTypes.arrayOf(PropTypes.number),
  }).isRequired,
  onBeginTimeChange: PropTypes.func.isRequired,
  onEndTimeChange: PropTypes.func.isRequired,
  setPage: PropTypes.func.isRequired,
  changeTable: PropTypes.func.isRequired,
};

export default SearchCard;
