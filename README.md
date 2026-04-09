# Claude Conversation Extractor

Claude 匯出的 `conversations.json` 太大包，對話、檔案、artifact 全混在一起沒法看。

這工具把它拆開，一個對話一個資料夾。

## 用法

### 網頁版

**https://lars4261working.github.io/claude-conversation-extractor/**

丟 JSON 進去，勾你要的，下載 ZIP。全程瀏覽器本地處理。

也能直接開 `index.html` 離線用。

### CLI 版

```bash
python3 extract_files.py
```

Python 3.7+，零依賴。

## 功能

- 撈出對話裡 Claude 產的檔案（.md .py .html 等等）
- 對話轉 Markdown 或 JSON
- 副檔名篩選
- 檔名可帶日期前綴
- 中／英／日文

## 輸出範例

```
extracted/
├── 001_週末晚餐食譜推薦/
│   ├── 001_週末晚餐食譜推薦_chat.md
│   ├── 001_週末晚餐食譜推薦_chat.json
│   └── 紅燒牛肉麵食譜.md
│
├── 002_React登入頁面開發/
│   ├── 002_React登入頁面開發_chat.md
│   ├── 002_React登入頁面開發_chat.json
│   ├── LoginPage.jsx
│   └── auth.py
│
├── 003_日本旅遊行程規劃/
│   ├── 003_日本旅遊行程規劃_chat.md
│   └── 003_日本旅遊行程規劃_chat.json
└── ...
```

## 自己架

Fork → Settings → Pages → Source 選 `main` → 完事。

注意 `conversations.json` 是你的對話紀錄，記得加進 `.gitignore` 別推上去。
