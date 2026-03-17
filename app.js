// 数据文件路径
const DATA_FILE = 'data/market_data.json';

// 页面加载时获取数据
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch(DATA_FILE + '?t=' + Date.now());
        const data = await response.json();
        
        // 隐藏加载提示，显示主要内容
        document.getElementById('loadingIndicator').style.display = 'none';
        document.getElementById('mainContent').style.display = 'block';
        
        // 渲染页面
        renderPage(data);
        
        // 绘制图表
        setTimeout(() => {
            drawCharts(data);
        }, 100);
        
    } catch (error) {
        console.error('加载数据失败:', error);
        document.getElementById('loadingIndicator').innerHTML = `
            <div style="color: #721c24; padding: 40px; text-align: center;">
                <p style="font-size: 18px; margin-bottom: 10px;">⚠️ 数据加载失败</p>
                <p style="color: #6c757d;">请稍后刷新页面重试</p>
            </div>
        `;
    }
});

// 渲染页面内容
function renderPage(data) {
    // 更新日期
    document.getElementById('reportDate').textContent = data.reportDate;
    document.getElementById('updateTime').textContent = '上次更新: ' + data.updateTime;
    document.getElementById('dataUpdateDate').textContent = data.updateTime;
    
    // 渲染A股卡片
    renderStockCards('aStockCards', data.aStock.indices);
    
    // 渲染美股卡片
    renderStockCards('usStockCards', data.usStock.indices);
    
    // 渲染高亮提示
    document.getElementById('aStockHighlight').innerHTML = `
        <strong>📈 市场特征：</strong>${data.aStock.highlight}
    `;
    
    document.getElementById('usStockHighlight').innerHTML = `
        <strong>🔥 科技股领涨：</strong>${data.usStock.highlight}
    `;
    
    // 渲染商品表格
    renderCommodityTable(data.commodities);
    
    // 渲染国际局势
    renderGeopoliticalNews(data.geopolitical);
    
    // 渲染板块表格
    renderSectorTables(data.sectors);
    
    // 渲染投资建议
    renderInvestmentAdvice(data.advice);
    
    // 渲染后市展望
    renderOutlook(data.outlook);
}

// 渲染股票指数卡片
function renderStockCards(containerId, indices) {
    const container = document.getElementById(containerId);
    container.innerHTML = indices.map(index => `
        <div class="card index-card">
            <div class="index-name">${index.name}</div>
            <div class="index-value">${formatNumber(index.value)}</div>
            <div class="index-change ${index.change >= 0 ? 'positive' : 'negative'}">
                ${index.change >= 0 ? '+' : ''}${index.change.toFixed(2)}%
            </div>
        </div>
    `).join('');
}

// 渲染商品表格
function renderCommodityTable(commodities) {
    const container = document.getElementById('commodityTable');
    container.innerHTML = `
        <table>
            <thead>
                <tr>
                    <th>品种</th>
                    <th>价格</th>
                    <th>涨跌幅</th>
                </tr>
            </thead>
            <tbody>
                ${commodities.map(item => `
                    <tr>
                        <td>${item.name}</td>
                        <td>${item.price}</td>
                        <td class="${item.change >= 0 ? 'positive' : 'negative'}">
                            ${item.change >= 0 ? '+' : ''}${item.change.toFixed(2)}%
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

// 渲染国际局势新闻
function renderGeopoliticalNews(news) {
    const container = document.getElementById('geopoliticalNews');
    container.innerHTML = news.map(item => `
        <div class="news-item">
            <div class="news-title">${item.title}</div>
            <div class="news-content">${item.content}</div>
        </div>
    `).join('');
}

// 渲染板块表格
function renderSectorTables(sectors) {
    const container = document.getElementById('sectorTables');
    container.innerHTML = `
        <div>
            <h3 style="margin-bottom: 15px; color: #1a1a2e;">🔥 领涨板块</h3>
            <table>
                <thead>
                    <tr>
                        <th>板块</th>
                        <th>涨幅</th>
                        <th>驱动因素</th>
                    </tr>
                </thead>
                <tbody>
                    ${sectors.gainers.map(item => `
                        <tr>
                            <td>${item.name}</td>
                            <td class="positive">+${item.change.toFixed(2)}%</td>
                            <td>${item.reason}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
        <div>
            <h3 style="margin-bottom: 15px; color: #1a1a2e;">📉 调整板块</h3>
            <table>
                <thead>
                    <tr>
                        <th>板块</th>
                        <th>跌幅</th>
                        <th>原因</th>
                    </tr>
                </thead>
                <tbody>
                    ${sectors.decliners.map(item => `
                        <tr>
                            <td>${item.name}</td>
                            <td class="negative">${item.change.toFixed(2)}%</td>
                            <td>${item.reason}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
}

// 渲染投资建议
function renderInvestmentAdvice(advice) {
    const container = document.getElementById('investmentAdvice');
    container.innerHTML = `
        <div class="advice-title">基于当前市场环境的投资策略</div>
        ${advice.map(item => `
            <div class="advice-item">
                <strong>${item.title}</strong>
                <p>${item.content}</p>
            </div>
        `).join('')}
    `;
}

// 渲染后市展望
function renderOutlook(outlook) {
    const container = document.getElementById('outlookGrid');
    container.innerHTML = `
        <div class="card">
            <h3 style="margin-bottom: 15px; color: #155724;">✅ 积极因素</h3>
            <ul style="line-height: 2; color: #495057; padding-left: 20px;">
                ${outlook.positive.map(item => `<li>${item}</li>`).join('')}
            </ul>
        </div>
        <div class="card">
            <h3 style="margin-bottom: 15px; color: #721c24;">⚠️ 风险因素</h3>
            <ul style="line-height: 2; color: #495057; padding-left: 20px;">
                ${outlook.negative.map(item => `<li>${item}</li>`).join('')}
            </ul>
        </div>
    `;
}

// 绘制图表
function drawCharts(data) {
    // A股走势图
    drawLineChart('chinaChart', data.charts.china, 'A股三大指数走势');
    
    // 美股走势图
    drawLineChart('usChart', data.charts.us, '美股三大指数走势');
    
    // 商品涨跌幅图
    drawBarChart('commodityChart', data.charts.commodity);
}

// 绘制折线图
function drawLineChart(canvasId, chartData, title) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: chartData.datasets.map(dataset => ({
                label: dataset.label,
                data: dataset.data,
                borderColor: dataset.borderColor,
                backgroundColor: dataset.backgroundColor,
                tension: 0.4,
                fill: true,
                pointRadius: 4,
                pointHoverRadius: 6
            }))
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        usePointStyle: true,
                        padding: 15
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: {
                        color: 'rgba(0,0,0,0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
}

// 绘制柱状图
function drawBarChart(canvasId, chartData) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: '涨跌幅(%)',
                data: chartData.data,
                backgroundColor: chartData.colors,
                borderColor: chartData.borderColors,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0,0,0,0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// 格式化数字
function formatNumber(num) {
    return num.toLocaleString('zh-CN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}