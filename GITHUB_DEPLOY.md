# GitHub Actions 自动部署配置指南

## 📋 概述

本项目已配置 GitHub Actions 自动化工作流，每天北京时间 09:00 自动更新金融数据并部署到 CloudBase。

---

## 🚀 快速开始

### 第一步：创建 GitHub 仓库

1. 登录 GitHub
2. 点击右上角 "+" → "New repository"
3. 填写仓库信息：
   - Repository name: `market-analysis`（或任意名称）
   - Description: 每日金融市场行情分析
   - 选择 Public 或 Private
4. 点击 "Create repository"

### 第二步：上传代码到 GitHub

**方式 A：使用 Git 命令行**

```bash
# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "🎉 初始化金融行情分析网站"

# 添加远程仓库（替换为您的仓库地址）
git remote add origin https://github.com/您的用户名/market-analysis.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

**方式 B：使用 GitHub Desktop**

1. 下载安装 GitHub Desktop
2. 打开项目文件夹
3. File → Add Local Repository
4. Publish repository

**方式 C：网页上传**

1. 打开刚创建的仓库
2. 点击 "uploading an existing file"
3. 拖拽所有文件上传
4. 点击 "Commit changes"

### 第三步：配置 GitHub Secrets

这是最关键的一步！需要添加腾讯云密钥。

1. **获取腾讯云密钥**
   - 访问：https://console.cloud.tencent.com/cam/capi
   - 点击"新建密钥"
   - 复制 `SecretId` 和 `SecretKey`

2. **添加到 GitHub Secrets**
   - 进入 GitHub 仓库
   - Settings → Secrets and variables → Actions
   - 点击 "New repository secret"
   - 添加两个密钥：
     ```
     Name: TENCENTCLOUD_SECRET_ID
     Value: 您的SecretId
     
     Name: TENCENTCLOUD_SECRET_KEY
     Value: 您的SecretKey
     ```

### 第四步：验证配置

1. 进入 Actions 标签页
2. 查看 "每日金融数据更新" 工作流
3. 点击 "Enable workflow"（如果是首次使用）
4. 可以点击 "Run workflow" 手动触发测试

---

## ⏰ 自动更新时间表

- **自动触发**：每天 UTC 01:00（北京时间 09:00）
- **手动触发**：随时可在 Actions 页面手动运行

---

## 🔧 工作流程说明

```
每天 09:00 (北京时间)
    ↓
GitHub Actions 自动运行
    ↓
获取最新日期时间
    ↓
更新 index.html 文件
    ↓
部署到 CloudBase
    ↓
提交更新到 GitHub
    ↓
完成！网站自动更新
```

---

## 📝 工作流文件说明

### `.github/workflows/daily-update.yml`
- 定时任务，每天自动运行
- UTC 时间 01:00（北京时间 09:00）
- 自动更新并部署

### `.github/workflows/manual-update.yml`
- 手动触发任务
- 可以随时在 Actions 页面运行
- 用于测试或紧急更新

---

## 🌐 访问地址

部署成功后，网站访问地址：
```
https://market-analysis-5gxkqa835c2b5bf9.tcloudbaseapp.com/market-analysis/index.html
```

---

## 🛠️ 高级配置

### 修改更新时间

编辑 `.github/workflows/daily-update.yml`：

```yaml
on:
  schedule:
    - cron: '0 1 * * *'  # UTC 时间
```

Cron 表达式说明：
```
┌───────────── 分钟 (0 - 59)
│ ┌───────────── 小时 (0 - 23)
│ │ ┌───────────── 日 (1 - 31)
│ │ │ ┌───────────── 月 (1 - 12)
│ │ │ │ ┌───────────── 星期几 (0 - 6) (0 是星期日)
│ │ │ │ │
* * * * *
```

北京时间转换示例：
- 北京 09:00 = UTC 01:00
- 北京 12:00 = UTC 04:00
- 北京 18:00 = UTC 10:00

### 添加通知功能

可以在工作流中添加通知，例如：
- 邮件通知
- 企业微信/钉钉通知
- Telegram 通知

---

## ❓ 常见问题

### Q1: Actions 运行失败
**A:** 检查 GitHub Secrets 是否正确配置

### Q2: 部署失败
**A:** 检查腾讯云密钥是否有权限访问 CloudBase 环境

### Q3: 时间不对
**A:** 检查 cron 表达式，注意使用 UTC 时间

### Q4: 想立即更新
**A:** 在 Actions 页面手动触发 workflow

---

## 🎉 完成！

配置完成后，您的网站将：
- ✅ 每天自动更新
- ✅ 自动部署到 CloudBase
- ✅ 无需电脑开机
- ✅ 无需手动操作

享受全自动的金融行情网站吧！🚀