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
      },
    },
  },
};

const data = {
  labels: ['um', 'dois', 'três', 'quatro', 'cinco'],
  datasets: [
    {
      label: 'Consumed',
      data: [1, 2, 3, 4, 5],
      borderColor: '#173C6C',
      backgroundColor: '#173C6C',
      borderWidth: 2,
    },
    {
      label: 'Forecast',
      data: [2, 4, 6, 8, 10],
      borderColor: '#F7A159',
      backgroundColor: '#F7A159',
      borderWidth: 2,
    },
  ],
};

function LineChart() {
  return (
    <Line options={options} data={data} />
  );
}

export default LineChart;
