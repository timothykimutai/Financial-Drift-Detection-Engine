import axios from 'axios';
import { FinancialsResponse, NarrativeResponse, DriftResponse } from './types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/v1';

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const fetchFinancials = async (ticker: string): Promise<FinancialsResponse> => {
    const response = await apiClient.get<FinancialsResponse>(`/financials/${ticker}`);
    return response.data;
};

export const fetchNarrative = async (ticker: string): Promise<NarrativeResponse> => {
    const response = await apiClient.get<NarrativeResponse>(`/narrative/${ticker}`);
    return response.data;
};

export const fetchDrift = async (ticker: string): Promise<DriftResponse> => {
    const response = await apiClient.get<DriftResponse>(`/drift/${ticker}`);
    return response.data;
};

export default apiClient;
