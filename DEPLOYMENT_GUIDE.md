# 🚀 Exoplanet AI Discovery Platform - 部署指南

## 📋 部署架構概述

由於這個專案包含前端（React 3D）和後端（FastAPI）兩個部分，您需要分開部署：

```
┌─────────────────┐    ┌─────────────────┐
│   Vercel        │    │   Railway/      │
│   (Frontend)    │◄──►│   Render/       │
│                 │    │   Heroku        │
│ • React 3D      │    │   (Backend)     │
│ • Static Site   │    │ • FastAPI       │
│ • CDN Delivery  │    │ • REST API      │
└─────────────────┘    └─────────────────┘
```

## 🎯 Vercel 部署配置

### **Vercel 表單填寫**

| 欄位 | 值 | 說明 |
|------|-----|------|
| **Framework** | `create-react-app` | React 應用框架 |
| **Build Command** | `cd frontend && npm install && npm run build` | 構建命令 |
| **Output Directory** | `frontend/build` | 輸出目錄 |
| **Install Command** | `cd frontend && npm install` | 安裝依賴 |

### **環境變數配置** (在 Vercel Dashboard 中設置)

```bash
# 後端 API URL
VITE_API_URL=https://your-backend-service.onrender.com
# 或者
REACT_APP_API_URL=https://your-backend-service.onrender.com
```

## 🔧 後端部署選項

### 選項1: Railway (推薦)
1. 註冊 Railway 帳戶
2. 連接 GitHub 倉庫
3. 選擇 `backend` 目錄部署
4. 設定以下配置：
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 選項2: Render
1. 註冊 Render 帳戶
2. 創建新 Web Service
3. 連接 GitHub 倉庫，選擇 `backend` 目錄
4. 設定：
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 選項3: Heroku
1. 安裝 Heroku CLI
2. 創建 Procfile：
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
3. 部署：
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

## 🌐 完整部署流程

### 步驟1: 準備代碼
```bash
# 確保所有更改已提交
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### 步驟2: 部署後端 (選擇其中一個)

#### Railway 部署：
1. 訪問 [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. 選擇倉庫，設定自動部署 `backend` 目錄
4. 等待部署完成，獲取後端 URL（如: `https://your-app.railway.app`）

#### Render 部署：
1. 訪問 [render.com](https://render.com)
2. New → Web Service
3. 連接 GitHub，選擇倉庫，設定根目錄為 `backend`
4. 等待部署完成，獲取後端 URL

### 步驟3: 部署前端到 Vercel

1. **訪問 [vercel.com](https://vercel.com)**
2. **Import Project** → 連接 GitHub 倉庫
3. **設定配置**：
   - Framework: `create-react-app`
   - Build Command: `cd frontend && npm install && npm run build`
   - Output Directory: `frontend/build`
   - Install Command: `cd frontend && npm install`

4. **設定環境變數**：
   - `VITE_API_URL` = `https://your-backend-url.com`

5. **部署**！

### 步驟4: 更新前端 API 調用

確保前端代碼中的 API 調用指向正確的後端 URL：

```javascript
// 在 frontend/src/ 下的相關文件中
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
```

## 🔧 故障排除

### 常見問題

#### 1. 前端無法連接到後端
- 檢查 CORS 設定
- 確認後端 URL 正確
- 檢查網路連線

#### 2. 3D 模型載入失敗
- 確認 public/fonts/ 目錄存在
- 檢查 Three.js 版本兼容性
- 確認 CDN 資源可訪問

#### 3. ML 模型載入失敗
- 確認 .joblib 文件已上傳
- 檢查文件路徑正確性

### 性能優化

#### 前端優化：
- 啟用 Vercel 的 CDN
- 設定快取標頭
- 壓縮靜態資源

#### 後端優化：
- 設定模型快取
- 使用異步處理
- 設定適當的記憶體限制

## 📊 監控和日誌

### Vercel 監控
- 訪問 Vercel Dashboard 查看部署狀態
- 設定錯誤追蹤 (Sentry)
- 監控效能指標

### 後端監控
- 設定日誌記錄
- 監控 API 調用
- 設定健康檢查端點

## 🔄 持續部署

### 自動部署設定
1. **GitHub 設定**: 啟用自動部署鉤子
2. **環境變數**: 在部署服務中設定必要的環境變數
3. **資料庫**: 設定持久化資料存儲（如果需要）

### 版本控制
- 使用語義化版本 (Semantic Versioning)
- 設定部署標籤
- 保留部署歷史記錄

## 💰 成本考量

### 免費方案
- **Vercel**: 100GB/月的免費頻寬
- **Railway**: 512MB RAM, 1GB 儲存空間
- **Render**: 512MB RAM, 100GB 頻寬

### 付費升級
- 根據流量和需求選擇適當的方案
- 監控使用情況，避免意外費用

## 🔐 安全考量

### API 安全
- 設定 API 金鑰驗證
- 啟用速率限制
- 使用 HTTPS

### 環境變數
- 不要在代碼中硬編碼敏感信息
- 使用環境變數管理配置
- 設定適當的訪問權限

## 📞 支援資源

- **Vercel 文檔**: [vercel.com/docs](https://vercel.com/docs)
- **Railway 文檔**: [docs.railway.app](https://docs.railway.app)
- **Render 文檔**: [render.com/docs](https://render.com/docs)
- **React 部署**: [create-react-app.dev](https://create-react-app.dev)

---

**🎉 部署完成後，您將擁有一個完整的雲端 Exoplanet AI Discovery Platform！**
