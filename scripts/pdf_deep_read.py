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


SECTION_ALIASES = {
    'intro': ['introduction', 'overview', 'background', 'motivation'],
    'method': ['methodology', 'method', 'design', 'approach', 'system design', 'architecture', 'implementation'],
    'exp': ['evaluation', 'experiments', 'experimental setup', 'results', 'performance evaluation'],
}


def slugify(text: str) -> str:
    s = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    return s[:80] or 'paper'


def download(url: str, out: Path):
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and out.stat().st_size > 0:
        return out
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={'User-Agent': 'paper-radar/0.3'})
    with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
        out.write_bytes(resp.read())
    return out


def clean(text: str) -> str:
    text = text.replace('\x00', ' ')
    text = re.sub(r'-\s+', '', text)
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def split_sentences(text: str):
    parts = re.split(r'(?<=[\.!?])\s+|(?<=[。！？])', text)
    return [p.strip() for p in parts if len(p.strip()) > 30]


def find_section_start(full_text: str, names):
    lower = full_text.lower()
    starts = []
    for name in names:
        for pat in [rf'\b{name}\b', rf'\d+\.\s*{name}\b', rf'{name}\s*[:\-]']:
            m = re.search(pat, lower)
            if m:
                starts.append(m.start())
    return min(starts) if starts else -1


def next_section_boundary(full_text: str, start: int):
    if start < 0:
        return min(len(full_text), 9000)
    lower = full_text.lower()[start+50:]
    m = re.search(r'(\b\d+\.\s*[a-z][a-z \-]{3,30}\b|\brelated work\b|\bconclusion\b|\bdiscussion\b|\breferences\b)', lower)
    if not m:
        return min(len(full_text), start + 9000)
    return min(len(full_text), start + 50 + m.start())


def grab_section(full_text: str, group: str, fallback_start=0, span=7000):
    start = find_section_start(full_text, SECTION_ALIASES[group])
    if start < 0:
        start = fallback_start
        end = min(len(full_text), start + span)
    else:
        end = next_section_boundary(full_text, start)
        end = min(end, start + span)
    return full_text[start:end].strip()


def sentence_score(sentence: str, group: str):
    s = sentence.lower()
    score = 0
    common = ['we ', 'our ', 'this paper', 'this work', 'propose', 'design', 'system']
    weights = {
        'intro': ['challenge', 'bottleneck', 'motivation', 'problem', 'limitations'],
        'method': ['approach', 'method', 'architecture', 'pipeline', 'algorithm', 'module', 'design'],
        'exp': ['evaluation', 'results', 'latency', 'throughput', 'speedup', 'overhead', 'cost'],
    }
    for k in common:
        if k in s:
            score += 2
    for k in weights[group]:
        if k in s:
            score += 3
    if re.search(r'\b\d+(\.\d+)?(x|%|ms|s|gb|tb)\b', s):
        score += 2
    score += min(len(sentence) // 80, 3)
    return score


def summarize_sentences(text: str, group: str, limit=4):
    sents = split_sentences(clean(text))
    ranked = sorted(((sentence_score(s, group), i, s) for i, s in enumerate(sents)), reverse=True)
    chosen = sorted(ranked[:limit], key=lambda x: x[1])
    return [x[2] for x in chosen]


def infer_focus(title: str, abstract: str, method: str):
    lower = (title + ' ' + abstract + ' ' + method[:2500]).lower()
    if any(k in lower for k in ['lsm', 'rocksdb', 'ssd', 'nvme', 'storage', 'file system', 'kv store']):
        return '存储 / KV / SSD'
    if any(k in lower for k in ['cache', 'memory', 'cxl', 'chiplet', 'prefetch']):
        return '架构 / 内存系统'
    if any(k in lower for k in ['cluster', 'runtime', 'scheduler', 'serverless', 'distributed', 'faas']):
        return '系统 / 集群 / 运行时'
    if any(k in lower for k in ['llm', 'inference', 'serving', 'training', 'moe']):
        return 'AI Infra / Serving'
    return '通用系统'


def analyze(pdf_path: Path, title: str, abstract: str):
    reader = PdfReader(str(pdf_path))
    pages = min(len(reader.pages), 14)
    texts = []
    for i in range(pages):
        try:
            texts.append(reader.pages[i].extract_text() or '')
        except Exception:
            continue
    full = clean(' '.join(texts))
    intro = grab_section(full, 'intro', 0, 7000)
    method = grab_section(full, 'method', max(len(intro)//2, 0), 9000)
    exp = grab_section(full, 'exp', max(len(method)//2, 0), 9000)

    intro_pts = summarize_sentences(intro or abstract, 'intro', 3)
    method_pts = summarize_sentences(method or abstract, 'method', 5)
    exp_pts = summarize_sentences(exp or abstract, 'exp', 4)
    focus = infer_focus(title, abstract, method)

    flow = method_pts[:5] if method_pts else intro_pts[:5]
    while len(flow) < 5:
        flow.append([
            '定义输入和目标 workload。',
            '构造核心模块与执行路径。',
            '补资源管理、调度或存储机制。',
            '在代表性场景中执行。',
            '给出性能和成本结果。',
        ][len(flow)])

    return {
        'mode': 'pdf' if full else 'abstract',
        'pages_scanned': pages,
        'focus': focus,
        'intro_points': intro_pts,
        'method_points': method_pts,
        'experiment_points': exp_pts,
        'core_take': (method_pts or intro_pts or [abstract[:120]])[0],
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
