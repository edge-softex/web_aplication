import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import PropTypes, { number, string } from 'prop-types';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
);

const options = {
  maintainAspectRatio: false,
  layout: {
    autoPadding: true,
  },
  responsive: true,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        color: '#4F4F4F',
      },
    },
    title: {
      display: false,
    },
    tooltip: {
      mode: 'index',
      intersect: false,
    },
  },
  scales: {
    y: {
      ticks: {
        color: '#4F4F4F',
        font: {
          size: 14,
        },
      },
      grid: {
        color: '#ECECEC',
        lineWidth: 2,
      },
      min: 0,
    },
    x: {
      ticks: {
        color: '#4F4F4F',
        font: {
          size: 14,
        },
        maxTicksLimit: 10,
      },
    },
  },
};

function LineChart(props) {
  const { timestamp, data, forecast } = props;

  let forecastDataSet = {};

  if ({ forecast }.forecast) {
    forecastDataSet = {
      label: 'Forecast',
      data: { forecast }.forecast,
      borderColor: '#F7A159',
      backgroundColor: '#F7A159',
      borderWidth: 2,
    };
  }

  const chartData = {
    labels: { timestamp }.timestamp,
    datasets: [
      {
        label: 'Generated',
        data: { data }.data,
        borderColor: '#173C6C',
        backgroundColor: '#173C6C',
        borderWidth: 2,
      },
      forecastDataSet,
    ],
  };

  return (
    <Line options={options} data={chartData} />
  );
}

LineChart.propTypes = {
  timestamp: PropTypes.arrayOf(string).isRequired,
  data: PropTypes.arrayOf(number).isRequired,
  forecast: PropTypes.arrayOf(number).isRequired,
};

export default LineChart;
