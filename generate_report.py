#!/usr/bin/env python3
"""
每日金融市场行情分析 - 自动生成脚本
使用 DeepSeek API 获取最新金融数据并生成 HTML 报告
"""

import os
import json
import requests
from datetime import datetime

# DeepSeek API 配置
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

def get_financial_analysis():
    """调用 DeepSeek API 获取金融分析和数据"""
    
    prompt = """你是一位专业的金融分析师。请搜索并整理今日（或最近交易日）的金融市场数据，然后生成一份详细的行情分析报告。

请搜索以下信息：
1. A股市场：上证指数、深证成指、创业板指的最新点位和涨跌幅
2. 美股市场：道琼斯、标普500、纳斯达克的最新收盘数据
3. 商品市场：黄金、原油（布伦特、WTI）、比特币、以太坊的最新价格和涨跌幅
4. 重要的国际财经新闻和市场热点

请以 JSON 格式返回以下数据（只返回JSON，不要其他内容）：

{
    "report_date": "2025年3月18日 星期二",
    "a_stock": {
        "shanghai": {"name": "上证指数", "value": "3,085.32", "change": "-0.26%"},
        "shenzhen": {"name": "深证成指", "value": "9,567.45", "change": "+0.19%"},
        "chinext": {"name": "创业板指", "value": "1,857.02", "change": "+1.41%"},
        "summary": "市场呈现明显的结构性分化格局..."
    },
    "us_stock": {
        "dow": {"name": "道琼斯指数", "value": "38,675.68", "change": "+0.83%"},
        "sp500": {"name": "标普500", "value": "5,234.18", "change": "+1.01%"},
        "nasdaq": {"name": "纳斯达克", "value": "16,428.82", "change": "+1.22%"},
        "summary": "美股三大指数止跌反弹..."
    },
    "commodities": [
        {"name": "黄金", "price": "$2,185.60/盎司", "change": "-0.76%"},
        {"name": "布伦特原油", "price": "$85.12/桶", "change": "-2.35%"},
        {"name": "WTI原油", "price": "$80.45/桶", "change": "-2.68%"},
        {"name": "比特币", "price": "$67,500", "change": "+3.20%"},
        {"name": "以太坊", "price": "$3,450", "change": "+5.80%"}
    ],
    "news": [
        {"title": "标题1", "content": "内容1"},
        {"title": "标题2", "content": "内容2"}
    ],
    "hot_sectors": {
        "gainers": [
            {"name": "存储芯片", "change": "+3.68%", "reason": "AI需求推动"},
            {"name": "PCB概念", "change": "+2.85%", "reason": "产业链升级"}
        ],
        "losers": [
            {"name": "石油石化", "change": "-3.20%", "reason": "油价下跌"},
            {"name": "传统能源", "change": "-2.80%", "reason": "能源转型"}
        ]
    },
    "investment_advice": [
        {"title": "1. 科技成长主线持续", "content": "详细建议..."},
        {"title": "2. 规避传统能源板块", "content": "详细建议..."}
    ],
    "chart_data": {
        "china_labels": ["3/13", "3/14", "3/15", "3/16", "3/17"],
        "shanghai_data": [3050, 3060, 3070, 3080, 3085],
        "shenzhen_data": [9400, 9450, 9500, 9550, 9567],
        "chinext_data": [1800, 1820, 1840, 1850, 1857],
        "us_labels": ["3/12", "3/13", "3/14", "3/15", "3/16"],
        "dow_data": [38200, 38300, 38400, 38500, 38675],
        "sp500_data": [5150, 5180, 5200, 5220, 5234],
        "nasdaq_data": [16000, 16100, 16200, 16350, 16428]
    }
}

请确保所有数据都是真实的最新数据，通过搜索获取。JSON 必须是有效的格式。"""

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 8000
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # 提取 JSON 部分
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0]
        elif '```' in content:
            content = content.split('```')[1].split('```')[0]
        
        content = content.strip()
        return json.loads(content)
        
    except Exception as e:
        print(f"Error calling DeepSeek API: {e}")
        return None


def generate_html(data):
    """生成 HTML 报告"""
    
    update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 生成商品表格行
    commodity_rows = ""
    for item in data['commodities']:
        change_class = "positive" if item['change'].startswith('+') else "negative"
        commodity_rows += f"""
                            <tr>
                                <td>{item['name']}</td>
                                <td>{item['price']}</td>
                                <td class="{change_class}">{item['change']}</td>
                            </tr>"""
    
    # 生成新闻
    news_items = ""
    for i, item in enumerate(data['news'], 1):
        news_items += f"""
            <div class="news-item">
                <div class="news-title">{i}. {item['title']}</div>
                <div class="news-content">{item['content']}</div>
            </div>"""
    
    # 生成领涨板块
    gainer_rows = ""
    for item in data['hot_sectors']['gainers']:
        gainer_rows += f"""
                            <tr>
                                <td>{item['name']}</td>
                                <td class="positive">{item['change']}</td>
                                <td>{item['reason']}</td>
                            </tr>"""
    
    # 生成下跌板块
    loser_rows = ""
    for item in data['hot_sectors']['losers']:
        loser_rows += f"""
                            <tr>
                                <td>{item['name']}</td>
                                <td class="negative">{item['change']}</td>
                                <td>{item['reason']}</td>
                            </tr>"""
    
    # 生成投资建议
    advice_items = ""
    for item in data['investment_advice']:
        advice_items += f"""
                <div class="advice-item">
                    <strong>{item['title']}</strong>
                    <p>{item['content']}</p>
                </div>"""
    
    # 图表数据
    cd = data['chart_data']
    china_labels = json.dumps(cd['china_labels'])
    us_labels = json.dumps(cd['us_labels'])
    
    # 商品图表数据
    commodity_names = json.dumps([item['name'] for item in data['commodities']])
    commodity_changes = [float(item['change'].replace('+', '').replace('%', '')) for item in data['commodities']]
    commodity_colors = []
    for item in data['commodities']:
        if item['change'].startswith('+'):
            commodity_colors.append("'rgba(46, 204, 113, 0.8)'")
        else:
            commodity_colors.append("'rgba(231, 76, 60, 0.8)'")
    
    # A股涨跌样式
    sh_change_class = "positive" if data['a_stock']['shanghai']['change'].startswith('+') else "negative"
    sz_change_class = "positive" if data['a_stock']['shenzhen']['change'].startswith('+') else "negative"
    ch_change_class = "positive" if data['a_stock']['chinext']['change'].startswith('+') else "negative"
    
    # 美股涨跌样式
    dow_change_class = "positive" if data['us_stock']['dow']['change'].startswith('+') else "negative"
    sp500_change_class = "positive" if data['us_stock']['sp500']['change'].startswith('+') else "negative"
    nasdaq_change_class = "positive" if data['us_stock']['nasdaq']['change'].startswith('+') else "negative"
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日金融市场行情分析 - {data['report_date']}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
/* 全局样式 */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}}

.container {{
    max-width: 1400px;
    margin: 0 auto;
    background: white;
    border-radius: 16px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    padding: 40px;
}}

/* 头部 */
.header {{
    text-align: center;
    margin-bottom: 40px;
    padding-bottom: 30px;
    border-bottom: 3px solid #667eea;
}}

.header h1 {{
    font-size: 32px;
    color: #1a1a2e;
    margin-bottom: 10px;
}}

.header .date {{
    font-size: 18px;
    color: #6c757d;
    margin-bottom: 15px;
}}

.update-info {{
    display: flex;
    justify-content: center;
    gap: 20px;
    align-items: center;
}}

.auto-update {{
    background: #d4edda;
    color: #155724;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 14px;
}}

.update-time {{
    color: #6c757d;
    font-size: 14px;
}}

/* 区块样式 */
.section {{
    margin-bottom: 40px;
}}

.section-title {{
    font-size: 24px;
    color: #1a1a2e;
    margin-bottom: 20px;
    padding-left: 15px;
    border-left: 4px solid #667eea;
}}

/* 网格布局 */
.grid-2 {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 30px;
    margin-bottom: 30px;
}}

.grid-3 {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 30px;
}}

/* 卡片 */
.card {{
    background: linear-gradient(135deg, #f5f7fa 0%, #e8ecef 100%);
    border-radius: 12px;
    padding: 25px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}}

.index-card {{
    text-align: center;
}}

.index-name {{
    font-size: 16px;
    color: #6c757d;
    margin-bottom: 10px;
}}

.index-value {{
    font-size: 32px;
    font-weight: bold;
    color: #1a1a2e;
    margin-bottom: 8px;
}}

.index-change {{
    font-size: 18px;
    font-weight: 600;
    padding: 5px 15px;
    border-radius: 20px;
    display: inline-block;
}}

.positive {{
    background: #d4edda;
    color: #155724;
}}

.negative {{
    background: #f8d7da;
    color: #721c24;
}}

/* 高亮提示 */
.highlight {{
    background: #fff3cd;
    padding: 15px 20px;
    border-radius: 8px;
    border-left: 4px solid #ffc107;
    margin: 15px 0;
}}

.highlight strong {{
    display: block;
    margin-bottom: 8px;
    color: #856404;
}}

.highlight p {{
    color: #856404;
    line-height: 1.6;
}}

/* 图表容器 */
.chart-container {{
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}}

.chart-title {{
    font-size: 18px;
    font-weight: 600;
    color: #1a1a2e;
    margin-bottom: 15px;
}}

/* 表格 */
table {{
    width: 100%;
    border-collapse: collapse;
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}}

th, td {{
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid #e9ecef;
}}

th {{
    background: #667eea;
    color: white;
    font-weight: 600;
}}

tr:hover {{
    background: #f8f9fa;
}}

/* 新闻项 */
.news-item {{
    background: white;
    border-left: 4px solid #667eea;
    padding: 15px 20px;
    margin-bottom: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    transition: transform 0.3s ease;
}}

.news-item:hover {{
    transform: translateX(5px);
}}

.news-title {{
    font-size: 16px;
    font-weight: 600;
    color: #1a1a2e;
    margin-bottom: 8px;
}}

.news-content {{
    font-size: 14px;
    color: #495057;
    line-height: 1.6;
}}

/* 投资建议 */
.advice-box {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 12px;
    padding: 30px;
    margin-top: 20px;
}}

.advice-title {{
    font-size: 22px;
    margin-bottom: 20px;
    font-weight: 600;
}}

.advice-item {{
    background: rgba(255,255,255,0.15);
    border-radius: 8px;
    padding: 15px 20px;
    margin-bottom: 12px;
    backdrop-filter: blur(10px);
}}

.advice-item strong {{
    display: block;
    font-size: 16px;
    margin-bottom: 8px;
}}

.advice-item p {{
    font-size: 14px;
    line-height: 1.6;
    opacity: 0.95;
}}

/* 风险提示 */
.risk-warning {{
    background: #fff3cd;
    border: 2px solid #ffc107;
    border-radius: 8px;
    padding: 15px 20px;
    margin-top: 30px;
    color: #856404;
}}

.risk-warning strong {{
    display: block;
    margin-bottom: 5px;
}}

/* 页脚 */
.footer {{
    text-align: center;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 2px solid #e9ecef;
    color: #6c757d;
    font-size: 14px;
}}

.footer a {{
    color: #667eea;
    text-decoration: none;
}}

.footer a:hover {{
    text-decoration: underline;
}}

/* 响应式设计 */
@media (max-width: 768px) {{
    body {{
        padding: 10px;
    }}
    
    .container {{
        padding: 20px;
    }}
    
    .header h1 {{
        font-size: 24px;
    }}
    
    .grid-2, .grid-3 {{
        grid-template-columns: 1fr;
    }}
    
    .index-value {{
        font-size: 28px;
    }}
}}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 每日金融市场行情分析</h1>
            <p class="date">{data['report_date']} | 北京时间 09:00</p>
            <div class="update-info">
                <span class="auto-update">🔄 每日自动更新</span>
                <span class="update-time">上次更新: {update_time}</span>
            </div>
        </div>

        <!-- A股市场 -->
        <div class="section">
            <h2 class="section-title">🇨🇳 A股市场概况</h2>
            <div class="grid-3">
                <div class="card index-card">
                    <div class="index-name">{data['a_stock']['shanghai']['name']}</div>
                    <div class="index-value">{data['a_stock']['shanghai']['value']}</div>
                    <div class="index-change {sh_change_class}">{data['a_stock']['shanghai']['change']}</div>
                </div>
                <div class="card index-card">
                    <div class="index-name">{data['a_stock']['shenzhen']['name']}</div>
                    <div class="index-value">{data['a_stock']['shenzhen']['value']}</div>
                    <div class="index-change {sz_change_class}">{data['a_stock']['shenzhen']['change']}</div>
                </div>
                <div class="card index-card">
                    <div class="index-name">{data['a_stock']['chinext']['name']}</div>
                    <div class="index-value">{data['a_stock']['chinext']['value']}</div>
                    <div class="index-change {ch_change_class}">{data['a_stock']['chinext']['change']}</div>
                </div>
            </div>
            <div class="highlight">
                <strong>📈 市场特征：</strong>
                <p>{data['a_stock']['summary']}</p>
            </div>
        </div>

        <!-- 美股市场 -->
        <div class="section">
            <h2 class="section-title">🇺🇸 美股市场概况</h2>
            <div class="grid-3">
                <div class="card index-card">
                    <div class="index-name">{data['us_stock']['dow']['name']}</div>
                    <div class="index-value">{data['us_stock']['dow']['value']}</div>
                    <div class="index-change {dow_change_class}">{data['us_stock']['dow']['change']}</div>
                </div>
                <div class="card index-card">
                    <div class="index-name">{data['us_stock']['sp500']['name']}</div>
                    <div class="index-value">{data['us_stock']['sp500']['value']}</div>
                    <div class="index-change {sp500_change_class}">{data['us_stock']['sp500']['change']}</div>
                </div>
                <div class="card index-card">
                    <div class="index-name">{data['us_stock']['nasdaq']['name']}</div>
                    <div class="index-value">{data['us_stock']['nasdaq']['value']}</div>
                    <div class="index-change {nasdaq_change_class}">{data['us_stock']['nasdaq']['change']}</div>
                </div>
            </div>
            <div class="highlight">
                <strong>🔥 市场表现：</strong>
                <p>{data['us_stock']['summary']}</p>
            </div>
        </div>

        <!-- 走势图 -->
        <div class="section">
            <h2 class="section-title">📈 价格走势图</h2>
            <div class="grid-2">
                <div class="chart-container">
                    <div class="chart-title">A股三大指数走势</div>
                    <canvas id="chinaChart"></canvas>
                </div>
                <div class="chart-container">
                    <div class="chart-title">美股三大指数走势</div>
                    <canvas id="usChart"></canvas>
                </div>
            </div>
        </div>

        <!-- 商品市场 -->
        <div class="section">
            <h2 class="section-title">💰 商品与外汇市场</h2>
            <div class="grid-2">
                <div>
                    <table>
                        <thead>
                            <tr>
                                <th>品种</th>
                                <th>价格</th>
                                <th>涨跌幅</th>
                            </tr>
                        </thead>
                        <tbody>
                            {commodity_rows}
                        </tbody>
                    </table>
                </div>
                <div class="chart-container">
                    <div class="chart-title">大宗商品涨跌幅</div>
                    <canvas id="commodityChart"></canvas>
                </div>
            </div>
        </div>

        <!-- 国际局势 -->
        <div class="section">
            <h2 class="section-title">🌍 市场热点分析</h2>
            {news_items}
        </div>

        <!-- 热门板块 -->
        <div class="section">
            <h2 class="section-title">🏢 热门板块表现</h2>
            <div class="grid-2">
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
                            {gainer_rows}
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
                            {loser_rows}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- 投资建议 -->
        <div class="section">
            <h2 class="section-title">💡 投资建议</h2>
            <div class="advice-box">
                <div class="advice-title">基于当前市场环境的投资策略</div>
                {advice_items}
            </div>
        </div>

        <!-- 风险提示 -->
        <div class="risk-warning">
            <strong>⚠️ 风险提示</strong>
            <p>本报告仅供参考，不构成投资建议。市场有风险，投资需谨慎。地缘政治局势、美联储政策、经济数据等因素可能导致市场大幅波动，请根据自身风险承受能力理性投资。</p>
        </div>

        <!-- 页脚 -->
        <div class="footer">
            <p>数据更新时间：{update_time}</p>
            <p>数据来源：DeepSeek AI 搜索整理 | 由 WorkBuddy 自动化系统每日更新</p>
        </div>
    </div>

    <script>
        // A股走势图
        const chinaCtx = document.getElementById('chinaChart').getContext('2d');
        new Chart(chinaCtx, {{
            type: 'line',
            data: {{
                labels: {china_labels},
                datasets: [{{
                    label: '上证指数',
                    data: {json.dumps(cd['shanghai_data'])},
                    borderColor: '#e74c3c',
                    backgroundColor: 'rgba(231, 76, 60, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }}, {{
                    label: '深证成指',
                    data: {json.dumps(cd['shenzhen_data'])},
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }}, {{
                    label: '创业板指',
                    data: {json.dumps(cd['chinext_data'])},
                    borderColor: '#2ecc71',
                    backgroundColor: 'rgba(46, 204, 113, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            usePointStyle: true,
                            padding: 15
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: false,
                        grid: {{
                            color: 'rgba(0,0,0,0.05)'
                        }}
                    }},
                    x: {{
                        grid: {{
                            display: false
                        }}
                    }}
                }},
                interaction: {{
                    intersect: false,
                    mode: 'index'
                }}
            }}
        }});

        // 美股走势图
        const usCtx = document.getElementById('usChart').getContext('2d');
        new Chart(usCtx, {{
            type: 'line',
            data: {{
                labels: {us_labels},
                datasets: [{{
                    label: '道琼斯',
                    data: {json.dumps(cd['dow_data'])},
                    borderColor: '#9b59b6',
                    backgroundColor: 'rgba(155, 89, 182, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }}, {{
                    label: '标普500',
                    data: {json.dumps(cd['sp500_data'])},
                    borderColor: '#f39c12',
                    backgroundColor: 'rgba(243, 156, 18, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }}, {{
                    label: '纳斯达克',
                    data: {json.dumps(cd['nasdaq_data'])},
                    borderColor: '#1abc9c',
                    backgroundColor: 'rgba(26, 188, 156, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            usePointStyle: true,
                            padding: 15
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: false,
                        grid: {{
                            color: 'rgba(0,0,0,0.05)'
                        }}
                    }},
                    x: {{
                        grid: {{
                            display: false
                        }}
                    }}
                }},
                interaction: {{
                    intersect: false,
                    mode: 'index'
                }}
            }}
        }});

        // 商品涨跌幅图
        const commodityCtx = document.getElementById('commodityChart').getContext('2d');
        new Chart(commodityCtx, {{
            type: 'bar',
            data: {{
                labels: {commodity_names},
                datasets: [{{
                    label: '涨跌幅(%)',
                    data: {json.dumps(commodity_changes)},
                    backgroundColor: [{', '.join(commodity_colors)}],
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        grid: {{
                            color: 'rgba(0,0,0,0.05)'
                        }}
                    }},
                    x: {{
                        grid: {{
                            display: false
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""
    
    return html


def main():
    print("📊 开始获取金融数据...")
    
    # 获取金融分析数据
    data = get_financial_analysis()
    
    if not data:
        print("❌ 获取数据失败")
        return
    
    print("✅ 数据获取成功")
    print(f"📅 报告日期: {data.get('report_date', '未知')}")
    
    # 生成 HTML
    print("📝 生成 HTML 报告...")
    html = generate_html(data)
    
    # 保存文件
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ index.html 已生成")


if __name__ == "__main__":
    main()
