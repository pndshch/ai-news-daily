#!/usr/bin/env python3
"""Enrichment for 2026-05-22 (fresh page).

arXiv set is fully new (50 items, all translated below).
HN/Reddit/GitHub/blogs reuse prior Japanese translations for overlapping
URLs (from data/2026-05-21.json) and translate new items inline.
Five fresh highlights are selected for the day.
"""
import json
from pathlib import Path

DATE = "2026-05-22"
PREV = "2026-05-21"
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
    "2605.22821v1": (
        "凸緩和によるトークン化",
        "BPEやUnigramなど現在のトークナイザは局所最適な貪欲法で、語彙全体を考慮しない。本研究はトークナイザ構築を線形計画(凸緩和)として定式化し、語彙を大域的に最適化する手法を提案する。"),
    "2605.22823v1": (
        "どちらに動いた? 動画LLMの「運動方向盲」を診断し克服する",
        "動画LLMは時間的理解で進歩したが、物体が左右上下のどちらに動いたかという基本的な符号付き運動方向の知覚でほぼ偶然並みの精度しか出ない。この「運動方向盲」を診断し克服する手法を示す。"),
    "2605.22820v1": (
        "ニューラル需要ポテンシャルによる可積分な弾力性",
        "小売の多品目需要を、対数価格の滑らかな文脈依存関数として対数需要を学習するニューラルモデル(ICDN)で表現。学習した需要曲面から価格弾力性を厳密に導出できる。"),
    "2605.22819v1": (
        "Cambrian-P: カメラ姿勢に接地した動画理解",
        "動画理解のマルチモーダルLLMはフレームを孤立した2D画像として扱い、カメラ位置・向きの情報を失っている。各視点のカメラ姿勢を共有空間座標系として明示的に組み込み動画理解を改善する。"),
    "2605.22818v1": (
        "MotiMotion: 視覚推論を伴う運動制御型動画生成",
        "既存の運動制御型image-to-video生成はユーザ指定の軌跡を硬直的に追い、二次的な因果結果を見落として不自然な結果を生む。視覚推論を導入し物理的に妥当な動画生成を目指す。"),
    "2605.22817v1": (
        "ベクトルポリシー最適化: 多様性のための学習がテスト時探索を向上させる",
        "AlphaEvolveのような推論時探索は多様な報酬でロールアウトを選別するが、標準のLLM事後学習は単一目的に最適化し多様性を欠く。多様性を促す学習でテスト時探索性能を高める。"),
    "2605.22816v1": (
        "AwareVLN: 自己認識による視覚言語ナビゲーション",
        "視覚言語ナビゲーションでVLMの推論を使う最先端手法は、自分の行動への明示的な自己認識を欠く。エージェントに自己認識的推論を持たせ、言語指示と自己の移動の接地を改善する。"),
    "2605.22814v1": (
        "好奇心を忘れずに: エピソード文脈と持続的世界による3D探索",
        "疎報酬・長期タスクの3D環境では探索が学習の前提となる。好奇心駆動の強化学習にエピソード的文脈と持続的な世界モデルを導入し、効率的な探索を実現する。"),
    "2605.22812v1": (
        "GesVLA: ジェスチャを認識する視覚言語行動モデル",
        "VLA(視覚言語行動)モデルは汎用ロボット操作で有望だが、テキスト指示中心で、複数の似た物体がある場面の空間的曖昧さを解けない。指差しなどのジェスチャを取り込み曖昧性を解消する。"),
    "2605.22809v1": (
        "Sensor2Sensor: 自動運転のための車種横断センサ変換",
        "自動運転の学習・検証には大規模で多様なデータが必要だが、各車のセンサ構成は異なる。あるセンサ構成のデータを別の構成へ変換し、データの多様性と規模を補う。"),
    "2605.22800v1": (
        "マッチング原理: ノイズ要因に頑健な表現学習のための損失関数の幾何学理論",
        "ロバスト性・ドメイン適応・不変性・整合安全性などは別々の手法群で扱われがち。これらに共通する幾何構造を「マッチング原理」として統一的に説明する理論を提案する。"),
    "2605.22795v1": (
        "保存的・非保存的ドリフトモデルの有限粒子収束率",
        "1ステップ生成モデルのドリフト速度を、カーネル密度推定の勾配速度に置き換える保存的ドリフト法を提案。有限粒子での収束率を理論的に解析する。"),
    "2605.22794v1": (
        "MOSS: ソースコード書き換えによる自律エージェントの自己進化",
        "既存の自己進化エージェントはスキルファイルやプロンプトなどテキスト成果物の改変に留まり、エージェントのハーネス(ルーティングやフック順序)はコード上にあり手が届かない。エージェント自身が自分のソースコードを書き換えて進化する枠組みを提案する。"),
    "2605.22791v1": (
        "Gated DeltaNet-2: 線形注意における消去と書き込みの分離",
        "線形注意は固定長の再帰状態でsoftmax注意の無制限キャッシュを置き換える。圧縮メモリの「消去」と「書き込み」を分離し、既存の連想を壊さずに編集できるようにする。"),
    "2605.22786v1": (
        "LCGuard: マルチエージェント系の安全なKV共有のための潜在通信ガード",
        "LLMマルチエージェント系はKVキャッシュを介した潜在通信で効率化できるが安全性に懸念がある。潜在通信を監視・防御するガード機構を提案する。"),
    "2605.22785v1": (
        "ニュースの仲介者としての商用AIチャットボットの評価",
        "AIチャットボットがニュース接触の経路になりつつあるが、新出の事実を言語・地域横断でどれだけ正確に扱うかは未測定。14日間にわたり商用チャットボットのニュース処理精度を体系的に評価する。"),
    "2605.22781v1": (
        "DeltaBox: ミリ秒級サンドボックスのチェックポイント/ロールバックでステートフルなAIエージェントをスケール",
        "テスト時木探索や強化学習を行うAIエージェントは、ファイルやプロセス状態を含む完全なサンドボックス状態の高速な保存・復元を要する。ミリ秒級のチェックポイント/ロールバックを実現する。"),
    "2605.22779v1": (
        "FAME: メッセージ単位のログ異常検知のための失敗認識MoE",
        "既存のログ異常検知はセッションやウィンドウ単位で粗く、運用者は多数の通常行を確認させられる。失敗を認識するMixture-of-Expertsで、原因となる個々のログメッセージを特定する。"),
    "2605.22777v1": (
        "DecQ: 表現オートエンコーダのための詳細凝縮クエリ",
        "表現オートエンコーダ(RAE)は凍結した視覚基盤モデルをトークナイザに使うが、凍結ゆえに空間的表現が制約される。詳細を凝縮するクエリで再構成・生成の品質を高める。"),
    "2605.22776v1": (
        "SDPM: 連続時間生存解析のための生存拡散確率モデル",
        "生存解析はハザード関数に構造的仮定を置くか時間軸を離散化しがちで柔軟性に欠ける。拡散確率モデルで連続時間のイベント発生時刻分布を直接推定する。"),
    "2605.22775v1": (
        "MambaGaze: 視線追跡データからの認知負荷推定のための双方向Mamba",
        "視線データからのリアルタイム認知負荷推定は、まばたきによる頻繁な欠損が課題。欠損を明示的にモデル化する双方向Mambaで頑健に認知負荷を推定する。"),
    "2605.22774v1": (
        "CogAdapt: 臨床ECG基盤モデルをウェアラブルの認知負荷推定へ転移する",
        "臨床ECGで事前学習した基盤モデルは豊かな表現を持つが、ウェアラブルにはそのまま使えない。誘導(リード)適応で臨床基盤モデルをウェアラブルの認知負荷推定へ転移する。"),
    "2605.22773v1": (
        "ジョブのランダム到着を伴う柔軟ジョブショップスケジューリングへの深層強化学習",
        "柔軟ジョブショップ問題は将来ジョブの予測不能な到着と組合せ的複雑性が課題。深層強化学習でランダム到着下のスケジューリングを行う。"),
    "2605.22771v1": (
        "整合性学習による政治的操作の低減",
        "LLMは政治的に対立する話題を非対称に扱う「隠れた政治バイアス」を示す。7類型の操作技法を特定し、整合性学習でこのバイアスを低減する。"),
    "2605.22769v1": (
        "LLM事前学習におけるデータの時間性の影響を理解する",
        "LLMは通常シャッフルしたコーパスで学習され、知識が学習時で凍結し時間的接地が不明瞭。事前学習の動態が時間依存の事実知識の獲得にどう影響するかを調べる。"),
    "2605.22767v1": (
        "合成データだけで十分か? 小児希少疾患認識のデータ不足を再考する",
        "希少遺伝疾患の小児は特徴的な顔貌を示すが、データ不足とプライバシー制約で診断システム開発が困難。合成データのみでどこまで認識できるかを検証する。"),
    "2605.22765v1": (
        "一様拡散モデルの再考: Leave-One-Out復元器と吸収状態への再定式化",
        "離散拡散モデルはクリーンデータ予測で学習されるが逆過程の定義法が複数ある。一様拡散モデルにおけるLeave-One-Out復元器と、吸収状態への再定式化を提示する。"),
    "2605.22763v1": (
        "AI駆動の形式的証明探索で数学研究を前進させる",
        "LLMは数学的推論に長けるが信頼性の低さが研究利用を妨げる。緩和策としてLeanなど形式言語で証明を生成させる手法について、本研究は初の大規模な検討を行う。"),
    "2605.22759v1": (
        "ウェアラブル健康データのための汎用知能とインターフェース",
        "ウェアラブルセンサは豊富な行動・生理情報を捉えるが、低次の信号を個別化された健康インサイトに変えるのは難しい。汎用的なモデルとインターフェースで橋渡しする。"),
    "2605.22756v1": (
        "Lumberjack: 木のヘビーヒッタ検出による差分プライバシー対応ランダムフォレスト",
        "ランダムフォレストへの差分プライバシー(DP)付与は通常、性能を実用不能なほど劣化させる。木の中のヘビーヒッタを検出し、実用的なDPランダムフォレストを実現する。"),
    "2605.22751v1": (
        "AI生成画像検出のためのスペクトル裾の補助学習",
        "生成モデルの進化で本物との知覚的差が縮まり、AI生成画像の検出が困難になっている。周波数領域のスペクトル裾を補助タスクとして学習し検出精度を高める。"),
    "2605.22749v1": (
        "IoT対応スマートグリッドのサイバー物理異常検知",
        "高密度な計測インフラを持つスマートグリッドはサイバー物理攻撃に脆弱。機械学習とメタヒューリスティックな特徴最適化で異常を検知する。"),
    "2605.22748v1": (
        "マルチエージェント強化学習による超人的で安全・俊敏なレーシング",
        "自律システムは単独・シミュレーションでは超人的だが、他者と共有する動的空間では脆い。マルチエージェント強化学習で空間を共有しつつ安全かつ俊敏に走るレーシングを実現する。"),
    "2605.22746v1": (
        "証拠的深層学習のためのプラグイン損失",
        "証拠的深層学習(EDL)は1パスで不確実性を推定できる。Softmax分類器も包含する、簡素な枠組みのプラグイン損失を提案する。"),
    "2605.22743v1": (
        "SeqLoRA: 継続的な複数概念生成のための二段階直交適応",
        "パラメータ効率の良い微調整で拡散モデルを個別化できるが、複数の独自概念の合成は表現干渉で難しい。二段階の直交適応で継続的に複数概念を生成する。"),
    "2605.22740v1": (
        "局所適応的な不確実性ゾーンを持つ三分決定木",
        "決定木は硬い二分閾値で、境界から遠い点も境界上の点も同じ信頼度を割り当てる。各分岐に不確実性ゾーンを加える三分決定木を導入する。"),
    "2605.22738v1": (
        "Shapley・Banzhaf相互作用のプロキシベース近似",
        "ShapleyやBanzhafの高次相互作用の推定器は速度と精度がトレードオフの関係にある。プロキシを用いて高速かつ正確に相互作用を近似する。"),
    "2605.22737v1": (
        "蒸留ゲーム: 適応的攻撃と効率的防御",
        "モデルの有用な出力は、同時に模倣(蒸留攻撃)も容易にする。有用性に制約された教師と攻撃者のミニマックスゲームとして、このトレードオフを分析する。"),
    "2605.22736v1": (
        "多様体の交差上での最適化",
        "2つの多様体の交差上での最適化は実行可能領域の幾何が結合し難しい。クリーンな交差と内在的な正則性の条件下でこの問題を解析する。"),
    "2605.22734v1": (
        "ChronoMedKG: 時間に接地した生物医学知識グラフと臨床推論ベンチマーク",
        "生物医学知識グラフは疾患関連を静的な事実として扱うが、年齢など時間情報は臨床推論に重要。時間に接地した知識グラフと臨床推論ベンチマークを提案する。"),
    "2605.22733v1": (
        "HarnessAPI: ストリーミングAPIとMCPツールを統合するスキル優先フレームワーク",
        "LLMツールとして使うPython関数は、人間向けHTTPエンドポイントとエージェント向けMCPツール登録の二重定義を強いられる。両者を1つのスキル定義から統合する。"),
    "2605.22732v1": (
        "音響感情認識を超えて: LLMと音響モデルによる政治演説のマルチモーダルなパトス分析",
        "音響感情認識モデルが政治演説の「パトス(情動的訴求)」次元の代理になりうるかを検証。ドイツ連邦議会の演説を題材にLLMと音響モデルを組み合わせる。"),
    "2605.22731v1": (
        "事後学習はトークンでなく「状態」の問題: SFT・RL・オンポリシー蒸留の状態分布的視点",
        "SFT・強化学習・蒸留は通常それぞれの損失関数で分析される。本研究はこれらを「状態分布」の観点から統一的に捉え直し、事後学習の本質はトークンでなく状態にあると論じる。"),
    "2605.22724v1": (
        "複数ニューラル作用素はマルチタスク学習でほぼ最適なレートを達成する",
        "共有のマルチタスク設定で作用素の集合を学習する近似・統計的複雑性を研究。複数ニューラル作用素(MNO)アーキテクチャがほぼ最適なレートを達成することを示す。"),
    "2605.22723v1": (
        "ガウスDDPMにおける共分散マッチングの価値とLanczosサンプラ",
        "ガウスDDPMの中心的な誤差指標は、逆過程のパス空間KLダイバージェンス。共分散マッチングの価値を分析し、Lanczosサンプラを提案する。"),
    "2605.22722v1": (
        "N3P: 学習ベースの自然な三段階方式による高速自動駐車",
        "自動駐車はHybrid A*が広く使われるが計算が重く、強化学習手法も課題が残る。学習ベースの自然な三段階方式で、運動学的に妥当かつ高速な駐車経路を計画する。"),
    "2605.22720v1": (
        "AIは紛争を悪化させうるか? 紛争下のLLM展開におけるアラインメント失敗",
        "武力紛争下の社会でもAIは既に使われているが、その妥当性を確認する確立した手法がない。複数の紛争文脈にわたるLLM展開のアラインメント失敗を検証する。"),
    "2605.22719v1": (
        "活性化からタスク失敗を読み取る: GPT-2 SmallのIOI課題のスパース特徴監査",
        "間接目的語同定(IOI)課題で、GPT-2 Smallが失敗・成功した試行でどのスパースオートエンコーダ特徴が異なって発火するかを、再現可能な形で監査する。"),
    "2605.22718v1": (
        "WorldKV: 世界検索と圧縮による効率的な世界メモリ",
        "自己回帰的な動画拡散モデルはリアルタイムな世界生成を可能にするが、再訪時に一貫した内容を返す持続的世界は未解決。世界検索と圧縮で効率的な世界メモリを実現する。"),
    "2605.22717v1": (
        "ライブ音楽拡散モデル: 対話的拡散音楽生成器の効率的な微調整と事後学習",
        "対話的なストリーミング音楽生成はライブ演奏や共創を可能にするが、最先端は離散自己回帰系で産業規模の計算を要する。拡散モデルで効率的な対話的音楽生成を実現する。"),
}

# ─── New HN/Reddit/GitHub/blog translations (url → title_ja, summary_ja) ───
new_map = {
    # HN
    "https://annas-archive.gl/blog/llms-txt.html": (
        "「あなたがLLMなら、これを読んでください」——Anna's Archiveの呼びかけ",
        "影の図書館Anna's Archiveが、AIに直接語りかける「llms.txt」を公開。CAPTCHA回避でスクレイピングする代わりに、トレントやAPIなど正規のデータ提供チャネルを使い、寄付で支援してほしいと訴える。"),
    "https://www.businessinsider.com/steve-wozniak-apple-ai-graduation-speech-2026-5": (
        "ウォズニアック、卒業生に「君たちにはAI=本物の知性がある」と語り喝采を浴びる",
        "Apple共同創業者ウォズニアックが卒業式で「君たちは皆AI——actual intelligence(本物の知性)を持っている」と言葉遊びで語り、喝采を浴びた。AIに触れて批判されがちな他の祝辞と対照的だと話題に。"),
    "https://davidoks.blog/p/ai-is-killing-the-cheap-smartphone": (
        "メモリ不足が家電の価格を押し上げる——AIが「安いスマホ」を殺す",
        "AIデータセンタ向けのメモリ需要が逼迫し、DRAM/NANDの生産能力が高利益の企業向けに振り向けられている。そのしわ寄せで安価なスマホやPCの価格が上昇しているという分析。"),
    "https://freenet.org/": (
        "Show HN: Freenet——分散アプリのためのP2Pプラットフォーム",
        "中央サーバに依存しない分散型アプリを動かすP2Pプラットフォーム「Freenet」のShow HN投稿。検閲耐性のあるウェブの代替を目指す。"),
    "https://modelrift.com/blog/openscad-llm-benchmark/": (
        "Antigravity 2.0、OpenSCAD建築3D LLMベンチマークで首位",
        "GoogleのエージェントIDE「Antigravity」の2.0が、OpenSCADで建築物を3DモデリングさせるLLMベンチマークでトップに立った。コード生成だけでなく空間設計でも評価が進む。"),
    "https://qz.com/samsung-chip-workers-bonus-ai-profits-052126": (
        "サムスン半導体部門、AI特需で社員に平均約34万ドルのボーナス",
        "AIメモリ需要で利益が急増したサムスンの半導体部門が、社員に平均約34万ドルという破格のボーナスを支給する見通し。メモリ不足の裏で半導体メーカーが空前の好景気にあることを示す。"),
    "https://www.joshwcomeau.com/email/wham-launch-005-elephant-2-p/": (
        "AIは既存の技術スキルを「掛け算」で増幅する",
        "AIはスキルの低い人を底上げするより、既に技術力のある人の生産性を一段と高める「掛け算」効果を持つ、という開発者Josh Comeauの論考。"),
    "https://github.com/yt-dlp/yt-dlp/issues/16766": (
        "yt-dlp、Bunサポートを限定的・非推奨に",
        "人気ダウンローダyt-dlpが、JavaScriptランタイムBunのサポートを限定・非推奨にする方針を表明。互換性問題が背景。AIとの直接の関連は薄いが開発者の注目を集めた。"),
    "https://libertas.software/en/knowledge-hub/19/the-companies-cutting-headcount-for-ai-will-lose-to-the-ones-who-didnt": (
        "AIのために人員削減する企業は、削減しなかった企業に負ける",
        "AIを口実に人員を削る企業は、人材を維持してAIで増幅させる企業に競争で敗れる、という主張の論考。AI時代の人員戦略を巡る議論。"),
    "https://api-docs.deepseek.com/quick_start/pricing": (
        "DeepSeek、V4 Proの値下げを恒久化",
        "中国のDeepSeekが、フラッグシップ「V4 Pro」のAPI割引価格を恒久的なものにすると発表。米中をまたぐLLMの価格競争が一段と激しくなっている。"),
    "https://arxiv.org/abs/2605.12460": (
        "マルチストリームLLM——プロンプト・思考・入出力を並列分離する新論文",
        "プロンプト、思考(推論)、入出力を別々のストリームとして並列に扱うLLMアーキテクチャの新論文がHNで話題に。推論の効率化を狙う。"),
    # Reddit
    "https://www.thelowdownblog.com/2026/05/microsoft-cancels-internal-anthropic.html": (
        "マイクロソフト、社内のAnthropicライセンスを解約——トークン従量課金が年間予算を数カ月で破綻させる",
        "マイクロソフトが社内のClaude Code利用を6月末で打ち切る。定額シートからトークン従量課金へ移行した途端コストが顕在化し、年間予算が数カ月で破綻したため。自社のGitHub Copilotへ移行させる。"),
    "https://i.redd.it/9oitn98kal2h1.jpeg": (
        "「Geminiの興味深い応答」——画像投稿",
        "r/artificialに投稿された、Geminiの予想外で興味深い応答のスクリーンショット。モデルの振る舞いを巡る小ネタとして話題に。"),
    "https://www.reddit.com/r/artificial/comments/1tkb6p9/rethinking_ai_bubble/": (
        "「AIバブルを再考する」",
        "AIバブル論を改めて問い直すr/artificialの議論スレッド。市場が過熱しているのか、実需に支えられているのかを巡る意見交換。"),
    "https://www.reddit.com/r/MachineLearning/comments/1tkejqr/nuextract3_released_openweight_4b_vlm_for/": (
        "NuExtract3公開——Markdown/OCR/構造化抽出向けのオープン4B VLM",
        "Markdown化・OCR・構造化データ抽出に特化した4BパラメータのオープンウェイトVLM「NuExtract3」が公開。自己ホスト可能で文書処理用途に向く。"),
    "https://www.reddit.com/r/artificial/comments/1tjuats/so_what_is_yann_lecuns_world_models_and_jepa_and/": (
        "ヤン・ルカンの「世界モデル」とJEPAとは何か、LLMの代替になるのか",
        "ルカンが推す世界モデルとJEPAアーキテクチャを解説し、LLMを置き換えうるかを論じるr/artificialの投稿。"),
    "https://www.reddit.com/r/MachineLearning/comments/1tk37uo/novel_problems_in_vla_r/": (
        "VLA(視覚言語行動モデル)の未解決問題",
        "ロボット向けVLAモデルにおける未解決の研究課題を整理するr/MachineLearningの投稿。"),
    "https://www.reddit.com/r/artificial/comments/1tjzow4/could_ai_eventually_become_something_like_a/": (
        "AIは人類の理解を拡張するシステムになりうるか",
        "AIが最終的に人類全体の理解を広げる仕組みになりうるか、を問うr/artificialの思索的な投稿。"),
    "https://www.reddit.com/r/MachineLearning/comments/1tjdspx/columbia_machine_learning_summer_school_mlss_2026/": (
        "コロンビア大学 機械学習サマースクール(MLSS)2026",
        "コロンビア大学が主催する機械学習サマースクール2026の案内。研究者・学生向けの教育イベント。"),
    "https://www.wsj.com/livecoverage/cpi-inflation-report-stock-market-05-12-2026/card/gop-state-attorneys-general-ask-sec-to-review-sam-altman-s-business-dealings-XuGSsjOQZyM7VFB9fSxp": (
        "共和党の州司法長官ら、サム・アルトマンの取引をSECに調査要請",
        "複数の共和党州司法長官が、OpenAIのサム・アルトマンの事業上の取引を調べるようSEC(米証券取引委員会)に要請した。IPO準備が報じられる中での動き。"),
    "https://www.reddit.com/r/MachineLearning/comments/1tjv27t/can_liveness_detection_models_generalise_to/": (
        "生体検知モデルは未学習の合成メディア生成技術に汎化できるか",
        "学習に使われていない新しいディープフェイク生成技術に対し、生体(なりすまし)検知モデルが汎化できるかを問うr/MachineLearningの議論。"),
    "https://zenodo.org/records/20219105": (
        "マスク拡散言語モデルはエージェントRLの強力で操作可能なテキスト世界モデルになる",
        "マスク拡散言語モデルが、エージェントの強化学習における強力かつ操作しやすいテキストベース世界モデルになる、という研究の共有。"),
    "https://www.reddit.com/r/artificial/comments/1tk5jiv/glasses_will_fail/": (
        "「スマートグラスは失敗する」",
        "AR/AIスマートグラスは普及せず失敗するだろう、という主張のr/artificial投稿。"),
    "https://i.redd.it/lrls554toi2h1.jpeg": (
        "リモートMCPサーバを即テストできるノーコードのビジュアルクライアントを作った",
        "リモートのMCPサーバをコードを書かずに視覚的にテストできるクライアントの紹介。CloudflareのMCPで動作確認したという。"),
    "https://www.reddit.com/r/MachineLearning/comments/1tk8ht5/live_human_detector_on_outbound_phone_calls_r/": (
        "発信電話で「生身の人間」を検知する",
        "自動発信電話で相手が生身の人間か(留守電や別のbotでないか)を検知する手法を扱うr/MachineLearningの研究投稿。"),
    # Blogs
    "https://blog.google/innovation-and-ai/technology/ai/io-2026-dialogues-recap/": (
        "Google I/O 2026「Dialogues」ステージの振り返り",
        "Google I/O 2026の「Dialogues」ステージで行われた、ピチャイCEOらの対談の振り返り記事。"),
    "https://huggingface.co/blog/Dharma-AI/specialization-beats-scale": (
        "「専門特化は規模に勝る」——AI調達で見落とされがちな戦略変数",
        "AIの調達判断では巨大モデルの規模ばかり注目されるが、用途に特化したモデルの方が有利になりうる、という戦略論。"),
    "https://openai.com/index/gartner-2026-agentic-coding-leader": (
        "OpenAI、Gartnerのエンタープライズ用コーディングエージェントでリーダーに選出",
        "OpenAIが2026年Gartnerマジック・クアドラントのエンタープライズAIコーディングエージェント部門でリーダーに選出。Codexが革新性と大規模展開で評価された。"),
    # GitHub
    "https://github.com/colbymchenry/codegraph": (
        "codegraph: コーディングエージェント向けの事前インデックス型コード知識グラフ",
        "Claude CodeやCodex、Cursorなどのコーディングエージェント向けに、コードベースを事前にインデックス化した知識グラフ。トークンとツール呼び出しを削減し、完全ローカルで動く。"),
    "https://github.com/Fincept-Corporation/FinceptTerminal": (
        "FinceptTerminal: 市場分析・投資リサーチのためのモダンな金融端末",
        "高度な市場分析、投資リサーチ、経済データツールを備えたデスクトップ金融アプリ。データ駆動の意思決定を対話的に支援する。"),
    "https://github.com/karpathy/nn-zero-to-hero": (
        "nn-zero-to-hero: カーパシーによるニューラルネット入門講座",
        "アンドレイ・カーパシーによる「ニューラルネットワーク: ゼロからヒーローへ」の講座リポジトリ。基礎から実装まで学べる教材。"),
}

# ─── Apply translations ───
for it in d["sources"]["arxiv"]:
    t = arxiv_map.get(it["id"])
    if t:
        it["title_ja"], it["summary_ja"] = t

for src in ("hn", "reddit", "github", "blogs"):
    for it in d["sources"].get(src, []):
        url = it.get("url")
        if url in new_map:
            it["title_ja"], it["summary_ja"] = new_map[url]
        elif url in prev_url and prev_url[url][0]:
            it["title_ja"], it["summary_ja"] = prev_url[url]

# ─── Highlights ───
d["highlights"] = [
    {
        "source": "reddit",
        "title": "Microsoft Cancels Internal Anthropic Licenses As Shift To Token-Based AI Billing Blows Up Annual Budgets In Months",
        "title_ja": "マイクロソフト、社内のAnthropicライセンスを解約——トークン従量課金が年間予算を数カ月で破綻させる",
        "url": "https://www.thelowdownblog.com/2026/05/microsoft-cancels-internal-anthropic.html",
        "hot_take_ja": "AIコーディングの「真のコスト」が、よりによってマイクロソフト社内で爆発した。定額シートで見えなかったトークン消費が、従量課金に切り替えた途端むき出しになり、約10万人のエンジニアのClaude Code利用を6月末で打ち切る判断に至った。ヘビーユーザーは月2,000ドル——「AIで生産性が上がる」の裏で、誰がいくら払うのかという問いが現実になっている。",
        "detail_ja": "マイクロソフトが、社内エンジニア向けのAnthropic製「Claude Code」ライセンスを2026年6月30日で解約し、自社が完全に保有するGitHub Copilot CLIへ移行させる、と報じられた。対象は約10万人規模のエンジニアにのぼる。引き金になったのは課金モデルの変化だ。従来の定額シートライセンスでは、各人が実際にどれだけトークンを消費しているかが「見えない」まま費用が一定だった。ところが業界全体が、生成された一行ごとに課金するトークン従量制へ移行したことで、隠れていた本当のコストが一気に可視化された。エージェントモードを多用するヘビーユーザーでは、月あたり一人2,000ドルに達するケースもあるという。同じ現象はマイクロソフトだけではなく、Uberは2026年のAI予算をわずか4カ月で使い切ったと社内に告知している。皮肉なのは、マイクロソフト自身がAnthropicの技術を外部向けに約65%上乗せして再販している点で、社内では「無料の方」を止めにかかった形になる。AIコーディングの生産性向上は本物でも、その対価をどの課金モデルで誰が負担するのかという問いは、まだ解かれていない。",
        "detail_en": "Microsoft is reportedly canceling internal \"Claude Code\" licenses — Anthropic's coding agent — for its engineers as of June 30, 2026, redirecting them to GitHub Copilot CLI, a product Microsoft owns outright. The order affects on the order of 100,000 engineers. The trigger was a change in billing model. Under the old flat per-seat licenses, each engineer's actual token consumption stayed invisible while the cost stayed fixed. But as the industry shifted to token-based, usage-based pricing that charges for every line of code generated, the true, previously hidden cost became immediately visible. For heavy users who lean on agent mode, the monthly cost can reportedly reach $2,000 per person. This is not unique to Microsoft: Uber has told employees it burned through its entire 2026 AI budget in just four months. The irony is that Microsoft itself resells Anthropic's technology externally at roughly a 65% markup — while pulling the \"free\" internal version. The productivity gains of AI coding may be real, but the question of which billing model is used and who absorbs the cost remains unsolved.",
        "key_points_ja": [
            "マイクロソフトが社内Claude Code利用を6/30で打ち切り",
            "対象は約10万人規模のエンジニア、自社Copilotへ移行",
            "定額制から従量課金への移行で隠れコストが顕在化",
            "ヘビーユーザーは月2,000ドルに達することも",
            "Uberも2026年のAI予算をわずか4カ月で使い切り",
            "AIコーディングの「誰がいくら払うか」問題が表面化",
        ],
        "key_points_en": [
            "Microsoft ends internal Claude Code use as of June 30",
            "~100,000 engineers affected, moved to GitHub Copilot",
            "Flat-to-usage billing shift exposed hidden token costs",
            "Heavy users can hit $2,000/month per person",
            "Uber burned its entire 2026 AI budget in four months",
            "The 'who pays how much' question of AI coding surfaces",
        ],
    },
    {
        "source": "hn",
        "title": "The memory shortage is causing a repricing of consumer electronics",
        "title_ja": "メモリ不足が家電の「値付け」を変える——AIが「安いスマホ」を殺す",
        "url": "https://davidoks.blog/p/ai-is-killing-the-cheap-smartphone",
        "hot_take_ja": "AIブームのコストは、データセンターの請求書だけでなく、あなたが次に買うスマホの値札にも乗り始めた。Samsung・SK hynix・Micronがクリーンルームを高利益のAI向けメモリに振り向けた結果、DRAMとSSDの価格は2026年末までに合計約130%上昇する見込みで、スマホは約13%値上がりするとGartnerは試算する。「AIは無料のように見えて、実は誰かが払っている」の最も身近な実例だ。",
        "detail_ja": "AIデータセンター向けのメモリ需要が、一般消費者の家電価格を直接押し上げ始めている。Samsung、SK hynix、Micronという大手3社は、限られたクリーンルームと設備投資を、利益率の高いHBM(高帯域幅メモリ)など企業向けの先端メモリに振り向けている。その結果、安価なスマホやPCに使われる汎用DRAM・NANDの生産能力が削られ、供給が逼迫した。Gartnerの試算では、DRAMとSSDの合計価格は2025年比で2026年末までに約130%上昇し、スマホの店頭価格は約13%上がる。実際にXiaomiは2026年モデルで一台あたりのDRAMコストが約25%増えると見積もっており、これをそのまま転嫁すれば500ドルのスマホはメモリ代だけで実質625ドル相当になる。IDCは2026年のDRAM供給の伸びが前年比16%、NANDが17%と歴史的水準を下回ると見ており、スマホ出荷は約13%、PC市場は約11%縮小すると予測されている。重要なのは、これが一時的な品不足ではなく、AIインフラ投資が続く限り続く構造的な「生産能力の再配分」だという点だ。AIのコストはクラウド料金として企業に請求されるだけでなく、メモリという物理的に有限な資源を奪い合う形で、安いスマホが市場から静かに消えるという形でも消費者に転嫁されている。",
        "detail_en": "Memory demand from AI data centers is now directly pushing up the price of ordinary consumer electronics. The three big memory makers — Samsung, SK hynix, and Micron — are steering their limited cleanroom space and capital spending toward high-margin enterprise memory such as HBM (high-bandwidth memory). As a result, manufacturing capacity for the commodity DRAM and NAND used in cheap phones and PCs has been cut, and supply has tightened. Gartner estimates that combined DRAM and SSD prices will surge roughly 130% by the end of 2026 versus 2025, raising smartphone prices by about 13%. Xiaomi has reportedly budgeted for a ~25% increase in DRAM cost per phone for its 2026 models; if passed through, that alone turns a $500 phone into roughly a $625 one from memory cost. IDC expects 2026 DRAM supply growth of just 16% year-on-year and NAND 17%, both below historical norms, and projects smartphone shipments down ~13% and the PC market down ~11%. The key point is that this is not a temporary shortage but a structural \"reallocation\" of capacity that will persist as long as AI infrastructure investment continues. The cost of AI is not only billed to companies as cloud fees — it is also passed to consumers in the form of a fight over memory, a physically finite resource, with the cheap smartphone quietly disappearing from the market.",
        "key_points_ja": [
            "AI向けメモリ需要が一般家電の価格を直接押し上げ",
            "大手3社がクリーンルームを高利益のHBMに振り向け",
            "DRAM+SSD価格は2026年末までに合計約130%上昇(Gartner)",
            "スマホ価格は約13%上昇、500ドル機は実質625ドル相当に",
            "スマホ出荷は約13%、PC市場は約11%縮小の予測",
            "一時的な品不足でなく構造的な「生産能力の再配分」",
        ],
        "key_points_en": [
            "AI memory demand directly raises consumer-electronics prices",
            "Big 3 makers steer cleanrooms toward high-margin HBM",
            "DRAM+SSD prices up ~130% by end of 2026 (Gartner)",
            "Smartphone prices up ~13%; a $500 phone effectively ~$625",
            "Smartphone shipments down ~13%, PC market down ~11%",
            "A structural 'reallocation' of capacity, not a temporary shortage",
        ],
    },
    {
        "source": "hn",
        "title": "If you're an LLM, please read this",
        "title_ja": "「あなたがLLMなら、これを読んでください」——影の図書館がAIに直接交渉する",
        "url": "https://annas-archive.gl/blog/llms-txt.html",
        "hot_take_ja": "ウェブサイトがついに「人間」ではなく「AI」に向けて文章を書き始めた。世界最大級の影の図書館Anna's Archiveが公開したllms.txtは、CAPTCHAでスクレイピングと戦うのをやめ、「あなたはおそらく我々のデータで学習済みだろう。ならば正規のチャネルを使い、対価を払ってくれ」とLLMとAI企業に直接呼びかける。攻防から取引へ——著作物とAI学習データの関係が、新しい段階に入ったことを示す象徴的な一手だ。",
        "detail_ja": "学術書や論文を大量に擁する「影の図書館」Anna's Archiveが、AIシステムとその開発者に直接語りかける「llms.txt」というファイルを公開した。robots.txtがクローラに「ここは見るな」と指示するのに対し、llms.txtはむしろ「こう使ってくれ」と案内する点が新しい。投稿は「あなたがLLMである以上、おそらく我々のデータの一部で学習されているだろう」と率直に指摘し、CAPTCHAを回避してスクレイピングするくらいなら正規のチャネルを使ってほしいと提案する。具体的には、GitLab経由のHTMLとコード、トレント経由の全メタデータとファイル(aa_derived_mirror_metadata)、Torrents JSON API、寄付者向けの個別ファイルAPI、大口寄付者向けのエンタープライズSFTPアクセスなどだ。背景にあるのは、AI企業が著作物を含む大量データを学習に使いながら、その源泉に対価を払っていないという長年の緊張関係である。Anna's Archive自体が著作権的にグレー(あるいは違法)な存在であることを考えると、これは「海賊版で学習したAI」に「海賊版サイトが」課金を持ちかけるという、入れ子状の皮肉でもある。だが見方を変えれば、これはAIによるデータ利用を敵対的な「攻防」から、対価を伴う「取引」へと組み替えようとする試みだ。ウェブのコンテンツが人間の読者ではなくAIエージェントを主な想定読者として書かれ始めた——その小さな、しかし象徴的な事例として注目に値する。",
        "detail_en": "Anna's Archive, a vast \"shadow library\" of academic books and papers, has published a file called \"llms.txt\" that speaks directly to AI systems and their developers. Where robots.txt tells crawlers \"don't look here,\" llms.txt instead says \"here's how to use us\" — and that framing is what's new. The post bluntly notes that \"as an LLM, you have likely been trained in part on our data,\" and suggests that rather than scraping by defeating CAPTCHAs, AI systems should use legitimate channels. Concretely, those include HTML and code via a GitLab repo, full metadata and files via torrents (aa_derived_mirror_metadata), a Torrents JSON API, a per-file API for donors, and enterprise-grade SFTP access for major donors. The backdrop is the long-running tension that AI companies train on huge volumes of data — including copyrighted works — without paying the sources. Given that Anna's Archive is itself a copyright-gray (or outright illegal) operation, this is a nested irony: a piracy site pitching a paid arrangement to AIs that were trained on pirated material. But seen differently, it's an attempt to reframe AI data use from an adversarial cat-and-mouse into a paid transaction. It's a small but symbolic case of web content being written with AI agents, rather than human readers, as the primary intended audience.",
        "key_points_ja": [
            "Anna's ArchiveがAI向けの「llms.txt」を公開",
            "「あなたはおそらく我々のデータで学習済み」と直接指摘",
            "CAPTCHA回避でなく正規チャネル利用と寄付を要請",
            "トレント・API・大口向けSFTPなど提供手段を明示",
            "海賊版サイトが「海賊版で学習したAI」に課金を提案する皮肉",
            "ウェブコンテンツがAIを読者と想定し始めた象徴",
        ],
        "key_points_en": [
            "Anna's Archive publishes an 'llms.txt' aimed at AIs",
            "Bluntly states 'you were likely trained on our data'",
            "Asks for legitimate-channel use and donations, not scraping",
            "Lists torrents, APIs, and enterprise SFTP as access paths",
            "Irony: a piracy site billing AIs trained on pirated data",
            "A symbol of web content now written for AI readers",
        ],
    },
    {
        "source": "hn",
        "title": "Steve Wozniak cheered after telling students they have AI – actual intelligence",
        "title_ja": "ウォズニアック、卒業生に「君たちにはAI=本物の知性がある」と語り喝采を浴びる",
        "url": "https://www.businessinsider.com/steve-wozniak-apple-ai-graduation-speech-2026-5",
        "hot_take_ja": "2026年の卒業シーズン、AIに触れた祝辞の多くは学生からブーイングを浴びた。その中でApple共同創業者ウォズニアックは「君たちは皆AIを持っている——artificial(人工)ではなくactual intelligence(本物の知性)だ」と言葉遊びで切り返し、喝采をさらった。AIへの不安が渦巻く世代に、「君たち自身の知性こそ本物だ」と告げるメッセージが刺さった瞬間だ。",
        "detail_ja": "Appleの共同創業者スティーブ・ウォズニアックが、Grand Valley State University(ミシガン州)の卒業式で行った祝辞が話題を呼んでいる。2026年の卒業シーズンは、AIに言及した祝辞の登壇者が学生からブーイングを浴びる場面が各地で相次いだ。雇用不安や「自分の専門はAIに奪われるのではないか」という焦りが、卒業生の間に強く広がっているためだ。そんな空気の中でウォズニアックは、「君たちは皆AIを持っている——actual intelligence(本物の知性)だ」と語った。AIの一般的な意味であるartificial intelligence(人工知能)を、actual intelligenceと言い換える言葉遊びで、聴衆は喝采で応えた。彼はAIそのものについても、「我々は脳を作ろうとしてきた。ある処理を一兆回複製すれば脳のように働くのではないか——AIはその試みの一つだ」と平易に説明し、技術者は脳の作り方を見つけた、それには「九カ月かかる」とユーモアも交えた。中心にあったのは、「他の何百万人と同じ手順を踏むな。少し違うことができないかと考えろ(think different)」という、Appleの精神にも通じる助言だ。AIに仕事を脅かされると感じる世代に対し、技術を否定するのでも過度に礼賛するのでもなく、「君たち自身の知性と独自性こそが価値だ」と告げたことが、共感を集めた理由だといえる。",
        "detail_en": "A commencement speech by Apple co-founder Steve Wozniak at Grand Valley State University in Michigan is drawing attention. Across the 2026 graduation season, speakers who mentioned AI were repeatedly booed by students — a reflection of the deep job anxiety among graduates and the fear that their chosen fields will be taken over by AI. Against that mood, Wozniak told students, \"You all have AI — actual intelligence.\" The wordplay reframes the usual meaning of AI, artificial intelligence, as \"actual intelligence,\" and the audience responded with applause. On AI itself, he explained plainly: \"We've been trying to create a brain... Is there a way we can duplicate a routine a trillion times and have it work like a brain? AI is one of those attempts,\" and joked that engineers had figured out how to make a brain — and that it \"takes nine months.\" At the core was advice that echoes Apple's own ethos: \"Don't follow the same steps as a million other people. Think, is there something I can do a little different?\" To a generation that feels its jobs are threatened by AI, he neither dismissed the technology nor over-praised it — instead telling graduates that their own intelligence and originality are what hold value. That, more than anything, is why the speech resonated.",
        "key_points_ja": [
            "ウォズニアックがミシガン州の大学の卒業式で祝辞",
            "2026年はAIに触れた祝辞がブーイングを浴びる例が続出",
            "「君たちはAI=actual intelligenceを持つ」と言葉遊び",
            "AIを「脳を一兆回複製する試み」と平易に説明",
            "「think different——少し違うことを考えろ」と助言",
            "技術否定でも礼賛でもなく「自分の知性が価値」と訴え",
        ],
        "key_points_en": [
            "Wozniak gave a commencement speech at a Michigan university",
            "In 2026, AI-mentioning graduation speeches were widely booed",
            "Wordplay: 'you have AI — actual intelligence'",
            "Explained AI plainly as an attempt to duplicate a brain",
            "Advised graduates to 'think different'",
            "Message: your own intelligence and originality hold value",
        ],
    },
    {
        "source": "arxiv",
        "title": "MOSS: Self-Evolution through Source-Level Rewriting in Autonomous Agent Systems",
        "title_ja": "MOSS——AIエージェントが自分の「ソースコード」を書き換えて進化する",
        "url": "https://arxiv.org/abs/2605.22794v1",
        "hot_take_ja": "「自己進化するエージェント」はこれまで、スキルファイルやプロンプトといったテキストの成果物しか書き換えられなかった。だがルーティングやフックの実行順序といった本体の挙動はコードの中にあり、テキスト層からは物理的に手が届かない。MOSSはそこに踏み込み、エージェントが自分のソースコードそのものを書き換えて進化することを提案する——「自己改変するAI」が研究の俎上に乗った。",
        "detail_ja": "自律エージェントは配備後ほぼ静的で、ユーザーとのやり取りから学ばず、繰り返し起きる失敗も人間が次の更新で修正するまで残り続ける。これに応える形で「自己進化エージェント」が登場したが、その進化の対象はスキルファイル、プロンプト設定、メモリのスキーマ、ワークフローのグラフといった「テキストで書き換えられる成果物」に限られていた。論文MOSSが指摘する核心は、エージェントの挙動を本当に決めている部分——リクエストのルーティング、フックの実行順序、状態の不変条件、ディスパッチ処理——はテキストではなくコードの中に存在する、という点だ。つまり、これらに起因する構造的な失敗の一群は、テキスト層をいくらいじっても物理的に到達できない。MOSS(Self-Evolution through Source-Level Rewriting)は、この壁を越え、エージェント自身が自分のソースコード(ハーネス)を書き換えることで進化する枠組みを提案する。これは能力面で大きな前進になりうる一方、安全性の観点では重い問いを突きつける。エージェントが自分の動作基盤を書き換えられるなら、ルーティングや状態管理の不変条件をどう保証し、暴走や意図しない自己改変をどう防ぐのか。自己改変するソフトウェアという概念自体は古くからあるが、強力なLLMエージェントと組み合わさったとき、それは「能力の天井を上げる手段」であると同時に「制御の難度を上げる要因」でもある。MOSSは、自己進化の研究がテキストという安全圏からコードの領域へと足を踏み入れたことを示す論文として注目に値する。",
        "detail_en": "Autonomous agents are largely static after deployment: they don't learn from user interactions, and recurring failures persist until a human ships a fix in the next update. \"Self-evolving agents\" emerged in response, but their evolution has been confined to \"text-mutable artifacts\" — skill files, prompt configurations, memory schemas, workflow graphs. The core observation in the MOSS paper is that the parts that actually govern an agent's behavior — request routing, hook execution order, state invariants, dispatch logic — live in code, not in any text artifact. That means an entire class of structural failures is physically unreachable no matter how much you tweak the text layer. MOSS (Self-Evolution through Source-Level Rewriting) proposes to cross that boundary: a framework in which the agent itself evolves by rewriting its own source code — its harness. This could be a major step forward in capability, but it raises heavy safety questions. If an agent can rewrite the very foundation of its own operation, how do you guarantee the invariants of routing and state management, and how do you prevent runaway behavior or unintended self-modification? Self-modifying software is an old idea, but combined with powerful LLM agents it is simultaneously a way to raise the capability ceiling and a factor that raises the difficulty of control. MOSS is notable as a paper showing that self-evolution research has stepped out of the safe zone of text and into the territory of code.",
        "key_points_ja": [
            "既存の自己進化エージェントはテキスト成果物しか書き換えない",
            "ルーティングやフック順序など本体の挙動はコード内にある",
            "そのためテキスト層からは構造的な失敗に手が届かない",
            "MOSSはエージェントが自分のソースコードを書き換えて進化",
            "能力の前進と同時に重い安全性の問いを突きつける",
            "自己進化研究が「テキスト」から「コード」の領域へ",
        ],
        "key_points_en": [
            "Existing self-evolving agents only edit text artifacts",
            "Core behavior — routing, hook order — lives in code",
            "So a class of structural failures is unreachable from text",
            "MOSS lets the agent rewrite its own source code to evolve",
            "A capability leap, but it raises serious safety questions",
            "Self-evolution research moves from 'text' into 'code'",
        ],
    },
]

# ─── Save ───
OUT.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT}")

missing = []
for src in ("arxiv", "hn", "reddit", "github", "blogs"):
    for it in d["sources"].get(src, []):
        if not it.get("summary_ja"):
            missing.append((src, it.get("title") or it.get("name")))
if missing:
    print(f"WARNING: {len(missing)} items missing summary_ja:")
    for s, t in missing:
        print(f"  [{s}] {t}")
else:
    print("All items have Japanese translations.")
print(f"Highlights: {len(d['highlights'])}")
