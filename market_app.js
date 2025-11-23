/**
 * Market Predictor AI - Frontend Application
 * Handles all UI interactions and API calls
 */

const API_BASE = 'http://localhost:5000/api';

// State management
const state = {
    currentSection: 'dashboard',
    symbols: { stocks: [], crypto: [] },
    currentAnalysis: null
};

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initializeNavigation();
    initializeTabs();
    loadPopularSymbols();
    loadQuickStats();
    initializeAnalysis();
    initializeCompare();
});

// Navigation
function initializeNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const section = btn.dataset.section;
            switchSection(section);

            navButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });
}

function switchSection(sectionName) {
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(sectionName).classList.add('active');
    state.currentSection = sectionName;
}

// Tabs
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.dataset.tab;

            tabButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            document.querySelectorAll('.symbols-list').forEach(list => {
                list.classList.remove('active');
            });
            document.getElementById(`${tab}-list`).classList.add('active');
        });
    });
}

// Load popular symbols
async function loadPopularSymbols() {
    try {
        const response = await fetch(`${API_BASE}/symbols`);
        const data = await response.json();

        if (data.success) {
            state.symbols = data.data;
            renderSymbols('stocks', data.data.stocks);
            renderSymbols('crypto', data.data.crypto);
        }
    } catch (error) {
        console.error('Error loading symbols:', error);
    }
}

function renderSymbols(type, symbols) {
    const container = document.getElementById(`${type}-list`);
    container.innerHTML = symbols.map(symbol => `
        <div class="symbol-card" onclick="quickAnalyze('${symbol.symbol}')">
            <div class="symbol-code">${symbol.symbol}</div>
            <div class="symbol-name">${symbol.name}</div>
        </div>
    `).join('');
}

// Quick stats
async function loadQuickStats() {
    const popularSymbols = ['AAPL', 'MSFT', 'BTC-USD', 'ETH-USD'];

    try {
        const response = await fetch(`${API_BASE}/quick-analysis`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symbols: popularSymbols })
        });

        const data = await response.json();

        if (data.success && data.data.length > 0) {
            renderQuickStats(data.data);
        }
    } catch (error) {
        console.error('Error loading quick stats:', error);
    }
}

function renderQuickStats(stats) {
    const container = document.getElementById('quickStats');
    container.innerHTML = stats.map(stat => {
        const isPositive = stat.change_percent >= 0;
        const icon = getRecommendationIcon(stat.recommendation);

        return `
            <div class="stat-card" onclick="quickAnalyze('${stat.symbol}')">
                <div class="stat-icon">${icon}</div>
                <div class="stat-content">
                    <div class="stat-label">${stat.symbol}</div>
                    <div class="stat-value">$${stat.current_price.toFixed(2)}</div>
                    <div class="stat-change ${isPositive ? 'positive' : 'negative'}">
                        ${isPositive ? '▲' : '▼'} ${Math.abs(stat.change_percent).toFixed(2)}%
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// Analysis functionality
function initializeAnalysis() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const symbolInput = document.getElementById('symbolInput');

    analyzeBtn.addEventListener('click', () => {
        const symbol = symbolInput.value.trim().toUpperCase();
        const period = document.getElementById('periodSelect').value;

        if (symbol) {
            analyzeSymbol(symbol, period);
        }
    });

    symbolInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            analyzeBtn.click();
        }
    });
}

function quickAnalyze(symbol) {
    document.getElementById('symbolInput').value = symbol;
    switchSection('analysis');
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.section === 'analysis');
    });
    analyzeSymbol(symbol, '6mo');
}

async function analyzeSymbol(symbol, period) {
    showLoading();

    try {
        const response = await fetch(`${API_BASE}/analyze/${symbol}?period=${period}`);
        const data = await response.json();

        if (data.success) {
            state.currentAnalysis = data.data;
            renderAnalysisResults(data.data);
        } else {
            showError(data.error || 'Error al analizar el símbolo');
        }
    } catch (error) {
        showError('Error de conexión. Asegúrate de que el servidor esté funcionando.');
    } finally {
        hideLoading();
    }
}

function renderAnalysisResults(analysis) {
    const container = document.getElementById('analysisResults');
    container.classList.add('show');

    const isPositive = analysis.change_percent >= 0;
    const recommendation = analysis.signals.recommendation.toLowerCase().replace(' ', '-');

    container.innerHTML = `
        <div class="result-card">
            <div class="result-header">
                <div>
                    <div class="result-symbol">${analysis.symbol}</div>
                </div>
                <div class="result-price">
                    <div class="price-value">$${analysis.current_price.toFixed(2)}</div>
                    <div class="price-change ${isPositive ? 'positive' : 'negative'}">
                        ${isPositive ? '▲' : '▼'} ${Math.abs(analysis.change_percent).toFixed(2)}%
                    </div>
                </div>
            </div>

            <div class="recommendation-section">
                <h3>Recomendación</h3>
                <div class="recommendation-badge ${recommendation}">
                    ${getRecommendationIcon(analysis.signals.recommendation)}
                    ${analysis.signals.recommendation}
                </div>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: ${analysis.signals.confidence}%"></div>
                </div>
                <p style="margin-top: 0.5rem; color: #64748b;">Confianza: ${analysis.signals.confidence}%</p>
            </div>

            <div class="predictions-grid">
                <div class="prediction-card">
                    <div class="prediction-title">Tendencia Predicha</div>
                    <div class="prediction-value" style="color: ${analysis.predictions.trend === 'BULLISH' ? 'var(--success)' : 'var(--danger)'}">
                        ${analysis.predictions.trend === 'BULLISH' ? '📈 ALCISTA' : '📉 BAJISTA'}
                    </div>
                </div>
                <div class="prediction-card">
                    <div class="prediction-title">Precio Estimado (7 días)</div>
                    <div class="prediction-value">$${analysis.predictions.next_7_days[6].toFixed(2)}</div>
                </div>
                <div class="prediction-card">
                    <div class="prediction-title">Cambio Estimado</div>
                    <div class="prediction-value" style="color: ${analysis.predictions.next_7_days[6] > analysis.current_price ? 'var(--success)' : 'var(--danger)'}">
                        ${((analysis.predictions.next_7_days[6] - analysis.current_price) / analysis.current_price * 100).toFixed(2)}%
                    </div>
                </div>
                <div class="prediction-card">
                    <div class="prediction-title">Precisión del Modelo</div>
                    <div class="prediction-value">${(analysis.model_accuracy.test_score * 100).toFixed(1)}%</div>
                </div>
            </div>

            <div class="chart-container">
                <h3 class="chart-title">Histórico y Predicciones</h3>
                <canvas id="priceChart"></canvas>
            </div>

            <div class="indicators-grid">
                ${renderIndicators(analysis.signals.indicators)}
            </div>

            <div>
                <h3 style="margin-bottom: 1rem;">Estadísticas</h3>
                <div class="stats-table">
                    <div class="stat-item">
                        <div class="stat-item-label">Máximo 52 semanas</div>
                        <div class="stat-item-value">$${analysis.statistics.high_52w.toFixed(2)}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-item-label">Mínimo 52 semanas</div>
                        <div class="stat-item-value">$${analysis.statistics.low_52w.toFixed(2)}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-item-label">Volumen Promedio</div>
                        <div class="stat-item-value">${formatVolume(analysis.statistics.avg_volume)}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-item-label">Volatilidad</div>
                        <div class="stat-item-value">${analysis.statistics.volatility.toFixed(2)}</div>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Render chart
    renderPriceChart(analysis);
}

function renderIndicators(indicators) {
    return Object.entries(indicators).map(([name, signal]) => `
        <div class="indicator-card">
            <div class="indicator-name">${name}</div>
            <div class="indicator-signal">${signal}</div>
        </div>
    `).join('');
}

function renderPriceChart(analysis) {
    const ctx = document.getElementById('priceChart').getContext('2d');

    // Prepare data
    const historicalDates = analysis.historical_data.dates;
    const historicalPrices = analysis.historical_data.prices;

    // Create future dates
    const lastDate = new Date(historicalDates[historicalDates.length - 1]);
    const futureDates = analysis.predictions.next_7_days.map((_, i) => {
        const date = new Date(lastDate);
        date.setDate(date.getDate() + i + 1);
        return date.toISOString().split('T')[0];
    });

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: [...historicalDates, ...futureDates],
            datasets: [
                {
                    label: 'Precio Histórico',
                    data: [...historicalPrices, ...Array(7).fill(null)],
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Predicción',
                    data: [...Array(historicalPrices.length - 1).fill(null), historicalPrices[historicalPrices.length - 1], ...analysis.predictions.next_7_days],
                    borderColor: '#8b5cf6',
                    backgroundColor: 'rgba(139, 92, 246, 0.1)',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: { size: 14 },
                    bodyFont: { size: 13 }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: false,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        callback: value => '$' + value.toFixed(2)
                    }
                }
            }
        }
    });
}

// Compare functionality
function initializeCompare() {
    const compareBtn = document.getElementById('compareBtn');
    const compareInput = document.getElementById('compareInput');

    compareBtn.addEventListener('click', () => {
        const symbols = compareInput.value
            .split(',')
            .map(s => s.trim().toUpperCase())
            .filter(s => s.length > 0);

        if (symbols.length >= 2) {
            compareSymbols(symbols);
        } else {
            showError('Ingresa al menos 2 símbolos para comparar');
        }
    });

    compareInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            compareBtn.click();
        }
    });
}

async function compareSymbols(symbols) {
    showLoading();

    try {
        const response = await fetch(`${API_BASE}/compare`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symbols })
        });

        const data = await response.json();

        if (data.success) {
            renderCompareResults(data.data);
        } else {
            showError(data.error || 'Error al comparar símbolos');
        }
    } catch (error) {
        showError('Error de conexión. Asegúrate de que el servidor esté funcionando.');
    } finally {
        hideLoading();
    }
}

function renderCompareResults(comparisons) {
    const container = document.getElementById('compareResults');
    container.classList.add('show');

    container.innerHTML = `
        <div class="compare-table">
            <table>
                <thead>
                    <tr>
                        <th>Símbolo</th>
                        <th>Precio Actual</th>
                        <th>Cambio %</th>
                        <th>Predicción 7d %</th>
                        <th>Recomendación</th>
                        <th>Precisión</th>
                    </tr>
                </thead>
                <tbody>
                    ${comparisons.map(comp => `
                        <tr onclick="quickAnalyze('${comp.symbol}')" style="cursor: pointer;">
                            <td><strong>${comp.symbol}</strong></td>
                            <td>$${comp.current_price.toFixed(2)}</td>
                            <td style="color: ${comp.change_percent >= 0 ? 'var(--success)' : 'var(--danger)'}">
                                ${comp.change_percent >= 0 ? '▲' : '▼'} ${Math.abs(comp.change_percent).toFixed(2)}%
                            </td>
                            <td style="color: ${comp.prediction_change >= 0 ? 'var(--success)' : 'var(--danger)'}">
                                ${comp.prediction_change >= 0 ? '▲' : '▼'} ${Math.abs(comp.prediction_change).toFixed(2)}%
                            </td>
                            <td>
                                <span class="recommendation-badge ${comp.recommendation.toLowerCase().replace(' ', '-')}" style="padding: 0.25rem 0.75rem; font-size: 0.875rem;">
                                    ${comp.recommendation}
                                </span>
                            </td>
                            <td>${(comp.model_accuracy * 100).toFixed(1)}%</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
}

// Utility functions
function getRecommendationIcon(recommendation) {
    const icons = {
        'STRONG BUY': '🚀',
        'BUY': '📈',
        'HOLD': '⏸️',
        'SELL': '📉',
        'STRONG SELL': '🔻'
    };
    return icons[recommendation] || '❓';
}

function formatVolume(volume) {
    if (volume >= 1e9) return (volume / 1e9).toFixed(2) + 'B';
    if (volume >= 1e6) return (volume / 1e6).toFixed(2) + 'M';
    if (volume >= 1e3) return (volume / 1e3).toFixed(2) + 'K';
    return volume.toFixed(0);
}

function showLoading() {
    document.getElementById('loadingOverlay').classList.add('show');
}

function hideLoading() {
    document.getElementById('loadingOverlay').classList.remove('show');
}

function showError(message) {
    const container = document.getElementById('analysisResults');
    container.classList.add('show');
    container.innerHTML = `
        <div class="error-message">
            <strong>Error:</strong> ${message}
        </div>
    `;
}

// Auto-refresh quick stats every 5 minutes
setInterval(loadQuickStats, 5 * 60 * 1000);
