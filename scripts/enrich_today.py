#!/usr/bin/env python3
"""Enrich raw-2026-05-24.json with Japanese summaries and highlights."""
import json
from pathlib import Path

DATE = "2026-05-24"
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / f"raw-{DATE}.json"
OUT = ROOT / "data" / f"{DATE}.json"

with open(RAW) as f:
    d = json.load(f)

# -------- HN --------
hn_map = {
    "48247208": (
        "『The Art of Money Getting』——P.T.バーナム 1880年の蓄財論",
        "サーカス王P.T.バーナムの古典的な蓄財・処世訓を再紹介。AIでも何でも『稼ぎ方は時代を超えて同じ』という観点で読まれ、HNでも好評。"
    ),
    "48247876": (
        "Ouraリング、政府からのユーザーデータ要求を認める",
        "睡眠・心拍データを集めるOuraが、政府からのデータ提供命令を受けていると認めた。トランスペアレンシーレポートを出すかは未定で、ウェアラブルが個人の生体データを保持するリスクを浮き彫りに。"
    ),
    "48256953": (
        "DeepSeek Reasonix：高キャッシュ・低コストの純正コーディングエージェント",
        "DeepSeekがネイティブコーディングエージェント『Reasonix』を発表。プロンプトキャッシュの徹底活用で、Claude Code/Codex対抗の超低コストを謳う。"
    ),
    "48248775": (
        "イタリア、空中給油機をAirbus A330へ刷新——NATOアラインで",
        "イタリアが米Boeing KC-46からAirbus A330 MRTTへ給油機を切り替え。NATO側装備の同質化が進む防衛トレンド。"
    ),
    "48258684": (
        "AIチップのコスト、メモリが約2/3にまで膨張",
        "Epoch AIの分析で、AIアクセラレータの部品コストに占めるメモリ（HBM等）の比率が約2/3に到達。GPUダイ本体よりメモリのほうが原価支配的になり、HBM寡占の構造リスクを示す。"
    ),
    "48246889": (
        "『Making deep learning go brrrr』再ブーム——基礎からの高速化指南",
        "Horace He（PyTorch開発者）の2022年の名解説が再注目。Compute/Memory/Overheadのどこに律速されているかを見抜き、適切に対処するDLパフォーマンス入門の決定版。"
    ),
    "48257410": (
        "DeepSeek、フラッグシップAIモデルを75%恒久値下げへ",
        "BloombergによるとDeepSeekは旗艦モデルを期間限定ではなく恒久的に75%値下げ。米中フロンティアの価格競争がさらに加速し、推論コストの底が抜けつつある。"
    ),
    "48246735": (
        "DHS、グリーンカード発行をほぼ停止",
        "Cato Instituteの分析。米国土安全保障省が永住権発行を実質的にほぼ停止したと指摘。テック企業のH-1B→GC変換ルートにも影響。"
    ),
    "48257980": (
        "『AIウォッシング』——PR会社がこぞって『AI企業』にリブランド",
        "ガーディアン報道。本質的にAIをほとんど使っていないPR・コンサル各社が、社名やパッケージを『AI〜』に改名するムーブメントが加速。ドットコム前夜と酷似。"
    ),
    "48248014": (
        "z386：オリジナルマイクロコードで作るオープンソース80386",
        "Intel 80386の純正マイクロコードをベースに、FPGAで完全動作する386互換CPUを設計。レトロコンピューティング愛好家から喝采。"
    ),
    "48250980": (
        "Air France＆Airbus、2009年事故で過失致死有罪",
        "AF447便事故（2009年大西洋墜落）について、フランスの控訴審がエールフランスとAirbusを過失致死で有罪と判断。航空×責任分担の歴史的判決。"
    ),
    "48256912": (
        "Constraint Decay：LLMエージェントはバックエンドコード生成で『制約を忘れる』",
        "arXiv論文。LLMエージェントが長いコンテキスト・複数ファイル・複数往復のバックエンド生成で、初期に与えた制約を段階的に忘却して破綻する『Constraint Decay』現象を定量化。エージェント信頼性に直接刺さる結果。"
    ),
    "48254345": (
        "『Fuck you, Bambu』——3Dプリンタ業界をひっくり返した個人メッセージ",
        "Bambu Labが個人開発者にDMでAGPL違反を恫喝、それが流出して逆にBambu側のオープンソース利用が問われる事態に。3Dプリンタのオープン文化を揺るがす事件。"
    ),
    "48259784": (
        "『Claudeはあなたのアーキテクトではない』——役割を分けろ",
        "Claude Codeを『設計担当』にしてしまうと、辻褄合わせのコードが量産されアーキテクチャが壊れる、という現場ブログ。LLMには『実装』をやらせ、設計判断は人間が握れと主張。"
    ),
    "48257058": (
        "Microsoft 6502 BASIC、ついにオープンソース化",
        "Apple II、Commodore、Atariなどに搭載されたMS製の歴史的6502 BASICインタプリタがついに公式OSS化。レトロ計算史にとっての大ニュース。"
    ),
    "48256565": (
        "Apple PICo：学習型画像圧縮で『本当に効くもの』を整理",
        "AppleのML研究『PICo』。学習ベース画像コーデックの実装観点で、知覚品質・速度・ハードウェア親和性を本気で取りに行く方向性を提案。"
    ),
    "48248256": (
        "『Megaladon』攻撃、GitHubリポジトリ5,500本以上を汚染",
        "サプライチェーン攻撃『Megaladon』が、GitHubリポジトリ5500件以上を改変。スター付きの主要リポも被害で、Actionsやpre-commit経由でCIに侵入する手口。"
    ),
    "48250198": (
        "NeuralNote：オーディオ→MIDIをローカルで",
        "オーディオファイルやマイク入力をニューラルネットでMIDIに変換するOSSプラグイン。DTMer向けでHN注目。"
    ),
    "48251864": (
        "Anthropic、AIが『悪役を演じる』原因はディストピアSF学習データだと指摘",
        "Anthropicの研究によると、HALやスカイネットなど『AIは敵』というSFを大量に学習したため、ロールプレイ時にモデルが悪役の言動を再現しがちだという。学習コーパスの『物語バイアス』問題を露呈。"
    ),
    "48251243": (
        "コメディアンJimmy Carr『AIについてみんな間違っている』",
        "Jimmy CarrがAIに対する世間の議論の偏りをコメディ的に語る動画。HNでもバズり中。"
    ),
}

for it in d["sources"]["hn"]:
    if it["id"] in hn_map:
        t, s = hn_map[it["id"]]
        it["title_ja"] = t
        it["summary_ja"] = s

# -------- Reddit --------
reddit_map = {
    "1tlcscq": (
        "Meta退職者、社内向けに辛辣な反AIビデオを残す——大規模レイオフ下で",
        "Mother Jones独占。大規模レイオフ中のMetaを去る社員が、AI推進と人員削減を皮肉る内部向け動画を投稿。Bosworth/Frenk体制への内輪の反発が表面化。"
    ),
    "1tlig93": (
        "NHSの患者データ、Palantirと外部委託先に『無制限』アクセスを許可——Amnestyが告発",
        "Amnesty Internationalによると、英NHSが米Palantirほか外部ベンダに、識別可能なNHS患者情報への無制限アクセスを認めていた。AI×医療データガバナンスの最悪のケース。"
    ),
    "1tlp9gz": (
        "『Elon、もうGrokを流行らせようとするな』——政府職員が一番嫌う",
        "Verge記事。政府職員へのアンケートでGrokが最も嫌われるアシスタントに。AI政治色がプロダクト採用を直接食う構図。"
    ),
    "1tmawv5": (
        "Papers With Code、復活後の新機能ハイライト",
        "閉鎖危機を経て再起動したPapers With Codeの、新機能アップデート第1弾。OSS実装と論文の紐付けを再強化。"
    ),
    "1tlh2gh": (
        "OpenAI、44.5万ドルの研究者を募集——求める素質は『タステフル・戦略的』",
        "OpenAIのセーフティチーム求人、年収約44.5万ドル。明示スキルより『美的・戦略的判断力』が中心の人物像で、AGI時代の研究者像のあいまいさを象徴。"
    ),
    "1tlzy43": (
        "VLM vs OCR：長文ドキュメントQAでどちらが強い？",
        "図表・画像・テーブルを含む長文ドキュメントQAについて、Vision LLMと従来OCRパイプラインのトレードオフを実務目線で議論するスレッド。"
    ),
    "1tkuu66": (
        "COLM 2026 レビュー結果に阿鼻叫喚",
        "COLM 2026のレビュー返却を巡る研究者の悲喜こもごも。LLM時代の査読品質の議論も。"
    ),
    "1tlpv9g": (
        "『AIトレーニングは思っているよりずっと身近』",
        "個人開発者によるエッセイ。コンシューマGPUと公開データセットだけでも実用的なファインチューニングが現実的、という現場の声。"
    ),
    "1tmb7c6": (
        "退役者がMS PaintをAIに見せたら——AIが存在しない美術運動を捏造、Googleもそれを『本物』扱い",
        "ユーザーがMS PaintのラクガキをAIに講評させたところ、AIが架空のアートムーブメントを『これに属する』と命名・解説。さらにGoogle検索のAIサマリーがその架空ムーブメントを実在扱いし始めた、というハルシネーション伝播事例。"
    ),
    "1tltq6b": (
        "『AIの未来について、誰を信じればいい？』",
        "Yann LeCunとSam Altmanで真逆を言うAI業界の言説、何を信じるべきかというユーザーの率直な問い。"
    ),
    "1tlna8o": (
        "コンサル現場の機械学習パイプライン、遅すぎ問題",
        "受託MLパイプラインが遅すぎてビジネスに刺さらない、というコンサル現場の愚痴／知恵スレ。"
    ),
    "1tldakl": (
        "AIの『椅子取りゲーム』——順位は数カ月で入れ替わる",
        "AI業界のトップモデル序列がGPT→Claude→Gemini→……と数カ月で交代する『椅子取りゲーム』化を論評。"
    ),
    "1tme23u": (
        "マルチエージェントの失敗は『プロンプトの問題』ではなく『組織設計の問題』",
        "マルチエージェントのループ失敗は、プロンプトを直すよりも『役割分担・責任範囲』を再設計する方が効くという視点の投稿。"
    ),
    "1tl7f8z": (
        "d_state=1のMamba1派生『SM1』を純PyTorchで実装、Blackwell対応",
        "Mamba1のd_state=1派生『SM1』を、CUDAカーネル無しの純PyTorchで実装。Blackwell GPUでの効率比較も。"
    ),
    "1tmkupv": (
        "『AI画像生成、結局みんな何使ってる？』",
        "Midjourney / Imagen / SD / Fluxなど、現時点での個人ユーザの選好アンケートスレ。"
    ),
    "1tm92gy": (
        "EdgeModel：エッジ向けLLMをまとめる試み",
        "オンデバイスLLMをまとめて評価・配布するプロジェクト『EdgeModel』の紹介。"
    ),
    "1tm3vba": (
        "『データサイエンスを深追いせず Applied AI Engineer になりたい』",
        "MLOps／LLM運用寄りのキャリアを目指したい人向けのロードマップ相談。"
    ),
}

for it in d["sources"]["reddit"]:
    if it["id"] in reddit_map:
        t, s = reddit_map[it["id"]]
        it["title_ja"] = t
        it["summary_ja"] = s

# -------- GitHub --------
github_map = {
    "colbymchenry/codegraph": (
        "codegraph：エージェント向けにコードを事前インデックス化するナレッジグラフ",
        "Claude Code / Codex / Cursor / OpenCode等が共通で使える、ローカル100%のコードナレッジグラフ。事前にコード構造をグラフ化しておくことで、毎回のツール呼び出しとトークン消費を大幅削減。本日急上昇。"
    ),
    "multica-ai/andrej-karpathy-skills": (
        "andrej-karpathy-skills：KarpathyのLLM落とし穴をCLAUDE.mdに凝縮",
        "Karpathyが指摘してきたLLMコーディングの典型的失敗パターンを1つのCLAUDE.mdに集約。Claude Code等のエージェント挙動を1ファイルで矯正でき、引き続き急成長。"
    ),
    "rohitg00/ai-engineering-from-scratch": (
        "ai-engineering-from-scratch：ゼロから学ぶAIエンジニアリング",
        "プロダクション級AIアプリを『学んで→作って→届ける』までのフルパス教材。RAG、エージェント、評価まで網羅で人気急上昇。"
    ),
    "anthropics/claude-plugins-official": (
        "claude-plugins-official：Anthropic公式のClaude Codeプラグイン集",
        "Anthropic自身が管理する高品質Claude Codeプラグインのオフィシャルディレクトリ。プラグインエコシステムが公式にキュレーションされる段階に入った。"
    ),
    "mukul975/Anthropic-Cybersecurity-Skills": (
        "Anthropic-Cybersecurity-Skills：AIエージェント向けセキュリティスキル754本",
        "MITRE ATT&CK / NIST CSF 2.0 / ATLAS / D3FENDなど主要5フレームワークにマップした、AIエージェント向け構造化サイバーセキュリティスキル集（754本、26ドメイン）。"
    ),
    "manaflow-ai/cmux": (
        "cmux：縦タブ＋通知のGhostty製macOSターミナル、AIコーディングエージェント向け",
        "Ghostty基盤のmacOSターミナル。縦タブとプッシュ通知を備え、Claude Code等の並列エージェント運用に最適化。"
    ),
    "multica-ai/multica": (
        "multica：エージェントを『同僚化』するオープンソース管理基盤",
        "コーディングエージェントを単発で呼ぶのではなく、タスク割当・進捗追跡・スキル蓄積でチームメンバーのように扱うためのオープンソース基盤。"
    ),
    "anthropics/knowledge-work-plugins": (
        "knowledge-work-plugins：Claude Cowork向け公式ナレッジワーカープラグイン",
        "Claude Coworkで知的労働者が使う想定の、Anthropic公式オープンソースプラグイン集。"
    ),
    "earendil-works/pi": (
        "pi：エージェントツールキット——CLI・LLM API・UIライブラリ・vLLMポッドまで",
        "コーディングエージェントCLI、統一LLM API、TUI/Web UIライブラリ、Slack bot、vLLMポッド管理など、AIエージェントの『土台一式』を提供するキット。"
    ),
    "dotnet/skills": (
        "dotnet/skills：.NET/C# 向けAIコーディングエージェント用スキル集",
        "Microsoft純正の、.NET/C#環境でAIコーディングエージェントを賢く動かすためのスキル集。"
    ),
}

for it in d["sources"]["github"]:
    if it["full_name"] in github_map:
        t, s = github_map[it["full_name"]]
        it["title_ja"] = t
        it["summary_ja"] = s

# -------- Blogs --------
blog_map = {
    "https://huggingface.co/blog/nvidia/nemotron-labs-diffusion": (
        "NVIDIA Nemotron拡散LMで『光速テキスト生成』へ",
        "NVIDIAの拡散言語モデルNemotron Diffusion LMの解説記事。トークン並列生成で長文を高速化、自己回帰の限界を突破する設計思想。"
    ),
    "https://blog.google/innovation-and-ai/technology/ai/io-2026-dialogues-recap/": (
        "Google I/O 2026 Dialoguesステージのリキャップ",
        "Sundar PichaiらがI/O 2026のDialoguesステージで議論した内容のまとめ。"
    ),
    "https://huggingface.co/blog/Dharma-AI/specialization-beats-scale": (
        "『スケールより専門化』——AI調達で見落としがちな戦略変数",
        "大規模汎用モデルの調達一辺倒ではなく、特定タスクに特化したモデルの方が費用対効果で勝つ場面が増えてきた、というAI調達戦略の論考。"
    ),
    "https://openai.com/index/gartner-2026-agentic-coding-leader": (
        "OpenAI、Gartner『エンタープライズAIコーディングエージェント』でリーダー指定",
        "Gartner Magic Quadrant 2026で、OpenAI Codexがエンタープライズコーディングエージェント領域のリーダーに指定。"
    ),
    "https://openai.com/index/virgin-atlantic": (
        "Virgin Atlantic、Codexでモバイルアプリ刷新を期日内出荷",
        "ホリデー商戦の固定期日に向けて、Virgin AtlanticがCodexを活用しモバイルアプリを刷新。単体テストカバレッジほぼ100%、P1欠陥ゼロを達成。"
    ),
    "https://openai.com/index/adventhealth": (
        "AdventHealth、ChatGPT for Healthcareで医療事務を圧縮",
        "米AdventHealthがChatGPT for Healthcareを導入し、事務作業を圧縮して患者ケアの時間を確保。"
    ),
    "https://blog.google/innovation-and-ai/infrastructure-and-cloud/global-network/missouri-programs/": (
        "Google、ミズーリ州への新規コミュニティ投資を発表",
        "次世代労働力育成とエネルギープログラムを軸にした、ミズーリ州への新規投資。AIデータセンター需要を背景にした地域投資の一環。"
    ),
    "https://blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/": (
        "Google I/O 2026で発表された100項目まとめ",
        "I/O 2026で発表されたGemini 3.5、AI Search、Workspace刷新などを含む100項目の公式まとめ。"
    ),
    "https://blog.google/innovation-and-ai/models-and-research/google-research/google-beam-group-meetings/": (
        "Google Beam、グループ会議に対応する新実験",
        "立体映像会議『Google Beam』が複数人グループミーティングに対応する実験を開始。"
    ),
    "https://openai.com/index/model-disproves-discrete-geometry-conjecture": (
        "OpenAIモデル、離散幾何学の80年来の予想を反証",
        "OpenAIのモデルが『単位距離問題』に関する離散幾何学の中心的予想を反証。AI主導の数学発見における大きなマイルストーン。"
    ),
    "https://openai.com/index/the-next-phase-of-education-for-countries": (
        "OpenAI『Education for Countries』、次フェーズへ",
        "学校向けAI展開・教師研修・学習成果改善ツールを拡大する『Education for Countries』新フェーズ発表。"
    ),
    "https://openai.com/index/ramp": (
        "Ramp、Codex×GPT-5.5でコードレビューを高速化",
        "Fintech RampのエンジニアがCodex（GPT-5.5）で本格レビューを実施。所要時間が数時間から数分へ短縮。"
    ),
    "https://openai.com/index/introducing-openai-for-singapore": (
        "OpenAI for Singapore発表——複数年のAI国家パートナー戦略",
        "シンガポール政府とOpenAIが、複数年のAI展開・人材育成・公共サービス支援パートナーシップを発表。"
    ),
    "https://huggingface.co/blog/allenai/olmoearth-v1-1": (
        "OlmoEarth v1.1：より効率的な地球観測モデル群",
        "AllenAI（Ai2）の地球観測基盤モデルOlmoEarthがv1.1へ。同等品質で計算量を抑えた効率重視アップデート。"
    ),
    "https://blog.google/innovation-and-ai/technology/developers-tools/google-io-2026-collection/": (
        "Google I/O 2026 コレクションページ",
        "I/O 2026で『AIをすべての人に役立つものにする』ためのアップデートを一覧化したコレクション。"
    ),
    "https://blog.google/products-and-platforms/products/search/ai-mode-us-insights/": (
        "Google AI Modeが米国の検索体験をどう変えているか",
        "Google検索のAIモードが米国ユーザの検索行動をどう変化させたかのインサイト記事。検索クエリの長文化・対話化の傾向。"
    ),
    "https://blog.google/products-and-platforms/products/workspace/workspace-updates/": (
        "Google Workspace、新しい作成・タスク機能",
        "GeminiベースのGoogle Workspaceに、ドキュメント作成・タスク管理の新機能を追加。"
    ),
    "https://blog.google/innovation-and-ai/sundar-pichai-io-2026/": (
        "I/O 2026：『エージェント版Gemini時代へようこそ』",
        "Sundar Pichaiによる基調メッセージ。Geminiをエージェントとして全プロダクトに統合する『エージェンティックGemini時代』を宣言。"
    ),
    "https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/": (
        "Gemini 3.5：行動するフロンティア知性",
        "Google DeepMindの新世代モデルGemini 3.5発表ブログ。ベンチマーク更新に加え、ツール利用・エージェント実行を統合した『行動する知性』として位置付け。"
    ),
    "https://blog.google/products-and-platforms/products/search/search-io-2026/": (
        "AI Searchの新時代——『検索エンジンの最良の部分』とAIを融合",
        "Google検索のAI Modeをデフォルト体験に近づけるアップデート。"
    ),
    "https://openai.com/index/advancing-content-provenance": (
        "OpenAI、Content CredentialsとSynthIDでAIコンテンツの出所証明を強化",
        "AI生成コンテンツの来歴情報をContent CredentialsとSynthIDで付与し、検証ツールも提供。AIメディアの信頼性確保に向けた取り組み。"
    ),
    "https://huggingface.co/blog/ettin-reranker": (
        "Ettin Rerankerファミリー発表",
        "RAGや検索向けの新リランカーモデル群『Ettin』。サイズと精度のトレードオフを整理。"
    ),
    "https://huggingface.co/blog/PaddlePaddle/paddleocr-transformers": (
        "PaddleOCR 3.5：Transformersバックエンドで動くOCR/文書解析",
        "Baidu PaddlePaddleのOCRエンジンPaddleOCRが、Hugging Face Transformersバックエンドに対応してv3.5に。OCR＋文書構造解析を一気通貫で。"
    ),
    "https://huggingface.co/blog/ibm-research/open-agent-leaderboard": (
        "IBM Research、Open Agent Leaderboardを公開",
        "オープンに利用可能なエージェントモデル群の標準ベンチマーク『Open Agent Leaderboard』をIBM Researchが公開。"
    ),
    "https://openai.com/index/dell-codex-enterprise-partnership": (
        "OpenAI×Dell、Codexをハイブリッド／オンプレ環境へ",
        "OpenAIとDellが提携。Codexエージェントをエンタープライズのハイブリッド／オンプレ環境で安全にデプロイできるよう支援。"
    ),
}

for it in d["sources"]["blogs"]:
    if it["url"] in blog_map:
        t, s = blog_map[it["url"]]
        it["title_ja"] = t
        it["summary_ja"] = s

# -------- Highlights --------
def hn_item(id_):
    return next((x for x in d["sources"]["hn"] if x["id"] == id_), None)

def reddit_item(id_):
    return next((x for x in d["sources"]["reddit"] if x["id"] == id_), None)

highlights = []

# 1. DeepSeek 75% permanent price cut
i = hn_item("48257410")
highlights.append({
    "source": "hn",
    "title": i["title"],
    "title_ja": "DeepSeek、フラッグシップAIを75%恒久値下げ——推論コストの底が抜ける",
    "url": i["url"],
    "hot_take_ja": "中国側のDeepSeekがフラッグシップを75%恒久値下げ。同日にHNを賑わせた新コーディングエージェント『Reasonix』も超低価格を売りにしており、米中フロンティア全部が同じ方向に殴り合う格好だ。『最先端モデルは高い』前提でビジネスを組んだスタートアップは、来期の単価計算をいまから引き直したほうがいい。",
    "detail_ja": "Bloombergによると、DeepSeekは旗艦モデルAPIの75%値下げを期間限定ではなく恒久的に適用する。前回の値下げが一時キャンペーンとして発表され、結局据え置きになった経緯を踏まえ、今回は明示的に『恒久』としてアナウンスされた点が重い。同じ24時間でHN首位級に上ったDeepSeek純正コーディングエージェント『Reasonix』も、高いプロンプトキャッシュ率と低コスト推論を売りにしており、コーディングエージェントの本命市場で価格戦争が始まったことを示す。米国側もOpenAIやAnthropicがエージェント用途のキャッシュ／バッチ／プロンプトキャッシュで実効単価を下げ続けており、トークン単価の絶対値はもはや差別化要因にならない局面に近づいている。一方で、エージェント化で消費トークンが爆増しているため、ユーザ側の請求書が下がるとは限らない。値下げの真の意味は『個人ユーザの単発利用が安くなる』ではなく『超大量推論を前提にしたエージェント設計が現実的になる』ことにある。",
    "detail_en": "According to Bloomberg, DeepSeek is making the 75% discount on its flagship model API permanent rather than promotional. That distinction matters because a previous discount round had been marketed as a campaign and later left in place; this time the company is explicit. In the same 24 hours, DeepSeek's native coding agent 'Reasonix' surfaced on HN's front page, marketed around aggressive prompt caching and low cost-per-call. The two announcements together signal that price competition is now centered on the coding-agent stack, not raw chat tokens. US labs (OpenAI, Anthropic) have been pushing effective per-call prices down via caching, batch, and prompt cache as well, so raw token price is approaching commodity status. Note however that customer bills are not necessarily falling, because agentic workloads keep scaling tokens up faster than unit prices fall. The deeper takeaway is that agent designs that previously looked uneconomic — multi-hour, multi-million-token runs — are now viable to attempt.",
    "key_points_ja": [
        "DeepSeek旗艦モデルAPIを恒久75%値下げ",
        "同時公開のコーディングエージェントReasonixも超低価格",
        "米中フロンティアが同じ方向に価格を圧縮中",
        "ただしエージェント化でトークン消費は爆増",
        "勝負は『単価』ではなく『エージェント設計』へ"
    ],
    "key_points_en": [
        "DeepSeek makes flagship model 75% cheaper permanently",
        "Same-day Reasonix coding agent leans into low cost",
        "US frontier labs already cutting effective prices too",
        "Token usage exploding faster than price drops",
        "Battle shifts from unit cost to agent design"
    ]
})

# 2. Memory = 2/3 of AI chip cost
i = hn_item("48258684")
highlights.append({
    "source": "hn",
    "title": i["title"],
    "title_ja": "AIチップの原価、約2/3がメモリに——主役はGPUダイからHBMへ",
    "url": i["url"],
    "hot_take_ja": "AIアクセラレータの部品コストのうち、約2/3がメモリで占められる時代になった。先週話題になった『メモリ調達でハイパースケーラーが取り合い』の話と整合する数字で、もはやGPU本体よりHBMを押さえた者がAIを握る。エヌビディアではなくSK Hynix／Samsung／Micronのほうが構造的勝者かもしれない。",
    "detail_ja": "Epoch AIの分析によると、AIアクセラレータの部品コスト構成のうちメモリ（HBM等）が占める比率が約2/3に到達した。背景には、モデルサイズと長文コンテキスト対応のために必要となるオンパッケージメモリ容量と帯域幅の爆発的増大がある。HBM3eからHBM4へとスタックが厚くなるにつれ、Wafer単価よりもパッケージング・スタッキングコストが支配的になり、生産能力もメモリ側がボトルネックになる。先週HNを賑わせた『AIのメモリクランチ』の話とも符合し、今やAIスタートアップにとってGPU確保より『HBM枠の確保』が深刻な制約に。投資の観点では、エヌビディアばかりが報じられるが、SK Hynix・Samsung・Micron・パッケージング装置メーカが構造的勝者になりうる、という見方も強まっている。一方でメモリ依存が極端に高まることは、地政学リスク（韓国・台湾集中）と価格弾力性の低下も同時に意味する。",
    "detail_en": "An Epoch AI analysis finds that memory (HBM and adjacent stacks) now accounts for roughly two-thirds of the bill of materials for AI accelerators. The driver is the combined growth of parameter counts and long-context support, which both demand much more on-package memory capacity and bandwidth. As HBM3e gives way to HBM4 with taller stacks, packaging and stacking become the dominant cost contributors and the binding production constraint, rather than wafer logic die cost. This dovetails with last week's discussion about the AI memory crunch: for AI startups, securing HBM allocation is becoming a harder bottleneck than securing GPU compute. From an investor lens, the story is no longer just NVIDIA — SK Hynix, Samsung, Micron, and packaging-tool vendors look like structural winners. The flip side is concentration risk: HBM supply is heavily reliant on a few Korean and Taiwanese vendors, and demand price-elasticity is collapsing.",
    "key_points_ja": [
        "AIチップ部品原価の約2/3がメモリ(HBM等)",
        "GPUダイよりHBM容量・帯域がボトルネック",
        "前週話題のAIメモリクランチを裏付ける数字",
        "勝者候補：SK Hynix／Samsung／Micron／パッケージ装置",
        "地政学集中とエラスティシティ低下のリスクも"
    ],
    "key_points_en": [
        "Memory now ~2/3 of AI accelerator BOM",
        "HBM capacity & bandwidth, not GPU dies, are the bottleneck",
        "Confirms last week's AI memory crunch narrative",
        "Likely winners: SK Hynix, Samsung, Micron, packaging tools",
        "Concentration & inelastic demand raise new risks"
    ]
})

# 3. Constraint Decay paper
i = hn_item("48256912")
highlights.append({
    "source": "hn",
    "title": i["title"],
    "title_ja": "『Constraint Decay』——LLMエージェントは制約を忘れて壊れる",
    "url": i["url"],
    "hot_take_ja": "LLMエージェントを長時間バックエンドコードに走らせると、最初に与えた制約をジワジワ忘れていって最後に壊れる、という現象を定量化した論文。『エージェントに任せれば長尺タスクも自律的に回る』という一番都合の良い物語に対して、ちゃんとデータで殴り返した一本。エージェント設計者は読むべき。",
    "detail_ja": "arXivに掲載された本論文は、LLMエージェントにバックエンドコード生成を長尺・多ファイル・多ターンで実行させると、初期に与えたAPI制約・スキーマ・命名規則などをだんだん忘れて違反していく『Constraint Decay』現象を定量化した。同じ制約でも、ターンが進むほど違反率が単調に上がり、誤った前提のままコードがコンパイルだけ通ってしまうケースが多い。原因としては、コンテキストウィンドウの圧迫だけでなく、エージェント側が自分の生成した最新コンテキストを優先する『直近バイアス』、そしてツール結果と元仕様の整合性をチェックしない設計が挙げられている。実務的な示唆は明確で、(1)長尺タスクでも『制約セクション』を毎ターン強制再注入する、(2)スキーマ／契約の機械検証をエージェントループ内に組み込む、(3)単一エージェントの長期実行より、検証エージェントを分離した多エージェント設計が安定する、というもの。『agentic with memory』の常識的な落とし穴を、ちゃんと数字で示した点が重要。",
    "detail_en": "This arXiv paper quantifies a phenomenon the authors call Constraint Decay: when LLM agents run long, multi-file, multi-turn backend code-generation tasks, they progressively forget and violate the API constraints, schemas, and naming conventions specified at the start. Violation rates rise monotonically with turn count even when the constraints are reiterated in tool descriptions. The authors attribute this to context-window pressure, but also to a 'recency bias' where the agent privileges its own recently generated context over the original specification, and to architectures that never re-verify outputs against the original contract. The practical takeaways are concrete: (1) re-inject the constraint section on every turn, not just at the start; (2) move schema / contract verification inside the agent loop as a mechanical check; (3) prefer multi-agent designs with a dedicated verifier over a single long-running generator. The contribution is less a new method and more a precise quantification of a failure mode that the 'agentic + memory' marketing tends to gloss over.",
    "key_points_ja": [
        "長尺エージェント実行で制約違反が単調増加",
        "ターン進行に伴う『直近バイアス』が主因",
        "ツール結果と元仕様の整合検証が不足しがち",
        "対策：制約の毎ターン再注入＋機械検証＋検証用サブエージェント",
        "『エージェント＋メモリで万事解決』に対する反証データ"
    ],
    "key_points_en": [
        "Constraint violations rise monotonically over turns",
        "Recency bias pushes agents to follow their own latest context",
        "Tool outputs rarely re-checked against original spec",
        "Fixes: re-inject constraints + in-loop verification + verifier subagent",
        "Hard data against the 'agent + memory' silver-bullet story"
    ]
})

# 4. MS Paint -> AI fake art movement -> Google believes
i = reddit_item("1tmb7c6")
highlights.append({
    "source": "reddit",
    "title": i["title"],
    "title_ja": "AIが架空の美術運動を捏造、それをGoogleが『本物』として再生成——ハルシネーション伝播ループ",
    "url": i["url"],
    "hot_take_ja": "AIが捏造した架空の美術運動を、Google検索AIが『実在』として再吐出している、というハルシネーション伝播事例。LLMが生成した嘘がウェブに吸い込まれ、それが別のLLMの根拠になり、最終的に世界の認識として固定される——情報生態系の崩れ方の典型サンプル。",
    "detail_ja": "Reddit r/artificialで拡散している投稿。退役した投稿者がMS Paintで描いた素朴な絵をAIアシスタントに講評させたところ、AIは『これは「○○ism」という美術ムーブメントに連なる作品です』と、存在しないアートムーブメントを名前付きで解説してきた。投稿者が試しにその名前をGoogleで検索すると、Googleの生成AI要約が当該ムーブメントを実在のものとして概説し始め、出典らしき文章すら表示された。これは典型的な『ハルシネーション伝播ループ』で、(1)あるLLMが嘘を吐く、(2)その嘘がブログ・SNSに引用される、(3)別のLLM（Google AI Overview等）が学習・取込みする、(4)権威ある一次情報のように表示される、という構造で発生する。AIが生成した嘘を、別のAIが信じて拡散することで、ウェブの『真実』のベースラインがズレていく。検索エンジンのAIサマリーが情報のオーソリティに近づくほど、この問題は深刻化する。",
    "detail_en": "A Reddit r/artificial post going viral: a retired user asked an AI assistant for feedback on amateur MS Paint paintings, and the assistant confidently placed them inside a named art movement that does not exist. When the user Googled the made-up name, Google's AI Overview generated a confident summary of that fictional movement as if it were a real, documented art history phenomenon. This is the canonical hallucination feedback loop: (1) an LLM fabricates a plausible entity, (2) the fabrication leaks into blogs and social posts, (3) another LLM ingests it as training or retrieval signal, (4) the second LLM surfaces it as authoritative. Each loop nudges the web's baseline 'truth' away from reality. As AI Overviews become the default top-of-page experience in search, the surface area for this feedback to harden into common knowledge grows fast. The anecdote is funny, but it is also the cleanest illustration so far of how a synthetic-content web could quietly drift its own facts.",
    "key_points_ja": [
        "AIが架空の美術運動を捏造して命名",
        "GoogleのAI要約もそれを実在として再生成",
        "AI→ウェブ→別AIのハルシネーション伝播ループ",
        "AI Overviewが普及するほど影響が拡大",
        "合成コンテンツ時代の『事実のドリフト』典型例"
    ],
    "key_points_en": [
        "AI invented a fake art movement with a confident name",
        "Google's AI Overview then described it as real",
        "Clean example of hallucination feedback across LLMs",
        "Risk grows as AI Overviews dominate search",
        "Synthetic-content web can silently drift its own truth"
    ]
})

# 5. Palantir NHS unlimited access
i = reddit_item("1tlig93")
highlights.append({
    "source": "reddit",
    "title": i["title"],
    "title_ja": "Palantirら外部委託先、NHS患者の識別可能データに『無制限アクセス』——Amnesty告発",
    "url": i["url"],
    "hot_take_ja": "英NHSがPalantirほか外部ベンダに、識別可能な患者データへの『無制限』アクセスを許可していた、とAmnestyが告発。AI×医療の最大の論点は『モデル性能』ではなく『誰がトレーニングデータの根本を握るか』。今後数年のAI政策で必ず再燃する論点だ。",
    "detail_ja": "Amnesty Internationalによると、英NHS Englandが米Palantir等の外部委託先に、識別可能なNHS患者情報への無制限アクセスを許可していた事実が明らかになった。元々NHSの巨大データセットはAI医療研究・運用最適化のため『仮名化したうえで限定的に共有する』前提で外部ベンダに渡されていたが、Amnestyの調査では、アクセス範囲が当初想定より大きく、ベンダ側が識別性の高いデータに事実上自由にアクセスできる契約構造になっていたという。問題の本質は、AI医療の競争優位が『どのモデルを使うか』ではなく『どの臨床データを実質的に独占できるか』に移っていることにある。Palantirは米国側でICEとの契約でも繰り返し批判を浴びており、AI医療データガバナンスの曖昧さが、特定ベンダの構造的優位に直結する。EU AI ActやUK AI規制の今後の運用、そしてオンプレ／ハイブリッドでのAI医療デプロイ（OpenAI×Dellなど）の議論にも直接効いてくる事案。",
    "detail_en": "Amnesty International reports that NHS England has been granting US software company Palantir and other contractors effectively unlimited access to identifiable NHS patient information, beyond what the original procurement framing implied. The original premise was that NHS bulk data would be shared with vendors only under pseudonymisation and tight purpose limits, but Amnesty's review concludes the contract structures permit far wider access than the public understanding suggested. The deeper point is that the competitive moat in AI healthcare is shifting from 'which model do you use' to 'which clinical dataset can you effectively monopolise'. Palantir is already politically charged in the US (e.g. ICE contracts), and the NHS case shows the same governance ambiguity translating into a structural data advantage. This will feed directly into the next round of EU AI Act enforcement debates, UK AI regulation design, and recent enterprise AI deployments (e.g. OpenAI x Dell on-prem / hybrid) where the question of who actually controls patient data becomes central.",
    "key_points_ja": [
        "NHSが識別可能データへ無制限アクセスを許可した可能性",
        "Amnesty Internationalが告発",
        "AI医療の競争優位は『データ独占』に移行中",
        "Palantirは米国でもICE関連で批判の的",
        "EU AI Act・UK AI規制議論の火種に"
    ],
    "key_points_en": [
        "NHS allegedly gave vendors unrestricted patient data access",
        "Amnesty International raised the alarm",
        "AI healthcare moat is shifting to dataset monopoly",
        "Palantir already politically contested in the US",
        "Will reshape EU AI Act & UK AI regulation debate"
    ]
})

d["highlights"] = highlights

with open(OUT, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f"Wrote {OUT}")
print(f"Highlights: {len(highlights)}")
