#!/usr/bin/env python3
"""
智能摘要生成器 - 为齿科数字化资讯生成摘要和重要程度评估
"""

import re
from typing import Dict, List, Tuple

def assess_importance(title: str, summary: str, source: str) -> Tuple[str, int]:
    """
    评估文章重要程度
    
    Returns:
        (emoji, importance_score): emoji表示重要程度，score用于排序
    """
    title_lower = title.lower()
    summary_lower = summary.lower()
    full_text = title_lower + " " + summary_lower
    
    # 高重要性关键词
    high_importance_keywords = [
        'launch', 'release', 'new product', 'breakthrough', 'revolutionary',
        'first', 'world premiere', 'major update', 'industry standard',
        'clinical trial', 'research study', 'scientific paper',
        '发布', '推出', '首发', '突破', '革命性', '临床试验', '研究论文'
    ]
    
    # 中重要性关键词  
    medium_importance_keywords = [
        'update', 'upgrade', 'improvement', 'enhancement', 'feature',
        'conference', 'exhibition', 'trade show', 'event', 'webinar',
        'case study', 'clinical case', 'workflow', 'integration',
        '更新', '升级', '改进', '展会', '会议', '案例研究', '工作流程'
    ]
    
    # 检查高重要性
    for keyword in high_importance_keywords:
        if keyword in full_text:
            return "🔴", 3
    
    # 检查中重要性
    for keyword in medium_importance_keywords:
        if keyword in full_text:
            return "🟡", 2
    
    # 默认低重要性
    return "🟢", 1

def generate_summary(title: str, summary: str, source: str) -> str:
    """
    生成简洁摘要
    """
    # 如果摘要太短，直接使用标题
    if len(summary.strip()) < 50:
        return title
    
    # 提取关键信息
    sentences = re.split(r'[.!?。！？]+', summary)
    if len(sentences) > 0:
        # 取前1-2个句子作为摘要
        key_sentences = sentences[:2]
        clean_summary = '. '.join([s.strip() for s in key_sentences if s.strip()])
        if clean_summary:
            return clean_summary + '.'
    
    return summary[:200] + "..." if len(summary) > 200 else summary

def extract_technical_terms(text: str) -> List[str]:
    """
    提取技术术语
    """
    technical_terms = []
    terms_to_check = [
        'CAD/CAM', 'intraoral scanner', '3D printing', 'digital workflow',
        'AI', 'artificial intelligence', 'machine learning', 'cloud',
        'implant', 'orthodontics', 'prosthodontics', 'restoration',
        '数字化', '口内扫描', '3D打印', '人工智能', '种植体', '正畸', '修复'
    ]
    
    text_lower = text.lower()
    for term in terms_to_check:
        if term.lower() in text_lower:
            technical_terms.append(term)
    
    return list(set(technical_terms))

def format_article_for_telegram(article: Dict) -> str:
    """
    格式化文章为 Telegram 消息
    """
    importance_emoji, importance_score = assess_importance(
        article['title'], article['summary'], article['source']
    )
    
    summary = generate_summary(
        article['title'], article['summary'], article['source']
    )
    
    technical_terms = extract_technical_terms(
        article['title'] + " " + article['summary']
    )
    
    message = f"{importance_emoji} <b>{article['source']}</b>\n"
    message += f"🔗 <a href='{article['link']}'>{article['title']}</a>\n"
    message += f"📝 {summary}\n"
    
    if technical_terms:
        message += f"🏷️ 技术标签: {', '.join(technical_terms[:3])}\n"
    
    if article.get('published'):
        message += f"⏰ {article['published']}\n"
    
    message += "\n"
    return message, importance_score

if __name__ == "__main__":
    # 测试函数
    test_article = {
        'source': 'Dental Economics',
        'title': 'New Intraoral Scanner Launch Revolutionizes Digital Dentistry',
        'link': 'https://example.com',
        'summary': 'A major breakthrough in intraoral scanning technology has been announced today. The new scanner offers unprecedented accuracy and speed.',
        'published': '2026-02-20'
    }
    
    message, score = format_article_for_telegram(test_article)
    print(f"Importance Score: {score}")
    print(f"Message:\n{message}")