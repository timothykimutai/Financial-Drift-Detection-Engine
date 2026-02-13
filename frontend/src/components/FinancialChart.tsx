import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { FinancialsResponse } from '../api/types';

interface Props {
    data: FinancialsResponse;
}

const FinancialChart: React.FC<Props> = ({ data }) => {
    const chartData = data.quarterly_index.map((q, i) => ({
        quarter: q,
        revenue: data.revenue_growth[i] * 100,
        ocf: data.ocf_growth[i] * 100
    }));

    return (
        <div style={{ width: '100%', height: 300 }}>
            <h3>Financial Momentum (% Growth)</h3>
            <ResponsiveContainer>
                <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="quarter" />
                    <YAxis label={{ value: '%', angle: -90, position: 'insideLeft' }} />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="revenue" name="Revenue Growth" stroke="#8884d8" strokeWidth={2} />
                    <Line type="monotone" dataKey="ocf" name="OCF Growth" stroke="#82ca9d" strokeWidth={2} />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default FinancialChart;
