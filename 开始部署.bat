@echo off
chcp 65001 >nul
echo ========================================
echo   金融行情网站部署工具
echo ========================================
echo.
echo 请按照以下步骤操作：
echo.
echo 1. 访问 https://console.cloud.tencent.com/tcb
echo 2. 创建云开发环境（按量计费）
echo 3. 开启静态网站托管
echo 4. 在文件管理中上传以下文件：
echo.
echo    需要上传的文件：
echo    - index.html
echo    - history.html
echo    - styles.css
echo    - app.js
echo    - README.md
echo    - data 文件夹（包含 market_data.json）
echo.
echo 5. 上传完成后，访问：
echo    https://您的环境ID.tcloudbaseapp.com
echo.
echo ========================================
echo.
echo 按任意键打开部署指南文档...
pause >nul
start 部署指南.md
echo.
echo 部署指南已打开！
pause