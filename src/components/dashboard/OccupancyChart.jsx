import React, { useState } from 'react';

const OccupancyChart = ({ occupancyData }) => {
  const [period, setPeriod] = useState('Week');
  
  const chartHeight = 200;
  
  return (
    <div className="bg-white rounded-lg shadow-sm p-4">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold">Weekly Occupancy</h2>
        <div className="flex space-x-1 bg-gray-100 rounded-lg p-1">
          {['Week', 'Month', 'Year'].map((p) => (
            <button
              key={p}
              className={`px-4 py-1 rounded-md text-sm font-medium transition-colors ${
                period === p
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-200'
              }`}
              onClick={() => setPeriod(p)}
            >
              {p}
            </button>
          ))}
        </div>
      </div>
      
      <div className="mt-6 relative" style={{ height: `${chartHeight + 40}px` }}>
        <div className="absolute left-0 top-0 h-full flex flex-col justify-between text-xs text-gray-500">
          <div>100%</div>
          <div>75%</div>
          <div>50%</div>
          <div>25%</div>
          <div>0%</div>
        </div>
        
        <div className="ml-10 h-full flex items-end space-x-4">
          {occupancyData.map((day, index) => {
            const barHeight = (day.occupancyPercentage / 100) * chartHeight;
            
            return (
              <div key={index} className="flex flex-col items-center flex-1">
                <div
                  className="w-full bg-blue-500 rounded-t-sm transition-all duration-500 ease-in-out hover:bg-blue-600"
                  style={{ 
                    height: `${barHeight}px`,
                    maxWidth: '30px',
                    margin: '0 auto'
                  }}
                ></div>
                <div className="text-xs text-gray-500 mt-2">{day.day}</div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default OccupancyChart;