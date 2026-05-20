#!/usr/bin/env python3
"""Enrichment for 2026-05-20 (fresh page).

arXiv set is fully new (50 items, all translated below).
HN/Reddit/GitHub/blogs reuse prior Japanese translations for overlapping
URLs (from data/2026-05-19.json) and translate new items inline.
Five fresh highlights are selected for the day.
"""
import json
from pathlib import Path

DATE = "2026-05-20"
PREV = "2026-05-19"
ROOT = Path(__file__).resolve().parent.parent
SRC_RAW = ROOT / "data" / f"raw-{DATE}.json"
SRC_PREV = ROOT / "data" / f"{PREV}.json"
OUT = ROOT / "data" / f"{DATE}.json"

d = json.loads(SRC_RAW.read_text(encoding="utf-8"))
d["date"] = DATE
prev = json.loads(SRC_PREV.read_text(encoding="utf-8"))

# ─── Reuse prior translations (others by url) ───
prev_url = {}
for src in ("hn", "reddit", "github", "blogs"):
    for it in prev["sources"].get(src, []):
        if it.get("url"):
            prev_url[it["url"]] = (it.get("title_ja"), it.get("summary_ja"))

# ─── arXiv translations (id → title_ja, summary_ja) ───
arxiv_map = {
    "2605.20185v1": (
        "PiG-Avatar: 階層的ニューラルフィールド誘導ガウシアンアバター",
        "既存のガウシアンアバターは体テンプレート表面にジオメトリを乗せるため、衣服など体から離れた非剛体形状を捉えにくい。パラメトリック体モデルを運動伝達のみに使い、連続ニューラルフィールドが支配する正準ボリューム空間にガウシアンを固定して表現とテンプレートを分離する。"),
    "2605.20183v1": (
        "MSAVBench: マルチショット音声・動画生成の包括的・信頼性ある評価へ",
        "動画生成が単一ショットから複数ショットの音声付き物語へ進む中、最先端モデルの評価手法が追いついていない。複数ショット音声動画生成を体系的に評価する初の包括ベンチマークと適応型ハイブリッド評価枠組みを提案する。"),
    "2605.20182v1": (
        "思考の原子: マイクロステートによる汎用EEG表現学習",
        "脳波(EEG)を時系列信号として扱う従来法に対し、脳活動の微小時間スケールの構成要素である「マイクロステート」に着目。汎用マイクロステートトークナイザを構築し、BCI向けの転移可能な表現を学習する。"),
    "2605.20179v1": (
        "TIDE: I/O考慮のエキスパートオフロードによる高効率・無損失なMoE拡散LLM推論",
        "拡散型LLM(dLLM)はMoE化でスケールするが、リソース制約デバイスへの展開が課題。I/Oを考慮したエキスパートのオフロードで、無損失かつ効率的な推論を実現する。"),
    "2605.20177v1": (
        "見ることから考えることへ: 知覚と推論の分離がVLMの事後学習を改善",
        "VLMの視覚タスク性能は推論力よりも視覚知覚の不足に律速されると指摘。視覚知覚・視覚推論・テキスト推論の3段階に分けて学習し、知覚を独立に鍛えることで改善する。"),
    "2605.20176v1": (
        "ClinSeekAgent: エージェント的臨床推論のためのマルチモーダル証拠探索の自動化",
        "既存研究は証拠が整理済みで手渡される前提だが、現実の臨床は能動的な証拠探索を要する。多様な情報源からマルチモーダル証拠を能動取得・計画・統合するエージェント枠組み。"),
    "2605.20174v1": (
        "画像改ざん箇所特定の多軸分析",
        "生成AIで説得力のある画像改ざんが容易になり、誤情報拡散の脅威が増している。ドメイン・品質・種類・サイズの4観点で改ざん検出を評価するベンチマークAUDITSを提案する。"),
    "2605.20173v1": (
        "本番LLMエージェントの実行時アーキテクチャパターンの選定と合成の方法論",
        "LLMの確率的出力と決定的システムの境界を「確率-決定境界(SDB)」と名付け、提案者・検証者・コミット・拒否信号の4要素契約として定式化。本番エージェント実行時設計の中核プリミティブと位置づける。"),
    "2605.20172v1": (
        "解集合プログラミングによる長期送電網計画",
        "送電網の長期計画は位相的・組合せ的な不変条件を満たしつつ、十年単位の改修を扱う必要がある。Answer Set Programmingで供給継続性とサービス品質を保つ計画問題を定式化する。"),
    "2605.20170v1": (
        "KoRe: 大規模言語モデルのためのコンパクトな知識表現",
        "LLMは世界知識をパラメータ内に暗黙符号化するため不透明で更新困難・幻覚を招きやすい。編集容易な知識グラフの利点を取り込んだコンパクトな知識表現を提案する。"),
    "2605.20167v1": (
        "HaorFloodAlert: バングラデシュ湿地の72時間洪水予測のための季節除去ML集成",
        "バングラデシュのハオール湿地の鉄砲水は予兆なく稲作を壊滅させるが、河川型向けの既存システムでは捉えられない。気温という季節的な「ズル」を除いた機械学習集成で、72時間先の洪水確率を予測する。"),
    "2605.20165v1": (
        "CaMo: 視覚言語モデルのカメラ運動に基づく評価と訓練",
        "VLMは空間QAで高得点だが、空間知能の鍵であるカメラ運動の理解を欠くと指摘。シーン意味とカメラ運動を明示的に語らせる評価枠組み「空間ナラティブスコア(SNS)」を提案する。"),
    "2605.20164v1": (
        "ルーブリックは等しく教えない: RLVRのためのポリシー考慮型ルーブリック報酬",
        "ルーブリック報酬は基準ごとの人間が割り当てた重要度を使うが、最適化信号としての現在の有用性とは別物。両者を切り分けるポリシー考慮型の重み付けを提案する。"),
    "2605.20159v1": (
        "航空宇宙SiC/SiC複合材のX線CTにおける欠陥検出の解釈可能なコンピュータビジョン",
        "航空宇宙複合材のX線CT検査は専門家の目視に依存し合否判断の追跡性が乏しい。プロトタイプ層を加えたp-ResNet-50で、高精度と事例ベースの説明を両立する。"),
    "2605.20158v1": (
        "大規模視覚言語モデルの胸部X線推論における視覚的帰属の再考",
        "医療用LVLMの説明(視覚的帰属)が本当にモデルの判断根拠を反映しているかは未検証。胸部X線推論を対象に、説明の忠実性を検証する手法を構築する。"),
    "2605.20157v1": (
        "SAGE: 不正検知の確信的負例収集のためのスケーラブルな自動ゲーティング集成",
        "音楽ストリーミングの再生水増し詐欺は、熱心なファンや睡眠音楽セッションなど正当な利用と紛らわしい。反実仮想を意識した負例収集で、確信度の高い正常例を選別する。"),
    "2605.20151v1": (
        "構造化された相互学習でモデル崩壊はいつ起きるか",
        "生成AIの普及で、モデルが互いの合成出力を学習し合う環境が生まれた。学習データが対象母集団から外れ、モデル間の学習が相関する条件下で、モデル崩壊がいつ起きるかを理論的に解析する。"),
    "2605.20150v1": (
        "TideGS: コア外最適化による10億超の3Dガウシアンスプラッティングのスケーラブル学習",
        "10億規模の3DGS学習は本質的にメモリ律速。GPUメモリを永続パラメータ表でなく可視ガウシアンの作業集合キャッシュとして使い、コア外最適化で大規模化する。"),
    "2605.20149v1": (
        "やり取りを減らす: 構造化プロンプトの比較研究",
        "曖昧なプロンプトは低品質回答と追加のやり取りを生む。生プロンプト・チェックリスト改良・明確化質問の3条件を、ChatGPT・Claude・Grokで4タスク種にわたり比較する。"),
    "2605.20147v1": (
        "PixVerve: 大規模高品質データセットによる100MPネイティブ超高解像度画像生成",
        "超高解像度(UHR)画像生成は高解像度コンテンツの希少性と複雑さが壁。9.5万件のオープンなUHRデータセットを構築し、100メガピクセル級のネイティブ生成を実現する。"),
    "2605.20145v1": (
        "ベイズ最適化のためのガウス過程の目的指向な下側裾キャリブレーション",
        "ベイズ最適化のEIなど採択基準は予測分布の下側裾に依存し、その誤較正が探索-活用バランスを歪める。最小化目的に合わせ下側裾を較正する手法を研究する。"),
    "2605.20138v1": (
        "宇宙機の衝突回避のためのハミルトン-ヤコビ到達可能性解析",
        "同一円軌道上の2衛星の衝突回避を、ハミルトン-ヤコビ到達可能性の枠組みで定式化。FCCの軌道基準に沿う最小離隔を不安全な状態集合として扱う。"),
    "2605.20134v1": (
        "TrajTok: 軌跡表現学習のための適応的空間トークン化",
        "生のGPS軌跡は連続・ノイズ・不規則サンプリングで扱いにくい。GPS点の空間分布から多解像度の六角セル分割を学習し、転移可能な軌跡埋め込みを得る。"),
    "2605.20132v1": (
        "FiLark: 分散音響センシングのためのストリーミング優先ソフトウェア枠組み",
        "分散音響センシング(DAS)はバッチ処理を超える超多チャンネルの連続データを生む。探索・注釈・アルゴリズム統合をストリーミング優先で行うPython枠組みを提案する。"),
    "2605.20128v1": (
        "MixRea: 大規模言語モデルの明示-暗黙推論のベンチマーク",
        "人間の「非注意盲」に着想を得て、LLMが明示指示下で重要な文脈手掛かりを見落とすかを検証。2,246問の選択式問題からなるベンチマークを提案する。"),
    "2605.20127v1": (
        "予測精度を超えて: モデル-脳整合性評価のための標的空間回復プロファイル",
        "視覚モデルを脳応答の予測精度だけで評価しても、脳応答空間のどの次元を捉えたかは分からない。予測が回復した応答次元を特定する統一的な評価枠組みを提案する。"),
    "2605.20122v1": (
        "ワッサースタイン距離推定の計算-統計ランタイムの最適化",
        "二乗ワッサースタイン距離は分布間の差を測る常用ツールだが、低次元でも計算が標本数と精度に対し悪スケール。計算量と統計精度のトレードオフを最適化する。"),
    "2605.20120v1": (
        "Aristotle APIを使ったLean 4でのAI支援定理証明: バッタ問題の形式化事例",
        "AI支援の定理証明はオリンピック級の数学のLean開発を生成できるが、実際に検証された宣言が何かが証拠的価値を左右する。IMO2009問6「バッタ問題」のLean 4形式化事例を報告する。"),
    "2605.20119v1": (
        "Toto 2.0: 時系列予測がスケーリング時代へ",
        "時系列基盤モデルがスケールすることを示す——単一の学習レシピで4Mから2.5Bパラメータまで一貫して予測品質が向上。5モデルのオープンウェイト系列Toto 2.0を公開し、3つのベンチマークでSOTAを達成する。"),
    "2605.20110v1": (
        "SetCon: 集合レベルの概念予測によるオープンエンド参照セグメンテーション",
        "参照セグメンテーションを複数インスタンスやオープンな対象集合に拡張するのは難しい。対象を逐次トークンでなく一貫した「集合」として扱い、完全性や排他性など集合レベルの性質を捉える。"),
    "2605.20108v1": (
        "未知の非線形ダイナミクスに対するk帰納的ニューラル・バリア証明書",
        "従来の(k=1)バリア証明書は毎ステップ非増加を課すが、k帰納版は閾値内の一時増加をk-1回まで許し柔軟性を高める。ニューラルネットでk帰納的バリア証明書を構成する。"),
    "2605.20107v1": (
        "JEPAの等方性を超えて: ハミルトン幾何と斜交予測",
        "JEPAは片視点の埋め込みを等方ガウスへ正則化し、ユークリッド対称性を暗黙に組み込む。下流幾何が既知なら最適共分散はその逆行列に比例し、等方性には明確な「コスト」があると示す。"),
    "2605.20105v1": (
        "最適な表現サイズ: 事前学習と線形プロービングの高次元解析",
        "事前学習→線形プロービングの2段階パラダイムを解析的にモデル化。構造抽出を主成分分析として定式化し、最適な表現次元を高次元解析で導く。"),
    "2605.20104v1": (
        "ドラフトを減らし検索を増やす: 投機的デコーディングのためのハイブリッド木構築",
        "投機的デコーディングは大きなドラフト木で受理率を上げるが、VRAM帯域と計算がボトルネック。検索を併用したハイブリッド木構築で、効率と受理率を両立する。"),
    "2605.20101v1": (
        "トポロジー最適化された空気圧ソフトアクチュエータ: 設計と実験検証",
        "非線形トポロジー最適化でソフトな空気圧アクチュエータを計算設計。2D枠組みを3Dに拡張し、製造可能な2設計を数値・実験の両面で検証する。"),
    "2605.20098v1": (
        "推論時論証のためのニューロシンボリック学習",
        "健康や金融の主張検証では、不完全・矛盾する情報下で二値でなく「不確か」を返すのが適切な場合がある。形式的論証意味論を用いた三値の主張検証枠組みを提案する。"),
    "2605.20090v1": (
        "MetaEarth-MM: シーン中心の統合モデリングによるマルチモーダルリモートセンシング画像生成",
        "地球観測ではモダリティの揃ったペア観測が不足しがち。5モダリティを統一枠組みで結合生成・任意変換できる生成基盤モデルMetaEarth-MMを提案する。"),
    "2605.20088v1": (
        "INSHAPE: 解釈可能な時系列分類のためのインスタンス単位シェイプレット",
        "シェイプレット発見は時系列分類を説明可能にするが、データ全体で最適化した集団レベルのパターンは個別事例とずれる。インスタンス単位のシェイプレットを学習して改善する。"),
    "2605.20087v1": (
        "ThoughtTrace: 実世界のLLM対話におけるユーザの思考の理解",
        "既存データは人が「何を言ったか」だけを記録し「何を考えたか」は捉えない。実対話に、プロンプトを送った理由や応答への反応など自己申告の思考を対応付けた初の大規模データセット。"),
    "2605.20086v1": (
        "進化的コーディングエージェントは何を進化させているのか",
        "LLMと進化的探索を組み合わせたコード生成は数学的発見で成果を上げるが、実際に何を進化させているのかは不明。新規アルゴリズム構造か、再調整か、既存知識の再結合かを分析する。"),
    "2605.20085v1": (
        "一人称視点の物体操作のための空間プロンプト付き視覚軌跡予測",
        "似た物体が散らかる環境では、言語より「何をどこへ」を空間的に示す方が扱いやすい。バウンディングボックスや点の空間プロンプトでタスク目標を定義する初の定式化を提案する。"),
    "2605.20084v1": (
        "BalanceRAG: 段階的検索拡張生成のための統合的リスク較正",
        "モデル単独で十分なら毎クエリにRAGを使う必要はない。LLM単独→RAGフォールバック→棄権というカスケードを、段階別でなく統合的に較正する。"),
    "2605.20082v1": (
        "VL-DPO: 選好整合な自動運転のための視覚言語誘導ファインチューニング",
        "標準の模倣学習目的では人間の運転選好の機微を捉えきれない。VLMの推論・常識理解を活かし、自車の動き予測を人間の選好に整合させる枠組みを提案する。"),
    "2605.20079v1": (
        "確率保存型フローガイダンス",
        "CFGなどのガイダンスは速度・スコアの発見的線形結合で生成多様体の幾何を無視し、強いガイダンスで確率保存を破る。連続の式を通じてガイダンスを解析し、確率保存型に改める。"),
    "2605.20075v1": (
        "CopT: 一般・エージェント推論のための連続空間での対比的オンポリシー思考",
        "通常のCoTは「考えてから答える」順で、答えが先に分かっても無駄なトークンを費やす(パフォーマティブ推論)。思考と回答の順を反転させた推論パイプラインCopTを提案する。"),
    "2605.20074v1": (
        "組合せ最適化におけるアルゴリズム整合下での蒸留保証に向けて",
        "構造化予測では、タスクの事前知識からアルゴリズム的に整合する目標アーキテクチャを選べる。組合せ最適化で蒸留が成功する条件を、グラフニューラルネットを対象に学習理論的に解析する。"),
    "2605.20073v1": (
        "機械学習と領域成長によるX線心臓血管造影の血管セグメンテーション",
        "X線血管造影の血管抽出にピクセル分類アプローチを提案。異方性拡散やヘッセ行列ベースの特徴を抽出し、領域成長で制御する分類とランダムフォレストを用いる。"),
    "2605.20072v1": (
        "身体化LLMの探究: 観測の忠実度が高いほど問題解決を妨げるとき",
        "ロボットの認知部品としてのLLMを行動的に研究。隠れた依存関係を持つ機械パズルで、RGB・RGB-D・記号観測を比較し、観測の忠実度が高いほど性能が下がる場合があると示す。"),
    "2605.20069v1": (
        "安定なランダム選抜のための滑らかな部分くじ",
        "研究助成や入試で広がる部分くじは、評価点の僅かな変化が選抜確率を大きく変える不安定さを抱える。点数変化に滑らかに応答する、安定な部分くじ設計を提案する。"),
    "2605.20068v1": (
        "裾アニーリング: 裾の重いデータのためのフローマッチング",
        "標準的な生成モデルは裾の重いデータが苦手。ソフトログ変換を座標ごとに適用してから学習し、生成後に指数化する簡潔な手法で、べき則の裾を扱えるようにする。"),
}

# ─── HN translations (url → title_ja, summary_ja) for new items ───
hn_new = {
    "https://github.com/antoinezambelli/forge": (
        "Show HN: Forge——ガードレールで8Bモデルをエージェントタスクで大幅底上げ",
        "自前ホストの小型LLMの信頼性レイヤー。壊れた出力の自動修復・リトライ誘導・ステップ強制などのガードレールと文脈管理で、8Bモデルを多段エージェントワークフローで上位に押し上げる。"),
    "https://twitter.com/github/status/2056884788179726685": (
        "GitHub、内部リポジトリへの不正アクセスを調査中",
        "GitHubが自社の内部リポジトリへの不正アクセスを調査していると公式アカウントで発表。開発基盤の中核企業だけに波紋が広がった一報。"),
    "https://github.com/wiltodelta/remove-ai-watermarks": (
        "Remove-AI-Watermarks——AI画像の透かしを除去するCLI・ライブラリ",
        "AI生成画像に埋め込まれた透かしを除去するCLI・ライブラリ。来歴表示の取り組みが進む裏で、それを無効化するツールも公然と出回る現実を示す。"),
    "https://www.tomshardware.com/tech-industry/artificial-intelligence/college-students-drown-out-ai-praising-commencement-speeches-with-boos-deal-with-it-one-speaker-fires-back-as-students-heckle-positive-pitches-for-ais-role": (
        "卒業生がAI礼賛の祝辞をブーイングでかき消す",
        "米国の大学の卒業式で、AIを称賛する祝辞に学生がブーイングを浴びせる事例が相次ぐ。AIへの就職不安や反発が若年層に広がっていることを象徴する。"),
    "https://www.emmi.ai/news/mistral-ai-acquires-emmi-ai": (
        "Mistral AI、Emmi AIを買収",
        "欧州のAI企業MistralがEmmi AIを買収。科学・シミュレーション系AIの取り込みで、欧州勢の技術的自立を狙う動きとみられる。"),
    "https://openai.com/index/advancing-content-provenance/": (
        "OpenAI、AI画像にGoogleのSynthID透かしを採用——検証ツールも提供",
        "OpenAIがAI生成画像の来歴明示にGoogleのSynthID透かしとContent Credentialsを採用し、検証ツールを公開。競合のプロベナンス技術を採る業界標準化の動き。"),
    "https://twitter.com/github/status/2056949168208552080": (
        "GitHubが侵害される",
        "GitHub公式が侵害を確認したとするフォローアップ投稿。内部リポジトリのソースコード流出につながる大規模インシデントの続報。"),
    "https://www.bbc.com/future/article/20260519-google-tackles-attempts-to-hack-its-ai-results": (
        "GoogleのAIは操作されている——検索大手は静かに反撃",
        "Google検索のAI回答を操作しようとする試み(プロンプト注入やSEO的な細工)が横行し、Googleが水面下で対策を進めている実態をBBCが伝える。"),
    "https://www.ox.ac.uk/news/2026-05-15-why-is-almost-everyone-right-handed-the-answer-may-lie-in-how-we-learned-to-walk": (
        "なぜほぼ全員が右利きなのか——二足歩行と結びつける新研究",
        "オックスフォード大の研究。右利きの普遍性を、人類が二足歩行を学んだ過程と結びつける。AI色は薄いがHN上位に上がった科学トピック。"),
    "https://news.ycombinator.com/item?id=48210590": (
        "Ask HN: GoogleはRailwayの障害について公式声明を出すべきでは?",
        "クラウド事業者Railwayで起きた障害をめぐり、原因とされるGoogle側が公式説明を出すべきかをHNコミュニティで議論する投稿。"),
    "https://apnews.com/article/ai-college-commencement-anxiety-boo-35aec9bac660eaeb05c5b8d392db2cac": (
        "卒業生が大学の卒業式でAI礼賛の励ましにブーイング",
        "AIの役割を前向きに語る祝辞に卒業生がブーイングを浴びせる現象を、就職不安の高まりとしてAPが報じる。"),
    "https://zfhuang99.github.io/rust/claude%20code/codex/contracts/spec-driven%20development/2025/12/01/rust-with-ai.html": (
        "AIと書いたRust 10万行から得た学び(2025)",
        "Claude CodeやCodexでRustを10万行書いた経験談。仕様駆動開発や契約による設計など、AIコーディングを大規模に回すための実践知をまとめる。"),
    "https://www.bleepingcomputer.com/news/security/github-confirms-breach-of-3-800-repos-via-malicious-vscode-extension/": (
        "GitHub、悪質なVS Code拡張機能経由で内部3,800リポジトリの侵害を確認",
        "従業員が導入した悪質なVS Code拡張機能を起点に、GitHub内部の約3,800リポジトリが侵害されたと同社が確認。顧客データは影響を受けていないとする。"),
    "https://reubenbrooks.dev/blog/structural-backpressure-beats-smarter-agents/": (
        "AIコーディングループのための形式検証ゲート",
        "AIエージェントを賢くするより、ループに構造的な「逆圧(バックプレッシャー)」をかける方が効くという主張。形式検証をゲートに置くアプローチを論じる。"),
    "https://superlog.sh/": (
        "Show HN: Superlog(YC P26)——自己インストールしてバグを直す可観測性ツール",
        "YC P26のスタートアップ。自動で導入され、観測データからバグを検出・修正までこなすことを謳う可観測性プロダクト。"),
    "https://github.com/GoogleChromeLabs/css-web-ui-demos/blob/main/html-in-canvas/awesome-html-in-canvas.md": (
        "HTML-in-Canvasのデモ集",
        "Google Chrome LabsによるHTMLをCanvas内に描画する実験的機能のデモ集。AI色は薄いがWeb UI技術として注目を集めた。"),
}

# ─── Reddit translations (url → title_ja, summary_ja) for new items ───
reddit_new = {
    "https://v.redd.it/pzv3jtzdu62h1": (
        "「AI対創造性」——自称・強欲な親AI企業からの動画",
        "r/artificialで1500超のスコアを集めたバズ動画。AIと創造性の対立を、皮肉を込めて「強欲な企業」視点で描いたとされる投稿。"),
    "https://www.reddit.com/r/artificial/comments/1tif4el/google_io_2026_confirms_ai_companies_are_creating/": (
        "Google I/O 2026はAI企業が自らバブルの物語を作っていると示す",
        "I/O 2026の発表を、AI企業が需要を自ら煽る「バブルの物語」だと批判する投稿。誇大宣伝への懐疑がコミュニティで共有されている。"),
    "https://www.the-independent.com/arts-entertainment/books/news/barnes-and-noble-james-daunt-ai-books-b2978925.html": (
        "バーンズ&ノーブルCEO、AI執筆本の店頭販売を支持",
        "大手書店チェーンのCEOがAIが書いた本を店頭で売ることに前向きと表明。出版業界でのAIコンテンツ受容をめぐる議論を呼んだ。"),
    "https://v.redd.it/56ct17atm12h1": (
        "1ドル未満で作った解説動画——Claude Design + ElevenLabs",
        "Claude DesignとElevenLabsを使い1ドル未満で制作した解説動画の紹介。生成AIで動画制作のコストが激減した実例。"),
    "https://eesuck1.github.io/machine-learning-on-spherical-manifold/": (
        "球面多様体上の機械学習",
        "r/MachineLearningの研究投稿。データやパラメータが球面多様体上にある場合の機械学習手法を扱う。"),
    "https://blocknow.com/meta-stock-layoffs-8000-jobs-ai-budget-145-billion/": (
        "Metaは第1四半期に売上560億ドル——それでもAI資金のため8,000人を解雇",
        "Metaが四半期売上560億ドルの記録を出しつつ、AIインフラ投資の原資として8,000人を解雇。好業績下の大量解雇に批判が集まる。"),
    "https://i.redd.it/93fsgy1k0c2h1.jpeg": (
        "この3年の営業トークを要約すると",
        "過去3年のAI関連の売り込み文句を皮肉ったミーム的な画像投稿。誇大なセールストークへの飽きを示す。"),
    "https://www.reddit.com/r/MachineLearning/comments/1ti1tgw/icml_proceedingsonly_d/": (
        "ICML、現地発表なしのProceedings掲載のみ枠について",
        "ICMLの「Proceedings掲載のみ(現地発表なし)」枠をめぐる議論。会議の運営方針に対する研究者の反応。"),
    "https://www.reddit.com/r/MachineLearning/comments/1thxv15/eccv_2026_no_modified_date_next_to_reviews_d/": (
        "【ECCV 2026】査読に更新日が表示されない件",
        "ECCV 2026の査読システムで、レビューに更新日が表示されない問題についての議論投稿。"),
    "https://www.nytimes.com/2026/05/19/business/media/future-of-truth-ai-quotes.html?unlocked_article_code=1.jlA.lQiD.-NWf4Mb2GtWZ&amp;smid=url-share": (
        "「AI時代の真実」を論じた本に、AIがでっち上げた引用が載っていた",
        "AI時代の真実をテーマにした書籍に、AIが捏造した引用が含まれていたとNYTが報じる。AIによる事実誤りの混入を象徴する皮肉な事例。"),
    "https://www.reddit.com/r/MachineLearning/comments/1thap7a/firsttime_icml_workshop_acceptance_globalsouthml/": (
        "ICMLワークショップ初採択も、韓国への渡航費が出せない",
        "GlobalSouthMLワークショップに初採択された研究者が、開催地・韓国への渡航費を工面できず選択肢を相談する投稿。"),
}

# ─── GitHub translations (url → title_ja, summary_ja) for new items ───
github_new = {
    "https://github.com/rohitg00/ai-engineering-from-scratch": (
        "ai-engineering-from-scratch: AIエンジニアリングをゼロから",
        "AIエンジニアリングを基礎から学び、自分で作って公開するための教材リポジトリ。学習用コンテンツとして本日急上昇した。"),
    "https://github.com/ggml-org/llama.cpp": (
        "",
        "C/C++によるLLM推論の定番ライブラリ。ローカルでのモデル実行基盤として根強い人気で、本日も上位にランクインした。"),
    "https://github.com/can1357/oh-my-pi": (
        "oh-my-pi: ターミナル向けAIコーディングエージェント",
        "ハッシュ固定の編集、最適化されたツールハーネス、LSP・Python・ブラウザ・サブエージェント対応を備えるターミナル用AIコーディングエージェント。"),
}

# ─── Blog translations (url → title_ja, summary_ja) for new items ───
blogs_new = {
    "https://blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/": (
        "Google I/O 2026で発表した100のこと",
        "Google I/O 2026の全発表を100項目にまとめた一覧。Gemini 3.5、検索のAIモード、Workspace刷新などを網羅する。"),
    "https://blog.google/innovation-and-ai/models-and-research/google-research/google-beam-group-meetings/": (
        "Google Beamのグループ会議を改善する新実験",
        "3D映像通話技術Google Beamで、室内参加者と画面越し参加者が混在するグループ会議を改善する実験的機能。"),
    "https://openai.com/index/model-disproves-discrete-geometry-conjecture": (
        "OpenAIのモデルが離散幾何学の中心的予想を反証",
        "OpenAIの内部汎用モデルが、80年来の「単位距離問題」に関する予想を反証。代数的整数論を駆使した無限族の構成を見つけ、AIが数学の未解決問題を自律的に解いた初の事例とされる。"),
    "https://openai.com/index/the-next-phase-of-education-for-countries": (
        "OpenAIの「国家向け教育」プログラム、次の段階へ",
        "OpenAIが学校でのAI導入を進める「Education for Countries」を拡大。新たな提携、教員研修、学習成果向上のためのツールを展開する。"),
    "https://openai.com/index/introducing-openai-for-singapore": (
        "OpenAI for Singaporeを発表",
        "OpenAIがシンガポールと複数年のAIパートナーシップを開始。展開拡大、現地人材育成、企業・公共サービスのAI活用を支援する。"),
}

# ─── Apply enrichment ───
for it in d["sources"]["arxiv"]:
    t = arxiv_map.get(it["id"])
    if t:
        it["title_ja"], it["summary_ja"] = t

new_maps = {"hn": hn_new, "reddit": reddit_new, "github": github_new, "blogs": blogs_new}
for src, nmap in new_maps.items():
    for it in d["sources"][src]:
        url = it.get("url")
        if url in nmap:
            tj, sj = nmap[url]
            if tj:
                it["title_ja"] = tj
            it["summary_ja"] = sj
        elif url in prev_url:
            tj, sj = prev_url[url]
            if tj:
                it["title_ja"] = tj
            if sj:
                it["summary_ja"] = sj

# ─── Highlights ───
d["highlights"] = [
    {
        "source": "blogs",
        "title": "An OpenAI model has disproved a central conjecture in discrete geometry",
        "title_ja": "OpenAIのモデルが離散幾何学の中心的予想を反証——AIが数学の未解決問題を初めて自力で解いた",
        "url": "https://openai.com/index/model-disproves-discrete-geometry-conjecture",
        "hot_take_ja": "ベンチマークの高得点とは次元が違う話だ。OpenAIの内部モデルが、エルデシュが1946年に提起した「単位距離問題」をめぐる予想を反証し、80年間誰も超えられなかった構成を上回る無限族を見つけた。しかも数学専用に特訓したモデルではなく汎用モデル——「AIが数学の最前線を自律的に押し進めた初の事例」と呼ばれるのも誇張ではない。",
        "detail_ja": "OpenAIは、自社の内部汎用モデルが離散幾何学の長年の予想を反証したと発表した。対象は、数学者ポール・エルデシュが1946年に提起した「単位距離問題(unit distance problem)」に関連する予想——平面上にn個の点を置いたとき、ちょうど距離1で結ばれる点ペアをどれだけ多く作れるか、という問題だ。約80年にわたり、最良の構成は正方格子に近い形だと広く信じられてきた。今回モデルが見つけたのは、それを上回る「まったく新しい構成の無限族」で、多項式オーダーの改善をもたらすという。鍵となったのは代数的整数論の道具立てだ。ガウス整数をより複雑な数体の一般化に置き換え、無限類体塔やゴロド-シャファレヴィチ理論といった高度な概念を用いて、単位長の差をはるかに多く生む豊かな対称性を引き出した。証明は外部の数学者グループによって検証され、著名な数学者ティモシー・ガワーズはこの成果を「迷いなくAnnals of Mathematicsに推薦する」と述べたと報じられている。重要なのは、これが数学専用に設計・訓練されたモデルではなく、汎用言語モデルだった点だ。注意したいのは、これは「人間が思いつかなかった構成をAIが発見した」事例であって、AIが数学全体を肩代わりできるという話ではないこと——とはいえ、分野の中心にある未解決問題が自律的に崩された意味は大きい。",
        "detail_en": "OpenAI announced that its internal general-purpose model has disproved a longstanding conjecture in discrete geometry. The target is a conjecture tied to the \"unit distance problem,\" posed by the mathematician Paul Erdős in 1946: given n points in the plane, how many pairs can be connected at exactly distance 1? For nearly 80 years, the best constructions were widely believed to look roughly like square grids. The model found \"an entirely new family of constructions\" that beats them, yielding a polynomial-order improvement. The key was machinery from algebraic number theory: it replaced the Gaussian integers with more complicated generalizations from number fields, drawing on advanced concepts such as infinite class field towers and Golod–Shafarevich theory to extract richer symmetries that produce far more unit-length differences. The proof was checked by a group of external mathematicians, and the prominent mathematician Timothy Gowers reportedly said he would recommend the work to the Annals of Mathematics \"without any hesitation.\" Crucially, this was not a model designed or trained specifically for mathematics — it was a general-purpose language model. One caveat: this is a case of AI discovering a construction humans had not thought of, not a claim that AI can take over mathematics wholesale — but the autonomous toppling of an open problem central to a field is significant nonetheless.",
        "key_points_ja": [
            "エルデシュが1946年に提起した「単位距離問題」の予想を反証",
            "80年信じられた「正方格子が最良」を覆す無限族を発見",
            "多項式オーダーの改善——代数的整数論が鍵",
            "無限類体塔やゴロド-シャファレヴィチ理論を活用",
            "数学専用でなく汎用モデルが達成した点が画期的",
            "証明は外部数学者が検証、ガワーズも高評価",
        ],
        "key_points_en": [
            "Disproves a conjecture tied to Erdős's 1946 unit distance problem",
            "Finds an infinite family beating the 80-year 'square grid' belief",
            "Polynomial-order improvement, driven by algebraic number theory",
            "Uses infinite class field towers and Golod–Shafarevich theory",
            "Done by a general-purpose model, not a math-specialized one",
            "Proof checked by external mathematicians; praised by Gowers",
        ],
    },
    {
        "source": "hn",
        "title": "GitHub confirms breach of 3,800 repos via malicious VSCode extension",
        "title_ja": "GitHub、悪質なVS Code拡張機能経由で内部3,800リポジトリの侵害を確認",
        "url": "https://www.bleepingcomputer.com/news/security/github-confirms-breach-of-3-800-repos-via-malicious-vscode-extension/",
        "hot_take_ja": "開発者の信頼を一身に背負うGitHub自身が、たった一人の従業員が入れた悪質なVS Code拡張機能から侵害された。サプライチェーン攻撃の弱点はもはやコードそのものではなく、開発環境に気軽に足す「拡張機能」だ。AIコーディング全盛で誰もが拡張やエージェントを盛る今、この一件は刺さる。",
        "detail_ja": "GitHubは、自社内部の約3,800リポジトリが侵害されたと確認した。侵入経路は、ある従業員が公式のVS Codeマーケットプレイスからダウンロードした悪質なVS Code拡張機能だった。拡張機能がインストールされた端末を足がかりに、攻撃者は内部リポジトリのソースコードを窃取した。GitHubは、影響を受けたリポジトリの外部に保存された顧客データは侵害されていないとしている。対応として同社は当該拡張機能をマーケットプレイスから削除し、侵害された端末を隔離してインシデント対応を開始した。報じられたタイムラインでは、GitHubは検知と封じ込めを前日に行ったとされ、「TeamPCP」を名乗るハッカー集団が地下フォーラムで犯行を主張し、窃取データに対し少なくとも5万ドルを要求したという。この事件が重いのは、攻撃対象が世界中の開発を支えるGitHub自身であり、しかも入口が「正規マーケットプレイスの拡張機能」だった点だ。VS Code拡張やIDEプラグインは強い権限で動くことが多く、審査をすり抜けた悪質拡張は実質的にマルウェアになりうる。AIコーディングツールやエージェントを拡張として次々に導入する流れの中で、開発環境そのものが攻撃面になっているという警鐘である。なお、攻撃の細部や被害範囲は調査が続いており、続報で更新される可能性がある。",
        "detail_en": "GitHub has confirmed that roughly 3,800 of its internal repositories were breached. The entry point was a malicious VS Code extension that an employee downloaded from the official VS Code Marketplace. Using the device where the extension was installed as a foothold, attackers exfiltrated source code from internal repositories. GitHub says customer data stored outside the affected repos was not compromised. In response, the company removed the malicious extension from the marketplace, isolated the compromised device, and launched incident response. On the reported timeline, GitHub detected and contained the breach the previous day, and a hacker group calling itself \"TeamPCP\" claimed responsibility on an underground forum, demanding at least $50,000 for the stolen data. What makes this serious is that the target was GitHub itself — the backbone of software development worldwide — and that the entry point was an extension from a legitimate marketplace. VS Code extensions and IDE plugins often run with broad privileges, so a malicious extension that slips past review is effectively malware. As developers pile on AI coding tools and agents as extensions, this is a warning that the development environment itself has become an attack surface. Note that the details of the attack and its full scope are still under investigation and may be updated in follow-up reporting.",
        "key_points_ja": [
            "GitHub内部の約3,800リポジトリが侵害される",
            "侵入経路は従業員が入れた悪質なVS Code拡張機能",
            "攻撃者は内部ソースコードを窃取、顧客データは無事とする",
            "GitHubは拡張を削除・端末隔離・インシデント対応を実施",
            "「TeamPCP」が犯行主張、5万ドル以上を要求と報道",
            "開発環境の拡張機能が新たな攻撃面に",
        ],
        "key_points_en": [
            "~3,800 GitHub-internal repos breached",
            "Entry point: a malicious VS Code extension an employee installed",
            "Attackers exfiltrated internal source code; customer data said safe",
            "GitHub removed the extension, isolated the device, started IR",
            "'TeamPCP' claimed it, reportedly demanding $50,000+",
            "Dev-environment extensions are now an attack surface",
        ],
    },
    {
        "source": "hn",
        "title": "Show HN: Forge – Guardrails take an 8B model from 53% to 99% on agentic tasks",
        "title_ja": "Show HN: Forge——ガードレールで8Bモデルをエージェントタスクで大幅底上げ",
        "url": "https://github.com/antoinezambelli/forge",
        "hot_take_ja": "「もっと賢いモデル」ではなく「もっと固い足場」。Forgeは8Bのローカルモデルに、出力の整形修復・リトライ誘導・ステップ強制といったガードレールをかぶせ、多段エージェントタスクの成功率を大きく押し上げる。プロキシ越しだとクライアントは“賢いモデルと話している”と錯覚する——スカフォールディングがモデル規模を肩代わりした好例だ。",
        "detail_ja": "「Forge」は、自前ホストの小型LLMでツール呼び出しや多段エージェントワークフローを安定させるための信頼性レイヤーだ。Hacker Newsには「ガードレールで8Bモデルを53%→99%に」というキャッチで投稿され、636ポイントを集めた。Forgeの発想は、モデルそのものを賢くするのではなく、モデルの周りに「足場(スカフォールディング)」を組むことにある。具体的には、壊れたツール呼び出し出力を自動修復する「レスキューパース」、誤りを優しく直させる「リトライ誘導」、必要な手順を順守させる「ステップ強制」、そしてVRAMを意識した文脈圧縮といったガードレールを重ねる。プロジェクトのREADMEによれば、現行の最良構成(Ministral-3 8B Instruct Q8 を llama-server で実行)は26シナリオの評価スイートで86.5%、最難関ティアで76%を記録するという。使い方は3通り——ワークフローを直接回す、自前のループにミドルウェアとして差し込む、あるいはOpenAI互換のプロキシとして既存クライアントの前に置く。プロキシ越しだと、クライアント側は「より賢いモデルと話している」と錯覚するという。これは、エージェント性能を上げる近道がパラメータ増大だけではなく、出力の検証と矯正という地味な工学にもあることを示す。今週のarXivにも「形式検証ゲート」や「確率-決定境界」など同じ思想の論文が並んでおり、「賢いエージェントより構造的なバックプレッシャー(逆圧)」という潮流の一例といえる。なお53%→99%という数値は投稿者の打ち出しで、READMEの公式数値とは測定条件が異なる点には留意したい。",
        "detail_en": "\"Forge\" is a reliability layer for stabilizing tool-calling and multi-step agentic workflows on self-hosted small LLMs. It was posted to Hacker News under the headline \"Guardrails take an 8B model from 53% to 99% on agentic tasks\" and drew 636 points. Forge's idea is not to make the model itself smarter but to build scaffolding around it. Concretely, it stacks guardrails: \"rescue parsing\" that auto-repairs malformed tool-call outputs, \"retry nudges\" that gently steer the model to fix errors, \"step enforcement\" that ensures required steps happen in order, and VRAM-aware context compaction. Per the project's README, its current best config (Ministral-3 8B Instruct Q8 on llama-server) scores 86.5% across a 26-scenario eval suite and 76% on the hardest tier. There are three ways to use it: run workflows directly, drop it into your own loop as middleware, or place it in front of existing clients as an OpenAI-compatible proxy — through the proxy, the client \"thinks it's talking to a smarter model.\" The takeaway is that the shortcut to better agentic performance isn't only more parameters; it's also the unglamorous engineering of verifying and correcting outputs. This week's arXiv echoes the same idea — papers on \"formal verification gates\" and the \"stochastic-deterministic boundary\" — making Forge one example of a \"structural backpressure beats smarter agents\" trend. Note that the \"53%→99%\" figure is the submitter's framing and uses different measurement conditions than the README's official numbers.",
        "key_points_ja": [
            "自前ホストの小型LLM向け信頼性レイヤー「Forge」",
            "モデルを賢くせず、周囲に「足場」を組む発想",
            "レスキューパース・リトライ誘導・ステップ強制が中核",
            "公式では8B最良構成が26シナリオで86.5%",
            "OpenAI互換プロキシで既存クライアントに透過適用",
            "「賢いエージェントより構造的バックプレッシャー」の潮流",
        ],
        "key_points_en": [
            "'Forge': a reliability layer for self-hosted small LLMs",
            "Don't make the model smarter — build scaffolding around it",
            "Rescue parsing, retry nudges, step enforcement at the core",
            "Official best 8B config scores 86.5% on 26 scenarios",
            "OpenAI-compatible proxy applies guardrails transparently",
            "Part of a 'structural backpressure beats smarter agents' trend",
        ],
    },
    {
        "source": "blogs",
        "title": "OpenAI adopts SynthID watermarking — as a watermark-removal tool trends the same day",
        "title_ja": "OpenAIがAI画像にSynthID透かしを採用——その同じ日、透かし除去ツールが急上昇",
        "url": "https://openai.com/index/advancing-content-provenance",
        "hot_take_ja": "来歴(プロベナンス)はいたちごっこだ。OpenAIがAI画像にGoogleのSynthID透かしとContent Credentialsを採用し検証ツールまで出した同じ日、Hacker Newsでは「AI透かしを消すCLI」が368ポイントを集めて急上昇した。透かしを入れる側と消す側が同じタイムラインに並ぶ——これがAIコンテンツ真正性の現実だ。",
        "detail_ja": "OpenAIは「コンテンツの来歴(プロベナンス)」を前進させる取り組みを発表した。AI生成画像にContent Credentials(C2PA)のメタデータを付与し、さらにGoogleが開発した不可視の電子透かし技術「SynthID」を採用、加えて画像が自社モデル由来かを判定する検証ツールも公開する内容だ。狙いは、AI生成メディアの出所を辿れるようにして信頼性を担保することにある。皮肉なのは、これとほぼ同じ日に、Hacker Newsで「Remove-AI-Watermarks」というAI画像の透かしを除去するCLI・ライブラリが368ポイントを集めて上位に上がったことだ。来歴技術には大きく二系統ある——画像に付随する署名付きメタデータ(C2PAのように削除されやすい)と、ピクセルに埋め込む不可視透かし(SynthIDのように頑健性を狙う)だ。前者はファイルを再エンコードするだけで落ちやすく、後者も加工・圧縮・除去ツールで弱められうる。つまり「入れる側」と「消す側」が同時並行で進歩する構造で、透かしは万能の真正性証明にはならない。それでも、何もないよりは検証の手掛かりになる——プロベナンスは「決定的な証明」ではなく「確率を上げる仕組み」と捉えるのが妥当だ。一方で、OpenAIが競合であるGoogleのSynthIDに収束した点は、技術が乱立せず標準化へ向かう前向きな兆候とも読める。",
        "detail_en": "OpenAI announced an initiative to advance \"content provenance.\" It attaches Content Credentials (C2PA) metadata to AI-generated images, adopts SynthID — the invisible digital watermarking technology developed by Google — and releases a verification tool that checks whether an image came from OpenAI's models. The goal is to make the origin of AI-generated media traceable and to bolster trust. The irony is that on roughly the same day, a CLI and library called \"Remove-AI-Watermarks\" for stripping watermarks from AI images climbed Hacker News with 368 points. Provenance tech comes in two broad flavors: signed metadata attached to a file (like C2PA, which is easy to strip) and invisible watermarks embedded in the pixels (like SynthID, which aims for robustness). The former is easily lost just by re-encoding a file, and the latter can be weakened by editing, compression, or removal tools. In other words, the \"adders\" and the \"removers\" advance in parallel, and watermarks are not a foolproof proof of authenticity. Still, they are better than nothing as a verification signal — provenance is best understood as a mechanism that raises the odds, not a definitive proof. On the other hand, OpenAI converging on Google's SynthID — a competitor's technology — can be read as a positive sign that the field is moving toward standardization rather than a thicket of incompatible schemes.",
        "key_points_ja": [
            "OpenAIがAI画像にC2PAメタデータとSynthID透かしを採用",
            "画像が自社モデル由来かを判定する検証ツールも公開",
            "同日、HNで「AI透かし除去CLI」が368点で急上昇",
            "来歴技術は署名メタデータと不可視透かしの2系統",
            "どちらも再エンコードや除去ツールで弱められうる",
            "競合SynthIDへの収束は標準化として前向きな兆候",
        ],
        "key_points_en": [
            "OpenAI adopts C2PA metadata and SynthID watermarks for AI images",
            "Also releases a tool to verify if an image is from its models",
            "Same day, an 'AI watermark remover' CLI hit 368 points on HN",
            "Provenance tech: signed metadata vs. invisible watermarks",
            "Both can be weakened by re-encoding or removal tools",
            "Converging on SynthID is a positive sign for standardization",
        ],
    },
    {
        "source": "reddit",
        "title": "Meta Made $56B in Q1 and Is Still Firing 8,000 People to Pay for AI",
        "title_ja": "Metaは第1四半期に売上560億ドル——それでもAI資金のため8,000人を解雇",
        "url": "https://www.reddit.com/r/artificial/comments/1thq6cn/meta_made_56b_in_q1_and_is_still_firing_8000/",
        "hot_take_ja": "数字の対比が生々しい。Metaは四半期売上560億ドル・純利益も過去最高級という絶好調の中で、約8,000人を解雇する。理由は「AIインフラへの投資原資」——2026年のAI設備投資は最大1,450億ドルに膨らむ見込みだ。好況下のリストラは、AIの計算コストが人件費を直接押しのけ始めたことの証拠といえる。",
        "detail_ja": "Metaが2026年第1四半期に四半期売上約560億ドル(前年比約33%増)、純利益も過去最高水準を記録した一方で、約8,000人の解雇に踏み切ったことが大きな話題になっている。Reddit上では「560億ドル稼いでなお8,000人解雇」という見出しで批判が集中した。同社の説明によれば、解雇の主因はAIインフラへの投資原資の確保だ。マーク・ザッカーバーグCEOは人員削減をAI支出の急増と明確に結びつけており、2026年のAI設備投資(データセンター、NVIDIAのGPU、自社シリコンなど)は最大で約1,450億ドルに達する見込みだという。報道によれば、今回の解雇は2023年の大規模再編以来で最大規模で、加えて約6,000件の未充足求人(オープンな採用枠)も取り消され、実質的な人員縮小は1万4,000人規模に及ぶ。アナリストの試算では、解雇により年間70〜80億ドルのコスト削減が見込まれ、巨額のインフラ投資の一部を相殺するという。ここで重要なのは、これが業績不振によるリストラではないという点だ。会社は記録的な利益を上げており、それでも人を切ってAIに資金を回している。つまりAIの計算資源コストが、企業の予算配分の中で人件費と直接トレードオフされ始めた——その象徴的な事例といえる。一方で、これがAI投資の合理的な配分なのか、それとも過剰投資(バブル)の兆候なのかは、まだ評価が分かれる。",
        "detail_en": "Meta posting roughly $56 billion in quarterly revenue in Q1 2026 (up about 33% year over year) and near-record net income — while still cutting about 8,000 jobs — has become a major talking point. On Reddit, criticism converged under the headline \"Made $56B and is still firing 8,000 people.\" By the company's own account, the layoffs are mainly about freeing up funds for AI infrastructure. CEO Mark Zuckerberg has explicitly tied the headcount cuts to surging AI spending, with 2026 AI capital expenditure (data centers, NVIDIA GPUs, custom silicon, and more) projected to reach up to roughly $145 billion. According to reporting, this is Meta's largest round of cuts since its 2023 restructuring, and on top of it about 6,000 unfilled job requisitions were canceled, bringing the effective headcount reduction to around 14,000. Analysts estimate the layoffs could yield $7–8 billion in annual cost savings, offsetting part of the massive infrastructure spend. The key point is that this is not a restructuring driven by poor performance: the company is posting record profits and is still cutting people to redirect money into AI. In other words, the cost of AI compute is starting to trade off directly against headcount in corporate budgets — a symbolic example of that shift. Whether this represents a rational allocation toward AI or a sign of overinvestment (a bubble) remains a matter of debate.",
        "key_points_ja": [
            "Metaは第1四半期に売上約560億ドル、純利益も過去最高級",
            "それでも約8,000人を解雇、AIインフラ投資が原資",
            "2026年のAI設備投資は最大約1,450億ドルの見込み",
            "未充足求人6,000件も取消、実質1.4万人規模の縮小",
            "業績不振でなく好況下のリストラという点が異例",
            "AIの計算コストが人件費と直接トレードオフに",
        ],
        "key_points_en": [
            "Meta posted ~$56B Q1 revenue and near-record net income",
            "Still cut ~8,000 jobs, funding AI infrastructure",
            "2026 AI capex projected at up to ~$145B",
            "6,000 open reqs also canceled — effective cut near 14,000",
            "Unusual: layoffs amid record profits, not weak results",
            "AI compute cost now trades off directly against headcount",
        ],
    },
]

# ─── Coverage check ───
missing = []
for src in ("arxiv", "hn", "reddit", "github", "blogs"):
    for it in d["sources"][src]:
        if not it.get("summary_ja"):
            missing.append((src, it.get("id") or it.get("url") or it.get("title")))
if missing:
    print(f"WARNING: {len(missing)} items without summary_ja:")
    for m in missing:
        print("  ", m)
else:
    print("All items enriched.")

OUT.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"Wrote {OUT} ({len(d['highlights'])} highlights)")
