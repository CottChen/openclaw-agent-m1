#!/usr/bin/env python3
"""
arXiv 学术论文深度分析工具（修复版）
使用 pypdf 进行 PDF 文本提取、结构化数据提取、混沌理论分析
专注于：LLM 训练和推理框架、Agent 架构、Multi-Agent 系统、混沌理论、熵脑理论
"""

import pypdf
import json
import requests
import sys
from pathlib import Path
from datetime import datetime
import re

# ==================== 配置 ====================
ARXIV_API = "https://export.arxiv.org/api/query"
PROJECT_DIR = Path("/home/devbox/project")

# 混沌理论关键词列表
CHAOS_TERMS = [
    'lyapunov', 'entropy', 'attractor', 'butterfly effect',
    'ergodicity', 'chaos', 'sensitivity', 'fractal',
    'nonlinear', 'deterministic', 'stochastic', 'phase space',
    'bifurcation', 'strange attractor', 'period doubling'
]

# ==================== 工具函数 ====================

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
        return str(output_path)
    except Exception as e:
        print(f"下载失败: {e}")
        return None

def extract_pdf_metadata(pdf_path):
    """使用 pypdf 提取 PDF 元数据"""
    print(f"分析 PDF 元数据: {pdf_path}")
    
    try:
        reader = pypdf.PdfReader(pdf_path)
        
        metadata = {
            'num_pages': len(reader.pages),
            'is_encrypted': reader.is_encrypted,
            'metadata': reader.metadata
        }
        
        print(f"  页数: {metadata['num_pages']}")
        print(f"  加密: {metadata['is_encrypted']}")
        
        if reader.metadata:
            print("  元数据:")
            for key, value in reader.metadata.items():
                print(f"    {key}: {value}")
        
        return metadata
    except Exception as e:
        print(f"元数据提取失败: {e}")
        return None

def extract_full_text(pdf_path):
    """提取 PDF 完整文本"""
    print(f"提取 PDF 文本: {pdf_path}")
    
    try:
        reader = pypdf.PdfReader(pdf_path)
        
        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            full_text += text + "\n\n"
        
        print(f"  总字符数: {len(full_text)}")
        return full_text
    except Exception as e:
        print(f"文本提取失败: {e}")
        return None

def analyze_chaos_theory_terms(text):
    """分析文本中的混沌理论相关术语"""
    print("分析混沌理论相关术语...")
    
    chaos_terms_found = []
    text_lower = text.lower()
    
    for term in CHAOS_TERMS:
        if term.lower() in text_lower:
            chaos_terms_found.append(term)
    
    print(f"  找到的混沌理论术语: {len(chaos_terms_found)}")
    
    if len(chaos_terms_found) > 0:
        print("  相关术语:")
        for term in sorted(set(chaos_terms_found))[:10]:
            print(f"    - {term}")
    else:
        print("  未找到混沌理论相关术语")
    
    return chaos_terms_found

def complete_paper_analysis(arxiv_id, analysis_modes=None):
    """完整的论文分析流程"""
    print("=" * 70)
    print(f"论文分析: {arxiv_id}")
    print("=" * 70)
    
    # 步骤1: 下载 PDF
    print("\n[步骤 1] 下载 PDF")
    print("-" * 70)
    pdf_path_str = download_arxiv_paper(arxiv_id)
    
    if not pdf_path_str:
        print("❌ 无法继续（下载失败）")
        return
    
    pdf_path = Path(pdf_path_str)
    
    # 步骤2: 提取元数据
    print("\n[步骤 2] 提取元数据")
    print("-" * 70)
    metadata = extract_pdf_metadata(pdf_path)
    
    if not metadata:
        print("❌ 无法继续（元数据提取失败）")
        return
    
    # 步骤3: 提取文本
    print("\n[步骤 3] 提取文本")
    print("-" * 70)
    full_text = extract_full_text(pdf_path)
    
    if not full_text:
        print("❌ 无法继续（文本提取失败）")
        return
    
    # 步骤4: 分析混沌理论术语
    print("\n[步骤 4] 分析混沌理论术语")
    print("-" * 70)
    chaos_analysis = None
    
    if analysis_modes:
        if 'chaos' in analysis_modes or 'all' in analysis_modes:
            chaos_analysis = analyze_chaos_theory_terms(full_text)
    
    # 步骤5: 保存分析结果
    print("\n[步骤 5] 保存分析结果")
    print("-" * 70)
    
    result = {
        'arxiv_id': arxiv_id,
        'pdf_path': str(pdf_path),
        'metadata': metadata,
        'text_length': len(full_text) if full_text else 0,
        'chaos_terms': chaos_analysis if chaos_analysis else [],
        'analyzed': True,
        'analyzed_at': datetime.now().isoformat()
    }
    
    result_path = PROJECT_DIR / f"{arxiv_id}_analysis.json"
    
    try:
        with open(result_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 分析结果已保存: {result_path}")
        print(f"\n分析摘要:")
        print(f"  页数: {metadata.get('num_pages', 0)}")
        print(f"  文本长度: {result['text_length']}")
        if chaos_analysis:
            print(f"  混沌术语数: {len(result['chaos_terms'])}")
        
        return result_path
    except Exception as e:
        print(f"保存结果失败: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arxiv_id = sys.argv[1]
        mode = sys.argv[2] if len(sys.argv) > 2 else None
        
        if mode in ['chaos', 'all']:
            complete_paper_analysis(arxiv_id, analysis_modes=[mode])
        elif mode == 'search':
            search_term = sys.argv[3] if len(sys.argv) > 3 else None
            if search_term:
                pdf_path = PROJECT_DIR / f"{arxiv_id}.pdf"
                
                if pdf_path.exists():
                    print(f"\n[附加任务] 搜索论文内容: '{search_term}'")
                    print("-" * 70)
                    
                    reader = pypdf.PdfReader(pdf_path)
                    
                    matches = []
                    for page_num, page in enumerate(reader.pages, 1):
                        text = page.extract_text()
                        
                        if search_term.lower() in text.lower():
                            start_pos = text.find(search_term)
                            context_start = max(0, start_pos - 50)
                            context_end = start_pos + len(search_term) + 50
                            
                            matches.append({
                                'page': page_num,
                                'line_start': start_pos,
                                'context': text[context_start:context_end]
                            })
                    
                    print(f"\n搜索结果:")
                    print(f"  找到 {len(matches)} 处匹配")
                    
                    for i, match in enumerate(matches[:5]):
                        print(f"{i+1}. 页面 {match['page']}: 位置 {match['line_start']}")
                        print(f"  上下文: {match['context'][:80]}")
                        print()
                else:
                    print("❌ 需要指定搜索词")
                    complete_paper_analysis(arxiv_id)
        else:
            # 帮助信息
            print("=" * 70)
            print("学术论文深度分析工具（修复版）")
            print("=" * 70)
            print("\n使用方法:")
            print()
            print("  python3 /home/devbox/project/paper_analyzer_fixed.py <arxiv_id> [mode]")
            print()
            print("  [mode]:  - chaos - 分析混沌理论相关术语")
            print("  [mode]:  - all - 完整分析（结构 + 混沌理论）")
            print("  [mode]:  - search - 搜索论文中的特定内容")
            print()
            print("示例:")
            print("  # 分析 ODESteer 论文的混沌理论内容")
            print("  python3 /home/devbox/project/paper_analyzer_fixed.py 2602.17560 chaos")
            print()
            print("  # 搜索论文中的 'entropy' 关键词")
            print("  python3 /home/devbox/project/paper_analyzer_fixed.py 2602.17560 search entropy")
            print()
            print("=" * 70)
