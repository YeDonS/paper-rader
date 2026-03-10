#!/usr/bin/env python3
import argparse
import json
import re
import ssl
import sys
import urllib.request
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / 'output' / 'pdf_cache'


def slugify(text: str) -> str:
    s = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    return s[:80] or 'paper'


def download(url: str, out: Path):
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and out.stat().st_size > 0:
        return out
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={'User-Agent': 'paper-radar/0.2'})
    with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
        out.write_bytes(resp.read())
    return out


def clean(text: str) -> str:
    text = text.replace('\x00', ' ')
    text = re.sub(r'-\n', '', text)
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def split_sentences(text: str):
    parts = re.split(r'(?<=[\.!?])\s+|(?<=[。！？])', text)
    return [p.strip() for p in parts if len(p.strip()) > 20]


def grab_section(full_text: str, names, fallback_start=0, span=6000):
    lower = full_text.lower()
    starts = []
    for name in names:
        m = re.search(rf'\b{name}\b', lower)
        if m:
            starts.append(m.start())
    if starts:
        start = min(starts)
    else:
        start = fallback_start
    end = min(len(full_text), start + span)
    return full_text[start:end].strip()


def summarize_sentences(text: str, limit=4):
    sents = split_sentences(clean(text))
    if not sents:
        return []
    picked = []
    for s in sents:
        ls = s.lower()
        if any(k in ls for k in ['we ', 'our ', 'this paper', 'this work', 'propose', 'design', 'method', 'evaluation', 'results', 'throughput', 'latency', 'speedup', 'overhead']):
            picked.append(s)
        if len(picked) >= limit:
            break
    if len(picked) < limit:
        for s in sents:
            if s not in picked:
                picked.append(s)
            if len(picked) >= limit:
                break
    return picked[:limit]


def analyze(pdf_path: Path, title: str, abstract: str):
    reader = PdfReader(str(pdf_path))
    pages = min(len(reader.pages), 12)
    texts = []
    for i in range(pages):
        try:
            texts.append(reader.pages[i].extract_text() or '')
        except Exception:
            continue
    full = clean(' '.join(texts))
    intro = grab_section(full, ['introduction', 'overview'], 0, 7000)
    method = grab_section(full, ['methodology', 'method', 'design', 'approach', 'system design'], max(len(intro)//2,0), 9000)
    exp = grab_section(full, ['evaluation', 'experiments', 'experimental setup', 'results'], max(len(method)//2,0), 9000)

    intro_pts = summarize_sentences(intro or abstract, 3)
    method_pts = summarize_sentences(method or abstract, 5)
    exp_pts = summarize_sentences(exp or abstract, 4)

    focus = '通用系统'
    lower = (title + ' ' + abstract + ' ' + method[:2000]).lower()
    if any(k in lower for k in ['lsm', 'rocksdb', 'ssd', 'nvme', 'storage', 'file system']):
        focus = '存储 / KV / SSD'
    elif any(k in lower for k in ['cache', 'memory', 'cxl', 'chiplet', 'prefetch']):
        focus = '架构 / 内存系统'
    elif any(k in lower for k in ['cluster', 'runtime', 'scheduler', 'serverless', 'distributed']):
        focus = '系统 / 集群 / 运行时'
    elif any(k in lower for k in ['llm', 'inference', 'serving', 'training', 'moe']):
        focus = 'AI Infra / Serving'

    core = method_pts[0] if method_pts else (intro_pts[0] if intro_pts else abstract[:120])
    flow = method_pts[:5] if method_pts else intro_pts[:5]
    if len(flow) < 5:
        defaults = [
            '定义输入和目标 workload。',
            '构造核心模块与执行路径。',
            '补资源管理、调度或存储机制。',
            '在代表性场景中执行。',
            '给出性能和成本结果。',
        ]
        for d in defaults:
            if len(flow) >= 5:
                break
            flow.append(d)

    return {
        'mode': 'pdf' if full else 'abstract',
        'pages_scanned': pages,
        'focus': focus,
        'intro_points': intro_pts,
        'method_points': method_pts,
        'experiment_points': exp_pts,
        'core_take': core,
        'flow_steps': flow[:5],
        'raw_excerpt': clean((method or intro or exp)[:3500]),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--title', required=True)
    ap.add_argument('--pdf-url', required=True)
    ap.add_argument('--summary', default='')
    args = ap.parse_args()

    cache = CACHE / f"{slugify(args.title)}.pdf"
    try:
        pdf_path = download(args.pdf_url, cache)
        data = analyze(pdf_path, args.title, args.summary)
        json.dump(data, sys.stdout, ensure_ascii=False)
    except Exception as e:
        json.dump({'mode': 'abstract', 'error': str(e), 'focus': '通用系统', 'intro_points': [], 'method_points': [], 'experiment_points': [], 'core_take': args.summary[:120], 'flow_steps': [], 'raw_excerpt': ''}, sys.stdout, ensure_ascii=False)


if __name__ == '__main__':
    main()
