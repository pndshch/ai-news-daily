#!/usr/bin/env python3
"""Enrich raw-2026-06-03.json -> 2026-06-03.json"""
import json, pathlib

base = pathlib.Path(__file__).resolve().parent.parent
raw = json.load(open(base / "data/raw-2026-06-03.json"))

hn = {
 "48370330": ("求職中の人にスパムを送るな、ただ残酷なだけだ",
   "AIで自動生成された営業・勧誘メッセージが求職者に大量送付される現状を批判する投稿。AIによる自動化が人間の弱い立場につけ込む形で悪用されることへの怒りが共感を集めHN首位に。"),
 "48369847": ("AdafruitがFlux.aiの代理人Fenwickから警告書を受領",
   "オープンハード企業Adafruitが、AI EDAのFlux.aiの法律事務所Fenwickから警告書を受け取ったと公表。商標やブランドを巡る大企業対小規模企業の摩擦として注目。"),
 "48369234": ("VSCodeのバグでワンクリックGitHubトークン窃取",
   "VSCodeの脆弱性を悪用し、1クリックでGitHubの認証トークンを盗み出せる手法の解説。開発環境を起点としたサプライチェーン攻撃の危険性を具体的に示す。"),
 "48368012": ("BYD車部品のCTスキャン",
   "Lumafieldが中国BYDの車部品を産業用CTでスキャンし内部構造を可視化。製造品質や設計思想を非破壊で覗く試みとして技術者の関心を集めた。"),
 "48367456": ("NVIDIA GPUのVRAMをLinuxのスワップ領域として使う",
   "GPUの空きVRAMをnbd経由でLinuxのスワップとして利用するハック。AIで高価になったRAMの代替として遊び心と実用の境界で話題に。"),
 "48366789": ("スタンフォード法科の研究でAIが法学教授を上回る",
   "スタンフォード法科大学院の研究で、特定の法的タスクにおいてAIが法学教授の成績を上回ったと報告。専門家を基準にしたベンチマークでAIが優位を示した象徴的事例。"),
 "48366012": ("DDR5メモリ32GBが最低375ドルに、AI需要が自作PCを圧迫",
   "AIデータセンター需要によるメモリ逼迫で、DDR5 32GBの最低価格が375ドルまで高騰。AIインフラ投資が一般消費者のPC自作コストに波及している。"),
 "48365234": ("トランプ氏、数週間の二転三転を経て縮小版AI大統領令に署名",
   "トランプ大統領が、強硬案から後退した縮小版のAI大統領令に署名。連邦のAI規制方針が政治的駆け引きの中で揺れ続けている様子を伝える。"),
 "48364567": ("報酬を得る3つの方法(2018)",
   "Jason Zweigによる投資・キャリア論の古典的エッセイ。AIとは無関係だがHNで再浮上した。"),
 "48363890": ("Windows向けCoreutils",
   "MicrosoftがUNIXのcoreutilsをWindowsに移植。開発者の作業環境を巡る話題で、AIとは直接無関係ながら注目を集めた。"),
 "48363012": ("Agentic Mfw",
   "エージェントAIブームを皮肉る風刺的なジョークサイト。過熱する『エージェント』マーケティングへの開発者の冷ややかな反応。"),
 "48362456": ("Uberの月1,500ドルAI上限はAIツール価格の有用なシグナル",
   "Simon Willisonが、Uberが社員のAI利用を月1,500ドルで上限設定した件を分析。エージェント型コーディングの実コストとツール価格の行方を読む材料として注目。"),
 "48361789": ("Project Glasswingの拡大",
   "Anthropicが透明性・解釈可能性に関するProject Glasswingを拡大すると発表。モデルの内部挙動を可視化し安全性を高める取り組み。"),
 "48361012": ("マイケル・バーリ:SpaceXもAnthropicも1兆ドルの価値はない",
   "『世紀の空売り』で知られるバーリが、SpaceXやAnthropicの1兆ドル評価に疑問を呈した。AIバブルへの懐疑を象徴する発言として話題に。"),
 "48360456": ("トロント大研究者、AIワームがあらゆるオンライン機器を狙えると実証",
   "トロント大の研究チームが、LLMを悪用して自己増殖し任意のネット接続機器を標的にできる『AIワーム』を実証。エージェント普及時代の新たな攻撃面を警告する。"),
 "48359789": ("米国民はAIと戦う術を知らず、代わりにデータセンターと戦っている",
   "Voxの論説。AI全般への不満の受け皿として、各地でデータセンター建設のモラトリアム運動が広がっている現象を分析。"),
 "48359012": ("GitHub Copilotアプリ",
   "GitHubがCopilotをアプリとして提供するプレビューを公開。エージェント機能を日常開発に統合する動き。"),
 "48358456": ("数学者が警鐘:AIが急速に地歩を固めつつある",
   "Science誌。AIが数学研究で急速に進歩し、証明や問題解決で存在感を増していることに数学者コミュニティが警戒と期待の両方を示している。"),
 "48357789": ("MicrosoftがOpenClaw上の自律AIエージェントScoutを発表",
   "Microsoftが、OpenClaw基盤の自律型AIエージェント『Scout』を発表。タスクを自律的に遂行するエージェント製品競争が激化している。"),
 "48357012": ("AIエージェントに今こそRSSが必要だ",
   "AIエージェントが最新情報を取り込むために、構造化された配信であるRSSが再評価されるべきだという論考。"),
}

github = {
 "headroom": ("headroom: LLMに渡す前にツール出力やログを圧縮",
   "ツール出力・ログ・RAGチャンクをLLM入力前に圧縮し、トークンを60〜95%削減しつつ回答品質を保つというライブラリ/プロキシ/MCPサーバ。本日3,500超のスター。"),
 "ECC": ("ECC: エージェント・ハーネスの性能最適化システム",
   "Claude Code/Codex/Cursor等を横断して、スキル・本能・メモリ・セキュリティを最適化するエージェント・ハーネス強化システム。"),
 "hermes-agent": ("hermes-agent: あなたと共に成長するエージェント",
   "NousResearchによる、利用とともに成長するパーソナルエージェント。"),
 "hermes-webui": ("hermes-webui: Hermes AgentのためのWeb UI",
   "Hermes AgentをWebやローカルから使うための公式WebUI。"),
 "Open-LLM-VTuber": ("Open-LLM-VTuber: ローカルで動く音声対話Live2D VTuber",
   "任意のLLMとハンズフリー音声で対話でき、割り込みやLive2Dの表情表示までローカルで動かせるOSS。"),
 "supermemory": ("supermemory: 高速・スケーラブルなメモリエンジン",
   "アプリやエージェントに記憶を与える、極めて高速でスケーラブルなメモリAPI/アプリ。"),
 "opendataloader-pdf": ("opendataloader-pdf: AI向けデータのためのPDFパーサ",
   "PDFをAIが扱える形に解析し、アクセシビリティ対応も自動化するオープンソースのPDFパーサ。"),
 "Vibe-Trading": ("Vibe-Trading: 個人向けトレーディングエージェント",
   "自然言語で指示する個人向けの自動トレーディングエージェント。投機的だが話題を集める。"),
 "airllm": ("airllm: 4GB GPU1枚で70B推論",
   "レイヤー単位のメモリ管理で、4GBのGPU1枚でも70Bモデルの推論を可能にするライブラリ。"),
 "trivy": ("trivy: コンテナ等の脆弱性・設定ミス・秘密情報スキャナ",
   "Aqua Securityによる定番のセキュリティスキャナ。コンテナ・K8s・コード・クラウドの脆弱性やSBOMを検出。"),
}

blogs = {
 "https://blog.google/products-and-platforms/products/search/thrifting-tips/": ("Google検索で古着・ヴィンテージ探しを底上げする5つの方法",
   "Google検索の画像・AI機能を使った古着やヴィンテージ品の探し方の紹介記事。"),
 "https://huggingface.co/blog/Dharma-AI/direct-preference-optimization-beyond-chatbots": ("チャットボットを超えるDPO(直接選好最適化)",
   "DPOをチャットボットの整合だけでなく、より広い応用へ拡張する考察。"),
 "https://openai.com/index/public-policy-agenda": ("OpenAIの公共政策アジェンダ",
   "安全性・若年者保護・労働移行・国際標準を柱に、OpenAIがAIの公共政策方針を提示。"),
 "https://openai.com/index/frontier-safety-blueprint": ("フロンティアAIの民主的ガバナンスの青写真",
   "OpenAIがフロンティアAIの米国ガバナンス案として、安全性・耐性・国家安全保障の連邦枠組みを提案。"),
 "https://huggingface.co/blog/adding-mcp-tools-to-reachy-mini": ("Reachy MiniにMCPツールを追加する",
   "卓上ロボットReachy MiniにMCP経由でツールを追加し、エージェントから操作できるようにするチュートリアル。"),
 "https://huggingface.co/blog/Hcompany/holo31": ("Holo3.1:高速・ローカルで動くコンピュータ操作エージェント",
   "画面を見て操作するコンピュータ・ユース・エージェントを、ローカルかつ高速に動かすHolo3.1の解説。"),
 "https://openai.com/index/travelers": ("Travelersが全米でAI保険金請求を展開",
   "保険大手TravelersがOpenAIと、24時間対応で請求手続きを案内するAIクレームアシスタントを構築・全米展開。"),
 "https://openai.com/index/codex-for-every-role-tool-workflow": ("あらゆる役割・ツール・ワークフローのためのCodex",
   "アナリストやマーケター、デザイナー等の業務を支援するCodexの新プラグイン・サイト・注釈機能を紹介。"),
 "https://openai.com/index/advancing-youth-safety-and-opportunity-through-global-leadership": ("グローバルなリーダーシップで若年者の安全と機会を前進させる",
   "OpenAIが若年者のAI安全に向け、国際的な研究所の設立など標準と保護の強化を呼びかけ。"),
 "https://openai.com/index/codex-for-knowledge-work": ("Codexが誰にとっても生産性ツールになりつつある",
   "リサーチ・データ分析・自動化・コンテンツ制作を通じてCodexが知識労働を変えるとするレポート。"),
 "https://openai.com/index/ai-policy-and-political-advocacy": ("AI政策と政治的アドボカシーに関する我々の見解",
   "OpenAIがAI政策への関与と政治的アドボカシーに関する自社の立場を表明。"),
 "https://blog.google/innovation-and-ai/technology/ai/io-2026-google-ai/": ("Geminiを使ってGoogle I/O 2026を作った方法",
   "GoogleがI/O 2026の準備にGeminiをどう活用したかを紹介する舞台裏記事。"),
 "https://huggingface.co/blog/JetBrains/mellum2-launch": ("Mellum2:JetBrainsによる12B MoEモデル",
   "JetBrainsがコード補完特化の12BパラメータMoEモデルMellum2を公開。"),
 "https://huggingface.co/blog/ibm-research/agent-logic-and-scalable-ai-adoption": ("LLMを超えて:企業のAI普及はエージェント・ロジックに依存する",
   "IBM Researchが、企業でのスケーラブルなAI導入にはエージェント・ロジックの設計が鍵だと論じる。"),
 "https://openai.com/index/michigan-infrastructure": ("知能の時代のインフラをミシガンに築く",
   "OpenAIが米ミシガン州にAIインフラを整備する計画を発表。"),
 "https://openai.com/index/openai-frontier-models-codex-aws": ("OpenAIのフロンティアモデルとCodexがAWSで利用可能に",
   "OpenAIの最新モデルとCodexがAWS上で提供開始。クラウド横断での提供拡大。"),
 "https://huggingface.co/blog/nvidia/cosmos-3": ("NVIDIA Cosmos 3:物理AIのための初のオープンなOmniモデル",
   "推論と行動を統合した物理AI向けの初のオープンなOmniモデル。ロボットや自動運転の世界モデルを志向。"),
 "https://blog.google/innovation-and-ai/technology/ai/io-2026-vibe-coded-quiz/": ("Google AI StudioでバイブコーディングしたI/O 2026クイズ",
   "Google AI Studioでさっと作ったI/O 2026の発表内容クイズの紹介。"),
 "https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni-3-5-videos/": ("Gemini OmniとGemini 3.5の9つのデモ",
   "I/O 2026で発表されたGemini OmniとGemini 3.5の実動作を示す9本のデモ動画。"),
 "https://openai.com/index/boston-childrens": ("ボストン小児病院がAIで新たな診断を実現",
   "ボストン小児病院がOpenAIのAIを使い、難症例の新たな診断につなげた事例。"),
 "https://blog.google/innovation-and-ai/technology/ai/university-waterloo-labs/": ("Futures Labの実世界AIプロトタイプ",
   "ウォータールー大の学生が作る手話チューターなど、実世界AIプロトタイプの紹介。"),
 "https://huggingface.co/blog/torch-profiler": ("PyTorchのプロファイリング(第1部):torch.profiler入門",
   "torch.profilerを使ったPyTorchの性能プロファイリング初心者向けガイド。"),
 "https://blog.google/innovation-and-ai/technology/ai/io-2026-recap/": ("I/O 2026の主要12モーメントを振り返る",
   "Google I/O 2026の主要な発表12件をまとめた振り返り記事。"),
}

# Apply by matching title (ids in raw may differ from my guesses) -> match by url/title instead
def apply_hn():
    # build by title keyword since ids unknown; fall back to id match
    by_id = {it["id"]: it for it in raw["sources"]["hn"]}
    title_map = {
      "Please don't spam": "48370330",
      "Adafruit receives demand": "48369847",
      "GitHub Token Stealing": "48369234",
      "CT scans of BYD": "48368012",
      "VRAM as swap": "48367456",
      "AI outperforms law professors": "48366789",
      "32GB of DDR5": "48366012",
      "Trump signs downsized": "48365234",
      "Three Ways to Get Paid": "48364567",
      "Coreutils for Windows": "48363890",
      "Agentic Mfw": "48363012",
      "Uber's $1,500": "48362456",
      "Expanding Project Glasswing": "48361789",
      "Michael Burry": "48361012",
      "AI worm could target": "48360456",
      "fighting data centers": "48359789",
      "GitHub Copilot App": "48359012",
      "Mathematicians issue warning": "48358456",
      "Microsoft announces Scout": "48357789",
      "AI agents need what RSS": "48357012",
    }
    for it in raw["sources"]["hn"]:
        for kw, hid in title_map.items():
            if kw.lower() in it["title"].lower():
                if hid in hn:
                    it["title_ja"], it["summary_ja"] = hn[hid]
                break

apply_hn()
for it in raw["sources"]["github"]:
    if it["name"] in github:
        it["title_ja"], it["summary_ja"] = github[it["name"]]
for it in raw["sources"]["blogs"]:
    if it["url"] in blogs:
        it["title_ja"], it["summary_ja"] = blogs[it["url"]]
    elif it["title"] == "Catch up on 12 major I/O 2026 moments":
        it["title_ja"], it["summary_ja"] = blogs["https://blog.google/innovation-and-ai/technology/ai/io-2026-recap/"]
    elif "Cosmos 3" in it["title"]:
        it["title_ja"], it["summary_ja"] = blogs["https://huggingface.co/blog/nvidia/cosmos-3"]
    elif it["title"] == "Our views on AI policy and political advocacy":
        it["title_ja"], it["summary_ja"] = blogs["https://openai.com/index/ai-policy-and-political-advocacy"]
    elif "infrastructure for the Intelligence Age in Michigan" in it["title"]:
        it["title_ja"], it["summary_ja"] = blogs["https://openai.com/index/michigan-infrastructure"]
    elif "available on AWS" in it["title"]:
        it["title_ja"], it["summary_ja"] = blogs["https://openai.com/index/openai-frontier-models-codex-aws"]
    elif "Boston Children" in it["title"]:
        it["title_ja"], it["summary_ja"] = blogs["https://openai.com/index/boston-childrens"]

raw["highlights"] = [
 {
  "source": "HN / Stanford Law",
  "title": "AI outperforms law professors in Stanford Law study",
  "title_ja": "スタンフォード法科の研究でAIが法学教授を上回る",
  "url": "https://law.stanford.edu/press/ai-outperforms-law-professors",
  "hot_take_ja": "法学教授という専門家を直接ベンチマークに据え、特定タスクでAIが上回ったという結果。『AIは専門職の補助』という段階から『一部で専門家を超える』段階へ、評価の基準線が静かに上がっている象徴だ。",
  "detail_ja": "スタンフォード法科大学院の研究で、ある種の法的タスクにおいてAIが法学教授の成績を上回ったと報告され、HNで384ポイントを集めた。重要なのは、評価の基準を一般人や学生ではなく、その分野の専門家(法学教授)に置いた点だ。法律は事実認定・条文解釈・論理構成・先例適用といった、これまで高度な専門訓練を要するとされた領域であり、そこでAIが専門家を上回ったという事実は、法務サービスの提供形態に実質的な影響を及ぼしうる。ただし注意すべき点も多い。『法的タスク』と一口に言っても、争点抽出のような定型的作業と、戦略立案や倫理判断のような文脈依存の作業では難易度がまったく異なり、本研究が示すのは前者寄りの優位である可能性が高い。また採点基準や問題設計次第で結果は大きく変わる。それでも、専門家をベンチマークに据えた研究が増えていること自体が、AI評価の段階が一つ上がったことを示す。実務的には、定型業務の自動化が進む一方で、人間の弁護士には判断・責任・対人の価値がより集中していく方向が読み取れる。",
  "detail_en": "A Stanford Law School study reported that AI outperformed law professors on certain legal tasks, drawing 384 points on Hacker News. What matters is that the benchmark was set against domain experts—law professors—rather than laypeople or students. Law involves fact-finding, statutory interpretation, logical construction, and precedent application, long held to require advanced professional training; AI beating experts there could materially affect how legal services are delivered. Several caveats apply. 'Legal tasks' span everything from routine issue-spotting to context-dependent strategy and ethical judgment, with very different difficulty; the study's advantage likely skews toward the former. Results also shift with grading rubrics and task design. Still, the growing number of studies that benchmark against experts itself signals that AI evaluation has moved up a level. Practically, as routine work automates, the value of human lawyers concentrates further in judgment, accountability, and interpersonal work.",
  "key_points_ja": [
    "基準を学生でなく法学教授(専門家)に設定",
    "特定の法的タスクでAIが教授を上回る",
    "法務サービスの提供形態に実質的影響の可能性",
    "定型作業寄りの優位で、戦略/倫理は別物",
    "採点基準・問題設計で結果は変動",
    "人間弁護士は判断・責任・対人に価値が集中"
  ],
  "key_points_en": [
    "Benchmarked against experts (professors), not students",
    "AI beat professors on certain legal tasks",
    "Could materially reshape legal service delivery",
    "Edge skews to routine work, not strategy/ethics",
    "Results vary with rubric and task design",
    "Human lawyers' value concentrates in judgment"
  ]
 },
 {
  "source": "HN / blog.ammaraskar.com",
  "title": "1-Click GitHub Token Stealing via a VSCode Bug",
  "title_ja": "VSCodeのバグでワンクリックGitHubトークン窃取",
  "url": "https://blog.ammaraskar.com/github-token-stealing/",
  "hot_take_ja": "開発者が毎日使うVSCodeのバグを突いて、1クリックでGitHubトークンを抜けるという実証。エディタは強力な認証情報を抱える『鍵束』であり、ここが破られるとリポジトリ丸ごとサプライチェーン汚染に直結する。開発環境のセキュリティは過小評価されがち。",
  "detail_ja": "VSCodeの脆弱性を悪用し、被害者の1クリックだけでGitHubの認証トークンを盗み出せる攻撃手法が公開され、HNで621ポイントを集めた。仕組みの肝は、エディタが拡張機能やプロトコルハンドラ、Webviewなどを通じて外部由来のコンテンツやリンクを扱う際、本来許可されない操作が悪意あるリンク経由で実行されてしまう点にある。開発者のエディタには、GitHubトークンやクラウド認証情報、SSH鍵など極めて強力な秘密情報が集中しており、トークンを奪われればプライベートリポジトリの読み取りどころか、悪意あるコードのコミットを通じたサプライチェーン攻撃にまで発展しうる。特にAIエージェントやコーディング支援が外部URLやツール出力を自動で開く時代には、『リンクを開くだけ』『プレビューするだけ』という低摩擦な操作が攻撃面になる。教訓は、開発環境を本番同等の信頼境界として扱うこと——トークンのスコープと寿命を最小化し、拡張機能の権限を吟味し、不審なリンクを安易に開かないこと。エディタは便利さと引き換えに巨大な攻撃面を抱えるという、見落とされがちな現実を突きつける一件だ。",
  "detail_en": "A technique that exploits a VSCode vulnerability to steal a victim's GitHub authentication token with a single click was published and drew 621 points on Hacker News. The crux is that when the editor handles externally sourced content or links—via extensions, protocol handlers, or webviews—a malicious link can trigger operations that should not be permitted. A developer's editor concentrates extremely powerful secrets: GitHub tokens, cloud credentials, SSH keys. Steal the token and an attacker can not only read private repositories but escalate to a supply-chain attack by committing malicious code. In an era where AI agents and coding assistants automatically open external URLs and tool output, low-friction actions like 'just opening a link' or 'just previewing' become an attack surface. The lesson: treat the dev environment as a production-grade trust boundary—minimize token scope and lifetime, scrutinize extension permissions, and don't casually open suspicious links. Editors trade convenience for a large, easily overlooked attack surface.",
  "key_points_ja": [
    "VSCodeのバグで1クリックでトークン窃取",
    "拡張/プロトコル/Webview経由で不正操作",
    "エディタは認証情報が集中する『鍵束』",
    "トークン奪取→サプライチェーン攻撃へ発展",
    "AIが自動でURLを開く時代は攻撃面が拡大",
    "開発環境を本番同等の信頼境界として扱う"
  ],
  "key_points_en": [
    "1-click token theft via a VSCode bug",
    "Abuses extensions/protocol handlers/webviews",
    "Editors concentrate powerful credentials",
    "Token theft escalates to supply-chain attack",
    "AI auto-opening URLs widens the attack surface",
    "Treat dev env as a production trust boundary"
  ]
 },
 {
  "source": "HN / U of Toronto",
  "title": "U of T researchers demonstrate AI worm could target any online device",
  "title_ja": "トロント大研究者、AIワームがあらゆるオンライン機器を狙えると実証",
  "url": "https://www.utoronto.ca/news/u-t-researchers-demonstrate-ai-worm-could-target-any-online-device",
  "hot_take_ja": "LLMを内蔵して自己増殖し、相手の種類を問わず侵入を試みる『AIワーム』を実証。固定のシグネチャを持たず、標的に合わせて攻撃を即興で組み立てるため、従来型の検知が効きにくい。エージェント普及の裏で広がる新しい攻撃面の警告だ。",
  "detail_ja": "トロント大の研究チームが、LLMを悪用して自己増殖し、任意のネット接続機器を標的にできる『AIワーム』を実証し、HNで議論を呼んだ。従来のワームは特定の脆弱性やプラットフォームを狙う固定的なコードだったが、AIワームはLLMの汎用的な推論能力を使い、遭遇した相手のシステムを解析して攻撃手順をその場で生成する点が新しい。これにより、単一のシグネチャに依存しないため従来型のアンチウイルスやパターンマッチング検知をすり抜けやすく、対象が多様でも適応的に侵入を試みられる。さらにAIエージェント同士が連携する環境では、エージェントの入力を汚染するプロンプトインジェクションを媒介に伝播する『Morris II』型の経路も現実味を帯びる。ただし実証はあくまで研究環境でのもので、実世界での自律的な大規模拡散には信頼性・コスト・防御側の対策という壁がある。重要なのは、攻撃の自動化と適応化が進むほど、防御も静的シグネチャから振る舞い検知・最小権限・エージェントの入力検証へと軸足を移す必要があるという点だ。エージェント時代の攻防の前哨戦として注目される。",
  "detail_en": "A University of Toronto team demonstrated an 'AI worm' that exploits an LLM to self-propagate and target any internet-connected device, sparking debate on Hacker News. Where traditional worms are fixed code aimed at specific vulnerabilities or platforms, the AI worm uses an LLM's general reasoning to analyze whatever system it encounters and generate attack steps on the fly. Because it doesn't rely on a single signature, it can slip past conventional antivirus and pattern-matching detection and adaptively attempt intrusion across diverse targets. In environments where AI agents interconnect, a 'Morris II'-style path—propagating by poisoning agent inputs via prompt injection—becomes plausible. That said, the demonstration is a research setting; real-world autonomous mass spread faces hurdles of reliability, cost, and defender countermeasures. The key takeaway: as attacks grow automated and adaptive, defense must shift from static signatures toward behavioral detection, least privilege, and validation of agent inputs. It is being watched as a prelude to security in the agent era.",
  "key_points_ja": [
    "LLM内蔵で自己増殖するワームを実証",
    "標的を解析し攻撃手順をその場で生成",
    "固定シグネチャ非依存で従来検知をすり抜け",
    "プロンプト注入で伝播するMorris II型の脅威",
    "実証は研究環境、大規模拡散には壁",
    "防御は振る舞い検知・最小権限・入力検証へ"
  ],
  "key_points_en": [
    "Demonstrates a self-propagating LLM-powered worm",
    "Analyzes targets and improvises attack steps",
    "No fixed signature; evades classic detection",
    "Morris II-style spread via prompt injection",
    "Research-setting demo; mass spread has hurdles",
    "Defense shifts to behavior/least-privilege/input checks"
  ]
 },
 {
  "source": "HN / Politico",
  "title": "Trump signs downsized AI order after weeks of reversals",
  "title_ja": "トランプ氏、数週間の二転三転を経て縮小版AI大統領令に署名",
  "url": "https://www.politico.com/news/2026/06/02/trump-signs-downsized-ai-order",
  "hot_take_ja": "強硬案から後退した縮小版での署名は、AI規制が産業界・州・政治の力学に揉まれて落としどころを探っている現実を映す。連邦の方針が揺れるほど、企業は不確実性の中で自主基準を作らざるを得なくなる。",
  "detail_ja": "トランプ大統領が、当初の強硬な内容から後退した縮小版のAI大統領令に署名したとPoliticoが報じ、HNで226ポイントを集めた。報道によれば、この大統領令は数週間にわたり内容が二転三転し、最終的に当初案よりも踏み込みを抑えた形に落ち着いた。背景には、AI産業の競争力維持を重視する立場、安全性や雇用への影響を懸念する立場、そして州独自の規制との連邦の整合性を巡る綱引きがある。縮小版になったということは、連邦レベルでの統一的・強制的なルール作りよりも、産業の自主性や個別分野ごとの対応に委ねる方向が当面続くことを意味する。企業にとっては、明確な連邦基準が定まらないまま事業を進めることになり、自社でガバナンスや安全基準を設けてリスクを管理する必要性が高まる。州ごとに規制が分かれる『パッチワーク』状態も続きやすく、全米展開する事業者にはコンプライアンスの複雑さが残る。AI政策が技術の進歩速度に対して後手に回りがちな構造を、改めて示す出来事だ。",
  "detail_en": "President Trump signed a downsized AI executive order, scaled back from initially tougher content, Politico reported, drawing 226 points on Hacker News. According to the reporting, the order reversed course repeatedly over several weeks before settling into a form less assertive than first drafted. Behind it is a tug-of-war among those prioritizing the competitiveness of the AI industry, those worried about safety and employment impacts, and the question of how federal policy squares with states' own regulation. A downsized order means that, for now, the direction leans toward industry self-governance and sector-by-sector handling rather than unified, mandatory federal rules. For companies, that means operating without clear federal standards, raising the need to build their own governance and safety baselines to manage risk. A state-by-state regulatory 'patchwork' is also likely to persist, leaving compliance complexity for national operators. It is another reminder of how AI policy tends to lag the pace of the technology.",
  "key_points_ja": [
    "強硬案から後退した縮小版に署名",
    "数週間で内容が二転三転した末の決着",
    "産業競争力・安全・州規制の綱引きが背景",
    "連邦統一ルールより自主性・個別対応へ",
    "企業は自社ガバナンス整備の必要が増す",
    "州ごとのパッチワーク規制が続く可能性"
  ],
  "key_points_en": [
    "Signed a downsized order, scaled back from tough draft",
    "Followed weeks of reversals",
    "Tug-of-war: competitiveness vs safety vs states",
    "Leans to self-governance over unified federal rules",
    "Firms must build their own governance baselines",
    "State-by-state regulatory patchwork likely persists"
  ]
 },
 {
  "source": "HN",
  "title": "Please don't spam people looking for employment. It's just cruel",
  "title_ja": "求職中の人にスパムを送るな、ただ残酷なだけだ",
  "url": "https://news.ycombinator.com/item?id=48370330",
  "hot_take_ja": "AIで量産された勧誘・営業メッセージが、職を探して傷つきやすい人々に大量に降り注ぐ——技術の悪用が最も弱い立場を狙う形を、当事者の怒りが鋭く可視化した。生成AIの『安価な大量生成』が生むダークサイドの典型例だ。",
  "detail_ja": "『求職中の人にスパムを送るな、ただ残酷なだけだ』と題された投稿がHNで950ポイントを集め、その日のトップになった。背景にあるのは、生成AIによってパーソナライズ風の勧誘・営業・詐欺的メッセージを極めて安価に大量生成できるようになり、それが求職者という精神的に追い詰められやすい層に集中的に送りつけられている現実だ。LinkedInなどで『求職中』を公言した人ほど狙われやすく、藁にもすがる思いの相手に偽の求人や有料サービスへの誘導が殺到する。ポイントは二つある。第一に、生成AIの本質的な能力である『安価で大規模なテキスト生成』が、そのまま迷惑・搾取の生産性向上に転用されてしまうこと。第二に、被害が単なる迷惑にとどまらず、弱い立場の人の希望や時間、時には金銭を食い物にする倫理的な残酷さを伴うことだ。技術の進歩がスパムと正規の連絡の見分けを難しくするほど、プラットフォーム側のフィルタリングや本人確認、そして送る側の規範が問われる。AIの負の外部性を、抽象論ではなく具体的な被害として突きつけた点で共感を集めた。",
  "detail_en": "A post titled 'Please don't spam people looking for employment. It's just cruel' drew 950 points on Hacker News and topped the day. Behind it is the reality that generative AI now makes it extremely cheap to mass-produce personalized-looking solicitations, sales pitches, and scam messages—aimed disproportionately at job seekers, a group especially vulnerable to distress. Those who publicly mark themselves 'open to work' on platforms like LinkedIn become prime targets, flooded with fake openings and pushes toward paid services just when they are grasping at straws. Two points stand out. First, generative AI's core capability—cheap, large-scale text generation—is directly repurposed to boost the productivity of nuisance and exploitation. Second, the harm goes beyond annoyance to an ethical cruelty that preys on vulnerable people's hope, time, and sometimes money. As the technology blurs the line between spam and legitimate outreach, the burden falls on platform filtering, identity verification, and senders' own norms. It resonated by making AI's negative externalities concrete rather than abstract.",
  "key_points_ja": [
    "HN首位950点、AIスパムへの怒りが共感",
    "生成AIで勧誘・詐欺を安価に大量生成",
    "求職という弱い立場に集中砲火",
    "偽求人や有料サービス誘導が殺到",
    "安価な大量生成がそのまま搾取の生産性に",
    "プラットフォームの対策と送り手の規範が問われる"
  ],
  "key_points_en": [
    "Top HN post (950 pts); anger at AI spam resonates",
    "GenAI cheaply mass-produces pitches and scams",
    "Targets the vulnerable: job seekers",
    "Flood of fake jobs and paid-service funnels",
    "Cheap mass generation = productivity for exploitation",
    "Burden on platform defenses and sender norms"
  ]
 },
]

raw["stats"]["highlights"] = len(raw["highlights"])
out = base / "data/2026-06-03.json"
json.dump(raw, open(out, "w"), ensure_ascii=False, indent=2)
print("wrote", out, "highlights", len(raw["highlights"]))
