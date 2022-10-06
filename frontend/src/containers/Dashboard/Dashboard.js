import React from 'react';

import Title from '../../components/atoms/Title/Title';
import Card from '../../components/Molecules/NavigationItems/Card/Card';

import './Dashboard.css';

function Dashboard() {
  return (
    <div className="dashboard-div">
      <div className="title_div-container">
        <Title>Dashboard</Title>
      </div>
      <Card>
        <h1>Teste</h1>
      </Card>
    </div>
  );
}

export default Dashboard;
