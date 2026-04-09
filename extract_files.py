#!/usr/bin/env python3
"""Extract files and conversations from Claude's conversations.json"""

import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

BASE_DIR = Path(__file__).parent
JSON_PATH = BASE_DIR / "conversations.json"
OUTPUT_DIR = BASE_DIR / "extracted_files"

# ── Global settings ──
USE_DATE_PREFIX = False
LANG = "zh"  # "zh" or "en"

# ─────────────────────────────────────────────
# i18n
# ─────────────────────────────────────────────

STRINGS = {
    "zh": {
        "tool_title":        "Claude 對話提取工具",
        "reading":           "讀取",
        "total_convs":       "共 {n} 個對話",
        "scanning":          "掃描檔案中...",
        "found_files":       "發現 {n} 個檔案，{t} 種類型",
        "menu_1":            "1) 提取檔案       依副檔名篩選 (.md .py .html ...)",
        "menu_2":            "2) 提取對話內容   人類可讀格式 (Markdown)",
        "menu_3":            "3) 提取對話內容   程式可讀格式 (JSON)",
        "menu_4":            "4) 全部提取       檔案 + 對話(兩種格式)",
        "menu_d":            "d) 資料夾日期前綴  目前: [{s}]",
        "menu_l":            "l) 語言 Language   目前: [{s}]",
        "menu_q":            "q) 離開",
        "folder_example":    "資料夾範例:",
        "choose_prompt":     "請選擇 [1-4/d/l/q]: ",
        "invalid_choice":    "請輸入 1-4、d、l 或 q",
        "date_on":           "開",
        "date_off":          "關",
        "date_toggled":      "日期前綴已{s}",
        "date_enabled":      "開啟",
        "date_disabled":     "關閉",
        "example_prefix":    "範例:",
        "conv_range":        "選擇對話範圍:",
        "conv_all":          "all        → 全部 {n} 個對話",
        "conv_list":         "list       → 列出所有對話(含日期)",
        "conv_num":          "輸入編號   → 例: 1 5 10-20 200",
        "conv_q":            "q          → 返回",
        "conv_prompt":       "請選擇: ",
        "conv_selected":     "已選擇 {n} 個對話",
        "conv_invalid_range":"無效範圍:",
        "conv_out_of_range": "超出範圍:",
        "conv_invalid":      "無效輸入:",
        "conv_none":         "沒有選到任何對話",
        "conv_total":        "共 {n} 個對話",
        "file_types_title":  "對話中發現的檔案類型",
        "ext_header":        "副檔名",
        "count_header":      "數量",
        "total_label":       "合計",
        "select_method":     "選擇方式:",
        "sel_by_num":        "輸入編號     → 例: 1 3 5",
        "sel_by_ext":        "輸入副檔名   → 例: .md .py .html",
        "sel_all":           "all          → 全部",
        "sel_skip":          "q            → 跳過檔案提取",
        "sel_prompt":        "請選擇要提取的類型: ",
        "sel_chosen":        "已選擇: {s} (共 {n} 個檔案)",
        "sel_confirm":       "確認? [Y/n]: ",
        "extracting":        "開始提取:",
        "extract_together":  "每個對話一個資料夾，所有內容放在一起",
        "label_files":       "檔案",
        "label_md":          "對話(Markdown)",
        "label_json":        "對話(JSON)",
        "done":              "完成！",
        "done_files":        "提取 {n} 個檔案",
        "done_md":           "{n} 個對話 → _chat.md",
        "done_json":         "{n} 個對話 → _chat.json",
        "output_dir":        "輸出目錄:",
        "bye":               "再見！",
        "part_files":        "檔案 {n} 個({bd})",
        "part_chat":         "對話 {n} 則",
        "no_title":          "無標題",
        "readable_user":     "🧑 使用者",
        "readable_claude":   "🤖 Claude",
        "readable_created":  "建立時間",
        "readable_updated":  "更新時間",
        "readable_thinking": "💭 思考過程",
        "readable_tool_call":"🔧 工具呼叫",
        "readable_result":   "📋",
        "readable_error":    "❌ 錯誤",
        "readable_ok":       "✅ 結果",
        "readable_attach":   "📎 附件",
        "readable_file":     "📁 檔案",
        "list_header_date":  "日期",
        "list_header_title": "標題",
    },
    "en": {
        "tool_title":        "Claude Conversation Extractor",
        "reading":           "Reading",
        "total_convs":       "{n} conversations",
        "scanning":          "Scanning files...",
        "found_files":       "Found {n} files, {t} types",
        "menu_1":            "1) Extract files      filter by extension (.md .py .html ...)",
        "menu_2":            "2) Extract chats      human-readable (Markdown)",
        "menu_3":            "3) Extract chats      machine-readable (JSON)",
        "menu_4":            "4) Extract all        files + chats (both formats)",
        "menu_d":            "d) Date prefix         current: [{s}]",
        "menu_l":            "l) Language            current: [{s}]",
        "menu_q":            "q) Quit",
        "folder_example":    "Folder example:",
        "choose_prompt":     "Choose [1-4/d/l/q]: ",
        "invalid_choice":    "Enter 1-4, d, l, or q",
        "date_on":           "ON",
        "date_off":          "OFF",
        "date_toggled":      "Date prefix {s}",
        "date_enabled":      "enabled",
        "date_disabled":     "disabled",
        "example_prefix":    "Example:",
        "conv_range":        "Select conversations:",
        "conv_all":          "all        → all {n} conversations",
        "conv_list":         "list       → list all conversations (with dates)",
        "conv_num":          "enter #    → e.g. 1 5 10-20 200",
        "conv_q":            "q          → back",
        "conv_prompt":       "Select: ",
        "conv_selected":     "Selected {n} conversations",
        "conv_invalid_range":"Invalid range:",
        "conv_out_of_range": "Out of range:",
        "conv_invalid":      "Invalid input:",
        "conv_none":         "No conversations selected",
        "conv_total":        "{n} conversations",
        "file_types_title":  "File types found in conversations",
        "ext_header":        "Extension",
        "count_header":      "Count",
        "total_label":       "Total",
        "select_method":     "Selection:",
        "sel_by_num":        "Enter #          → e.g. 1 3 5",
        "sel_by_ext":        "Enter extension  → e.g. .md .py .html",
        "sel_all":           "all              → all types",
        "sel_skip":          "q                → skip file extraction",
        "sel_prompt":        "Choose types to extract: ",
        "sel_chosen":        "Selected: {s} ({n} files)",
        "sel_confirm":       "Confirm? [Y/n]: ",
        "extracting":        "Extracting:",
        "extract_together":  "One folder per conversation, all content together",
        "label_files":       "files",
        "label_md":          "chats (Markdown)",
        "label_json":        "chats (JSON)",
        "done":              "Done!",
        "done_files":        "Extracted {n} files",
        "done_md":           "{n} conversations → _chat.md",
        "done_json":         "{n} conversations → _chat.json",
        "output_dir":        "Output:",
        "bye":               "Bye!",
        "part_files":        "{n} files ({bd})",
        "part_chat":         "{n} messages",
        "no_title":          "Untitled",
        "readable_user":     "🧑 User",
        "readable_claude":   "🤖 Claude",
        "readable_created":  "Created",
        "readable_updated":  "Updated",
        "readable_thinking": "💭 Thinking",
        "readable_tool_call":"🔧 Tool call",
        "readable_result":   "📋",
        "readable_error":    "❌ Error",
        "readable_ok":       "✅ Result",
        "readable_attach":   "📎 Attachment",
        "readable_file":     "📁 File",
        "list_header_date":  "Date",
        "list_header_title": "Title",
    },
}


def t(key, **kwargs):
    """Get translated string"""
    s = STRINGS.get(LANG, STRINGS["zh"]).get(key, key)
    return s.format(**kwargs) if kwargs else s


# ─────────────────────────────────────────────
# Utilities
# ─────────────────────────────────────────────

def sanitize_filename(name, max_len=80):
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', name)
    name = name.strip('. ')
    return name[:max_len] if name else "unnamed"


def get_file_ext(filename):
    if '.' in filename:
        ext = '.' + filename.rsplit('.', 1)[-1].lower()
        if re.match(r'^\.[a-z0-9]{1,10}$', ext):
            return ext
    return ''


ARTIFACT_LANG_MAP = {
    "python": ".py", "javascript": ".js", "typescript": ".ts",
    "html": ".html", "text/html": ".html", "css": ".css",
    "json": ".json", "markdown": ".md", "yaml": ".yaml",
    "bash": ".sh", "shell": ".sh", "svg": ".svg",
    "jsx": ".jsx", "tsx": ".tsx", "cpp": ".cpp", "c": ".c",
    "rust": ".rs", "go": ".go", "java": ".java",
    "sql": ".sql", "xml": ".xml", "text": ".txt",
}


def format_timestamp(ts_str):
    if not ts_str:
        return ""
    try:
        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ts_str


def get_conv_date(conv):
    ts = conv.get("created_at", "")
    if not ts:
        return ""
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return ""


def get_title(conv):
    return conv.get("name", "") or t("no_title")


def make_folder_name(idx, conv):
    title = get_title(conv)
    date = get_conv_date(conv)
    if USE_DATE_PREFIX and date:
        return sanitize_filename(f"{idx + 1:03d}_{date}_{title}")
    return sanitize_filename(f"{idx + 1:03d}_{title}")


def make_chat_filename(idx, conv, ext):
    """Generate chat record filename with _chat suffix"""
    title = get_title(conv)
    date = get_conv_date(conv)
    if USE_DATE_PREFIX and date:
        return sanitize_filename(f"{idx + 1:03d}_{date}_{title}_chat") + ext
    return sanitize_filename(f"{idx + 1:03d}_{title}_chat") + ext


# ─────────────────────────────────────────────
# Conversation content formatting
# ─────────────────────────────────────────────

def conv_to_human_readable(conv):
    title = get_title(conv)
    created = format_timestamp(conv.get("created_at", ""))
    updated = format_timestamp(conv.get("updated_at", ""))

    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"- {t('readable_created')}: {created}")
    lines.append(f"- {t('readable_updated')}: {updated}")
    lines.append(f"- UUID: {conv.get('uuid', '')}")
    lines.append("")
    lines.append("---")
    lines.append("")

    for msg in conv.get("chat_messages", []):
        sender = msg.get("sender", "unknown")
        ts = format_timestamp(msg.get("created_at", ""))
        label = t("readable_user") if sender == "human" else t("readable_claude")

        lines.append(f"## {label}　`{ts}`")
        lines.append("")

        for att in msg.get("attachments", []):
            fn = att.get("file_name", "")
            ftype = att.get("file_type", "")
            fsize = att.get("file_size", 0)
            if fn:
                size_str = f" ({fsize} bytes)" if fsize else ""
                lines.append(f"> {t('readable_attach')}: **{fn}** [{ftype}]{size_str}")
                lines.append("")

        for f in msg.get("files", []):
            fn = f.get("file_name", "")
            if fn:
                lines.append(f"> {t('readable_file')}: **{fn}**")
                lines.append("")

        for c in msg.get("content", []):
            ctype = c.get("type", "")

            if ctype == "text":
                text = c.get("text", "")
                if text.strip():
                    lines.append(text)
                    lines.append("")

            elif ctype == "thinking":
                thinking = c.get("thinking", "")
                if thinking.strip():
                    lines.append("<details>")
                    lines.append(f"<summary>{t('readable_thinking')}</summary>")
                    lines.append("")
                    lines.append(thinking)
                    lines.append("")
                    lines.append("</details>")
                    lines.append("")

            elif ctype == "tool_use":
                name = c.get("name", "")
                inp = c.get("input", {})
                if isinstance(inp, dict):
                    summary_parts = []
                    for k, v in inp.items():
                        v_str = str(v)
                        if len(v_str) > 100:
                            v_str = v_str[:100] + "..."
                        summary_parts.append(f"{k}={v_str}")
                    params = ", ".join(summary_parts)
                else:
                    params = str(inp)[:200]
                lines.append(f"> {t('readable_tool_call')}: `{name}`")
                lines.append(f"> ```")
                lines.append(f"> {params[:300]}")
                lines.append(f"> ```")
                lines.append("")

            elif ctype == "tool_result":
                is_error = c.get("is_error", False)
                content = c.get("content", "")
                status = t("readable_error") if is_error else t("readable_ok")
                content_str = str(content)
                if len(content_str) > 500:
                    content_str = content_str[:500] + f"... ({len(content_str)} chars)"
                lines.append(f"> {t('readable_result')} {status}:")
                lines.append(f"> ```")
                lines.append(f"> {content_str}")
                lines.append(f"> ```")
                lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def conv_to_json(conv):
    clean = {
        "uuid": conv.get("uuid", ""),
        "title": get_title(conv),
        "created_at": conv.get("created_at", ""),
        "updated_at": conv.get("updated_at", ""),
        "messages": [],
    }

    for msg in conv.get("chat_messages", []):
        clean_msg = {
            "sender": msg.get("sender", ""),
            "created_at": msg.get("created_at", ""),
            "content": [],
        }

        atts = []
        for att in msg.get("attachments", []):
            atts.append({
                "file_name": att.get("file_name", ""),
                "file_type": att.get("file_type", ""),
                "file_size": att.get("file_size", 0),
                "extracted_content": att.get("extracted_content", ""),
            })
        if atts:
            clean_msg["attachments"] = atts

        files = []
        for f in msg.get("files", []):
            files.append({"file_name": f.get("file_name", "")})
        if files:
            clean_msg["files"] = files

        for c in msg.get("content", []):
            ctype = c.get("type", "")
            if ctype == "text":
                clean_msg["content"].append({"type": "text", "text": c.get("text", "")})
            elif ctype == "thinking":
                clean_msg["content"].append({"type": "thinking", "thinking": c.get("thinking", "")})
            elif ctype == "tool_use":
                clean_msg["content"].append({"type": "tool_use", "name": c.get("name", ""), "input": c.get("input", {})})
            elif ctype == "tool_result":
                clean_msg["content"].append({"type": "tool_result", "name": c.get("name", ""), "is_error": c.get("is_error", False), "content": c.get("content", "")})

        clean["messages"].append(clean_msg)

    return clean


# ─────────────────────────────────────────────
# File scanning
# ─────────────────────────────────────────────

def scan_all_files(data):
    files_by_conv = defaultdict(list)
    ext_stats = defaultdict(int)

    for idx, conv in enumerate(data):
        for msg in conv.get("chat_messages", []):
            for att in msg.get("attachments", []):
                fn = att.get("file_name", "")
                content = att.get("extracted_content", "")
                if fn and content:
                    ext = get_file_ext(fn)
                    if ext:
                        ext_stats[ext] += 1
                        files_by_conv[idx].append((fn, content, "attachment"))

            for c in msg.get("content", []):
                if c.get("type") != "tool_use":
                    continue
                tool_name = c.get("name", "")
                inp = c.get("input", {})
                if not isinstance(inp, dict):
                    continue

                if tool_name in ("create_file", "Write", "write_to_file", "EditFile"):
                    path = inp.get("file_path", inp.get("path", ""))
                    content = inp.get("content", inp.get("file_text", ""))
                    if path and content:
                        fn = Path(path).name
                        ext = get_file_ext(fn)
                        if ext:
                            ext_stats[ext] += 1
                            files_by_conv[idx].append((fn, content, "tool"))

                elif tool_name == "artifacts":
                    atitle = inp.get("title", inp.get("identifier", ""))
                    content = inp.get("content", "")
                    lang = str(inp.get("language", inp.get("type", "") or "")).lower()
                    if not (atitle and content):
                        continue
                    ext = get_file_ext(atitle)
                    if not ext and lang in ARTIFACT_LANG_MAP:
                        ext = ARTIFACT_LANG_MAP[lang]
                        atitle = atitle + ext
                    elif not ext:
                        continue
                    ext_stats[ext] += 1
                    fn = sanitize_filename(atitle)
                    files_by_conv[idx].append((fn, content, "artifact"))

                elif tool_name == "present_files":
                    file_list = inp.get("files", [])
                    if isinstance(file_list, list):
                        for f in file_list:
                            if not isinstance(f, dict):
                                continue
                            fn = f.get("file_name", f.get("name", ""))
                            content = f.get("content", "")
                            if fn and content:
                                ext = get_file_ext(fn)
                                if ext:
                                    ext_stats[ext] += 1
                                    files_by_conv[idx].append((fn, content, "present"))

    return files_by_conv, dict(ext_stats)


# ─────────────────────────────────────────────
# Interactive UI
# ─────────────────────────────────────────────

def show_main_menu():
    global USE_DATE_PREFIX, LANG
    date_status = t("date_on") if USE_DATE_PREFIX else t("date_off")

    print()
    print("=" * 60)
    print(f"  {t('tool_title')}")
    print("=" * 60)
    print()
    print(f"  {t('menu_1')}")
    print(f"  {t('menu_2')}")
    print(f"  {t('menu_3')}")
    print(f"  {t('menu_4')}")
    print(f"  {t('menu_d', s=date_status)}")
    print(f"  {t('menu_l', s=LANG.upper())}")
    print(f"  {t('menu_q')}")
    print()

    example_title = "Python接收Discord指令執行bash" if LANG == "zh" else "Python_Discord_bash"
    if USE_DATE_PREFIX:
        print(f"  {t('folder_example')} 001_2026-03-15_{example_title}/")
    else:
        print(f"  {t('folder_example')} 001_{example_title}/")
    print()

    while True:
        choice = input(f"  {t('choose_prompt')}").strip().lower()
        if choice == 'd':
            USE_DATE_PREFIX = not USE_DATE_PREFIX
            s = t("date_enabled") if USE_DATE_PREFIX else t("date_disabled")
            print(f"  → {t('date_toggled', s=s)}")
            if USE_DATE_PREFIX:
                print(f"    {t('example_prefix')} 001_2026-03-15_xxx/")
            else:
                print(f"    {t('example_prefix')} 001_xxx/")
            print()
            continue
        if choice == 'l':
            LANG = "en" if LANG == "zh" else "zh"
            print(f"  → Language: {LANG.upper()}")
            print()
            return show_main_menu()  # redraw menu
        if choice in ('1', '2', '3', '4', 'q'):
            return choice
        print(f"  ⚠ {t('invalid_choice')}")


def list_conversations(data):
    print()
    print(f"  {'#':<5} {t('list_header_date'):<12} {t('list_header_title')}")
    print(f"  {'-'*5} {'-'*12} {'-'*45}")
    for i, conv in enumerate(data, 1):
        title = get_title(conv)
        date = get_conv_date(conv)
        display_title = title[:50] + ".." if len(title) > 52 else title
        print(f"  {i:<5} {date:<12} {display_title}")
    print(f"  {'-'*5} {'-'*12} {'-'*45}")
    print(f"  {t('conv_total', n=len(data))}")


def select_conversations(data):
    print()
    print(f"  {t('conv_range')}")
    print(f"    {t('conv_all', n=len(data))}")
    print(f"    {t('conv_list')}")
    print(f"    {t('conv_num')}")
    print(f"    {t('conv_q')}")
    print()

    while True:
        choice = input(f"  {t('conv_prompt')}").strip().lower()

        if choice == 'q':
            return None
        if choice == 'list':
            list_conversations(data)
            print()
            continue
        if choice == 'all':
            return list(range(len(data)))

        indices = set()
        valid = True
        for part in choice.split():
            if '-' in part:
                try:
                    a, b = part.split('-', 1)
                    a, b = int(a), int(b)
                    for n in range(a, b + 1):
                        if 1 <= n <= len(data):
                            indices.add(n - 1)
                except ValueError:
                    print(f"  ⚠ {t('conv_invalid_range')} {part}")
                    valid = False
            elif part.isdigit():
                n = int(part)
                if 1 <= n <= len(data):
                    indices.add(n - 1)
                else:
                    print(f"  ⚠ {t('conv_out_of_range')} {part} (1-{len(data)})")
                    valid = False
            else:
                print(f"  ⚠ {t('conv_invalid')} {part}")
                valid = False

        if indices:
            print(f"  {t('conv_selected', n=len(indices))}")
            return sorted(indices)
        elif valid:
            print(f"  ⚠ {t('conv_none')}")


def select_file_types(ext_stats):
    sorted_exts = sorted(ext_stats.items(), key=lambda x: -x[1])

    print()
    print("=" * 60)
    print(f"  {t('file_types_title')}")
    print("=" * 60)
    print(f"  {'#':<5} {t('ext_header'):<12} {t('count_header'):>6}")
    print(f"  {'-'*5} {'-'*12} {'-'*6}")
    for i, (ext, count) in enumerate(sorted_exts, 1):
        print(f"  {i:<5} {ext:<12} {count:>6}")
    print(f"  {'-'*5} {'-'*12} {'-'*6}")
    print(f"  {'':5} {t('total_label'):<12} {sum(ext_stats.values()):>6}")
    print()
    print(f"  {t('select_method')}")
    print(f"    {t('sel_by_num')}")
    print(f"    {t('sel_by_ext')}")
    print(f"    {t('sel_all')}")
    print(f"    {t('sel_skip')}")
    print()

    while True:
        choice = input(f"  {t('sel_prompt')}").strip()
        if not choice or choice.lower() == 'q':
            return set()
        if choice.lower() == 'all':
            return set(ext_stats.keys())

        selected = set()
        for p in choice.split():
            if p.isdigit():
                idx = int(p)
                if 1 <= idx <= len(sorted_exts):
                    selected.add(sorted_exts[idx - 1][0])
            else:
                ext = p if p.startswith('.') else '.' + p
                if ext.lower() in ext_stats:
                    selected.add(ext.lower())

        if selected:
            total = sum(ext_stats.get(e, 0) for e in selected)
            print(f"\n  {t('sel_chosen', s=', '.join(sorted(selected)), n=total)}")
            confirm = input(f"  {t('sel_confirm')}").strip().lower()
            if confirm in ('', 'y', 'yes'):
                return selected
            print()


# ─────────────────────────────────────────────
# Extraction
# ─────────────────────────────────────────────

def get_conv_folder(idx, conv):
    folder_name = make_folder_name(idx, conv)
    folder_path = OUTPUT_DIR / folder_name
    folder_path.mkdir(parents=True, exist_ok=True)
    return folder_path


def write_file_no_overwrite(folder_path, safe_fn, content, is_json=False):
    ext = get_file_ext(safe_fn) or ""
    file_path = folder_path / safe_fn
    counter = 1
    while file_path.exists():
        stem = safe_fn.rsplit('.', 1)[0] if '.' in safe_fn else safe_fn
        file_path = folder_path / f"{stem}_{counter}{ext}"
        counter += 1
    if is_json:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
    else:
        file_path.write_text(content, encoding="utf-8")


def extract_all(data, conv_indices, files_by_conv, selected_exts,
                do_files=False, do_readable=False, do_json=False):
    total_files = 0
    total_readable = 0
    total_json = 0

    for idx in conv_indices:
        conv = data[idx]
        title = get_title(conv)
        date = get_conv_date(conv)
        msg_count = len(conv.get("chat_messages", []))

        parts = []
        folder_path = None

        # ── files ──
        if do_files and idx in files_by_conv:
            seen = {}
            for fn, content, source in files_by_conv[idx]:
                ext = get_file_ext(fn)
                if ext in selected_exts:
                    if fn not in seen or len(content) > len(seen[fn]):
                        seen[fn] = content

            if seen:
                if folder_path is None:
                    folder_path = get_conv_folder(idx, conv)

                for fn, content in seen.items():
                    safe_fn = sanitize_filename(fn)
                    ext = get_file_ext(fn)
                    if not get_file_ext(safe_fn):
                        safe_fn += ext
                    write_file_no_overwrite(folder_path, safe_fn, content)
                    total_files += 1

                ext_bd = defaultdict(int)
                for fn in seen:
                    ext_bd[get_file_ext(fn)] += 1
                bd = ", ".join(f"{e}x{c}" for e, c in sorted(ext_bd.items()))
                parts.append(t("part_files", n=len(seen), bd=bd))

        # ── chat markdown ──
        if do_readable:
            if folder_path is None:
                folder_path = get_conv_folder(idx, conv)
            content = conv_to_human_readable(conv)
            chat_fn = make_chat_filename(idx, conv, ".md")
            write_file_no_overwrite(folder_path, chat_fn, content)
            total_readable += 1
            parts.append(t("part_chat", n=msg_count))

        # ── chat json ──
        if do_json:
            if folder_path is None:
                folder_path = get_conv_folder(idx, conv)
            clean = conv_to_json(conv)
            chat_fn = make_chat_filename(idx, conv, ".json")
            write_file_no_overwrite(folder_path, chat_fn, clean, is_json=True)
            total_json += 1
            if not do_readable:
                parts.append(t("part_chat", n=msg_count))

        if parts:
            info = " + ".join(parts)
            print(f"  [{idx+1:3d}] {date}  {title[:40]:<40} → {info}")

    return total_files, total_readable, total_json


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    print(f"\n  {t('reading')}: {JSON_PATH.name} ...")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"  {t('total_convs', n=len(data))}")

    print(f"  {t('scanning')}")
    files_by_conv, ext_stats = scan_all_files(data)
    print(f"  {t('found_files', n=sum(ext_stats.values()), t=len(ext_stats))}")

    while True:
        mode = show_main_menu()

        if mode == 'q':
            print(f"\n  {t('bye')}")
            break

        conv_indices = select_conversations(data)
        if conv_indices is None:
            continue

        do_files = mode in ('1', '4')
        do_readable = mode in ('2', '4')
        do_json = mode in ('3', '4')

        selected_exts = set()
        if do_files:
            selected_exts = select_file_types(ext_stats)
            if not selected_exts:
                do_files = False
                if mode == '1':
                    continue

        OUTPUT_DIR.mkdir(exist_ok=True)

        print()
        print("=" * 60)
        parts_desc = []
        if do_files:
            parts_desc.append(t("label_files"))
        if do_readable:
            parts_desc.append(t("label_md"))
        if do_json:
            parts_desc.append(t("label_json"))
        print(f"  {t('extracting')} {' + '.join(parts_desc)}")
        print(f"  {t('extract_together')}")
        print("=" * 60)

        nf, nr, nj = extract_all(
            data, conv_indices, files_by_conv, selected_exts,
            do_files=do_files, do_readable=do_readable, do_json=do_json
        )

        print()
        print("=" * 60)
        print(f"  {t('done')}")
        if do_files:
            print(f"    ✓ {t('done_files', n=nf)}")
        if do_readable:
            print(f"    ✓ {t('done_md', n=nr)}")
        if do_json:
            print(f"    ✓ {t('done_json', n=nj)}")
        print(f"  {t('output_dir')} {OUTPUT_DIR}")
        print("=" * 60)


if __name__ == "__main__":
    main()
