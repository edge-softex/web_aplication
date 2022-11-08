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
import { useSelector } from 'react-redux';

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

function LineChart() {
  let dataSet = useSelector((state) => state.power.powerData);
  if (!dataSet) {
    dataSet = { timestamp: ['None'], data: [0], forecast: [0] };
  }
  const { timestamp, data, forecast } = dataSet;

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
      {
        label: 'Forecast',
        data: { forecast }.forecast,
        borderColor: '#F7A159',
        backgroundColor: '#F7A159',
        borderWidth: 2,
      },
    ],
  };

  return (
    <Line options={options} data={chartData} />
  );
}

export default LineChart;
