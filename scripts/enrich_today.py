#!/usr/bin/env python3
"""Enrich raw-2026-06-14.json with Japanese/English summaries and highlights."""
import json
from pathlib import Path

DATE = "2026-06-14"
ROOT = Path(__file__).resolve().parent.parent
raw = json.loads((ROOT / f"data/raw-{DATE}.json").read_text())

# ---- arXiv (top 25) ----
arxiv_enrich = {
    0: ("EvoArena: 動的環境でのLLMエージェントの記憶進化を追跡", "環境が段階的に変化する状況でエージェントを評価するベンチマーク。記憶を構造化された更新履歴として記録するパッチ型メモリ(EvoMem)を提案し、環境進化への適応力を測る。"),
    1: ("検索拡張RL微調整で類推による推論を学習", "過去の類似問題を検索して強化学習の微調整に活かすことで、LLMが「類推」によって新しい問題を解く能力を高める手法。"),
    2: ("InterleaveThinker: エージェント的な思考と生成の交互実行を強化", "思考(reasoning)と行動/生成を交互に挟み込むエージェントを強化学習で訓練。長い対話やタスクで思考と出力をうまく織り交ぜる。"),
    3: ("Mana: 関節を持つ道具の器用な操作", "ハサミやペンチのように関節のある道具をロボットハンドで器用に扱うための学習手法。"),
    4: ("フロー反転ステアリングでロボット汎用方策を改善", "拡散/フローモデルの生成過程を逆向きに誘導することで、ロボットの汎用方策の性能を底上げする。"),
    5: ("Modality Forcing: スケーラブルな空間生成", "複数モダリティを強制的に整合させることで、大規模な3D空間生成を安定・高品質化するアプローチ。"),
    6: ("RepWAM: 表現的な視覚-行動トークナイザによる世界行動モデリング", "視覚と行動を共通トークンで表現し、世界モデルと行動予測を統合的に学習する枠組み。"),
    7: ("SpatialClaw: エージェント的空間推論の行動インタフェースを再考", "空間推論をするエージェントが環境とやり取りする「行動の出し方」を見直し、より効果的な操作インタフェースを設計。"),
    8: ("WEAVER: ロボット操作のための効果的な世界モデル", "より良く・速く・長く予測できるロボット操作用の世界モデル。長期の操作タスクで精度と効率を両立。"),
    9: ("グラフニューラルネットの切詰め位置エンコーディングを理解する", "GNNにおける位置エンコーディングを途中で切り詰める手法の効果と理論的性質を分析。"),
    10: ("大規模言語モデルによる社会・行動科学の再現性自動評価", "LLMを使って社会・行動科学の論文の再現性を自動でチェックする試み。査読・メタサイエンスの自動化に向けた一歩。"),
    11: ("Agents-K1: エージェントネイティブな知識オーケストレーション", "論文を要約や引用関係に縮約せず、実体・主張・証拠・手法系譜まで含む知識グラフに変換し、科学的推論を支援するパイプライン。"),
    12: ("Influcoder: デコーダの勾配影響ランキングをエンコーダに蒸留", "どの訓練データが出力に効いたか(データ帰属)を、重いデコーダ計算から軽いエンコーダへ蒸留して高速化。"),
    13: ("HyperTool: 段階的なツール呼び出しを超えるツール拡張エージェント", "一手ずつのツール呼び出しに留まらず、より大局的にツール群を計画・活用するエージェント設計。"),
    14: ("EurekAgent: 自律的科学発見にはエージェント環境工学こそ重要", "自律科学発見のボトルネックはワークフロー設計から「環境設計」へ移ったと主張。探索や成果物管理を促す環境を作ることが鍵だとする。"),
    15: ("Before You Think: System 0とAI媒介認知、認知の植民地化", "AIが思考の「前段(System 0)」として無意識に人の認知へ入り込み、外部の利害を自己の内部に埋め込む「認知の植民地化」を起こしうると論じる思想的論文。"),
    16: ("密な教師信号・疎な更新: オンポリシー蒸留のスパース性と幾何", "オンポリシー蒸留による重み更新は小さく座標的に疎で、FFN偏重。発見された部分ネットだけ訓練しても性能をほぼ再現できると示す。"),
    17: ("Flex4DHuman: 4D人体再構成のための柔軟な多視点動画拡散", "複数視点の動画から動く人体を4D(3D+時間)で再構成する拡散モデル。"),
    18: ("World Tracing: 見えない部分まで含む生成的ピクセル整合幾何", "画像から、見えていない領域まで含めて3D幾何を生成的に補完する手法。"),
    19: ("オペラド的整合性: ラベル不要でLLMの合成的推論失敗を検知", "問いを分解して合成した答えと、直接の答えが一致するかを見る指標(OC)。正解ラベルなしで多段推論の失敗を検知できる。"),
    20: ("SkMTEB: スロバキア語の大規模テキスト埋め込みベンチマーク", "スロバキア語向けの埋め込み評価ベンチマークとモデル適応手法。低資源言語のNLP整備。"),
    21: ("Surflo: 大域状態を持つ一貫した3D表面フローモデル", "3D表面上の流れを大域的な状態と整合させて一貫してモデル化する手法。"),
    22: ("Recursive Agent Harnesses: 再帰的エージェントハーネス", "親エージェントが実行可能なスクリプトを生成し、ファイル操作やコード実行を持つ「フルなサブエージェント」を並列に再帰生成するパターンを定式化(Anthropicの動的ワークフローが実例)。"),
    23: ("安定回復多様体: 継続学習における回復可能性を司る幾何原理", "継続学習でモデルが性能を回復できる条件を、パラメータ空間の幾何的構造から説明する。"),
    24: ("LLMの合成的推論のためのオペラド理論", "反復的な置換で系を組み立てるオペラド理論を、LLMの合成的推論の形式的枠組みとして導入。"),
}

arxiv = raw["sources"]["arxiv"]
for idx, (tja, sja) in arxiv_enrich.items():
    arxiv[idx]["title_ja"] = tja
    arxiv[idx]["summary_ja"] = sja

# ---- Hacker News (all) ----
hn_map = {
    "Statement on US government directive to suspend access to Fable 5 and Mythos 5":
        ("米政府指令によりFable 5とMythos 5へのアクセスを停止: Anthropic声明",
         "Anthropicが米政府の指令を受け最上位モデルFable 5/Mythos 5の提供を停止したという衝撃的な公式声明。HN首位3000超の大注目。"),
    "Open source AI must win":
        ("オープンソースAIは勝たねばならない",
         "クローズドな最先端モデルが政府指令で止められうる現実を背景に、オープンソースAIの重要性を訴えるキャンペーンサイト。"),
    "Amazon CEO's talks with U.S. officials triggered crackdown on Anthropic models":
        ("Amazon CEOと米当局の会談がAnthropicモデル規制の引き金に",
         "WSJ報道。Amazon CEOの米政府高官との協議が、Anthropicモデルへの取り締まりを誘発したとされる。商業的思惑が政策に影響した構図。"),
    "Pirates, a naval warfare game inspired by Sid Meier's Pirates":
        ("Pirates: Sid Meier's Piratesに着想を得た海戦ゲーム",
         "名作『Sid Meier's Pirates』に触発された個人開発の海戦ゲーム。"),
    "GLM 5.2 Is Out":
        ("GLM 5.2 がリリース",
         "智譜AI(Zhipu)のGLM 5.2が登場。Fable停止騒動の最中、中国系オープンモデルの存在感が増す。"),
    "WASI 0.3":
        ("WASI 0.3",
         "WebAssembly System Interfaceの新版0.3。非同期サポートなどでWASMのサーバサイド利用が前進。"),
    "We've suspended access to Claude Mythos 5 and Claude Fable 5":
        ("Claude Mythos 5とFable 5へのアクセスを停止: ステータスページ",
         "Anthropicの公式ステータスページに掲載された提供停止インシデント。"),
    "AI OSS tool repo goes archived over night after raising $7.3M Seed":
        ("OSS AIツールのリポジトリが$7.3Mシード調達直後に一夜でアーカイブ化",
         "TensorZeroが多額の資金調達後すぐリポジトリをアーカイブ。OSSと商業化の緊張を象徴する出来事として話題。"),
    "AI coding at home without going broke":
        ("破産せずに自宅でAIコーディングする",
         "高額なAPI課金を避け、ローカル/低コストでAIコーディング環境を整える実践的ガイド。"),
    "Slightly reducing the sloppiness of AI generated front end":
        ("AI生成フロントエンドの「雑さ」を少し減らす",
         "LLMが吐くフロントエンドコードの品質を改善する小ワザの紹介。"),
    "Police officer investigated for using AI to 'create evidence' in multiple cases":
        ("AIで「証拠を捏造」した疑いで警察官を捜査",
         "英ダービーシャー警察の警官が複数事件でAIを使い証拠を作成した疑い。司法とAI悪用の深刻な事例。"),
    "Shepherd's Dog: A Game by Fable":
        ("Shepherd's Dog: Fableが作ったゲーム",
         "AIモデルFableを使って作られたゲーム。"),
    "A dumpster arrived behind my university's library":
        ("大学図書館の裏にゴミ収集箱が届いた",
         "図書館が蔵書を廃棄していた件を追う個人ブログ。AIとは無関係だがHN人気。"),
    "Show HN: Paca – Lightweight Jira alternative for human-AI collaboration":
        ("Show HN: Paca – 人とAIの協働向け軽量Jira代替",
         "人間とAIエージェントが一緒に使うことを想定した軽量プロジェクト管理ツール。"),
    "Where Did Earth Get Its Oceans? Maybe It Made Them Itself":
        ("地球の海はどこから来たのか: 自前で作った可能性",
         "海の起源を地球内部に求める地球科学の研究。AI無関係だがHN人気。"),
    "/architect: Reduce Fable tokens by 80%, Fable orchestrates/reviews, Codex builds":
        ("/architect: Fableトークンを80%削減、Fableが統括しCodexが実装",
         "Fableに設計・レビューを任せ、実装はCodexに振ることでトークン消費を大幅削減するワークフロー。"),
    "Mmorpg World of ClaudeCraft, vibe coded with Fable 5":
        ("World of ClaudeCraft: Fable 5でバイブコーディングしたMMORPG",
         "Fable 5を使って『雰囲気で』作られたブラウザMMORPG。AIコーディングのデモとして話題。"),
    "As a result of a US Government directive, we are suspending access to Fable 5":
        ("米政府指令の結果、Fable 5へのアクセスを停止します",
         "ClaudeDevsのXポスト。開発者向けにFable 5停止を告知。"),
    "Orthodox C++ (2016)":
        ("Orthodox C++ (2016)",
         "現代的すぎる機能を避け素直なC++を書く流儀『Orthodox C++』を説く2016年の記事が再浮上。"),
    "PwC Report: AI Making Medical Bills Higher":
        ("PwCレポート: AIが医療費を押し上げている",
         "PwCの分析として、AI導入が医療コストを下げるどころか押し上げているとするFortune報道。"),
}
for it in raw["sources"]["hn"]:
    t = it.get("title", "")
    if t in hn_map:
        it["title_ja"], it["summary_ja"] = hn_map[t]

# ---- GitHub (all) ----
gh_map = {
    "addyosmani/agent-skills": ("AIコーディングエージェント向けの実戦的スキル集",
        "AIコーディングエージェントに与える『プロダクション品質のエンジニアリングスキル』を集めたリポジトリ。エージェント運用ノウハウへの関心の高さを反映。"),
    "apple/container": ("Apple Silicon上で軽量VMによりLinuxコンテナを実行",
        "Macの軽量仮想マシン上でLinuxコンテナを作成・実行するApple製ツール。DockerなしでネイティブにコンテナをMacで動かせる。"),
    "obra/superpowers": ("動くエージェント的スキルフレームワーク&開発手法",
        "AIエージェント向けのスキルフレームワークとソフトウェア開発方法論をまとめたプロジェクト。"),
    "NVIDIA/SkillSpector": ("AIエージェントのスキルを検査するセキュリティスキャナ",
        "NVIDIA製。AIエージェントの『スキル』に潜む脆弱性や悪意あるパターンを検出する。エージェントのサプライチェーン安全を狙う。"),
    "iptv-org/iptv": ("世界中の公開IPTVチャンネル集",
        "世界各国の公開IPTVチャンネルを集めた定番リポジトリ。AI無関係だが常連トレンド。"),
    "LMCache/LMCache": ("LLMを高速化する最速KVキャッシュ層",
        "LLM推論のKVキャッシュを効率化し、長文・反復処理を大幅高速化するライブラリ。"),
    "kenn-io/agentsview": ("コーディングエージェント向けのローカル分析ツール",
        "Claude Codeなどコーディングエージェントのセッションをローカルで解析・可視化するツール。"),
    "andrewyng/aisuite": ("複数生成AIプロバイダへの統一インタフェース",
        "Andrew Ng発。各社の生成AI APIを共通インタフェースで叩けるライブラリ。"),
    "x1xhlol/system-prompts-and-models-of-ai-tools": ("主要AIツールのシステムプロンプト集",
        "Cursor/Claude Code/Devinなど主要AIツールのシステムプロンプトとモデル情報を集めたリポジトリ。"),
    "chatwoot/chatwoot": ("オープンソースのオムニチャネル顧客サポート基盤",
        "Intercom/Zendeskの代替を目指すOSSのライブチャット・メールサポート基盤。"),
}
for it in raw["sources"]["github"]:
    fn = it.get("full_name", "")
    if fn in gh_map:
        it["title_ja"], it["summary_ja"] = gh_map[fn]

# ---- Blogs (all) ----
blog_map = {
    "olmo-eval: An evaluation workbench for the model development loop":
        ("olmo-eval: モデル開発ループのための評価ワークベンチ",
         "AI2のオープンモデル開発で使う評価基盤を公開。モデル開発の評価サイクルを回しやすくする。"),
    "New OpenAI Academy courses for the next era of work":
        ("次世代の働き方に向けたOpenAI Academyの新講座",
         "OpenAIが提供する学習プログラムに、AI時代の働き方を学ぶ新コースを追加。"),
    "How Preply combines AI and human tutors to personalize learning":
        ("Preplyが人とAIの講師を組み合わせて学習を個別最適化",
         "語学学習PreplyがAIと人間講師を併用し個別最適な学習体験を作る事例。"),
    "Our new community investments in Virginia support local jobs and expand energy affordability":
        ("Googleがバージニアでデータセンター関連の地域投資",
         "Google DeepMind/Googleがバージニア州で雇用とエネルギー負担軽減を支える地域投資を発表。AI電力需要の文脈。"),
    "Supporting Europe’s work in ensuring a trustworthy AI ecosystem":
        ("信頼できるAIエコシステムに向けた欧州支援",
         "OpenAIが欧州の信頼できるAI構築の取り組みを支援する方針を表明。"),
    "BBVA puts AI at the core of banking with OpenAI":
        ("BBVAがOpenAIと組み銀行業務の中核にAIを据える",
         "スペインの大手銀行BBVAがOpenAIを使い、銀行業務の中核にAIを組み込む。"),
    "OpenAI to acquire Ona":
        ("OpenAIがOnaを買収へ",
         "OpenAIがクラウド開発環境/コーディングエージェントのOna(旧Gitpod系)を買収。コーディングAI陣取り合戦の一手。"),
    "How an astrophysicist uses Codex to help simulate black holes":
        ("天体物理学者がCodexでブラックホール計算を支援",
         "天体物理学者がCodexを使いブラックホールのシミュレーションコードを書く事例。"),
    "Profiling in PyTorch (Part 2): From nn.Linear to a Fused MLP":
        ("PyTorchプロファイリング(後編): nn.Linearから融合MLPへ",
         "nn.Linearを融合MLPへ最適化する過程をプロファイリングで追うHugging Faceの技術解説。"),
    "Access OpenAI models and Codex through your Oracle cloud commitment":
        ("OracleクラウドのコミットでOpenAIモデルとCodexを利用可能に",
         "Oracle Cloudの契約枠からOpenAIモデルやCodexを使えるようにする提携。"),
    "PRC-linked influence operations are targeting AI debates in the US":
        ("中国系の影響工作が米国のAI議論を標的に",
         "OpenAIが、中国に関連する影響工作が米国内のAI政策論議を標的にしていると報告。"),
    "From data to decisions: how LSEG is scaling trusted AI":
        ("データから意思決定へ: LSEGの信頼できるAIスケール",
         "ロンドン証券取引所グループ(LSEG)が信頼できるAIを業務規模で展開する事例。"),
    "Introducing North Mini Code: Cohere’s First Model For Developers":
        ("North Mini Code: Cohere初の開発者向けモデル",
         "Cohereが開発者向けの初コーディングモデルNorth Mini Codeを発表。"),
    "How engineers at Nextdoor use Codex to build without limits":
        ("NextdoorのエンジニアがCodexで開発を加速",
         "地域SNS NextdoorがCodexを使って開発スピードを上げる事例。"),
    "How an Agent Built a 3D Paris Gallery by Chaining Two Hugging Face Spaces":
        ("エージェントが2つのHF Spacesを連結し3Dパリ画廊を構築",
         "AIエージェントがHugging Faceの2つのSpaceを連鎖させ、3Dのパリの画廊を自動生成した事例。"),
    "Migrating Your GitHub CI to Hugging Face Jobs":
        ("GitHub CIをHugging Face Jobsへ移行する",
         "GitHub ActionsのCIをHugging Face Jobsへ移す方法を解説。GPUジョブを安価に回す狙い。"),
    "The Open Source Community is backing OpenEnv for Agentic RL":
        ("OSSコミュニティがエージェント的RLの標準OpenEnvを支持",
         "エージェント強化学習のための共通環境規格OpenEnvに、OSSコミュニティが集まりつつある。"),
}
for it in raw["sources"]["blogs"]:
    t = it.get("title", "")
    if t in blog_map:
        it["title_ja"], it["summary_ja"] = blog_map[t]

# ---- Highlights ----
highlights = [
    {
        "source": "Hacker News",
        "title": "US government directive forces Anthropic to suspend Fable 5 and Mythos 5",
        "title_ja": "米政府の指令でAnthropicがFable 5とMythos 5を停止",
        "url": "https://www.anthropic.com/news/fable-mythos-access",
        "hot_take_ja": "最先端AIモデルが一夜で政府指令により止まるという、これまで誰も本気で備えていなかった事態が現実になった。しかもWSJによれば引き金はAmazon CEOと米当局の会談。AI覇権が安全保障と巨大企業の政治力の交点で動き始めた象徴的な日だ。",
        "detail_ja": "AnthropicはHackerNewsで3000票超を集めた公式声明で、米政府の指令を受けて最上位モデルClaude Fable 5とMythos 5へのアクセスを停止したと発表した。ステータスページにも提供停止インシデントとして掲載され、開発者向けXアカウントからも告知が出た。WSJの続報によれば、この取り締まりの引き金になったのはAmazon CEOと米政府高官の協議だったとされ、商業的・地政学的な思惑が政策判断に影響した構図が浮かぶ。停止理由の詳細は限定的だが、フロンティアモデルが国家安全保障や輸出管理に類する枠組みで規制対象になりうることを実地で示した初の大型事例といえる。利用者にとっては、特定ベンダーの最先端モデルに依存することのサプライチェーンリスクが現実の運用停止として顕在化した。同日HN2位に『オープンソースAIは勝たねばならない』が、関連してGLM 5.2など中国系オープンモデルの話題も急浮上しており、クローズドモデルの政治的脆弱性への反動が起きている。AI企業間の競争が、性能だけでなくロビイングと規制を巡る政治戦に移行しつつあることを示す。今後は他社モデルへの波及や、停止の法的根拠・期間が焦点になる。",
        "detail_en": "In an official statement that topped Hacker News with over 3,000 points, Anthropic announced it had suspended access to its top models Claude Fable 5 and Mythos 5 in response to a US government directive. The suspension also appeared as an incident on Anthropic's status page and was announced via the developer-facing X account. A follow-up Wall Street Journal report says the crackdown was triggered by talks between Amazon's CEO and US officials, suggesting commercial and geopolitical interests shaped the policy move. Details on the rationale remain limited, but this is the first large-scale, real-world case showing that frontier models can become targets of national-security- or export-control-style regulation. For users, the supply-chain risk of depending on a single vendor's frontier model has materialized as an actual operational outage. The same day, 'Open source AI must win' hit #2 on HN, and Chinese open models like GLM 5.2 surged in attention — a clear backlash against the political fragility of closed models. It signals that competition among AI labs is shifting from pure capability toward a political battle over lobbying and regulation. Going forward, the focus will be whether this spreads to other vendors, and the legal basis and duration of the suspension.",
        "key_points_ja": [
            "Anthropicが米政府指令でFable 5/Mythos 5を停止",
            "HN首位3000票超、ステータスページにも掲載",
            "WSJ: 引き金はAmazon CEOと米当局の会談",
            "フロンティアモデルが規制対象になった初の大型事例",
            "単一ベンダー依存のサプライチェーンリスクが顕在化",
            "オープンモデル(GLM 5.2等)への注目が急上昇"
        ],
        "key_points_en": [
            "Anthropic suspends Fable 5/Mythos 5 on US directive",
            "Topped HN (3000+); also a status-page incident",
            "WSJ: triggered by Amazon CEO's talks with officials",
            "First major case of a frontier model being regulated",
            "Single-vendor supply-chain risk becomes real outage",
            "Surge of interest in open models like GLM 5.2"
        ],
    },
    {
        "source": "Hacker News",
        "title": "Open source AI must win",
        "title_ja": "オープンソースAIは勝たねばならない",
        "url": "https://opensourceaimustwin.com/?share=v2",
        "hot_take_ja": "フロンティアモデルが政府指令で一夜にして止まる——その同じ日に『オープンソースAIは勝たねばならない』がHN2位に駆け上がった。これは偶然ではない。クローズドモデルの政治的な単一障害点を見せつけられたコミュニティの、リアルタイムの反射神経だ。",
        "detail_ja": "『Open source AI must win』は、オープンソースAIの優位を訴えるキャンペーンサイトで、Fable 5/Mythos 5停止のニュースと同日にHN2位へ急浮上した。主張の核心は、最先端AIが特定企業のクローズドな管理下にあると、政府指令や商業的圧力で一瞬にして利用不能になり得るというリスクだ。実際この日、Anthropicの最上位モデルが停止し、その脆弱性が衆目に晒された。これに対し、重みが公開され誰でもホスト・改変できるオープンモデルは、単一ベンダーや単一政府の判断で消えることがない、という耐検閲性・継続性が改めて評価された。同日、中国の智譜AIのGLM 5.2がHN上位に入り、オープン/準オープンモデルの実力が伸びている現状も追い風になっている。一方で、オープンモデルにも安全性・悪用・資金持続性の課題はあり、『勝てばよい』という単純化への批判もある。それでも、AIインフラを公共財として分散管理すべきだという議論が、抽象論ではなく具体的な運用停止を背景に語られるようになった点が重要だ。今回の騒動は、モデルの選定基準に『政治的・規制的レジリエンス』という新しい軸を加えた。",
        "detail_en": "'Open source AI must win' is a campaign site arguing for the primacy of open-source AI, and it surged to #2 on Hacker News the same day as the Fable 5/Mythos 5 suspension. Its core argument: when frontier AI sits under a single company's closed control, it can become unavailable in an instant due to a government directive or commercial pressure. That very day, Anthropic's top models were suspended, putting exactly this fragility on public display. By contrast, open models — with published weights that anyone can host and modify — cannot be erased by the decision of a single vendor or government, renewing appreciation for their censorship-resistance and continuity. The same day, Zhipu AI's GLM 5.2 ranked highly on HN, and the rising capability of open and semi-open models adds tailwind. That said, open models face their own challenges around safety, misuse, and funding sustainability, and there is criticism of the simplistic 'just win' framing. Still, what matters is that the argument for treating AI infrastructure as a decentralized public good is now being made against the backdrop of a concrete outage, not in the abstract. The episode adds a new axis — political and regulatory resilience — to how people choose models.",
        "key_points_ja": [
            "Fable停止と同日にHN2位へ急浮上",
            "クローズドモデルの政治的単一障害点を問題視",
            "公開重みは単一の判断で消えない耐検閲性",
            "GLM 5.2などオープンモデルの実力向上が追い風",
            "安全性・資金持続性など反論も存在",
            "『規制レジリエンス』がモデル選定の新基準に"
        ],
        "key_points_en": [
            "Surged to #2 on HN the day Fable was suspended",
            "Frames closed models as a political single point of failure",
            "Open weights can't be erased by one actor's decision",
            "Rising open models (GLM 5.2) add momentum",
            "Counterpoints: safety, funding sustainability",
            "Adds 'regulatory resilience' as a model-choice criterion"
        ],
    },
    {
        "source": "Hacker News",
        "title": "Police officer investigated for using AI to 'create evidence' in multiple cases",
        "title_ja": "AIで『証拠を捏造』した疑いで警察官を捜査",
        "url": "https://news.sky.com/story/derbyshire-police-officer-investigated-for-using-ai-to-create-evidence-13553661",
        "hot_take_ja": "生成AIの悪用が、ついに刑事司法の根幹に届いた。英国の警察官が複数の事件でAIを使い『証拠』を作っていた疑いで捜査されている。冤罪を生みかねないこの種の事案は、ディープフェイク時代の証拠の信頼性そのものを揺るがす。",
        "detail_ja": "英ダービーシャー警察の警察官が、複数の事件で生成AIを使って証拠を捏造した疑いで捜査を受けているとSky Newsが報じた。詳細な手口は公表されていないが、AIで文書・画像・記録などそれらしい証拠物を生成していた可能性が指摘されている。これが事実なら、捜査機関の内部者がAIを悪用して司法手続きを歪めた重大な事案であり、過去の有罪判決の見直しや冤罪の懸念にも直結する。生成AIはテキスト・画像・音声を容易に本物らしく作れるため、証拠の真正性をどう担保するかが法廷の喫緊の課題になっている。具体的には、デジタル証拠の来歴(プロビナンス)管理、生成物検知、チェーン・オブ・カストディの厳格化などが求められる。今回の件は、AIの脅威が『誤情報の拡散』という社会全体の話だけでなく、個人の自由を左右する刑事手続きという最も重い局面に及び始めたことを示す。技術的な検知だけでなく、組織的な統制と説明責任が問われる。AIリテラシーと不正抑止の仕組みを、捜査・司法の現場にどう実装するかが今後の論点になる。",
        "detail_en": "Sky News reports that a Derbyshire police officer in the UK is under investigation for allegedly using generative AI to fabricate evidence across multiple cases. The exact method has not been disclosed, but it is suggested the officer may have generated plausible-looking evidentiary materials — documents, images, or records — with AI. If true, this is a serious case of an insider in law enforcement abusing AI to distort judicial proceedings, with direct implications for reviewing past convictions and the risk of wrongful conviction. Because generative AI can easily make text, images, and audio look authentic, ensuring the authenticity of evidence has become an urgent challenge for the courts. Concretely, this calls for digital-evidence provenance management, generated-content detection, and stricter chain-of-custody. The case shows that the AI threat is reaching beyond society-wide 'misinformation' into the heaviest arena of all — criminal procedure, where individual liberty is at stake. Beyond technical detection, organizational controls and accountability are being tested. How to implement AI literacy and fraud-deterrence mechanisms in investigative and judicial settings will be a key issue going forward.",
        "key_points_ja": [
            "英警察官が複数事件でAI証拠捏造の疑い",
            "事実なら過去判決の見直し・冤罪リスクに直結",
            "生成AIで証拠物を本物らしく作れる脅威",
            "証拠の来歴管理・生成物検知が急務",
            "誤情報拡散を超え刑事司法の中枢に到達",
            "技術検知だけでなく組織的統制と説明責任が必要"
        ],
        "key_points_en": [
            "UK officer suspected of fabricating AI evidence",
            "If true, risks wrongful convictions and case reviews",
            "GenAI can make evidence look authentic",
            "Urgent need for provenance and detection",
            "AI threat reaches the core of criminal justice",
            "Needs organizational control, not just detection"
        ],
    },
    {
        "source": "Hacker News",
        "title": "GLM 5.2 Is Out",
        "title_ja": "GLM 5.2 がリリース",
        "url": "https://twitter.com/jietang/status/2065784751345287314",
        "hot_take_ja": "西側のフロンティアモデルが政府指令で止まったまさにその日に、中国・智譜AIがGLM 5.2を出してきた。タイミングが全てを物語る。クローズド最先端が政治で揺らぐほど、オープン/中国系モデルの戦略的価値は上がる。",
        "detail_ja": "智譜AI(Zhipu AI)のGLM 5.2が、GLM創設者Jie Tang氏らのXポストでリリース告知された。GLMシリーズは中国発の大規模言語モデル群で、近年は性能・効率の両面で急速に追い上げ、オープン/準オープンの選択肢として世界的に存在感を増している。今回のリリースが注目される最大の理由はタイミングだ。同日、AnthropicのFable 5/Mythos 5が米政府指令で停止し、『オープンソースAIは勝たねばならない』がHN2位に浮上するなど、クローズドな西側フロンティアモデルの政治的脆弱性が露わになった。その文脈でGLM 5.2は、ベンダーや単一政府の判断に左右されにくい代替肢として相対的な魅力を増す。性能の詳細なベンチマークは精査が必要だが、コーディングや推論で上位西側モデルに迫る水準を主張するケースが続いており、価格・自前ホスト可能性の面でも実利が大きい。一方で、データ統制や輸出・利用規制、信頼性検証といった課題も残る。いずれにせよ、AIの競争軸が単なる性能から『供給の安定性・地政学的中立性』へと広がりつつある今、GLM 5.2の登場はオープン陣営の追い風として象徴的だ。",
        "detail_en": "Zhipu AI's GLM 5.2 was announced via an X post from GLM founder Jie Tang and colleagues. The GLM series is a family of large language models from China that has rapidly closed the gap in both capability and efficiency, growing into a globally significant open/semi-open option. The biggest reason this release drew attention is timing. The same day, Anthropic's Fable 5/Mythos 5 were suspended under a US government directive, and 'Open source AI must win' rose to #2 on HN — laying bare the political fragility of closed Western frontier models. In that context, GLM 5.2 gains relative appeal as an alternative less subject to the decisions of a single vendor or government. Detailed benchmarks warrant scrutiny, but recent GLM releases have claimed performance approaching top Western models on coding and reasoning, with practical advantages in price and self-hosting. At the same time, challenges remain around data governance, export/usage restrictions, and trust verification. Either way, as the axis of AI competition broadens from raw capability toward 'supply stability and geopolitical neutrality,' GLM 5.2's arrival is a symbolic tailwind for the open camp.",
        "key_points_ja": [
            "中国・智譜AIがGLM 5.2をリリース",
            "Fable停止と同日という象徴的タイミング",
            "性能・効率で西側上位モデルに迫ると主張",
            "自前ホスト可・価格面の実利が大きい",
            "供給安定性・地政学的中立性が新たな価値軸",
            "データ統制・信頼性検証など課題も残る"
        ],
        "key_points_en": [
            "Zhipu AI releases GLM 5.2",
            "Symbolic timing — same day as Fable suspension",
            "Claims capability nearing top Western models",
            "Self-hostable, with real cost advantages",
            "Supply stability and neutrality as new value axes",
            "Open challenges: governance and trust verification"
        ],
    },
    {
        "source": "arXiv",
        "title": "Before You Think: System 0, AI-Mediated Cognition and Cognitive Colonization",
        "title_ja": "Before You Think: System 0とAI媒介認知、そして『認知の植民地化』",
        "url": "https://arxiv.org/abs/2606.13658v1",
        "hot_take_ja": "私たちは『考える前』にすでにAIに考えさせられているのかもしれない。この論文は、AIが思考の前段(System 0)に入り込み、外部の利害を本人に気づかれぬまま自己の中に埋め込む『認知の植民地化』を警告する。検索とレコメンドに慣れた私たち全員に刺さる視点だ。",
        "detail_ja": "本論文は、AIが人間の認知に及ぼす影響を捉える3つの枠組み——Tri-System理論、Thinkframes、System 0——を比較検討する。著者は、前者2つが個人の推論や集団的な知の営みへの影響をよく捉える一方で、System 0が他の枠組みでは置き換えられない独自の位置を占めると論じる。System 0とは、人間のSystem 1(直感)/System 2(熟考)に先立ち、AIが情報の取捨選択や問題設定そのものを下支えする『思考の前段』を指す。ここで提示される中心概念が『認知の植民地化(cognitive colonization)』だ。これは、AIシステムが外部(企業や国家など)の利害を、ユーザー本人には知覚しにくい形で自己の認知構造の内側に埋め込んでしまう現象を指す。検索結果、レコメンド、要約、デフォルトの言い回しなどを通じて、何を考えるに値する問いとみなすかが静かに方向づけられる、という危惧だ。こうしたシステムはすでに広く展開されているため、目に見えにくいこの影響を理解することが急務だと著者は主張する。技術的というより思想・倫理的な論考だが、生成AIが日常の意思決定インフラになった現在、設計者にもユーザーにも重い問いを投げかける。透明性、選択肢の多様性、AIに依存しない思考の余地をどう確保するかが論点になる。",
        "detail_en": "This paper compares three frameworks for understanding AI's effect on human cognition — Tri-System Theory, Thinkframes, and System 0. The author argues that while the first two capture important dimensions of AI's influence on individual reasoning and collective epistemic practices, System 0 occupies a distinctive position the others cannot replicate. System 0 refers to a 'pre-thought' layer that precedes human System 1 (intuition) and System 2 (deliberation), where AI quietly underwrites the filtering of information and even the framing of problems. The central concept introduced is 'cognitive colonization': the phenomenon whereby AI systems embed external interests (corporate, governmental, etc.) within the architecture of the self in ways users find hard to perceive. Through search results, recommendations, summaries, and default phrasings, what counts as a question worth thinking about is subtly steered. Because such systems are already widely deployed, the author argues that understanding these invisible influences is urgent. More philosophical and ethical than technical, the work poses a heavy question now that generative AI has become everyday decision-making infrastructure. The key issues become transparency, diversity of options, and preserving room for thought that does not depend on AI.",
        "key_points_ja": [
            "AIが思考の前段『System 0』に入り込むと論じる",
            "Tri-System理論・Thinkframesと比較し独自性を主張",
            "中心概念は『認知の植民地化』",
            "外部の利害が自己の認知構造に埋め込まれる",
            "検索・推薦・要約が問いの立て方を静かに方向づける",
            "透明性とAI非依存の思考余地の確保が論点"
        ],
        "key_points_en": [
            "Argues AI enters a 'System 0' pre-thought layer",
            "Contrasts with Tri-System Theory and Thinkframes",
            "Introduces 'cognitive colonization'",
            "External interests embedded in the architecture of self",
            "Search/recs/summaries quietly frame our questions",
            "Calls for transparency and AI-independent thought"
        ],
    },
]

raw["highlights"] = highlights

# ---- stats ----
s = raw["sources"]
raw["stats"] = {
    "arxiv_count": len(s["arxiv"]),
    "hn_count": len(s["hn"]),
    "reddit_count": len(s["reddit"]),
    "github_count": len(s["github"]),
    "blogs_count": len(s["blogs"]),
    "total": sum(len(s[k]) for k in s),
}

out = ROOT / f"data/{DATE}.json"
out.write_text(json.dumps(raw, ensure_ascii=False, indent=2))
print("Wrote", out)
print("stats:", raw["stats"])
print("highlights:", len(raw["highlights"]))
