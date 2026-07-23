(function () {
  "use strict";

  const typeLabels = {
    product_case: "产品案例",
    builder_insight: "Builder 方法",
    model_capability: "模型能力",
    market_signal: "市场信号",
    business_policy: "商业与政策",
    early_signal: "早期信号"
  };
  const stageLabels = {
    validated: "已有市场验证",
    early_growth: "早期增长",
    proof_of_concept: "原型 / Demo",
    not_applicable: "阶段未公开"
  };

  function text(value, fallback) {
    const normalized = String(value || "").trim();
    return normalized || fallback || "未公开";
  }

  function list(value) {
    return Array.isArray(value) ? value.filter(Boolean).map(String) : [];
  }

  function option(select, value, label) {
    const node = document.createElement("option");
    node.value = value;
    node.textContent = label || value;
    select.appendChild(node);
  }

  function unique(products, key) {
    return Array.from(new Set(products.flatMap((product) => {
      const value = product[key];
      return Array.isArray(value) ? value : value ? [value] : [];
    }).map(String))).sort((a, b) => a.localeCompare(b, "zh-CN"));
  }

  function field(card, label, value) {
    const row = document.createElement("p");
    const strong = document.createElement("strong");
    strong.textContent = label + "：";
    row.appendChild(strong);
    row.appendChild(document.createTextNode(text(value)));
    card.appendChild(row);
  }

  function listField(card, label, values) {
    const entries = list(values);
    if (!entries.length) return;
    const title = document.createElement("strong");
    title.textContent = label + "：";
    card.appendChild(title);
    const ul = document.createElement("ul");
    entries.forEach((entry) => {
      const li = document.createElement("li");
      li.textContent = entry;
      ul.appendChild(li);
    });
    card.appendChild(ul);
  }

  function renderCard(product) {
    const card = document.createElement("article");
    card.className = "product-card";

    const heading = document.createElement("h2");
    const link = document.createElement("a");
    link.textContent = text(product.product_name, product.title);
    link.href = text(product.url, "#");
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    heading.appendChild(link);
    card.appendChild(heading);

    const badges = document.createElement("div");
    badges.className = "product-badges";
    [
      typeLabels[product.intelligence_type] || product.intelligence_type,
      stageLabels[product.product_stage] || product.product_stage,
      product.region === "china" ? "中国" : "全球",
      product.score ? product.score + "/10" : ""
    ].filter(Boolean).forEach((value) => {
      const badge = document.createElement("span");
      badge.textContent = value;
      badges.appendChild(badge);
    });
    card.appendChild(badges);

    field(card, "团队 / Builder", product.builder_name);
    field(card, "目标用户", product.target_user);
    field(card, "用户问题", product.user_problem);
    field(card, "产品信号", product.product_signal || product.summary);
    field(card, "市场验证", product.market_reaction || product.market_signal);
    field(card, "商业模式", product.business_model);
    listField(card, "新工作流", product.product_workflow);
    listField(card, "工具与数据", product.tool_stack);
    listField(card, "可迁移方法", product.transferable_lessons);
    listField(card, "最小 MVP 路径", product.mvp_path);
    listField(card, "技能信号", product.skill_signals);

    const footer = document.createElement("small");
    footer.textContent = "首次发现 " + text(product.first_seen) + " · 最近更新 " + text(product.last_seen);
    card.appendChild(footer);
    return card;
  }

  document.addEventListener("DOMContentLoaded", async function () {
    const root = document.getElementById("product-database");
    if (!root) return;
    const status = document.getElementById("product-status");
    const results = document.getElementById("product-results");
    const search = document.getElementById("product-search");
    const type = document.getElementById("product-type");
    const stage = document.getElementById("product-stage");
    const region = document.getElementById("product-region");
    const vertical = document.getElementById("product-vertical");

    let products = [];
    try {
      const response = await fetch(root.dataset.source, { cache: "no-store" });
      if (!response.ok) throw new Error("HTTP " + response.status);
      const payload = await response.json();
      products = Array.isArray(payload.products) ? payload.products : [];
    } catch (error) {
      status.textContent = "数据库尚未生成或读取失败。请先成功运行一次 daily-summary 工作流。";
      return;
    }

    unique(products, "intelligence_type").forEach((value) => option(type, value, typeLabels[value] || value));
    unique(products, "product_stage").forEach((value) => option(stage, value, stageLabels[value] || value));
    unique(products, "region").forEach((value) => option(region, value, value === "china" ? "中国" : "全球"));
    unique(products, "verticals").forEach((value) => option(vertical, value, value));

    function render() {
      const query = search.value.trim().toLocaleLowerCase("zh-CN");
      const filtered = products.filter((product) => {
        const haystack = JSON.stringify(product).toLocaleLowerCase("zh-CN");
        return (!query || haystack.includes(query)) &&
          (!type.value || product.intelligence_type === type.value) &&
          (!stage.value || product.product_stage === stage.value) &&
          (!region.value || product.region === region.value) &&
          (!vertical.value || list(product.verticals).includes(vertical.value));
      });
      results.replaceChildren(...filtered.map(renderCard));
      status.textContent = "共 " + products.length + " 个产品记录，当前显示 " + filtered.length + " 个。";
    }

    [search, type, stage, region, vertical].forEach((control) => {
      control.addEventListener(control === search ? "input" : "change", render);
    });
    render();
  });
}());
