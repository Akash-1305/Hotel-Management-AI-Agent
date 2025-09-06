import React from 'react';

const MetricCard = ({ title, value, icon: Icon, color, bgColor }) => {
  return (
    <div className="bg-white rounded-lg shadow-sm p-6 flex items-center transition-transform hover:translate-y-[-2px]">
      <div className={`${bgColor} ${color} p-3 rounded-full mr-4`}>
        <Icon className="h-6 w-6" />
      </div>
      <div>
        <h3 className="text-gray-500 text-sm font-medium">{title}</h3>
        <p className={`text-2xl font-semibold mt-1 ${color.includes('green') ? 'text-green-600' : color.includes('red') ? 'text-red-600' : color.includes('blue') ? 'text-blue-600' : 'text-gray-900'}`}>
          {value}
        </p>
      </div>
    </div>
  );
};

export default MetricCard;