#!/usr/bin/env python3
"""Enrich raw-2026-06-04.json -> 2026-06-04.json"""
import json, pathlib

base = pathlib.Path(__file__).resolve().parent.parent
raw = json.load(open(base / "data/raw-2026-06-04.json"))

# ---- arXiv (top 25) : index -> (title_ja, summary_ja) ----
arxiv = {
 0: ("STRIDE: 部分摂動からのスパース復元による学習データ寄与推定",
     "モデル予測を学習データに遡る寄与推定(TDA)を、再学習を繰り返さずに行う手法。データ部分集合の摂動とスパース復元を使い、LLM規模でも効率的に「どのデータが効いたか」を特定する。"),
 1: ("3D軌道とテキストで操る動的3D形状生成 T2Mo",
     "テキストだけでは曖昧になりがちな動きの指定を、3D軌道を制御信号として加えることで精密化するフィードフォワード型の動的3D形状生成フレームワーク。"),
 2: ("音声と矛盾するテキストに引っ張られる音声言語モデルの是正",
     "音声言語モデルは音声証拠が明確でも矛盾するテキストに従いがち。本研究は『音声の答えが表現されていないのか、表現はあるが上書きされているのか』を反実仮想で切り分け、是正可能性を示す。"),
 3: ("GRAIL: 3Dアセットと動画事前知識からヒューマノイドの全身操作を生成",
     "テレオペやモーキャプに頼らず、3Dアセットと動画の事前知識からヒューマノイドのロコ・マニピュレーション(移動+操作)のデモを大量生成する手法。"),
 4: ("X4Val: 分散低減した方策評価のためのニューラル代理モデル学習",
     "実機テストデータが高価でスケールしにくいロボット学習の評価を、ニューラル代理モデルで分散を抑えつつ効率化するフレームワーク。"),
 5: ("StreamMA: マルチエージェント推論のストリーミング通信",
     "各推論ステップを生成と同時に下流エージェントへ流すことで、パイプライン深さに比例して増える従来のエンドツーエンド遅延を削減するマルチエージェント推論システム。"),
 6: ("分布的DAggerによるリッチ・フィードバックからの強化学習",
     "正誤1ビットだけで報酬を与える従来のRLVRを超え、より豊かなフィードバック(部分点や過程情報)を分布的DAggerで活用して推論モデルを訓練する手法。"),
 7: ("適応的PSOを用いた多列RBFニューラルネットワーク",
     "勾配法ベースのRBFネットワーク訓練を、適応/非適応の粒子群最適化(PSO)で隠れユニット選択まで含めて改善する手法。"),
 8: ("Vision Transformerによる細粒度の車種分類オープンソースパイプライン",
     "追い越し事故での自転車側の負傷度に効く車体タイプを、自然な路上動画から自動分類する2段階のオープンソースCVパイプライン。"),
 9: ("失敗した推論トレースは『何が直せるか』を教える(ただし読んでも分からない)",
     "推論失敗の原因を『運の悪いサンプリング(再試行で直る)』と『本質的な能力不足』に切り分ける。失敗トレースは中身を読むのではなく統計的シグナルとして使えと主張。"),
 10: ("HORIZON: 回復可能性で律する物理ドメイン・スケーリングのカリキュラム",
     "頑健なロボット方策の学習で、ただランダム化を広げるのではなく『回復可能性』を中心制約に据え、より難しい物理を学習可能な順序で与えるカリキュラム。"),
 11: ("GeM-NR: 非剛体シーン変化のための幾何認識マルチビュー編集",
     "従来は剛体や見た目だけに限られていたマルチビュー画像編集を、幾何を考慮して非剛体の形状変化まで一貫して編集できるよう拡張。"),
 12: ("BBOmix: 教師なし生物表現学習のハイパラ最適化ベンチマーク",
     "高次元オミクスデータでオートエンコーダ等の教師なし表現学習を行う際の、ハイパーパラメータ最適化を評価する表形式ベンチマーク。"),
 13: ("ランダム畳み込み特徴のマッチングによる金融時系列生成",
     "歴史的に1本の経路しかない金融時系列の生成で、敵対的学習の記憶化(過学習)を避けるため、ランダム畳み込み特徴のマッチングを用いる手法。"),
 14: ("文脈内学習のための活性化ベース能動学習:課題と知見",
     "Transformerの活性化を細かいシグナルとして使い、LLMの文脈内学習用サンプルを能動的に選ぶ手法を検証。期待ほど単純ではない課題も報告。"),
 15: ("代数構造を保つKoopman学習のための深層埋め込み乗法的DMD",
     "非線形ダイナミクスを線形スペクトル問題に変えるKoopman理論を、観測量が合成に整合する(代数構造を保つ)ように深層学習で構成する手法。"),
 16: ("LLM駆動エージェントによる効率的・根拠付きの移動予測",
     "都市シミュレーションや交通計画に使う個人移動予測を、LLMエージェントで解釈性と根拠を保ちつつ効率化するアプローチ。"),
 17: ("完全準同型暗号で因果構造学習のデータプライバシーを保護",
     "分散環境での因果構造学習における情報漏洩を、完全準同型暗号(FHE)を使って計算しながらデータを秘匿することで防ぐ手法。"),
 18: ("Geometry Gaussians: ガウシアンスプラッティングで見た目と幾何を分離",
     "3DGSから正確な幾何を取り出すと描画品質が落ちる問題に対し、見た目と幾何の表現を分離して両立させる手法。"),
 19: ("自己評価は既に備わっている:ベースLLMから潜在的なジャッジ較正を引き出す",
     "LLMが『別のジャッジモデルが自分の出力をどう採点するか』を、専用訓練なしの少数ショットだけで予測できることを発見。自己評価能力は訓練前から潜在的に存在する。"),
 20: ("Audio Interaction Model: 常時オンの統合型オーディオ言語モデル",
     "従来オフラインだった大規模音声言語モデルや、単一タスクのストリーミング音声モデルを、常時『知覚→判断→発話』する1つのオンラインモデルに統合する試み。"),
 21: ("Graph Set Transformer: グラフの集合上で学習するアーキテクチャ",
     "要素ごとの予測が集合全体の文脈と局所構造の両方に依存するタスク向けに、グラフの集合を直接扱えるTransformer型アーキテクチャを提案。"),
 22: ("子どもの一人称視点入力から視覚と言語を継続学習",
     "シャッフルして何百エポックも回す従来法と異なり、子どもの一人称動画の連続的・時間構造を保った入力から語と指示対象の対応を継続学習する研究。"),
 23: ("標準模擬患者ケースによる動的臨床意思決定でのLLM評価",
     "静的・単発のベンチマークでは捉えられない、情報収集→治療計画→経過に応じた調整という臨床の動的プロセスでLLMを評価するフレームワーク。"),
 24: ("RePercENT: 2モダリティを超える分離表現学習のスケーリング",
     "アライメントや融合を超え、全てのクロスモーダル相互作用を活かしつつモダリティ固有情報も保つ分離表現学習を、3モダリティ以上へスケールさせる手法。"),
}

# ---- HN : id -> (title_ja, summary_ja) ----
hn = {
 "48385906": ("Gemma 4 12B:エンコーダ不要の統合マルチモーダルモデル",
   "Googleが画像・テキストを別エンコーダなしで扱う統合型のオープンモデルGemma 4 12Bを公開。アーキテクチャを簡素化しつつマルチモーダル性能を狙う。HN994ポイントの注目作。"),
 "48383220": ("Metaの従業員は最大30分まで勤務中トラッキングをオプトアウト可能に",
   "Metaが社内の勤務トラッキングについて、従業員が最大30分まで追跡を停止できる仕組みを導入。AI時代の職場監視と従業員プライバシーの綱引きを象徴する話題。"),
 "48392004": ("AI利用で落第急増、UCバークレーCSで数学力の低下を教員が指摘",
   "UCバークレーのCS講義で、AIへの過度な依存とともに落第が急増し基礎数学力の低下が観測されているとの報道。AIが学習を助けるのか損なうのかという核心的議論。"),
 "48383056": ("Uberの月1,500ドルAI上限はAIツール価格の有用なシグナル",
   "Simon Willisonが、Uberが社員のAI利用を月1,500ドルで上限設定した件を分析。エージェント型コーディングの実コストとツール価格の行方を読む材料として注目。"),
 "48383241": ("DDR5メモリ32GBが最低375ドルに、AI需要が自作PCを圧迫",
   "AIデータセンター需要によるメモリ逼迫で、DDR5 32GBの最低価格が375ドルまで高騰。AIインフラ投資が一般消費者のPC自作コストに波及している。"),
 "48392343": ("脆弱なアプリを作り1,500ドル投じてLLMがハッキングできるか検証",
   "意図的に脆弱なWebアプリを作り、約1,500ドル分のLLM実行で自動侵入を試みた実験ブログ。LLMが実際にどこまで攻撃できる/できないかを具体データで示し話題に。"),
 "48382052": ("数学者が警鐘:AIが急速に地歩を固めつつある",
   "Science誌。AIが数学研究で急速に進歩し、証明や問題解決で存在感を増していることに数学者コミュニティが警戒と期待の両方を示している。"),
 "48392082": ("私たちはどうやってClaudeを各製品で封じ込めているか",
   "Anthropicのエンジニアリング記事。製品横断でClaudeの権限・行動を安全に『封じ込める』ための設計思想と実装(サンドボックス、権限制限等)を解説。"),
 "48386725": ("Gooey: Zig製のGPUアクセラレーションUIフレームワーク",
   "Zig言語で書かれたGPU描画のUIフレームワーク。AIとは直接無関係だが、低レベル高速UIへの開発者の関心を集めHN上位に。"),
 "48396004": ("Show HN: Uruky(EU拠点のKagi代替)が画像検索とURL書き換えを追加",
   "EU拠点のプライバシー重視検索エンジンUrukyが画像検索などを追加。検索市場でのKagi代替を志向するプロダクト。"),
 "48400311": ("Google従業員が社内で『自社AIはダメ』というミームを共有",
   "404Mediaの報道。Google社員が自社AI製品の品質を皮肉るミームを内部で共有していると伝え、I/Oでの大々的発表との温度差が話題に。"),
 "48386129": ("Show HN: Nutrepedia — ClojureとHtmxで作る29言語の栄養情報",
   "ClojureとHtmxで構築された29ロケール対応の栄養情報サイト。技術スタックの選択が開発者の関心を集めた。"),
 "48388909": ("プレビューURL付きのセルフホスト開発サンドボックス(Docker/Go、K8s不要)",
   "Kubernetesなしで、DockerとgoだけでプレビューURL付きの開発サンドボックスを立てるOSS。エージェント開発のための隔離環境として注目。"),
 "48400842": ("AIが自分自身を作るとき:再帰的自己改善に向けた我々の進捗",
   "Anthropicの研究所記事。AIがAI研究開発を加速させる『再帰的自己改善(RSI)』の現状と計測手法を整理。フロンティアAIの臨界点を巡る重要な議論。"),
 "48390400": ("数学者の嘆き(2002)[PDF]",
   "Lockhartの古典的エッセイ。数学教育が本質的な創造性を欠いていると嘆く内容で、AIと数学の議論の文脈で再び読まれている。"),
 "48400213": ("GoogleがTimnit Gebruを解雇する原因となったLLMへの警告は全て現実になった",
   "Gebruが2020年に共著論文で警告したLLMのリスク(環境負荷、バイアス、誤情報等)が現実化したと振り返る投稿。AI倫理研究者排除の代償を問う。"),
 "48399974": ("KVarN: HuaweiによるvLLMネイティブのKVキャッシュ量子化バックエンド",
   "HuaweiがvLLM向けに、KVキャッシュを量子化してメモリを節約するネイティブバックエンドを公開。長文推論の効率化に寄与。"),
 "48386529": ("AIデータセンターがそんなに良いものなら、なぜ秘密裏に建設されるのか",
   "AIデータセンターが地域に与える影響(電力・水・騒音)への不透明さを批判する論説。米国各地で広がるデータセンター反対運動の文脈。"),
 "48387095": ("Launch HN: Hyper(YC P26)— エージェント開発を支える『会社の脳』",
   "社内知識を集約しエージェント開発に供給する『カンパニーブレイン』を掲げるYCスタートアップのローンチ。"),
 "48387251": ("胚はどのように四肢を形作るか:『遺伝的ブレーキ』の発見",
   "モントリオール大の発生生物学研究。AIとは無関係だが、四肢形成を制御する遺伝的ブレーキの発見としてHNで注目。"),
}

# ---- GitHub : name -> (title_ja, summary_ja) ----
github = {
 "headroom": ("headroom: LLMに渡す前にツール出力やログを圧縮",
   "ツール出力・ログ・RAGチャンクをLLM入力前に圧縮し、トークンを60〜95%削減しつつ回答品質を保つというライブラリ/プロキシ/MCPサーバ。本日3,000超のスター獲得。"),
 "hermes-agent": ("hermes-agent: あなたと共に成長するエージェント",
   "NousResearchによる、利用とともに成長するパーソナルエージェント。巨大なスター数を持つOSSエージェントフレームワーク。"),
 "ECC": ("ECC: エージェント・ハーネスの性能最適化システム",
   "Claude Code/Codex/Cursor等を横断して、スキル・本能・メモリ・セキュリティを最適化するエージェント・ハーネス強化システム。"),
 "Open-LLM-VTuber": ("Open-LLM-VTuber: ローカルで動く音声対話Live2D VTuber",
   "任意のLLMとハンズフリー音声で対話でき、割り込みやLive2Dの表情表示までローカルで動かせるOSS。"),
 "trivy": ("trivy: コンテナ等の脆弱性・設定ミス・秘密情報スキャナ",
   "Aqua Securityによる定番のセキュリティスキャナ。コンテナ・K8s・コード・クラウドの脆弱性やSBOMを検出。"),
 "cosmos": ("NVIDIA Cosmos: 物理AIのためのオープンなワールドモデル基盤",
   "ロボットや自動運転向けの物理AIを構築するための、ワールドモデル・データセット・ツールのオープンプラットフォーム。"),
 "last30days-skill": ("last30days-skill: 横断的に話題を調べて根拠付き要約を作るスキル",
   "Reddit・X・YouTube・HN・Polymarket・Webを横断して任意トピックを調べ、根拠に基づく要約を合成するエージェントスキル。"),
 "copilot-sdk": ("copilot-sdk: GitHub Copilot Agentを組み込むマルチSDK",
   "GitHub Copilot Agentを自社アプリやサービスに統合するためのマルチプラットフォームSDK。"),
 "PaddleOCR": ("PaddleOCR: PDF・画像をAI向け構造化データに変換するOCR",
   "100以上の言語に対応し、PDFや画像をLLMが扱える構造化データに変換する軽量OCRツールキット。"),
}

# ---- Blogs : url -> (title_ja, summary_ja) ----
blogs = {
 "https://huggingface.co/blog/nvidia/nemotron-3-5-content-safety": ("Nemotron 3.5コンテンツ安全性:カスタマイズ可能なマルチモーダル安全モデル",
   "NVIDIAが企業向けに、テキスト・画像のコンテンツ安全性をカスタマイズして判定できるマルチモーダルなガードモデルを公開。"),
 "https://huggingface.co/blog/ServiceNow-AI/eva-bench-data": ("EVA-Bench Data 2.0:3ドメイン・121ツール・213シナリオ",
   "ServiceNowによるエージェント評価ベンチEVA-Benchの拡充版。3ドメイン・121ツール・213シナリオで実務的なエージェント能力を測る。"),
 "https://openai.com/index/endava-frontiers": ("Endavaがソフト開発をAIエージェント中心に再設計",
   "EndavaがChatGPT EnterpriseとCodexを使い、開発ワークフローの自動化とAIネイティブな組織文化づくりを進めた事例。"),
 "https://openai.com/index/chatgpt-memory-dreaming": ("Dreaming:より役立つChatGPTのための新しいメモリ",
   "ChatGPTが会話の合間に記憶を整理・統合する『Dreaming』という新メモリ機構を導入。好みや文脈を新鮮に保ち、会話をまたいで一貫した応答を狙う。"),
 "https://huggingface.co/blog/hf-cli-for-agents": ("hf CLIをエージェント最適化でHub操作の手段として設計",
   "Hugging Face Hubを操作するhf CLIを、人間よりもAIエージェントが使いやすい形に設計し直した解説。"),
 "https://openai.com/index/introducing-new-capabilities-to-gpt-rosalind": ("GPT-Rosalindに新機能:生命科学研究を強化",
   "OpenAIの生命科学特化モデルGPT-Rosalindが、生物学的推論・医薬化学・ゲノミクス解析・実験ワークフローの能力を強化。"),
 "https://blog.google/products-and-platforms/products/search/thrifting-tips/": ("Google検索で古着・ヴィンテージ探しを底上げする5つの方法",
   "Google検索の画像・AI機能を使った古着やヴィンテージ品の探し方の紹介記事。"),
 "https://huggingface.co/blog/Dharma-AI/direct-preference-optimization-beyond-chatbots": ("チャットボットを超えるDPO(直接選好最適化)",
   "DPOをチャットボットの整合だけでなく、より広い応用(推薦や制御等)へ拡張する考察。"),
 "https://openai.com/index/wasmer": ("WasmerがCodexでエッジ向けNode.jsランタイムを構築",
   "WasmerがGPT-5.5搭載Codexを使い、エッジ向けNode.jsランタイムの開発を10〜20倍に加速し数週間で出荷した事例。"),
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
 "https://blog.google/innovation-and-ai/technology/ai/io-2026-google-ai/": ("Geminiを使ってGoogle I/O 2026を作った方法",
   "GoogleがI/O 2026の準備にGeminiをどう活用したかを紹介する舞台裏記事。"),
 "https://huggingface.co/blog/JetBrains/mellum2-launch": ("Mellum2:JetBrainsによる12B MoEモデル",
   "JetBrainsがコード補完特化の12Bパラメータ Mixture-of-Expertsモデル Mellum2 を公開。"),
 "https://huggingface.co/blog/ibm-research/agent-logic-and-scalable-ai-adoption": ("LLMを超えて:企業のAI普及はエージェント・ロジックに依存する",
   "IBM Researchが、企業でのスケーラブルなAI導入にはLLM単体でなくエージェント・ロジックの設計が鍵だと論じる。"),
 "https://blog.google/innovation-and-ai/technology/ai/io-2026-vibe-coded-quiz/": ("Google AI StudioでバイブコーディングしたI/O 2026クイズ",
   "Google AI StudioでさっとコーディングしたI/O 2026の発表内容クイズの紹介。"),
 "https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni-3-5-videos/": ("Gemini OmniとGemini 3.5の9つのデモ",
   "I/O 2026で発表されたGemini OmniとGemini 3.5の実動作を示す9本のデモ動画。"),
 "https://blog.google/innovation-and-ai/technology/ai/university-waterloo-labs/": ("Futures Labの実世界AIプロトタイプ",
   "ウォータールー大の学生が作る手話チューターなど、教育や仕事を変える実世界AIプロトタイプの紹介。"),
 "https://huggingface.co/blog/torch-profiler": ("PyTorchのプロファイリング(第1部):torch.profiler入門",
   "torch.profilerを使ったPyTorchの性能プロファイリング初心者向けガイド。"),
}

# Apply
for i, (tj, sj) in arxiv.items():
    raw["sources"]["arxiv"][i]["title_ja"] = tj
    raw["sources"]["arxiv"][i]["summary_ja"] = sj
for it in raw["sources"]["hn"]:
    if it["id"] in hn:
        it["title_ja"], it["summary_ja"] = hn[it["id"]]
for it in raw["sources"]["github"]:
    if it["name"] in github:
        it["title_ja"], it["summary_ja"] = github[it["name"]]
for it in raw["sources"]["blogs"]:
    if it["url"] in blogs:
        it["title_ja"], it["summary_ja"] = blogs[it["url"]]

# ---- Highlights ----
raw["highlights"] = [
 {
  "source": "HN / Google",
  "title": "Gemma 4 12B: A unified, encoder-free multimodal model",
  "title_ja": "Gemma 4 12B:エンコーダ不要の統合マルチモーダルモデル",
  "url": "https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemma-4-12b/",
  "hot_take_ja": "画像用エンコーダを別に持たず、テキストも画像も1つのモデルで処理する『エンコーダ不要』設計が肝。アーキを単純化しつつマルチモーダルを成立させるなら、オープンモデルの作り方が一段変わる。HN994ポイントの注目はダテじゃない。",
  "detail_ja": "GoogleがオープンモデルGemma 4の12B版を公開した。最大の特徴は、従来のマルチモーダルモデルが画像専用エンコーダ(ViT等)を別途持ち、その出力を言語モデルに橋渡ししていたのに対し、Gemma 4は単一の統合モデルで画像とテキストを直接扱う『エンコーダ不要(encoder-free)』設計を採る点だ。これによりパイプラインが単純化し、モダリティ間の情報損失や接続部の調整コストを減らせる可能性がある。12Bという規模はローカルや単一GPUでも扱いやすく、研究・実装の裾野を広げる。オープンウェイトで配布されるため、ファインチューニングや商用組み込みの自由度も高い。一方で、専用エンコーダを捨てた構成が高解像度画像や細粒度の視覚タスクでどこまで通用するかは実運用での検証が要る。HNで994ポイントを集め、オープンモデル陣営の設計トレンドを占う一手として受け止められている。",
  "detail_en": "Google released the 12B version of its open Gemma 4 model. The headline is its 'encoder-free' design: where conventional multimodal models bolt a dedicated image encoder (e.g. a ViT) onto a language model and bridge the two, Gemma 4 handles images and text directly within a single unified model. That simplifies the pipeline and can cut information loss and the tuning overhead at the modality boundary. At 12B parameters it is tractable on local or single-GPU setups, broadening who can research and build with it, and being open-weight it allows fine-tuning and commercial embedding. The open question is how far dropping the dedicated encoder holds up on high-resolution or fine-grained visual tasks—something only real-world use will settle. With 994 points on Hacker News, it is being read as a signal of where open-model architecture is heading.",
  "key_points_ja": [
    "画像専用エンコーダを持たない統合設計",
    "テキストと画像を単一モデルで直接処理",
    "12Bでローカル/単一GPUでも扱いやすい",
    "オープンウェイトで改変・商用が自由",
    "高解像度/細粒度視覚での実力は要検証",
    "HN994点、オープン勢の設計潮流を示唆"
  ],
  "key_points_en": [
    "Unified design with no dedicated image encoder",
    "Handles text and images in one model directly",
    "12B size runs on local/single-GPU setups",
    "Open weights: free to fine-tune and embed",
    "High-res/fine-grained vision still to be proven",
    "994 HN points; signals open-model direction"
  ]
 },
 {
  "source": "HN / Anthropic",
  "title": "When AI Builds Itself: Our progress toward recursive self-improvement",
  "title_ja": "AIが自分自身を作るとき:再帰的自己改善に向けた我々の進捗",
  "url": "https://www.anthropic.com/institute/recursive-self-improvement",
  "hot_take_ja": "『AIがAIの研究開発を加速し、それがさらに速いAIを生む』という再帰的自己改善(RSI)を、抽象論ではなく計測対象として扱い始めたのが重要。臨界点を煽るのではなく、どこまで来たかを定量化しようという姿勢は、安全議論を地に足のついたものにする。",
  "detail_ja": "Anthropicが、AIがAI自身の研究開発を加速させる『再帰的自己改善(Recursive Self-Improvement, RSI)』の現状についての見解を公開した。RSIは、AIがより優れたAIを作る作業を担い、その成果がさらに能力の高いAIを生む正のフィードバックループを指す。これはAI安全論で長く語られてきた概念だが、本記事の要点は、それを思弁ではなく『今どの程度進んでいるか』を測る対象として扱おうとする点にある。具体的には、コード生成・実験設計・モデル評価といったAI研究の各工程をAIがどれだけ自動化・高速化できているかを指標化し、加速の度合いを追跡する。完全自律のRSIにはまだ距離があるが、人間研究者の生産性を底上げする『半自律』の段階は既に進行中だという認識を示す。重要なのは、こうした能力が予期せず急加速する可能性に備え、計測とガードレールを先回りで整える必要があるという主張だ。HNでも議論を呼び、フロンティアAIの臨界点を巡る現実的な指標づくりとして注目されている。",
  "detail_en": "Anthropic published its view on the state of recursive self-improvement (RSI)—the loop in which AI accelerates the research and development of better AI, whose output in turn yields still more capable AI. RSI is a long-standing idea in AI safety, but the article's contribution is to treat it not as speculation but as something to measure: how far along are we, really. It proposes tracking how much AI already automates and speeds up the stages of AI research—code generation, experiment design, model evaluation—and quantifying the degree of acceleration. Fully autonomous RSI remains distant, but a 'semi-autonomous' phase that boosts human researchers' productivity is already underway. The core argument is that, because such capabilities could accelerate unexpectedly, measurement and guardrails should be put in place ahead of time. It drew debate on Hacker News as a grounded attempt to build real indicators for the critical-point discussion around frontier AI.",
  "key_points_ja": [
    "RSI=AIがより良いAIを作る正のループ",
    "思弁でなく『今どこまで来たか』を計測",
    "コード生成・実験設計・評価の自動化度を指標化",
    "完全自律は先、だが半自律は既に進行中",
    "急加速に備え計測とガードレールを先回り",
    "フロンティア安全議論を地に足のついた形に"
  ],
  "key_points_en": [
    "RSI: positive loop of AI building better AI",
    "Measures 'how far' rather than speculating",
    "Tracks automation of coding, experiments, eval",
    "Full autonomy distant; semi-autonomy here now",
    "Build measurement and guardrails ahead of time",
    "Grounds the frontier-safety debate in metrics"
  ]
 },
 {
  "source": "HN / Daily Cal",
  "title": "Failing grades soar as AI usage grows, math skills dwindle in UC Berkeley CS",
  "title_ja": "AI利用増で落第急増、UCバークレーCSで数学力低下を教員が指摘",
  "url": "https://www.dailycal.org/news/campus/academics/failing-grades-soar-as-professors-see-greater-ai-usage-dwindling-math-skills-in-uc-berkeley/article_16fad0bf-02cb-4b8c-8d88-888ffd9f8608.html",
  "hot_take_ja": "『AIで勉強がはかどる』の逆。手を動かして詰まる過程を飛ばすと、試験で効く基礎数学が身につかない——という現場の声だ。トップ校のCSで落第が増えているという事実は、AI時代の学習設計を真剣に問い直させる。",
  "detail_ja": "UCバークレーのコンピュータサイエンス講義で、学生のAI利用拡大と並行して落第が急増し、基礎的な数学力の低下が見られると教員らが報告している。背景にあるのは、課題をAIに解かせることで『答えは出るが、自分では導出できない』状態が広がっているという懸念だ。プログラミングや数学は、自力で詰まり、試行錯誤する過程そのものが理解を作る。AIがその摩擦を肩代わりすると、表面的には進捗しているように見えても、試験のように自力が問われる場面で破綻する。記事は特定教員の体感に基づくもので統計的因果を厳密に立証したわけではないが、AIが学習を助けるのか損なうのかという議論に具体的なデータ点を加えた。注意すべきは、これは『AIを使うな』ではなく、AIを前提にカリキュラムや評価をどう再設計するかという問題提起である点だ。663ポイントを集め、教育とAIの緊張関係を象徴する話題として広く議論された。",
  "detail_en": "Professors in UC Berkeley's computer science courses report that failing grades have soared alongside growing student AI use, with a visible decline in basic math skills. The worry is a spread of the 'the answer appears but I can't derive it myself' state caused by handing assignments to AI. In programming and math, the very process of getting stuck and working through it is what builds understanding; when AI absorbs that friction, progress can look fine on the surface yet collapse when students must perform unaided, as in exams. The article rests on faculty observation rather than a rigorous causal study, but it adds a concrete data point to the debate over whether AI helps or harms learning. Importantly, the framing is not 'don't use AI' but how to redesign curricula and assessment around it. With 663 points, it became a flashpoint for the tension between education and AI.",
  "key_points_ja": [
    "AI利用拡大と並行し落第が急増",
    "『答えは出せても自力で導けない』状態",
    "詰まる過程の省略で基礎数学が定着せず",
    "試験など自力が問われる場で破綻",
    "教員の体感ベースで厳密な因果証明ではない",
    "問いは『使うな』でなく評価の再設計"
  ],
  "key_points_en": [
    "Failing grades soar alongside rising AI use",
    "'Get the answer but can't derive it' state",
    "Skipping the struggle erodes core math",
    "Breaks down when unaided, e.g. exams",
    "Faculty observation, not a causal study",
    "Question is redesigning assessment, not banning"
  ]
 },
 {
  "source": "HN / kasra.blog",
  "title": "I built a vulnerable app and spent $1,500 seeing if LLMs could hack it",
  "title_ja": "脆弱なアプリを作り1,500ドル投じてLLMがハッキングできるか検証した",
  "url": "https://kasra.blog/blog/i-spent-1500-seeing-if-llms-could-hack-my-app/",
  "hot_take_ja": "『LLMはハッカーになれるか』を、雰囲気でなく実費1,500ドルの実験で測った労作。どこまで自動で侵入でき、どこで詰まるかが具体的に分かるのが価値。AI攻撃の現実的な脅威レベルを冷静に見積もる材料になる。",
  "detail_ja": "あるエンジニアが、意図的に脆弱性を仕込んだWebアプリを用意し、約1,500ドル分のLLM API実行を費やして『LLMは実際にこのアプリを攻撃・侵入できるのか』を体系的に検証したブログが話題を集めた。結果はニュアンスに富む。LLMは既知の脆弱性パターン(SQLインジェクション、認可不備、設定ミス等)の発見や、定型的な攻撃手順の実行では有用な働きを見せる一方、複数ステップにわたる連鎖や、文脈を保ったまま試行錯誤を続ける長時間タスクでは脱線・幻覚・コスト爆発が起きやすい。重要なのは、これが『LLMは万能ハッカー』でも『役立たず』でもなく、その中間のリアルな能力曲線を実費データで描き出した点だ。防御側にとっては、AIによる自動偵察・自動エクスプロイトが現実の脅威になりつつある一方、まだ人間の戦略性が優位を保つ領域も明確だと分かる。攻撃の自動化が安価になるほど、基本的なセキュリティ衛生(入力検証・最小権限・監視)の重要性が増すという実務的教訓も読み取れる。HN356ポイント。",
  "detail_en": "An engineer built a deliberately vulnerable web app and spent roughly $1,500 in LLM API calls to systematically test whether LLMs could actually attack and break into it. The results are nuanced: LLMs are useful at spotting known vulnerability patterns (SQL injection, broken authorization, misconfigurations) and executing routine attack steps, but they tend to derail, hallucinate, and blow up in cost on multi-step chains and long-horizon tasks that require sustained, context-aware trial and error. The value is that this isn't 'LLMs are omnipotent hackers' or 'useless'—it traces the real capability curve in between, with hard cost data. For defenders, it shows that AI-driven automated recon and exploitation is becoming a genuine threat, while areas where human strategic reasoning still dominates remain identifiable. The practical lesson: as automated attacks get cheaper, basic security hygiene—input validation, least privilege, monitoring—matters more, not less. 356 points on HN.",
  "key_points_ja": [
    "脆弱アプリ+実費1,500ドルで攻撃力を実測",
    "既知パターン発見や定型手順では有用",
    "多段の連鎖や長時間タスクで脱線・幻覚・高コスト",
    "『万能』でも『無能』でもない中間の能力曲線",
    "自動偵察・自動侵入は現実の脅威に",
    "基本のセキュリティ衛生の重要性が増す"
  ],
  "key_points_en": [
    "Vulnerable app + $1,500 to measure real capability",
    "Useful at known patterns and routine steps",
    "Derails/hallucinates/costly on long multi-step chains",
    "Neither omnipotent nor useless—a real middle curve",
    "Automated recon and exploitation now a real threat",
    "Basic security hygiene matters more, not less"
  ]
 },
 {
  "source": "Blog / OpenAI",
  "title": "Dreaming: Better memory for a more helpful ChatGPT",
  "title_ja": "Dreaming:より役立つChatGPTのための新しいメモリ",
  "url": "https://openai.com/index/chatgpt-memory-dreaming",
  "hot_take_ja": "会話の合間にChatGPTが記憶を『寝かせて整理する』という発想が面白い。人間が睡眠で記憶を固定するのに着想を得た設計で、過去の断片を統合し直すことで、長く使うほど文脈が散らからず賢くなることを狙う。メモリ競争の新局面。",
  "detail_ja": "OpenAIがChatGPTの新しいメモリ機構『Dreaming』を発表した。従来のメモリは会話から事実を抜き出して保存する仕組みだったが、断片が増えると重複・矛盾・陳腐化が起き、文脈が散らかりやすいという課題があった。Dreamingは、人間が睡眠中に記憶を整理・固定するプロセスに着想を得て、会話の合間(アクティブでない時間)に蓄えた記憶を再処理・統合し、重要なものを残して関連付け直す。これにより、ユーザーの好みや文脈を新鮮に保ち、会話をまたいで一貫性のある応答ができることを狙う。ポイントは、メモリを『単なる保存』から『継続的に手入れされる動的な知識』へと位置づけ直した点だ。長期利用でこそ効く設計であり、パーソナルアシスタントの価値が『どれだけ覚えているか』から『どれだけ整理して使えるか』へ移りつつあることを示す。一方で、何を保持し何を捨てるかの判断はプライバシーや誤った記憶の固定化というリスクもはらむため、透明性とユーザー制御が鍵になる。各社が競うAIメモリ領域で、機構面の差別化を打ち出す一手だ。",
  "detail_en": "OpenAI introduced a new ChatGPT memory mechanism called 'Dreaming.' Earlier memory simply extracted and stored facts from conversations, but as fragments pile up they bring duplication, contradiction, and staleness, cluttering context. Inspired by how humans consolidate memory during sleep, Dreaming reprocesses and integrates stored memories during idle periods between conversations, keeping what matters and re-linking it. The goal is to keep a user's preferences and context fresh and to deliver consistent responses across sessions. The key shift is recasting memory from 'mere storage' to 'continuously curated, dynamic knowledge.' It pays off most in long-term use and signals that the value of a personal assistant is moving from how much it remembers to how well it organizes and applies what it remembers. At the same time, deciding what to keep or discard carries privacy risks and the danger of cementing wrong memories, so transparency and user control are crucial. It is a mechanism-level differentiator in the increasingly competitive AI-memory space.",
  "key_points_ja": [
    "会話の合間に記憶を再処理・統合する新機構",
    "人間の睡眠による記憶固定に着想",
    "重複・矛盾・陳腐化で散らかる課題に対応",
    "好み/文脈を新鮮に保ち会話をまたぎ一貫",
    "『保存』から『手入れされる動的知識』へ",
    "保持判断のプライバシーと透明性が鍵"
  ],
  "key_points_en": [
    "New mechanism reprocesses/integrates memory when idle",
    "Inspired by human sleep-time consolidation",
    "Tackles clutter from duplication and staleness",
    "Keeps preferences fresh, consistent across sessions",
    "Shifts memory from storage to curated knowledge",
    "Retention decisions raise privacy/transparency needs"
  ]
 },
]

raw["stats"]["highlights"] = len(raw["highlights"])
out = base / "data/2026-06-04.json"
json.dump(raw, open(out, "w"), ensure_ascii=False, indent=2)
print("wrote", out, "highlights", len(raw["highlights"]))
