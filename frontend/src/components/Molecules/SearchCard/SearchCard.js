import React from 'react';

import Input from '../../atoms/Input/Input';
import './SearchCard.css';

const elements = [
  {
    timestamps: '19/09/2022', pvTemperature: '28 C', AmbientTemp: '30 C', irrandiance: '1000 W/m³', poweravr: '500 w',
  },
  {
    timestamps: '19/09/2022', pvTemperature: '28 C', AmbientTemp: '30 C', irrandiance: '1000 W/m³', poweravr: '500 w',
  },
  {
    timestamps: '19/09/2022', pvTemperature: '28 C', AmbientTemp: '30 C', irrandiance: '1000 W/m³', poweravr: '500 w',
  },
  {
    timestamps: '19/09/2022', pvTemperature: '28 C', AmbientTemp: '30 C', irrandiance: '1000 W/m³', poweravr: '500 w',
  },
];

function SearchCard() {
  return (
    <div className="searchcard_div-container">
      <div className="head_div">
        <Input width="22%" />
        <div className="head_div-right">
          <Input title="Data e hora inicial" width="30%" />
          <Input title="Data e hora final" width="30%" />
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
          {elements.map((element) => (
            <div className="list_div-element">
              <div className="element_div-content">{element.timestamps}</div>
              <div className="element_div-content">{element.pvTemperature}</div>
              <div className="element_div-content">{element.AmbientTemp}</div>
              <div className="element_div-content">{element.irrandiance}</div>
              <div className="element_div-content">{element.poweravr}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default SearchCard;
