---
layout: default
title: AI 产品机会与 Builder 情报
---

{% assign zh_posts = site.posts | where: "lang", "zh" %}
{% assign latest = zh_posts | first %}

{% if latest %}
<div class="latest-daily">
{{ latest.content }}
</div>
{% else %}
# AI 产品机会与 Builder 情报

首份中文 AI 日报将在 GitHub Actions 成功运行后显示在这里。
{% endif %}

## 产品情报数据库

[打开可搜索、可筛选的产品数据库]({{ '/products/' | relative_url }})，或直接下载 [JSON]({{ '/data/product-intelligence.json' | relative_url }}) / [CSV]({{ '/data/product-intelligence.csv' | relative_url }})。

[阅读产品 PRD 与完整工作流]({{ '/workflow-product-guide.html' | relative_url }}) · [部署与密钥配置 SOP]({{ '/personal-ai-daily-setup.html' | relative_url }})

## 历史日报

<div class="archive-grid">
{% for post in zh_posts %}
  <a class="archive-card" href="{{ post.url | relative_url }}">{{ post.date | date: "%Y-%m-%d" }}</a>
{% else %}
  <span>暂无归档</span>
{% endfor %}
</div>
