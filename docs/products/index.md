---
layout: default
title: AI产品情报库
permalink: /products/
---

# AI产品情报库

这里保存日报中识别出的 AI 产品、用户问题、使用流程、AI 的作用、实现思路和学习任务。每天运行后自动去重并更新。

[返回今日日报]({{ '/' | relative_url }}) · [下载 JSON]({{ '/data/product-intelligence.json' | relative_url }}) · [下载 CSV]({{ '/data/product-intelligence.csv' | relative_url }})

<div id="product-database" class="product-database" data-source="{{ '/data/product-intelligence.json' | relative_url }}">
  <div class="product-filters" role="search" aria-label="筛选产品情报">
    <label>搜索
      <input id="product-search" type="search" placeholder="产品、用户问题、知识点……">
    </label>
    <label>情报类型
      <select id="product-type"><option value="">全部</option></select>
    </label>
    <label>地区
      <select id="product-region"><option value="">全部</option></select>
    </label>
    <label>垂直方向
      <select id="product-vertical"><option value="">全部</option></select>
    </label>
  </div>
  <p id="product-status" class="product-status">正在读取数据库……</p>
  <div id="product-results" class="product-results"></div>
</div>

<script src="{{ '/assets/js/products.js' | relative_url }}" defer></script>
