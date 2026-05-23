#!/usr/bin/env python3
"""Enrichment for 2026-05-23.

arXiv set is identical to 2026-05-22 (50/50 ids overlap) -- reuse all
translations from prev day. HN/Reddit/GitHub/blogs reuse prior Japanese
translations for overlapping URLs and translate new items inline.
Five fresh highlights selected for the day.
"""
import json
from pathlib import Path

DATE = "2026-05-23"
PREV = "2026-05-22"
ROOT = Path(__file__).resolve().parent.parent
SRC_RAW = ROOT / "data" / f"raw-{DATE}.json"
SRC_PREV = ROOT / "data" / f"{PREV}.json"
OUT = ROOT / "data" / f"{DATE}.json"

d = json.loads(SRC_RAW.read_text(encoding="utf-8"))
d["date"] = DATE
prev = json.loads(SRC_PREV.read_text(encoding="utf-8"))

# ─── Reuse prior arXiv translations by id ───
prev_arxiv = {}
for it in prev["sources"].get("arxiv", []):
    if it.get("id"):
        prev_arxiv[it["id"]] = (it.get("title_ja"), it.get("summary_ja"))

# ─── Reuse prior translations (others by url) ───
prev_url = {}
for src in ("hn", "reddit", "github", "blogs"):
    for it in prev["sources"].get(src, []):
        if it.get("url"):
            prev_url[it["url"]] = (it.get("title_ja"), it.get("summary_ja"))

# ─── HN translations for today's new items ───
hn_url_map = {
    "https://api-docs.deepseek.com/quick_start/pricing": (
        "DeepSeek、V4 Proの値下げを恒久化",
        "DeepSeekはV4 Proの期間限定だった価格割引を恒久化。OpenAI/Anthropicとの価格競争を一段と加速させ、開発者向けの実効単価でフロンティア層と直接対峙する姿勢を鮮明にした。"),
    "https://www.theverge.com/tech/930447/microsoft-claude-code-discontinued-notepad": (
        "Microsoft、Claude Codeライセンスを打ち切り",
        "Microsoftが社内のClaude Codeライセンスを廃止し、自社製/OpenAI製の代替に統合する方針。トークン課金が予算をオーバーランした件と表裏一体で、エンタープライズのAI調達戦略の見直しが進んでいる。"),
    "https://modelrift.com/blog/openscad-llm-benchmark/": (
        "Antigravity 2.0がOpenSCAD建築3D LLMベンチで首位",
        "GoogleのコーディングIDE Antigravity 2.0がOpenSCAD建築モデリングのLLMベンチマークでトップに。3D空間推論を要する記述タスクでフロンティアLLMの優劣が逆転しつつあることを示す。"),
    "https://www.joshwcomeau.com/email/wham-launch-005-elephant-2-p/": (
        "AIは既存の技術スキルを掛け算する",
        "Josh Comeauの主張。AIはスキルの代替ではなく、土台となる技術力の上に積まれて生産性を桁違いに高める「乗算器」として機能する。素人がAIで一気に専門家になるわけではない、という現実的な視点。"),
    "https://isaiprofitable.com/": (
        "AIはまだ儲かっているか？",
        "主要AI企業の収益性をシンプルなページで可視化するサイト。OpenAI/Anthropic/Googleなどの推定P/Lを並べ、「AIは本当に儲かっているのか」という古典的な問いに端的に答える試み。"),
    "https://fortune.com/2026/05/22/microsoft-ai-cost-problem-tokens-agents/": (
        "Microsoft内部資料：AIは人を雇うより高い",
        "Fortuneが入手したMicrosoft内部分析。エージェント時代のトークン消費が爆発し、AIに任せる方が人件費より高くつくケースが多発。AI万能論への強烈な冷や水で、投資家層にも波及している。"),
    "https://this.weekinsecurity.com/oura-says-it-gets-government-demands-for-user-data-will-it-share-how-many/": (
        "Ouraリング、政府からのデータ要求を受けていることを公表",
        "ウェアラブル「Oura」が政府機関からユーザデータの開示要求を受けていることを認めた。健康センサーデータの法執行アクセスは初期だが、心拍や睡眠などプライバシー含意が大きい問題として注目される。"),
    "https://libertas.software/en/knowledge-hub/19/the-companies-cutting-headcount-for-ai-will-lose-to-th": (
        "AIで人員を削った企業は、削らなかった企業に負ける",
        "「AIで首切り」を進めた企業より、AIで既存社員を強化した企業が長期で勝つという主張。レイオフ報道が続く中、組織能力の積み上げを重視する反対意見として広く共有された。"),
    "https://dontquotetheai.com/": (
        "AIの出力をそのまま貼り付けないで",
        "Slack等でAI回答をそのままコピペして送ってくる相手にうんざりした人向けのマニフェスト風サイト。AI時代の対人マナー＝自分のフィルタを通せ、という空気を象徴する小ネタ。"),
    "https://github.com/anomalyco/models.dev": (
        "Models.dev: AIモデル仕様・価格・能力のDB",
        "AIモデルのスペック・価格・対応機能を横断比較するオープンソースDB。エージェント自動選択や調達検討で参照する用途を狙う。"),
    "https://www.cato.org/blog/dhs-quits-granting-green-cards-almost-entirely": (
        "DHS、グリーンカード発行をほぼ停止",
        "Cato研究所のブログ。米DHSが新規グリーンカード発給を実質凍結しているというデータ分析。AI業界の海外人材調達にも影響する政策ニュースとしてHNでも議論。"),
    "https://www.businessinsider.com/steve-wozniak-apple-ai-graduation-speech-2026-5": (
        "ウォズニアック、卒業式で『AI＝Actual Intelligence』と説いて喝采",
        "Apple共同創業者のウォズニアックが卒業生に「AI（人工知能）より大事なのは Actual Intelligence（本物の知性）」と語って大きな拍手。AIブームへの軽妙なカウンター言説として広がっている。"),
    "https://annas-archive.gl/blog/llms-txt.html": (
        "LLMの皆さん、これを読んでください",
        "海賊版書籍/論文ライブラリ Anna's Archive が「LLMが学習する際はうちのデータも使っていい」と公式に宣言。著作権処理を回避する形で『LLM時代の知識コモンズ』を自称する強気な立ち位置。"),
    "https://github.com/yt-dlp/yt-dlp/issues/16766": (
        "yt-dlpがBunサポートを縮小・非推奨化",
        "動画ダウンローダ yt-dlp プロジェクトが Bun ランタイムのサポートを限定的とし非推奨化。AIには直接関係ないが、JS実行系の標準争いとして波及効果が大きい変化。"),
    "https://github.com/amatsuda/rubish": (
        "Rubish: 純Rubyで書かれたUnixシェル",
        "全てRubyで実装されたUnixシェル。AI関連ではないがHNでバズった創作プロジェクト系の話題。"),
    "https://github.com/unprovable/ShadowCat": (
        "ShadowCat: QRコード経由でブラウザ間ファイル転送",
        "QRコードを連続表示して片方の端末から別の端末へファイル転送するブラウザツール。LANやBluetoothに頼らない物理的なエアギャップ転送のデモンストレーション。"),
    "https://www.euronews.com/my-europe/2026/05/21/italy-moves-to-airbus-a330-tankers-in-major-nato-aligned-shift": (
        "イタリア、ボーイング給油機をキャンセルしA330MRTTへ",
        "イタリアがボーイングPegasus給油機の発注を取りやめ、エアバスA330 MRTTに切替。NATO内の調達整合性が背景。AIとは無関係だが地政学・産業の重大ニュースとして上位入り。"),
    "https://kk.org/cooltools/book-freak-210-the-art-of-money-getting/": (
        "古典 \"The Art of Money Getting\" レビュー",
        "Kevin Kellyによる19世紀の自己啓発古典紹介。AI関連ではない読み物。"),
    "https://www.1940airterminal.org/news/liquidation-of-simulators": (
        "1940年エアターミナル博物館、清算開始",
        "古い航空関連シミュレータを保管していた博物館が解散へ。AIとは無関係。"),
    "https://horace.io/brrr_intro.html": (
        "深層学習を高速化する第一原理 (2022)",
        "GPU上で深層学習を高速に回すための計算/メモリ帯域/オーバーヘッドという3軸の枠組み。2022年の名記事が再びHN上位に。エージェント時代の推論最適化文脈で再評価。"),
}

# ─── Reddit translations for today's new items ───
reddit_translations = {
    "Microsoft Cancels Internal Anthropic Licenses As Shift To Token-Based AI Billing Blows Up Annual Budgets In Months": (
        "Microsoft、社内Anthropicライセンスを取消し──トークン課金で年間予算が数ヶ月で破裂",
        "MicrosoftがClaude Code等の社内利用を打ち切り。エージェント時代のトークン消費爆発で、想定の数倍コストが出てしまったことが背景とされる。AI調達のリスクが顕在化した事例。"),
    "Interesting Response from Gemini": (
        "Geminiから興味深い回答が返ってきた件",
        "Geminiの予想外な応答スクリーンショットがバズり。アライメントやペルソナの揺らぎを示唆する小ネタとして広く共有された。"),
    "Exclusive: Departing Meta staffer posts biting anti-AI video internally amid mass layoffs": (
        "退職するMeta社員、社内に痛烈な反AI動画を投下",
        "大規模レイオフのさなか、退職するMeta社員が「AIへの過信」を皮肉る内部動画を公開。組織内のAI推進派と懐疑派の溝を可視化したリーク。"),
    "Amnesty : US software company Palantir and other contractors were granted unlimited access to identifiable NHS England patient information": (
        "Amnesty報告：PalantirがNHS England患者データに無制限アクセス",
        "Amnesty Internationalの報告で、PalantirなどのIT企業がNHS Englandの個人特定可能な患者情報に無制限にアクセスできる契約構造が指摘された。AI/データ統治の象徴的な事例。"),
    "Rethinking AI Bubble": (
        "AIバブル論を再考する",
        "「AIバブル崩壊」をめぐる議論への反論ポスト。インフラ投資の規模と実需を分けて見るべき、という立論で多くのコメントが付いた。"),
    "NuExtract3 released: open-weight 4B VLM for Markdown, OCR and structured extraction (self-hostable) [P]": (
        "NuExtract3公開：4Bオープン重みVLMでMarkdown/OCR/構造化抽出",
        "NuMindから4Bパラメータのオープン重みVLM「NuExtract3」がリリース。Markdown変換・OCR・スキーマベースの構造化抽出を狙ったセルフホスト可能なモデル。"),
    "Novel Problems in VLA [R]": (
        "VLA（視覚-言語-行動）モデルの新しい難問",
        "ロボット用VLMで未解決の問題群を整理する研究議論ポスト。行動空間・物理整合・サンプル効率などコミュニティの関心が高い領域。"),
    "COLM 2026 ReviewsDiscussion [D]": (
        "COLM 2026レビュー結果ディスカッション",
        "言語モデル系トップ会議 COLM 2026 の査読が共有され、スコア分布・査読品質をめぐる毎年恒例の議論が始まった。"),
    "Elon, stop trying to make Grok happen.\nNew data suggests government workers don’t like Elon Musk’s chatbot. Does anybody?": (
        "イーロン、もうGrokは諦めて：政府職員にも不評",
        "新データで米政府職員のGrok利用率がほぼゼロと判明。マスクが押し進めるGrok普及策が現場で受け入れられていない様子を伝える皮肉な記事。"),
    "This just happened": (
        "今こんなことが起きた",
        "ChatGPT/Geminiなどとのやり取りで起きた珍事スクショ系ポスト。文脈情報乏しいが、コメント欄でモデルの癖を語り合うスレッドに。"),
    "Could AI eventually become something like a system that expands human understanding for humanity": (
        "AIは人類の理解を拡張するシステムになり得るか",
        "AIを「人類の理解装置」として位置付ける哲学的議論。短いポストながらコメント欄に長文の応答が連なった。"),
    "The musical chairs game of AI": (
        "AI業界の椅子取りゲーム",
        "OpenAI/Anthropic/Google/xAIの間で続く研究者引き抜き合戦を、椅子取りゲームに喩えたエッセイ。短期サイクルでの人事流動を一覧化。"),
    "AI training is becoming the new coding revolution": (
        "AIトレーニングは新たな『プログラミング革命』",
        "プロンプト/ファインチューニング/小型モデル学習のスキルが、かつてのコーディング能力のように汎用キャリアスキルになりつつある、という主張。"),
    "I think AI training is way more accessible than people realize": (
        "AI訓練は思っているより敷居が低い",
        "個人でも小型モデルのファインチューニングや独自評価セット構築が十分可能、というやや楽観的なポスト。コメント欄では現実的な制約も議論。"),
    "Claude made me realize most AI models optimize for confidence, not truth": (
        "ClaudeでわかったAIの真実：多くのモデルは確信度を最適化していて真実を最適化していない",
        "Claudeが「自信ありげに間違える」現象から、現行モデルは「もっともらしさ」を最大化していて真実性は二次的、と気づいたユーザのポスト。"),
    "Live Human Detector on Outbound Phone Calls [R]": (
        "アウトバウンド通話の「生身の人間」検出器",
        "自動発信時に相手が人間か留守電/IVRかを判定する音声モデルの研究紹介。営業オートコール文脈でのプロダクト寄り研究。"),
    "Starbucks": (
        "スタバ、AI注文の話",
        "スターバックスのAI関連体験談ポスト。文脈不足だが小ネタとして上位入り。"),
    "pipeline is really slow - consulting [D]": (
        "MLパイプラインが遅すぎる相談",
        "コンサル現場のMLパイプライン高速化相談スレッド。データ前処理・特徴量・推論コストの典型的なボトルネック議論。"),
    "OpenAI is hiring a $445,000 researcher. Requirements? Be 'tasteful and strategic.'": (
        "OpenAI、年収445Kの研究者を募集──要件は『洗練と戦略性』",
        "OpenAIが新ポジションで年収約4,500万円の研究者を募集。職務記述書に『tasteful and strategic』とだけ書かれた要件が話題になり、AI業界の価値観を象徴する求人として拡散した。"),
}

# ─── GitHub trending translations (today's new items) ───
github_url_map = {
    "https://github.com/multica-ai/andrej-karpathy-skills": (
        "andrej-karpathy-skills: KarpathyのLLMコーディング洞察をCLAUDE.md化",
        "Andrej KarpathyがLLMコーディングで指摘してきた落とし穴を1つのCLAUDE.mdに集約したリポジトリ。Claude Codeなどのエージェント挙動をプロジェクト単位で改善する用途で爆発的に伸びている（149K+★）。"),
    "https://github.com/colbymchenry/codegraph": (
        "codegraph: コーディングエージェント向けの事前構築コード知識グラフ",
        "Claude Code/Codex/Cursor/OpenCodeなどのコーディングエージェント向けに、コードベースを事前にナレッジグラフ化してツール呼び出し回数とトークン消費を削減するローカル実行ツール。"),
    "https://github.com/anthropics/claude-plugins-official": (
        "anthropics/claude-plugins-official",
        "Anthropic公式が管理する高品質Claude Codeプラグインのディレクトリ。サードパーティ製プラグインのキュレーションを公式に始めたシグナル。"),
    "https://github.com/rohitg00/ai-engineering-from-scratch": (
        "ai-engineering-from-scratch: AIエンジニアリングを基礎から構築",
        "RAG/Agents/評価/デプロイなどAIエンジニアリングの実装をスクラッチから学ぶ教材リポジトリ。コミュニティ向けに丁寧に構築されている。"),
    "https://github.com/Fincept-Corporation/FinceptTerminal": (
        "FinceptTerminal: モダンな金融分析アプリ",
        "Bloomberg Terminal風の市場分析・投資リサーチ・経済データツール。AIではないがオープンソース金融端末として注目。"),
    "https://github.com/ChromeDevTools/chrome-devtools-mcp": (
        "chrome-devtools-mcp: コーディングエージェント向けChrome DevTools",
        "Chrome DevToolsの機能をMCP経由でAIエージェントに公開する公式実装。Webデバッグやパフォーマンス計測をエージェントが扱える。"),
    "https://github.com/multica-ai/multica": (
        "multica: マネージド・エージェント・プラットフォーム",
        "コーディングエージェントを『実際のチームメイト』として扱う、タスクアサインや進捗トラッキング、スキル蓄積を備えたオープンソースのマネージドエージェント基盤。"),
    "https://github.com/presenton/presenton": (
        "presenton: オープンソースのAIプレゼン生成器",
        "Gamma/Beautiful AI/Decktopusの代替を狙うオープンソースのAIスライド生成ツール。API提供あり。"),
    "https://github.com/dotnet/skills": (
        "dotnet/skills: .NET/C#向けAIエージェント用スキル集",
        "Microsoft/.NETチーム公式の、AIコーディングエージェント支援用スキル集。Claude Codeなどのスキル機能に対応した.NET特化リポジトリ。"),
    "https://github.com/mukul975/Anthropic-Cybersecurity-Skills": (
        "Anthropic-Cybersecurity-Skills: 754のサイバーセキュリティ用スキル",
        "MITRE ATT&CK/NIST CSF 2.0/MITRE ATLAS/D3FEND/NIST AI RMFにマッピングされた754のサイバーセキュリティスキルをAIエージェント向けに構造化したコレクション。"),
}

# ─── Blogs translations (today's new items) ───
blogs_url_map = {
    # New blog today: Nemotron Diffusion (no url? check raw) — handled below
}

# ─── Apply enrichments ───

# arxiv
for it in d["sources"].get("arxiv", []):
    aid = it.get("id")
    if aid in prev_arxiv:
        tj, sj = prev_arxiv[aid]
        if tj:
            it["title_ja"] = tj
        if sj:
            it["summary_ja"] = sj

# hn
for it in d["sources"].get("hn", []):
    u = it.get("url")
    if u in prev_url and prev_url[u][0]:
        it["title_ja"], it["summary_ja"] = prev_url[u]
    elif u in hn_url_map:
        it["title_ja"], it["summary_ja"] = hn_url_map[u]

# reddit (translate by title because reddit urls are subreddit links)
for it in d["sources"].get("reddit", []):
    u = it.get("url") or it.get("permalink")
    if u in prev_url and prev_url[u][0]:
        it["title_ja"], it["summary_ja"] = prev_url[u]
    else:
        t = it.get("title")
        if t in reddit_translations:
            it["title_ja"], it["summary_ja"] = reddit_translations[t]

# github
for it in d["sources"].get("github", []):
    u = it.get("url")
    if u in prev_url and prev_url[u][0]:
        it["title_ja"], it["summary_ja"] = prev_url[u]
    elif u in github_url_map:
        it["title_ja"], it["summary_ja"] = github_url_map[u]

# blogs
blogs_title_map = {
    "Towards Speed-of-Light Text Generation with Nemotron-Labs Diffusion Language Models": (
        "Nemotron-Labs拡散言語モデルで『光速テキスト生成』へ",
        "NVIDIA Nemotron-Labsが、自己回帰ではなく拡散モデルで文章を生成する『Nemotron Diffusion LM』を発表。長文生成のレイテンシをGPU効率の観点で大幅短縮できると主張し、Transformer以外の言語生成パラダイムへの本格投資を示す。"),
    "How Virgin Atlantic ships faster with Codex": (
        "Virgin Atlantic、Codexで開発を加速",
        "OpenAIのCodexを用いてVirgin Atlanticがソフトウェアリリースを高速化した事例。大企業のCodex導入事例として宣伝された。"),
}

for it in d["sources"].get("blogs", []):
    u = it.get("url")
    if u in prev_url and prev_url[u][0]:
        it["title_ja"], it["summary_ja"] = prev_url[u]
    else:
        t = it.get("title")
        if t in blogs_title_map:
            it["title_ja"], it["summary_ja"] = blogs_title_map[t]

# ─── Highlights ───
def find_item(src, predicate):
    for it in d["sources"][src]:
        if predicate(it):
            return it
    return None

highlights = []

# 1. Microsoft AI more expensive than humans (Fortune)
it = find_item("hn", lambda x: "Microsoft reports AI is more expensive" in x.get("title", ""))
if it:
    highlights.append({
        "source": "hn",
        "title": it["title"],
        "title_ja": "Microsoft内部資料：AIは人を雇うより高くつく",
        "url": it["url"],
        "hot_take_ja": "「AIで人を置き換えればコストが下がる」という前提が崩れ始めた。Microsoftの内部分析でさえ、エージェント時代のトークン消費は人件費を超えると示している。AIで\"雇う\"より\"切る\"を急いだ企業ほど、来年の決算で痛い目を見るかもしれない。",
        "detail_ja": "Fortuneが入手したMicrosoftの社内資料によると、生成AIエージェントを業務に組み込んだ場合のトークン課金が想定を大きく上回り、人を雇う方が安いケースが多発しているという。背景にはエージェントの自律実行に伴う長時間・多段の推論があり、1回の業務処理で数百万トークンに達するケースもある。Microsoft自身が同じ週にClaude Code等の社内ライセンスを取消したことと符合し、エンタープライズAI調達の経済性が根本から見直されつつあることを示す。トークン単価は下がり続けているが、エージェントの利用量はそれ以上のペースで増加するため、年間予算が数ヶ月で蒸発するパターンが顕在化。投資家層も「AIで人件費が下がる」前提のバリュエーションを疑い始めている。一方で、AIが真に置き換え可能なタスクと、置き換えると逆にコスト増になるタスクを切り分けるFinOps的な動きも始まっている。",
        "detail_en": "An internal Microsoft analysis obtained by Fortune shows that, once token-based billing for generative AI agents is factored in, AI is often more expensive than hiring humans for the same work. The driver is agentic execution: a single task can chew through millions of tokens across long, multi-step reasoning chains. Microsoft itself, in the same week, cancelled internal Claude Code licenses, underscoring how rapidly the economics of enterprise AI procurement are being reassessed. Per-token prices keep falling, but agent usage is growing even faster, so annual AI budgets are evaporating in months. Investors are starting to question valuations built on the assumption that AI will cut payroll costs. A counter-trend is also emerging: FinOps-style efforts to separate tasks where AI genuinely replaces labor from those where it raises total cost.",
        "key_points_ja": [
            "Microsoft内部分析：AI＞人件費のケース多発",
            "エージェント長時間実行で消費トークン爆発",
            "同社はClaude Code社内ライセンスも打ち切り",
            "『AIで人を減らせばコスト減』前提が揺らぐ",
            "AI FinOpsという新領域が立ち上がりつつある",
        ],
        "key_points_en": [
            "Microsoft internal data: AI often costs more than hiring",
            "Agentic loops burn millions of tokens per task",
            "Same week MSFT killed internal Claude Code licenses",
            "Headcount-replacement narrative under pressure",
            "AI FinOps emerging as a distinct discipline",
        ],
    })

# 2. DeepSeek V4 Pro permanent discount
it = find_item("hn", lambda x: "DeepSeek" in x.get("title", "") and "V4 Pro" in x.get("title", ""))
if it:
    highlights.append({
        "source": "hn",
        "title": it["title"],
        "title_ja": "DeepSeek、V4 Pro値下げを恒久化──フロンティアと真っ向勝負",
        "url": it["url"],
        "hot_take_ja": "DeepSeekが期間限定だったV4 Pro値下げを公式に「ずっとこの価格」に切り替え。Microsoftが「AIは人より高い」と嘆く同じ週に、中国勢が値段で殴り続ける構図がはっきりした。フロンティアモデルの実効単価は、もう国境線で議論する段階ではない。",
        "detail_ja": "DeepSeekは旗艦モデルDeepSeek V4 Proのプロモーション割引を恒久化すると発表した。割引前は他社フロンティアモデルに近い水準だったが、今後は通常価格として大幅に安価な単価が適用される。中国勢の追い上げで、推論コスト面ではOpenAI/Anthropicが選択肢の中心と言える時期は終わりつつある。同時期にMicrosoftがエージェント課金で予算超過を起こし内部Claude Codeライセンスを取消した報道もあり、安価で十分強力なオープン/中華系モデルへの需要圧力が一層強まる構図だ。エンタープライズ顧客はもはや「ベストモデル」だけでなく「タスク当たり総コスト」で評価する流れに移行しており、DeepSeekの今回の決定はその圧力に明確に応える動き。一方でモデル能力ベンチでV4 Proがフロンティアにどこまで追いついているかは依然議論があり、価格と性能のトレードオフが各社で再評価される。",
        "detail_en": "DeepSeek made its V4 Pro promotional pricing permanent, formalizing a steep discount that previously had an end date. With Microsoft openly admitting in the same week that AI agents cost more than employees and cancelling internal Claude Code licenses, the global frontier-model price war just escalated. Enterprise buyers increasingly evaluate models on total cost per task, not just raw capability, and DeepSeek is leaning hard into that calculus. Whether V4 Pro actually matches the frontier on hard benchmarks remains debated, but its effective price/performance is now low enough that many teams will at least test it for high-volume agentic workloads. The decision pressures Western labs to either drop list prices further or differentiate on reliability, tooling, and safety guarantees.",
        "key_points_ja": [
            "V4 Pro価格割引が常時適用に",
            "フロンティアとの実効単価差が拡大",
            "MS『AIは人より高い』報道と同タイミング",
            "総コスト＝(モデル能力×タスク当たり消費)で評価へ",
            "OpenAI/Anthropicへの価格圧力さらに強まる",
        ],
        "key_points_en": [
            "V4 Pro discount becomes the permanent list price",
            "Effective gap to frontier models widens further",
            "Lands same week MSFT calls AI more expensive than hiring",
            "Buyers shift to cost-per-task, not best benchmark",
            "Pressure mounts on OpenAI/Anthropic list pricing",
        ],
    })

# 3. Nemotron Diffusion Language Models
it = find_item("blogs", lambda x: "Nemotron-Labs Diffusion" in x.get("title", ""))
if it:
    highlights.append({
        "source": "blogs",
        "title": it["title"],
        "title_ja": "NVIDIA、拡散モデルでテキストを『光速生成』するNemotron Diffusion LM",
        "url": it.get("url", ""),
        "hot_take_ja": "Transformerの自己回帰生成は1トークンずつ進むのが宿命。NVIDIAは「文章も画像生成と同じく拡散で並列に作れる」と本気で主張し、Nemotron Diffusion LMでレイテンシを桁レベル削るデモを出した。エージェント時代の最大のボトルネックは「遅さ」であり、もしこれが本物なら、推論パラダイムの再編が起きる。",
        "detail_ja": "NVIDIA Nemotron-LabsはDiffusion Language Model（DLM）アプローチで、テキスト生成のレイテンシを大幅に短縮したと発表した。一般的なLLMは自己回帰でトークンを1つずつ生成するため、長文ほど時間がかかる。一方DLMはノイズ除去で並列に複数トークンを生成でき、画像拡散モデルと同じ思想でテキストを扱う。NVIDIAはGPUの並列性を最大限活用すれば「光速に近い」生成が可能と主張し、ベンチで自己回帰モデルと同等品質を維持しつつ大幅な速度向上を示した。これは特にエージェント・長文要約・コード生成の遅延ボトルネックに直撃する話題で、もし広範囲に通用するなら推論パイプライン全体が組み直しになる。一方で複雑な推論や厳密な制約への対応、トークン依存の強いタスクでは依然課題があり、Transformer自己回帰との棲み分けが現実解という見方も強い。NVIDIA自身は自社GPUの強みである並列性を最大限活かせる方式を推進する戦略的意味もある。",
        "detail_en": "NVIDIA's Nemotron-Labs unveiled a Diffusion Language Model (DLM) that generates text by denoising in parallel rather than autoregressive token-by-token decoding. Long-form generation latency drops dramatically because GPU parallelism is used end-to-end, much like image diffusion. The team claims quality comparable to autoregressive baselines on internal benchmarks, while pushing toward what they call \"speed-of-light\" generation. If the approach generalizes, the most painful bottleneck of the agentic era — long-context, multi-step latency — could collapse. Caveats remain: complex reasoning, strict constraints, and tasks with strong token-level dependencies still favor autoregression, and many will treat DLMs as a complement rather than a replacement. The strategic angle is also clear: parallel decoding maps perfectly onto NVIDIA's hardware strengths.",
        "key_points_ja": [
            "拡散モデルで並列にテキスト生成",
            "自己回帰と同等品質で大幅低遅延を主張",
            "エージェントの長文遅延を狙い撃ち",
            "厳密推論等は自己回帰優位の余地あり",
            "GPU並列性を最大化＝NVIDIAの戦略適合",
        ],
        "key_points_en": [
            "Diffusion-based parallel text generation",
            "Claims AR-comparable quality, far lower latency",
            "Aimed at agentic long-context bottlenecks",
            "AR still likely wins on strict reasoning tasks",
            "Plays directly to NVIDIA GPU parallelism",
        ],
    })

# 4. OpenAI hires tasteful and strategic
it = find_item("reddit", lambda x: "OpenAI is hiring a $445,000" in x.get("title", ""))
if it:
    highlights.append({
        "source": "reddit",
        "title": it["title"],
        "title_ja": "OpenAI、年収445Kの研究者を募集──要件はただ『洗練と戦略性』",
        "url": it.get("url", "https://www.reddit.com" + it.get("permalink", "")),
        "hot_take_ja": "OpenAIの新求人が話題。年収約4,500万円のポストに必要なのは『tasteful and strategic』──論文業績でも特定スキルでもなく、センス。AI研究の評価軸がいかに「定量からセンスへ」シフトしているかを示す象徴的な求人で、Twitterでは皮肉と憧れが半々で飛び交っている。",
        "detail_ja": "OpenAIが新たに開いた研究者ポジションは年収約44.5万ドル（約4,500万円）。だが職務記述書には特定の博士号要件もML技能要件も無く、代わりに『tasteful and strategic（洗練されていて戦略的）』というやや抽象的な要件が書かれていることがバズった。これは、モデルが急速に賢くなる時代において、研究者個人の価値が「実装スキル」から「何を作るべきかを見極めるセンス＝taste」と「どう動くべきか＝strategy」にシフトしているという業界の合意の現れでもある。SteveJobsが繰り返した『taste matters』論や、Karpathyが最近言及した『AIエンジニアの新しい技能はテイスト』論ともきれいに重なる。一方で、客観基準の薄い採用は属人的なネットワーク採用に偏りやすく、批判の声もある。求人文化として『センス採用』が今後どこまで広がるかは、AI業界の人材像そのものの議論につながる。",
        "detail_en": "OpenAI opened a research role paying around $445K/year with a job description that, instead of degrees or specific skills, asks the candidate to be \"tasteful and strategic.\" The wording went viral on Reddit and Twitter because it crystallizes a real shift: as models get smarter, the bottleneck moves from implementation skill to judgment — what to build, what to ignore, how to position. Echoes of Karpathy's recent comments about \"taste\" as the new core skill for AI engineers, and Jobs-style design culture, are all over the discussion. Critics note the obvious downside: \"taste\" is hard to evaluate fairly and risks reinforcing insider networks. Still, the post is a useful artifact of what frontier labs now value in senior researchers.",
        "key_points_ja": [
            "OpenAIが$445Kの研究者ポスト公開",
            "要件が『tasteful and strategic』のみ",
            "実装スキルからセンスへの評価シフト",
            "Karpathy『新しい技能はテイスト』論と符合",
            "属人的採用への懸念も同時に噴出",
        ],
        "key_points_en": [
            "OpenAI posts a $445K researcher role",
            "Requirements: simply \"tasteful and strategic\"",
            "Signals a shift from implementation to judgment",
            "Echoes Karpathy's \"taste is the new skill\" thesis",
            "Critics flag risks of nepotism in subjective hiring",
        ],
    })

# 5. Karpathy CLAUDE.md skills going viral
it = find_item("github", lambda x: "andrej-karpathy-skills" in x.get("full_name", ""))
if it:
    highlights.append({
        "source": "github",
        "title": it["full_name"],
        "title_ja": "Karpathy流コーディング教訓を1つのCLAUDE.mdに固めた『andrej-karpathy-skills』が爆伸び",
        "url": it["url"],
        "hot_take_ja": "Karpathy本人がXで繰り返してきた『LLMはこの種のミスをしがち』という観察を、丸ごとClaude Codeのプロジェクト指示（CLAUDE.md）に翻訳したリポジトリが、1日で3,000★以上の勢いで伸びている。エージェントの賢さを引き出すのは「もっといいモデル」ではなく「もっといい指示書」だ、という現場感の正しい反映と言える。",
        "detail_ja": "GitHubトレンド首位の『multica-ai/andrej-karpathy-skills』は、Andrej Karpathyが過去にX/YouTubeで繰り返し言及してきたLLMコーディングの落とし穴（過剰な抽象化、テスト軽視、デバッグでの妄想推論など）を、Claude CodeのプロジェクトレベルでLLMに食わせるCLAUDE.mdとして単一ファイルにまとめたもの。Claude Codeはディレクトリ直下のCLAUDE.mdを自動で読み、全タスクに渡って指示を効かせるため、リポジトリ単位で『AIの行動ポリシー』を共有できる。本ツールはその枠組みを使い、誰でもKarpathy式のレビュー視点をエージェントに与えられるようにした点が支持されている。総スター数は約149K、24時間で+3,372とほぼ瞬間的なバイラル。背景には、コーディングエージェントの普及で『プロンプトよりプロジェクト全体のシステムプロンプト設計が効く』という共通理解が広がっていることがある。なお、Karpathy本人が公式に関与しているわけではなく、コミュニティ編集型のキュレーション。",
        "detail_en": "`multica-ai/andrej-karpathy-skills` topped GitHub trending by distilling Andrej Karpathy's well-known critiques of LLM coding behavior — over-abstracting, ignoring tests, hallucinating debugging steps — into a single CLAUDE.md that Claude Code automatically loads at the project root. The hit rate is ~149K stars total and +3,372 in the last 24 hours. The popularity isn't really about Karpathy's specific advice; it's about the realization that coding-agent quality is now driven less by model upgrades and more by how the project tells the agent to behave. CLAUDE.md became the de facto place to encode that, and curated community files like this one are the closest thing to \"shareable agent policies.\" Note the project is community-curated, not officially endorsed by Karpathy.",
        "key_points_ja": [
            "Karpathy流のLLMコード批評を1ファイルに集約",
            "Claude Codeが自動で読むCLAUDE.mdとして配布",
            "24時間で+3.3K★、累計約149K★の急上昇",
            "『良いモデル』より『良い指示書』が効く時代",
            "Karpathy本人公式ではなくコミュニティ編集",
        ],
        "key_points_en": [
            "Karpathy's LLM coding lessons bundled into one CLAUDE.md",
            "Loaded automatically by Claude Code at repo root",
            "+3.3K stars in 24h, ~149K total — instant viral",
            "Reflects shift: better instructions > better model",
            "Community-maintained, not officially Karpathy's",
        ],
    })

d["highlights"] = highlights

OUT.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT} with {len(highlights)} highlights")

# Quick coverage check
for src in ("arxiv", "hn", "reddit", "github", "blogs"):
    items = d["sources"][src]
    miss = sum(1 for it in items if not it.get("title_ja"))
    print(f"  {src}: {len(items)} total, {miss} untranslated")
