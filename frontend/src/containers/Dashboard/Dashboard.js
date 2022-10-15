import React from 'react';

import Title from '../../components/atoms/Title/Title';
import Card from '../../components/Molecules/NavigationItems/Card/Card';
import LineChart from '../../components/atoms/LineChart/LineChart';

import './Dashboard.css';

function Dashboard() {
  return (
    <div className="dashboard-div">
      <div className="title_div-container">
        <Title>Dashboard</Title>
      </div>
      <div className="cards_div-container">
        <Card
          width={470}
          height={439}
          title="Yield Today"
        >
          <LineChart />
        </Card>
        <Card
          width={470}
          height={439}
          title="Yield Today"
        >
          <LineChart />
        </Card>
        <Card
          width={470}
          height={439}
          title="Yield Today"
        >
          <LineChart />
        </Card>
        <Card
          width={470}
          height={439}
          title="Yield Today"
        >
          <LineChart />
        </Card>
        <Card
          width={470}
          height={439}
          title="Yield Today"
        >
          <LineChart />
        </Card>
      </div>
    </div>
  );
}

export default Dashboard;
