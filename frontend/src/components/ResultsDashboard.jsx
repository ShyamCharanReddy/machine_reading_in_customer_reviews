import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, Tooltip as RechartsTooltip, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Legend } from 'recharts';
import { Database, TrendingUp, AlertCircle, Bot } from 'lucide-react';
import Explainability from './Explainability';

export default function ResultsDashboard({ data }) {
  const [visibleSections, setVisibleSections] = useState(0);

  // Staggered loading effect
  useEffect(() => {
    setVisibleSections(0);
    const intervals = [];
    
    // Reveal one section every 600ms
    for (let i = 1; i <= 5; i++) {
       intervals.push(setTimeout(() => {
          setVisibleSections(prev => prev + 1);
       }, i * 600));
    }
    
    return () => intervals.forEach(clearTimeout);
  }, [data]);

  if (!data) return null;

  const { extraction, hybrid_scoring, pain_points, explainability, agentic_insight } = data;

  const pieData = [
    { name: 'Positive', value: hybrid_scoring.roberta_distribution.positive, color: '#10b981' },
    { name: 'Neutral', value: hybrid_scoring.roberta_distribution.neutral, color: '#9ca3af' },
    { name: 'Negative', value: hybrid_scoring.roberta_distribution.negative, color: '#ef4444' }
  ];

  return (
    <div className="space-y-6">
      {/* 1. Extraction Stats */}
      <div className={`transition-all duration-700 ease-out transform ${visibleSections >= 1 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
        <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-6 flex items-center gap-4">
          <div className="p-3 bg-blue-50 rounded-full text-blue-600">
            <Database className="h-6 w-6" />
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <h3 className="text-sm font-medium text-gray-500">Extraction Summary</h3>
              {extraction.is_simulated && (
                <span className="px-2 py-0.5 bg-amber-100 text-amber-700 text-[10px] font-bold uppercase rounded-full tracking-wider animate-pulse">
                  Simulated Data
                </span>
              )}
            </div>
            <p className="text-gray-900">
              Scraped <span className="font-bold text-lg">{extraction.total_reviews_scraped}</span> reviews from <span className="font-semibold">{extraction.source_domain}</span> in {extraction.extraction_time_ms}ms.
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* 2. Hybrid Scoring */}
        <div className={`transition-all duration-700 ease-out transform ${visibleSections >= 2 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
          <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-6 h-full flex flex-col">
            <div className="flex items-center gap-2 mb-4">
              <TrendingUp className="h-5 w-5 text-indigo-500" />
              <h3 className="text-md font-semibold text-gray-800">Hybrid Scoring Profile</h3>
            </div>
            
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="bg-gray-50 rounded p-3">
                <div className="text-xs text-gray-500 mb-1">VADER Compound</div>
                <div className="text-xl font-bold">{hybrid_scoring.vader_compound}</div>
              </div>
              <div className="bg-gray-50 rounded p-3">
                <div className="text-xs text-gray-500 mb-1">Final Verdict</div>
                <div className="text-xl font-bold text-indigo-600">{hybrid_scoring.final_prediction}</div>
              </div>
            </div>

            <div className="flex-1 w-full h-48 min-h-[200px]">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <RechartsTooltip formatter={(val) => `${(val * 100).toFixed(1)}%`} />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* 3. Pain Point Discovery & SHAP combined block */}
        <div className={`flex flex-col gap-6 transition-all duration-700 ease-out transform ${visibleSections >= 3 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
          
          <div className="bg-white rounded-lg shadow-sm border border-gray-100 p-6">
            <div className="flex items-center gap-2 mb-4">
              <AlertCircle className="h-5 w-5 text-amber-500" />
              <h3 className="text-md font-semibold text-gray-800">Discovered Themes (LDA)</h3>
            </div>
            <ul className="space-y-3">
              {pain_points.map((topic, idx) => (
                <li key={idx} className="flex items-start">
                  <span className="flex-shrink-0 h-6 w-6 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center text-xs font-bold mr-3">{idx + 1}</span>
                  <span className="text-gray-700">{topic}</span>
                </li>
              ))}
            </ul>
          </div>
          
          <div className={`flex-1 transition-all duration-700 ease-out transform ${visibleSections >= 4 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
            <Explainability data={explainability} />
          </div>

        </div>
      </div>

      {/* 4. Agentic Insights */}
      <div className={`transition-all duration-1000 ease-in-out transform ${visibleSections >= 5 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg shadow-sm border border-blue-100 p-6">
          <div className="flex items-center gap-2 mb-4">
            <Bot className="h-6 w-6 text-blue-600" />
            <h3 className="text-lg font-bold text-gray-800">Agentic Executive Summary</h3>
          </div>
          <div className="bg-white/80 rounded border border-blue-50/50 p-5 shadow-inner">
             <p className="text-gray-800 leading-relaxed font-medium italic">
               "{agentic_insight}"
             </p>
          </div>
        </div>
      </div>

    </div>
  );
}
