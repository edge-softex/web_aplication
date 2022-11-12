import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import getPowerData from '../../store/actions/powerDataAction';
import getYieldData from '../../store/actions/yieldDataAction';

import Title from '../../components/atoms/Title/Title';
import Card from '../../components/Molecules/Card/Card';
import LineChart from '../../components/atoms/LineChart/LineChart';
import BarChart from '../../components/atoms/BarChart/BarChart';
import HalfDoughnutChart from '../../components/atoms/halfDoughnutChart/HalfDoughnutChart';

import './Dashboard.css';

function Dashboard() {
  const powerData = useSelector((state) => state.power.powerData);
  const yieldData = useSelector((state) => state.yield.yieldData);
  const dispatch = useDispatch();

  // useEffect(() => {
  //   dispatch(getPowerData());
  // }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      dispatch(getPowerData());
      dispatch(getYieldData());
    }, 1000);
    return () => clearInterval(interval);
  }, []);

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
          data={yieldData.data[yieldData.data.length - 1]}
          forecast={0}
        >
          <LineChart
            timestamp={yieldData.timestamp}
            data={yieldData.data}
            forecast={[]}
          />
        </Card>
        <Card
          minWidth={604}
          width="57%"
          height={439}
          title="Yield History"
          data={0}
          forecast={0}
        >
          <BarChart />
        </Card>
        <Card
          minWidth={604}
          width="57%"
          height={439}
          title="Instant Power"
          data={powerData.data[powerData.data.length - 1]}
          forecast={powerData.forecast[powerData.forecast.length - 6]}
        >
          <LineChart
            timestamp={powerData.timestamp}
            data={powerData.data}
            forecast={powerData.forecast}
          />
        </Card>
        <Card
          minWidth={400}
          width="35%"
          height={439}
          title="Strings"
          data={0}
          forecast={0}
        >
          <LineChart
            timestamp={[]}
            data={[]}
            forecast={[]}
          />
        </Card>
        <Card
          minWidth={400}
          width="35%"
          height={439}
          title="Irradiance"
          data={0}
          forecast={0}
        >
          <LineChart
            timestamp={[]}
            data={[]}
            forecast={[]}
          />
        </Card>
        <Card
          minWidth={400}
          width="35%"
          height={439}
          title="Pv cell temperature"
          data={0}
          forecast={0}
        >
          <HalfDoughnutChart />
        </Card>
        <Card
          minWidth={400}
          width="35%"
          height={439}
          title="Abient temperature"
          data={0}
          forecast={0}
        >
          <HalfDoughnutChart />
        </Card>
      </div>
    </div>
  );
}

export default Dashboard;
