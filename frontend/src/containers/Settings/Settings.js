import React from 'react';

import Title from '../../components/atoms/Title/Title';
import Card from '../../components/Molecules/Card/Card';
import UnderConstruction from '../../components/atoms/UnderConstruction/UnderConstruction';

import './Settings.css';

function Settings() {
  return (
    <div className="settings-div">
      <div className="title_div-container">
        <Title>Configurações</Title>
      </div>
      <div className="cards_div-container">
        <Card
          minWidth={400}
          width="35%"
          height={439}
          title="Configurações"
          unit=""
          showData={false}
          showForecast={false}
        >
          <UnderConstruction />
        </Card>
      </div>
    </div>
  );
}

export default Settings;
