# 部署指南

## 方式一：使用 CloudBase 云开发（推荐）

### 步骤 1：开通云开发
1. 访问 [腾讯云控制台](https://console.cloud.tencent.com/tcb)
2. 点击"新建环境"，选择"按量计费"（有免费额度）
3. 记录环境ID（例如：env-xxxxxx）

### 步骤 2：安装 CLI 工具
```bash
npm install -g @cloudbase/cli
```

### 步骤 3：登录并部署
```bash
# 登录
tcb login

# 部署（替换为您的环境ID）
tcb hosting deploy ./ -e env-xxxxxx
```

### 步骤 4：访问网站
部署成功后，访问地址为：
```
https://您的环境ID.tcloudbaseapp.com
```

---

## 方式二：使用 GitHub Pages

### 步骤 1：创建 GitHub 仓库
1. 在 GitHub 创建新仓库（例如：market-analysis）
2. 上传项目文件

### 步骤 2：开启 Pages
1. 进入仓库 Settings → Pages
2. Source 选择 "main" 分支
3. 点击 Save

### 步骤 3：访问网站
```
https://您的用户名.github.io/market-analysis
```

---

## 方式三：使用 Vercel

### 步骤 1：安装 Vercel CLI
```bash
npm install -g vercel
```

### 步骤 2：部署
```bash
vercel
```

按照提示操作，完成后会获得访问地址。

---

## 自动更新配置

网站已经配置了 WorkBuddy 自动化任务：
- 更新时间：每天早上 9:00
- 自动更新 index.html 文件
- 保持数据最新

如需修改更新时间，请编辑自动化任务配置。