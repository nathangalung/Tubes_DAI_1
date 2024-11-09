// Chart.jsx
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const Chart = ({ costs, title = "Objective Function Cost vs Iteration" }) => {
  const chartData = {
    labels: costs?.map((_, index) => index + 1),
    datasets: [
      {
        label: 'Objective Function Cost',
        data: costs,
        borderColor: '#4f46e5',
        backgroundColor: 'rgba(79, 70, 229, 0.1)',
        fill: true,
        tension: 0.4
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top',
        labels: { color: '#94a3b8' }
      }
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Iteration',
          color: '#94a3b8'
        },
        grid: {
          color: '#2d3748',
          drawBorder: true
        },
        ticks: { color: '#94a3b8' }
      },
      y: {
        title: {
          display: true,
          text: 'Cost',
          color: '#94a3b8'
        },
        grid: {
          color: '#2d3748',
          drawBorder: true
        },
        ticks: { color: '#94a3b8' }
      }
    }
  };

  return (
    <div className="bg-[#111318] rounded-2xl p-6">
      <h3 className="text-lg font-semibold mb-4">{title}</h3>
      <div className="h-[400px] w-full">
        {costs?.length > 0 ? (
          <Line data={chartData} options={chartOptions} />
        ) : (
          <div className="flex items-center justify-center h-full text-[#94a3b8]">
            No data available
          </div>
        )}
      </div>
    </div>
  );
};

export default Chart;