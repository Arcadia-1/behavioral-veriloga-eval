const DATA_URL = "data/model_eval_roster.json";
const LANGUAGE_KEY = "vabench-dashboard-language";

const I18N = {
  en: {
    documentTitle: "Run vaBench Model Eval",
    brandSubtitle: "Behavioral Verilog-A Benchmark",
    navHome: "Home",
    navLeaderboard: "Leaderboard",
    navBenchmark: "Benchmark",
    navRunModels: "Run Models",
    navProtocol: "Protocol",
    navAccuracy: "Accuracy",
    navNews: "News",
    navContributors: "Contributors",
    languageToggle: "中文",
    languageToggleAria: "Switch guide language to Chinese",
    heroEyebrow: "Model evaluation guide",
    heroTitle: "Run vaBench with a new model",
    heroText:
      "Use one public runner to list the model roster, run a one-task smoke test, score generated Verilog-A with EVAS, and optionally send the same candidates through Spectre as the final judge.",
    primaryAction: "Start with a smoke test",
    secondaryAction: "Read the result contract",
    tocTitle: "On this page",
    tocCompatibility: "Compatibility",
    tocPrerequisites: "Prerequisites",
    tocSmoke: "Smoke test",
    tocRun: "Run with a model",
    tocSpectre: "Spectre final judge",
    tocCustom: "Custom models",
    tocResults: "Results",
    compatibilityTitle: "What models can run?",
    compatibilityBody:
      "Any model is testable once it can be called through the runner's API contract. Today that means OpenAI-compatible chat completions, Anthropic messages-compatible endpoints, or a local/provider proxy that exposes one of those shapes.",
    directOpenAITitle: "Direct path",
    directOpenAIBody:
      "Providers such as DeepSeek work when their base URL and model name expose an OpenAI-compatible chat completions endpoint.",
    adapterTitle: "Adapter path",
    adapterBody:
      "If a provider uses another request format, put an OpenAI-compatible proxy in front of it or add a small adapter before claiming benchmark support.",
    judgeTitle: "Judge boundary",
    judgeBody:
      "EVAS is the fast development gate. Spectre is still the final paper-facing judge for reported model scores.",
    prerequisitesTitle: "Prerequisites",
    prereqPython: "Python 3 in the repository environment.",
    prereqRelease:
      'The vaBench release package and current model roster under <code>benchmark-vabench-release-v1/reports/</code>.',
    prereqKey:
      'A provider key passed through an environment variable or <code>--api-key-file</code>. Do not put keys directly in shell history.',
    prereqSpectre: 'Cadence/Spectre access only when running <code>--final-judge spectre</code>.',
    listRosterTitle: "List the current roster",
    smokeTitle: "Smoke test",
    smokeBody:
      "Start with one row. This proves that task selection, prompting, provider access, candidate extraction, and EVAS scoring are wired correctly before spending a full run.",
    deepseekSmokeTitle: "DeepSeek V4 Flash smoke",
    verifiedSmoke: "smoke verified",
    smokeInterpretTitle: "How to read the smoke result",
    smokeInterpretBody:
      "API success means the run generated a candidate and wrote an EVAS result. The candidate may still fail behavior correctness; that is a model-quality result, not an integration failure.",
    runTitle: "Run with a model",
    runBody:
      "For a development baseline, run EVAS first. The output root contains generated candidates, raw responses, EVAS scores, and the unified summary files.",
    evasOnlyTitle: "EVAS-only baseline",
    fastGate: "fast gate",
    apiFormatHelp: "Use <code>openai</code> or <code>anthropic</code>.",
    proxyHelp: "Optional. Use it only when the provider needs a local or network proxy.",
    filterHelp: "Use these for cheap targeted runs before full-roster execution.",
    resumeHelp: "Resume a partially completed run without regenerating completed samples.",
    spectreTitle: "Run the Spectre final judge",
    spectreBody:
      "Use Spectre for leaderboard or paper-facing claims. The runner first performs generation plus EVAS scoring, then sends the selected candidates to the Spectre dual-judge runner.",
    spectreCommandTitle: "Full eval with Spectre",
    requiresSpectre: "requires Spectre",
    claimAllowedNote:
      'The summary marks <code>claim_allowed</code> false unless Spectre ran to completion and no backend produced an inconclusive result.',
    customTitle: "Custom models and agents",
    customBody:
      "If a model cannot speak the existing API formats, keep the benchmark protocol fixed and adapt only the model-call layer. The evaluator expects candidate Verilog-A files and deterministic run metadata; it does not require the model provider to be built into the benchmark.",
    customStep1:
      "Expose the provider through an OpenAI-compatible proxy, or add a narrow adapter in the generation runner.",
    customStep2:
      "Run <code>--print-commands</code> to inspect the planned EVAS and Spectre stages without spending API calls.",
    customStep3:
      "Run one task with <code>--limit 1</code>, then scale to the full roster after the output schema looks correct.",
    previewTitle: "Command preview",
    noApiSpend: "no API spend",
    resultsTitle: "Results",
    resultsBody:
      "Every run writes a single top-level summary. Use it for dashboards, comparisons, and future leaderboard submissions.",
    summaryJsonHelp:
      "Machine-readable status, selected roster size, EVAS counts, optional Spectre counts, and claim gate.",
    summaryMdHelp: "Human-readable run report for quick review.",
    generationHelp: "Generated candidates, raw model responses, generation metadata, and EVAS score artifacts.",
    spectreHelp:
      'Optional Spectre dual-judge artifacts when <code>--final-judge spectre</code> is used.',
    footerGenerated: "Generated from vaBench release reports.",
    rosterStatus: "ready",
    loadingStatus: "loading",
    loadError:
      "Could not load model roster data. Run python3 runners/export_vabench_eval_framework.py, then serve docs/ over HTTP. {message}",
    lastExported: "Last exported {date}",
    scoredRows: "Scored rows",
    scoredRowsDetail: "rows commercial models should run",
    entries: "Entries",
    entriesDetail: "function-level scored entries",
    goldAligned: "Gold aligned",
    goldAlignedDetail: "Spectre-aligned before model scoring",
    promotedRows: "Promoted rows",
    promotedRowsDetail: "new rows inside the 300 surface",
  },
  zh: {
    documentTitle: "运行 vaBench 模型评测",
    brandSubtitle: "行为级 Verilog-A 基准",
    navHome: "首页",
    navLeaderboard: "排行榜",
    navBenchmark: "Benchmark",
    navRunModels: "运行模型",
    navProtocol: "协议",
    navAccuracy: "精度",
    navNews: "更新",
    navContributors: "贡献者",
    languageToggle: "English",
    languageToggleAria: "切换为英文界面",
    heroEyebrow: "模型评测指南",
    heroTitle: "用新模型运行 vaBench",
    heroText:
      "用一个公开 runner 完成名单查看、单题 smoke、EVAS 快速评分，并可选地把同一批候选送到 Spectre 作为最终判定。",
    primaryAction: "从 smoke test 开始",
    secondaryAction: "查看结果契约",
    tocTitle: "本页目录",
    tocCompatibility: "可接入范围",
    tocPrerequisites: "前置条件",
    tocSmoke: "Smoke test",
    tocRun: "运行模型",
    tocSpectre: "Spectre 最终判定",
    tocCustom: "自定义模型",
    tocResults: "结果",
    compatibilityTitle: "哪些模型可以跑？",
    compatibilityBody:
      "只要模型能通过 runner 的 API 契约被调用，就可以测试。目前直接支持 OpenAI-compatible chat completions、Anthropic messages-compatible endpoint，或暴露这两类接口的本地/服务商 proxy。",
    directOpenAITitle: "直接接入",
    directOpenAIBody:
      "DeepSeek 这类服务商只要 base URL 和 model name 暴露 OpenAI-compatible chat completions endpoint，就能直接跑。",
    adapterTitle: "适配器接入",
    adapterBody:
      "如果服务商请求格式不同，需要在前面放一个 OpenAI-compatible proxy，或者先补一个小 adapter，再声称 benchmark support。",
    judgeTitle: "裁判边界",
    judgeBody:
      "EVAS 是快速开发门控；论文或排行榜口径的最终模型分数仍然需要 Spectre 判定。",
    prerequisitesTitle: "前置条件",
    prereqPython: "仓库环境中可用的 Python 3。",
    prereqRelease:
      'vaBench release package 以及 <code>benchmark-vabench-release-v1/reports/</code> 下的当前 model roster。',
    prereqKey:
      '通过环境变量或 <code>--api-key-file</code> 传入服务商 key。不要把 key 直接写进 shell history。',
    prereqSpectre: '只有运行 <code>--final-judge spectre</code> 时才需要 Cadence/Spectre 访问权限。',
    listRosterTitle: "查看当前评测名单",
    smokeTitle: "Smoke test",
    smokeBody:
      "先跑 1 行。这可以在全量花费前验证题目选择、prompt、服务商访问、候选提取和 EVAS 评分是否接好。",
    deepseekSmokeTitle: "DeepSeek V4 Flash smoke",
    verifiedSmoke: "smoke 已验证",
    smokeInterpretTitle: "如何理解 smoke 结果",
    smokeInterpretBody:
      "API 成功表示已经生成候选并写出 EVAS 结果。候选仍可能行为正确性失败；这是模型质量结果，不是接入失败。",
    runTitle: "运行一个模型",
    runBody:
      "开发 baseline 时先跑 EVAS。输出目录会包含生成候选、原始响应、EVAS 分数和统一 summary 文件。",
    evasOnlyTitle: "仅 EVAS baseline",
    fastGate: "快速门控",
    apiFormatHelp: "使用 <code>openai</code> 或 <code>anthropic</code>。",
    proxyHelp: "可选。只有服务商需要本地或网络代理时才使用。",
    filterHelp: "全量运行前，用这些参数做低成本定向测试。",
    resumeHelp: "恢复未完成运行，不重新生成已经完成的样本。",
    spectreTitle: "运行 Spectre 最终判定",
    spectreBody:
      "排行榜或论文口径需要用 Spectre。runner 会先做生成和 EVAS 评分，再把选中的候选送到 Spectre dual-judge runner。",
    spectreCommandTitle: "完整评测含 Spectre",
    requiresSpectre: "需要 Spectre",
    claimAllowedNote:
      '除非 Spectre 完整跑完且没有后端 inconclusive，summary 中的 <code>claim_allowed</code> 会保持 false。',
    customTitle: "自定义模型与 agent",
    customBody:
      "如果模型不支持现有 API 格式，应保持 benchmark protocol 不变，只适配模型调用层。评测器需要的是候选 Verilog-A 文件和确定性的运行元数据，不要求服务商内置在 benchmark 里。",
    customStep1:
      "通过 OpenAI-compatible proxy 暴露服务商，或在 generation runner 中补一个窄 adapter。",
    customStep2:
      "用 <code>--print-commands</code> 查看计划执行的 EVAS 和 Spectre 阶段，不消耗 API。",
    customStep3:
      "先用 <code>--limit 1</code> 跑单题，确认输出 schema 正确后再扩大到完整 roster。",
    previewTitle: "命令预览",
    noApiSpend: "不消耗 API",
    resultsTitle: "结果",
    resultsBody:
      "每次运行都会写一个顶层 summary。后续看板、模型比较和排行榜提交都应该基于它。",
    summaryJsonHelp:
      "机器可读状态、选中的 roster 大小、EVAS 计数、可选 Spectre 计数和 claim gate。",
    summaryMdHelp: "便于快速查看的人类可读运行报告。",
    generationHelp: "生成候选、模型原始响应、生成元数据和 EVAS 评分产物。",
    spectreHelp: '使用 <code>--final-judge spectre</code> 时生成的 Spectre dual-judge 产物。',
    footerGenerated: "由 vaBench release reports 生成。",
    rosterStatus: "就绪",
    loadingStatus: "加载中",
    loadError:
      "无法加载 model roster 数据。请运行 python3 runners/export_vabench_eval_framework.py，然后通过 HTTP 服务打开 docs/。{message}",
    lastExported: "最近导出 {date}",
    scoredRows: "计分行",
    scoredRowsDetail: "商业模型应运行的行",
    entries: "Entries",
    entriesDetail: "功能级计分 entries",
    goldAligned: "Gold 对齐",
    goldAlignedDetail: "模型计分前已完成 Spectre 对齐",
    promotedRows: "新增行",
    promotedRowsDetail: "300 表面中的新增行",
  },
};

const FALLBACK_COMMANDS = {
  list_roster: "python3 runners/run_vabench_model_eval.py --list",
  deepseek_v4_flash_smoke:
    "python3 runners/run_vabench_model_eval.py --model deepseek-v4-flash --base-url https://api.deepseek.com --api-format openai --api-key-file <key-file> --limit 1 --final-judge none --proxy-url <proxy-url-if-needed>",
  evas_only_baseline:
    "python3 runners/run_vabench_model_eval.py --model <model> --base-url <url> --api-format openai --api-key-file <key-file> --final-judge none --tag <tag> --resume",
  full_eval_with_spectre:
    "python3 runners/run_vabench_model_eval.py --model <model> --base-url <url> --api-format openai --api-key-file <key-file> --final-judge spectre --tag <tag> --resume",
};

const state = {
  language: localStorage.getItem(LANGUAGE_KEY) === "zh" ? "zh" : "en",
  payload: null,
};

function t(key) {
  return I18N[state.language]?.[key] || I18N.en[key] || key;
}

function format(key, values) {
  return t(key).replace(/\{(\w+)\}/g, (_, name) => values[name] ?? "");
}

function number(value) {
  if (typeof value !== "number" || !Number.isFinite(value)) {
    return "-";
  }
  return value.toLocaleString(state.language === "zh" ? "zh-CN" : "en-US");
}

function byId(id) {
  return document.getElementById(id);
}

function make(tag, className, content) {
  const element = document.createElement(tag);
  if (className) {
    element.className = className;
  }
  if (content !== undefined) {
    element.textContent = content;
  }
  return element;
}

function prettyCommand(command) {
  return String(command || "")
    .replaceAll(" --", " \\\n  --")
    .replaceAll(" <key-file>", " <key-file>");
}

function applyStaticTranslations() {
  document.documentElement.lang = state.language === "zh" ? "zh-Hans" : "en";
  document.title = t("documentTitle");
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.textContent = t(element.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-html]").forEach((element) => {
    element.innerHTML = t(element.dataset.i18nHtml);
  });
  document.querySelectorAll("[data-i18n-aria-label]").forEach((element) => {
    element.setAttribute("aria-label", t(element.dataset.i18nAriaLabel));
  });
  const toggle = byId("language-toggle");
  if (toggle) {
    toggle.setAttribute("aria-pressed", state.language === "zh" ? "true" : "false");
  }
}

function renderCards(payload) {
  const summary = payload.summary || {};
  const cards = [
    [t("scoredRows"), summary.scored_model_row_count, t("scoredRowsDetail")],
    [t("entries"), summary.entry_count, t("entriesDetail")],
    [t("goldAligned"), summary.gold_aligned_rows, t("goldAlignedDetail")],
    [t("promotedRows"), summary.promoted_v1_1_rows, t("promotedRowsDetail")],
  ];
  byId("roster-cards").replaceChildren(
    ...cards.map(([label, value, detail]) => {
      const card = make("article", "metric-card");
      card.append(make("span", "", label), make("strong", "", number(value)), make("p", "", detail));
      return card;
    }),
  );
}

function commandMap(payload) {
  return {
    ...FALLBACK_COMMANDS,
    ...(payload.example_commands || {}),
    list_roster: FALLBACK_COMMANDS.list_roster,
  };
}

function renderCommands(payload) {
  const commands = commandMap(payload);
  byId("command-list-roster").textContent = prettyCommand(commands.list_roster);
  byId("command-deepseek-smoke").textContent = prettyCommand(commands.deepseek_v4_flash_smoke);
  byId("command-evas-only").textContent = prettyCommand(commands.evas_only_baseline);
  byId("command-full-spectre").textContent = prettyCommand(commands.full_eval_with_spectre);
}

function renderStatus(payload) {
  const status = byId("roster-status");
  status.textContent = t("rosterStatus");
  status.className = `status ${payload.status === "ready" ? "pass" : "warn"}`;
  byId("generated-at").textContent = payload.date ? format("lastExported", { date: payload.date }) : "";
}

function renderAll() {
  if (!state.payload) {
    return;
  }
  renderCards(state.payload);
  renderCommands(state.payload);
  renderStatus(state.payload);
}

function showError(error) {
  const main = document.querySelector("main");
  const message = make("div", "load-error", format("loadError", { message: error.message }));
  main.prepend(message);
}

function initLanguageToggle() {
  const toggle = byId("language-toggle");
  if (!toggle) {
    return;
  }
  toggle.addEventListener("click", () => {
    state.language = state.language === "zh" ? "en" : "zh";
    localStorage.setItem(LANGUAGE_KEY, state.language);
    applyStaticTranslations();
    renderAll();
  });
}

async function boot() {
  initLanguageToggle();
  applyStaticTranslations();
  try {
    const response = await fetch(DATA_URL);
    if (!response.ok) {
      throw new Error(`${DATA_URL}: ${response.status}`);
    }
    state.payload = await response.json();
    renderAll();
  } catch (error) {
    showError(error);
    console.error(error);
    const status = byId("roster-status");
    if (status) {
      status.textContent = t("loadingStatus");
      status.className = "status warn";
    }
  }
}

boot();
