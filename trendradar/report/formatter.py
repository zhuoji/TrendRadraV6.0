# coding=utf-8
"""
平台标题格式化模块

提供多平台标题格式化功能
"""

from typing import Dict

from trendradar.report.helpers import clean_title, html_escape, format_rank_display


def format_title_for_platform(
    platform: str, title_data: Dict, show_source: bool = True, show_keyword: bool = False
) -> str:
    """统一的标题格式化方法"""
    # 物理避坑：针对飞书渠道，强制使用 wework 的干净排名格式，彻底干掉 <font> 标签
    if platform == "feishu":
        rank_display = format_rank_display(
            title_data["ranks"], title_data["rank_threshold"], "wework"
        )
    else:
        rank_display = format_rank_display(
            title_data["ranks"], title_data["rank_threshold"], platform
        )

    link_url = title_data["mobile_url"] or title_data["url"]
    cleaned_title = clean_title(title_data["title"])
    keyword = title_data.get("matched_keyword", "") if show_keyword else ""
    title_prefix = "🆕 " if title_data.get("is_new") else ""

    if platform == "feishu":
        if link_url:
            formatted_title = f"[{cleaned_title}]({link_url})"
        else:
            formatted_title = cleaned_title

        if show_source:
            result = f"[{title_data['source_name']}] {title_prefix}{formatted_title}"
        elif show_keyword and keyword:
            result = f"[{keyword}] {title_prefix}{formatted_title}"
        else:
            result = f"{title_prefix}{formatted_title}"

        if rank_display:
            result += f" {rank_display}"
        if title_data["time_display"]:
            result += f" - {title_data['time_display']}"
        if title_data["count"] > 1:
            result += f" ({title_data['count']}次)"
        return result

    # 这里的代码是为其他平台保留的，保持原样即可
    elif platform == "dingtalk":
        if link_url:
            formatted_title = f"[{cleaned_title}]({link_url})"
        else:
            formatted_title = cleaned_title
        if show_source:
            result = f"[{title_data['source_name']}] {title_prefix}{formatted_title}"
        elif show_keyword and keyword:
            result = f"[{keyword}] {title_prefix}{formatted_title}"
        else:
            result = f"{title_prefix}{formatted_title}"
        if rank_display: result += f" {rank_display}"
        if title_data["time_display"]: result += f" - {title_data['time_display']}"
        if title_data["count"] > 1: result += f" ({title_data['count']}次)"
        return result
    else:
        # 其他平台的逻辑按原代码执行，如果报错请告诉我
        return cleaned_title
