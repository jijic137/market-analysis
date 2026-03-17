#!/usr/bin/env node

/**
 * 每日金融市场数据更新脚本
 * 用于自动获取最新数据并更新网站
 */

const fs = require('fs');
const path = require('path');

// 模拟数据获取（实际应从 API 获取）
function getLatestMarketData() {
    const now = new Date();
    const dateStr = now.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
    });
    
    return {
        reportDate: dateStr,
        updateTime: now.toISOString().replace('T', ' ').substr(0, 19),
        // ... 其他数据
    };
}

// 更新 index.html 中的数据
function updateIndexHtml(data) {
    const indexPath = path.join(__dirname, '..', '..', '..', 'index.html');
    let html = fs.readFileSync(indexPath, 'utf8');
    
    // 更新日期
    html = html.replace(
        /<p class="date">.*?<\/p>/,
        `<p class="date">${data.reportDate} | 北京时间 09:00</p>`
    );
    
    // 更新时间戳
    html = html.replace(
        /上次更新: .*?<\/span>/,
        `上次更新: ${data.updateTime}</span>`
    );
    
    // 保存文件
    fs.writeFileSync(indexPath, html, 'utf8');
    console.log('✅ index.html 已更新');
}

// 部署到 CloudBase
function deployToCloudBase() {
    const { execSync } = require('child_process');
    
    try {
        console.log('🚀 开始部署到 CloudBase...');
        execSync('tcb hosting deploy ./ /market-analysis -e market-analysis-5gxkqa835c2b5bf9', {
            stdio: 'inherit',
            cwd: path.join(__dirname, '..', '..', '..')
        });
        console.log('✅ 部署成功！');
    } catch (error) {
        console.error('❌ 部署失败:', error.message);
        process.exit(1);
    }
}

// 主函数
function main() {
    console.log('📊 开始更新金融市场数据...');
    
    // 1. 获取最新数据
    const data = getLatestMarketData();
    console.log('✅ 数据获取完成');
    
    // 2. 更新 HTML 文件
    updateIndexHtml(data);
    
    // 3. 部署到 CloudBase
    if (process.env.AUTO_DEPLOY === 'true') {
        deployToCloudBase();
    } else {
        console.log('ℹ️  自动部署未启用，请手动运行部署命令');
    }
    
    console.log('✨ 更新完成！');
}

// 执行
if (require.main === module) {
    main();
}

module.exports = { getLatestMarketData, updateIndexHtml, deployToCloudBase };