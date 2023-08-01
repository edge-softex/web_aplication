import React from 'react';
import PropTypes from 'prop-types';

import axios from 'axios';
import { API_URL } from '../../../network';

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

const downloadUrl = `${API_URL}/pvdata/downloadhistory/`;
let downloadUrlFilter = downloadUrl;

function downloadFile() {
  axios({
    url: downloadUrlFilter,
    method: 'GET',
    responseType: 'blob',
  }).then((response) => {
    fileDownload(response.data, 'pvdata.csv');
  });
}

function SearchCard(props) {
  const {
    pvData,
    onBeginTimeChange,
    onEndTimeChange,
    setPage,
  } = props;
  const rows = [];
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

  return (
    <div className="searchcard_div-container">
      <div className="head_div">
        <div className="head_div-left">
          <DropDown
            options={[
              { value: 'pvdata', name: 'Dados monitorados' },
              { value: 'forecast', name: 'Previsão de geração' },
            ]}
            width="100%"
            height={48}
            title="Escolher Tabela"
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
              onBeginTimeChange(`${e.target.value}.0-03:00`);
              setPage(1);
              defaultInitDate = e.target.value;
              downloadUrlFilter = `${downloadUrl}?time_begin=${defaultInitDate}.0-03:00&time_end=${defaultEndDate}.0-03:00`;
            }}
          />
          <Input
            title="Data e hora finais"
            width="30%"
            type="datetime-local"
            placeholder="Data e hora finais"
            value={defaultEndDate}
            onChange={(e) => {
              onEndTimeChange(`${e.target.value}.0-03:00`);
              setPage(1);
              defaultEndDate = e.target.value;
              downloadUrlFilter = `${downloadUrl}?time_begin=${defaultInitDate}.0-03:00&time_end=${defaultEndDate}.0-03:00`;
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
          </div>
          {rows}
        </div>
      </div>
    </div>
  );
}

SearchCard.propTypes = {
  pvData: PropTypes.shape({
    pages: PropTypes.number,
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
  onBeginTimeChange: PropTypes.func.isRequired,
  onEndTimeChange: PropTypes.func.isRequired,
  setPage: PropTypes.func.isRequired,
};

export default SearchCard;
