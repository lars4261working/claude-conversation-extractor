# Claude Conversation Extractor

Claude 匯出的 `conversations.json` 太大包，裡面對話、檔案、artifact 全混在一起根本沒法看。

這工具把它拆開，一個對話一個資料夾，該有的都有。

## 用法

### 網頁版

開瀏覽器直接用，不用裝東西：

**https://lars4261working.github.io/claude-conversation-extractor/**

丟 `conversations.json` 進去 → 勾你要的 → 下載 ZIP，結束。

全部都在瀏覽器跑，資料不會傳到任何地方。

本地也能用，直接開 `index.html` 就行。

### CLI 版

```bash
python3 extract_files.py
```

Python 3.7+，零依賴。跑起來是互動選單，照著選就好。

## 能幹嘛

- 把對話裡 Claude 產的檔案撈出來（.md .py .html 什麼都有）
- 對話內容轉成好讀的 Markdown 或程式能吃的 JSON
- 可以按副檔名篩選只要特定類型
- 檔名可以選要不要帶日期
- 支援中/英/日文切換

## 拆出來長這樣

```
extracted/
├── 001_Python接收Discord指令執行bash/
│   ├── 001_..._chat.md      ← 對話內容（人看的）
│   ├── 001_..._chat.json    ← 對話內容（程式吃的）
│   └── script.py            ← Claude 當時產的檔案
│
├── 016_伊朗局勢對黃金美元美股石油的影響/
│   ├── 016_..._chat.md
│   ├── 016_..._chat.json
│   └── 市場簡報.md
└── ...
```

帶日期的話：`001_2026-03-15_Python接收Discord指令執行bash/`

## 自己架

1. Fork 或 clone 這個 repo
2. Settings → Pages → Source 選 `main`
3. 等一下就能用了

## 檔案

| 檔案 | 幹嘛的 |
|------|--------|
| `index.html` | 網頁版，單檔搞定 |
| `extract_files.py` | CLI 版 |

## 注意

`conversations.json` 是你的私人對話，別推上 GitHub。`.gitignore` 已經幫你擋了。
