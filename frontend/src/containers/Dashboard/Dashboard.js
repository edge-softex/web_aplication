import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import getPowerData from '../../store/actions/powerDataAction';
import getYieldData from '../../store/actions/yieldDataAction';
import getMeteorologicalData from '../../store/actions/meteorologicalDataAction';
import getHistoryData from '../../store/actions/historyDataAction';

import Title from '../../components/atoms/Title/Title';
import Card from '../../components/Molecules/Card/Card';
import LineChart from '../../components/atoms/LineChart/LineChart';
import BarChart from '../../components/atoms/BarChart/BarChart';
import HalfDoughnutChart from '../../components/atoms/halfDoughnutChart/HalfDoughnutChart';

import './Dashboard.css';

function Dashboard() {
  const powerData = useSelector((state) => state.power.powerData);
  const yieldData = useSelector((state) => state.yield.yieldData);
  const meteorologicalData = useSelector((state) => state.meteorological.meteorologicalData);
  const historyData = useSelector((state) => state.history.historyData);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(getPowerData());
    dispatch(getYieldData());
    dispatch(getMeteorologicalData());
    dispatch(getHistoryData());
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      dispatch(getPowerData());
      dispatch(getYieldData());
      dispatch(getMeteorologicalData());
      dispatch(getHistoryData());
    }, 5000);
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
          unity="Wh"
          showForecast={false}
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
          showData={false}
          showForecast={false}
        >
          <BarChart
            timestamp={historyData.timestamp}
            data={historyData.data}
          />
        </Card>
        <Card
          minWidth={604}
          width="57%"
          height={439}
          title="Instant Power"
          data={powerData.data[powerData.data.length - 6]}
          forecast={powerData.forecast[powerData.forecast.length - 6]}
          unity="W"
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
          unit="VA"
          showData={false}
          showForecast={false}
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
          data={meteorologicalData.irradiance[meteorologicalData.irradiance.length - 1]}
          unity="W/m²"
          showForecast={false}
        >
          <LineChart
            timestamp={meteorologicalData.timestamp}
            data={meteorologicalData.irradiance}
            forecast={[]}
          />
        </Card>
        <Card
          minWidth={400}
          width="27.5%"
          height={439}
          title="Pv cell temperature"
          data={meteorologicalData.temperature_pv[meteorologicalData.temperature_pv.length - 1]}
          unity="℃"
          showForecast={false}
        >
          <HalfDoughnutChart />
        </Card>
        <Card
          minWidth={400}
          width="27.5%"
          height={439}
          title="Abient temperature"
          data={meteorologicalData.temperature_amb[meteorologicalData.temperature_amb.length - 1]}
          unity="℃"
          showForecast={false}
        >
          <HalfDoughnutChart />
        </Card>
      </div>
    </div>
  );
}

export default Dashboard;
