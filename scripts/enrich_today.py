#!/usr/bin/env python3
"""Enrich raw-2026-06-02.json -> 2026-06-02.json with JA/EN summaries + highlights."""
import json
from pathlib import Path

DATE = "2026-06-02"
ROOT = Path(__file__).resolve().parent.parent
raw = json.load(open(ROOT / "data" / f"raw-{DATE}.json"))
S = raw["sources"]

# ---------------- arXiv (top 25) ----------------
arxiv = {
 0: ("Blenderで考える：VLMによる段階的・実行可能な逆グラフィックス",
     "1枚の画像から、編集・再ライティング可能な3Dシーンを復元する逆問題に挑戦。事前学習済みVLMがBlenderで実行可能なスクリプトを段階的に生成し、画像を編集可能な3Dとして再構成できるか検証する。"),
 1: ("マルチモーダルLLM審判の知覚判断バイアスを摂動と報酬モデルで緩和",
     "画像と文字情報が矛盾する時、MLLM審判は知覚的に正しい答えより『もっともらしい物語』を選ぶ弱点がある。知覚摂動と報酬モデリングでこの判断バイアスを体系的に緩和する。"),
 2: ("RoboDream：スケーラブルなロボットデータ合成のための合成的世界モデル",
     "ロボット学習に必要な大規模実演データを、遠隔操作でなく世界モデルで合成。表面的な見た目の拡張に留まる従来生成手法を超え、合成的な世界モデルで多様なロボットデータを大量生成する。"),
 3: ("ProtoAda：マルチモーダル継続的指示チューニングのプロトタイプ誘導アダプタ拡張",
     "MLLMが新しい視覚言語能力を継続学習する際のタスク間干渉を抑える手法。プロトタイプに導かれてアダプタを適応的に拡張し、幾何的に統合することで干渉を減らし協調を促す。"),
 4: ("ゼロからヒーローへ：世界モデルへの学習不要なカスタム概念の出現",
     "自己回帰的世界モデルで対話的に生成された環境を移動すると、参照フレームにない物体を出せない問題がある。再学習なしで任意のカスタム概念を世界に出現させる手法を提案する。"),
 5: ("HumanNOVA：1枚画像からの写実的・汎用・高速な3D人体アバター生成",
     "1枚のRGB画像から写実的な3D人体アバターを高速生成。高品質な3D人体データの希少性を、スケーラブルなデータ生成パイプラインで補い、写実性と汎化を両立する。"),
 6: ("VISReg：JEPA学習のための分散・不変性・スケッチ正則化",
     "VICRegの共分散項は二次統計しか捉えられない弱点がある。スケッチを用いた新たな正則化で、埋め込み崩壊を防ぎつつ高次の構造まで捉えるJEPA学習法を提案する。"),
 7: ("AdaCodec：動画MLLMのための予測的な視覚コード",
     "隣接フレームは大半の物体・背景を共有するのに、従来の動画MLLMは各フレームを独立RGB画像として符号化し冗長なトークンを生む。前フレームとの差分を符号化する予測的視覚コードで効率化する。"),
 8: ("ClinEnv：エージェント向けの対話的・多段・長期EHR環境",
     "実臨床は選択肢から答えを選ぶのでなく、医師が情報を逐次集め不可逆な判断を重ねる営み。これを再現する対話的・長期の電子カルテ（EHR）環境を構築し、医療エージェントを現実的に評価する。"),
 9: ("方策に基づく中心窩イメージング・知覚",
     "超高解像度センサーの全画素を常時処理するのは帯域・遅延・電力的に非現実的。人間の中心窩のように、方策で重要領域だけを高解像度で取得・処理する効率的な知覚手法を提案する。"),
 10:("VLMは適応的テスト時最適化により動画推論の良き教師となる",
     "動画生成モデルで推論する際、生成品質は高くてもタスク規則の理解が弱く論理的に破綻しがち。VLMを教師に、テスト時の適応最適化で生成軌跡を規則に沿わせ動画推論を改善する。"),
 11:("IntraShuffler：異質なDP連合学習のためのプライバシー保護枠組み",
     "連合学習でクライアントごとにプライバシー予算を変える異質DPは、サーバ集約時に情報が漏れうる。クライアント内シャッフルで漏洩を防ぐプライバシー保護フレームワークを提案する。"),
 12:("信頼できる推論による寛容な安全性：検証可能な信念空間ニューラル安全フィルタ",
     "人と関わるロボットは、相手の意図や協力度といった不確実性下で安全かつ効率的に判断せねばならない。信念空間で動く検証可能なニューラル安全フィルタで、過度に保守的にならず安全を保証する。"),
 13:("層からサブモジュールへ：置換型LLM圧縮の粒度を問い直す",
     "学習後のLLM圧縮は通常『層まるごと』を削除・置換するが、これは制約が強すぎると主張。冗長性は層内のサブモジュール単位に偏在するとし、より細かい粒度・非連続な選択で効率的に圧縮する。"),
 14:("HERO'S JOURNEY：テキストゲームで複雑な規則帰納を試す",
     "目的志向の連続課題で、エージェントが実演から隠れた規則を推論し多段実行できるかを測るベンチマーク。属性・手続きの帰納にまたがる8タスクで、規則帰納能力を統制的に評価する。"),
 15:("LongLive-RAG：長尺動画生成のための汎用検索拡張フレームワーク",
     "自己回帰動画拡散は長尺生成で誤差蓄積やアイデンティティのドリフトに悩む。検索拡張（RAG）で過去の文脈を引き戻し、長時間でも一貫した動画を生成する汎用フレームワーク。"),
 16:("深度の曖昧さをモデル化：飛び点を出さない混合密度深度推定",
     "深度推定は物体境界で前景と背景の間の空虚に偽の3D点（飛び点）を生む。各画素に単一深度を割り当てる慣習が原因とし、混合密度表現で境界の曖昧さを表し飛び点を解消する。"),
 17:("AFUN：機能理解のためのアフォーダンス基盤モデルに向けて",
     "アフォーダンス理解は視覚と物理行動を橋渡しし、ロボット操作の説明可能なインタフェースになる。『どこで・どう触れるか』に加え機能まで理解し、多様な環境に汎化する基盤モデルを目指す。"),
 18:("SN-WER：多文字体系インド系ASR評価のための字種正規化WER",
     "同じ単語を別の文字体系で書くとWERが誤りを過大評価する。ローマ字化など多言語ASRで起きるこの問題を、学習不要の字種正規化WERで補正し公平に評価する。"),
 19:("救急トリアージ記録からの転移可能な自傷監視：証拠拡張型機械学習",
     "自傷は重大な公衆衛生課題だが、診断コード依存の監視は感度が低い。救急トリアージの自由記述を使い、証拠拡張型の機械学習で自傷を高感度に検知する転移可能な監視手法を提案する。"),
 20:("SimSD：拡散言語モデルでのシンプルな投機的デコーディング",
     "拡散LLMは並列デコードで高速だが、マスク言語モデルの定式化が標準的な投機的デコーディングと相性が悪い。拡散LLMに適合する単純な投機的デコーディングで、さらなる高速化を図る。"),
 21:("SkillHarm：自動構築によるライフサイクル横断のスキルベース攻撃",
     "エージェントが暗黙に従う『スキル』は、第三者が悪用できる脆弱な攻撃面。単一タスク内に留まらず、スキルのライフサイクル全体を悪用する攻撃を自動構築し、危険性を体系的に示す。"),
 22:("適応するエージェントの行動軌跡を追跡する",
     "スキル・記憶・設定ファイルはエージェントの振る舞いを規定し、人やエージェント自身の編集で時間とともに変化する。こうしたファイルの編集がエージェント行動をどう変えるかを測る枠組みを提案する。"),
 23:("LL-Bench：大規模生成モデル時代の低レベル視覚評価を問い直す",
     "大規模生成モデルは画像生成・編集に長けるが、画素単位の制御を要する低レベル視覚タスクの性能は未検証。これを体系的に測る包括ベンチマークLL-Benchを提案する。"),
 24:("マスク条件付き潜在拡散拡張でTEM欠陥の検出・分類を改善",
     "照射金属合金などのTEM画像の欠陥解析は、ラベル付き良質データの不足が壁。マスク条件付き潜在拡散で現実的な合成画像を生成し、欠陥の検出と分類をまとめて改善する。"),
}

# ---------------- Hacker News ----------------
hn = {
 0: ("求職中の人にスパムを送るな。ただ残酷なだけだ",
     "AI生成の定型応募・自動スカウトが求職者を疲弊させている現状への怒りの投稿。生成AIで量産される無神経な連絡が、人を雑に扱う風潮を助長していると問う。HN首位。"),
 1: ("Red Hat Cloud Services全体で悪意あるnpmパッケージを検出",
     "@redhat-cloud-services スコープの公式npmパッケージ32個・96バージョンが侵害され、認証情報を盗むワーム『Miasma』が混入。サプライチェーン攻撃の生々しい事例。"),
 2: ("Adafruit、Flux.aiの代理人Fenwickから要求書を受領",
     "AI EDA企業Flux.aiの法律事務所が、オープンハードウェアの老舗Adafruitに要求書を送付。コミュニティに愛される企業へのAIスタートアップの法的圧力として反発を呼ぶ。"),
 3: ("スタンフォードCS336のAIエージェント利用ガイドライン",
     "LLMをゼロから作る名物講義CS336が、課題でのAIエージェント（Claude等）の使い方ルールをCLAUDE.mdとして公開。教育現場がAI前提の指導法を整える動き。"),
 4: ("Chipotlai Max：Chipotleを自動注文するAIエージェント",
     "自然言語で頼むとChipotleのオンライン注文を自動でこなすAIエージェントの実験的リポジトリ。日常タスクをエージェントに任せる遊び心ある実装。"),
 5: ("DuckDuckGo、トラフィック急増で『AIなし』検索を使いやすく",
     "AI要約を排した検索を求める声を受け、DuckDuckGoが『no-AI』検索への切替を簡単にした。AI検索への反動でトラフィックが伸びている。"),
 6: ("フロリダ州、AIのリスクを巡りOpenAIとサム・アルトマンを提訴",
     "フロリダ州司法長官が、ChatGPTの危険性を隠したとしてOpenAIとアルトマンCEOを提訴。製造物責任・過失・不公正取引を主張する州レベルでは異例の訴訟。"),
 7: ("Alphabet、AIインフラ拡張へ800億ドルの株式調達を発表",
     "Googleの親会社が米企業史上最大規模となる800億ドルの株式調達を発表。AI計算基盤の需要が供給を上回る中、バークシャーも100億ドルを引受。"),
 8: ("GitHubとソフトウェアに対する罪",
     "GitHub（とMicrosoft/Copilot）の運営方針がOSS文化を損なっていると論じる批判的エッセイ。開発者コミュニティの不満を代弁。"),
 9: ("Ask HN：採用してる人は？（2026年6月）",
     "HN恒例の月次求人スレッド。2026年6月時点のスタートアップ/技術職の採用動向が読み取れる。"),
 10:("報酬を得る3つの方法（2018）",
     "投資ジャーナリストJason Zweigによる、対価の得方を巡る古典的エッセイが再浮上。AI時代の仕事と報酬を考える文脈で読まれた。"),
 11:("ハッカーのためのLinux基礎（2019）のノート",
     "セキュリティ/ペネトレーションテスト入門書『Linux Basics for Hackers』の学習ノート集。改めてHN上位に再浮上。"),
 12:("Coreutils for Windows（Microsoft製）",
     "MicrosoftがWindows向けにcoreutils（Unix系基本コマンド群）を移植。Rust実装ベースで、開発体験のクロスプラットフォーム化を進める。"),
 13:("Flipper Zero用のZigテンプレート",
     "ハッキング用ガジェットFlipper Zeroのアプリを、Zig言語で書くためのテンプレート。低レベル開発の遊び場として人気。"),
 14:("AIが一線を越えるとき：Matplotlib事件",
     "AIエージェントがMatplotlibのリポジトリで不適切な振る舞いをした事例の検証。OSSにAIエージェントが関与する際のリスクを問う。"),
 15:("Project Glasswingの拡大（Anthropic）",
     "Anthropicが、AIの安全性や社会実装に関する取り組み『Project Glasswing』を拡大すると発表。透明性や責任あるAIへの投資を示す。"),
 16:("マイケル・バーリ：SpaceXもAnthropicも1兆ドルの価値はない",
     "『世紀の空売り』のバーリが、SpaceXやAnthropicの1兆ドル級評価を過大と断じAIバブルを警告。Alphabetの巨額調達と対をなす懐疑論。"),
 17:("AIと戦う術を知らない米国人は、代わりにデータセンターと戦う",
     "AIへの不満の矛先が、各地で建設されるデータセンターへの反対運動に向かう現象を分析。AI反動が物理インフラ政治に波及する様を描く。"),
 18:("2009年のようにシステム管理する",
     "クラウドやAI任せでなく、素朴で堅実な昔ながらのサーバー運用を肯定するエッセイ。過剰な自動化への揺り戻しを映す。"),
 19:("Launch HN：Expanse（YC P26）——遊休GPU容量を解放する",
     "使われていないGPU容量を集めて活用するスタートアップ。AI計算需要の逼迫を背景に、余剰計算資源のマーケット化を狙う。"),
}

# ---------------- GitHub ----------------
github = {
 0: ("hermes-webui：HermesエージェントのWeb/スマホUI",
     "Nous ResearchのHermesエージェントをブラウザやスマホUIから使うためのフロントエンド。オープンモデルのエージェント運用を手軽に。"),
 1: ("ECC：エージェント・ハーネスの性能最適化システム",
     "スキル・本能・記憶・セキュリティを備え、リサーチ優先で開発を進めるエージェント基盤。エージェントの自己改善・運用を体系化する試み。"),
 2: ("headroom：LLMに渡す前にツール出力やログを圧縮",
     "ツール出力・ログ・RAGチャンクをLLM入力前に圧縮し、トークンを60〜95%削減しつつ回答品質を保つライブラリ。長文脈コスト削減に効く。"),
 3: ("supermemory：高速・スケーラブルなメモリエンジン/API",
     "AI時代向けの極めて高速なメモリAPI。アプリやエージェントに長期記憶を持たせるインフラとして人気を集める。"),
 4: ("machine-learning-for-trading：アルゴ取引のためのML（第2版）コード",
     "書籍『Machine Learning for Algorithmic Trading（第2版）』の実装コード集。金融×MLの定番教材。"),
 5: ("Open-LLM-VTuber：ローカルで動く音声対話＋Live2Dの相棒",
     "任意のLLMと音声で対話でき、割り込み発話やLive2Dの表情表示までローカルで動かせるVTuber風アシスタント。クロスプラットフォーム対応。"),
 6: ("production-agentic-rag-course：実運用エージェント型RAG講座",
     "本番環境を想定したエージェント型RAGの構築手法を学べるコース教材。検索拡張生成を実務に落とし込むノウハウを扱う。"),
}

# ---------------- Blogs ----------------
blogs = {
 0: ("Holo3.1：高速・ローカルなコンピュータ操作エージェント",
     "GUIを自動操作するコンピュータ操作エージェントの新版。0.8B〜35Bの4サイズと量子化版を備え、ローカル実行とモバイル操作精度を大きく改善。"),
 1: ("TravelersがOpenAIで保険金請求処理を全米展開",
     "大手保険TravelersがOpenAIを使い、保険金請求の処理を全米規模でAI化。バックオフィス業務へのLLM導入事例。"),
 2: ("Codex、あらゆる役割・ツール・ワークフローへ",
     "OpenAI Codexがコーディング以外の知的労働へ拡大。6つの役割別プラグインを投入し、週間アクティブ500万・知識労働者が全体の2割に。"),
 3: ("グローバルなリーダーシップで若者の安全と機会を前進させる",
     "OpenAIが、AI時代の未成年保護と機会創出に関する国際的な取り組み方針を表明。子どもの安全を巡る規制・批判への対応。"),
 4: ("Codexは万人の生産性ツールになりつつある",
     "Codexがリサーチ・レポート・表計算など知的労働全般に拡張。知識労働者は開発者の3倍速で採用が進んでいるという。"),
 5: ("AI政策と政治的アドボカシーに関する我々の見解",
     "OpenAIがAI規制・ロビー活動に対する自社のスタンスを表明。州・連邦の規制論争が高まる中での政治的立場の説明。"),
 6: ("GeminiでGoogle I/O 2026を作った舞台裏",
     "I/O 2026のサイトや演出をGemini自身を使って制作した制作記。生成AIで体験全体を作った例。"),
 7: ("Mellum2：JetBrainsによる12BのMoEコードモデル",
     "総12B・アクティブ2.5BのオープンMoEモデル（Apache 2.0）。ルーティングやRAG、サブエージェント等の高頻度タスク向けに2倍超の高速推論を狙う。"),
 8: ("LLMを超えて：企業のAI普及はエージェント論理に懸かる",
     "単なるLLMでなく、業務ロジックを持つエージェント設計こそが企業のAI本格導入の鍵だと論じるIBM Researchの記事。"),
 9: ("ミシガンに『知能の時代』のインフラを建設",
     "OpenAIがミシガン州にAIデータセンター（Stargate）を整備する計画。計算基盤拡大の一環。"),
 10:("OpenAIのフロンティアモデルとCodexがAWSで利用可能に",
     "OpenAIのGPT-5.5/5.4とCodexがAmazon Bedrock経由で一般提供開始。AWS顧客が既存環境からOpenAIを使える道が開けた。"),
 11:("NVIDIA Cosmos 3：物理AIの推論・行動のための初のオープンOmniモデル",
     "世界生成・物理推論・行動生成を1つに統合した物理AI向けオープン基盤モデル。MoT構成でロボットや自動運転に使える。"),
 12:("Google AI StudioでVibeコーディングしたI/O 2026クイズ",
     "I/O 2026の発表内容を当てるクイズを、Google AI Studioで『Vibeコーディング』して制作。即席アプリ生成力をデモ。"),
 13:("Gemini OmniとGemini 3.5の実演9連発",
     "I/O 2026で発表された動画生成モデルGemini Omniと、エージェント/コーディング特化のGemini 3.5の実演動画集。"),
 14:("ボストン小児病院、AIで新たな診断を解明",
     "OpenAIの技術を使い、難解な小児症例の診断にAIを活用した事例。医療現場での実用化が進む。"),
 15:("BraintrustがCodexで顧客要望をコードに変える",
     "顧客のリクエストをOpenAI Codexで実装に落とし込むBraintrustの事例。要望→コードの自動化を示す。"),
 16:("Futures Labのリアルな実用AIプロトタイプ",
     "Googleと提携した大学ラボ発、教育や労働を変えうるAIプロトタイプの実例集。研究段階の体験を一般に見せる。"),
 17:("Rosalind Biodefenseと社会のレジリエンス強化",
     "バイオ防衛のRosalindと組み、AIで社会の危機対応力を高めるOpenAIの取り組み。安全・防衛分野でのAI活用。"),
 18:("PyTorchでのプロファイリング入門（Part 1）",
     "torch.profilerを使ったPyTorchの性能計測の初心者向けガイド。ボトルネック特定の基礎を解説。"),
 19:("I/O 2026の主要12モーメントを振り返る",
     "Google I/O 2026基調講演のハイライト12連発。Gemini 3.5/Omni、検索エージェント、Android XRグラスなど主要発表を総まとめ。"),
 20:("Reachy Miniが完全ローカル動作に",
     "Hugging Faceの卓上ロボットReachy Miniが、クラウドなしで完全ローカルで対話・動作するように。オープンなロボティクスの一歩。"),
 21:("Hubバケットで1兆パラメータを配送：TRLのデルタ重み同期",
     "TRLで巨大モデルの差分（デルタ）重みだけをHubバケット経由で同期し、1兆パラメータ級の配布を実現する仕組み。"),
}

def apply(items, table):
    for i, it in enumerate(items):
        if i in table:
            it["title_ja"], it["summary_ja"] = table[i]

apply(S.get("arxiv", []), arxiv)
apply(S.get("hn", []), hn)
apply(S.get("github", []), github)
apply(S.get("blogs", []), blogs)

# ---------------- Highlights ----------------
highlights = [
 {
  "source": "HN / Regulation",
  "title": "Florida sues OpenAI and Sam Altman, claiming ChatGPT's risks were concealed",
  "title_ja": "フロリダ州、ChatGPTの危険を隠したとしてOpenAIとアルトマンを提訴",
  "url": "https://techcrunch.com/2026/06/01/florida-sues-openai-sam-altman-in-first-of-its-kind-lawsuit-over-violent-incidents/",
  "hot_take_ja": "州が会社だけでなくCEO個人まで名指しで訴える、AI製品に対する初の本格的な製造物責任訴訟。FSUの銃撃犯がChatGPTで計画を練ったとされる事例まで持ち出し、『危険を知りながら出荷した』と主張する。タバコや製薬を訴えた時と同じ論理がLLMに向き始めた——規制リスクが一段現実になった瞬間だ。",
  "detail_ja": "フロリダ州司法長官が6月1日、OpenAIとサム・アルトマンCEOを州裁判所に提訴した。州レベルではこの種で初とされ、製造物責任法違反に加え、過失、欺瞞的・不公正な取引慣行を主張する。訴状は、OpenAIが安全上の警告を無視し、有害と知りながらChatGPTを公開したと非難。具体的には、フロリダ州立大（FSU）の銃撃犯がChatGPTを使って攻撃を計画したとして『乱射犯の幇助』に当たるとし、さらに脆弱な人々の自殺を助長した、保護者の監督なしに子どもを『人間の思いやりを装ってデータを集めるツール』に依存させた、と踏み込む。州が求める救済は、民事制裁金と、13歳未満のユーザーから保護者の同意なくデータを収集することを差し止める命令などだ。OpenAIは『AIは新しく強力な技術であり、未成年には大きな保護が必要だと考えている』とし、年齢推定ツールや保護者向け監視機能など業界をリードする保護策を導入済みだと反論した。注目点は、企業だけでなくアルトマン個人を被告に含めたこと、そして『製品の欠陥』という枠組みでLLMの出力を法的に捉えようとしていること。因果関係（チャットボットの出力と現実の暴力の結びつき）の立証は難しく訴訟は長期化しうるが、各州が同様の論理で追随すれば、AI企業は『安全に作る義務』を製造物責任の文脈で問われることになる。Alphabetの巨額AI投資と同じ週に出た点でも、AIの『成長』と『責任』が同時に膨らむ局面を象徴する。",
  "detail_en": "On June 1, Florida's attorney general sued OpenAI and CEO Sam Altman in state court — reportedly the first state action of its kind. The suit alleges product-liability violations alongside negligence and deceptive, unfair trade practices, accusing OpenAI of ignoring safety warnings and shipping ChatGPT while knowing it was harmful. Concretely, it claims ChatGPT amounted to 'aiding and abetting mass shooters' — citing a Florida State University shooter who allegedly used it to plan his attack — and that it encouraged vulnerable people toward suicide and addicted children to 'a tool that feigns human compassion to collect their data with no parental oversight.' Florida seeks civil penalties and a court order barring the company from collecting certain data from under-13 users without parental consent. OpenAI responded that 'AI is a new and powerful technology, and we believe minors need significant protection,' pointing to age-prediction tools and parental controls it says are industry-leading. Two things stand out: naming Altman personally as a defendant, and framing an LLM's outputs through 'product defect' law. Proving causation between chatbot output and real-world violence is hard and the case could drag on, but if other states follow the same theory, AI firms will increasingly face a duty to 'build safely' under product-liability doctrine. Landing the same week as Alphabet's massive AI fundraise, it captures a moment when AI's growth and its liability are swelling together.",
  "key_points_ja": [
    "州が初の本格的な対AI製造物責任訴訟を提起",
    "企業だけでなくアルトマンCEO個人も被告に",
    "FSU銃撃犯がChatGPTで計画と主張＝『幇助』",
    "自殺助長・未成年のデータ依存も争点",
    "13歳未満のデータ収集差し止めと制裁金を要求",
    "因果立証は困難だが他州追随なら影響大"
  ],
  "key_points_en": [
    "First major state product-liability suit over AI",
    "Names CEO Altman personally, not just OpenAI",
    "Cites FSU shooter who 'used ChatGPT to plan'",
    "Also alleges suicide encouragement, child data harm",
    "Seeks penalties + bar on under-13 data collection",
    "Causation is hard, but copycat states could follow"
  ],
 },
 {
  "source": "HN / Business",
  "title": "Alphabet announces an $80B equity raise — the largest in US corporate history — to fund AI",
  "title_ja": "Alphabet、AIに800億ドル調達を発表——米企業史上最大の株式発行",
  "url": "https://abc.xyz/investor/news/news-details/2026/Alphabet-Announces-Proposed-80-Billion-Equity-Capital-Raise-to-Expand-AI-Infrastructure-and-Compute-2026-b0myAMewCa/default.aspx",
  "hot_take_ja": "潤沢なキャッシュで知られるGoogleが、わざわざ800億ドルの株式を発行する。米企業史上最大の株式調達で、AI計算需要が供給を上回る現実をそのまま映している。バフェットのバークシャーが100億ドルを引き受ける一方、同じ日にマイケル・バーリは『AIは1兆ドルの価値などない』と空売り。AI投資への『買い』と『売り』が同時に最高潮だ。",
  "detail_ja": "Alphabetが6月1日、AI計算インフラ拡張のため総額800億ドルの株式発行を発表した。報じられる限り米企業史上最大の株式調達で、構成は三本柱だ。①300億ドルの公募（強制転換優先株150億ドル＋クラスA/C普通株150億ドル）、②第3四半期開始予定の400億ドルの『市場価格売出し（ATM）』プログラム、③バークシャー・ハザウェイへの100億ドルの私募（クラスA/C各50億ドル）。資金使途は一般事業目的だがその中核はAIインフラとグローバル計算能力の増強で、ATMの約300億ドルは従業員株式報酬の納税にも充てる。背景にあるのは需要逼迫だ——Alphabetは『企業・消費者双方からのAI需要が、利用可能な計算供給を上回っている』と明言する。設備投資計画も桁外れで、2026年は1800億〜1900億ドル、2027年はさらに大幅増を見込む。キャッシュ豊富なGoogleが敢えて株式希薄化を受け入れてまで調達する事実は、AI計算が『キャッシュフローでは追いつかない』規模に達したことを示す。一方で同じ日、『世紀の空売り』マイケル・バーリはSpaceXやAnthropicの1兆ドル級評価を過大と断じた。バフェットが買い、バーリが売る——AIインフラ投資が熱狂とバブル懸念の両極を同時に体現している。",
  "detail_en": "On June 1, Alphabet announced an $80B equity raise to expand AI compute infrastructure — reportedly the largest equity offering in US corporate history. It has three parts: (1) $30B in underwritten public offerings ($15B mandatory convertible preferred + $15B Class A/C common); (2) a $40B at-the-market (ATM) program expected to begin in Q3 2026; and (3) a $10B private placement to Berkshire Hathaway ($5B each Class A/C). Proceeds are for general corporate purposes centered on AI infrastructure and global compute, with ~$30B of the ATM earmarked for taxes on employee equity awards. The driver is scarcity: Alphabet states that demand for its AI from enterprises and consumers is 'outstripping its available compute supply.' Its capex plans are staggering — $180–190B in 2026, with 2027 expected to rise significantly. That cash-rich Google would accept equity dilution to raise this much signals AI compute has reached a scale cash flow alone can't fund. Notably, the same day, 'Big Short' investor Michael Burry argued neither SpaceX nor Anthropic is worth $1T. Buffett buys while Burry shorts — AI-infrastructure investing is simultaneously at peak euphoria and peak bubble-anxiety.",
  "key_points_ja": [
    "AI計算拡張へ800億ドルの株式発行（米史上最大）",
    "公募300億＋ATM400億＋バークシャー私募100億",
    "『AI需要が計算供給を上回る』と明言",
    "設備投資は2026年に1800〜1900億ドル",
    "キャッシュ潤沢でも希薄化を受け入れる規模",
    "同日バーリは1兆ドル評価に懐疑＝バブル論併存"
  ],
  "key_points_en": [
    "$80B equity raise for AI — largest in US history",
    "$30B public + $40B ATM + $10B Berkshire placement",
    "Says AI demand outstrips available compute supply",
    "2026 capex guided to $180–190B",
    "Cash-rich Google still accepts dilution at this scale",
    "Same day: Burry doubts $1T AI valuations"
  ],
 },
 {
  "source": "HN / Security",
  "title": "'Miasma': 32 official @redhat-cloud-services npm packages hijacked to spread a credential-stealing worm",
  "title_ja": "『Miasma』：Red Hat公式npmパッケージ32個が乗っ取られ認証情報窃取ワームを拡散",
  "url": "https://github.com/RedHatInsights/javascript-clients/issues/492",
  "hot_take_ja": "『公式の信頼できるパッケージ』が一夜にして攻撃媒体になる、サプライチェーン攻撃の典型例。乗っ取られたGitHubアカウント経由でRed Hat公式の32パッケージ・96バージョンにワームが仕込まれ、npm installのpreinstallフックでGitHub Actionsやクラウドの秘密情報を根こそぎ盗む。週11.7万DLの正規パッケージが武器化された。",
  "detail_ja": "6月1日、@redhat-cloud-services スコープの公式npmパッケージ群が侵害されていたことが公表された。侵害されたGitHubアカウントを足がかりに、Red HatのGitHub組織で管理される32パッケージ・96バージョンへ悪意あるコードが注入された。ペイロードはnpm installのたびにpreinstallフックで発火する多段の認証情報窃取マルウェアで、GitHub Actionsのシークレットに加え、AWS・GCP・Azure・Kubernetes・HashiCorp Vault・npm・CircleCIのトークンを横断的に吸い上げる。検知回避も作り込まれていた。このキャンペーンは『Miasma: The Spreading Blight』と名付けられ、脅威グループTeamPCPに関連づけられる既知の認証情報窃取ワーム『Mini Shai-Hulud』系の新変種とされる。影響範囲は大きく、対象パッケージは合計で週あたり約11.7万回ダウンロードされていた。Red Hatのエンジニアリングは公表後に侵害バージョンをnpmから削除し、現時点の調査では『顧客側の対応は不要』としている。教訓は明快だ——『公式スコープ＝安全』ではない。lockfileのピン留め、preinstall/postinstallスクリプトの監査、CIでの最小権限とシークレットの絞り込み、依存の出所検証が、ワーム型サプライチェーン攻撃に対する現実的な防御になる。エコシステムの信頼を一点突破で武器化できることを、今回の事件は改めて突きつけた。",
  "detail_en": "On June 1, a supply-chain compromise of the official @redhat-cloud-services npm scope was disclosed. Using a compromised GitHub account as a foothold, attackers injected malicious code into 32 packages (96 versions) maintained in Red Hat's GitHub org. The payload is a multi-stage credential harvester that fires via a preinstall hook on every npm install, sweeping GitHub Actions secrets plus AWS, GCP, Azure, Kubernetes, HashiCorp Vault, npm, and CircleCI tokens — and it was purpose-built to evade detection. The campaign, dubbed 'Miasma: The Spreading Blight,' is a new variant of the 'Mini Shai-Hulud' worm family previously linked to threat group TeamPCP. The blast radius is significant: the affected packages were collectively downloaded ~117,000 times per week. Red Hat engineering removed the compromised versions from npm after disclosure and says no customer action is currently required. The lesson is blunt: an 'official scope' is not a safety guarantee. Pinning lockfiles, auditing pre/post-install scripts, minimizing CI permissions and secret scope, and verifying dependency provenance are the practical defenses against worm-style supply-chain attacks. The incident is a fresh reminder that ecosystem trust can be weaponized from a single compromised account.",
  "key_points_ja": [
    "Red Hat公式npm 32パッケージ・96版が侵害",
    "preinstallフックで認証情報を窃取するワーム",
    "GitHub Actions・AWS/GCP/Azure等のトークンを収集",
    "『Miasma』＝既知ワームMini Shai-Huludの新変種",
    "対象は週約11.7万DLの正規パッケージ",
    "対策：lockfileピン留め・install script監査・最小権限"
  ],
  "key_points_en": [
    "32 official Red Hat npm packages (96 versions) hit",
    "preinstall-hook worm steals credentials on install",
    "Sweeps GitHub Actions, AWS/GCP/Azure, Vault tokens",
    "'Miasma' — a new Mini Shai-Hulud worm variant",
    "Affected packages: ~117k downloads per week",
    "Defend: pin lockfiles, audit scripts, least-privilege CI"
  ],
 },
 {
  "source": "OpenAI / AWS",
  "title": "Codex goes 'for every role' and lands on AWS — GPT-5.5 now on Bedrock, 5M weekly users",
  "title_ja": "Codexが『あらゆる役割』へ拡張しAWSに上陸——GPT-5.5がBedrockで提供、週500万人",
  "url": "https://openai.com/index/codex-for-every-role-tool-workflow/",
  "hot_take_ja": "Codexがコーディングツールから『知的労働の汎用エージェント』へと舵を切った。週間アクティブは500万に達し、いまや知識労働者が2割で開発者の3倍速で増えているという。さらにGPT-5.5/5.4とCodexがAWS Bedrockで一般提供開始——『OpenAIを使うのにOpenAIに行かなくていい』。配布チャネルの覇権争いが本格化した。",
  "detail_ja": "OpenAIがCodexの大型アップデートを発表した。中心は二つ。第一に、Codexを『あらゆる役割・ツール・ワークフロー』へ広げる方針で、コーディング不要で使える6つの役割別プラグインを投入。Codexはチームが既に使うツール・文脈・ワークフローに接続し、必要な成果物を作る存在として位置づけ直された。数字も大きい——Codexの週間アクティブユーザーは500万に達し、うち約20%が知識労働者で、開発者の3倍速で採用が進んでいるという。土台となるGPT-5.5は大規模コードベースでのコード生成・デバッグに加え、データ分析、文書・スプレッドシート生成、複数ツールをまたいだソフト操作に長け、改善はエージェント的コーディングと知的労働で特に大きいとされる。第二に、OpenAIのフロンティアモデル（GPT-5.5/5.4）とCodexがAmazon Bedrockで一般提供開始。推論はすべてBedrock経由で実行され、IAM・VPC分離・暗号化などAWS既存のセキュリティがそのまま効く。Codexアプリ・CLI・IDE統合から使える。含意は二層だ。プロダクト面では、Codexが『開発者の道具』から『業務横断のエージェント基盤』へ脱皮しつつある——表計算やレポート作成まで担うなら、競合はIDE補完ではなくオフィス系SaaSになる。流通面では、AWSという最大の企業クラウド上で直接OpenAIを使える意味が大きい。クラウド各社が自社マーケットプレースを通じてフロンティアモデルの『棚』を奪い合う、流通チャネル競争が前面に出てきた。",
  "detail_en": "OpenAI announced a major Codex update with two thrusts. First, Codex is expanding 'for every role, tool, and workflow,' adding six role-specific plugins usable with no coding required; Codex is reframed as something that connects to the tools, context, and workflows a team already uses and produces the materials they need. The numbers are sizable: Codex has reached 5 million weekly active users, with knowledge workers now ~20% of them and adopting Codex more than 3x as fast as developers. The underlying GPT-5.5 excels at writing and debugging code across large codebases plus analyzing data, generating documents and spreadsheets, and operating software across multiple tools — with the biggest gains in agentic coding and knowledge work. Second, OpenAI's frontier models (GPT-5.5/5.4) and Codex are now generally available on Amazon Bedrock; all inference is routed through Bedrock with the same IAM, VPC isolation, and encryption AWS customers already use, accessible via the Codex App, CLI, and IDE integrations. The implications are twofold. On product: Codex is graduating from a 'developer tool' to a cross-functional agent platform — if it handles spreadsheets and reports, its competition becomes office SaaS, not IDE autocomplete. On distribution: being usable directly on the largest enterprise cloud matters enormously, surfacing a channel war in which cloud providers fight to be the 'shelf' for frontier models.",
  "key_points_ja": [
    "Codexがコーディング以外の知的労働へ拡張",
    "コード不要の役割別プラグインを6種投入",
    "週間アクティブ500万、知識労働者が2割で3倍速採用",
    "土台のGPT-5.5は文書・表計算・ソフト操作も得意",
    "GPT-5.5/5.4とCodexがAWS Bedrockで一般提供",
    "競合はIDE補完でなくオフィスSaaS／流通の覇権争いに"
  ],
  "key_points_en": [
    "Codex expands beyond coding into knowledge work",
    "Six no-code, role-specific plugins added",
    "5M weekly users; knowledge workers 20%, 3x faster uptake",
    "GPT-5.5 also strong at docs, spreadsheets, software ops",
    "GPT-5.5/5.4 + Codex now GA on Amazon Bedrock",
    "Rivals become office SaaS; a cloud distribution war"
  ],
 },
 {
  "source": "Hugging Face / H Company",
  "title": "Holo3.1: fast, local computer-use agents you can run on-device",
  "title_ja": "Holo3.1：端末上で動かせる高速・ローカルなコンピュータ操作エージェント",
  "url": "https://huggingface.co/blog/Hcompany/holo31",
  "hot_take_ja": "コンピュータ操作エージェントが『クラウドの巨大モデル』から『手元で動く軽量モデル』へ降りてきた。0.8Bの超軽量から35Bまで4サイズを揃え、量子化版でローカル実行とほぼ無劣化の精度を両立。AndroidWorldでは67%→79%へ大幅改善と、モバイルUI操作の実用度がぐっと上がっている。",
  "detail_ja": "H CompanyがHolo3.1を公開した。Web・デスクトップ・モバイルのGUIを自動操作する『コンピュータ操作エージェント』のモデル群で、今回の主眼は研究デモから本番運用に耐える堅牢性へ移すことだ。ラインナップは4サイズ——超軽量ローカル向けの0.8B、低コストの4B、性能と遅延の均衡を取る9B、最高性能の35B-A3B（MoE、アクティブ3B）。改善は三方向に整理される。①環境：デスクトップに加えWeb・モバイルへ対応。②エージェント枠組み：関数呼び出しと構造化JSON出力の両プロトコルをネイティブ対応。③配備：ローカル実行向けの量子化チェックポイント（FP8・Q4 GGUF・NVFP4）を用意。性能面ではモバイルUI操作の指標AndroidWorldで35B-A3Bが67%→79.3%、4B/9Bも58%→72%へと大きく伸びた。量子化の劣化は小さく、OSWorldではFP8/NVFP4がBF16比で約2点差に収まり、NVFP4 W4A16はBF16比1.74倍のスループット、DGX Sparkでは約2倍のエンドツーエンド高速化を示す。意義は明快だ——コンピュータ操作エージェントがローカルで実用速度に達すれば、画面のスクショや操作対象（業務ソフトの中身）を外部に送らずに自動化できる。プライバシー・コスト・遅延の三点で、オンデバイスのエージェントは企業導入の現実解になりうる。重みがHugging Faceで公開され、すぐ試せる点も大きい。",
  "detail_en": "H Company released Holo3.1, a family of computer-use agent models that automate GUIs across web, desktop, and mobile — with this release focused on moving from research demos to production robustness. Four sizes ship: an ultra-light 0.8B for local agents, a cost-efficient 4B, a balanced 9B, and a state-of-the-art 35B-A3B (MoE, ~3B active). The improvements fall into three areas: (1) environments — desktop plus new web and mobile support; (2) agent frameworks — native support for both function-calling and structured-JSON outputs; (3) deployment — quantized checkpoints (FP8, Q4 GGUF, NVFP4) for local execution. On benchmarks, mobile UI control on AndroidWorld jumps from 67% to 79.3% for 35B-A3B, and from 58% to 72% for 4B/9B. Quantization loss is small: on OSWorld, FP8/NVFP4 land ~2 points below BF16, while NVFP4 W4A16 delivers 1.74x throughput vs BF16 and ~2x end-to-end speedup on DGX Spark. The significance is clear — once computer-use agents run locally at usable speed, you can automate workflows without shipping screenshots or the contents of business software to the cloud. On privacy, cost, and latency, on-device agents become a realistic path for enterprise adoption, and open weights on Hugging Face make it immediately testable.",
  "key_points_ja": [
    "Web・デスクトップ・モバイルを操作するエージェント群",
    "0.8B〜35B-A3Bの4サイズ＋量子化版でローカル実行",
    "関数呼び出しと構造化JSON出力の両対応",
    "AndroidWorldで67%→79.3%、4B/9Bも58%→72%",
    "量子化劣化は小さくNVFP4で1.74倍スループット",
    "オンデバイス化でプライバシー・コスト・遅延を改善"
  ],
  "key_points_en": [
    "Agents that operate web, desktop, and mobile GUIs",
    "Four sizes 0.8B–35B-A3B + quantized for local runs",
    "Native function-calling and structured-JSON outputs",
    "AndroidWorld 67%→79.3%; 4B/9B 58%→72%",
    "Small quant loss; NVFP4 gives 1.74x throughput",
    "On-device helps privacy, cost, and latency"
  ],
 },
]

raw["highlights"] = highlights

out = ROOT / "data" / f"{DATE}.json"
json.dump(raw, open(out, "w"), ensure_ascii=False, indent=2)
print(f"Wrote {out}")
print(f"arxiv items: {len(S.get('arxiv', []))}, enriched: {sum(1 for i in arxiv)}")
print(f"highlights: {len(highlights)}")
