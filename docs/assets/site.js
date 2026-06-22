const DATA = {
  summary: "data/site_summary.json",
  backends: "data/backend_coverage.json",
  alignment: "data/spectre_alignment_table.json",
  tasks: "data/task_gallery.json",
  categories: "data/category_coverage.json",
  modelRoster: "data/model_eval_roster.json",
  precision: "data/precision_overview.json",
};

const LANGUAGE_KEY = "vabench-dashboard-language";

const NEWS_ITEMS = [
  {
    date: "2026-06-22",
    type: "Accuracy",
    title: {
      en: "Precision overview separates equivalence from bit-exact equality",
      zh: "精度总览区分等价通过与 bit-exact 完全相同",
    },
    body: {
      en: "Accuracy now reports full-300 common-row precision evidence, task-metric rows, and pointwise-difference caveats.",
      zh: "Accuracy 页面现在报告 full-300 common-row 精度证据、task-metric 行和逐点差异说明。",
    },
    href: "accuracy.html",
  },
  {
    date: "2026-06-22",
    type: "Docs",
    title: {
      en: "GitHub Pages deployment workflow",
      zh: "GitHub Pages 部署 workflow",
    },
    body: {
      en: "The docs/ site can now be published by GitHub Pages using the checked-in Actions workflow.",
      zh: "docs/ 站点现在可以通过仓库中的 Actions workflow 发布到 GitHub Pages。",
    },
    href: "index.html",
  },
  {
    date: "2026-06-22",
    type: "Release",
    title: {
      en: "Model evaluation guide and unified runner",
      zh: "模型评测指南与统一 runner",
    },
    body: {
      en: "Added a public Run Models page for OpenAI-compatible and Anthropic-compatible model evaluation, including DeepSeek V4 Flash smoke commands.",
      zh: "新增 Run Models 页面，说明 OpenAI-compatible 与 Anthropic-compatible 模型接入，并给出 DeepSeek V4 Flash smoke 命令。",
    },
    href: "run-model-eval.html",
  },
  {
    date: "2026-06-22",
    type: "Benchmark",
    title: {
      en: "vaBench is organized as one 300-row denominator",
      zh: "vaBench 统一为 300 行管理分母",
    },
    body: {
      en: "The 271 inherited rows and 29 promoted rows are now managed as one vaBench 300 surface, with provenance retained only as an audit label.",
      zh: "271 个继承行和 29 个新增行统一管理为 vaBench 300；来源只作为审计标签保留。",
    },
    href: "benchmark.html",
  },
  {
    date: "2026-06-22",
    type: "Protocol",
    title: {
      en: "Golden alignment table clarifies tolerance-gated equivalence",
      zh: "Golden 对齐表明确容差等价口径",
    },
    body: {
      en: "The protocol page separates bit-exact claims from waveform/task-metric parity and keeps Spectre as the final judge.",
      zh: "Protocol 页面区分 bit-exact 与 waveform/task-metric parity，并保持 Spectre 为最终判定。",
    },
    href: "protocol.html",
  },
  {
    date: "2026-06-22",
    type: "Docs",
    title: {
      en: "Website navigation split into benchmark-facing pages",
      zh: "网站导航拆为面向 benchmark 的页面",
    },
    body: {
      en: "Home, Leaderboard, Benchmark, Run Models, Protocol, News, and Contributors now map to separate reader intents.",
      zh: "Home、Leaderboard、Benchmark、Run Models、Protocol、News、Contributors 分别对应不同读者意图。",
    },
    href: "index.html",
  },
];

const VERIFIED_LEADERBOARD_ROWS = [];

const SMOKE_ROWS = [
  {
    model: "deepseek-v4-flash",
    provider: "DeepSeek",
    status: "integration_smoke_passed",
    evas: "generated + scored 1 row; candidate failed behavior correctness",
    spectre: "not run",
  },
];

const I18N = {
  en: {
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
    languageToggleAria: "Switch site language to Chinese",
    footerGenerated: "Generated from vaBench release reports.",
    homeEyebrow: "Behavioral Verilog-A evaluation",
    homeTitle: "vaBench 300",
    homeText:
      "A benchmark and evaluation framework for analog and mixed-signal behavioral Verilog-A tasks. EVAS provides a fast development gate; Spectre remains the final judge for reported scores.",
    homePrimaryAction: "Run a model",
    homeSecondaryAction: "View leaderboard",
    featureBenchmarkEyebrow: "Benchmark",
    featureBenchmarkTitle: "300 released rows",
    featureBenchmarkBody: "Browse tasks by category, level, form, score surface, and provenance.",
    featureLeaderboardEyebrow: "Leaderboard",
    featureLeaderboardTitle: "Model results",
    featureLeaderboardBody: "Separate verified Spectre-scored runs from integration smoke tests.",
    featureProtocolEyebrow: "Protocol",
    featureProtocolTitle: "EVAS/Spectre gates",
    featureProtocolBody: "Track four-backend certification, golden alignment, and tolerance rules.",
    featureAccuracyEyebrow: "Accuracy",
    featureAccuracyTitle: "Precision evidence",
    featureAccuracyBody: "See whether EVAS and Spectre are bit-identical, equivalent, or numerically different.",
    homeLeaderboardEyebrow: "Leaderboard status",
    homeLeaderboardTitle: "Ready for model submissions",
    homeNewsEyebrow: "News",
    homeNewsTitle: "Latest updates",
    viewAllNews: "View all news",
    leaderboardEyebrow: "Leaderboard",
    leaderboardPageTitle: "vaBench model leaderboard",
    leaderboardPageText:
      "Verified rows require Spectre final judging. EVAS-only runs and API smoke tests are shown as integration evidence, not ranked benchmark scores.",
    verifiedRunsEyebrow: "Verified runs",
    verifiedRunsTitle: "Spectre-scored submissions",
    verifiedRunsDescription: "This table stays empty until a model has run the scored roster with Spectre final judge enabled.",
    integrationEyebrow: "Integration status",
    integrationTitle: "Smoke-tested model access",
    submitRunTitle: "Submit or reproduce a run",
    submitRunText: "Use the unified runner first. Publish the top-level summary when a result is ready to rank.",
    benchmarkEyebrow: "Benchmark",
    benchmarkPageTitle: "vaBench 300 task set",
    benchmarkPageText:
      "Browse the benchmark by function family, task form, level, difficulty, and score surface. The public management denominator is 300 rows; the current model-scored roster is 265 rows.",
    coverageEyebrow: "Coverage",
    coverageTitle: "Function categories",
    coverageDescription: "Entry and row coverage across analog and mixed-signal behavioral function families.",
    taskGalleryEyebrow: "Task gallery",
    taskGalleryTitle: "Released rows",
    taskGalleryDescription: "Search and filter the 300 rows. Provenance labels are audit labels, not separate benchmark denominators.",
    protocolEyebrow: "Protocol",
    protocolPageTitle: "Evaluation and certification gates",
    protocolPageText:
      "Spectre is the final judge. EVAS is a fast evaluator that must remain aligned with Spectre on the supported voltage-domain/event-driven subset.",
    backendCertificationEyebrow: "Backend certification",
    backendCertificationTitle: "Four execution surfaces",
    backendCertificationDescription: "These rows certify the benchmark and evaluator surfaces, not model leaderboard rankings.",
    claimBoundaryEyebrow: "Claim boundary",
    claimBoundaryTitle: "What can be claimed",
    parityGatesEyebrow: "Parity gates",
    alignmentEyebrow: "Spectre alignment",
    alignmentTitle: "Golden reference equivalence table",
    alignmentDescription:
      "Each row states what was compared, the measured EVAS/Spectre difference, and the tolerance gate. Bit-exact equality is not asserted.",
    accuracyEyebrow: "Accuracy",
    accuracyPageTitle: "EVAS and Spectre precision",
    accuracyPageText:
      "The benchmark does not claim bit-exact equality. It reports whether each surface is behavior-equivalent to the Spectre reference under explicit gates.",
    accuracyIdenticalEyebrow: "Equivalence answer",
    accuracyIdenticalTitle: "Are the outputs exactly identical?",
    accuracyTermsEyebrow: "Reading tolerance",
    accuracyTermsTitle: "What the gate means",
    precisionStrictEyebrow: "Four-way reference",
    precisionStrictTitle: "Precision vs Spectre strict",
    precisionStrictDescription:
      "EVAS Python, EVAS Rust, and Spectre AX are compared against the same Spectre strict reference on the current full-300 common-row set.",
    spectreAnchorEyebrow: "Tolerance anchor",
    spectreAnchorTitle: "Spectre AX vs classic",
    spectreAnchorDescription:
      "Official Spectre modes are not bit-identical either. This self-consistency report is the reference anchor for deciding what waveform drift is acceptable before calling EVAS mismatched.",
    newsEyebrow: "News",
    newsPageTitle: "Updates and release notes",
    newsPageText: "Track benchmark, evaluator, runner, and documentation changes in one human-readable timeline.",
    contributorsEyebrow: "Contributors",
    contributorsPageTitle: "People and attribution",
    contributorsPageText: "A lightweight place for benchmark maintainers, task authors, evaluator contributors, and citation instructions.",
    maintainersEyebrow: "Maintainers",
    maintainersTitle: "vaBench release maintainers",
    maintainersBody: "Own the public denominator, task metadata, score roster, and report exports.",
    taskAuthorsEyebrow: "Task authors",
    taskAuthorsTitle: "Benchmark task contributors",
    taskAuthorsBody: "Contribute prompts, gold Verilog-A, checkers, and Spectre/EVAS validation evidence.",
    evaluatorContributorsEyebrow: "Evaluator",
    evaluatorContributorsTitle: "EVAS and Spectre harness contributors",
    evaluatorContributorsBody: "Maintain the fast evaluator, dual-judge runner, bridge scripts, and parity regressions.",
    citationTitle: "Citation",
    citationBody: "Replace this block with the paper citation once the benchmark release is frozen.",
    thRank: "Rank",
    thModel: "Model",
    thProvider: "Provider",
    thDate: "Date",
    thScore: "Score",
    thJudge: "Judge",
    thArtifact: "Artifact",
    thStatus: "Status",
    thEVAS: "EVAS",
    thSpectre: "Spectre",
    thCategory: "Category",
    thEntries: "Entries",
    thRows: "Rows",
    thScoredRows: "Scored Rows",
    thTask: "Task",
    thForm: "Form",
    thLevel: "Level",
    thBackends: "Backends",
    thParity: "Parity",
    thBackend: "Backend",
    thBehavior: "Behavior",
    thEvidence: "Evidence",
    thClaim: "Claim",
    thActualDifference: "Actual Difference",
    thToleranceGate: "Tolerance Gate",
    thSurface: "Surface",
    thEquivalentRows: "Equivalent Rows",
    thEffectiveMeanRms: "Effective Mean RMS",
    thEffectiveWorstSignalRms: "Effective Worst Signal RMS",
    thRawMeanRms: "Raw Mean RMS",
    thRawWorstSignalRms: "Raw Worst Signal RMS",
    thTaskMetricRows: "Task-Metric Rows",
    thTaskMetricDelta: "Metric Delta",
    thDiagnosticWaveform: "Diagnostic Waveform",
    thDiagnosticMeanRms: "Diagnostic Mean RMS",
    thDiagnosticWorstSignalRms: "Diagnostic Worst Signal RMS",
    thAcceptancePolicy: "Acceptance Policy",
    thReportingRule: "Reporting Rule",
    thMetric: "Metric",
    thValue: "Value",
    filterSearch: "Search",
    filterCategory: "Category",
    filterForm: "Form",
    filterLevel: "Level",
    filterProvenance: "Provenance",
    filterStatus: "Status",
    filterPolicy: "Policy",
    resetFilters: "Reset",
    taskSearchPlaceholder: "task id, category, function",
    alignmentSearchPlaceholder: "task id, category, policy",
    loadingTaskRows: "Loading task rows...",
    loadingAlignmentRows: "Loading alignment rows...",
    allOption: "All",
    noRowsMatch: "No rows match the current filters.",
    noVerifiedRuns: "No verified model submissions yet.",
    noVerifiedRunsDetail: "Run a model with --final-judge spectre before adding a ranked row.",
    notRanked: "not ranked",
    integrationSmokePassed: "integration smoke passed",
    notRun: "not run",
    generatedScoredFailed: "generated and EVAS-scored 1 row; candidate failed behavior correctness",
    listRoster: "list roster",
    evasOnlyBaseline: "EVAS-only baseline",
    fullEvalWithSpectre: "full eval with Spectre",
    rowsShown: "{shown} of {total} rows shown",
    alignmentRowsShown: "{shown} of {total} alignment rows shown",
    rowsWithRate: "{passed} / {total} rows ({rate})",
    missingCheckers: "{count} missing checkers",
    certified: "certified",
    notCertified: "not certified",
    staticBackend: "static",
    evasBackend: "EVAS",
    spectreBackend: "Spectre",
    spectreRef: "Spectre ref",
    spectreAx: "Spectre AX",
    evasRust: "EVAS Rust",
    evasPython: "EVAS Python",
    counted: "counted",
    notCounted: "not counted",
    meanRmsLine: "mean RMS {mean}, worst {worst}",
    gainDeltaLine: "gain delta {delta}",
    acceptanceBasis: "Acceptance basis",
    bitExactEquality: "Bit-exact equality",
    relativeRmsGate: "Relative RMS gate",
    smallAbsoluteGate: "Small absolute gate",
    gainMetricGate: "Gain metric gate",
    pllRows: "PLL rows",
    edgeWindowPolicy: "Edge window policy",
    metricBenchmarkRows: "Benchmark rows",
    metricScoredRows: "Scored model rows",
    metricFourBackend: "Four-backend status",
    metricMismatch: "EVAS PASS / Spectre FAIL",
    metricReleaseEntries: "Release entries",
    metricCategories: "Categories",
    metricAlignedRows: "Gold aligned rows",
    metricBitExact: "Bit-exact claim",
    metricBackendCertified: "Certified backends",
    metricFourwayRows: "Precision evidence rows",
    metricEquivalentSurfaces: "Equivalent surfaces",
    metricPrecisionComparisons: "Gate-passed comparisons",
    metricReviewRows: "Rows needing review",
    metricSpectreSelf: "Spectre self-check",
    metricTaskMetricRows: "Task-metric comparisons",
    detailSingleDenominator: "single public management denominator",
    detailModelRoster: "rows commercial models should run",
    detailCertifiedSurfaces: "certified execution surfaces",
    detailAuditedMismatch: "audited mismatch count",
    detailFunctionEntries: "function-level entries behind rows",
    detailFunctionFamilies: "analog and mixed-signal families",
    detailSpectreAligned: "aligned within stated tolerance gates",
    detailNotAsserted: "not asserted",
    detailNotBitExact: "not a bit-exact promise",
    detailCommonRows: "single public management denominator",
    detailPrecisionRows: "current full-300 common-row evidence",
    detailEquivalentSurfaces: "EVAS Python, EVAS Rust, Spectre AX",
    detailPrecisionComparisons: "surface-row comparisons passed",
    detailReviewRows: "precision rows blocked or needing review",
    detailSpectreSelf: "AX/classic pairs passed",
    detailTaskMetricRows: "accepted by extracted circuit metrics",
    identicalNoTitle: "No bit-exact claim",
    identicalNoBody: "EVAS outputs and Spectre outputs are not claimed to match point-by-point or bit-for-bit.",
    equivalentYesTitle: "Equivalent under gates",
    equivalentYesBody: "On the current full-300 common-row evidence, EVAS Python, EVAS Rust, and Spectre AX pass the Spectre-strict-referenced gates.",
    differenceTitle: "What differs",
    differenceBody: "The remaining numerical differences are mainly solver sampling, event timing, interpolation, edge windows, transition/cross details, and task-metric extraction.",
    toleranceAnchorTitle: "Where tolerance comes from",
    toleranceAnchorBody: "The tolerance is anchored by observed Spectre AX/classic self-consistency, not by an arbitrary decimal precision.",
    pointwiseEyebrow: "Pointwise caveats",
    pointwiseTitle: "Why raw RMS can look larger",
    pointwiseDescription:
      "These categories explain why a waveform-only pointwise comparison can differ even when the row passes behavior or task-metric acceptance.",
    taskMetricEyebrow: "Task-metric rows",
    taskMetricTitle: "Rows not judged by raw pointwise equality",
    taskMetricDescription:
      "Measurement-flow rows can use extracted circuit metrics as the acceptance gate. Diagnostic waveform-only RMS is shown to avoid misreading the row as a functional mismatch.",
    anchorComparedPairs: "Compared pairs",
    anchorPassedPairs: "Passed pairs",
    anchorNeedsReviewPairs: "Needs review pairs",
    anchorRowMeanMax: "Row mean relative RMS max",
    anchorWorstSignalMax: "Worst-signal relative RMS max",
    anchorMaxPointAbs: "Max point absolute voltage",
    loadError:
      "Could not load vaBench site data. Run python3 runners/export_vabench_eval_framework.py, python3 runners/export_vabench_github_pages.py, and python3 runners/export_vabench_precision_overview.py, then serve docs/ over HTTP. {message}",
  },
  zh: {
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
    footerGenerated: "由 vaBench release reports 生成。",
    homeEyebrow: "行为级 Verilog-A 评测",
    homeTitle: "vaBench 300",
    homeText:
      "面向模拟与混合信号行为级 Verilog-A 任务的 benchmark 和评测框架。EVAS 是快速开发门控；论文和排行榜分数仍以 Spectre 为最终判定。",
    homePrimaryAction: "运行模型",
    homeSecondaryAction: "查看排行榜",
    featureBenchmarkEyebrow: "Benchmark",
    featureBenchmarkTitle: "300 个 released rows",
    featureBenchmarkBody: "按类别、层级、表单、计分面和来源浏览题目。",
    featureLeaderboardEyebrow: "排行榜",
    featureLeaderboardTitle: "模型结果",
    featureLeaderboardBody: "区分 Spectre 计分的 verified runs 和接入 smoke tests。",
    featureProtocolEyebrow: "协议",
    featureProtocolTitle: "EVAS/Spectre gates",
    featureProtocolBody: "查看四后端认证、golden alignment 和容差规则。",
    featureAccuracyEyebrow: "精度",
    featureAccuracyTitle: "精度证据",
    featureAccuracyBody: "查看 EVAS 与 Spectre 是完全相同、gate 内等价，还是存在数值差异。",
    homeLeaderboardEyebrow: "排行榜状态",
    homeLeaderboardTitle: "已准备接收模型提交",
    homeNewsEyebrow: "更新",
    homeNewsTitle: "最近更新",
    viewAllNews: "查看所有更新",
    leaderboardEyebrow: "排行榜",
    leaderboardPageTitle: "vaBench 模型排行榜",
    leaderboardPageText:
      "Verified rows 需要 Spectre 最终判定。EVAS-only runs 和 API smoke tests 只作为接入证据展示，不作为正式排行分数。",
    verifiedRunsEyebrow: "Verified runs",
    verifiedRunsTitle: "Spectre 计分提交",
    verifiedRunsDescription: "只有模型使用 Spectre final judge 跑完 scored roster 后，才会进入这张表。",
    integrationEyebrow: "接入状态",
    integrationTitle: "已 smoke-test 的模型访问",
    submitRunTitle: "提交或复现一次运行",
    submitRunText: "先使用统一 runner。结果可排名时发布顶层 summary。",
    benchmarkEyebrow: "Benchmark",
    benchmarkPageTitle: "vaBench 300 题目集",
    benchmarkPageText:
      "按功能族、任务表单、层级、难度和计分面浏览 benchmark。公开管理分母是 300 行；当前模型计分 roster 是 265 行。",
    coverageEyebrow: "覆盖",
    coverageTitle: "功能类别",
    coverageDescription: "模拟与混合信号行为功能族的 entry 和 row 覆盖。",
    taskGalleryEyebrow: "题目列表",
    taskGalleryTitle: "Released rows",
    taskGalleryDescription: "搜索和筛选 300 行。来源标签只是审计标签，不是单独 benchmark 分母。",
    protocolEyebrow: "协议",
    protocolPageTitle: "评测与认证 gate",
    protocolPageText:
      "Spectre 是最终判定。EVAS 是快速 evaluator，但必须在支持的 voltage-domain/event-driven 子集上保持与 Spectre 对齐。",
    backendCertificationEyebrow: "后端认证",
    backendCertificationTitle: "四个执行面",
    backendCertificationDescription: "这些行认证 benchmark 和 evaluator 表面，不是模型排行榜结果。",
    claimBoundaryEyebrow: "结论边界",
    claimBoundaryTitle: "可以声称什么",
    parityGatesEyebrow: "Parity gates",
    alignmentEyebrow: "Spectre 对齐",
    alignmentTitle: "Golden reference 等价表",
    alignmentDescription:
      "每行说明比较了什么、EVAS/Spectre 实际差异以及使用哪个容差 gate。不宣称 bit-exact 完全一致。",
    accuracyEyebrow: "精度",
    accuracyPageTitle: "EVAS 与 Spectre 精度",
    accuracyPageText:
      "benchmark 不声称 bit-exact 完全一致；它报告各执行面是否在明确 gate 下与 Spectre reference 行为等价。",
    accuracyIdenticalEyebrow: "等价结论",
    accuracyIdenticalTitle: "输出是否完全一致？",
    accuracyTermsEyebrow: "如何理解容差",
    accuracyTermsTitle: "Gate 具体约束什么",
    precisionStrictEyebrow: "四路参考",
    precisionStrictTitle: "相对 Spectre strict 的精度",
    precisionStrictDescription:
      "EVAS Python、EVAS Rust 和 Spectre AX 都在当前 full-300 common-row 集合上与 Spectre strict reference 比较。",
    spectreAnchorEyebrow: "容差锚点",
    spectreAnchorTitle: "Spectre AX vs classic",
    spectreAnchorDescription:
      "Spectre 官方两种模式本身也不是 bit-identical。这份自一致性报告用于锚定哪些 waveform drift 在判定 EVAS mismatch 前是可接受的。",
    newsEyebrow: "更新",
    newsPageTitle: "更新与 release notes",
    newsPageText: "用一条人类可读时间线追踪 benchmark、evaluator、runner 和文档变化。",
    contributorsEyebrow: "贡献者",
    contributorsPageTitle: "人员与引用",
    contributorsPageText: "用于放置 benchmark 维护者、任务作者、evaluator 贡献者和引用说明。",
    maintainersEyebrow: "维护者",
    maintainersTitle: "vaBench release 维护者",
    maintainersBody: "维护公开分母、任务元数据、score roster 和报告导出。",
    taskAuthorsEyebrow: "任务作者",
    taskAuthorsTitle: "Benchmark 题目贡献者",
    taskAuthorsBody: "贡献 prompts、gold Verilog-A、checkers 以及 Spectre/EVAS 验证证据。",
    evaluatorContributorsEyebrow: "Evaluator",
    evaluatorContributorsTitle: "EVAS 与 Spectre harness 贡献者",
    evaluatorContributorsBody: "维护快速 evaluator、dual-judge runner、bridge scripts 和 parity regressions。",
    citationTitle: "引用",
    citationBody: "benchmark release 冻结后，把这里替换成论文引用。",
    thRank: "排名",
    thModel: "模型",
    thProvider: "服务商",
    thDate: "日期",
    thScore: "分数",
    thJudge: "裁判",
    thArtifact: "产物",
    thStatus: "状态",
    thEVAS: "EVAS",
    thSpectre: "Spectre",
    thCategory: "类别",
    thEntries: "Entries",
    thRows: "行数",
    thScoredRows: "计分行",
    thTask: "题目",
    thForm: "表单",
    thLevel: "层级",
    thBackends: "后端",
    thParity: "Parity",
    thBackend: "后端",
    thBehavior: "行为结果",
    thEvidence: "证据",
    thClaim: "结论",
    thActualDifference: "实际差异",
    thToleranceGate: "容差 Gate",
    thSurface: "执行面",
    thEquivalentRows: "等价行",
    thEffectiveMeanRms: "有效平均 RMS",
    thEffectiveWorstSignalRms: "有效最差信号 RMS",
    thRawMeanRms: "原始平均 RMS",
    thRawWorstSignalRms: "原始最差信号 RMS",
    thTaskMetricRows: "Task-metric 行",
    thTaskMetricDelta: "指标差异",
    thDiagnosticWaveform: "诊断波形",
    thDiagnosticMeanRms: "诊断平均 RMS",
    thDiagnosticWorstSignalRms: "诊断最差信号 RMS",
    thAcceptancePolicy: "接受策略",
    thReportingRule: "报告规则",
    thMetric: "指标",
    thValue: "值",
    filterSearch: "搜索",
    filterCategory: "类别",
    filterForm: "表单",
    filterLevel: "层级",
    filterProvenance: "来源",
    filterStatus: "状态",
    filterPolicy: "策略",
    resetFilters: "重置",
    taskSearchPlaceholder: "task id、类别、功能",
    alignmentSearchPlaceholder: "task id、类别、策略",
    loadingTaskRows: "正在加载题目行...",
    loadingAlignmentRows: "正在加载对齐行...",
    allOption: "全部",
    noRowsMatch: "当前筛选条件下没有匹配行。",
    noVerifiedRuns: "还没有 verified model submissions。",
    noVerifiedRunsDetail: "模型需要用 --final-judge spectre 跑完后，才加入排行。",
    notRanked: "不排名",
    integrationSmokePassed: "接入 smoke 通过",
    notRun: "未运行",
    generatedScoredFailed: "已生成并用 EVAS 评分 1 行；候选行为正确性失败",
    listRoster: "查看名单",
    evasOnlyBaseline: "仅 EVAS baseline",
    fullEvalWithSpectre: "完整评测含 Spectre",
    rowsShown: "当前显示 {shown} / {total} 行",
    alignmentRowsShown: "当前显示 {shown} / {total} 个对齐行",
    rowsWithRate: "{passed} / {total} 行 ({rate})",
    missingCheckers: "{count} 行缺少 checker",
    certified: "已认证",
    notCertified: "未认证",
    staticBackend: "静态",
    evasBackend: "EVAS",
    spectreBackend: "Spectre",
    spectreRef: "Spectre ref",
    spectreAx: "Spectre AX",
    evasRust: "EVAS Rust",
    evasPython: "EVAS Python",
    counted: "计分",
    notCounted: "不计分",
    meanRmsLine: "平均 RMS {mean}，最差 {worst}",
    gainDeltaLine: "增益差 {delta}",
    acceptanceBasis: "接受依据",
    bitExactEquality: "Bit-exact 完全相同",
    relativeRmsGate: "相对 RMS gate",
    smallAbsoluteGate: "小绝对误差 gate",
    gainMetricGate: "增益指标 gate",
    pllRows: "PLL 行",
    edgeWindowPolicy: "边沿窗口策略",
    metricBenchmarkRows: "Benchmark 行数",
    metricScoredRows: "模型计分行",
    metricFourBackend: "四后端状态",
    metricMismatch: "EVAS PASS / Spectre FAIL",
    metricReleaseEntries: "Release entries",
    metricCategories: "类别",
    metricAlignedRows: "Gold 对齐行",
    metricBitExact: "Bit-exact 声称",
    metricBackendCertified: "认证后端",
    metricFourwayRows: "精度证据行",
    metricEquivalentSurfaces: "等价执行面",
    metricPrecisionComparisons: "Gate 通过比较",
    metricReviewRows: "待复核行",
    metricSpectreSelf: "Spectre 自检",
    metricTaskMetricRows: "Task-metric 比较",
    detailSingleDenominator: "统一公开管理分母",
    detailModelRoster: "商业模型应运行的行",
    detailCertifiedSurfaces: "已认证执行面",
    detailAuditedMismatch: "已审计 mismatch 数",
    detailFunctionEntries: "行背后的功能级 entries",
    detailFunctionFamilies: "模拟与混合信号功能族",
    detailSpectreAligned: "在所列容差 gate 内对齐",
    detailNotAsserted: "不宣称",
    detailNotBitExact: "不承诺 bit-exact",
    detailCommonRows: "统一公开管理分母",
    detailPrecisionRows: "当前 full-300 common-row 证据",
    detailEquivalentSurfaces: "EVAS Python、EVAS Rust、Spectre AX",
    detailPrecisionComparisons: "surface-row 比较通过数",
    detailReviewRows: "blocked 或 needs-review 的精度行",
    detailSpectreSelf: "AX/classic 通过的 pair",
    detailTaskMetricRows: "由提取出的电路指标接受",
    identicalNoTitle: "不声称 bit-exact",
    identicalNoBody: "EVAS 输出和 Spectre 输出不主张逐点或逐 bit 完全相同。",
    equivalentYesTitle: "在 gate 内等价",
    equivalentYesBody: "在当前 full-300 common-row 证据上，EVAS Python、EVAS Rust 和 Spectre AX 都通过了以 Spectre strict 为 reference 的 gate。",
    differenceTitle: "差别主要是什么",
    differenceBody: "剩余数值差异主要来自 solver 采样、event timing、插值、边沿窗口、transition/cross 细节以及任务指标提取方式。",
    toleranceAnchorTitle: "容差从哪里来",
    toleranceAnchorBody: "容差由 Spectre AX/classic 自一致性中的可观测漂移锚定，不是随意设定的小数位精度。",
    pointwiseEyebrow: "逐点差异说明",
    pointwiseTitle: "为什么 raw RMS 可能更大",
    pointwiseDescription:
      "这些类别解释为什么纯逐点波形比较可能产生差异，即使该行已经通过 behavior 或 task-metric 接受规则。",
    taskMetricEyebrow: "Task-metric 行",
    taskMetricTitle: "不是用 raw pointwise equality 判定的行",
    taskMetricDescription:
      "测量流程类 row 可以用提取出的电路指标作为接受 gate。这里保留诊断用 waveform-only RMS，避免被误读成功能 mismatch。",
    anchorComparedPairs: "比较 pair",
    anchorPassedPairs: "通过 pair",
    anchorNeedsReviewPairs: "待复核 pair",
    anchorRowMeanMax: "行平均相对 RMS 最大值",
    anchorWorstSignalMax: "最差信号相对 RMS 最大值",
    anchorMaxPointAbs: "最大点绝对电压",
    loadError:
      "无法加载 vaBench 网站数据。请运行 python3 runners/export_vabench_eval_framework.py、python3 runners/export_vabench_github_pages.py 和 python3 runners/export_vabench_precision_overview.py，然后通过 HTTP 服务打开 docs/。{message}",
  },
};

const CATEGORY_LABELS_ZH = {
  "Baseband Signal Conditioning": "基带信号调理",
  "Bias Reference and Power Management": "偏置、基准与电源管理",
  "Calibration, DEM, and Control": "校准、DEM 与控制",
  "Comparator and Decision Circuits": "比较器与判决电路",
  "Data Converter Models": "数据转换器模型",
  "Measurement Instrumentation Flows": "测量仪表流程",
  "PLL Clock and Timing Systems": "PLL、时钟与时序系统",
  "RF and AFE Behavioral Macromodels": "RF 与 AFE 行为宏模型",
  "Sampling and Analog Memory": "采样与模拟存储",
  "Stimulus and Source Generators": "激励与源发生器",
};

const PROVENANCE_LABELS_ZH = {
  inherited_v1: "v1 继承",
  "promoted_v1.1": "v1.1 新增",
};

const POLICY_LABELS_ZH = {
  full_300_closure: "full-300 闭环",
  spectre_equivalence_core_v1: "Spectre 等价 core v1",
  spectre_equivalence_core_v2: "Spectre 等价 core v2",
  gain_metric: "增益指标",
  gain_extraction_metric_parity_v1: "增益指标 parity",
  pll_task_aware: "PLL task-aware",
};

const STATUS_LABELS_ZH = {
  pass: "通过",
  passed: "通过",
  ready: "就绪",
  certified: "已认证",
  true: "通过",
  false: "未通过",
  fail: "失败",
  failed: "失败",
  error: "错误",
  pending: "待处理",
  missing: "缺失",
  partial: "部分完成",
  score_enabled: "计分启用",
  spectre_aligned_within_tolerance: "Spectre 容差内一致",
  integration_smoke_passed: "接入 smoke 通过",
  equivalent_to_spectre_strict: "等价",
  needs_review: "待复核",
};

const GATE_LABELS_ZH = {
  behavior_checker: "行为 checker",
  relative_waveform: "相对 waveform RMS",
  small_absolute_voltage: "小绝对电压误差",
  edge_window: "边沿/不连续窗口",
  task_metric: "任务指标",
};

const GATE_MEANINGS_ZH = {
  behavior_checker: "电路级功能正确性是主要接受信号。",
  relative_waveform: "只有归一化 RMS 误差保持在 gate 内，逐点波形差异才被接受。",
  small_absolute_voltage: "当信号幅度很小导致相对误差被放大时，可由绝对电压误差 gate 接受。",
  edge_window: "不连续点附近的 solver 采样差异不直接视为功能 mismatch，前提是稳定区匹配。",
  task_metric: "部分行使用提取出的电路指标判定，而不是逐点 waveform equality。",
};

const TAXONOMY_ZH = {
  solver_sampling_grid: {
    label: "Solver 采样网格",
    what_changes: "EVAS 和 Spectre 可能保存不同的 transient accepted steps，因此报告会在重采样后的共同网格上比较共同信号。",
    why_expected: "自适应求解器即使得到等价的电路轨迹，也可能选择不同的输出点。",
    reporting_rule: "把 aligned-grid RMS 当作诊断指标；不要解读为 bit-exact 完全一致。",
  },
  event_time_and_cross: {
    label: "事件时间与 cross() 定位",
    what_changes: "cross() 事件和 timer 事件可能在略有不同的局部时间触发。",
    why_expected: "两个引擎的 event scheduling 和 breakpoint localization 机制不同。",
    reporting_rule: "先检查 behavior、event consistency 和 edge-window 指标，再判断是否 mismatch。",
  },
  edge_window: {
    label: "边沿与不连续窗口",
    what_changes: "快速边沿、不连续点或数字阈值附近的少数采样点可能主导 raw pointwise error。",
    why_expected: "一个采样点的边沿位置差异可能产生很大的瞬时电压差，但稳定区域仍匹配。",
    reporting_rule: "effective metrics 可以扣除有界局部窗口；raw metrics 仍然保留用于审计。",
  },
  interpolation: {
    label: "共同网格插值",
    what_changes: "保存的 waveform 会先插值，再做 RMS 比较。",
    why_expected: "原始输出时间不同，必须插值后才能逐点比较。",
    reporting_rule: "把插值误差视为精度诊断的一部分，而不是任务功能分数。",
  },
  transition_smoothing: {
    label: "transition() 平滑",
    what_changes: "transition() ramp 的 breakpoint 位置和采样斜率可能略有不同。",
    why_expected: "EVAS 和 Spectre 不承诺内部平滑调度完全一致。",
    reporting_rule: "当 transition 边沿抬高 raw RMS 时，应检查稳定区行为和 checker 指标。",
  },
  task_metric_gate: {
    label: "Task-metric gate",
    what_changes: "部分 row 用提取出的电路指标接受，例如 gain、lock 或 frequency，而不是 raw pointwise waveform equality。",
    why_expected: "测量流程类任务可能使用 dither/noise-like stimulus，逐点相位不是设计目标。",
    reporting_rule: "报告 task metric，同时只把 pointwise waveform diagnostics 作为解释上下文。",
  },
};

const state = {
  language: localStorage.getItem(LANGUAGE_KEY) === "zh" ? "zh" : "en",
  payloads: {},
  tasks: [],
  alignment: [],
  taskFiltersReady: false,
  alignmentFiltersReady: false,
};

function t(key) {
  return I18N[state.language]?.[key] || I18N.en[key] || key;
}

function format(key, values) {
  return t(key).replace(/\{(\w+)\}/g, (_, name) => values[name] ?? "");
}

function locale() {
  return state.language === "zh" ? "zh-CN" : "en-US";
}

function text(value) {
  if (value === null || value === undefined || value === "") {
    return "-";
  }
  return String(value);
}

function number(value) {
  if (value === null || value === undefined || value === "") {
    return "-";
  }
  if (typeof value === "number" && Number.isFinite(value)) {
    return Number.isInteger(value) ? value.toLocaleString(locale()) : value.toPrecision(3);
  }
  return String(value);
}

function preciseNumber(value) {
  if (value === null || value === undefined || value === "") {
    return "-";
  }
  if (typeof value === "number" && Number.isFinite(value)) {
    if (value === 0) {
      return "0";
    }
    if (Math.abs(value) >= 1000 || Math.abs(value) < 0.001) {
      return value.toExponential(3);
    }
    return value.toPrecision(6);
  }
  return String(value);
}

function percent(value) {
  if (typeof value !== "number" || !Number.isFinite(value)) {
    return "-";
  }
  return `${(value * 100).toFixed(1)}%`;
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

function translated(value) {
  const output = text(value);
  if (state.language !== "zh") {
    const englishMap = {
      not_asserted: "not asserted",
      spectre_aligned_within_tolerance: "Spectre-aligned within tolerance",
      waveform_relative_rms_and_absolute_voltage: "waveform RMS and absolute-voltage parity",
      extracted_gain_metric: "extracted gain metric",
      gain_extraction_metric_parity_v1: "gain extraction metric parity",
      pll_task_level_lock_frequency_control: "PLL lock/frequency/control task metric",
    };
    return englishMap[output] || output;
  }
  const map = {
    "not_asserted": "不宣称",
    "gain_extraction_metric_parity_v1": "增益提取指标 parity",
    "not bit-exact; equivalent within the stated acceptance gate": "不是 bit-exact；在所列 acceptance gate 内等价",
    "gold EVAS transient/metric result vs gold Spectre reference result for the same released row":
      "同一 released row 的 gold EVAS transient/metric 结果与 gold Spectre reference 结果",
    "common saved transient waveform columns compared on an aligned sample grid":
      "在对齐采样网格上比较共同保存的 transient waveform columns",
    "EVAS and Spectre extracted gain metric compared instead of pointwise waveform":
      "比较 EVAS 和 Spectre 提取出的 gain metric，而不是逐点波形",
    "task-level PLL lock/frequency/control checker pass, not pointwise waveform equality":
      "通过 task-level PLL lock/frequency/control checker，不主张逐点波形相等",
    "behavior/spec pass plus EVAS/Spectre waveform or task-metric parity":
      "behavior/spec pass 加 EVAS/Spectre waveform 或 task-metric parity",
    "Do not state bit-exact EVAS/Spectre equality; state behavior/spec pass plus tolerance-gated waveform or task-metric parity.":
      "不要声称 EVAS/Spectre bit-exact 完全相同；应表述为 behavior/spec pass 加容差约束下的 waveform 或 task-metric parity。",
    "Claim 300/300 four-backend behavior certification only when backend_coverage.status is pass and every listed full-300 summary remains current.":
      "只有当 backend_coverage.status 为 pass 且所有列出的 full-300 summary 仍为当前证据时，才声称 300/300 四后端行为认证。",
    "Current full-300 backend evidence is grounded by the explicit results/*/summary.json files listed in backend_coverage.":
      "当前 full-300 后端证据以 backend_coverage 中列出的 results/*/summary.json 为准。",
    "Negative candidates are static-shape audited partial-pass assets unless a separate full-checker validation report is produced.":
      "Negative candidates 只是经过 static-shape 审计的 partial-pass 资产，除非另有 full-checker validation report。",
  };
  let result = map[output] || output;
  result = result.replaceAll("row behavior checker PASS under full-300 closure; tolerance is checker-specific", "full-300 闭环下 row behavior checker PASS；容差由 checker 指定");
  result = result.replaceAll("checker-only closure: all four backends passed the row behavior checker; no waveform scalar was materialized for this row", "checker-only 闭环：四个后端都通过 row behavior checker；该行没有物化 waveform scalar");
  result = result.replaceAll("task_checker_status=passed", "task checker=通过");
  result = result.replaceAll("status=passed", "状态=通过");
  result = result.replaceAll("relative_gate PASS", "relative gate 通过");
  result = result.replaceAll("small_absolute_gate PASS", "small absolute gate 通过");
  result = result.replaceAll("relative_gain_delta", "相对增益差");
  result = result.replaceAll("mean_rel_rms", "平均相对 RMS");
  result = result.replaceAll("worst_rel_rms", "最差信号相对 RMS");
  result = result.replaceAll("max_rmse_v", "最大 RMSE");
  result = result.replaceAll("max_abs_v", "最大绝对误差");
  return result;
}

function categoryLabel(value) {
  const original = text(value);
  return state.language === "zh" ? CATEGORY_LABELS_ZH[original] || original : original;
}

function provenanceLabel(value) {
  const original = text(value);
  return state.language === "zh" ? PROVENANCE_LABELS_ZH[original] || original : original;
}

function policyLabel(value) {
  const original = text(value);
  return state.language === "zh" ? POLICY_LABELS_ZH[original] || original : original;
}

function statusLabel(value) {
  const normalized = String(value || "").toLowerCase();
  if (state.language === "zh" && STATUS_LABELS_ZH[normalized]) {
    return STATUS_LABELS_ZH[normalized];
  }
  const englishMap = {
    equivalent_to_spectre_strict: "equivalent",
    needs_review: "needs review",
  };
  if (state.language !== "zh" && englishMap[normalized]) {
    return englishMap[normalized];
  }
  return text(value);
}

function statusClass(value) {
  const normalized = String(value || "").toLowerCase();
  if (["pass", "passed", "ready", "certified", "true", "score_enabled", "integration_smoke_passed", "equivalent_to_spectre_strict"].includes(normalized)) {
    return "pass";
  }
  if (["fail", "failed", "false", "error"].includes(normalized)) {
    return "fail";
  }
  if (["pending", "missing", "partial", "not run", "needs_review"].includes(normalized)) {
    return "warn";
  }
  return "";
}

function pill(value, label) {
  const element = make("span", `status ${statusClass(value)}`, label || statusLabel(value));
  element.title = text(value);
  return element;
}

function codeText(value) {
  return make("code", "mono", text(value));
}

function rateBar(value) {
  const wrapper = make("div", "rate-bar");
  const fill = document.createElement("span");
  const clamped = Math.max(0, Math.min(1, typeof value === "number" ? value : 0));
  fill.style.width = `${clamped * 100}%`;
  wrapper.append(fill);
  return wrapper;
}

function ratioText(passed, total) {
  return `${number(passed)} / ${number(total)}`;
}

function metricCard(label, value, detail) {
  const card = make("article", "metric-card");
  card.append(make("span", "", label), make("strong", "", value), make("p", "", detail));
  return card;
}

function option(value, label) {
  const element = document.createElement("option");
  element.value = value;
  element.textContent = label || value;
  return element;
}

function populateSelect(id, values, labeler = (value) => value) {
  const select = byId(id);
  if (!select) {
    return;
  }
  const selected = select.value;
  select.replaceChildren(option("", t("allOption")), ...values.map((value) => option(value, labeler(value))));
  if ([...select.options].some((item) => item.value === selected)) {
    select.value = selected;
  }
}

function uniqueValues(rows, key) {
  return [...new Set(rows.map((row) => row[key]).filter(Boolean))].sort();
}

function applyStaticTranslations() {
  document.documentElement.lang = state.language === "zh" ? "zh-Hans" : "en";
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.textContent = t(element.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
    element.placeholder = t(element.dataset.i18nPlaceholder);
  });
  document.querySelectorAll("[data-i18n-aria-label]").forEach((element) => {
    element.setAttribute("aria-label", t(element.dataset.i18nAriaLabel));
  });
  const toggle = byId("language-toggle");
  if (toggle) {
    toggle.setAttribute("aria-pressed", state.language === "zh" ? "true" : "false");
  }
}

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`${url}: ${response.status}`);
  }
  return response.json();
}

function renderFooter() {
  const generated = state.payloads.summary?.generated_at || state.payloads.modelRoster?.date || "";
  const node = byId("generated-at");
  if (node) {
    node.textContent = generated ? `${generated}` : "";
  }
}

function renderNewsList(id, limit) {
  const container = byId(id);
  if (!container) {
    return;
  }
  const rows = limit ? NEWS_ITEMS.slice(0, limit) : NEWS_ITEMS;
  container.replaceChildren(
    ...rows.map((item) => {
      const anchor = document.createElement("a");
      anchor.className = "news-item";
      anchor.href = item.href;
      anchor.append(
        make("span", "news-meta", `${item.date} · ${item.type}`),
        make("strong", "", item.title[state.language]),
        make("p", "", item.body[state.language]),
      );
      return anchor;
    }),
  );
}

function renderHome() {
  const summary = state.payloads.summary?.summary || {};
  const model = state.payloads.modelRoster?.summary || {};
  const backend = state.payloads.summary?.summary || {};
  const metrics = byId("home-metrics");
  if (metrics) {
    metrics.replaceChildren(
      metricCard(t("metricBenchmarkRows"), number(summary.form_count), t("detailSingleDenominator")),
      metricCard(t("metricScoredRows"), number(model.scored_model_row_count || summary.scored_form_count), t("detailModelRoster")),
      metricCard(t("metricFourBackend"), statusLabel(summary.four_backend_status), t("detailCertifiedSurfaces")),
      metricCard(t("metricMismatch"), number(backend.evas_pass_spectre_fail_count), t("detailAuditedMismatch")),
    );
  }
  const preview = byId("home-leaderboard-preview");
  if (preview) {
    const panel = make("div", "empty-state");
    panel.append(
      pill("pending", t("noVerifiedRuns")),
      make("p", "", t("noVerifiedRunsDetail")),
      make("a", "text-link", t("homePrimaryAction")),
    );
    panel.querySelector("a").href = "run-model-eval.html";
    preview.replaceChildren(panel);
  }
  renderNewsList("home-news-list", 3);
}

function renderLeaderboard() {
  const tbody = byId("leaderboard-table");
  if (tbody) {
    if (VERIFIED_LEADERBOARD_ROWS.length === 0) {
      const tr = document.createElement("tr");
      const td = make("td", "", "");
      td.colSpan = 7;
      const empty = make("div", "empty-state");
      empty.append(pill("pending", t("noVerifiedRuns")), make("p", "", t("noVerifiedRunsDetail")));
      td.append(empty);
      tr.append(td);
      tbody.replaceChildren(tr);
    }
  }

  const smoke = byId("smoke-table");
  if (smoke) {
    smoke.replaceChildren(
      ...SMOKE_ROWS.map((row) => {
        const tr = document.createElement("tr");
        tr.append(
          make("td", "", row.model),
          make("td", "", ""),
          make("td", "table-note", state.language === "zh" ? t("generatedScoredFailed") : row.evas),
          make("td", "", state.language === "zh" ? t("notRun") : row.spectre),
        );
        tr.children[1].append(pill(row.status, t("integrationSmokePassed")));
        return tr;
      }),
    );
  }

  const commands = byId("leaderboard-commands");
  const examples = state.payloads.modelRoster?.example_commands || {};
  if (commands) {
    const items = [
      [t("listRoster"), examples.list_roster || "python3 runners/run_vabench_model_eval.py --list"],
      [t("evasOnlyBaseline"), examples.evas_only_baseline],
      [t("fullEvalWithSpectre"), examples.full_eval_with_spectre],
    ].filter(([, command]) => command);
    commands.replaceChildren(
      ...items.map(([label, command]) => {
        const group = make("div");
        group.append(make("dt", "", label), make("dd", "", command));
        return group;
      }),
    );
  }
}

function renderBenchmarkMetrics() {
  const summary = state.payloads.summary?.summary || {};
  const tasks = state.payloads.tasks?.summary || {};
  const model = state.payloads.modelRoster?.summary || {};
  const categories = state.payloads.categories?.rows || [];
  const metrics = byId("benchmark-metrics");
  if (!metrics) {
    return;
  }
  metrics.replaceChildren(
    metricCard(t("metricBenchmarkRows"), number(tasks.row_count || summary.form_count), t("detailSingleDenominator")),
    metricCard(t("metricReleaseEntries"), number(summary.entry_count), t("detailFunctionEntries")),
    metricCard(t("metricScoredRows"), number(model.scored_model_row_count || tasks.scored_rows), t("detailModelRoster")),
    metricCard(t("metricCategories"), number(categories.length), t("detailFunctionFamilies")),
  );
}

function renderCategories() {
  const tbody = byId("category-table");
  if (!tbody) {
    return;
  }
  tbody.replaceChildren(
    ...(state.payloads.categories?.rows || []).map((row) => {
      const tr = document.createElement("tr");
      tr.append(
        make("td", "", categoryLabel(row.category)),
        make("td", "", number(row.entry_count)),
        make("td", "", number(row.form_count)),
        make("td", "", number(row.l1_entry_count)),
        make("td", "", number(row.l2_entry_count)),
        make("td", "", number(row.scored_form_count)),
      );
      return tr;
    }),
  );
}

function initTaskFilters() {
  if (state.taskFiltersReady || !byId("task-search")) {
    return;
  }
  ["task-search", "filter-category", "filter-form", "filter-level", "filter-provenance"].forEach((id) => {
    byId(id)?.addEventListener("input", renderTaskTable);
  });
  byId("reset-filters")?.addEventListener("click", () => {
    ["task-search", "filter-category", "filter-form", "filter-level", "filter-provenance"].forEach((id) => {
      const node = byId(id);
      if (node) {
        node.value = "";
      }
    });
    renderTaskTable();
  });
  state.taskFiltersReady = true;
}

function setupTaskFilters() {
  const rows = state.tasks;
  populateSelect("filter-category", uniqueValues(rows, "category"), categoryLabel);
  populateSelect("filter-form", uniqueValues(rows, "form"));
  populateSelect("filter-level", uniqueValues(rows, "level"));
  populateSelect("filter-provenance", uniqueValues(rows, "provenance"), provenanceLabel);
  initTaskFilters();
}

function currentTaskRows() {
  const query = byId("task-search")?.value.trim().toLowerCase() || "";
  const category = byId("filter-category")?.value || "";
  const form = byId("filter-form")?.value || "";
  const level = byId("filter-level")?.value || "";
  const provenance = byId("filter-provenance")?.value || "";
  return state.tasks.filter((row) => {
    const localizedHaystack = [categoryLabel(row.category), provenanceLabel(row.provenance), policyLabel(row.parity_policy)]
      .join(" ")
      .toLowerCase();
    if (query && !String(row.search_text || "").includes(query) && !localizedHaystack.includes(query)) {
      return false;
    }
    return (!category || row.category === category) && (!form || row.form === form) && (!level || row.level === level) && (!provenance || row.provenance === provenance);
  });
}

function metricLine(row) {
  if (row.mean_relative_rms_error !== null && row.mean_relative_rms_error !== undefined) {
    return format("meanRmsLine", {
      mean: number(row.mean_relative_rms_error),
      worst: number(row.max_relative_rms_error),
    });
  }
  if (row.relative_gain_delta !== null && row.relative_gain_delta !== undefined) {
    return format("gainDeltaLine", { delta: number(row.relative_gain_delta) });
  }
  return policyLabel(row.parity_policy);
}

function renderTaskTable() {
  const rows = currentTaskRows();
  const count = byId("task-count");
  if (count) {
    count.textContent = format("rowsShown", { shown: number(rows.length), total: number(state.tasks.length) });
  }
  const tbody = byId("task-table");
  if (!tbody) {
    return;
  }
  if (rows.length === 0) {
    const tr = document.createElement("tr");
    const td = make("td", "", t("noRowsMatch"));
    td.colSpan = 7;
    tr.append(td);
    tbody.replaceChildren(tr);
    return;
  }
  tbody.replaceChildren(
    ...rows.map((row) => {
      const tr = document.createElement("tr");
      const task = make("td");
      const taskTitle = make("div", "task-title");
      taskTitle.append(make("strong", "", text(row.base_function)), codeText(row.task_id), make("small", "", text(row.release_entry_id)));
      task.append(taskTitle);

      const category = make("td");
      category.append(
        make("strong", "", categoryLabel(row.category)),
        make("div", "table-note", `${text(row.difficulty)} · ${text(row.track)} · ${provenanceLabel(row.provenance)}`),
      );

      const backend = make("td");
      const backendStack = make("div", "backend-stack");
      backendStack.append(pill(row.static, t("staticBackend")), pill(row.evas, t("evasBackend")), pill(row.spectre, t("spectreBackend")));
      backend.append(backendStack);

      const parity = make("td");
      parity.append(pill(row.parity_status), make("div", "table-note", metricLine(row)));

      tr.append(
        task,
        category,
        make("td", "", text(row.form)),
        make("td", "", text(row.level)),
        make("td", "", row.counted_in_score ? t("counted") : t("notCounted")),
        backend,
        parity,
      );
      return tr;
    }),
  );
}

function renderBenchmark() {
  state.tasks = state.payloads.tasks?.rows || [];
  renderBenchmarkMetrics();
  renderCategories();
  setupTaskFilters();
  renderTaskTable();
}

function renderProtocolMetrics() {
  const alignment = state.payloads.alignment?.summary || {};
  const summary = state.payloads.summary?.summary || {};
  const backends = state.payloads.backends || {};
  const metrics = byId("protocol-metrics");
  if (!metrics) {
    return;
  }
  metrics.replaceChildren(
    metricCard(t("metricAlignedRows"), number(alignment.aligned_row_count), t("detailSpectreAligned")),
    metricCard(t("metricBitExact"), translated(alignment.bit_exact_claim), t("detailNotAsserted")),
    metricCard(t("metricBackendCertified"), `${number(backends.certified_backend_count)} / ${number(backends.required_backend_count)}`, t("detailCertifiedSurfaces")),
    metricCard(t("metricMismatch"), number(summary.evas_pass_spectre_fail_count), t("detailAuditedMismatch")),
  );
}

function renderBackends() {
  const tbody = byId("backend-table");
  if (!tbody) {
    return;
  }
  const rows = [...(state.payloads.backends?.rows || [])].sort((a, b) => (b.pass_rate || 0) - (a.pass_rate || 0));
  tbody.replaceChildren(
    ...rows.map((row) => {
      const tr = document.createElement("tr");
      const backend = make("td");
      const stack = make("div", "task-title");
      stack.append(make("strong", "", translated(row.label)), make("small", "", text(row.backend)));
      backend.append(stack);

      const behavior = make("td");
      const behaviorStack = make("div", "parity-stack");
      behaviorStack.append(
        pill(row.certification_passed, row.certification_passed ? t("certified") : t("notCertified")),
        make("span", "table-note", format("rowsWithRate", { passed: number(row.pass_rows), total: number(row.total_rows), rate: percent(row.pass_rate) })),
        rateBar(row.pass_rate),
      );
      if (row.behavior_checker_missing_rows !== null && row.behavior_checker_missing_rows !== undefined) {
        behaviorStack.append(make("span", "table-note", format("missingCheckers", { count: number(row.behavior_checker_missing_rows) })));
      }
      behavior.append(behaviorStack);

      const evidence = make("td");
      evidence.append(codeText(row.evidence), make("div", "table-note", translated(row.notes)));

      const status = make("td");
      status.append(pill(row.status));
      tr.append(backend, status, make("td", "", `${number(row.pass_rows)} / ${number(row.total_rows)}`), behavior, evidence);
      return tr;
    }),
  );
}

function renderClaimBoundary() {
  const list = byId("protocol-list");
  if (list) {
    const boundary = state.payloads.summary?.claim_boundary || [];
    list.replaceChildren(
      ...boundary.map((item) => {
        const li = make("li", "", translated(item));
        return li;
      }),
    );
  }
  const terms = byId("parity-terms");
  if (terms) {
    const contract = state.payloads.summary?.equivalence_contract || {};
    const labels = {
      acceptance_basis: t("acceptanceBasis"),
      bit_exact_claim: t("bitExactEquality"),
      relative_rms_gate: t("relativeRmsGate"),
      small_absolute_gate: t("smallAbsoluteGate"),
      gain_metric_gate: t("gainMetricGate"),
      pll_task_aware: t("pllRows"),
      edge_window_policy: t("edgeWindowPolicy"),
    };
    terms.replaceChildren(
      ...Object.entries(labels)
        .filter(([key]) => contract[key] !== undefined)
        .map(([key, label]) => {
          const group = make("div");
          group.append(make("dt", "", label), make("dd", "", translated(contract[key])));
          return group;
        }),
    );
  }
}

function initAlignmentFilters() {
  if (state.alignmentFiltersReady || !byId("alignment-search")) {
    return;
  }
  ["alignment-search", "filter-alignment-status", "filter-alignment-policy"].forEach((id) => {
    byId(id)?.addEventListener("input", renderAlignmentTable);
  });
  byId("reset-alignment-filters")?.addEventListener("click", () => {
    ["alignment-search", "filter-alignment-status", "filter-alignment-policy"].forEach((id) => {
      const node = byId(id);
      if (node) {
        node.value = "";
      }
    });
    renderAlignmentTable();
  });
  state.alignmentFiltersReady = true;
}

function setupAlignmentFilters() {
  const rows = state.alignment;
  populateSelect("filter-alignment-status", uniqueValues(rows, "alignment_status"), statusLabel);
  populateSelect("filter-alignment-policy", uniqueValues(rows, "parity_policy"), policyLabel);
  initAlignmentFilters();
}

function currentAlignmentRows() {
  const query = byId("alignment-search")?.value.trim().toLowerCase() || "";
  const status = byId("filter-alignment-status")?.value || "";
  const policy = byId("filter-alignment-policy")?.value || "";
  return state.alignment.filter((row) => {
    const haystack = [
      row.task_id,
      row.legacy_task_id,
      row.release_entry_id,
      row.category,
      categoryLabel(row.category),
      row.form,
      provenanceLabel(row.provenance),
      row.parity_policy,
      policyLabel(row.parity_policy),
      row.alignment_status,
      statusLabel(row.alignment_status),
      row.equality_claim,
      translated(row.equality_claim),
      row.metric_family,
      translated(row.metric_family),
      row.equivalence_basis,
      translated(row.equivalence_basis),
      row.similarity_summary,
      row.tolerance_profile,
      row.tolerance_result,
    ]
      .filter(Boolean)
      .join(" ")
      .toLowerCase();
    return (!query || haystack.includes(query)) && (!status || row.alignment_status === status) && (!policy || row.parity_policy === policy);
  });
}

function renderAlignmentTable() {
  const rows = currentAlignmentRows();
  const count = byId("alignment-count");
  if (count) {
    count.textContent = format("alignmentRowsShown", { shown: number(rows.length), total: number(state.alignment.length) });
  }
  const tbody = byId("alignment-table");
  if (!tbody) {
    return;
  }
  if (rows.length === 0) {
    const tr = document.createElement("tr");
    const td = make("td", "", t("noRowsMatch"));
    td.colSpan = 5;
    tr.append(td);
    tbody.replaceChildren(tr);
    return;
  }
  tbody.replaceChildren(
    ...rows.map((row) => {
      const tr = document.createElement("tr");
      const task = make("td");
      const taskTitle = make("div", "task-title");
      taskTitle.append(
        make("strong", "", text(row.task_id)),
        make("small", "", `${categoryLabel(row.category)} · ${text(row.form)} · ${provenanceLabel(row.provenance)} · ${translated(row.metric_family)}`),
      );
      task.append(taskTitle);

      const claim = make("td");
      const claimStack = make("div", "parity-stack");
      claimStack.append(pill(row.alignment_status), make("span", "table-note", translated(row.equality_claim)));
      claim.append(claimStack);

      const backends = make("td");
      const backendStack = make("div", "backend-stack");
      backendStack.append(
        pill(row.spectre_reference_status, t("spectreRef")),
        pill(row.spectre_ax_status, t("spectreAx")),
        pill(row.evas_rust_behavior_checker_pass, t("evasRust")),
        pill(row.evas_python_behavior_checker_pass, t("evasPython")),
      );
      backends.append(backendStack);

      tr.append(
        task,
        claim,
        backends,
        make("td", "table-note", `${translated(row.similarity_summary)}; ${translated(row.equivalence_basis)}`),
        make("td", "table-note", `${translated(row.tolerance_profile)}; ${translated(row.tolerance_result)}`),
      );
      return tr;
    }),
  );
}

function renderProtocol() {
  state.alignment = state.payloads.alignment?.rows || [];
  renderProtocolMetrics();
  renderBackends();
  renderClaimBoundary();
  setupAlignmentFilters();
  renderAlignmentTable();
}

function gateLabel(gate) {
  if (state.language === "zh") {
    return GATE_LABELS_ZH[gate.name] || gate.label || gate.name;
  }
  return gate.label || gate.name;
}

function gateMeaning(gate) {
  if (state.language === "zh") {
    return GATE_MEANINGS_ZH[gate.name] || gate.meaning || "";
  }
  return gate.meaning || "";
}

function taxonomyField(item, field) {
  if (state.language === "zh") {
    return TAXONOMY_ZH[item.name]?.[field] || item[field] || "";
  }
  return item[field] || "";
}

function explanationCard(titleKey, bodyKey, statusValue) {
  const card = make("article", "explanation-card");
  card.append(pill(statusValue, t(titleKey)), make("p", "", t(bodyKey)));
  return card;
}

function renderAccuracyMetrics() {
  const precision = state.payloads.precision || {};
  const summary = precision.summary || {};
  const metrics = byId("accuracy-metrics");
  if (!metrics) {
    return;
  }
  metrics.replaceChildren(
    metricCard(t("metricBenchmarkRows"), number(summary.benchmark_management_rows), t("detailCommonRows")),
    metricCard(t("metricFourwayRows"), number(summary.precision_evidence_rows || summary.fourway_common_rows), t("detailPrecisionRows")),
    metricCard(t("metricPrecisionComparisons"), ratioText(summary.precision_pass_comparisons, summary.precision_total_comparisons), t("detailPrecisionComparisons")),
    metricCard(t("metricTaskMetricRows"), number(summary.task_metric_comparisons), t("detailTaskMetricRows")),
  );
}

function renderAccuracyAnswer() {
  const container = byId("accuracy-answer");
  if (!container) {
    return;
  }
  container.replaceChildren(
    explanationCard("identicalNoTitle", "identicalNoBody", "not_asserted"),
    explanationCard("equivalentYesTitle", "equivalentYesBody", "equivalent_to_spectre_strict"),
    explanationCard("differenceTitle", "differenceBody", "pending"),
    explanationCard("toleranceAnchorTitle", "toleranceAnchorBody", "pass"),
  );
}

function renderAccuracyGates() {
  const terms = byId("accuracy-gates");
  if (!terms) {
    return;
  }
  const gates = state.payloads.precision?.gates || [];
  terms.replaceChildren(
    ...gates.map((gate) => {
      const group = make("div");
      const threshold = gate.threshold ? `${gate.threshold}. ` : "";
      group.append(make("dt", "", gateLabel(gate)), make("dd", "", `${threshold}${gateMeaning(gate)}`));
      return group;
    }),
  );
}

function renderPrecisionTable() {
  const tbody = byId("precision-table");
  if (!tbody) {
    return;
  }
  const rows = state.payloads.precision?.simulator_precision_rows || [];
  tbody.replaceChildren(
    ...rows.map((row) => {
      const tr = document.createElement("tr");
      const surface = make("td");
      const stack = make("div", "task-title");
      stack.append(make("strong", "", text(row.candidate_label)), make("small", "", `${text(row.candidate)} vs ${text(row.reference_label)}`));
      surface.append(stack);

      const equivalent = make("td");
      equivalent.append(
        pill(row.claim),
        make("div", "table-note", ratioText(row.equivalent_rows, row.compared_rows)),
        rateBar(row.equivalence_rate),
      );

      tr.append(
        surface,
        equivalent,
        make("td", "", `${number(row.task_metric_rows)} (${preciseNumber(row.max_task_metric_relative_delta)})`),
        make("td", "", preciseNumber(row.worst_effective_mean_relative_rms_error)),
        make("td", "", preciseNumber(row.worst_effective_signal_relative_rms_error)),
        make("td", "", preciseNumber(row.worst_raw_mean_relative_rms_error)),
        make("td", "", preciseNumber(row.worst_raw_signal_relative_rms_error)),
      );
      return tr;
    }),
  );
}

function renderTaskMetricRows() {
  const tbody = byId("task-metric-table");
  if (!tbody) {
    return;
  }
  const rows = state.payloads.precision?.task_metric_rows || [];
  tbody.replaceChildren(
    ...rows.map((row) => {
      const tr = document.createElement("tr");
      const task = make("td");
      const stack = make("div", "task-title");
      stack.append(
        make("strong", "", `${text(row.release_entry_id)}:${text(row.form)}`),
        make("small", "", categoryLabel(row.category)),
      );
      task.append(stack);
      const diagnostic = make("td");
      diagnostic.append(pill(row.diagnostic_waveform_status), make("div", "table-note", text(row.diagnostic_note)));
      tr.append(
        make("td", "", text(row.candidate_label)),
        task,
        make("td", "", translated(row.acceptance_policy)),
        make("td", "", preciseNumber(row.relative_gain_delta)),
        diagnostic,
        make("td", "", preciseNumber(row.diagnostic_waveform_mean_relative_rms_error)),
        make("td", "", preciseNumber(row.diagnostic_waveform_worst_signal_relative_rms_error)),
      );
      return tr;
    }),
  );
}

function renderPointwiseTaxonomy() {
  const container = byId("pointwise-taxonomy");
  if (!container) {
    return;
  }
  const rows = state.payloads.precision?.pointwise_difference_taxonomy || [];
  container.replaceChildren(
    ...rows.map((item) => {
      const card = make("article", "feature-card static-card");
      card.append(
        make("span", "", taxonomyField(item, "label")),
        make("strong", "", taxonomyField(item, "what_changes")),
        make("p", "", taxonomyField(item, "why_expected")),
        make("p", "table-note", taxonomyField(item, "reporting_rule")),
      );
      return card;
    }),
  );
}

function renderSpectreAnchor() {
  const tbody = byId("spectre-anchor-table");
  if (!tbody) {
    return;
  }
  const anchor = state.payloads.precision?.spectre_self_consistency || {};
  const rows = [
    [t("anchorComparedPairs"), number(anchor.compared_pairs)],
    [t("anchorPassedPairs"), number(anchor.passed_pairs)],
    [t("anchorNeedsReviewPairs"), number(anchor.needs_review_pairs)],
    [t("anchorRowMeanMax"), preciseNumber(anchor.row_mean_relative_rms_max)],
    [t("anchorWorstSignalMax"), preciseNumber(anchor.worst_signal_relative_rms_max)],
    [t("anchorMaxPointAbs"), `${preciseNumber(anchor.max_point_abs_v)} V`],
  ];
  tbody.replaceChildren(
    ...rows.map(([label, value]) => {
      const tr = document.createElement("tr");
      tr.append(make("td", "", label), make("td", "", value));
      return tr;
    }),
  );
}

function renderAccuracy() {
  renderAccuracyMetrics();
  renderAccuracyAnswer();
  renderAccuracyGates();
  renderPrecisionTable();
  renderTaskMetricRows();
  renderPointwiseTaxonomy();
  renderSpectreAnchor();
}

function renderNews() {
  renderNewsList("news-list");
}

function renderAll() {
  renderFooter();
  const page = document.body.dataset.page || "home";
  if (page === "home") {
    renderHome();
  } else if (page === "leaderboard") {
    renderLeaderboard();
  } else if (page === "benchmark") {
    renderBenchmark();
  } else if (page === "protocol") {
    renderProtocol();
  } else if (page === "accuracy") {
    renderAccuracy();
  } else if (page === "news") {
    renderNews();
  }
}

function showError(error) {
  const main = document.querySelector("main");
  if (!main) {
    return;
  }
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
    const [summary, backends, alignment, tasks, categories, modelRoster, precision] = await Promise.all([
      fetchJson(DATA.summary),
      fetchJson(DATA.backends),
      fetchJson(DATA.alignment),
      fetchJson(DATA.tasks),
      fetchJson(DATA.categories),
      fetchJson(DATA.modelRoster),
      fetchJson(DATA.precision),
    ]);
    state.payloads = { summary, backends, alignment, tasks, categories, modelRoster, precision };
    renderAll();
  } catch (error) {
    showError(error);
    console.error(error);
  }
}

boot();
