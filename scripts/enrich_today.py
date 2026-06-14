#!/usr/bin/env python3
"""Enrich raw-2026-06-15.json with Japanese/English summaries + highlights."""
import json
from pathlib import Path

DATE = "2026-06-15"
data_dir = Path(__file__).resolve().parent.parent / "data"
raw = json.load(open(data_dir / f"raw-{DATE}.json", encoding="utf-8"))
s = raw["sources"]

# ---- arXiv (top 25) ----
arxiv = {
0: ("EvoArena: 動的環境でのLLMエージェントの記憶進化を追跡",
    "環境が段階的に変化する状況でエージェントを評価するベンチマーク。記憶を構造化された更新履歴として記録し、環境進化への適応力を測る。静的評価では見えない「知識の陳腐化」への頑健性を可視化する。"),
1: ("類推による推論をRAG型強化ファインチューニングで学習",
    "意味的に似た問題が必ずしも同じ解法を必要としない点に着目し、解法戦略の類似性で事例を検索して強化学習する手法。表層が違っても解き方が共通する問題から学べるようにする。"),
2: ("InterleaveThinker: テキストと画像を交互生成する強化学習",
    "単一画像生成しかできない既存モデルの制約を超え、テキストと画像を交互に出力する「インターリーブ生成」を強化学習で実現。視覚的ナラティブや手順説明、身体性タスクへの応用を狙う。"),
3: ("Mana: 関節を持つ道具の器用な操作",
    "ハサミやペンチのように内部に可動関節を持つ道具を、接触の多い操作で扱うロボット学習。剛体に偏っていた従来研究を関節付き道具へ拡張し、機能的な使い方を学習する。"),
4: ("Flow Reversal Steeringでロボット汎用方策を改善",
    "フローマッチング型の汎用ロボット方策から、直接指令では失敗する難タスクの適切な行動を逆向きに推論して引き出す手法。事前学習した豊かな行動分布を有効活用する。"),
5: ("Modality Forcing: スケーラブルな空間生成",
    "テキスト→画像モデルが内部に持つ幾何・遠近・スケールの事前知識を活用し、密な深度データなしで奥行き予測や乱雑なシーン生成を行う簡潔な手法。"),
6: ("RepWAM: 表現中心の世界行動モデル",
    "従来の世界モデルが流用する再構成志向の動画トークナイザを脱し、行動予測に有用な表現を学ぶ視覚-行動トークナイザを提案。見た目の忠実度より制御に役立つ表現を重視する。"),
7: ("SpatialClaw: 空間推論エージェントの行動インターフェース再考",
    "VLMの空間推論を補強するツール拡張で、ボトルネックは知覚モジュールよりも『行動インターフェース』にあると指摘。3Dでの位置・関係・動きの推論を改善する新たな操作設計。"),
8: ("WEAVER: ロボット操作のための高性能世界モデル",
    "方策評価・改善・計画を少ない実機操作で可能にする世界モデル。忠実度・長期一貫性・速度を同時に満たすことを目指し、シミュレータとしての実用性を高める。"),
9: ("グラフニューラルネット向け切り捨て位置エンコーディングの理解",
    "スペクトル系と歩行(walk)系の位置エンコーディングは理論上等価だが、次数を切り捨てた際の表現力差を分析。GNN設計での実用的な選択指針を与える。"),
10: ("LLMで社会・行動科学の再現性評価を自動化",
    "本来は別の研究者が元データを再分析して行う再現性検証を、LLMが自動化できることを示す。コストが高くスケールしない検証作業を肩代わりする可能性を提示。"),
11: ("Agents-K1: エージェントネイティブな知識オーケストレーション",
    "論文を要約と引用エッジに還元してしまう既存研究の限界を超え、エンティティ・主張・証拠・手法系譜まで構造化して科学推論に使う知識編成フレームワーク。"),
12: ("Influcoder: デコーダの勾配影響ランキングをエンコーダに蒸留",
    "学習データの各サンプルが出力に与える影響(データ帰属)を、重いデコーダ計算からエンコーダへ蒸留して高速に推定。高品質データ選別の効率化を狙う。"),
13: ("HyperTool: ステップ単位を超えたツール拡張エージェント",
    "原子的なツール呼び出しを毎回推論トレースに展開すると文脈を浪費する問題に対し、決定論的なツールワークフローをまとめて扱い実行粒度の不整合を解消する。"),
14: ("EurekAgent: 自律的科学発見にはエージェント環境設計が全て",
    "最適化指標と実行環境を与えればエージェントは仮説提案・検証・反復ができるが、真のボトルネックは『環境エンジニアリング』だと主張。環境設計を自動化する。"),
15: ("Before You Think: System 0とAIによる『認知の植民地化』",
    "AIが思考の『前段(System 0)』として無意識に判断を方向づけ、外部の利害を自己の認知構造に埋め込む『認知の植民地化』を論じる。すでに広く使われている点で危険だと警告する哲学・認知科学論文。"),
16: ("密な教師・疎な更新: On-policy蒸留の幾何とスパース性",
    "オンポリシー生徒軌跡と密な教師信号を組み合わせる蒸留が、モデルのパラメータをどう変えるかを分析。更新が疎で特定の幾何構造を持つことを複数のモデル対で示す。"),
17: ("Flex4DHuman: 単眼動画から4D人体を再構成する多視点動画拡散",
    "スケルトンや深度に頼らず、相対カメラ姿勢だけで単眼/疎な多視点動画を同期した密な多視点動画に変換し4D人体を再構成する拡散モデル。"),
18: ("World Tracing: 見えない領域まで生成するピクセル整合な3D幾何",
    "深度推定は入力ピクセルに忠実だが可視面で止まり、画像→3Dは完全だが位置ずれする——両者の弱点を、ピクセル整合のまま不可視部分も生成する表現で解消する。"),
19: ("Operadic consistency: 合成推論の失敗を検知するラベル不要の信号",
    "正解ラベルなしでLLMの推論失敗を見抜く新手法。オペラッド理論(反復代入の数学)に基づき、自己一貫性やエントロピーとは別軸の合成的な整合性を測る。"),
20: ("SkMTEB: スロバキア語の大規模テキスト埋め込みベンチマーク",
    "低資源の西スラブ語スロバキア語向けに初の包括的MTEB型ベンチを構築。31データセット・7タスクで31モデルを評価し、多言語モデルの実力を検証する。"),
21: ("Surflo: 大域状態を持つ一貫した3D表面フローモデル",
    "幾何は視点不変という性質を活かし、視点ごとにバラバラな点群を出す従来法を超えて、入力枚数に依存しない一貫した3D状態を復元する。"),
22: ("Recursive Agent Harnesses(再帰的エージェントハーネス)",
    "モデル呼び出しを再帰させる長文脈推論(RLM)と、サブエージェントを大量生成する実運用コーディングエージェント——Anthropicの動的ワークフローを含む両者に共通する『再帰的ハーネス』パターンを命名・分析する。"),
23: ("安定回復多様体: 継続学習における回復可能性の幾何原理",
    "破滅的忘却を『知識の破壊』ではなく回復可能性の幾何構造として捉え直す。Split CIFAR-100とResNet-18で、忘れた知識がどの程度回復可能かを解析。"),
24: ("LLMの合成推論のためのオペラッド",
    "複雑な質問を部分質問に分解して答えを合成する戦略に、厳密な数学的基盤がないという問題に対し、多入力1出力の操作をモデル化するオペラッドを導入する。"),
}

# ---- HN ----
hn = {
0: ("AmazonのCEOが米当局と協議、Anthropicモデルへの規制を誘発(WSJ)",
    "WSJ報道。Amazon CEOと米当局の協議が、Anthropicの最新モデル(Fable 5/Mythos 5)停止につながる規制強化の引き金になったとされる。大手クラウド事業者の政治的働きかけがAI規制を動かした構図が問題視されている。"),
1: ("GLM 5.2 がリリース",
    "智譜AI(Zhipu)がGLM 5.2を公開。中国製オープンウェイトモデルの最新版で、コーディングや推論性能の向上が注目されている。"),
2: ("英警察官、複数事件でAIによる『証拠捏造』を捜査される",
    "ダービーシャー州警察の警官が、AIを使って証拠を『作成』した疑いで複数事件にわたり捜査対象に。司法分野でのAI悪用という新たなリスクを浮き彫りにする。"),
3: ("『みんながAIを何にでも使っている』は事実ではない",
    "DuckDuckGo創業者Gabriel Weinbergによる反論。AI利用は一部ヘビーユーザーに偏り、多くの人は限定的にしか使っていないとデータで指摘。誇張された普及言説への冷や水。"),
4: ("家でAIコーディングを破産せずに行う方法",
    "ローカルやコスト効率の良い構成でAIコーディング環境を組む実践記事。高額なAPI課金に頼らず開発を回す工夫が支持を集めた。"),
5: ("OSSツールのリポジトリ、$7.3Mシード調達後に一夜でアーカイブ化",
    "TensorZeroが$7.3Mのシード資金調達後にリポジトリを突如アーカイブ。オープンソースと資金調達・商用化の緊張関係を象徴する出来事として議論に。"),
6: ("リオデジャネイロの『自製』LLM、実は既存モデルのマージだった疑い",
    "リオ市が誇る『国産』LLMが、既存モデルを統合(マージ)しただけではないかとGitHub上で指摘される。自前開発を装ったAIの真贋問題が話題に。"),
7: ("Show HN: Paca — 人間とAIの協働向け軽量Jira代替",
    "人間とAIエージェントが共同で作業する前提で設計された軽量プロジェクト管理ツール。AI時代のワークフローツールの方向性を示す。"),
8: ("Show HN: Kage — 任意のサイトを単一バイナリ化してオフライン閲覧",
    "任意のWebサイトを丸ごと単一バイナリに『影写し』してオフラインで閲覧できるツール。アーカイブやポータブル化の用途で注目。"),
9: ("Linux 7.1 リリース",
    "Linuxカーネル7.1がリリース。Torvaldsによるアナウンス。"),
10: ("KPMG、ハルシネーションが原因でAI利用レポートを撤回",
    "大手会計事務所KPMGが、AIで作成したとみられるレポートに虚偽情報(ハルシネーション)が見つかり撤回。AIを業務に使うコンサル自身がAIの欠陥に足をすくわれた皮肉な事例。"),
11: ("Orthodox C++ (2016)",
    "肥大化したモダンC++慣行に対し、シンプルで実用的なサブセットに絞る『正統派C++』を説く定番エッセイが再浮上。"),
12: ("Claudeを化学者にする(Making Claude a Chemist)",
    "Anthropicの研究記事。Claudeに化学の専門能力を持たせ、分子設計や反応予測などの科学タスクを支援させる取り組みを紹介する。"),
13: ("PwCレポート: AIが医療費を押し上げている",
    "PwCの分析で、AIの導入がむしろ医療費の上昇要因になっていると指摘。効率化が必ずしもコスト削減につながらない現実を示す。"),
14: ("Metaの混迷するAI戦略(Wired)",
    "Wired報道。社内メモなどから、ザッカーバーグ下でのMetaのAI戦略が一貫性を欠き混乱している様子が描かれる。"),
15: ("Weave: 行ではなく言語構造に基づくマージ",
    "テキストの行単位ではなく、言語の構文構造に基づいて差分をマージするツール。コード/文章のマージ衝突を減らすアプローチ。"),
16: ("Intel Kira Boyko氏インタビュー: Xeon 6の製品ディレクター",
    "Intelの新Xeon 6製品ディレクターへのインタビュー。サーバ向けCPU戦略やAIワークロード対応を語る。"),
17: ("Show HN: 終了前のFableで80個のミニゲームを作った",
    "サービス終了したFableを使って80本のミニゲームを制作したという作品集。短命だったモデルで何ができたかの記録として興味深い。"),
18: ("Show HN: RK3588SのNPUでデュアルYOLOv8nのUAV検出を42FPS",
    "エッジSoCのNPUを使い、ドローン検出をデュアルYOLOv8nで42FPS動作させた実装。省電力エッジ推論の好例。"),
19: ("KPMGのAIレポートが、AIハルシネーションの実演に",
    "撤回されたKPMGのAIレポートを巡る続報(The Register)。AI活用を喧伝する内容そのものがAIの捏造を露呈する結果になったと皮肉る。"),
}

# ---- GitHub ----
github = {
0: ("iptv-org/iptv — 世界中の公開IPTVチャンネル集",
    "世界各国の公開IPTVチャンネルを集約したリスト。AIとは直接関係ないが今日のトレンド上位。"),
1: ("NVIDIA/SkillSpector — AIエージェントのスキル用セキュリティスキャナ",
    "NVIDIA製。AIエージェントの『スキル』に潜む脆弱性・悪意あるパターン・セキュリティリスクを検出するスキャナ。エージェント拡張の安全性が新たな関心事になっていることを示し、本日962スターを獲得。"),
2: ("chatwoot/chatwoot — オープンソースの顧客対応プラットフォーム",
    "Intercom/Zendesk代替のOSSライブチャット・メール・オムニチャネルサポート基盤。AI連携サポートでも人気。"),
3: ("GorvGoyl/Clone-Wars — 人気サービスのOSSクローン集",
    "Airbnb・Netflix・TikTokなど人気サイトの100以上のOSSクローンをソース・デモ・技術スタック付きでまとめたリスト。"),
4: ("andrewyng/aisuite — 複数生成AIプロバイダの統一インターフェース",
    "Andrew Ng氏らによる、複数の生成AIプロバイダをシンプルに統一APIで扱えるライブラリ。プロバイダ切り替えを容易にする。"),
}

# ---- Blogs ----
blogs = {
0: ("olmo-eval: モデル開発ループ向け評価ワークベンチ",
    "AllenAIによる、モデル開発の反復に使える評価ワークベンチ。OLMo系の評価を効率化する。"),
1: ("OpenAI Academy、次世代の働き方向け新コース",
    "OpenAIが実務的なAIスキル習得・反復可能なワークフロー構築・エージェント活用を学ぶ3つのアカデミーコースを開講。"),
2: ("PreplyがAIと人間チューターを組み合わせて学習を個別化",
    "語学学習プラットフォームPreplyが、AIと人間のチューターを組み合わせて学習体験をパーソナライズする取り組み。"),
3: ("バージニア州での地域投資とエネルギー支援",
    "OpenAIによるバージニア州での雇用・エネルギー手頃化に向けた地域投資の発表。データセンター立地に伴う地域施策。"),
4: ("欧州の信頼できるAIエコシステム構築を支援",
    "OpenAIが欧州の信頼できるAIエコシステム整備への取り組みを支援すると表明。"),
5: ("天体物理学者がCodexでブラックホールのシミュレーションを支援",
    "ある天体物理学者がOpenAIのCodexを使い、ブラックホールのシミュレーション作業を効率化した事例。"),
6: ("BBVAがOpenAIと銀行業務の中核にAIを据える",
    "スペインの銀行BBVAがChatGPT Enterpriseを10万人規模に展開し、OpenAIと組んでAI銀行業務変革を加速。"),
7: ("OpenAIがOnaを買収",
    "OpenAIが開発者向けエージェント企業Onaを買収する。コーディング/エージェント領域の強化を狙う動き。"),
8: ("PyTorchでのプロファイリング(第2部): nn.Linearから融合MLPへ",
    "nn.Linearの素朴な実装から融合MLPまで、ボトルネックを計測して最適化する実践プロファイリング解説。"),
9: ("OracleクラウドのコミットメントでOpenAIモデルとCodexを利用",
    "Oracle Cloudの利用枠を通じてOpenAIモデルとCodexにアクセスできるようになるという提携。"),
10: ("中国系の影響工作が米国のAI論争を標的に(OpenAI報告)",
    "OpenAIの新報告。中国系(PRC-linked)の影響工作がAIを使い、米国のテック論争・データセンター・関税・ChatGPTに関する偽情報を標的に展開していると指摘。AI規制論争そのものが情報工作の舞台になっている。"),
11: ("LSEGが信頼できるAIをスケールさせる",
    "ロンドン証券取引所グループ(LSEG)が、データから意思決定までの信頼できるAI活用をスケールさせる取り組み。"),
12: ("Cohere、開発者向け初モデル North Mini Code を発表",
    "CohereがNorth Mini Codeを発表。同社初の開発者向けコーディングモデルとして、企業向けに展開する。"),
13: ("NextdoorのエンジニアがCodexで制約なく開発",
    "NextdoorのエンジニアがOpenAI Codexを使い開発速度を上げている事例紹介。"),
14: ("エージェントが2つのHugging Face Spaceを連鎖させて3Dパリギャラリーを構築",
    "AIエージェントが2つのHugging Face Spaceを自動で連鎖させ、3Dのパリのギャラリーを生成したデモ。Space同士のオーケストレーションの可能性を示す。"),
15: ("GitHub CIをHugging Face Jobsへ移行する",
    "GitHubのCIワークフローをHugging Face Jobsへ移行する方法の解説記事。"),
16: ("オープンソースコミュニティがエージェント型RL基盤OpenEnvを支持",
    "エージェント強化学習向けの環境標準OpenEnvを、OSSコミュニティが後押ししているという話題。"),
}

def apply(items, mp):
    for i, it in enumerate(items):
        if i in mp:
            tj, sj = mp[i]
            it["title_ja"] = tj
            it["summary_ja"] = sj

apply(s["arxiv"], arxiv)
apply(s["hn"], hn)
apply(s["github"], github)
apply(s["blogs"], blogs)

# ---- Highlights ----
raw["highlights"] = [
{
  "source": "Hacker News",
  "title": "KPMG pulls report on AI usage due to apparent hallucinations",
  "title_ja": "KPMG、AIのハルシネーションでAI活用レポートを撤回",
  "url": "https://techcrunch.com/2026/06/13/kpmg-pulls-report-on-ai-usage-hallucinations/",
  "hot_take_ja": "AI活用を企業に説いて回るコンサル自身が、AI生成レポートの捏造で赤っ恥。皮肉が効きすぎている。『人間が必ず検証する』というAI導入の大前提が、検証する側でこそ守られていないことを示す象徴的な失態だ。",
  "detail_ja": "大手会計・コンサルのKPMGが、AIの業務活用に関するレポートを公開後に撤回した。原因は、レポート内に存在しない出典や誤った事実、いわゆるハルシネーション(幻覚)が含まれていたことだ。AIを使って作成したとみられる文書が、検証されないまま外部に出てしまった構図である。AI導入を企業に推奨する立場のコンサルティング会社自身が、AI出力の信頼性管理に失敗した点が強く批判されている。生成AIは流暢で説得力のある文章を作る一方、存在しない引用や統計を平然と生成する性質があり、専門家のレビューを挟まないと致命的な誤りが残る。今回の件は、ツールの問題というより運用プロセス——『人間による最終検証』——の欠如が本質だ。同様の撤回はDeloitteなど他社でも報告されており、業界横断的な課題になりつつある。AIで生産性を上げるほど、検証コストを削りたくなる誘惑が強まるという構造的なジレンマを浮き彫りにしている。信頼が商品であるプロフェッショナルサービス業ほど、この失敗のダメージは大きい。",
  "detail_en": "KPMG, one of the Big Four accounting and consulting firms, withdrew a report on enterprise AI adoption after publication. The reason: the document contained hallucinations — fabricated citations and incorrect facts that did not exist in reality. A document apparently produced with AI assistance went out the door without proper verification. The irony is sharp: a consultancy that advises clients on deploying AI failed at managing the reliability of AI output itself. Generative models produce fluent, persuasive prose but will confidently invent nonexistent references and statistics, so without expert review fatal errors slip through. The core failure here is less about the tool than about the operational process — the missing 'human-in-the-loop' final check. Similar retractions have been reported at other firms such as Deloitte, making this a cross-industry problem. It highlights a structural dilemma: the more you lean on AI for productivity, the stronger the temptation to cut the verification cost that makes the output trustworthy. For professional-services firms whose entire product is trust, the reputational damage from this kind of slip is especially severe.",
  "key_points_ja": [
    "KPMGがAI活用レポートを公開後に撤回",
    "原因は存在しない出典・事実誤認=ハルシネーション",
    "AI導入を勧める側がAIの欠陥に足をすくわれた",
    "本質はツールでなく『人間の最終検証』の欠如",
    "Deloitte等でも同様の撤回が報告され業界課題に",
    "信頼が商品のコンサルほどダメージが大きい"
  ],
  "key_points_en": [
    "KPMG pulled an AI-adoption report after publishing",
    "Cause: fabricated citations and false facts (hallucinations)",
    "Firm that sells AI advice tripped on AI's flaws",
    "Root issue is missing human verification, not the tool",
    "Similar retractions reported at Deloitte and others",
    "Trust-based consultancies suffer the most reputational damage"
  ]
},
{
  "source": "Hacker News",
  "title": "No, everyone is not using AI for everything",
  "title_ja": "いや、みんながAIを何にでも使っているわけではない",
  "url": "https://gabrielweinberg.com/p/people-are-consuming-ai-like-they",
  "hot_take_ja": "DuckDuckGo創業者が、AI普及の誇張に冷や水。利用は一部のヘビーユーザーに激しく偏り、世間の大半は『たまに触る』程度というデータを突きつける。バブル的な万能論ではなく、消費の実態に即した冷静な普及曲線を見るべきだという主張だ。",
  "detail_ja": "DuckDuckGo創業者のGabriel Weinbergが、『誰もがあらゆる場面でAIを使っている』という言説に対し、データに基づく反論を展開した。彼の論点は、AI利用がごく一部のヘビーユーザーに極端に集中しており、利用頻度の分布は非常に偏っている、というものだ。多くの人はAIを日常の中心に据えているわけではなく、ときどき検索や下書きに使う程度にとどまる。これは新メディアの消費パターンとして珍しいことではなく、テレビや動画と同様に『ごく一部が大半の利用時間を生む』べき乗則的な分布に従う。誇張された普及言説は、ベンダーや投資家が市場規模を大きく見せたい動機と結びつきやすく、ユーザー数(MAU)と実際のエンゲージメントの乖離を見落とさせる。Weinbergは、普及の伸びそのものは認めつつも、『全員が全部AI化している』という前提で製品戦略や政策を立てるのは危険だと示唆する。実態を直視すれば、まだ多くの人にとってAIは選択肢の一つにすぎず、習慣として定着するにはUX・信頼・コストの壁が残っている。過熱した期待を一段冷ます、健全な現実チェックの記事だ。",
  "detail_en": "Gabriel Weinberg, founder of DuckDuckGo, pushed back with data against the narrative that 'everyone is using AI for everything.' His point: AI usage is heavily concentrated among a small set of power users, and the frequency distribution is extremely skewed. Most people do not put AI at the center of their day — they reach for it occasionally to search or draft something. This is unremarkable as a media-consumption pattern; like TV or video, it follows a power-law in which a small minority generates most of the usage time. Inflated adoption narratives align neatly with the incentives of vendors and investors to make the market look bigger, and they obscure the gap between headline monthly-active-user counts and real engagement. Weinberg acknowledges that adoption is genuinely growing, but warns it is risky to build product strategy or policy on the assumption that 'everyone has AI-ified everything.' Facing the reality, for many people AI is still just one option among several, and UX, trust, and cost barriers remain before it becomes a durable habit. It is a healthy reality check that cools the overheated hype by a notch.",
  "key_points_ja": [
    "DuckDuckGo創業者がAI普及の誇張に反論",
    "利用は一部のヘビーユーザーに極端に集中",
    "大半は『たまに使う』程度でべき乗則的分布",
    "MAUと実エンゲージメントの乖離を指摘",
    "『全員全部AI化』前提の戦略は危険",
    "定着にはUX・信頼・コストの壁が残る"
  ],
  "key_points_en": [
    "DuckDuckGo founder rebuts AI-hype narrative",
    "Usage heavily concentrated among power users",
    "Most people use it occasionally; power-law distribution",
    "Gap between MAU headlines and real engagement",
    "Risky to plan around 'everyone AI-ifies everything'",
    "UX, trust, cost barriers remain before habit forms"
  ]
},
{
  "source": "Hacker News",
  "title": "Rio de Janeiro's \"homegrown\" LLM appears to be a merge of an existing model",
  "title_ja": "リオの『国産』LLM、実は既存モデルのマージだった疑い",
  "url": "https://github.com/nex-agi/Nex-N2/issues/4",
  "hot_take_ja": "『独自開発の国産LLM』を謳ったモデルが、既存オープンウェイトを統合(マージ)しただけではないかとGitHub上で暴かれた。重みの指紋は隠せない。ナショナル/シティAIの旗を掲げる流れの中で、こうした“見せかけの自製”がどれだけあるかを問う一件だ。",
  "detail_ja": "リオデジャネイロ発の『自製(homegrown)』を謳うLLM(Nex-N2)について、実体は既存のオープンウェイトモデルを統合(モデルマージ)しただけではないか、という指摘がGitHubのissueで提起された。モデルマージとは、複数の学習済みモデルの重みを数式的に混ぜ合わせて新しいモデルを作る手法で、ゼロからの事前学習に比べ計算コストが桁違いに小さい。問題は、それ自体は正当な技術である一方、『独自に一から開発した』と説明すれば誇大広告・出自の偽装になりうる点だ。技術的には、トークナイザの一致、重みの統計的な指紋、特定プロンプトでの既存モデル特有の振る舞いなどから、ベースモデルの素性はかなり高い精度で推定できる。今回の指摘もそうした証跡に基づくとみられる。背景には、各国・各都市が『主権AI』『地場のLLM』を政治的アピールとして打ち出す潮流があり、成果を急ぐあまり実態と説明が乖離するケースが出ている。オープンウェイトの再利用は歓迎すべきだが、由来の透明性(どのモデルをベースに、何を足したのか)を欠けば信頼を損なう。AIの『国産』表明は、重みレベルでの検証にさらされる時代になったことを示す事例だ。",
  "detail_en": "A GitHub issue alleges that an LLM from Rio de Janeiro (Nex-N2) marketed as 'homegrown' is in reality just a merge of an existing open-weight model. Model merging mathematically blends the weights of several trained models into a new one, at a tiny fraction of the compute of pretraining from scratch. The technique is perfectly legitimate in itself — the problem is that calling the result 'developed independently from the ground up' becomes false advertising and provenance laundering. Technically, the lineage of a base model can be inferred with high confidence from tokenizer matches, statistical fingerprints in the weights, and base-model-specific behaviors on certain prompts; the allegation appears to rest on exactly this kind of evidence. The backdrop is a wave of countries and cities touting 'sovereign AI' or a 'local LLM' as a political talking point, where the rush to show results can open a gap between reality and the marketing. Reusing open weights is welcome, but without transparency about provenance — which model it is based on and what was added — it erodes trust. The episode shows that 'made here' claims about AI are now subject to verification at the level of the weights themselves.",
  "key_points_ja": [
    "リオの『国産LLM』が既存モデルのマージと指摘",
    "マージは正当な技術だが『一から開発』は誇大",
    "トークナイザ・重みの指紋でベースは推定可能",
    "背景に各都市の『主権AI』政治アピール",
    "オープンウェイト再利用は出自の透明性が要",
    "AIの自製主張は重みレベルで検証される時代に"
  ],
  "key_points_en": [
    "Rio's 'homegrown LLM' alleged to be a model merge",
    "Merging is legit, but 'built from scratch' is overclaim",
    "Base model inferable from tokenizer & weight fingerprints",
    "Backdrop: cities touting 'sovereign AI' politically",
    "Open-weight reuse needs provenance transparency",
    "'Made-here' AI claims now verified at weight level"
  ]
},
{
  "source": "GitHub Trending",
  "title": "NVIDIA/SkillSpector — Security scanner for AI agent skills",
  "title_ja": "NVIDIA SkillSpector — AIエージェントのスキル用セキュリティスキャナ",
  "url": "https://github.com/NVIDIA/SkillSpector",
  "hot_take_ja": "エージェントの『スキル』が攻撃面になる時代に、NVIDIAが専用のセキュリティスキャナを出してきた。1日で約960スター。プロンプトインジェクションや悪意あるスキルが現実の脅威になり、『エージェントのアンチウイルス』が必要とされ始めている兆候だ。",
  "detail_ja": "NVIDIAが、AIエージェントの『スキル』(エージェントが読み込んで実行する拡張機能やツール定義)に潜む脆弱性・悪意あるパターン・セキュリティリスクを検出するスキャナ『SkillSpector』を公開し、本日のGitHubトレンドで約960スターを集めた。背景には、ClaudeのスキルやMCPサーバ、各種プラグインのように、エージェントが外部から取り込んだ指示やコードを実行する仕組みが急速に普及し、それ自体が新しい攻撃面になっている事情がある。具体的な脅威としては、スキルの説明文や同梱ファイルに隠した間接プロンプトインジェクション、認証情報の窃取、外部へのデータ送信、過剰な権限要求などが挙げられる。SkillSpectorはこうしたスキルを静的に解析し、危険なパターンを洗い出すことを狙う——いわば『エージェント版のアンチウイルス/SAST』だ。重要なのは、従来のソフトウェアサプライチェーン問題が、自然言語の指示やツール定義という新しい形で再来している点である。エージェントが自律的に多数のスキルを取り込むほど、人間が中身を一つずつ確認するのは非現実的になり、自動スキャンの必要性が高まる。大手であるNVIDIAがこの領域にツールを出したこと自体、エージェントセキュリティが研究の話題から実運用の必須事項へ移りつつあることを示している。一方で、静的解析は巧妙に難読化された悪意や実行時の挙動を完全には捉えられず、銀の弾丸ではない点には注意が必要だ。",
  "detail_en": "NVIDIA released SkillSpector, a scanner that detects vulnerabilities, malicious patterns, and security risks in AI agent 'skills' — the extensions and tool definitions that agents load and execute — and it drew roughly 960 stars on today's GitHub trending. The context: mechanisms like Claude skills, MCP servers, and various plugins, where an agent ingests and runs externally supplied instructions or code, are spreading fast and have themselves become a new attack surface. Concrete threats include indirect prompt injection hidden in a skill's description or bundled files, credential theft, data exfiltration, and excessive permission requests. SkillSpector aims to statically analyze such skills and surface dangerous patterns — essentially an 'antivirus/SAST for agents.' The key point is that the classic software supply-chain problem is returning in a new form: natural-language instructions and tool definitions. The more autonomously an agent pulls in many skills, the less realistic it is for a human to vet each one, raising the need for automated scanning. That a major vendor like NVIDIA is shipping tooling here signals that agent security is moving from a research topic to an operational necessity. At the same time, static analysis cannot fully capture cleverly obfuscated malice or runtime behavior, so it is no silver bullet.",
  "key_points_ja": [
    "NVIDIAがエージェントのスキル用セキュリティスキャナを公開",
    "1日で約960スターを獲得",
    "スキル=新たな攻撃面(間接インジェクション等)",
    "認証情報窃取・データ送信・過剰権限を検出",
    "『エージェント版アンチウイルス/SAST』の発想",
    "静的解析は万能でなく難読化や実行時挙動は限界"
  ],
  "key_points_en": [
    "NVIDIA ships a security scanner for agent skills",
    "~960 stars on GitHub in a single day",
    "Skills are a new attack surface (indirect injection)",
    "Detects credential theft, exfiltration, over-permissioning",
    "An 'antivirus/SAST for agents' concept",
    "Static analysis is no silver bullet vs. obfuscation/runtime"
  ]
},
{
  "source": "Company Blog (OpenAI)",
  "title": "PRC-linked influence operations are targeting AI debates in the US",
  "title_ja": "中国系の影響工作が米国のAI論争を標的に(OpenAI報告)",
  "url": "https://openai.com/index/prc-linked-influence-operations-ai-debates",
  "hot_take_ja": "OpenAIが、中国系の影響工作がAIを使って米国のAI政策論争そのものを揺さぶっていると報告。データセンター・関税・オープンソース論争が情報工作の戦場になっている。AIの規制をめぐる議論が、AIで操作されるという入れ子構造だ。",
  "detail_ja": "OpenAIが脅威レポートを公開し、中国系(PRC-linked)とされる影響工作が、米国内のAIをめぐる政策論争を標的に展開していると報告した。具体的には、データセンターの立地・電力をめぐる世論、関税政策、そしてChatGPTに関する虚偽の主張などが、生成AIを使って増幅・操作されているという。重要なのは、これらの工作がAI技術そのものを道具として使い、AIの規制やオープンソース化といった『AIの未来を決める議論』に介入している入れ子構造だ。前日のニュースで話題になった『Open source AI must win(オープンソースAIが勝たねば)』のような言説が、純粋な技術コミュニティの声なのか、それとも特定国家の戦略的利益に沿って増幅されたものなのかを見分けにくくしている。手口としては、本物の論者になりすましたアカウント群が、もっともらしい主張を大量に投下し、特定の政策方向(例えば輸出規制の緩和や、ある陣営への不信)へ世論を誘導するというパターンが典型だ。OpenAIのようなプラットフォーム側がこうした活動を検知・公開すること自体は前進だが、検知と生成のいたちごっこは続く。受け手側のリテラシー——『誰がなぜこの主張を広めているのか』を問う習慣——がこれまで以上に重要になる。AI政策の議論を読むとき、その議論自体が操作対象になりうるという二重の警戒が必要だと突きつける報告だ。",
  "detail_en": "OpenAI published a threat report stating that influence operations described as PRC-linked are targeting AI policy debates inside the United States. Specifically, public opinion around data-center siting and power, tariff policy, and false claims about ChatGPT are being amplified and manipulated using generative AI. The crucial part is the nested structure: these operations use AI as a tool to intervene in the very debates that will decide AI's future, such as regulation and open-sourcing. It makes narratives like the 'Open source AI must win' framing that trended the day before harder to read — is it the authentic voice of a technical community, or amplified in line with a particular state's strategic interests? A typical playbook is clusters of accounts impersonating genuine commentators that flood plausible-sounding claims to steer opinion toward a specific policy direction — for example, loosening export controls or seeding distrust of one camp. It is progress that a platform like OpenAI detects and discloses such activity, but the cat-and-mouse game between detection and generation continues. Audience literacy — the habit of asking 'who is spreading this claim, and why' — matters more than ever. The report drives home a double caution: when you read AI-policy arguments, the argument itself may be the target of manipulation.",
  "key_points_ja": [
    "OpenAIが中国系の影響工作を脅威報告",
    "データセンター・関税・ChatGPT偽情報を標的",
    "AIを道具にAI政策論争へ介入する入れ子構造",
    "『オープンソースAI必勝』言説の真偽を曖昧化",
    "なりすまし群が世論を特定方向に誘導",
    "受け手のリテラシーと二重の警戒が重要"
  ],
  "key_points_en": [
    "OpenAI reports PRC-linked influence operations",
    "Targets data centers, tariffs, false ChatGPT claims",
    "Nested: AI used to sway AI-policy debates",
    "Blurs authenticity of 'open-source must win' narrative",
    "Impersonation clusters steer opinion to set policy",
    "Audience literacy and double caution now essential"
  ]
}
]

# ---- stats ----
raw["stats"] = {
    "arxiv": len(s["arxiv"]),
    "hn": len(s["hn"]),
    "reddit": len(s["reddit"]),
    "github": len(s["github"]),
    "blogs": len(s["blogs"]),
}

out = data_dir / f"{DATE}.json"
json.dump(raw, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("Wrote", out)
print("highlights:", len(raw["highlights"]))
