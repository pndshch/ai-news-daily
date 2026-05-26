#!/usr/bin/env python3
"""Enrich raw-2026-05-26.json with Japanese summaries and highlights."""
import json
from pathlib import Path

DATE = "2026-05-26"
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / f"raw-{DATE}.json"
OUT = ROOT / "data" / f"{DATE}.json"

with open(RAW) as f:
    d = json.load(f)

# -------- arXiv --------
arxiv_map = {
    "2605.26115v1": (
        "TriSplat：シミュレーションすぐ使える3D再構成",
        "スパースビューからフィードフォワードで三角形プリミティブを直接予測し、シミュレーション可能なメッシュをそのまま出力する3D再構成。Gaussian主流のSplatting系で曖昧だった表面表現を、推定法線で安定化する。"
    ),
    "2605.26114v1": (
        "MobileGym：モバイルGUIエージェントの検証可能シミュレータ",
        "本物のアプリのバックエンドを再現せず、JSON状態に対する決定論的判定で『成功・失敗』を検証可能にする軽量シミュレータ。GUIエージェントのオンラインRLを現実的に回せる。"
    ),
    "2605.26113v1": (
        "AnyScene：自動運転データ生成の高制御版",
        "occupancyガイドで稀少安全シナリオを生成する手法。従来は浅い条件付けや参照フレーム依存だったのを、任意位置・任意視点でも細かい制御を可能にする。"
    ),
    "2605.26112v1": (
        "モデル拡張から『ハーネス拡張』へ——エージェントAIの次のボトルネック",
        "エージェントAIの次の本丸はモデルサイズではなく、その周辺『ハーネス』——監査可能・永続・モジュール化された実行層——の設計だと主張する論文。メモリ・検索・ツール・検証を実装詳細扱いせず一級市民として扱う。"
    ),
    "2605.26111v1": (
        "MLLM容量を絞り切るsubject-driven画像生成",
        "subject保持＋テキスト指示追従の両立を、別エンコーダ方式ではなくMLLMの能力を統合的に利用して達成する設計。コピペアーチファクトを抑える。"
    ),
    "2605.26110v1": (
        "Prism：MLLMの継続的インストラクションチューニング基盤",
        "MCIT研究の評価不整合と実験再現性問題を解決する、プラグイン型の標準実験基盤。"
    ),
    "2605.26109v1": (
        "Helix4D：複雑トポロジ対応の4Dメッシュ生成",
        "Trellis2の表現力をvideo-to-4Dに拡張。透明物体・薄板・内部表面のような従来手法が苦手な構造でも破綻しない動的メッシュ生成。"
    ),
    "2605.26108v1": (
        "Reward-Tilted Distribution Matching：少ステップ生成の人間好み調整",
        "DMDと報酬ガイド型RLを統合し、few-step flow generatorを人間選好にアラインする2段階フレームワーク。"
    ),
    "2605.26106v1": (
        "Looped Diffusion LM——層を『回す』だけで拡散言語モデルが伸びる",
        "Masked Diffusion ModelのTransformer中間層を選択的にループするだけで、最大3.3倍のFLOPS削減＋推論時にループ数で計算量を動的調整可能に。シンプルだが効くアーキテクチャ提案。"
    ),
    "2605.26105v1": (
        "On-Policyな敵対的Flow蒸留で自己回帰ビデオ生成",
        "強力なブラックボックスteacherをcausal studentに蒸留する難題に対し、studentのロールアウト分布上で敵対的Flow蒸留を行う設計。"
    ),
    "2605.26104v1": (
        "EVIDENT：エンティティ視覚証拠でVideo Temporal Groundingを汎化",
        "VTGのfine-tuneが分布シフトで急落する原因が『未知クエリ』より『視覚ドメインシフト』だと特定し、エンティティ注意を経由したルーティングで解決。"
    ),
    "2605.26103v1": (
        "Global SfMとフィードフォワード再構成の合流",
        "古典的Structure-from-Motionとフィードフォワード3D再構成の利点を統合し、SfMの長年の失敗ケースを打開する設計。"
    ),
    "2605.26102v1": (
        "InstructSAM：任意指示でインスタンスセグメント",
        "VLMとSAM3を明示的な『推論-to-インスタンス』クエリ経由でつなぎ、任意の自然言語指示で複数インスタンスを切る統一フレームワーク。"
    ),
    "2605.26100v1": (
        "コード変更を『構造ラベル』として整理するLLM",
        "rename/move/ロジック変更などコードパッチの変更タイプをLLMで識別し、レビュー効率を上げるための構造化ラベリング手法。"
    ),
    "2605.26099v1": (
        "『言語モデルには睡眠が要る』——KVキャッシュをfast weightに固める",
        "長い文脈を周期的にfast weight(SSMブロック)に固めてKVキャッシュを捨てる『睡眠機構』。推論レイテンシは維持したまま、長期文脈タスクの性能を回復できる新パラダイム。",
    ),
    "2605.26097v1": (
        "言語モデルの忘却：容量・最適化・自己生成リプレイ",
        "新タスク学習時の破壊的忘却を、自己生成サンプルをリプレイすることでほぼ解消できることを示す。ただし容量が飽和しているモデルでは忘却が残ることも明らかに。"
    ),
    "2605.26095v1": (
        "舗装損傷をMask R-CNNでピクセル単位評価",
        "細く分岐する亀裂を正確にローカライズし、整備に直結する幾何精度で評価するインスタンスセグメンテーション応用。"
    ),
    "2605.26093v1": (
        "GoBOED：意思決定駆動のベイズ実験計画",
        "従来BOEDの『パラメータ不確実性最小化』ではなく、下流の意思決定品質を直接最大化する目的駆動型BOED。"
    ),
    "2605.26092v1": (
        "OrpQuant：乗算器不要のPower-of-2量子化",
        "幾何的直交残差射影を使ったエッジ向けLLM/ViT量子化。乗算をシフトに置換でき、超低ビット領域での精度劣化を抑える。"
    ),
    "2605.26089v1": (
        "Channel-wise Vector Quantization——パッチでなく『チャネル』を量子化",
        "画像を『パッチごとの離散トークン』ではなく『チャネルごとの離散レベル』として表現する新しいトークン化パラダイム。"
    ),
    "2605.26087v1": (
        "DiscoverPhysics：『見たことない物理』をLLMに発見させる",
        "重力法則を改変した22の人工世界を用意し、LLMエージェントが実験設計・観測・法則仮説の提示までを行えるか評価。記憶でなく真の科学的推論を測るベンチ。"
    ),
    "2605.26086v1": (
        "Claw-Anything：『常時稼働型』パーソナルアシスタントの評価ベンチ",
        "数か月分のユーザー活動・複数バックエンド連携・GUI/CLI横断のリアルなマルチデバイス状態を再現し、常時動くAIエージェントの実力を測る。"
    ),
    "2605.26081v1": (
        "VeriTrace：研究エージェントの『メンタルモデル』を明示的に進化させる",
        "DeepResearchエージェントが暗黙的に持つ中間表象を、解釈更新／逸脱フィードバック／スキーマ改訂の3ループで明示制御する認知グラフ。Qwen3.5-27Bで強baselineを4.22pp改善。"
    ),
    "2605.26079v1": (
        "AIベンチを自動監査するエージェント——四分の一が壊れていた",
        "168本のフロンティアLLMベンチを自動監査し、25.7%以上に環境依存・仕様欠落・正解誤りなど致命的問題があることを発見。ベンチ自体の信頼性に切り込む論文。"
    ),
    "2605.26078v1": (
        "Wasserstein Policy GradientのGlobal Convergence証明",
        "entropy正則化RL目的におけるWasserstein Policy Gradient法のglobal収束を理論的に証明。最適輸送幾何を活用した方策勾配の数理基盤。"
    ),
}

for it in d["sources"]["arxiv"]:
    if it["id"] in arxiv_map:
        t, s = arxiv_map[it["id"]]
        it["title_ja"] = t
        it["summary_ja"] = s

# -------- HN --------
hn_map = {
    "48272984": (
        "AIで『より良いコードを』『より遅く』書く——意外なAIコーディングの本音",
        "Nolan Lawsonのエッセイ。AIに任せると速くなるという神話に対し、『AIを使うことでむしろ熟考が増え、結果として遅く・良くなる』という体験談。HNで上位。"
    ),
    "48278374": (
        "GitHub Actionsダウン障害",
        "GitHub Actions/Pagesが大規模障害。CIに依存する全エコシステムに影響、AI関連の自動化パイプラインも巻き込まれた。"
    ),
    "48266485": (
        "教皇レオ14世『AIは少数の権力者ではなく人類に奉仕すべき』",
        "ローマ教皇レオ14世が初の回勅でAI倫理を中心議題に据えた。少数企業によるAI集中を新たな『非人間化』と警告。"
    ),
    "48270770": (
        "ノルウェー、HuaweiのフラッシュストレージでLLMトレーニング",
        "ノルウェーが2ペタバイトのHuawei製ストレージを大規模LLMトレーニングに使用——西側内部での中国ハード採用例として地政学的に議論を呼ぶ。"
    ),
    "48266906": (
        "オランダ警察、サイバー攻撃支援で800台のサーバ押収",
        "サイバー攻撃インフラの摘発。AI関連の悪用ホスティングも対象に含まれる可能性。"
    ),
    "48268871": (
        "Uber COO『AIトークン消費の正当化が日に日に難しくなっている』",
        "UberのCOOがAIエージェント運用の費用対効果を疑問視。メガテック内部からAI支出への効果検証圧力が初めて公に。"
    ),
    "48277485": (
        "Uber社長『AI支出の正当化が難しくなっている』(追加報道)",
        "同件の追従報道。AI予算が普通のIT支出と同じROI査定に入る転換点との見方。"
    ),
    "48270812": (
        "日本がMach-5ラムジェットエンジン試験に成功",
        "AI直接の話題ではないがHN高評価の日本発技術ニュース。"
    ),
    "48278610": (
        "『外注＋ローカルAI』がフロンティアラボより経済的になる時代",
        "値下がりするローカルモデルとオフショア人材の組み合わせが、フロンティアAPI＋現地エンジニアより経済的になる、という議論。"
    ),
    "48267126": (
        "C拡張・可搬性・代替コンパイラ",
        "C拡張機能の可搬性とPythonエコシステムへの影響を整理した技術記事。AI研究のビルド基盤としても重要。"
    ),
    "48273169": (
        "CVE-2026-28952：ClaudeがmacOS 26.5カーネル脆弱性を発見",
        "AppleがClaudeに発見されたmacOSカーネル脆弱性を公表。AIによる本格的なゼロデイ発見の象徴的事例で、攻撃・防御の双方で議論を呼ぶ。"
    ),
    "48266435": (
        "教皇レオ：少数企業の不透明AIが『新たな非人間化』を生む",
        "回勅の核となる警告部分にフォーカスした続報。"
    ),
    "48273147": (
        "Rust言語のパフォーマンス[PDF]",
        "Rustの性能分析論文。AIインフラの低レベル実装言語として注目される。"
    ),
    "48265745": (
        "GPTに1〜100の数を当てさせる——統計的偏りの可視化",
        "GPTに『1〜100の数を当てよ』と何度も問うと、人間と似た特定の数字に強くバイアスする現象。"
    ),
    "48277537": (
        "AWS API Gatewayの認証を末尾スラッシュ1個で迂回——$12K bounty",
        "trailing slashだけで認証が迂回できる脆弱性をホワイトハットが発見。クラウドAPIゲートウェイ系の認証実装の脆さを示す。"
    ),
    "48282709": (
        "Stack Overflowのフォーラムは死んだ——会社はAIで生きている",
        "AIで質問する文化に置き換わり、Stack Overflowのフォーラム機能は実質死亡。しかし企業としてはAI関連事業で生き延びている、という分析。"
    ),
    "48272393": (
        "Show HN：OpenBrief——ローカル動画ダウンローダ＆要約",
        "オンデバイスで動画を取得して要約する個人開発ツール。"
    ),
    "48278090": (
        "GitHub Actions/Pagesの障害",
        "ステータスページの公式インシデント。Pagesも影響を受けたためGitHub Pagesホスティングの公開ドキュメントが一時的に不安定に。"
    ),
    "48264635": (
        "Show HN：Geomatic——コマンド駆動＋自動微分の幾何スタジオ",
        "コマンドベースで幾何構築でき、autodiffで動く幾何学スタジオ。教育・研究用途。"
    ),
    "48277784": (
        "『AIバブルはインターネットバブルと違う』議論",
        "インターネットバブル時代との比較分析。設備投資集中度や時間軸に焦点。"
    ),
}

for it in d["sources"]["hn"]:
    if str(it["id"]) in hn_map:
        t, s = hn_map[str(it["id"])]
        it["title_ja"] = t
        it["summary_ja"] = s

# -------- Reddit --------
reddit_map = {
    "1tndgv8": (
        "Uber COO『AIトークン消費の正当化が難しい』(r/artificial)",
        "Business Insiderインタビューを巡るRedditでの議論。AI支出の効果検証懐疑論が技術コミュニティでも広がる。"
    ),
    "1tn3e7k": (
        "AI生成画像が『現実より現実的』になる転換点",
        "視覚的に区別不能なAI生成コンテンツが標準になる、という議論。来歴情報の重要性が高まる。"
    ),
    "1tmprdm": (
        "自己教師あり学習でロスが単調でないとき、何で選ぶ？",
        "SSLでハイパパラやアーキを選ぶ実践的方法を聞く投稿。ML実務の悩みどころが見える。"
    ),
    "1tnhnh5": (
        "『METRのAI時間軸グラフ』に重大な誤り——METR批判の議論",
        "AI能力の進歩を時間軸でプロットした有名な『METR Time Horizons』グラフに、複数の重大な統計的誤りが指摘される。今後のAI進歩予測の根拠が揺れる。"
    ),
    "1to2l4c": (
        "[D] ガチのAI研究議論はどこでするべきか",
        "学術的な議論の場がXやRedditで成立しなくなった、という嘆きと提案。"
    ),
    "1tnarvu": (
        "AIエージェントに必要なのは自律性よりも『監査ログ』",
        "エージェントの自律性を増やすより、何をしたか追跡可能にするほうが先だ、という現場の声。"
    ),
    "1tnjhts": (
        "今週のAI関連リポジトリTop10",
        "Trending系まとめ。Claude Codeのスキル・プラグインまわりが目立つ。"
    ),
    "1tnwdss": (
        "EMNLP投稿数すでに11,000本——査読崩壊への危惧",
        "メインNLP会議の投稿激増。査読人材不足とAI生成論文問題が背景に。"
    ),
    "1to0dmn": (
        "AIは『少数の私人が握る認識インフラ』になりつつある",
        "教皇回勅と問題意識が共鳴するコミュニティ議論。"
    ),
    "1tmpfa9": (
        "Claudeの利用上限を一瞬で食い潰す方法",
        "Claudeの長文・ツール利用での上限到達コツ。ユーザ側のコスト管理の難しさを示す。"
    ),
    "1tnvmgt": (
        "WizがAnthropicのコンプライアンスAPIと統合",
        "セキュリティ・コンプラ自動化。Claudeを企業環境に組み込む補助インフラの整備が進む。"
    ),
    "1tndecr": (
        "なぜ今急にデータセンタ需要が爆発しているのか",
        "AIブームによるDC建設ラッシュの背景を整理。Norwayの件など最新事例も。"
    ),
    "1to5v3m": (
        "結局どのAI画像生成サービスが課金する価値ある？",
        "コンシューマ向け画像生成比較。ユーザ評価の現状把握に。"
    ),
    "1tn8uoq": (
        "ICMLワークショップは参加価値あるか[D]",
        "アカデミアの会議参加コスパ議論。"
    ),
    "1tnhfxp": (
        "12.6Mパラメータ・512KB SRAMマイコン上でDCGAN推論",
        "純Cで26秒生成。超低リソース環境での生成AIデモ。"
    ),
    "1tn73ve": (
        "1つだけAIプロバイダに課金するとしたらどれ？",
        "コンシューマAIサブスク選びの実況世論調査。"
    ),
    "1tnn89v": (
        "Aiki——ローカル版Wikipedia RAGシステム",
        "ローカルで動くWikipedia特化RAGの公開。"
    ),
    "1tn1rtk": (
        "NVIDIA Isaac SimでのRL：Isaac Labも併用してる？",
        "ロボティクスRL実務者の現場アンケート。"
    ),
    "1tmq1eb": (
        "MergeNB：Jupyter向けマージコンフリクト解決ツール",
        "VS Code拡張。ノートブックの.ipynbの差分・統合を可視化。"
    ),
    "1tnnaa6": (
        "Conifer——OSSローカル推論ランタイムを作る",
        "個人開発のローカル推論ランタイム公開。"
    ),
}

for it in d["sources"]["reddit"]:
    if str(it["id"]) in reddit_map:
        t, s = reddit_map[str(it["id"])]
        it["title_ja"] = t
        it["summary_ja"] = s

# -------- GitHub --------
github_map = {
    "rohitg00/ai-engineering-from-scratch": (
        "AI Engineering を一から学ぶ大型カリキュラム",
        "AIエンジニアリングを土台から学ぶための包括的な公開教材。プロダクション運用までカバー。"
    ),
    "affaan-m/ECC": (
        "ECC：エージェントハーネスを丸ごと最適化するシステム",
        "スキル・直感・メモリ・セキュリティを横断して扱う統合ハーネスのOSS実装。今週の『ハーネス拡張』論文の文脈に合致。"
    ),
    "anthropics/knowledge-work-plugins": (
        "Anthropic公式：ナレッジワーク向けプラグイン集",
        "Claude Code向けに、ナレッジワーカーが業務で使えるプラグインをまとめたOSSリポジトリ。"
    ),
    "Leonxlnx/taste-skill": (
        "Taste-Skill——AIに『良いセンス』を持たせるスキル",
        "Claude向けのスキルファイルで、生成出力の『つまらなさ』を抑える狙い。バイラル系。"
    ),
    "DigitalPlatDev/FreeDomain": (
        "DigitalPlat FreeDomain：無料ドメインプロジェクト",
        "AI直接ではないがインフラ系で急上昇しているOSS。"
    ),
    "mukul975/Anthropic-Cybersecurity-Skills": (
        "AIエージェント用サイバーセキュリティスキル754個",
        "MITRE ATT&CKなど5フレームワークにマップされた構造化セキュリティスキル集。Claude Code向けの実務応用。"
    ),
    "hardikpandya/stop-slop": (
        "AI生成文章特有の癖を除去するスキル",
        "geohotの『Eternal Sloptember』議論と呼応する、文章スロップ撲滅スキル。"
    ),
    "thedotmack/claude-mem": (
        "claude-mem：エージェントの永続メモリ層",
        "Claudeセッションを跨いだ永続コンテキストを実現。今週の『メモリは外部状態』論調と一致。"
    ),
    "twentyhq/twenty": (
        "Twenty：AI時代のSalesforceオルタナティブ",
        "SalesforceのオープンソースAI志向代替。"
    ),
    "Open-Dev-Society/OpenStock": (
        "OpenStock：OSSのリアルタイム株価プラットフォーム",
        "Bloomberg/有料ターミナルのOSS代替を目指す。"
    ),
}

for it in d["sources"]["github"]:
    if it.get("full_name") in github_map:
        t, s = github_map[it["full_name"]]
        it["title_ja"] = t
        it["summary_ja"] = s

# -------- Blogs --------
blog_map = {
    "https://openai.com/index/grupo-folha-grupo-uol-partnership": (
        "OpenAI、ブラジル最大手メディアGrupo Folha/UOLとコンテンツ提携",
        "南米最大級のニュースグループとの戦略的コンテンツ提携。学習データと最新情報配信の両面でブラジル市場を押さえる動き。"
    ),
    "https://huggingface.co/blog/agent-glossary": (
        "『ハーネス』『スキャフォールド』など、AIエージェントの用語を整理",
        "言葉が乱立するエージェント周辺の概念をHugging Faceが整理。今週のarXiv『Scaling the Harness』とも噛み合う。"
    ),
    "https://huggingface.co/blog/nvidia/nemotron-labs-diffusion": (
        "NVIDIA Nemotron Labs：拡散LMで『光速テキスト生成』に挑む",
        "NVIDIAが拡散言語モデルNemotron Diffusion LMを推進。自己回帰生成に比べ大幅な並列性能で、リアルタイム生成の実用化を狙う。"
    ),
    "https://blog.google/innovation-and-ai/technology/ai/io-2026-dialogues-recap/": (
        "Google I/O 2026 Dialoguesステージのまとめ",
        "Geminiやエージェント関連セッションのハイライト集。"
    ),
    "https://huggingface.co/blog/Dharma-AI/specialization-beats-scale": (
        "『スケールより専門化が勝つ』——AI調達の戦略変数",
        "汎用フロンティアモデルに頼るより、用途特化モデルを選んだほうが調達効率が良い場面が増えていることを示す分析。"
    ),
    "https://openai.com/index/virgin-atlantic": (
        "Virgin AtlanticがCodexで開発を加速",
        "航空エンタープライズ事例。Codexによるコード生産性向上の社内事例。"
    ),
    "https://openai.com/index/gartner-2026-agentic-coding-leader": (
        "OpenAI、Gartnerの『エンタープライズコーディングエージェント』Leaderに選出",
        "Codex系のエンタープライズ評価でリーダーポジション。Claude Code/Cursor勢との競合構図が明確化。"
    ),
    "https://openai.com/index/adventhealth": (
        "AdventHealthがOpenAIで『全人的ケア』を推進",
        "米大手医療法人での運用事例。電子カルテ業務効率化の枠を超えた患者ケア統合の試み。"
    ),
    "https://blog.google/innovation-and-ai/infrastructure-and-cloud/global-network/missouri-programs/": (
        "Googleがミズーリ州にAIコミュニティ投資",
        "地域経済とAI教育・職業訓練を結ぶ投資パッケージ発表。"
    ),
    "https://blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/": (
        "Google I/O 2026：発表100連発まとめ",
        "Gemini系・Workspace・Android・Beam・検索AI Modeまで横断するI/Oの全発表サマリ。"
    ),
    "https://blog.google/innovation-and-ai/models-and-research/google-research/google-beam-group-meetings/": (
        "Google Beamに『グループ会議』実験——立体テレプレゼンスの次の一手",
        "1対1主体だったGoogle Beamがグループミーティングに対応する実験を開始。"
    ),
    "https://openai.com/index/model-disproves-discrete-geometry-conjecture": (
        "OpenAIのモデルが離散幾何の中心予想を『反証』した",
        "AIが既存予想を実際に反証するに至った——AIが数学の新発見に踏み込む象徴的事例。手法はモデルがアイデアを出し人間が検証する協働型。"
    ),
    "https://openai.com/index/ramp": (
        "Ramp、Codexでコードレビューを加速",
        "FinTechのRampでのCodex導入事例。コードレビュー効率化の実数値が公開された。"
    ),
    "https://openai.com/index/the-next-phase-of-education-for-countries": (
        "OpenAI『Education for Countries』の次フェーズ",
        "国家レベルでのOpenAI教育プログラム拡大。各国とのパートナーシップが本格化。"
    ),
    "https://openai.com/index/introducing-openai-for-singapore": (
        "OpenAIがシンガポール向けプログラムを開始",
        "シンガポール政府との戦略連携。アジア拠点戦略の中核。"
    ),
}

for it in d["sources"]["blogs"]:
    if it["url"] in blog_map:
        t, s = blog_map[it["url"]]
        it["title_ja"] = t
        it["summary_ja"] = s

# -------- Highlights --------
def hn_item(id_):
    return next(it for it in d["sources"]["hn"] if str(it["id"]) == str(id_))

def reddit_item(id_):
    return next(it for it in d["sources"]["reddit"] if str(it["id"]) == str(id_))

def blog_item(url):
    return next(it for it in d["sources"]["blogs"] if it["url"] == url)

def arxiv_item(id_):
    return next(it for it in d["sources"]["arxiv"] if it["id"] == id_)

highlights = []

# 1. OpenAI model disproves discrete geometry conjecture - biggest news of the day
i = blog_item("https://openai.com/index/model-disproves-discrete-geometry-conjecture")
highlights.append({
    "source": "blog",
    "title": i["title"],
    "title_ja": "OpenAIモデルが離散幾何の『中心予想』を反証——AIが本物の数学的発見に踏み込む",
    "url": i["url"],
    "hot_take_ja": "OpenAIが、離散幾何学で長年信じられてきた中心予想をモデルが反証した、と公表した。『AIが既存予想を強化する』『AIが定理を再証明する』の段階を越え、『AIが反例を見つけて予想を倒す』段階に達したという意味で、過去のAlphaProofやAlphaGeometryから一歩進んだマイルストーンだ。研究者・モデル・形式検証ツールが組んだ協働型ワークフローで成立した点も重要で、これは『AI for Math』が学術界に定着するシナリオを後押しする。",
    "detail_ja": "OpenAIは自社のフロンティアモデルが離散幾何学の長年の中心予想を反証した、と発表した。具体的には、モデルが手がかり・候補となる反例構成を生成し、研究者がそれを精査・形式化したうえで、コンピュータによる厳密検証を通すという協働パイプラインを取った。鍵となる進歩は2点。第一に『反証』であること——既知定理の再証明や定理化されているものの確認ではなく、信じられていた予想を倒すには、構造的に新しい反例を発見しなければならない。第二に、結果が形式検証で裏付けられていることで、AI数学の最大の弱点だった『もっともらしいが嘘の証明』を回避できている。技術的にはAlphaProof / AlphaGeometryの系譜だが、OpenAI側がこの種の発表に踏み込んだことは、学術コミュニティの受容度・査読フローへの影響として大きい。すぐ実応用に直結するわけではないが、(1)AIを研究プロセスにどう組み込むかの規範例ができたこと、(2)『AIは記憶しかしてない』言説への強い反論材料になること、(3)競争相手のDeepMind/Anthropicも同種の発表で応酬すると見られること、の3点で来年のAI for Science議論を方向づける一発になる。",
    "detail_en": "OpenAI announced that one of its frontier models has disproved a long-standing central conjecture in discrete geometry. Importantly, the result was obtained through a human-AI collaboration: the model generated candidate counterexample constructions and reasoning, human researchers refined and formalized them, and the final disproof was verified by a formal proof checker. Two things make this a notable milestone. First, it is a disproof, not a re-derivation — overturning a long-believed conjecture requires finding genuinely new structure, which is much harder than confirming known results. Second, the chain ends in a formally checked artifact, which closes the biggest credibility gap in AI math (the 'plausible but wrong' problem). Technically the work is in the AlphaProof / AlphaGeometry lineage, but the fact that OpenAI is now publishing this kind of headline result matters for academic uptake. Even though the math itself is not directly applicable engineering, the broader implications are large: (1) it sets a norm for how AI is woven into the research process, (2) it is strong evidence against the 'LLMs just memorize' narrative, and (3) it will pressure DeepMind and Anthropic to make competing claims, shaping the 'AI for Science' conversation for the next year.",
    "key_points_ja": [
        "OpenAIモデルが離散幾何の中心予想を反証",
        "AIが反例構成を生み、人間と形式検証ツールが確認",
        "再証明ではなく『予想を倒した』のが質的進歩",
        "形式検証で『もっともらしい嘘の証明』を回避",
        "AI for Mathの学術受容に影響する象徴的事件"
    ],
    "key_points_en": [
        "OpenAI model disproves a central conjecture in discrete geometry",
        "Model generated counterexample constructions, humans + formal checker verified",
        "Qualitative jump: disproving a conjecture, not re-deriving theorems",
        "Formal verification closes the 'plausible but wrong' credibility gap",
        "Pressures DeepMind/Anthropic to respond; reshapes AI for Science"
    ]
})

# 2. CVE-2026-28952 - Claude found a macOS kernel vuln
i = hn_item("48273169")
highlights.append({
    "source": "hn",
    "title": i["title"],
    "title_ja": "ClaudeがmacOS 26.5のカーネル脆弱性を発見——CVE-2026-28952としてApple公式公表",
    "url": i["url"],
    "hot_take_ja": "AppleがmacOS 26.5のセキュリティアップデートに、Claudeが発見したカーネル脆弱性CVE-2026-28952を正式にクレジット入りで掲載した。OSベンダがAIをCVEのfinderとして公式記載するのは依然珍しく、AIによる本格的なゼロデイ発見が研究実験から運用フローに昇格した瞬間だ。攻撃側の参入障壁が下がる一方、防御側も同じ武器を持つフェーズに入る。",
    "detail_ja": "AppleのmacOS 26.5セキュリティリリースノートに、AIモデルClaudeを発見者としてクレジットしたカーネル脆弱性CVE-2026-28952が掲載された。ベンダの公式ページにAIが脆弱性発見者として記載されること自体は前例があるものの、Apple規模・カーネル領域・OS核心の脆弱性という3点が揃った事例は依然稀。実務的なインパクトは3つ。(1)AIによるバグ発見の運用化：脆弱性発見が研究プロジェクトからエンジニアリングの一部に降りてきた。(2)非対称性の変化：これまで攻撃側はファジング＋人間の経験で十分強かったが、AIによる仕様理解＋経路探索が組み合わさることで、防御側も同じ武器を持たないと劣勢になる。(3)責任の問題：『AIが発見した』脆弱性の責任・賞金・帰属について、業界の取り決めが追い付いていない。同日のAWS API Gateway認証迂回($12K bounty)とあわせ、『AIで攻撃発見』『AIで防御発見』が同じ週に並んだのは象徴的。SOCやベンダのレッドチーム運用は、AIを前提に組み直しが進む。",
    "detail_en": "Apple's macOS 26.5 security release notes credit Anthropic's Claude with the discovery of a kernel-level vulnerability, CVE-2026-28952. While AI-credited CVEs are no longer unprecedented, the combination here is still rare: Apple-scale, kernel-domain, and an OS-core vulnerability. Three practical implications. (1) Operationalization: AI-driven bug discovery is moving from research projects into normal engineering pipelines. (2) Asymmetry shift: attackers have been strong with fuzzing plus human intuition for years, but AI's ability to internalize complex specs and reason about reachable paths means defenders now must use the same tools or fall behind. (3) Norms: attribution, bounties, and responsibility for 'AI-found' vulnerabilities are still ad hoc, and the industry will need to formalize them. Combined with the same-day $12K AWS API Gateway trailing-slash bypass, this week is a snapshot of AI being applied symmetrically to both attack-surface discovery and audit. SOC and red-team workflows will get redesigned around AI as a default assumption.",
    "key_points_ja": [
        "macOS 26.5にCVE-2026-28952をClaudeがfinderとして掲載",
        "Apple規模＋カーネル領域での公式AIクレジットは依然レア",
        "AIによる脆弱性発見が運用フローに昇格する分水嶺",
        "攻撃・防御の非対称性が再定義される",
        "同日のAWS API Gateway迂回と合わせ象徴的な一週間"
    ],
    "key_points_en": [
        "Apple credits Claude as finder of kernel CVE-2026-28952 in macOS 26.5",
        "Apple-scale, kernel-domain AI-credited CVE is still rare",
        "Marks AI bug discovery moving from research to ops",
        "Attack/defense asymmetry being redefined by AI capability",
        "Paired with the $12K AWS API Gateway bypass — defining week"
    ]
})

# 3. METR time horizons graph - methodological pushback
i = reddit_item("1tnhnh5")
highlights.append({
    "source": "reddit",
    "title": i["title"],
    "title_ja": "AI能力進歩の『時間軸』予測グラフ(METR)に重大な統計誤り——AI予測ナラティブを揺さぶる批判",
    "url": i["url"],
    "hot_take_ja": "AI能力が指数的に伸びている根拠としてあちこちで引用されていたMETRの『時間軸（Time Horizons）』グラフに、複数の統計的誤りが指摘された。AGI到達時期や投資判断の前提に使われてきた図なので、影響は単なる学術論争に留まらない。データ・選定・回帰の前提が崩れると、AI進歩を線形外挿してきた言説そのものが再評価対象になる。",
    "detail_ja": "METRが公開した『AI Time Horizons』グラフは、AIモデルが解ける『人間がかかる時間』を縦軸に置き、AI能力の指数的進歩を主張する図として広く引用されてきた。Reddit上で、データセレクション(ベンチタスクの偏り)、課題分布の対数変換と回帰の解釈、信頼区間の扱い、観察期間の打ち切り、などに重大な誤りがあると指摘する詳細な批判がまとめられた。実務的な影響は二段階。第一に、研究者コミュニティが頻繁に引用してきた図が揺らぐと、論文・スライド・投資家ピッチでの『AIは指数的に進歩している』という主張のエビデンス基盤が薄くなる。第二に、政策議論（AGIへの時間軸を前提にした規制提言）にも影響する。重要なのは、批判は『AIの進歩が止まった』と主張しているのではなく、『進歩の形と速度を線形外挿で語ること』に再現性のある測定基盤が欠けている、と指摘している点。今後はベンチマーク監査(同日に公開された『Automated Benchmark Auditing』論文の問題意識とも合致)とより厳密な能力評価が、定量予測の前提になる流れだ。",
    "detail_en": "METR's widely cited 'AI Time Horizons' graph — which plots the time it would take a human to complete the hardest task an AI can do, used as evidence of exponential AI progress — has been challenged in a detailed Reddit post for multiple statistical errors. The critique covers benchmark selection bias, the interpretation of the log-transformed regression, treatment of confidence intervals, and time-window truncation. The implications come in two layers. First, the graph has been quoted heavily in research talks, investor pitches, and policy briefings as the canonical evidence that AI capability is improving exponentially; if its statistical foundations are shaky, that line of argument loses some weight. Second, policy debates that assume specific AGI timelines (e.g. multi-year regulatory roadmaps) lean on graphs like this. Crucially, the critique does not argue that AI progress has stopped — it argues that we lack reproducible measurement infrastructure to claim a particular curve shape. The same week's 'Automated Benchmark Auditing' arXiv paper, which found critical issues in 25.7% of frontier benchmarks, reinforces the same theme: claims about AI capability need more rigorous measurement before they support quantitative extrapolation.",
    "key_points_ja": [
        "METR『AI時間軸』グラフに統計的誤りを多数指摘",
        "ベンチ選定・回帰・信頼区間の扱いに問題",
        "『AIは指数的進歩』議論のエビデンス基盤が揺らぐ",
        "AGI到達時期前提の政策・投資判断にも影響",
        "同日の自動ベンチ監査論文(25.7%の問題発見)とも共鳴"
    ],
    "key_points_en": [
        "Numerous statistical errors found in METR's AI Time Horizons graph",
        "Issues span benchmark selection, regression, CIs, truncation",
        "Weakens the canonical 'exponential AI progress' evidence",
        "Affects AGI-timeline-based policy and investment narratives",
        "Aligns with same-week ABA paper finding 25.7% broken benchmarks"
    ]
})

# 4. Language Models Need Sleep - new mechanism
i = arxiv_item("2605.26099v1")
highlights.append({
    "source": "arxiv",
    "title": i["title"],
    "title_ja": "『言語モデルにも睡眠が要る』——KVキャッシュを永続重みに固める新パラダイム",
    "url": i.get("url", f"https://arxiv.org/abs/{i['id'].rstrip('v1234567890').rstrip('v')}"),
    "hot_take_ja": "Transformerの長文処理は注意機構のコストで詰む。本論文は、推論を一旦止めて『睡眠』中に最近の文脈をSSMブロックの高速重みに圧縮し、KVキャッシュを捨てる、という生物学的に魅力的な発想を実装し動かしてみせた。回数を増やすほど性能が伸びる、というスケーリング挙動も観測され、長文エージェントの設計原理を変える可能性がある。",
    "detail_ja": "Transformer型LLMは長期文脈タスクで、注意計算がコンテキスト長に対し劣スケールするせいで詰まる。本論文は『睡眠的固定化(sleep-like consolidation)』機構を提案する：定期的に推論を停止し、それまで蓄積した文脈をN回のオフラインの再帰パスでSSMブロック内のfast weightsに圧縮し、その後KVキャッシュをクリアする。学習済みのローカル更新則によりfast weightsが更新されるため、起きている間(=wake-time prediction)のレイテンシは保たれ、追加計算は睡眠フェーズに押し込まれる。検証はセルラーオートマトン・マルチホップグラフ検索などの合成課題と、実用的な数学推論タスクに実施。通常のTransformerやSSM-attentionハイブリッドが落ちるところで本手法は機能し、しかも『睡眠パスN回を増やすと性能が伸びる』というスケーリングが見られた。これは(a)エージェントの長期メモリ設計に新しい原理を与え、(b)『推論で重み更新せよ』というtest-time training/fast weight系研究と融合する。短期的にはプロダクション用途より研究方向の影響が大きいが、エージェントが長時間動き続ける時代に向けて『AIにも休息サイクルを設計する』という発想を業界に持ち込んだ点でインパクトがある。",
    "detail_en": "Transformer-based LLMs struggle on long-horizon tasks because their attention mechanism scales poorly with context length. This paper proposes a 'sleep-like consolidation' mechanism: the model periodically pauses and, during sleep, performs N offline recurrent passes over recently accumulated context, updating fast weights inside SSM blocks via a learned local rule, then clears its key-value cache. Wake-time prediction latency is preserved while extra compute is pushed to the sleep phase. Evaluation covers controlled synthetic tasks (cellular automata, multi-hop graph retrieval) and a realistic math reasoning task on which both regular transformers and SSM-attention hybrids fail. The method works there, and crucially it shows a scaling property: increasing the number of sleep passes raises performance. The paper sits at the intersection of test-time training and fast-weight literatures and offers a new design principle for long-horizon agent memory. The short-term impact is more on research direction than production deployment, but framing 'AI needs rest cycles' explicitly is a memorable contribution that will likely seed more concrete agent architectures in the next year.",
    "key_points_ja": [
        "推論を止めKVキャッシュをSSMのfast weightに圧縮",
        "睡眠フェーズで追加計算、wake時のレイテンシは維持",
        "通常Transformerが落ちる長期文脈タスクで機能",
        "『睡眠回数を増やす』ことでさらに性能が伸びる",
        "長時間動くエージェントのメモリ設計を変える可能性"
    ],
    "key_points_en": [
        "Pause inference and consolidate KV cache into SSM fast weights",
        "Extra compute pushed to sleep, wake-time latency preserved",
        "Works on long-horizon tasks where standard transformers fail",
        "Performance scales with number of sleep passes",
        "New design principle for long-running agent memory"
    ]
})

# 5. Nemotron-Labs Diffusion LM - production-grade diffusion text
i = blog_item("https://huggingface.co/blog/nvidia/nemotron-labs-diffusion")
highlights.append({
    "source": "blog",
    "title": i["title"],
    "title_ja": "NVIDIA Nemotron Diffusion LM——自己回帰を超える『光速テキスト生成』への本気の挑戦",
    "url": i["url"],
    "hot_take_ja": "NVIDIAが拡散言語モデルNemotron Diffusion LMを公開。自己回帰LLMの一文字ずつ出すボトルネックを並列生成で吹き飛ばす設計で、レイテンシ・スループットの常識を書き換えに来ている。今週はarXivの『Looped Diffusion LM』論文もあり、拡散LMが研究から本気のプロダクト戦線に出てきた週となった。",
    "detail_ja": "NVIDIAがHugging Face上で公開したブログでNemotron-Labs Diffusion Language Modelsを発表した。中心メッセージは『拡散LMで光速テキスト生成に近づける』。自己回帰モデルは1トークンずつ逐次的に予測する仕組み上、レイテンシが文長に比例し、ストリーミングや高スループット推論で本質的に不利だった。拡散LMは『マスクされた全トークンを並列に予測し、反復的にrefineする』方式で、ハードウェアの並列性と相性が良い。Nemotronはこの設計でレイテンシとスループットの両方を従来比で大幅改善する、と主張する。意義は3つ。(1)NVIDIAが自社推論プラットフォーム最適化と拡散LMを統合してきた——GPU上の戦略的Show of Force。(2)同時期のarXiv『Looped Diffusion Language Models』が、層をループするだけで拡散LMがFLOPSベースで自己回帰モデルを超える性能を出せると報告しており、研究面でも追い風。(3)エージェント時代において『大量推論を低レイテンシで』の需要が爆発する中、拡散LMが本物の選択肢に上がってきた。OpenAI/Anthropic/Googleが軒並み自己回帰モデルで構築している現状に対し、NVIDIAは『推論経済学そのものを変える』軸で殴り込んできた格好だ。",
    "detail_en": "NVIDIA published a Hugging Face blog announcing its Nemotron-Labs Diffusion Language Models, with the explicit framing of moving toward 'speed-of-light text generation'. Autoregressive LLMs predict one token at a time, so latency scales with sequence length and parallel hardware is underutilized. Diffusion language models instead refine all tokens in parallel through iterative denoising, mapping much more naturally onto GPU parallelism. NVIDIA claims significant gains in both latency and throughput versus autoregressive baselines on its hardware. Three points of significance. (1) NVIDIA is now actively co-designing inference platforms with diffusion LMs — a strategic GPU-side move. (2) The same-week arXiv 'Looped Diffusion Language Models' paper shows that simple architecture tricks let masked diffusion LMs match same-size autoregressive models with up to 3.3× fewer training FLOPs — research tailwind. (3) In an agent-heavy era where bulk inference at low latency is the binding constraint, diffusion LMs are now a credible alternative — not just a research curiosity. OpenAI, Anthropic, and Google have built their stacks on autoregressive models; NVIDIA's bet is to change the inference economics underneath them.",
    "key_points_ja": [
        "NVIDIAが拡散LM『Nemotron Diffusion』を発表",
        "並列生成で自己回帰LMのレイテンシ壁を破壊",
        "GPU並列性と相性がよく推論経済学を変える",
        "同日のarXiv『Looped Diffusion LM』が研究面で追い風",
        "エージェント時代の大量推論需要を狙う戦略"
    ],
    "key_points_en": [
        "NVIDIA unveils Nemotron Diffusion Language Models",
        "Parallel denoising breaks the autoregressive latency wall",
        "Maps naturally onto GPU parallelism, shifts inference economics",
        "Same-week arXiv 'Looped Diffusion LM' adds research tailwind",
        "Targets the agent-era demand for bulk low-latency inference"
    ]
})

d["highlights"] = highlights

with open(OUT, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f"Wrote {OUT}")
print(f"Highlights: {len(highlights)}")
