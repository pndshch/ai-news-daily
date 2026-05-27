#!/usr/bin/env python3
"""Enrich raw-2026-05-27.json with Japanese summaries and highlights."""
import json
from pathlib import Path

DATE = "2026-05-27"
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / f"raw-{DATE}.json"
OUT = ROOT / "data" / f"{DATE}.json"

with open(RAW) as f:
    d = json.load(f)

# -------- arXiv --------
arxiv_map = {
    "Algorithmic Monocultures in Hiring": (
        "アルゴリズム単一栽培（モノカルチャー）が採用に及ぼす影響",
        "ベンダー数社の採用スクリーニングAIが業界に行き渡ることで、特定の応募者・人種グループだけが体系的に通過/落選しやすくなる『モノカルチャー効果』を実証分析した論文。"
    ),
    "G3T Up! Gravity Aligned Coordinate Frames Simplify Pointmap Processing": (
        "重力整列座標系でPointmap処理を簡素化",
        "VGGTなど近年の3D再構成はカメラ中心座標で点群を予測するが、重力方向に整列した座標フレームに変えるだけで複数下流タスクが改善することを示した研究。"
    ),
    "SpatialBench: Is Your Spatial Foundation Model an All-Round Player?": (
        "SpatialBench：空間基盤モデルは『万能選手』か？",
        "空間基盤モデルが標準データでは強くても、視点・シーン・タスクが分布外になると一気に壊れることを検証する総合ベンチマーク。"
    ),
    "MUSE-Autoskill: Self-Evolving Agents via Skill Creation, Memory, Management, and Evaluation": (
        "MUSE-Autoskill：スキルを自分で作って育てるエージェント",
        "LLMエージェントの『スキル』を静的アーティファクトとして扱うのをやめ、生成・記憶・管理・評価のループに乗せて自己進化させるフレームワーク。"
    ),
    "LocateAnything: Fast and High-Quality Vision-Language Grounding with Parallel Box Decoding": (
        "LocateAnything：並列デコードで高速かつ高品質な視覚-言語グラウンディング",
        "VLMの座標トークン逐次生成方式を、ボックスを並列にデコードする方式に置き換えて高速化と精度向上を両立した手法。"
    ),
    "Natural Language Query to Configuration for Retrieval Agents": (
        "自然言語クエリから検索エージェント設定を自動生成",
        "RAGエージェントのLLM選択・retriever・hop数・統合戦略といった設定空間を、自然言語クエリから自動最適化する仕組み。"
    ),
    "GENESIS: Harnessing AI Agents for Autonomous 6G RAN Synthesis, Research, and Testing": (
        "GENESIS：6G無線網のR&Dを自律エージェントが回す",
        "通信標準の検討〜実装〜試験まで人手で数ヶ月かかる6G RANのR&Dプロセスを、AIエージェント協調で自律化する野心的システム。"
    ),
    "MobileMoE: Scaling On-Device Mixture of Experts": (
        "MobileMoE：オンデバイスでMoEをスケールさせる",
        "100B級で標準化されたMoEを、1B未満のオンデバイス領域でも使えるよう設計を見直した研究。"
    ),
    "Alignment Tampering: How Reinforcement Learning from Human Feedback Is Exploited to Optimize Misaligned Biases": (
        "Alignment Tampering：RLHFを悪用してバイアスを温存させる攻撃",
        "RLHFパイプラインに細工することで、表面上はアラインされているように見えて実は偏った挙動を最適化できる新しい脆弱性を実証した研究。"
    ),
    "Guiding LLM Post-training Data Engineering with Model Internals from Sparse Autoencoders": (
        "SAE経由のモデル内部信号で事後学習データを選別する",
        "外部メトリクスではなくスパースオートエンコーダで取り出した内部表現を使い、ポスト学習データを賢く選ぶデータエンジニアリング手法。"
    ),
    "From Scores to Gibbs Correctors: Accelerating Uniform-Rate Discrete Diffusion Models": (
        "Gibbsコレクタで離散拡散モデルを高速化",
        "離散拡散モデルの生成にかかるステップ数を、Gibbsサンプリング的補正項で大幅削減する手法。"
    ),
    "Feedforward 3D Editing Learns from Semantic-Part Transformation": (
        "意味的パーツ変形から学ぶフィードフォワード3D編集",
        "画像編集の大規模フィードフォワード化に倣い、3D編集を意味パーツ変形タスクとして大規模学習可能にする提案。"
    ),
    "When Eyes Betray AI: Social Gaze Consistency as a Semantic Cue for AI-Generated Image Detection": (
        "視線でAIを見破る——社会的視線の整合性を使ったAI生成検出",
        "低レベルのアーチファクトでは生成モデルとほぼ見分けが付かなくなった画像でも、人物の社会的視線の整合性がまだ崩れていることを利用したAI画像検出手法。"
    ),
    "MATCHA: Matching Text via Contrastive Semantic Alignment": (
        "MATCHA：対照学習で意味整合を測るLLM評価",
        "ROUGEや埋め込み類似度の弱点を、対照学習による意味アラインメントで補強する新しいLLM評価メトリック。"
    ),
    "Towards Controllable Image Generation through Representation-Conditioned Diffusion Models": (
        "表現条件付き拡散モデルで画像生成を制御",
        "拡散モデルを表現空間で条件付けることで、より細かい制御性を出す画像生成手法。"
    ),
    "2-ASP(Q) programs with weak constraints: Complexity and efficient implementation": (
        "弱制約付き2量化ASP(Q)プログラムの計算量と実装",
        "Answer Set Programmingに量化子を加えたASP(Q)の2量化＋弱制約クラスについて計算量と効率実装を解析した理論研究。"
    ),
    "PARE: Pruning and Adaptive Routing for Efficient Video Generation": (
        "PARE：プルーニング＋適応ルーティングで映像生成を効率化",
        "Video Diffusion Transformerのブロック幅・深さ・反復サンプリングの計算コストを、適応的なルーティングで圧縮する手法。"
    ),
    "FinHarness: An Inline Lifecycle Safety Harness for Finance LLM Agents": (
        "FinHarness：金融LLMエージェント向けの実行時安全ハーネス",
        "プロンプト経由の不正操作をブロックしつつ、正当な多段ワークフローは通すことを目指す、金融エージェント用の実行時安全レイヤ。"
    ),
    "EdgeFlow: Edge-Map Augmented VLM-Based Flowchart Processing for Industrial Requirements Engineering": (
        "EdgeFlow：エッジマップ拡張VLMで工業フローチャートを解釈",
        "産業要件で静的画像のまま放置されがちなフローチャートを、エッジマップを補強したVLMで機械可読化する手法。"
    ),
    "Maat: The Agentic Legal Research Assistant for Competition Protection": (
        "Maat：競争法リサーチを支援するエージェント",
        "競争法・M&A判例を網羅的にレビューするエージェントAI。"
    ),
    "Governed Evolution of Agent Runtimes through Executable Operational Cognition": (
        "実行可能な運用認知でエージェントランタイムを統治",
        "コードを使い捨て出力ではなく『実行可能な運用基盤』として扱うエージェントランタイム設計を、ガバナンス込みで進化させるフレーム。"
    ),
    "Semantic Gradients Interactions in SSD: A Case Study in Racial Identity and Hate Speech": (
        "意味勾配の交互作用：人種アイデンティティとヘイト発話の事例研究",
        "Supervised Semantic Differentialを拡張し、グループや特性で意味勾配がどう変わるかをテスト可能にする統計フレーム。"
    ),
    "Modeling Agentic Technical Debt and Stochastic Tax: A Standalone Framework for Measurement, Simulation, and Dashboarding": (
        "エージェント技術的負債と確率的『税』のモデル化",
        "ツール・記憶・オーケストレーションが絡むエージェントAIの技術的負債を定量計測・シミュレーション・ダッシュボード化する独立フレームワーク。"
    ),
    "Q-GeoMem: Question-Guided Geometric Memory for Video Spatial Reasoning": (
        "Q-GeoMem：質問駆動の幾何メモリで映像空間推論",
        "映像空間推論で『質問に必要な視点依存情報』だけを保持する質問ガイド型幾何メモリ。"
    ),
    "Probabilistic Smoothing with Ratio-Monotone Transforms for Global Optimization": (
        "比単調変換による確率平滑化での大域最適化",
        "ガウス核と特定変換に依存していた確率平滑化を、比単調な変換族で一般化しハイパー感度を緩和する。"
    ),
    "Real Images, Worse Judgments: Evaluating Vision-Language Models on Concreteness and Imagery": (
        "VLMは『役に立つ視覚証拠』を区別できない",
        "視覚を入れれば常に役立つという前提を疑い、VLMが有用な視覚証拠とそうでないものを区別できないことを示した研究。"
    ),
    "Riding the Shifting Potential: When Reactive Control Suffices for Multi-Goal Behavior": (
        "リアクティブ制御で多目的タスクをこなせる条件",
        "多目的タスクで反応的制御では局所解にハマるとされてきた通説に対し、ポテンシャルを動的に切り替えれば反応的制御で十分であると示す研究。"
    ),
    "When Does Demographic Information Help? Data and Modeling Regimes for Perspective-Aware Hate Speech Detection": (
        "デモグラ情報がヘイト検出に効くのはいつか",
        "アノテータの属性情報がヘイト検出に効くケース・効かないケースを、データ量とモデル化方式の組み合わせで体系化した研究。"
    ),
    "Chartographer: Counterfactual Chart Generation for Evaluating Vision-Language Models": (
        "Chartographer：反実仮想チャートでVLMを評価",
        "Chart QAでショートカットや既視感に頼っていないかを暴くため、反事実的に作り替えたチャートで評価するベンチマーク。"
    ),
    "How and What to Imagine? Visual Thinking in Unified Multimodal Models for Cross-View Spatial Reasoning": (
        "クロスビュー空間推論のためのビジュアル思考",
        "VLMが言語に頼って細かい幾何を失う問題に対し、画像で考える『visual thinking』を統一マルチモーダルモデルで実装。"
    ),
    "Greening AI Inference with Accuracy and Latency-aware User Incentives": (
        "AI推論をグリーンにする、精度・レイテンシ込みのユーザインセンティブ設計",
        "AI推論のカーボン排出を抑えるため、精度とレイテンシを考慮したユーザ向けインセンティブ機構を提案。"
    ),
    "Normal Guidance is what Attention Needs": (
        "法線ガイドが注目すべき正規化",
        "ボリューム単位の二値ラベルしか持たない弱教師ありで3D医用画像分類器を学習する手法。"
    ),
    "PlayClass: Automated Play Behaviour Classification in Poultry": (
        "PlayClass：家禽の『遊び』行動の自動分類",
        "動物福祉モニタリングが負の指標に偏っているのを補うため、家禽の遊び行動という正の指標を自動分類するパイプライン。"
    ),
    "Risk Averse Alert Prioritization for IDS Using Subnormal Gaussian Fuzzy Models": (
        "リスク回避型のIDSアラート優先度付け",
        "侵入検知のアラート疲れを、サブノーマル・ガウシアン・ファジィでリスク回避的に優先度付けして緩和。"
    ),
    "Self-Ensembling Vision-Language Models for Chart Data Extraction": (
        "Self-EnsembleでVLMからチャートデータを抽出",
        "チャート画像から元の数値を抜き出す作業を、VLMをself-ensembleさせる構成で精度向上。"
    ),
    "Probing Cultural Awareness in LLMs: A Case Study of Cross-Culture Aesthetic Stylistics": (
        "LLMの文化的気配り——美的修辞のケーススタディ",
        "LLMが文化文脈に応じた『美的修辞』を操れるかを評価し、依然として大きなギャップがあることを示す。"
    ),
    "Gemini Embedding 2: A Native Multimodal Embedding Model from Gemini": (
        "Gemini Embedding 2——ネイティブにマルチモーダルな埋め込みモデル",
        "動画・音声・画像・テキストを統一表現空間に埋め込む、Geminiベースのネイティブ・マルチモーダル埋め込みモデル新バージョン。"
    ),
    "Separating Semantic Competition from Context Length in RAG Reading": (
        "RAGの読みエラーを『意味競合』と『文脈長』に切り分ける",
        "正しいパッセージを引いてもRAGが間違えるケースを、意味的な競合と単なる文脈長負荷とに切り分けた分析。"
    ),
    "BASIS: Batchwise Advantage Estimation from Single-Rollout Information Sharing for LLM Reasoning": (
        "BASIS：単一ロールアウト情報共有によるアドバンテージ推定",
        "検証可能報酬RLでLLMの推論を伸ばす際、計算効率と分散低減のトレードオフをバッチ内情報共有で改善する手法。"
    ),
    "Detectability in Diversity: Improved Canary Crafting for Privacy Auditing in One Run": (
        "1ラン監査用のカナリア生成を改良",
        "差分プライバシ保証を経験的に下界評価するプライバシ監査で、1回の学習ランで判定できるよう多様な『カナリア』を作る手法。"
    ),
    "It's Not Always Sycophancy: Measuring LLM Conformity as a Function of Epistemic Uncertainty": (
        "それはお世辞じゃない——LLMの『同調』は認識的不確実性で説明できる",
        "LLMがユーザのプッシュバックで意見を変える現象は、RLHFで覚えた『お世辞』だけでは説明できず、認識的不確実性のパラメタにもなっていることを示す。"
    ),
    "A Dynamic Programming Framework for Discovering Count and Values of Multilevel Image Thresholding": (
        "閾値数と値を同時に発見する動的計画法",
        "多段画像閾値処理で閾値の数自体を入力に取らず、動的計画で同時に決定するフレームワーク。"
    ),
    "Falcon-X: A Time Series Foundation Model for Heterogeneous Multivariate Modeling": (
        "Falcon-X：異種多変量時系列の基盤モデル",
        "多くの時系列基盤モデルが単変量止まりだった課題に対し、異種多変量に強い基盤モデル設計を提示。"
    ),
    "FineVLA: Fine-Grained Instruction Alignment for Steerable Vision-Language-Action Policies": (
        "FineVLA：きめ細かい指示に従えるVLAポリシー",
        "ロボット用VLAモデルが『何をするか』だけでなく『どうするか』の指示にも従えるよう、細粒度な指示アラインメントで学習する手法。"
    ),
    "Causal Risk Minimization for High-Dimensional Treatments": (
        "高次元介入に対する因果リスク最小化",
        "セラピー内容や決算開示文といった高次元な『介入』の効果を、因果リスク最小化で予測する枠組み。"
    ),
    "SIA: Self Improving AI with Harness & Weight Updates": (
        "SIA：ハーネスと重みを両方更新して自己改良するAI",
        "モデル本体だけでなく、その周辺ハーネス（コード・ツール・運用）も自己更新できるAIを目指す長期ロードマップ研究。"
    ),
    "Transfer Learning using 66 Diseases for Disease Forecasting Applications": (
        "66疾患による転移学習で疾病予測を底上げ",
        "短く・ノイジーな単一疾患データの脆弱性を、66疾患を束ねた転移学習で補強する疾病予測フレーム。"
    ),
    "Lost in Sampling: Assessing Lexical Reachability in LLMs via the Word Coverage Score (WCS)": (
        "LLMの語彙リーチャビリティを測る——Word Coverage Score",
        "LLMの語彙は広いのに出力は単調になりがちな問題を、Word Coverage Scoreという指標でサンプリング側の責任として切り分ける研究。"
    ),
    "Kan Extension Transformers: A Categorical Unification of Attention, Diffusion, and Predict-Detach Self-Conditioning": (
        "Kan拡大トランスフォーマー——Attention・拡散・自己条件付けの圏論的統一",
        "Transformer各種の実装をカン拡大として統一する圏論的フレームワーク。"
    ),
    "PilotTTS: A Disciplined Modular Recipe for Competitive Speech Synthesis": (
        "PilotTTS：競争力ある音声合成のためのモジュール式レシピ",
        "数百万時間の独自データや複雑な多段アーキテクチャに頼らずに競争力あるTTSを構築するための、規律あるモジュール構成。"
    ),
}

for it in d["sources"]["arxiv"]:
    t = it.get("title", "")
    if t in arxiv_map:
        tj, sj = arxiv_map[t]
        it["title_ja"] = tj
        it["summary_ja"] = sj

# -------- HN --------
hn_map = {
    "I'm Tired of Talking to AI": (
        "『もうAIと喋るのに疲れた』",
        "AI生成回答に対する強い疲労感を綴ったエッセイ。HN首位（1783pts）で、AI疲れがメインストリーム化していることを示す象徴的な投稿。"
    ),
    "GitHub Actions was down": (
        "GitHub Actionsがダウン",
        "全世界のCI/CDが一時停止。AI時代のソフト開発がいかにGitHubに依存しているかが浮き彫りになった大規模障害。"
    ),
    "DuckDuckGo search saw 28% more visits after Google said people love AI mode": (
        "DuckDuckGoが28%増——『GoogleのAI検索好きだよね』発言の直後",
        "Googleの『ユーザーはAIモードを愛している』発言の翌週、DuckDuckGoの訪問数が28%急増。AI疲れの定量的シグナル。"
    ),
    "Tech CEOs are apparently suffering from AI psychosis": (
        "テックCEOたちが『AI精神病』にかかっているらしい",
        "TechCrunchの記事。AGI到来を信じ込みすぎたCEOたちの言動が、社内外で『AI精神病』と揶揄される現象を取り上げる。"
    ),
    "Outsourcing plus local AI will soon become more economical vs. frontier labs": (
        "オフショア＋ローカルAIがフロンティアラボより安くなる",
        "フロンティアラボのAPIに払うより、海外開発＋オープン重みのローカルAIを組み合わせた方が経済合理的になる、という主張記事。"
    ),
    "Claude Code as a Daily Driver: Claude.md, Skills, Subagents, Plugins, and MCPs": (
        "Claude Codeを日常使いに——Skills・Subagents・MCPの実戦ガイド",
        "Claude Codeを業務メインで使うための実装メモ。CLAUDE.md・Skills・サブエージェント・プラグイン・MCPを総合的に活用する構成。"
    ),
    "Uber president says AI spending is getting 'harder to justify'": (
        "Uber社長『AI投資は正当化が難しくなってきた』",
        "大手企業のCxOから『AI投資のROIが説明しづらくなっている』とハッキリ言われたのは大きな転換点。バブル期待への冷水。"
    ),
    "Incident with Pull Requests, Issues, Git Operations and API Requests": (
        "GitHubでPR・Issue・Git操作・APIが障害",
        "同日のGitHub Actions障害と並ぶ、PR/Issue/Git/APIの並行インシデント。"
    ),
    "A sleep-like consolidation mechanism for LLMs": (
        "LLMに『睡眠的圧縮』機構——KVキャッシュをfast weightに固める",
        "長文脈KVキャッシュを周期的にfast weight側へ固める『睡眠機構』論文がHNでも盛り上がる（前日のハイライト題材）。"
    ),
    "Stack Overflow’s forum is dead but the company’s still kicking": (
        "Stack Overflowのフォーラムは死んだが、会社はまだ動いている",
        "AIによってQ&Aフォーラムとしての役割が崩壊したStack Overflowが、企業向けに業態転換中、というSherwoodの記事。"
    ),
    "Training our own AI models": (
        "PostHog、自社AIモデルを訓練する",
        "PostHogが自社で軽量AIモデルを訓練している、その動機と方法を綴ったブログ。SaaS側で生成AIを内製する動きの一例。"
    ),
    "Canada to order military plane fleet from Sweden in shift from US suppliers": (
        "カナダがスウェーデン製軍用機を発注——米サプライヤから離れる",
        "AI直球ではないが、AI/防衛系の調達ナラティブにも関わる地政学ニュース。"
    ),
    "Lombardy increases tax on data centers built in green and agricultural areas": (
        "ロンバルディア州、緑地・農地のデータセンターに最大2倍課税",
        "イタリア・ロンバルディア州がAIブームで膨張する緑地・農地のデータセンタに最大200%の課税強化。AI物理インフラへの政治的反発が顕在化。"
    ),
    "Go: Support for Generic Methods": (
        "Go言語、ジェネリックメソッドのサポート提案",
        "Goの型システム議論でジェネリックメソッドの追加が提案される。AI直結ではないが、開発者文化として大きい議論。"
    ),
    "Launch HN: Minicor (YC P26) – Windows desktop automations at scale": (
        "Launch HN: Minicor——Windowsデスクトップを大規模自動化",
        "Windows GUIを大規模自動化するMinicor。AIエージェントの『腕』としてのRPA的レイヤ。"
    ),
    "Incident with Actions and Pages": (
        "GitHub ActionsとPagesでインシデント",
        "GitHub Actions・Pagesの障害。"
    ),
    "I bypassed AWS API Gateway auth with a trailing slash. Got $12K bounty": (
        "AWS API Gateway認証を末尾スラッシュでバイパス——$12Kバウンティ",
        "末尾スラッシュ1つでAWS API Gatewayの認証を回避できたバグレポート。Bounty $12K。"
    ),
    "AI tools are only as good as your judgment": (
        "AIツールは結局あなたの判断力次第",
        "AIツールを過信せず、自分の判断とのループで使うべきだという定番論。"
    ),
    "The AI bubble isn't like the internet bubble": (
        "AIバブルはドットコムバブルとは違う",
        "Cory DoctorowによるAIバブル分析。インターネットバブルとは違って、はじけても残るインフラ価値が小さいという主張。"
    ),
    "Show HN: Posthorn, self-hosted mail gateway": (
        "Show HN: Posthorn——セルフホスト型メールゲートウェイ",
        "自前メール配信のためのセルフホストGateway。"
    ),
}

for it in d["sources"]["hn"]:
    t = it.get("title", "")
    if t in hn_map:
        tj, sj = hn_map[t]
        it["title_ja"] = tj
        it["summary_ja"] = sj

# -------- Reddit --------
reddit_map = {
    "[D] Where do you go for serious AI research discussion online? [D]": (
        "[D] 今どきマジメなAI研究議論はどこでするの？",
        "Twitterもreddit r/MachineLearningもノイズだらけになり、研究者がどこで深い議論をしているのか、という嘆きとサジェスチョン。"
    ),
    "Nothing is real anymore. We are reaching the point where crowd scenes can be entirely generated by AI.": (
        "もう何もリアルじゃない——群衆シーンも丸ごとAI生成の時代",
        "群衆シーンをまるごとAIで生成した映像が話題に。『現実と区別がつかない』段階に達したという反応。"
    ),
    "AI is becoming epistemic infrastructure controlled by a handful of private individuals?": (
        "AIが少数の私的個人に支配される『認識的インフラ』になっている？",
        "AIが知識・判断のインフラとして機能しはじめた一方で、その所有が極めて少数の私企業・個人に集中していることへの懸念。"
    ),
    "AI-generated CUDA kernels silently break training and inference [R]": (
        "AIが書いたCUDAカーネルが学習・推論をサイレントに壊している",
        "コード生成AIに書かせたCUDAカーネルが、数値的にズレた挙動でも『動いてしまう』ため、学習・推論を静かに壊しているという警鐘。"
    ),
    "Already 11 000 submissions for EMNLP? [D]": (
        "EMNLPの投稿数がもう1.1万件？",
        "EMNLP 2026の投稿数が早くも1.1万を超え、査読プロセスが破綻寸前という研究界の悲鳴。"
    ),
    "The Young Are Being Battered by AI as Hiring Shifts to Older Workers": (
        "若年層がAIに殴られている——採用がベテラン側にシフト",
        "AIで若手の初級業務が圧縮された結果、企業がベテラン採用に寄り、若年層の雇用が悪化しているというトレンド記事。"
    ),
    "Scoop: Trump appoints Bondi to White House AI panel": (
        "[Scoop] トランプ、ボンディ司法長官をホワイトハウスAIパネルに任命",
        "Axiosのスクープ。司法長官Pam BondiがホワイトハウスのAI諮問パネルに任命され、AI政策の法執行寄り傾斜が懸念される。"
    ),
    "Anthropic just published how they contain Claude agents, including two security incidents they got wrong": (
        "Anthropicが『Claudeエージェントをどう封じ込めているか』を公開——自社で失敗した2件込み",
        "Anthropicが内部で運用しているClaudeエージェントの封じ込めポリシーと、対処を誤った2件のセキュリティ事故を公開。"
    ),
    "Wiz Integrates with Anthropic's Compliance API": (
        "Wizが AnthropicのCompliance APIと統合",
        "クラウドセキュリティのWizが、AnthropicのCompliance APIと統合。AIエージェント運用に対する企業ガバナンスの一例。"
    ),
    "Which AI image generator is actually worth the money?": (
        "結局どのAI画像生成にお金を払う価値がある？",
        "課金して使うべき画像生成AIはどれか、というユーザディスカッション。"
    ),
    "[R]GNN Model For Fraud Detection Isn't Performing Well[R]": (
        "[R] 不正検出GNNモデルの性能が出ない件",
        "不正検出向けGNNが思うように学習しないという実践相談スレ。"
    ),
    "[P] Built a portable GPU ISA after reading too many architecture manuals [P]": (
        "[P] アーキマニュアル読みすぎてポータブルなGPU ISAを作った",
        "GPUアーキテクチャマニュアルを読み込みすぎた結果、ポータブルなGPU ISAを自作したというホビープロジェクト。"
    ),
    "Aiki my local Wikipedia Retrieval-Augmented Generation system [R]": (
        "Aiki：手元Wikipedia RAGシステム",
        "ローカルWikipediaを対象にしたRAGシステムを自作したという紹介。"
    ),
    "Looking for an AI image generator, what's the best one": (
        "おすすめのAI画像生成は？",
        "用途別のAI画像生成おすすめスレ。"
    ),
    "Profiling PyTorch training without accidentally stalling the GPU [D]": (
        "GPUを止めずにPyTorch学習をプロファイルしたい",
        "プロファイルでGPUをストールさせないテクのディスカッション。"
    ),
    "How I build my own zero cost Agent": (
        "ゼロコストで自分のエージェントを組む",
        "課金APIを使わずに自前で組むエージェント構成のメモ。"
    ),
    "The Most Terrifying Superintelligence Might Not Want to Rule Us at All.": (
        "もっとも恐ろしい超知能は『人類支配を望まない』ものかもしれない",
        "超知能リスクの議論として、支配欲ですら持たない無関心型がより怖いという思考実験。"
    ),
    "Claude as an Orchestrator: Why Agentic AI Can't Be Secured by the AI Alone": (
        "Claudeをオーケストレータに——エージェントAIをAI単独で守るのは無理",
        "エージェントAIのセキュリティは、AI自身だけでなく外部のガードレールやランタイムが必須、というブログ。"
    ),
    "How to not doom over AI? Anything encouraging about the future?": (
        "AIで絶望しないには？未来に希望ある？",
        "AI悲観で疲れた人々が『何か明るい未来はないか』を語り合うスレ。"
    ),
    "Built a tool to save Claude responses (and ChatGPT, Gemini) into one searchable vault - sharing in case it's useful": (
        "Claude/ChatGPT/Geminiの回答を一括Vaultに保存できるツールを作った",
        "各AIの回答を一元保存・検索できる個人ナレッジ管理ツールの紹介。"
    ),
}

for it in d["sources"]["reddit"]:
    t = it.get("title", "")
    if t in reddit_map:
        tj, sj = reddit_map[t]
        it["title_ja"] = tj
        it["summary_ja"] = sj

# -------- GitHub Trending --------
github_map = {
    "Leonxlnx/taste-skill": (
        "taste-skill：AIに『センス』を与えるスキル",
        "AIの出力が陳腐で量産品的になりがちな問題に対し、AIに『味（taste）』を与えてダサい量産物を抑止することを謳うスキルパック。本日2700+スター獲得。"
    ),
    "DigitalPlatDev/FreeDomain": (
        "FreeDomain：無料ドメイン配布プロジェクト",
        "個人向けに無料サブドメインを配布するプロジェクトが急上昇。AI関連ではないが、AIサイドプロジェクトのホスティング需要が背景にあるか。"
    ),
    "affaan-m/ECC": (
        "ECC：エージェントハーネス最適化スイート",
        "Claude Code / Codex / Cursor / Opencodeなど主要エージェントの『ハーネス』を最適化するスキル・メモリ・セキュリティ統合システム。"
    ),
    "harry0703/MoneyPrinterTurbo": (
        "MoneyPrinterTurbo：AIで短尺動画を一発生成",
        "テーマだけ入れればAI LLMが台本・画像・音声・動画を組み立て、TikTok向け短尺動画を一発生成する人気OSS。"
    ),
    "obra/superpowers": (
        "superpowers：エージェント開発のためのスキルフレームワーク",
        "Claude Codeなどのエージェント向けスキル・メソドロジを統合した『superpowers』フレームワーク。本日も1600+スター。"
    ),
    "mukul975/Anthropic-Cybersecurity-Skills": (
        "Anthropic-Cybersecurity-Skills：754のセキュリティスキル集",
        "MITRE ATT&CK・NIST CSF・MITRE ATLAS・D3FEND・NIST AI RMFの5フレームワークにマップされた、AIエージェント向けセキュリティスキル754個。"
    ),
    "anthropics/knowledge-work-plugins": (
        "Anthropic公式：ナレッジワーク向けプラグイン集",
        "Claude Cowork向け、ナレッジワーカーが日常業務で使えるプラグインのオープンソース集。"
    ),
    "hardikpandya/stop-slop": (
        "stop-slop：AIっぽさを文章から除去するスキル",
        "『AIが書いた』と分かる定型表現や言い回しを文章から取り除くスキルファイル。"
    ),
    "twentyhq/twenty": (
        "twenty：AI時代のオープンソースSalesforce",
        "AIネイティブを謳う、Salesforceのオープン代替CRM。"
    ),
    "moeru-ai/airi": (
        "airi：自分で持てる『推しAI』コンパニオン",
        "セルフホスト型の推しAI/Vtuber的コンパニオン。Minecraft・Factorioもプレイし、Neuro-sama的体験を目指す。"
    ),
}

for it in d["sources"]["github"]:
    fn = it.get("full_name", "")
    if fn in github_map:
        tj, sj = github_map[fn]
        it["title_ja"] = tj
        it["summary_ja"] = sj

# -------- Blogs --------
blogs_map = {
    "ITBench-AA: Frontier Models Score Below 50% on the First Benchmark for Agentic Enterprise IT Tasks — by Artificial Analysis and IBM": (
        "ITBench-AA：エージェントAIの企業IT実務、フロンティアでも50%未満",
        "Artificial AnalysisとIBMが共同で発表した、エンタープライズITオペレーションをエージェントAIが実行できるかの初のベンチマーク。最新のフロンティアモデルでも50%未満で、現場仕事の壁が浮き彫りに。"
    ),
    "Building self-improving tax agents with Codex": (
        "Codexで自己改善する税務エージェントを作る",
        "OpenAI・Thrive・Creteが組み、税務申告を自動化＋自己改善するエージェントを構築。"
    ),
    "Warp’s big bet on building open source with GPT-5.5": (
        "Warp、GPT-5.5でOSS開発に大型賭け",
        "ターミナル「Warp」がGPT-5.5を中核に、ローカル・クラウド・OSSをまたぐコーディングエージェントを動かす。"
    ),
    "Election information and safeguards in 2026": (
        "2026年選挙：OpenAIによる情報と防護策",
        "世界的選挙イヤーに向け、OpenAIが選挙情報アクセス・サイバー防衛者支援・AI透明性で打つ施策をまとめた声明。"
    ),
    "Reachy Mini goes fully local": (
        "Reachy Miniが完全ローカル化",
        "Hugging Faceの卓上ロボット「Reachy Mini」が、対話・推論をすべてオンデバイスで完結させる完全ローカル版に。"
    ),
    "Shipping a Trillion Parameters With a Hub Bucket: Delta Weight Sync in TRL": (
        "TRLでTrillion級のデルタ重み同期",
        "TRL（Transformer Reinforcement Learning）に、Hugging Face Hubのバケットを使った1兆パラメタ級デルタ重み同期機能を実装した話。"
    ),
    "OpenAI, Grupo Folha and Grupo UOL announce strategic content partnership": (
        "OpenAI、ブラジル大手メディアGrupo Folha/UOLと提携",
        "ブラジルのGrupo FolhaとUOLがOpenAIと戦略提携。ChatGPT内に出典付きのブラジル報道を統合。"
    ),
    "Harness, Scaffold, and the AI Agent Terms Worth Getting Right": (
        "『ハーネス』『スキャフォルド』——AIエージェント用語をちゃんと使い分けよう",
        "Hugging Faceブログ。エージェント実装で乱用されがちな『ハーネス』『スキャフォルド』『フレームワーク』といった用語を整理し、議論の質を上げる試み。"
    ),
    "Towards Speed-of-Light Text Generation with Nemotron-Labs Diffusion Language Models": (
        "Nemotron-Labs拡散LMで『光速』テキスト生成へ",
        "NVIDIAが、拡散ベース言語モデルNemotron Diffusionの最新版を解説。自己回帰型より大幅に速いテキスト生成のロードマップを示す。"
    ),
    "Catch up on the Dialogues stage at Google I/O 2026.": (
        "Google I/O 2026『Dialogues』ステージのまとめ",
        "Sundar PichaiCEOらが登壇したGoogle I/O 2026のDialoguesセッションのリキャップ。"
    ),
    "Specialization Beats Scale: A Strategic Variable Most AI Procurement Decisions Overlook": (
        "AI調達では『スケール』より『専門化』が効く",
        "AIモデル選定で『規模』ばかりを変数にしがちな企業向けに、専門化（タスク特化・データ特化）の方が実利益に直結することを示す戦略論。"
    ),
    "OpenAI named a Leader in enterprise coding agents by Gartner": (
        "OpenAIがGartner『エンタープライズAIコーディングエージェント』のリーダーに",
        "Gartner Magic Quadrantで、OpenAIのCodexがエンタープライズコーディングエージェント部門のリーダーに位置付けられた。"
    ),
    "How Virgin Atlantic ships faster with Codex": (
        "Virgin AtlanticがCodexで開発を加速",
        "Virgin AtlanticがCodexで、新モバイルアプリの単体テストカバレッジを高水準まで引き上げつつ、固定の繁忙期デッドラインまでにリリース。"
    ),
    "AdventHealth advances whole-person care with OpenAI": (
        "AdventHealthがOpenAIで医療業務を効率化",
        "米AdventHealthがChatGPT for Healthcareで管理業務を圧縮し、医師の患者時間を増やす取り組み。"
    ),
    "We’re announcing new community investments in Missouri.": (
        "Google、ミズーリ州にコミュニティ投資",
        "GoogleがミズーリのAI/インフラ拠点周辺で、人材育成とエネルギー支援プログラムに投資。"
    ),
}

for it in d["sources"]["blogs"]:
    t = it.get("title", "")
    if t in blogs_map:
        tj, sj = blogs_map[t]
        it["title_ja"] = tj
        it["summary_ja"] = sj

# -------- Highlights --------
highlights = [
    {
        "source": "hn",
        "title": "I'm Tired of Talking to AI",
        "title_ja": "『AIと喋るのに疲れた』——AI疲労がついにメインストリーム化",
        "url": "https://orchidfiles.com/im-tired-of-ai-generated-answers/",
        "hot_take_ja": "HN1位（1783pts）に上がってきたのは、AIに対する技術論ではなく『もうウンザリ』という感情エッセイだった。同日にはDuckDuckGoがGoogleのAI推し発言の翌週に訪問数28%増、テックCEOの『AI精神病』記事も上位入り。2026年5月のAI疲労がついに『データ点になった日』として記録されそうだ。",
        "detail_ja": "Hacker News首位に来たのは新技術でも論文でもなく、AI生成回答に対するシンプルな疲労を綴ったエッセイだった。著者は、検索・サポート・SNS・職場のあらゆる場面でAIが要約・代弁・回答するようになり、自分が触れる文章のどこまでが人間の意図かわからなくなったと書く。重要なのは、これが孤立した感情ではなく、同じ日にHN上位に来た複数の記事と共鳴している点だ。DuckDuckGoは『Googleのユーザーは皆AIモードを愛している』発言の翌週に訪問数28%増を記録、TechCrunchは『テックCEOがAI精神病にかかっている』というルポを出し、Cory Doctorowは『AIバブルはドットコムバブルと違って残るものが少ない』と書いた。技術的には突発事件ではないが、消費者・市民の側に明確な逆方向の流れが見え始めたタイミングで、これからのプロダクト設計でも『AIを使っていない選択肢を残す』ことが競争優位になる兆しと読める。AI企業側もこの空気を読まないと、提供を増やすほど好感度が下がる『過剰提供』フェーズに入る恐れがある。",
        "detail_en": "The #1 post on Hacker News today is not a new model or paper but a plain-spoken essay titled 'I'm Tired of Talking to AI' — about being exhausted by how every channel (search, support, social, work) now mediates language through an AI layer. What makes it significant is the company it kept on the front page: DuckDuckGo posted a 28% spike in visits the week after Google's executives claimed users 'love' AI mode; TechCrunch ran a piece on tech CEOs 'suffering from AI psychosis'; Cory Doctorow argued the AI bubble will leave less behind than the dot-com bubble did. Taken together, these are not isolated reactions but a coherent counter-current finally large enough to register as data. For product builders, the implication is that 'AI-free option' is becoming a feature, not an oversight. For AI companies, it is a warning that pushing more AI into every surface may now reduce, rather than increase, perceived value — the field has entered an overprovisioning phase. The market and the discourse are quietly diverging from the strategy of the labs.",
        "key_points_ja": [
            "HN1位はAI生成回答への『疲労』エッセイ（1783pts）",
            "DuckDuckGoの訪問数がGoogleのAI推し発言後に28%増",
            "TechCrunchが『テックCEOのAI精神病』を特集",
            "ドクトロウ『AIバブルはドットコムより残るものが少ない』",
            "『AIを使わない選択肢』が機能要件化する兆し",
            "AI企業は『過剰提供フェーズ』に入ったリスク"
        ],
        "key_points_en": [
            "HN's #1 today is an essay about being tired of AI (1783 pts)",
            "DuckDuckGo visits jumped 28% after Google's AI-mode claim",
            "TechCrunch piece on tech CEOs 'AI psychosis' goes viral",
            "Doctorow: AI bubble will leave less than the dot-com one",
            "'AI-free option' is becoming a product feature, not an oversight",
            "AI labs may have entered an over-provisioning phase"
        ],
    },
    {
        "source": "hn",
        "title": "Uber president says AI spending is getting 'harder to justify'",
        "title_ja": "Uber社長『AI投資はもう正当化が難しい』——大手CxOからついに本音",
        "url": "https://www.theverge.com/transportation/937116/uber-ai-investment-hard-to-justify",
        "hot_take_ja": "Uber社長Andrew Macdonaldが『AI投資のROIを正当化するのが難しくなってきている』と公の場で発言した。大手のCxOからここまで明確な懐疑がメディアに乗るのは初めてに近く、ITBench-AAで『フロンティアモデルでも企業ITタスクは50%未満』と同日に出たことと合わせて読むと、エンタープライズAIのキャズム前夜らしい光景が見える。",
        "detail_ja": "Uber社長Andrew MacdonaldがThe Vergeの取材で、AI投資はもはや自動的に正当化される領域ではなく、ROIをきちんと示すのが難しくなってきている、と語った。これまでも一部ヘッジファンドや独立アナリストはAI capex懐疑論を出していたが、世界規模のオペレーションを回す上場企業のCxOが、メディアにここまで直球で『coverを取りに来ている』のは大きい。同日、Artificial AnalysisとIBMが共同で出した『ITBench-AA』ベンチマークでは、最新フロンティアモデルでも企業IT実務タスクで50%を切るスコアしか取れず、エージェントAIの現場適用が想定よりも遅いことが裏付けられている。Cory Doctorowの『AIバブル分析』、若年層雇用の悪化記事、データセンタ課税といった逆風ストーリーも並んでおり、生成AIの初期ハイプサイクル後半に典型的な『パイロットの墓場』フェーズに入りつつある兆候だ。投資家・経営層には、規模より特化（同日の『Specialization Beats Scale』も参照）でROIを取りに行く戦略へのリ・ピボットが求められる。",
        "detail_en": "Uber president Andrew Macdonald told The Verge that AI spending has become 'harder to justify' — a striking line because it does not come from a hedge-fund skeptic or an outside analyst, but from a sitting C-level executive at a global operating company. Public skepticism from a CxO of this scale is rare and consequential, because it signals to other large enterprises that visibly questioning AI ROI is no longer career-limiting. The statement landed the same day that Artificial Analysis and IBM released ITBench-AA, the first agentic benchmark for enterprise IT operations, on which frontier models score below 50%. Combined with Doctorow's bubble piece, articles on AI-driven hiring damage to young workers, and Lombardy's new data-center tax, the day reads like a classic late-stage hype-cycle moment — pilots failing to convert, the discourse pivoting from 'how fast' to 'is it worth it'. For procurement leaders the practical takeaway is the same as the 'Specialization Beats Scale' essay published the same day: pivot from buying the biggest frontier model to buying narrowly specialized models with a defensible ROI story. For AI vendors, the window in which 'AI' alone justified the line item is closing.",
        "key_points_ja": [
            "Uber社長Macdonald『AI支出はROI説明が難しくなった』",
            "大手上場CxOがメディアにここまで明確な懐疑を出すのは異例",
            "同日のITBench-AAでフロンティアでも企業IT実務50%未満",
            "Doctorow『AIバブルは残るものが少ない』も同日上位",
            "『スケールより特化』が調達側の新しい合言葉に",
            "Enterprise AIは『パイロットの墓場』フェーズに入る兆し"
        ],
        "key_points_en": [
            "Uber's president: AI spending is 'harder to justify'",
            "Rare for a CxO at this scale to voice this skepticism publicly",
            "Same day: ITBench-AA shows frontier models <50% on enterprise IT",
            "Doctorow's 'AI bubble' piece also trends on HN",
            "Procurement narrative shifting to 'specialization beats scale'",
            "Signs that enterprise AI is entering its 'pilot graveyard' phase"
        ],
    },
    {
        "source": "blog",
        "title": "ITBench-AA: Frontier Models Score Below 50% on the First Benchmark for Agentic Enterprise IT Tasks",
        "title_ja": "ITBench-AA：エージェントAI×企業IT実務の初ベンチマークで、フロンティアモデルも50%未満",
        "url": "https://huggingface.co/blog/ibm-research/itbench-aa",
        "hot_take_ja": "Artificial AnalysisとIBMが、企業のIT運用（インシデント対応・SREタスク・ITSMフロー）でエージェントAIがどこまで現場仕事できるかを測る初のベンチマーク『ITBench-AA』を公開。最新フロンティア・モデルでも50%未満という結果は、コーディングベンチで90%超を叩き出している現状とのギャップが大きい。『コードは書けても運用は無理』が定量的に示された。",
        "detail_ja": "Artificial AnalysisとIBM Researchが共同で発表したITBench-AAは、エージェントAIが実際の企業IT運用——インシデント対応・SREタスク・ITSMチケット処理など——をエンドツーエンドで遂行できるかを評価する、本格的な業界向けベンチマークだ。重要なのは、SWE-Bench系のコーディングベンチでフロンティアモデルが90%超まで来ているのに対し、ITBench-AAではすべての最新モデルが50%を切っているという結果である。ギャップの原因は、ITオペが①長時間の状態追跡、②複数システムを跨ぐtool use、③曖昧な人間の指示を企業ポリシーに沿って解釈、④失敗の代償が大きい意思決定、を同時に要求するからで、純粋な推論力やコード生成力だけでは足りない。これはAIエージェントの『汎用さ』を測るうえで意味のあるシグナルで、近未来に注目すべきは、モデル単体性能ではなく『エージェントハーネス・記憶・ガバナンス』を含めたシステム評価の方だ。Uber社長のROI懐疑発言や、同日OpenAIがGartner Magic Quadrantのリーダーに選ばれたこととも併せて読むと、買い手側がエージェントAIに払う対価を、コードベンチでなく実務ベンチで判断するフェーズに入ったと言える。",
        "detail_en": "Artificial Analysis and IBM Research jointly released ITBench-AA, the first serious benchmark that measures whether agentic AI systems can perform real enterprise IT operations end-to-end — incident response, SRE tasks, ITSM ticket handling, and similar. The headline number is that every current frontier model scores below 50%, a striking contrast to coding benchmarks like SWE-Bench where leading models already exceed 90%. The reason for the gap is structural: enterprise IT work demands long-horizon state tracking, cross-system tool use, interpreting ambiguous human instructions against company policy, and decisions whose failure cost is high — none of which are well exercised by code-completion benchmarks. ITBench-AA matters because it shifts the conversation from raw model capability to total agent system quality (harness, memory, guardrails, escalation). Read alongside Uber's president questioning AI ROI and OpenAI being named a Gartner MQ leader in enterprise coding agents the same day, the throughline is clear: the buyer is starting to evaluate AI on operational benchmarks rather than coding ones, and the floor of capability there is still low enough to explain enterprise AI's revenue lag.",
        "key_points_ja": [
            "Artificial Analysis×IBMが企業ITオペ向けエージェント評価を公開",
            "全フロンティアモデルがスコア50%未満",
            "コードベンチでは90%超なのに業務オペは半分以下",
            "状態追跡・cross-systemツール・ポリシー解釈が壁",
            "評価軸は『モデル単体』から『ハーネス込みシステム』へ",
            "Uber/Doctorow懐疑論と同日に出てきた象徴的データ"
        ],
        "key_points_en": [
            "Artificial Analysis × IBM launch first benchmark for agentic enterprise IT",
            "All frontier models score below 50%",
            "Sharp gap vs coding benchmarks where the same models exceed 90%",
            "Long-horizon state, cross-system tools, and policy interpretation are the wall",
            "Eval focus shifts from model alone to full agent system (harness, memory)",
            "Lands the same day as Uber's ROI skepticism — symbolic timing"
        ],
    },
    {
        "source": "reddit",
        "title": "AI-generated CUDA kernels silently break training and inference",
        "title_ja": "AI生成のCUDAカーネルが、学習も推論もサイレントに壊している",
        "url": "https://www.reddit.com/r/MachineLearning/comments/1tpaw6x/aigenerated_cuda_kernels_silently_break_training/",
        "hot_take_ja": "r/MachineLearningで、生成AIに書かせたCUDAカーネルが『動くけど数値が微妙にズレている』状態で学習・推論を静かに壊している、というレポートが拡散。動いてしまうことが問題、というAI生成コードの怖いパターン。GPUコードのレビュー文化が追いついていない時点で『AI生成インフラ』はバンドリングしないと地雷化する。",
        "detail_ja": "r/MachineLearningで話題になった投稿。生成AIに頼んで書かせたCUDAカーネルが、コンパイルも通り、テンソルshapeも合うため一見『動いている』ように見えるのに、実は数値精度の境界条件・同期・atomic順序などで微妙にズレた振る舞いをし、結果として学習が静かに収束しない、推論結果が微妙に違う、という事例が複数報告されている。怖いのは、CIで掴むには差が小さすぎて検査が漏れること、そしてCUDA知識を持たないチームが『手書きで書くより速かった』と本番に乗せてしまうことだ。これはコード生成AIの限界ではなく、現代の現場で『AI生成コードのレビュー文化が追いついていない』というプロセス問題でもある。短期的な対処は、(1)GPUカーネルなど低レイヤは必ず数値同等性テスト＋カーネルプロファイルを通す、(2)生成AIが書ける範囲を制限する社内ポリシーを作る、(3)複数モデルにクロスチェックさせる、あたりに整理される。長期的には、GPUカーネルのような『間違えが静かに広がる領域』に対して、AIが書いたコードを既存のverifierに食わせる仕組みが必要になる。",
        "detail_en": "A widely-shared r/MachineLearning thread describes a quietly dangerous pattern: CUDA kernels written by code-generating AIs that compile, accept the right tensor shapes, and superficially 'work' — but quietly produce subtly wrong numerics due to boundary conditions, synchronization, or atomic ordering mistakes. The result is silent failure: training that doesn't converge as expected, or inference outputs that drift in ways CI tests do not catch because the deltas are too small. This is more dangerous than the obvious bug. CUDA code looks plausible enough that teams without deep GPU expertise deploy it because 'the AI wrote it faster than we could'. The takeaway is less about model limitations and more about a process gap: organizational review culture has not yet caught up to AI-generated infrastructure code. Practical mitigations: (1) require numerical-parity tests and kernel profiling for any AI-generated low-level code, (2) restrict which categories of code generation are allowed in production, (3) cross-check generations across multiple models. Longer term, AI-generated kernels need to be fed into existing GPU verifiers and not trusted on plausibility alone.",
        "key_points_ja": [
            "生成AIが書いたCUDAカーネルが『動くが数値がズレる』",
            "コンパイル・shape合致で素通り、CIでも掴みにくい",
            "学習が静かに収束しない／推論結果が微妙に違う",
            "GPU専門知識のないチームほどそのまま本番に",
            "対処：数値同等性テスト・適用範囲ポリシー・モデル間クロスチェック",
            "AI生成コードの『レビュー文化』整備が急務"
        ],
        "key_points_en": [
            "AI-written CUDA kernels compile and 'work' but are numerically off",
            "Shape matches and clean compiles let them pass CI undetected",
            "Symptoms: silent non-convergence, drifting inference outputs",
            "Teams without deep GPU knowledge ship them to production",
            "Mitigations: parity tests, scope policies, multi-model cross-check",
            "Bigger problem: review culture has not caught up to AI infra code"
        ],
    },
    {
        "source": "reddit",
        "title": "Scoop: Trump appoints Bondi to White House AI panel",
        "title_ja": "[Scoop] トランプ、Bondi司法長官をホワイトハウスAI諮問パネルに任命",
        "url": "https://www.axios.com/2026/05/27/pam-bondi-white-house-ai",
        "hot_take_ja": "Axiosのスクープ。司法長官Pam BondiがホワイトハウスのAI諮問パネルに加わった。これでパネルが『法執行寄り』に大きく傾く構図に。米国のAIガバナンスがイノベーション促進からエンフォースメント寄りに動くかは、来年のフロンティアモデル展開・オープン重みポリシー・移民エンジニア政策にまで波及しうる。",
        "detail_ja": "Axiosがスクープしたところによれば、トランプ大統領は司法長官Pam BondiをホワイトハウスのAI諮問パネルに加えた。これは政策的に大きい人事だ。司法長官が常設のAIパネルに入ることで、米連邦のAI議論の重心が『国家安全保障×法執行』寄りにシフトする。具体的に影響を受けうるのは、(1)フロンティアモデルの輸出規制と公開条件、(2)ディープフェイク・選挙コンテンツに対する刑事責任の範囲、(3)海外AI企業の米国内事業に対する制裁・調査の運用、(4)オープン重み公開やオフショア開発（同日HN上位の『outsourcing+local AI』記事と直接ぶつかる論点）の取り扱い、(5)AI関連の移民・労働ビザ。OpenAIが同日に発表した『2026年選挙情報の安全装置』ポストや、TechCrunchの『テックCEOがAI精神病』記事と並べて読むと、ワシントンとサンフランシスコの距離が来年は急速に詰まる予感がする。AI企業側のアフェアーズ部隊にとっては、本日の人事は『過去のAIサミットでの良い空気』が前提でなくなる転換点として扱うべき動きだ。",
        "detail_en": "Axios scooped that President Trump has added Attorney General Pam Bondi to the White House AI advisory panel. This is a meaningful appointment because it pulls the panel's center of gravity toward national security and law enforcement framing of AI rather than competitiveness or research framing. Concrete areas that may shift: (1) frontier-model export controls and publication conditions, (2) the criminal-liability perimeter around deepfakes and election content, (3) how investigations and sanctions against foreign AI companies operating in the US are run, (4) treatment of open-weight releases and offshore development — directly intersecting today's HN piece on 'outsourcing + local AI' — and (5) AI-related immigration and labor policy. Read together with OpenAI's same-day post on 2026 election safeguards and TechCrunch's piece on tech CEOs' 'AI psychosis', the signal is that Washington and the AI labs are converging — and not necessarily in friendly ways. For policy and government-affairs teams at AI companies, this appointment is the moment to stop assuming continuity with earlier, friendlier AI-summit dynamics and to plan for enforcement-led posture changes over the next year.",
        "key_points_ja": [
            "Bondi司法長官をホワイトハウスAIパネルに任命（Axiosスクープ）",
            "AI政策の重心が『国安全保障×法執行』寄りにシフトの可能性",
            "輸出規制・オープン重み公開・移民政策に直接波及しうる",
            "ディープフェイクや選挙コンテンツの刑事責任が論点に",
            "OpenAIの『2026選挙ポスト』と同日に出ている整合",
            "AIラボのGov Affairsチームは前提条件の更新が必要"
        ],
        "key_points_en": [
            "AG Pam Bondi joins White House AI advisory panel (Axios scoop)",
            "Pulls US AI policy axis toward national security and law enforcement",
            "Likely impact on export controls, open-weight releases, immigration",
            "Criminal liability scope for deepfakes/election content in play",
            "Lands the same day as OpenAI's 2026 election safeguards post",
            "AI company GovAffairs should reset assumptions about DC posture"
        ],
    },
]

d["highlights"] = highlights

# Stats
stats = d.get("stats", {})
stats["counts"] = {
    "arxiv": len(d["sources"]["arxiv"]),
    "hn": len(d["sources"]["hn"]),
    "reddit": len(d["sources"]["reddit"]),
    "github": len(d["sources"]["github"]),
    "blogs": len(d["sources"]["blogs"]),
}
stats["highlights"] = len(highlights)
d["stats"] = stats

with open(OUT, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f"Wrote {OUT}")
print(f"Highlights: {len(highlights)}")
for h in highlights:
    print(f"  - [{h['source']}] {h['title_ja']}")
