import React, { useState, useEffect } from 'react';
import { fetchFinancials, fetchNarrative, fetchDrift } from '../api/client';
import { FinancialsResponse, NarrativeResponse, DriftResponse } from '../api/types';
// import FinancialChart from '../components/FinancialChart';
// import NarrativeChart from '../components/NarrativeChart';
// import DriftPanel from '../components/DriftPanel';

const Dashboard: React.FC = () => {
    const [ticker, setTicker] = useState('NVDA');
    const [finData, setFinData] = useState<FinancialsResponse | null>(null);
    const [narData, setNarData] = useState<NarrativeResponse | null>(null);
    const [driftData, setDriftData] = useState<DriftResponse | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadData = async () => {
            setLoading(true);
            try {
                const [fin, nar, drift] = await Promise.all([
                    fetchFinancials(ticker),
                    fetchNarrative(ticker),
                    fetchDrift(ticker)
                ]);
                setFinData(fin);
                setNarData(nar);
                setDriftData(drift);
            } catch (error) {
                console.error("Failed to fetch analytical signals:", error);
            } finally {
                setLoading(false);
            }
        };
        loadData();
    }, [ticker]);

    if (loading) return <div>Analyzing Securities...</div>;

    return (
        <div className="dashboard-container">
            <header>
                <h1>Financial Narrative Drift Engine</h1>
                <input
                    value={ticker}
                    onChange={(e) => setTicker(e.target.value.toUpperCase())}
                    placeholder="Enter Ticker (e.g. MSFT)"
                />
            </header>

            <main>
                <section className="drift-overview">
                    {driftData && (
                        <div className="info-card">
                            <h3>Drift Score: {driftData.drift_score.toFixed(2)}</h3>
                            <p>{driftData.explanation}</p>
                        </div>
                    )}
                </section>

                <div className="charts-grid">
                    {/* Charts will be rendered here */}
                    <div className="chart-placeholder">Financial Momentum (Revenue vs OCF)</div>
                    <div className="chart-placeholder">Narrative Sentiment (Optimism vs Risk)</div>
                </div>
            </main>
        </div>
    );
};

export default Dashboard;
