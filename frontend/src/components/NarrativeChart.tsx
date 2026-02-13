import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';
import { NarrativeResponse } from '../api/types';

interface Props {
    data: NarrativeResponse;
    quarters: string[];
}

const NarrativeChart: React.FC<Props> = ({ data, quarters }) => {
    const chartData = quarters.map((q, i) => ({
        quarter: q,
        optimism: data.optimism_score[i],
        risk: data.risk_mentions[i]
    }));

    return (
        <div style={{ width: '100%', height: 300 }}>
            <h3>Narrative Sentiment & Risk</h3>
            <ResponsiveContainer>
                <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="quarter" />
                    <YAxis yAxisId="left" orientation="left" stroke="#8884d8" label={{ value: 'Optimism', angle: -90, position: 'insideLeft' }} />
                    <YAxis yAxisId="right" orientation="right" stroke="#82ca9d" label={{ value: 'Risk Mentions', angle: 90, position: 'insideRight' }} />
                    <Tooltip />
                    <Legend />
                    <Bar yAxisId="left" dataKey="optimism" name="Optimism Score" fill="#8884d8" />
                    <Bar yAxisId="right" dataKey="risk" name="Risk Mentions" fill="#82ca9d" />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default NarrativeChart;
