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

## 自己架

Fork → Settings → Pages → Source 選 `main` → 完事。
