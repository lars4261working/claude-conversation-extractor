# Claude Conversation Extractor

從 Claude 匯出的 `conversations.json` 中提取檔案與對話內容。  
Extract files and chat history from Claude's exported `conversations.json`.

## 兩種使用方式

### 網頁版 (推薦)

直接在瀏覽器中使用，不需要安裝任何東西：

**[https://你的帳號.github.io/倉庫名稱/]()**

- 上傳你的 `conversations.json`
- 勾選要提取的對話和選項
- 下載 ZIP

所有資料在瀏覽器本地處理，不會上傳到任何伺服器。

> 也可以直接用瀏覽器打開 `index.html`

### CLI 版

```bash
python3 extract_files.py
```

Python 3.7+，不需要額外套件。支援互動式選單操作。

## 功能

| 功能 | 網頁版 | CLI 版 |
|------|--------|--------|
| 提取檔案 (.md .py .html ...) | ✓ | ✓ |
| 提取對話 — Markdown (人類可讀) | ✓ | ✓ |
| 提取對話 — JSON (程式可讀) | ✓ | ✓ |
| 副檔名篩選 | ✓ | ✓ |
| 日期前綴開關 | ✓ | ✓ |
| 中/英文切換 | ✓ | ✓ |
| 搜尋/篩選對話 | ✓ | - |
| 全選/取消全選 | ✓ | - |
| 列出對話清單 | ✓ | `list` |

## 輸出結構

每個對話一個資料夾，所有內容放在一起：

```
extracted/
├── 001_Python接收Discord指令執行bash/
│   ├── 001_Python接收Discord指令執行bash_chat.md    ← 對話紀錄
│   ├── 001_Python接收Discord指令執行bash_chat.json   ← 對話紀錄
│   └── (這個對話沒有產生檔案)
│
├── 016_伊朗局勢對黃金美元美股石油的影響/
│   ├── 016_伊朗局勢..._chat.md
│   ├── 016_伊朗局勢..._chat.json
│   └── 史詩之怒行動第13天_市場簡報.md  ← Claude 產生的檔案
└── ...
```

開啟日期前綴時：`001_2026-03-15_Python接收Discord指令執行bash/`

## 部署到 GitHub Pages

1. 建立 GitHub repository
2. 把這些檔案推上去
3. 到 Settings → Pages → Source 選 `main` branch
4. 等幾分鐘，網址就會生效：`https://你的帳號.github.io/倉庫名稱/`

## 檔案說明

| 檔案 | 用途 |
|------|------|
| `index.html` | 網頁版（單檔，可獨立使用） |
| `extract_files.py` | CLI 版 |
| `conversations.json` | Claude 匯出的對話資料（你的資料，勿上傳） |

> **注意**：`conversations.json` 包含你的私人對話，推上 GitHub 前請確認 `.gitignore` 有排除它。

## .gitignore 建議

```
conversations.json
projects.json
users.json
extracted_files/
```
