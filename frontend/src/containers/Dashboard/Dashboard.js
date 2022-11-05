import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import { getPowerData } from '../../store/actions/powerDataAction';

import Title from '../../components/atoms/Title/Title';
import Card from '../../components/Molecules/Card/Card';
import LineChart from '../../components/atoms/LineChart/LineChart';
import BarChart from '../../components/atoms/BarChart/BarChart';
import HalfDoughnutChart from '../../components/atoms/halfDoughnutChart/HalfDoughnutChart';

import './Dashboard.css';

function Dashboard() {
  const powerData = useSelector((state) => state.power.powerData);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(getPowerData());
  }, []);

  console.log(powerData);

  return (
    <div className="dashboard-div">
      <div className="title_div-container">
        <Title>Dashboard</Title>
      </div>
      <div className="cards_div-container">
        <Card
          minWidth={400}
          width="35%"
          height={439}
          title="Yield Today"
        >
          <LineChart />
        </Card>
        <Card
          minWidth={604}
          width="57%"
          height={439}
          title="Yield History"
        >
          <BarChart />
        </Card>
        <Card
          minWidth={604}
          width="57%"
          height={439}
          title="Instant Power"
        >
          <LineChart powerData/>
        </Card>
        <Card
          minWidth={400}
          width="35%"
          height={439}
          title="Yield Today"
        >
          <LineChart />
        </Card>
        <Card
          minWidth={400}
          width="35%"
          height={439}
          title="Yield Today"
        >
          <LineChart />
        </Card>
        <Card
          minWidth={400}
          width="35%"
          height={439}
          title="Yield Today"
        >
          <HalfDoughnutChart />
        </Card>
        <Card
          minWidth={400}
          width="35%"
          height={439}
          title="Yield Today"
        >
          <HalfDoughnutChart />
        </Card>
      </div>
    </div>
  );
}

export default Dashboard;
