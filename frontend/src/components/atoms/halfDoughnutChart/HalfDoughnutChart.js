import React, { useState, useRef, useEffect } from 'react';
import {
  Chart as ChartJS, ArcElement, Tooltip, Legend,
} from 'chart.js';
import { Doughnut } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);

function createGradient(ctx, area) {
  const colorStart = '#F9C74F24';
  const colorMid = '#F5CB6477';
  const colorEnd = '#F9C74F';

  const gradient = ctx.createLinearGradient(0, area.bottom, 0, area.top);

  gradient.addColorStop(0, colorStart);
  gradient.addColorStop(0.3, colorMid);
  gradient.addColorStop(1, colorEnd);

  return gradient;
}

function HalfDoughnutChart() {
  const chartRef = useRef(null);
  const [chartData, setChartData] = useState({
    datasets: [],
  });

  useEffect(() => {
    const chart = chartRef.current;

    if (chart) {
      setChartData({
        labels: '',
        datasets: [
          {
            data: [12, 19],
            backgroundColor: [
              createGradient(chart.ctx, chart.chartArea),
              '#F5F5F5',
            ],
            borderColor: [
              '#00000000',
              '#00000000',
            ],
            borderWidth: 1,
            cutout: '62%',
            circumference: 180,
            rotation: 270,
          },
        ],
      });
    }
  }, []);

  const options = {
    maintainAspectRatio: true,
    responsive: true,
  };

  return <Doughnut options={options} ref={chartRef} data={chartData} />;
}

export default HalfDoughnutChart;
