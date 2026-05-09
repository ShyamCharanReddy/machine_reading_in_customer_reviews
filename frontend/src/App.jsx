import React, { useState } from 'react';
import InputSection from './components/InputSection';
import ResultsDashboard from './components/ResultsDashboard';
import { analyzeUrl } from './services/api';
import { Activity } from 'lucide-react';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async (url) => {
    setIsLoading(true);
    setError(null);
    setData(null);
    try {
      const result = await analyzeUrl(url);
      setData(result);
    } catch (err) {
      setError('An error occurred while generating insights. Ensure the backend server is running.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans pb-12">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center gap-2">
              <div className="p-2 bg-blue-600 rounded-lg">
                <Activity className="h-6 w-6 text-white" />
              </div>
              <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
                SentiInsight AI
              </h1>
            </div>
            <nav>
              <a href="#" className="text-sm font-medium text-gray-500 hover:text-gray-900">Documentation</a>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 mt-10">
        <div className="max-w-3xl mx-auto text-center mb-10">
          <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
            Agentic Sentiment Analysis
          </h2>
          <p className="mt-4 text-lg text-gray-500">
            Instantly uncover customer pain points and shifting trends from e-commerce product reviews using precise, dual-engine machine learning algorithms.
          </p>
        </div>

        <InputSection onAnalyze={handleAnalyze} isLoading={isLoading} />
        
        {error && (
          <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-8 rounded p-4">
            <p className="text-red-700">{error}</p>
          </div>
        )}

        {data && <ResultsDashboard data={data} />}
        
      </main>
    </div>
  );
}

export default App;
