import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import PropTypes, { number, string } from 'prop-types';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
);

export const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
    },
    title: {
      display: false,
    },
  },
};

function BarChart(props) {
  const { timestamp, data } = props;

  const chartData = {
    labels: { timestamp }.timestamp,
    datasets: [
      {
        data: { data }.data,
        backgroundColor: '#173C6C',
      },
    ],
  };

  return <Bar options={options} data={chartData} />;
}

BarChart.propTypes = {
  timestamp: PropTypes.arrayOf(string).isRequired,
  data: PropTypes.arrayOf(number).isRequired,
};

export default BarChart;
