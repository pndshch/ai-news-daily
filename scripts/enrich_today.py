#!/usr/bin/env python3
"""Enrich raw-2026-06-06.json with Japanese/English summaries + highlights."""
import json
from pathlib import Path

DATE = "2026-06-06"
ROOT = Path(__file__).resolve().parent.parent
raw = json.load(open(ROOT / f"data/raw-{DATE}.json"))
src = raw["sources"]

def setja(items, idx, title_ja, summary_ja):
    if idx < len(items):
        items[idx]["title_ja"] = title_ja
        items[idx]["summary_ja"] = summary_ja

# ============ ARXIV (top listing identical to 2026-06-05, reuse translations) ============
arxiv = [
    ("TailLoR: 継続学習で主成分を保護するパラメータ効率的手法", "LoRA微調整時に重要な主成分(過去知識)を守りつつ新タスクを学ぶ継続学習法。破滅的忘却を抑えながら効率的に適応する。"),
    ("HANDOFF: 蒸留した相補的教師でヒューマノイド全身制御", "複数の専門教師方策を1つの生徒に蒸留し、ヒューマノイドの全身協調タスクをエージェント的に解く制御フレームワーク。"),
    ("Code2LoRA: ソフト進化に対応するコードLLM向けハイパーネット生成アダプタ", "コードベースの変化に応じてLoRAアダプタをハイパーネットワークで動的生成し、再学習なしにコードLLMを最新の仕様へ追従させる。"),
    ("TempoVLA: 速度を制御できるVision-Language-Action方策", "ロボット動作の実行速度を言語指示で調整できるVLA方策。同じタスクを速く/遅く実行する制御性を学習で獲得する。"),
    ("適応的な相手に対する繰り返しゲームでのリグレット最小化", "対戦相手が学習・適応してくる繰り返しゲームで、後悔(リグレット)を抑える新しいアルゴリズムを理論的に提案。"),
    ("PAR3D: 部位認識表現を持つ統一3D-MLLM", "シーン理解のため、物体を部位レベルで認識する表現を組み込んだ統一的な3Dマルチモーダル大規模言語モデル。"),
    ("操作誘導の段階的Human-to-AIテキスト変換ベンチマーク", "人間が書いた文章をAI的に書き換える過程を多粒度で評価するベンチマーク。AI生成テキスト検出研究の基盤となる。"),
    ("DNQ: 部分観測のnプレイヤーゲーム向けDeep Nash Q-Network", "観測が限られた多人数ゲームでナッシュ均衡を学習するQ学習手法。複雑な戦略ゲームへの強化学習適用を広げる。"),
    ("再帰なしで再帰型ネットワークを事前学習する", "RNNの学習を、時間方向に逐次なBPTTではなく「教師ありメモリ訓練(SMT)」で並列化。勾配消失を避け長距離依存を学べると主張。"),
    ("複雑度バランス型の拡散スプリッティング", "拡散モデルのサンプリングを計算複雑度の観点で均衡化し、生成品質と速度のトレードオフを改善する手法。"),
    ("想像して考える: ワールドシミュレータによる空間推論エージェント", "VLMが観測外のレイアウトを推論できるよう、ワールドシミュレータで未観測の視点を「想像」させ空間推論を強化する。"),
    ("RREDCoT: 推論モデル向けセグメント単位の報酬再配分", "推論の連鎖(CoT)をセグメント単位に分け、各段階に報酬を再配分することで推論モデルの学習を安定・効率化する。"),
    ("拡散言語モデルのための自己拡張検索", "拡散型の言語モデルが復号途中に捨てる低確信トークンを先読み信号として使い、検索を補強して生成を改善するRAG手法(SARDI)。"),
    ("MLEvolve: ML アルゴリズム自動発見の自己進化フレームワーク", "LLMエージェントが機械学習アルゴリズムを長期にわたり自己進化的に探索・発見する枠組み。分岐間の情報共有と階層制御で長期最適化を実現。"),
    ("PC Layer: LLM事前学習を改善する多項式重み前処理", "重み行列を多項式で前処理(プリコンディショニング)し、LLM事前学習の収束を速める新しい層。"),
    ("良い補間器はどれくらい豊富にあるか?", "過剰パラメータモデルが訓練データを完全に補間しつつ汎化する「良い補間器」の存在量を理論的に分析する。"),
    ("Goedel-Architect: ブループリント生成によるLean4形式証明の効率化", "定理証明を、定義と補題の依存グラフ(ブループリント)を先に生成・洗練してから埋めるエージェント的フレームワーク。Lean4で機能。"),
    ("You Only Index Once: 共有ルーティングのクロス層スパース注意", "長文推論の復号効率を上げるため、一度作ったインデックスを層をまたいで共有するスパース注意。速度と品質を両立。"),
    ("成人とLLMを科学者として比較: 能動的探索で得をするのは誰か", "人間とLLMに同じ探索課題を課し、能動的に実験して仮説を立てる能力を比較。LLMと人の科学的探索の差を測る。"),
    ("Benchmark Everything Everywhere All at Once", "多様なタスク・モダリティを一括で評価する統合ベンチマーク基盤の提案。"),
    ("方策更新なしのフローベース方策適応", "学習済み方策の重みを更新せず、フローベースの手法で新環境へ適応させる強化学習アプローチ。"),
    ("エージェントは自分を忌避するか: アクセス拒否信号への遵守を測る", "LLMエージェントが「このリソースへのアクセスは拒否」という帯域内信号にちゃんと従うかを測定。エージェントの安全性評価。"),
    ("AI-RAN向けパラメータ-KPI依存学習のためのイベント検出", "無線アクセスネットワーク(AI-RAN)で、設定パラメータと性能指標(KPI)の依存関係を学習するためのイベント検出手法。"),
    ("In-Context Multiple Instance Learning", "文脈内学習(in-context)の枠組みで複数インスタンス学習(MIL)を行う手法。ラベルが袋単位の弱教師問題に対応。"),
    ("足場か語彙か? ポパー的コード生成の二層・事前登録研究", "コード生成における足場(scaffold)と語彙の役割を、事前登録した統制実験で検証する方法論的研究。"),
]
for i, (t, s) in enumerate(arxiv):
    setja(src["arxiv"], i, t, s)

# ============ HN ============
hn = [
    ("S&P 500、SpaceXの早期採用を見送り——OpenAI・Anthropicも門前払い", "指数委員会が黒字要件などの除外を拒否し、未黒字のAI大手やSpaceXのS&P500入りを阻んだ。時価総額の熱狂と財務実態の乖離が指数の門前で可視化された。"),
    ("Claudeはrsyncのバグを増やしたのか?", "vibe codingでrsyncのバグが増えたという主張を統計的に再検証した分析。データ上は明確な悪化は確認できないと結論づける(関連トピックが既出)。"),
    ("pg_durable: MicrosoftがDB内耐久実行をOSS化", "PostgreSQL内で耐久的なワークフロー実行を可能にするMicrosoftのオープンソース。外部キューなしで障害復旧可能な処理を書ける。"),
    ("宇宙飛行士、空気漏れ修理で待避後にISS帰還を指示される", "ISSの空気漏れ対応に関する宇宙ニュース。AI以外の話題。"),
    ("Gemma 4 QATモデル: モバイル・ノートPC向けに圧縮を最適化", "量子化を意識して学習(QAT)したGemma 4を公開し、精度を保ったまま端末上で高効率に動かせるようにした。"),
    ("Ask HN: なぜHN民はこれほど反AIなのか?", "Hacker Newsコミュニティに広がるAIへの反発・疲労感を巡る議論スレッド。AI礼賛への反動が可視化されている。"),
    ("プログラマはClaudeのためには文書を書くが、同僚のためには書かない", "AIに読ませる目的だと急にコメントやドキュメントを整備し始める——AIが開発文化を変えてしまった皮肉な観察。"),
    ("AI抜きのHacker News", "HNからAI関連投稿を除外して表示する試み。AI話題の飽和への反動として注目を集めた。"),
    ("あなたのリビングのスマートTVはAIスクレイピング経済の一ノード", "スマートTVがアプリ内SDK経由で住宅用プロキシと化し、AI企業のウェブスクレイピングを中継している実態を暴いた調査。"),
    ("NVIDIA、Windows PC向けに強力なCPUシステムを提案", "NVIDIAがWindows PC向けの高性能CPUシステムを構想しているという話題。"),
    ("Ask HN: あなたのAI開発の技術スタック/ワークフローは?", "開発者たちが日々使うAI開発環境・ワークフローを共有し合うスレッド。"),
    ("Show HN: Lowfat – LLMトークンを91.8%削減するCLIフィルタ", "コマンド出力を間引いてLLMに渡すトークンを大幅削減する、プラグイン式のCLIフィルタ。"),
    ("Transformerは本質的に簡潔である", "Transformerが簡潔(succinct)な表現能力を本質的に備えることを理論的に示した研究。"),
    ("GitHub、チャット連携(Slack/Teams)の購読を誤って削除", "GitHubの障害でSlack/Teams連携の購読設定が誤って削除された件の報告。"),
    ("米軍はGPSを世界規模の「ナンバーズ・ステーション」に変えた", "GPS信号に隠された軍の暗号運用を解説。AI以外のセキュリティ話題。"),
    ("英国の警察、法廷向け供述でのAI利用停止を指示される", "イングランド・ウェールズの警察に、AIが生成した法廷文書の使用を止めるよう通達。誤情報(ハルシネーション)のリスクが理由。"),
    ("静かなナンバーズ・ステーション: 19年分のGPS暗号を解読", "GPSの暗号運用を長期にわたり解析した技術記事。"),
    ("米下院、州のAI規制を禁じる法案草案を公表", "州のAI開発規制を3年間凍結し連邦標準に一本化する超党派の討議草案(Great American AI Act)。AI規制の主導権を巡る攻防が本格化。"),
    ("Mantine-datatable等が侵害——所有者アカウント停止", "人気npmパッケージが供給網攻撃で侵害され、所有者アカウントが凍結された。OSS依存のリスクを改めて露呈。"),
    ("Microsoft、AIアシスタント『Scout』に依存させたい", "MicrosoftがAIアシスタントへのユーザー依存を狙っているとする批評記事。"),
]
for i, (t, s) in enumerate(hn):
    setja(src["hn"], i, t, s)

# ============ GITHUB ============
github = [
    ("superpowers: 21万★超のエージェント型スキルフレームワーク", "AIエージェントにスキルとソフトウェア開発手法を与えるフレームワーク。GitHubトレンド最上位で、エージェント開発の定番化が進む。"),
    ("Agent-Reach: AIエージェントにネット全体を見る「目」を与える", "Twitter/Reddit/YouTubeなどを読んで検索できるようにし、エージェントに広範なウェブ閲覧能力を付与するツール。"),
    ("CopilotKit: エージェント/生成UIのフロントエンド基盤", "React/Angular/モバイル/Slack等にAIエージェントのUIを組み込むためのフロントエンドスタック。"),
    ("PaddleOCR: PDF・画像を構造化データに変換するOCR", "軽量で強力なOCRエンジン。文書をAI向けの構造化データに変換でき、根強い人気を保つ。"),
    ("last30days-skill: 任意トピックを横断調査するエージェントスキル", "Reddit/X/YouTube/HN/Polymarket等を横断し、直近30日の話題を調べるAIエージェントスキル。"),
    ("mempalace: ベンチ最強を謳うOSSのAIメモリシステム", "LLMエージェント向けの長期記憶を実現するオープンソース。ベンチマークで最良と主張し、無料で提供。"),
    ("VibeVoice: オープンソースの最先端音声AI", "高品質な音声合成・音声AIをオープンソースで提供するプロジェクト。"),
    ("OpenAI Plugins", "OpenAIのプラグイン関連リポジトリ。"),
    ("career-ops: Claude Code上に作る求職自動化システム", "14のスキルモード、Goダッシュボード、PDF生成を備えたAI求職支援システム。"),
    ("Trivy: コンテナ・コード等の脆弱性スキャナ", "コンテナ/K8s/コードの脆弱性・設定ミス・秘密情報・SBOMを検出する定番セキュリティツール。"),
    ("Whisper: 大規模弱教師による頑健な音声認識", "OpenAIの音声認識モデル。多言語で高精度な文字起こしを実現する定番OSS。"),
    ("Personal AI Infrastructure: 個人の能力を拡張するエージェント基盤", "人間の能力を増幅するための自分専用エージェントAIインフラのテンプレート。"),
    ("mxc: 方針駆動の階層的な隔離・封じ込め", "ポリシーに基づき多層的にプロセスを隔離・封じ込めるツール。"),
]
for i, (t, s) in enumerate(github):
    setja(src["github"], i, t, s)

# ============ BLOGS ============
blogs = [
    ("5つのラボ・5つの知性: 小型モデルで金融ドラマを作る", "複数の小型モデルを組み合わせ、金融シナリオのドラマを生成したハッカソンの記録。"),
    ("2026年5月にGoogleが発表したAIニュースまとめ", "Google DeepMindの5月の主要発表を振り返るまとめ記事。"),
    ("Nemotron 3.5 コンテンツ安全性: カスタム可能なマルチモーダル安全性", "NVIDIAの、企業向けにカスタマイズ可能なマルチモーダル安全性(コンテンツモデレーション)モデル。"),
    ("EVA-Bench Data 2.0: 3ドメイン・121ツール・213シナリオ", "エージェント評価用ベンチマークの拡張版。多数のツールと現実的なシナリオを収録。"),
    ("Endava、AIエージェント中心にソフト開発を再設計", "受託開発大手Endavaが、AIエージェントを軸に開発プロセスを作り替えた事例。"),
    ("Dreaming: ChatGPTのより賢いメモリ", "ChatGPTがアイドル時に過去対話を整理・統合し記憶を改善する仕組み(既出トピック)。"),
    ("知能の時代のバイオ防衛", "OpenAIによる、AI時代の生物学的脅威への防衛戦略(関連トピックが既出)。"),
    ("hf CLIをエージェント最適化で再設計", "Hugging Face Hubを扱うCLIを、AIエージェントが使いやすい形に設計し直した話。"),
    ("GPT-Rosalindに新機能を追加", "OpenAIのライフサイエンス向けモデルGPT-Rosalindの機能拡張(既出トピック)。"),
    ("Google検索で古着・ヴィンテージ探しを強化する5つの方法", "AI検索機能を使った古着・ヴィンテージショッピングの活用術。"),
    ("チャットボットを超えたDPO", "直接選好最適化(DPO)をチャット以外の領域に応用する解説記事。"),
    ("WasmerがCodexでエッジ向けNode.jsランタイムを構築", "OpenAI Codexを使い、エッジで動くNode.js互換ランタイムを開発した事例。"),
    ("フロンティアAIの民主的ガバナンス青写真", "OpenAIが示す、最先端AIを民主的に統治するための枠組みの提案。"),
    ("OpenAIの公共政策アジェンダ", "OpenAIが掲げる政策面の方針・提言をまとめたもの。"),
    ("Reachy MiniにMCPツールを追加", "卓上ロボットReachy MiniにMCP経由でツールを使わせる方法の紹介。"),
    ("Holo3.1: 高速・ローカルなコンピュータ操作エージェント", "ローカルで動く高速なGUI操作(コンピュータ操作)エージェント(既出トピック)。"),
    ("保険大手Travelers、OpenAIで保険金請求をAI化し全米展開", "保険会社Travelersが請求処理にAIを導入し、全国展開した事例。"),
    ("あらゆる役割・ツール・ワークフローのためのCodex", "OpenAI Codexを職種横断で使えるよう拡張した発表。"),
    ("グローバルリーダーシップで若者の安全と機会を前進", "OpenAIの若年層保護に関する取り組みの紹介。"),
    ("GeminiでGoogle I/O 2026を作った方法", "Geminiを活用してI/Oイベントの制作を行った舞台裏。"),
    ("Mellum2: JetBrainsの12B MoEコーディングモデル", "JetBrainsが公開した、コード補完特化の12Bパラメータ混合専門家(MoE)モデル。"),
    ("LLMを超えて: 企業AI普及はエージェントロジック次第", "IBM研究による、スケーラブルな企業AI導入にはエージェントの論理設計が鍵という論考。"),
]
for i, (t, s) in enumerate(blogs):
    setja(src["blogs"], i, t, s)

# ============ HIGHLIGHTS ============
highlights = [
    {
        "source": "Hacker News",
        "title": "S&P 500 rejects SpaceX, also blocking entry for OpenAI and Anthropic",
        "title_ja": "S&P 500、SpaceXの早期採用を拒否——OpenAI・Anthropicも入れず",
        "url": "https://arstechnica.com/tech-policy/2026/06/sp-500-blocks-fast-spacex-entry-wont-waive-rule-for-unprofitable-ai-firms/",
        "hot_take_ja": "時価総額では誰もが認めるAIの主役なのに、S&P 500には入れない。理由は単純で、四半期GAAP黒字という条件を満たさないから。指数委員会は「時価総額の大きさだけを理由に例外を認めるべきではない」と言い切った。期待の熱狂と財務の冷たさのギャップが、指数の門前ではっきり可視化された一件だ。",
        "detail_ja": "S&P Dow Jones Indicesの指数委員会が、SpaceX・OpenAI・Anthropicの3社を念頭に検討していた採用ルールの緩和を6月4日に見送った。委員会は、①上場後12カ月の「熟成(seasoning)」期間、②浮動株比率(public float)10%以上、③直近四半期と過去4四半期合計でのGAAP黒字、という3要件の例外適用を検討したが、最終的に「財務的健全性・熟成・浮動株要件の例外を、時価総額の大きさだけを根拠に認めるべきではない」と結論づけた。SpaceXは2025年に約49億ドルの赤字を計上しており、黒字要件を満たさないため早期採用の道は閉ざされた。Bloomberg Intelligenceの試算では、S&P500入りが実現すればSpaceXに約140億ドル、OpenAIに80億ドル超、Anthropicに46億ドルのパッシブ買いが発生するとされ、それが宙に浮いた格好だ。背景には、世界で7.5兆ドル規模のパッシブ資金がこの指数に連動しており、組入れ＝自動的な巨額買いを意味するという構造がある。一方でNasdaqやFTSE Russellは既に規則を調整しており、SpaceXは他指数経由なら入れる可能性がある。注意点として、これらの企業は多くがまだ非上場・赤字であり、今回の決定は「将来IPOしても自動では入れない」という規律の再確認という側面が強い。AIへの市場の熱狂と、伝統的な指数が課す財務規律との緊張関係を象徴する出来事と言える。",
        "detail_en": "On June 4, the S&P Dow Jones Indices committee declined to relax its index-inclusion rules that had been under consideration with SpaceX, OpenAI, and Anthropic in mind. The committee had weighed waiving three separate requirements: the 12-month post-IPO 'seasoning' period, the 10% minimum public float, and the profitability test (positive GAAP earnings in the most recent quarter and summed over the trailing four quarters). It ultimately concluded that 'exceptions to the financial viability, seasoning, and IWF requirements should not be granted solely based on market capitalization.' SpaceX posted a roughly $4.94 billion loss in 2025, so it fails the profitability bar and gets no fast track. Bloomberg Intelligence estimated S&P 500 entry would trigger about $14 billion of passive buying for SpaceX, over $8 billion for OpenAI, and $4.6 billion for Anthropic — flows that are now on hold. The stakes are high because roughly $7.5 trillion in passive money tracks the index, so inclusion effectively means automatic large-scale buying. Meanwhile Nasdaq and FTSE Russell have already adjusted their rules, leaving a path for SpaceX into other indices. A caveat: most of these firms remain private and unprofitable, so the decision is largely a reaffirmation that even post-IPO they would not get automatic entry. It crystallizes the tension between the market's enthusiasm for AI and the financial discipline that traditional indices still enforce.",
        "key_points_ja": [
            "6/4にS&Pが採用ルール緩和を見送り",
            "熟成・浮動株・GAAP黒字の3要件は維持",
            "「時価総額だけで例外は認めない」と明言",
            "SpaceXは2025年に約49億ドルの赤字",
            "実現時はSpaceXに約140億ドルのパッシブ買い試算",
            "NasdaqやFTSEは既に規則を調整済み",
        ],
        "key_points_en": [
            "S&P declined to relax inclusion rules on June 4",
            "Seasoning, float, and GAAP-profit rules all kept",
            "'No exceptions based on market cap alone'",
            "SpaceX posted a ~$4.94B loss in 2025",
            "Entry would have meant ~$14B passive buying for SpaceX",
            "Nasdaq and FTSE Russell already eased their rules",
        ],
    },
    {
        "source": "Hacker News",
        "title": "US House lawmakers release draft bill to prohibit state AI rules",
        "title_ja": "米下院、州のAI規制を3年凍結する超党派法案草案を公表",
        "url": "https://www.insurancejournal.com/news/national/2026/06/05/872609.htm",
        "hot_take_ja": "州ごとにバラバラなAI規制を「3年間凍結して連邦に一本化する」——そんな269ページの超党派草案が出た。引き換えに大手AI開発者には半年ごとの第三者監査を課す、いわば「規制の集権化と引き換えの透明性」ディール。だが労組や消費者団体は数時間で猛反発、業界団体は歓迎と、賛否がきれいに割れた。AI規制の主導権を州と連邦どちらが握るかの天王山だ。",
        "detail_ja": "下院のJay Obernolte議員(共和・カリフォルニア)とLori Trahan議員(民主・マサチューセッツ)が6月4日、269ページに及ぶ超党派のAI規制討議草案「Great American AI Act」を公表した。最大の柱は、AIモデルの「開発」を直接規制する州法を3年間先取り(preemption)して凍結し、連邦標準に一本化する点だ。重要な線引きとして、この凍結はモデルの「利用・配備(use/deployment)」を規制する州法には及ばず、既存の消費者保護法・公民権法・プライバシー法もそのまま残る。一方で、カリフォルニア・ニューヨーク・イリノイが先行して定めたAI開発の透明性義務などは実質的に凍結・上書きされる見込みだ。代償として、大規模AI開発者には半年ごとの第三者監査が義務付けられ、フロンティアラボにはモデルの一定の開示も求められる。法案は公表から数時間で労働組合・消費者擁護団体・下院民主党の委員会から強い反対に遭った一方、主要テック企業を代表するITI(Information Technology Industry Council)は歓迎を表明した。これは2025年に予算法案へ盛り込まれて削除された「10年間のモラトリアム」案の再来であり、トランプ政権のAI大統領令(州法を標的に連邦標準を志向)とも軌を一にする。注意点として現時点はあくまで「討議草案」であり、3年のサンセット条項付き。州の規制権限と連邦の統一基準のどちらを優先するかという、AIガバナンスの根本的な綱引きが本格化したことを示す。",
        "detail_en": "On June 4, Reps. Jay Obernolte (R-CA) and Lori Trahan (D-MA) released a 269-page bipartisan discussion draft, the 'Great American AI Act.' Its centerpiece is a three-year federal preemption that would freeze state laws 'specifically regulating the development' of AI models, consolidating authority at the federal level. Crucially, the preemption would not reach state laws governing the use or deployment of AI, and existing consumer-protection, civil-rights, and privacy laws would remain intact — but AI-development transparency laws already enacted in California, New York, and Illinois would effectively be frozen or superseded. In exchange, large AI developers would face semi-annual third-party audits, and frontier labs would be pushed to open up their models to a degree. Within hours the draft drew strong opposition from labor unions, consumer advocates, and a formal House Democratic commission, while the Information Technology Industry Council, representing major tech firms, praised it. The proposal echoes the '10-year moratorium' that was inserted into a 2025 budget bill and then stripped out, and aligns with the Trump administration's AI executive order that targets state laws in favor of a uniform federal standard. Note that this is still only a discussion draft and carries a three-year sunset. It marks the start of a serious tug-of-war over whether state regulatory power or a single federal standard should govern AI.",
        "key_points_ja": [
            "超党派の269ページ草案「Great American AI Act」",
            "州のAI『開発』規制を3年間先取り・凍結",
            "『利用・配備』規制や既存の消費者保護法は対象外",
            "代償に大手開発者へ半年ごとの第三者監査",
            "CA・NY・ILの透明性法は実質凍結の見込み",
            "労組・消費者団体は反発、業界団体ITIは歓迎",
        ],
        "key_points_en": [
            "Bipartisan 269-page 'Great American AI Act' draft",
            "3-year preemption of state AI-development rules",
            "Use/deployment and existing laws left untouched",
            "Trade-off: semi-annual audits of big developers",
            "CA, NY, IL transparency laws to be frozen",
            "Unions oppose; tech group ITI applauds",
        ],
    },
    {
        "source": "Hacker News",
        "title": "The Smart TV in Your Living Room Is a Node in the AI Scraping Economy",
        "title_ja": "リビングのスマートTVはAIスクレイピング経済の一ノードだった",
        "url": "https://blog.includesecurity.com/2026/06/the-smart-tv-in-your-livingroom-is-a-node-in-the-aiscraping-economy/",
        "hot_take_ja": "あなたのスマートTVが、夜中にこっそり他人のウェブスクレイピングを代行しているかもしれない。アプリに埋め込まれたBright DataのSDKが、家庭のネット回線を「住宅用プロキシ」の出口ノードに変え、AI企業のボット対策回避に貸し出す仕組みだ。常時給電・帯域ほぼ無制限・誰も見ていない——TVは中継機として“理想の被害者”だった。",
        "detail_ja": "セキュリティ企業IncludeSecurityの調査で、スマートTVがAI向けのウェブスクレイピングを中継する「住宅用プロキシ(residential proxy)」のノードとして使われている実態が明らかになった。仕組みの核は、提携アプリに組み込まれたBright DataのSDKだ。インストールされるとSDKはBright Dataのインフラへ常時WebSocket接続を張り、同社はスクレイピングの仕事をユーザー家庭のネット回線経由で送り出す。Bright Dataは「4億超の家庭用IP」へのアクセスを商品化し、CloudflareやDataDomeのボット対策を回避したいAI企業に販売する。提携先にはCTVゲーム大手PlayWorks Digital(約2.5億世帯)、125以上のTVブランドを抱えるCloudTV、Viber/Rakuten(2.5〜8.2億ユーザー)などが挙がる。スマートTVが狙われるのは、常時給電で24時間スタンバイ、帯域が実質無制限、企業の監視がほぼなく、ユーザーの注意も向かないという「理想的な条件」が揃うからだ。調査では既定でも月500MB、設定によっては月200GBもの通信を中継しうるという。SDKは検査回避のためVPNを迂回して物理インターフェース(en0/pdp_ip0)に直接バインドし、URLSessionフックを避けてCFNetworkを使うなど、マルウェアのC2(指令)通信に近い手口も確認された。同意ダイアログには「device resourcesをoccasionallyに使う」とあるが、実際の設定は大量通信を許す内容で、通信にメッセージ署名やHMAC、クライアント証明書、デバイス認証が一切なく、バッテリー・CPU・帯域・画面状態などのテレメトリを第三者サーバへ常時送り続ける点も問題視されている。",
        "detail_en": "An investigation by security firm IncludeSecurity reveals that smart TVs are being used as nodes in a 'residential proxy' network that relays web-scraping traffic for AI companies. The mechanism centers on Bright Data's SDK, embedded in partner apps. Once installed, the SDK opens a persistent WebSocket connection to Bright Data's infrastructure, letting the company route scraping jobs through users' home internet connections. Bright Data monetizes access to '400M+ home IP addresses,' selling it to AI firms that need residential IPs to bypass anti-bot defenses from services like Cloudflare and DataDome. Named partners include PlayWorks Digital (400+ CTV game titles, ~250M homes), CloudTV (125+ TV brands), and Viber/Rakuten (250M–820M users). Connected TVs are ideal because they are always plugged in, run 24/7 in standby, have effectively unlimited bandwidth, receive minimal corporate oversight, and get little user attention. The research found a device could relay 500 MB monthly by default — or up to 200 GB in some configurations. To evade inspection, the SDK bypasses VPNs by binding to physical interfaces (en0/pdp_ip0) instead of system routes, and avoids URLSession hooks via CFNetwork — tactics reminiscent of malware command-and-control. Consent dialogs say Bright Data will 'occasionally' use device resources, yet configurations permit far heavier traffic, the protocol has no message signing, HMAC, client certificates, or device attestation, and the device continuously streams telemetry (battery, CPU, bandwidth, screen state) to third-party servers.",
        "key_points_ja": [
            "スマートTVが住宅用プロキシの出口ノードに",
            "アプリ内のBright Data製SDKが常時接続を確立",
            "「4億超の家庭IP」をAI企業へ販売しボット対策回避",
            "常時給電・帯域無制限のTVが狙われやすい",
            "既定で月500MB、設定次第で月200GBを中継",
            "VPN迂回・署名なし通信などC2類似の手口",
        ],
        "key_points_en": [
            "Smart TVs act as residential-proxy exit nodes",
            "Bright Data SDK in apps keeps a persistent link",
            "Sells '400M+ home IPs' to AI scrapers to dodge bot defenses",
            "Always-on, high-bandwidth TVs are ideal targets",
            "Relays 500MB/mo by default, up to 200GB configured",
            "VPN bypass and unsigned traffic mimic malware C2",
        ],
    },
    {
        "source": "arXiv",
        "title": "Pretraining Recurrent Networks without Recurrence",
        "title_ja": "再帰なしで再帰型ネットワークを事前学習する(SMT)",
        "url": "https://arxiv.org/abs/2606.06494",
        "hot_take_ja": "RNN学習の宿敵は「時間方向に逐次でしか勾配を流せない」BPTTだった。この論文は、RNNの学習を“1ステップのメモリ遷移を当てる教師あり学習”に置き換えることで、再帰的な勾配伝播そのものを消し去る。並列化でき勾配消失も避けられるなら、RNN/状態空間モデル復権の追い風になりうる。",
        "detail_ja": "RNN(再帰型ニューラルネット)の学習は、長い系列にまたがって「どの計算がどれだけ結果に寄与したか(credit assignment)」を割り当てる必要がある。標準手法のBPTT(通時的誤差逆伝播)はこれを苦手とする:時間方向に逐次的なので並列化できず、勾配が消失・爆発しやすく、長距離の依存関係を学びにくい。本研究が提案するSupervised Memory Training(SMT)は、再帰的な勾配伝播そのものを回避する。鍵は、RNNの学習を「1ステップのメモリ遷移ラベル (m_t, x_{t+1}) → m_{t+1} を当てる教師あり学習」へと還元する点だ。このメモリラベルは、予測的状態(predictive state)目的でTransformerベースのエンコーダを先に訓練して取得する。いったんラベルが手に入れば、各時刻の更新が独立した教師あり問題になるため、時間方向に並列学習でき、長系列でも勾配消失の問題を避けられる、と著者は主張する。これはRNNやSSM(状態空間モデル)が長文・長系列モデリングで再び注目される流れの中で意義が大きい。注意点として、SMTは良いメモリラベルを作るエンコーダの質に依存し、Transformerの事前訓練という別コストを要する。それでも、逐次性というRNN学習最大のボトルネックを設計レベルで外そうとする発想は新規性が高く、効率的な系列モデルの学習法に新たな選択肢を示す。",
        "detail_en": "Training recurrent neural networks (RNNs) requires assigning credit across long sequences of computations. The standard approach, backpropagation through time (BPTT), handles this poorly: it is sequential in time (limiting parallelism) and suffers from vanishing or exploding gradients, making long-range associations hard to learn. This paper proposes Supervised Memory Training (SMT), which sidesteps recurrent credit propagation entirely. The key idea is to reduce RNN training to supervised learning on one-step memory-transition labels of the form (m_t, x_{t+1}) → m_{t+1}. These memory labels are obtained by first training a Transformer-based encoder on a predictive-state objective. Once the labels exist, each timestep's update becomes an independent supervised problem, so training can be parallelized across time and avoids the vanishing-gradient issue even on long sequences, the authors argue. This matters amid renewed interest in RNNs and state-space models (SSMs) for long-context and long-sequence modeling. A caveat: SMT depends on the quality of the encoder that produces the memory labels and incurs the separate cost of pretraining that Transformer. Still, the idea of removing sequentiality — the biggest bottleneck in RNN training — at the design level is genuinely novel and offers a new option for efficiently training sequence models.",
        "key_points_ja": [
            "BPTTは逐次的で並列化できず勾配も不安定",
            "SMTは1ステップのメモリ遷移を当てる教師あり学習に還元",
            "メモリラベルはTransformerエンコーダで生成",
            "各時刻が独立化し時間方向に並列学習が可能",
            "勾配消失を避け長距離依存を学べると主張",
            "RNN/SSM復権の流れに新たな学習法を提示",
        ],
        "key_points_en": [
            "BPTT is sequential, non-parallel, gradient-unstable",
            "SMT reduces training to one-step memory-transition labels",
            "Memory labels produced by a Transformer encoder",
            "Each timestep becomes independent, enabling parallel training",
            "Claims to avoid vanishing gradients on long sequences",
            "A fresh training option amid the RNN/SSM revival",
        ],
    },
    {
        "source": "Hacker News",
        "title": "Programmers will document for Claude, but not for each other",
        "title_ja": "プログラマはClaudeのためには文書を書くが、同僚のためには書かない",
        "url": "https://blog.plover.com/2026/03/09/#documentation-wins-2",
        "hot_take_ja": "「ドキュメントを書け」と何年言われても動かなかった開発者が、AIに読ませるためなら嬉々としてREADMEや設計メモを整え始める。読み手が人間からAIに変わった途端、長年の文化的課題があっさり溶けた——という皮肉。AIが“最良のドキュメント読者”になることで、結果的に人間にとっての文書も充実するなら、それは怪我の功名かもしれない。",
        "detail_ja": "ベテラン開発者Mark Dominus(blog.plover.com)が綴った、AI時代のソフトウェア文化に関する鋭い観察記事で、Hacker Newsで大きな共感を呼んだ。要点はタイトル通り、「プログラマは同僚のためにはドキュメントを書かないのに、Claudeのためなら書く」という現象だ。コードのコメント、README、設計上の前提、命名規約といった文書化は、ソフト工学で何十年も『重要だが後回しにされる』典型だった。レビューや教育で繰り返し促されても定着しなかったのに、AIコーディング支援が普及すると状況が一変する。AIに正確なコードを書かせ、文脈を理解させるには、明示的な仕様・制約・意図の記述が効くと開発者が体感し、自発的に文書を整えるようになった、というわけだ。背景には、AIが人間の同僚と違って「行間を読む」「過去の経緯を覚えている」「直接質問できる」といった暗黙の補完をしてくれないため、書き手が文脈を言語化せざるを得ない事情がある。皮肉なのは、長年の啓蒙より、AIという新しい『読者』の登場の方が行動変容に効いた点だ。含意として、結果的に書かれた文書は人間にとっても有益なので、AIが副次的にコードベースの可読性・保守性を底上げする可能性がある。一方で、文書がAI向けに最適化されすぎ、人間にとっての読みやすさやニュアンスが失われるリスクや、「AIが読むから人間は読まなくていい」という新たな怠慢を生む懸念も指摘できる。",
        "detail_en": "A sharp observation on AI-era software culture by veteran developer Mark Dominus (blog.plover.com) that struck a chord on Hacker News. The thesis is in the title: programmers won't write documentation for their colleagues, but they will write it for Claude. Documenting code — comments, READMEs, design assumptions, naming conventions — has for decades been the classic 'important but perpetually deferred' task in software engineering. Repeated nudging in reviews and onboarding never made it stick, yet the spread of AI coding assistants changed things overnight. Developers found that to get an AI to write correct code and understand context, explicit specs, constraints, and statements of intent really help — so they began voluntarily fleshing out documentation. Part of the reason is that, unlike a human colleague, an AI won't 'read between the lines,' remember historical context, or be asked a quick follow-up, which forces the author to put context into words. The irony is that a new kind of 'reader' — the AI — drove behavior change more effectively than years of advocacy. The implication is upbeat: the docs that result are also useful to humans, so AI may incidentally raise a codebase's readability and maintainability. On the flip side, there's a risk that docs become over-optimized for AI at the expense of human nuance, and a worry about a new kind of laziness — 'the AI reads it, so humans don't have to.'",
        "key_points_ja": [
            "AIに読ませる目的だと開発者が自発的に文書化",
            "長年定着しなかった文書化が一気に進む皮肉",
            "AIは行間を読まないので意図の明文化が必要",
            "副産物として人間向けの可読性も向上しうる",
            "AI最適化で人間向けのニュアンス喪失のリスク",
            "『AIが読むから不要』という新たな怠慢の懸念",
        ],
        "key_points_en": [
            "Devs document voluntarily when the reader is AI",
            "A long-unsolved cultural problem suddenly shifts",
            "AI won't read between lines, forcing explicit intent",
            "Side effect: human readability may improve too",
            "Risk of docs over-optimized for AI, losing nuance",
            "New laziness worry: 'the AI reads it, so we needn't'",
        ],
    },
]

raw["highlights"] = highlights

# ============ stats ============
raw["stats"] = {f"{s}_count": len(src[s]) for s in src}
raw["stats"]["total"] = sum(len(v) for v in src.values())
raw["stats"]["highlights"] = len(highlights)

out = ROOT / f"data/{DATE}.json"
json.dump(raw, open(out, "w"), ensure_ascii=False, indent=1)
print(f"Wrote {out}")
print("highlights:", len(highlights), "| stats:", raw["stats"])
