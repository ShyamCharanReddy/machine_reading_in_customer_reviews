import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

export const analyzeUrl = async (url) => {
  try {
    const response = await api.post('/analyze-url', { url });
    return response.data;
  } catch (error) {
    console.error('Error analyzing URL:', error);
    throw error;
  }
};
