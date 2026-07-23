---
layout: default
title: Horizon AI Daily
---

{% assign zh_posts = site.posts | where: "lang", "zh" %}
{% assign latest = zh_posts | first %}

{% if latest %}
<div class="latest-daily">
{{ latest.content }}
</div>
{% else %}
# Horizon AI Daily

首份中文 AI 日报将在 GitHub Actions 成功运行后显示在这里。
{% endif %}

## 历史日报

<div class="archive-grid">
{% for post in zh_posts %}
  <a class="archive-card" href="{{ post.url | relative_url }}">{{ post.date | date: "%Y-%m-%d" }}</a>
{% else %}
  <span>暂无归档</span>
{% endfor %}
</div>
