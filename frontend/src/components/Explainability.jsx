import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export default function Explainability({ data }) {
  if (!data) return null;

  const chartData = data.map(entry => ({
      word: entry.word,
      importance: Math.abs(entry.shapValue),
  }));

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-6 h-full flex flex-col">
      <div className="mb-4">
        <h3 className="text-md font-semibold text-gray-800">Trust & Transparency (SHAP Values)</h3>
        <p className="text-xs text-gray-500">Top words driving negative sentiment</p>
      </div>
      
      <div className="flex-1 w-full h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart layout="vertical" data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <XAxis type="number" hide />
            <YAxis dataKey="word" type="category" axisLine={false} tickLine={false} />
            <Tooltip cursor={{fill: 'transparent'}} />
            <Bar dataKey="importance" radius={[0, 4, 4, 0]}>
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill="#ef4444" opacity={entry.importance} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
