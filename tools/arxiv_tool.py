#!/usr/bin/env python3
"""
arXiv 论文处理与混沌理论分析工具
使用 pypdf 处理 PDF 文本提取、搜索、分析
"""

import pypdf
import json
import requests
import sys
from pathlib import Path

ARXIV_API = "https://export.arxiv.org/api/query"
PROJECT_DIR = Path("/home/devbox/project")

def download_arxiv_paper(arxiv_id, output_path=None):
    """从 arXiv 下载论文 PDF"""
    if output_path is None:
        output_path = PROJECT_DIR / f"{arxiv_id}.pdf"
    
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    
    print(f"正在下载: {pdf_url}")
    print(f"保存到: {output_path}")
    
    try:
        response = requests.get(pdf_url, stream=True, timeout=60)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"下载成功: {output_path}")
        return output_path
    except Exception as e:
        print(f"下载失败: {e}")
        return None

def extract_pdf_text(pdf_path, max_chars=5000):
    """使用 pypdf 提取 PDF 文本内容"""
    print(f"提取 PDF 文本: {pdf_path}")
    
    try:
        reader = pypdf.PdfReader(pdf_path)
        
        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            full_text += text + "\n\n"
        
        print(f"总字符数: {len(full_text)}")
        return full_text
    except Exception as e:
        print(f"文本提取失败: {e}")
        return None

def search_in_pdf(pdf_path, search_query, case_sensitive=False):
    """在 PDF 文本中搜索特定内容"""
    print(f"在 PDF 中搜索: '{search_query}'")
    
    try:
        reader = pypdf.PdfReader(pdf_path)
        
        matches = []
        for page_num, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            
            if case_sensitive:
                if search_query not in text:
                    continue
            elif search_query.lower() not in text.lower():
                    continue
            
            if search_query in text:
                matches.append({
                    'page': page_num,
                    'line_start': text.find(search_query),
                    'context': text[max(0, text.find(search_query)-50):50] + search_query + text[text.find(search_query):text.find(search_query)+len(search_query):text.find(search_query)+50]
                })
        
        print(f"找到 {len(matches)} 处匹配")
        return matches
    except Exception as e:
        print(f"搜索失败: {e}")
        return []

def analyze_chaos_terms(text):
    """分析文本中的混沌理论相关术语"""
    print("分析混沌理论相关术语...")
    
    chaos_terms = [
        'lyapunov', 'entropy', 'attractor', 'butterfly effect',
        'ergodicity', 'chaos', 'sensitivity', 'fractal',
        'nonlinear', 'deterministic', 'stochastic', 'phase space',
        'bifurcation', 'strange attractor', 'period doubling'
    ]
    
    found_terms = []
    for term in chaos_terms:
        if term.lower() in text.lower():
            found_terms.append(term)
    
    print(f"找到的混沌理论术语: {len(found_terms)}")
    for term in found_terms[:10]:
        print(f"  - {term}")
    
    return found_terms

def main_workflow(arxiv_id):
    """完整工作流程：下载、提取、分析"""
    print("=" * 70)
    print(f"处理论文: {arxiv_id}")
    print("=" * 70)
    
    # 步骤1: 下载 PDF
    pdf_path = download_arxiv_paper(arxiv_id)
    if pdf_path is None:
        print("无法继续（下载失败）")
        return
    
    # 步骤2: 提取文本
    text = extract_pdf_text(pdf_path, max_chars=3000)
    if text is None:
        print("无法继续（文本提取失败）")
        return
    
    # 步骤3: 分析混沌理论术语
    chaos_terms = analyze_chaos_terms(text)
    
    # 保存结果
    result = {
        'arxiv_id': arxiv_id,
        'pdf_path': str(pdf_path),
        'chaos_terms': chaos_terms,
        'text_length': len(text)
    }
    
    result_path = PROJECT_DIR / f"{arxiv_id}_analysis.json"
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"分析结果已保存: {result_path}")
    
    return result_path

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arxiv_id = sys.argv[1]
        print(f"处理指定的论文: {arxiv_id}")
        result = main_workflow(arxiv_id)
    else:
        print("使用方法:")
        print("  python3 arxiv_tool.py <arxiv_id>")
        print("\n示例:")
        print("  python3 arxiv_tool.py 2501.16673")
