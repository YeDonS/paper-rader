#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / 'references' / 'summary-template.md'


def clean(text: str) -> str:
    text = text.replace('\x00', ' ')
    text = re.sub(r'-\s+', '', text)
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_pdf(pdf_path: Path, max_pages=14):
    reader = PdfReader(str(pdf_path))
    pages = min(len(reader.pages), max_pages)
    chunks = []
    for i in range(pages):
        try:
            txt = clean(reader.pages[i].extract_text() or '')
        except Exception:
            txt = ''
        if txt:
            chunks.append(f"[Page {i+1}] {txt[:5000]}")
    return pages, chunks


def build_protocol_prompt(title: str, abstract: str, body_chunk: str, section_name: str):
    protocol = REF.read_text() if REF.exists() else ''
    return f'''你现在是严厉但靠谱的系统论文精读助手。严格遵守下面协议，不要偷懒，不要输出协议解释，不要输出多余寒暄。

【精读协议】
{protocol}

【额外硬规则】
- 全部用中文。
- 不要出现“Section III describes”“Emails:”这种垃圾元信息；看到就忽略。
- 不要输出“通信/RF/边缘硬件”这类前台标签词。
- 只围绕当前要求的小节输出，不要把整篇一次性写完。
- 如果正文信息不足，可以明确写“从当前抽取正文里只能确认到……”，但不能瞎编。
- 输出纯文本，不要 markdown 代码块。

【论文标题】
{title}

【摘要】
{abstract}

【当前抽取正文】
{body_chunk}

【当前任务】
只生成这一小节：{section_name}
'''


def run_gemini(prompt: str):
    try:
        out = subprocess.check_output(['gemini', '-p', prompt], text=True, timeout=240)
        return out.strip(), 'gemini'
    except Exception as e:
        return None, f'gemini:{e}'


def run_openai(prompt: str):
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        return None, 'openai:no_api_key'
    payload = {
        'model': 'gpt-4.1',
        'messages': [
            {'role': 'system', 'content': '你是严格的中文论文精读助手。'},
            {'role': 'user', 'content': prompt},
        ],
        'temperature': 0.2,
    }
    req = urllib.request.Request(
        'https://api.openai.com/v1/chat/completions',
        data=json.dumps(payload).encode(),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        },
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=240) as r:
            data = json.loads(r.read().decode())
        return data['choices'][0]['message']['content'].strip(), 'openai'
    except Exception as e:
        return None, f'openai:{e}'


def llm(prompt: str):
    out, src = run_gemini(prompt)
    if out:
        return out, src
    out2, src2 = run_openai(prompt)
    if out2:
        return out2, src2
    raise RuntimeError(f'LLM failed | {src} | {src2}')


def html_wrap(title: str, sections_html: str, model_used: str):
    safe_title = title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{safe_title} · LLM精读</title><style>
:root{{--bg:#0b1020;--panel:#121a30;--soft:#1a2442;--text:#ecf2ff;--muted:#9fb0d1;--accent:#7c9cff}}*{{box-sizing:border-box}}body{{margin:0;font-family:Inter,system-ui,sans-serif;background:radial-gradient(circle at top,#18254f 0,#0b1020 45%,#0b1020 100%);color:var(--text)}}.wrap{{max-width:1180px;margin:0 auto;padding:24px 20px 70px}}.panel{{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:20px;padding:20px}}section{{margin:0 0 24px 0}}h1,h2,h3{{margin-top:0}}.muted{{color:var(--muted)}}table{{width:100%;border-collapse:collapse}}td,th{{border:1px solid rgba(255,255,255,.08);padding:10px;vertical-align:top}}th{{background:rgba(255,255,255,.05)}}pre{{white-space:pre-wrap;word-break:break-word;background:#10182d;padding:12px;border-radius:12px}}ul,ol{{padding-left:22px}}a{{color:#c8d6ff}}</style></head>
<body><div class="wrap"><div class="panel"><h1>{safe_title}</h1><div class="muted">LLM 精读页（基于 PDF 正文抽取 + 强模型重写，当前来源：{model_used}）</div>{sections_html}</div></div></body></html>'''


def ensure_section(title, sid, body):
    return f'<section id="{sid}"><h2>{title}</h2>{body}</section>'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--title', required=True)
    ap.add_argument('--summary', default='')
    ap.add_argument('--pdf', required=True)
    args = ap.parse_args()

    pages, chunks = extract_pdf(Path(args.pdf))
    body = '\n\n'.join(chunks)

    tasks = [
        ('abs', '0. 摘要翻译'),
        ('motivation', '1. 方法动机'),
        ('design', '2. 方法设计'),
        ('compare', '3. 与其他方法对比'),
        ('exp', '4. 实验表现与优势'),
        ('apply', '5. 学习与应用'),
        ('summary', '6. 总结'),
        ('flow', '方法流程图'),
    ]
    rendered = []
    models = []
    for sid, name in tasks:
        prompt = build_protocol_prompt(args.title, args.summary, body[:24000], name)
        out, src = llm(prompt)
        models.append(src)
        rendered.append(ensure_section(name, sid, out))

    model_used = ', '.join(dict.fromkeys(models))
    html = html_wrap(args.title, ''.join(rendered), model_used)
    json.dump({'ok': True, 'mode': 'llm-pdf', 'pages_scanned': pages, 'html': html, 'model_used': model_used}, sys.stdout, ensure_ascii=False)


if __name__ == '__main__':
    main()
