#!/usr/bin/env python3
"""Enrichment for 2026-05-21 (fresh page).

arXiv set is fully new (50 items, all translated below).
HN/Reddit/GitHub/blogs reuse prior Japanese translations for overlapping
URLs (from data/2026-05-20.json) and translate new items inline.
Five fresh highlights are selected for the day.
"""
import json
from pathlib import Path

DATE = "2026-05-21"
PREV = "2026-05-20"
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
    "2605.21489v1": (
        "拡散教師モデルを用いる期待値計算の分散削減",
        "text-to-3Dや蒸留などの下流パイプラインは凍結した拡散モデルを教師に使い、ノイズにわたるモンテカルロ期待値で勾配を得る。各標本がレンダリング等の高コストな上流計算を要するため推定分散が計算コストを支配する問題に、分散削減で取り組む。"),
    "2605.21488v1": (
        "均衡推論器: アトラクタの学習がスケーラブルな推論を可能にする",
        "潜在状態を反復更新するテスト時計算は推論の強力な枠組みだが汎化の機構は不明。汎化的推論はタスク条件付きアトラクタ(安定固定点が正解に対応する潜在力学系)の学習から生じるとの仮説を立て、検証器なしでテスト時スケーリングを実現。Sudoku-Extremeで精度2.6%→99%超。"),
    "2605.21487v1": (
        "Uni-Edit: 知的な編集は統合モデル調整の汎用タスクである",
        "統合マルチモーダルモデルの理解・生成・編集の強化は混合マルチタスク学習に頼り、タスク間競合で多段パイプラインを要し性能はトレードオフに留まる。編集を汎用タスクと捉え、真の相互強化を狙う新パラダイムを提案する。"),
    "2605.21486v1": (
        "ハイパーパラメータ転移の定量化と埋め込み層学習率の重要性",
        "ハイパーパラメータ転移は小規模から大規模へ最適設定を外挿でき、LLM学習に不可欠。muPなどのパラメータ化で実現するが、本研究は転移を定量化し、埋め込み層の学習率が見過ごせない要素であることを示す。"),
    "2605.21485v1": (
        "EvoStruct: タンパク質言語モデル適応による抗体CDR設計の進化的・構造的事前知識の橋渡し",
        "同変GNNによる抗体CDR設計は配列回復率が最高だが語彙崩壊が深刻で、チロシンやグリシンなど少数のアミノ酸を過剰予測する。原因をGNNエンコーダの学習傾向に突き止め、進化的事前知識と構造を橋渡しして改善する。"),
    "2605.21484v1": (
        "不動点反復による離散拡散画像生成器の1ステップ蒸留",
        "離散拡散モデルは画像合成に優れるが遅い反復復号に依存。補助スコアネットで計算が倍増したり多段化で最適化が分断される既存蒸留に対し、不動点蒸留(FPD)で1ステップ生成を実現する。"),
    "2605.21483v1": (
        "Velocityformer: 宇宙論的速度再構成のための対称性破れ整合の同変グラフトランスフォーマー",
        "運動学的スニヤエフ-ゼルドビッチ効果の精密測定には分光サーベイから銀河速度を正確に再構成する必要がある。対称性の破れに整合した同変グラフトランスフォーマーで、再構成速度と真の速度の相関を高める。"),
    "2605.21482v1": (
        "DeepWeb-Bench: 大量の情報源横断証拠と長期導出を要するディープリサーチのベンチマーク",
        "フロンティアのディープリサーチ製品は既存ベンチで高得点で能力差が見えにくい。大量の証拠収集・情報源横断の照合・長期多段導出を要する難ベンチを提案。9モデル評価で「検索は律速でなく、導出と較正の失敗が誤りの7割超」と判明。"),
    "2605.21481v1": (
        "AiraXiv: 人間とAI科学者のためのAI駆動オープンアクセス基盤",
        "AI生成・人間執筆の研究成果が急増し、従来の会議・ジャーナル中心の出版が査読負荷と規模で限界に。人間とAIが著者・読者として参加し論文がフィードバックで継続進化するAI時代の出版基盤AiraXivを提案。ICAIS 2025の投稿基盤として実運用した。"),
    "2605.21479v1": (
        "WikiVQABench: WikipediaとWikidataに基づく知識接地型視覚QAベンチマーク",
        "既存のVQAベンチは画像だけで解ける知覚タスクが中心だが、現実は画像に映らない外部知識を要する。WikipediaとWikidataを体系的に組み合わせた人手作成の知識接地型VQAベンチマークを提案する。"),
    "2605.21478v1": (
        "全身アバターアニメーションのための潜在ダイナミクス",
        "ポーズ駆動の全身アバターは高品質な新視点を生むが、ゆったりした衣服など動的要素はポーズだけでは説明できない(履歴・慣性・接触に依存)。明示的シミュレーションに頼らず潜在ダイナミクスで動的変形を扱う。"),
    "2605.21475v1": (
        "スキーマグラフは固定すべきか: リレーショナル深層学習のための全解像度グラフ構造学習",
        "リレーショナルDBをグラフ化しGNNで学習するリレーショナル深層学習では、グラフ構築時に全解像度性を設計原則とするのが通例。その前提を問い直し、グラフ構造そのものを学習する手法を検討する。"),
    "2605.21472v1": (
        "Stream3D: 証拠的記憶による逐次的マルチビュー3D生成",
        "SAM 3DやTRELLISなど視点条件付き3D生成器は単一視点から高品質再構成を行うが、現実の観測は長い単眼ストリームで来る。各フレームに独立適用すると時間的不整合が深刻。証拠的記憶を持つ初のストリーミング3D生成を提案する。"),
    "2605.21470v1": (
        "レイテンシ最適化のためのエージェントJITコンパイル",
        "コンピュータ操作エージェントは「取得→スクショ→実行」の逐次ループで各反復にLLM呼び出しを要し、高レイテンシと誤操作を招く。Web操作の計画とスケジューリングをJITコンパイルして高速化する。"),
    "2605.21468v1": (
        "RLVR学習は最小限でよい: ランク1軌跡によるLLMの外挿",
        "検証可能報酬による強化学習(RLVR)の重み軌跡は極めて低ランクで予測可能だと示す。下流性能の大半がランク1の方向で説明でき、最小限のRLVR学習から性能を外挿できる。"),
    "2605.21467v1": (
        "DelTA: RLVRのための識別的トークン信用割当",
        "応答レベルの報酬がトークンレベルの確率変化にどう変換されるかは未解明。RLVR更新を識別器の視点で捉え、ポリシー勾配の更新方向が暗黙に識別器として働くことを示し、トークン単位の信用割当を改善する。"),
    "2605.21466v1": (
        "StreamGVE: 数ステップのストリーミング動画生成による学習不要の動画編集",
        "既存の動画編集は高コストな反復を要し品質も不十分。原因をデータ対データのパラダイムに帰し、ノイズ対データの生成枠組みで動画編集を再考。数ステップのストリーミング生成で学習不要の編集を実現する。"),
    "2605.21465v1": (
        "文法適応へのLLM活用: メタモデルと文法の共進化の研究",
        "モデル駆動工学ではメタモデルの進化に合わせ文法を手作業で適応させる必要がある。LLMで文法適応を自動化し、ルールベース手法が苦手な複雑な文法シナリオに対応する。"),
    "2605.21463v1": (
        "Mem-π: いつ何を生成するかを学ぶ適応的記憶",
        "既存の記憶拡張エージェントは類似度検索でエピソード記憶から静的な項目を返し、現在の文脈とずれがち。Mem-πは外部記憶からの検索でなく、必要時に有用な指針をオンデマンド生成する。"),
    "2605.21461v1": (
        "活性化関数に基づく重み付き最小二乗GNSS測位の機械学習枠組み",
        "都市部の谷間では高層ビルがGNSS信号の遮蔽や非見通し受信、マルチパスを起こし誤差を生む。活性化関数を用いた機械学習で重み付き最小二乗測位を改善する枠組みを提案する。"),
    "2605.21460v1": (
        "HITL-D: 人間参加型の拡散支援共有制御",
        "自律操作は高い能力を持つが、拡散ベース方策と人間の専門性を融合する共有制御は未開拓。多段の挿入・精密操作タスクで人間の操作性能を高める人間参加型拡散の共有制御枠組みを提案する。"),
    "2605.21458v1": (
        "シミュレーションと現実のギャップに注意し、科学者のように考えよ",
        "安価だが交絡やドリフトを抱える事前学習シミュレータと、不偏だが高コストな現実実験。計画者がいつどうシミュレータを実験で補うべきかを研究し、3つの理論的結果を与える。"),
    "2605.21455v1": (
        "解釈可能なルーブリック埋め込みによるラベルバイアスの緩和",
        "採用や入試など真のラベルが得難い領域では過去の人間評価で学習するが、過去評価が特定集団を不当に優遇していればバイアスを継承する。解釈可能なルーブリック埋め込みでラベルバイアスを緩和する。"),
    "2605.21454v1": (
        "ProtoPathway: 生物学的構造を持つプロトタイプ-経路融合によるマルチモーダル癌生存予測",
        "全スライド画像とトランスクリプトミクスを統合する、設計段階から解釈可能な癌生存予測枠組み。組織病理側は学習可能な形態プロトタイプ、遺伝子側は生物学的経路に基づく表現を用いる。"),
    "2605.21453v1": (
        "AI生成のPythonリファクタリングPRにおける品質とセキュリティの兆候",
        "AIエージェントのリファクタリング寄与の品質・リスク特性の実証は乏しい。実プロジェクトのPython PRを分析し、品質属性を平均22.5%改善する一方、24.17%のファイルが新たなLint問題を、4.7%が新たなセキュリティ指摘を生むと示す。マージ率は73.5%。"),
    "2605.21451v1": (
        "ニューラルネットの近似理論: 古典と新展開",
        "万能近似定理はニューラルネットの表現力を数学的に説明し、緩い条件下で連続関数やL^p空間、ソボレフ空間で稠密だと主張する。過去40年の定性的結果と最近の進展を概観する。"),
    "2605.21446v1": (
        "霧に迷う: センサ擾乱が運転VLAの推論の脆さを露呈する",
        "解釈可能な自動運転は説明の生成だけでなく、現実のセンサ劣化下でも説明が信頼できることを要する。Vision-Language-Actionモデルを8種のセンサ擾乱・1,996シナリオで検証し、推論の脆弱性を明らかにする。"),
    "2605.21443v1": (
        "TempGlitch: ゲームプレイ動画の時間的グリッチ検出でVLMを評価",
        "VLMはゲームのQA、特にグリッチ検出に使われ始めたが、多くの評価はグリッチを単一フレームの静的異常として扱う。空間的と時間的なグリッチの区別を見落としていると指摘し、時間的グリッチ検出でVLMを評価する。"),
    "2605.21442v1": (
        "torchtune: PyTorchネイティブの事後学習ライブラリ",
        "現代のLLMは強い下流性能のため多段学習を要し、事後学習がオープンウェイトモデル適応の主要インターフェース。効率的なファインチューニング・実験・展開を支援するPyTorchネイティブの事後学習ライブラリを公開する。"),
    "2605.21440v1": (
        "ReMATF: 動的シーンのための再帰的・運動適応的マルチスケール乱流補正",
        "大気乱流は幾何的歪み・ぼけ・時間的ちらつきで動画品質を劣化させる。SOTA手法は多フレーム入力と大きな計算コストを要しリアルタイム展開が難しい。再帰的で運動に適応するマルチスケール乱流補正を提案する。"),
    "2605.21439v1": (
        "入力制約付き不確かな非線形系のための完全駆動多様体制約に基づく出力フィードバック制御",
        "未知の入力制約を持つ未知時変非線形系に対する、低複雑度・モデル不要・出力フィードバック制御器を提案。アクチュエータ非飽和時は所定精度を達成し、飽和後は柔軟な精度を保つ。"),
    "2605.21437v1": (
        "週次地震活動予測のためのニューラル負の二項回帰: セル別分散推定と裾リスク評価",
        "週次地震数予測はポアソン分布と単一の大域分散仮定に頼るが、中央アジアのデータでこの仮定は系統的に破れる(p<10^-179)。セル別に分散を推定するニューラル負の二項回帰で裾リスクを評価する。"),
    "2605.21435v1": (
        "ガウシアン層(シーフ)ニューラルネットワーク",
        "GNNのメッセージパッシングはベクトル値ノード特徴に適するが、ノード特徴が確率分布で表される方が良い場合がある。特徴が平均と共分散を持つガウス分布のとき、それを素朴に扱う問題を層(シーフ)理論で扱う。"),
    "2605.21431v1": (
        "iTryOn: 空間-意味誘導によるインタラクティブ動画バーチャル試着",
        "動画バーチャル試着は時間的一貫性で進展したが、モデルが衣服を見せるだけの非インタラクティブ場面に限られがち。能動的な人-衣服インタラクションという現実の重要側面を、空間-意味誘導で扱う。"),
    "2605.21429v1": (
        "roto 2.0: ロボット触覚オリンピアード",
        "触覚ベースの強化学習は研究が断片化し、飽和した姿勢タスクに偏る。4種のロボット形態(16〜24自由度)にわたり触覚ベースRLを標準化する、GPU並列のベンチマークroto 2.0を提案する。"),
    "2605.21428v1": (
        "ガウス周辺分布下での多クラス線形分類の多項式時間ロバスト学習",
        "ガウス分布下での多クラス線形分類器の不可知学習を研究。二値(k=2)にはアルゴリズム理論が整備されているが多クラスは未開拓。多項式時間でロバストに学習する手法を与える。"),
    "2605.21427v1": (
        "PALS: MoEモデルのための電力考慮型LLMサービング",
        "LLM推論はデータセンターの主要負荷でGPU電力を大量消費する。既存システムはGPU電力を静的制約として扱うが、制御可能な資源とみなす電力考慮型のMoEサービング実行系を提案する。"),
    "2605.21426v1": (
        "適応的信号蘇生: 疎な視覚ネットワークのためのチャネル単位の枝刈り後修復",
        "ワンショットの大きさベース枝刈りは高疎度域で精度崩壊を招く。原因を修復の粒度のミスマッチに帰し、層単位でなくチャネル単位で枝刈り後の修復を行い精度を回復する。"),
    "2605.21422v1": (
        "選好を意識した影響関数ベースの効率的ファインチューニング向けデータ選択",
        "LLM拡大に伴い学習効率はデータの有効活用に依存。既存のデータ選択は目標例を等価値に扱うが非効率。目標例の重要度差を考慮する影響関数ベースのデータ選択手法を提案する。"),
    "2605.21421v1": (
        "AIGaitor: エッジ計算によるプライバシー保護・クラウド不要の運動解析",
        "モーションキャプチャは運動計測の標準だが、コスト・技術的複雑さ・プライバシー懸念で臨床利用が限られる。マーカーレス単眼解析をスマホ上のオンデバイス処理で完結させ、クラウド不要でプライバシーを守る。"),
    "2605.21420v1": (
        "HiRes: 反応条件推薦のための検証可能な先例記憶",
        "反応条件推薦は逆合成の切断選択直後に位置し、化学者は正確な予測とそれを裏付ける先例の両方を求める。学習した反応空間を分類器特徴かつ検証可能な先例記憶として使う検索拡張型システムを提案する。"),
    "2605.21418v1": (
        "FedCritic: 6GマルチセルOFDMAのためのサーバレス連合クリティック学習による資源割当",
        "6G超高密度ネットワークでは積極的な周波数再利用がセル間干渉を増幅し、スケジューリングと電力制御が隣接セル間で強く結合する。サーバレスの連合クリティック学習で分散的に下りリンク資源を管理する。"),
    "2605.21417v1": (
        "順序が重要: 混合感情認識のためのランク考慮型選択的融合",
        "混合感情の認識は、感情が単一の支配信号でなく微妙で重なり合うマルチモーダル手掛かりの混合として表れるため難しい。多様な動画・音声エンコーダの相補的表現をランクを考慮して選択的に融合する。"),
    "2605.21414v1": (
        "PointACT: マルチスケールな点-行動相互作用を持つVision-Language-Actionモデル",
        "VLAモデルは大規模事前学習バックボーンで汎用ロボット操作に有望だが、多くは2D視覚表現に頼り、精密操作に不可欠な細かい幾何や空間接地の推論が苦手。マルチスケールの点-行動相互作用で3D操作を強化する。"),
    "2605.21413v1": (
        "ベンチマーク構築を通じてAIを教える: 責任ある知識労働の演習としてのQuestBench",
        "AI教育の多くはAIを生産性ツールとして使う訓練に偏る。学生がAIを検証し機械が作った知識を判断する自らの役割を学ぶ場が必要だとし、ベンチマーク構築を演習とする授業実践QuestBenchを提案する。"),
    "2605.21411v1": (
        "RoadTones: 道路イベント動画からのトーン制御可能なテキスト生成",
        "既存の動画言語モデルは道路イベントの事実記述は生成できるが、トーン・緊急度・スタイルを制御できない。伝達が重要な場面向けに、トーンを制御できるテキスト生成のデータセット・モデル・評価を提案する。"),
    "2605.21406v1": (
        "MC-Risk: リスク識別と動作計画のための多成分リスク場",
        "鳥瞰図グリッド上で早期・較正済み・クラス別のリスク局在を与える、計画整合の多成分リスク場。動力付きエージェント場など3つの解釈可能なモジュールを線形合成する。"),
    "2605.21405v1": (
        "標準ライブラリか外部か: LLM支援によるゼロ依存Pythonライブラリの性能と正しさ",
        "外部Pythonライブラリは依存管理の負荷やサプライチェーンリスクを生む。標準ライブラリだけでこのエコシステムをどこまで再現できるか、正しさと性能の代償はいくらかを、単一ファイルモジュール集zerodepで実証的に検証する。"),
    "2605.21404v1": (
        "LLMエージェントのベンチマーク論文12本は自らについて何を開示しているか: 試行的監査と公開採点スキーマ",
        "著名なLLMエージェントベンチマーク論文12本を読み、評価の実施方法を次元ごとに記録。同じベンチ・同じモデル名でも結果が食い違いその理由が分からない不満を動機に、開示状況を監査し公開採点スキーマを提案する。"),
    "2605.21403v1": (
        "一致の引き寄せに対する語形融合の通言語的影響の定量化",
        "動詞が文法主辞でなく介在名詞に誤って一致する「一致の引き寄せ」誤りは、一部言語(英・独・露)では語形融合で増幅されるが他言語(トルコ語・アルメニア語)では増幅されない。LLMのサプライザルと注意エントロピーを処理の代理指標としてこの通言語的パターンを調べる。"),
}

# ─── HN translations (url → title_ja, summary_ja) for new items ───
hn_new = {
    "https://axelk.ee/ai-is-just-unauthorised-plagiarism-at-a-bigger-scale/": (
        "AIは規模を拡大した無断盗用にすぎない",
        "AIは原作者の同意なく全入力を取り込み、出所に報いず利益を得るという批判エッセイ。自作のECチュートリアルをChatGPT生成のコピーが検索上位で上回った実体験を交え、派生コンテンツを優遇するGoogleの順位付けも批判する。"),
    "https://qwen.ai/blog?id=qwen3.7": (
        "Qwen3.7-Max: エージェントのフロンティア",
        "AlibabaのQwenチームによる新フラッグシップ「Qwen3.7-Max」の発表。「The Agent Frontier」を掲げ、単発の応答でなくツール利用や多段の自律タスク遂行能力を前面に押し出した最上位モデル。"),
    "https://github.com/kageroumado/phosphene": (
        "Show HN: Appleの動画壁紙をリバースエンジニアリングした",
        "macOSなどの動画壁紙の仕組みを解析したプロジェクト「phosphene」。AI色は薄いがHN上位に上がった技術ネタ。"),
    "https://noslopgrenade.com/": (
        "AI生成の長文の塊を会話に投げ込むのはやめよう",
        "AIが吐いた長大なテキストをそのまま会話やレビューに貼り付ける行為への抗議サイト。生成AIによる「中身の薄い大量出力(スロップ)」が会話を埋める現象への苛立ちを示す。"),
    "https://www.thehandbasket.co/p/hating-ai-is-good-actually": (
        "AIを避けることこそ人間的な選択だ",
        "「AIを嫌うのはむしろ正しい」と論じるオピニオン記事。AIの利用を拒むことを人間性の表明として擁護し、HN上位で賛否を呼んだ。"),
    "https://techcrunch.com/2026/05/20/intuit-to-lay-off-over-3000-employees-to-refocus-on-ai/": (
        "Intuit、AIへの注力のため3,000人超を解雇",
        "TurboTaxやQuickBooksを擁する財務ソフト大手Intuitが、全世界人員の約17%にあたる3,000人超の解雇を発表。組織の簡素化とAI製品開発への資源集中が理由で、四半期売上17%増という好決算下での削減。"),
    "https://valhovey.github.io/gaia-mary/": (
        "プロジェクト・ヘイル・メアリー——恒星航法チャート",
        "SF小説『プロジェクト・ヘイル・メアリー』の恒星航法を可視化したインタラクティブなチャート。AIとは無関係だがHN上位に上がった話題。"),
    "https://www.osnews.com/story/145029/get-your-passwords-out-of-bitwarden-while-you-still-can/": (
        "今のうちにBitwardenからパスワードを移しておけ",
        "パスワード管理ツールBitwardenの方針変更を懸念し、パスワードを別ツールに移すよう促す記事。AI色は薄いがHN上位に上がったセキュリティ話題。"),
    "https://news.ycombinator.com/item?id=48221896": (
        "Show HN: オフラインのパスワード解読の習得に4年を捧げた",
        "オフラインでのパスワードクラッキング技術の習得に4年を費やした経験を共有するShow HN投稿。"),
    "https://www.wsj.com/tech/ai/openai-is-preparing-to-file-for-an-ipo-very-soon-0ec95af5": (
        "OpenAI、近く新規株式公開(IPO)を申請する準備",
        "OpenAIが近くIPOを申請する準備を進めているとWSJが報道。営利再編を経たAI大手の上場は、業界の資金調達と評価額をめぐる大きな節目となる。"),
    "https://github.com/helvesec/rmux": (
        "Show HN: Rmux——Playwright風SDKを持つプログラム可能なターミナルマルチプレクサ",
        "tmuxのようなターミナル多重化を、Playwright風のSDKでプログラム制御できるツール。エージェントによるターミナル自動操作と相性がよい。"),
    "https://www.barebones.com/products/bbedit/bbedit16.html": (
        "BBEdit 16",
        "老舗のmacOS用テキストエディタBBEditのメジャーアップデート。AIとは無関係だがHN上位に上がった話題。"),
    "https://www.niemanlab.org/2026/05/more-than-340-local-news-outlets-are-limiting-the-internet-archives-access-to-their-journalism/": (
        "340超の地域ニュースがInternet Archiveのアクセスを制限",
        "340を超える米地域ニュース媒体が、自社報道へのInternet Archiveのアクセスを制限していると報じる記事。報道コンテンツのアーカイブ・収集をめぐる緊張の一端。"),
    "https://www.wsj.com/opinion/how-i-choose-which-cloudflare-employees-to-replace-with-ai-40a197e5": (
        "Cloudflare CEOが語る、どの従業員をAIで置き換えるかの選び方",
        "Cloudflareのマシュー・プリンスCEOが、どの従業員の業務をAIに置き換えるかをどう判断するかを論じたWSJ寄稿。AIによる人員置換を経営者が公然と語る象徴的な一文。"),
}

# ─── Reddit translations (url → title_ja, summary_ja) for new items ───
reddit_new = {
    "https://openai.com/index/model-disproves-discrete-geometry-conjecture/": (
        "OpenAIのモデルが離散幾何学の中心的予想を反証",
        "OpenAIの汎用モデルがエルデシュの「単位距離問題」をめぐる予想を反証したという発表が、r/artificialで434スコアを集めて拡散。AIが数学の未解決問題を自力で押し進めた事例として議論を呼ぶ。"),
    "https://www.reddit.com/r/MachineLearning/comments/1tiy6s4/openai_claims_a_generalpurpose_reasoning_model/": (
        "OpenAIが汎用推論モデルでエルデシュの単位距離限界の反例を発見と主張",
        "汎用推論モデルがエルデシュの単位距離限界に対する反例を見つけたというOpenAIの主張を、r/MachineLearningで技術的に検討する議論スレッド。"),
    "https://www.reddit.com/r/MachineLearning/comments/1tiw739/how_competitive_are_phd_admissions_currently_d/": (
        "今のPhD入学はどれくらい競争が激しいか",
        "機械学習分野の博士課程入試の競争激化について現状を尋ね合うr/MachineLearningの議論。AI人気で志願者が膨らむ実情がうかがえる。"),
    "https://www.reddit.com/r/artificial/comments/1tj9m8s/google_is_officially_replacing_vertex_ai_with_the/": (
        "Google、Vertex AIを新「Gemini Enterprise Agent Platform」へ置き換え",
        "GoogleがエンタープライズAI基盤Vertex AIを、新たな「Gemini Enterprise Agent Platform」に正式に置き換えると伝える投稿。エージェント中心への路線転換を示す。"),
    "https://www.reddit.com/r/MachineLearning/comments/1tjmrxm/do_vlms_in_production_still_use_fixedpatch_vits/": (
        "本番のVLMはいまだ固定パッチViTを視覚に使っているのか",
        "実運用の視覚言語モデルが視覚処理に今も固定パッチのViTを使っているのかを問う、r/MachineLearningの技術議論。"),
    "https://www.reddit.com/r/MachineLearning/comments/1tiqlsu/any_tool_to_get_accepted_conference_papers_sorted/": (
        "採択済み会議論文を引用数順に並べるツールはあるか",
        "学会の採択論文を引用数で並べ替えられるツールを探すr/MachineLearningの質問投稿。"),
    "http://comicsands.com/ai-misses-graduate-names": (
        "卒業式で「新AIシステム」が数百人の卒業生名を読み飛ばし会場がブーイング",
        "大学の卒業式で導入された「新しいAIシステム」が数百人の卒業生の名前を飛ばしたとされ、会場がブーイングに包まれたという報道。AI導入の拙速さを象徴する一件。"),
    "https://www.reddit.com/r/artificial/comments/1tif4kd/feels_like_ai_tooling_is_evolving_faster_than/": (
        "AIツールの進化が開発者体験の進化を追い越している気がする",
        "AIツール自体は急速に進化する一方、それを使う開発者体験(DX)が追いついていないという問題提起のr/artificial投稿。"),
    "https://www.reddit.com/r/artificial/comments/1tic62c/andrej_karpathy_just_joined_anthropic/": (
        "アンドレイ・カーパシーがAnthropicに加わったとの投稿",
        "著名なAI研究者アンドレイ・カーパシーがAnthropicに加わったとするr/artificialの投稿。エンゲージメントは小さく、裏取りを要する話題。"),
    "https://www.reddit.com/r/artificial/comments/1ti8wc0/if_ai_didnt_threaten_our_jobs_would_most_people/": (
        "もしAIが雇用を脅かさなければ、人々のAI観は変わるか",
        "AIへの反発の根は雇用不安にあるのではないか——もし職を脅かさなければ大半の人の感情は違うはず、と問うr/artificialの議論。"),
    "https://www.reddit.com/r/MachineLearning/comments/1tij4st/cantante_optimizing_agentic_systems_via/": (
        "CANTANTE: 対比的信用割当によるエージェントシステムの最適化",
        "対比的な信用割当(クレジット帰属)でエージェントシステムを最適化する研究のr/MachineLearning投稿。"),
    "https://www.reddit.com/r/artificial/comments/1tjd2w3/what_is_the_actual_cost_of_developing_agentic_ai/": (
        "2026年、企業向けエージェントAI開発の実際のコストは",
        "2026年に企業プラットフォーム向けのエージェントAIを開発する実コストを問うr/artificialの議論。"),
    "https://www.reddit.com/r/MachineLearning/comments/1ticoy5/instructions_for_icml_workshop_reviews_d/": (
        "ICMLワークショップ査読の指示について",
        "ICMLワークショップの査読指示をめぐるr/MachineLearningの議論投稿。"),
    "https://www.reddit.com/r/artificial/comments/1ti1rry/anyone_can_customize_llms_for_their_needs/": (
        "誰でも自分のニーズに合わせてLLMをカスタマイズできる",
        "専門家でなくても自分の用途に合わせてLLMをカスタマイズできる、という主張のr/artificial投稿。"),
}

# ─── GitHub translations (url → title_ja, summary_ja) for new items ───
github_new = {
    "https://github.com/multica-ai/andrej-karpathy-skills": (
        "andrej-karpathy-skills: Claude Codeの挙動を改善するCLAUDE.md",
        "アンドレイ・カーパシーのLLMコーディングの落とし穴に関する観察をもとに、Claude Codeの挙動を改善する単一のCLAUDE.mdファイル。"),
    "https://github.com/obra/superpowers": (
        "superpowers: 機能するエージェント的スキル枠組みと開発方法論",
        "実際に機能するとうたうエージェント的スキルの枠組みとソフトウェア開発方法論。20万スター超を集める。"),
    "https://github.com/msitarzewski/agency-agents": (
        "agency-agents: 手元に完結するAIエージェンシー",
        "フロントエンドからRedditコミュニティ運用まで、個性と手順と成果物を備えた専門エージェント群を集めた「AIエージェンシー」一式。"),
    "https://github.com/anthropics/claude-plugins-official": (
        "claude-plugins-official: Anthropic公式のClaude Codeプラグイン集",
        "高品質なClaude Codeプラグインを集めた、Anthropic公式管理のディレクトリ。"),
    "https://github.com/HKUDS/CLI-Anything": (
        "CLI-Anything: あらゆるソフトをエージェントネイティブに",
        "あらゆるソフトウェアをエージェントが扱えるCLIに変える「CLI-Anything」。エージェント時代のツール統合を狙うプロジェクト。"),
    "https://github.com/multica-ai/multica": (
        "multica: オープンソースのマネージドエージェント基盤",
        "コーディングエージェントを「本物のチームメイト」に変え、タスク割当・進捗追跡・スキル蓄積を行うオープンソースのマネージドエージェント基盤。"),
    "https://github.com/antoinezambelli/forge": (
        "forge: 自前ホストLLMのツール呼び出し・エージェント枠組み",
        "自前ホストの小型LLMでツール呼び出しと多段の自律ワークフローを安定させるPython枠組み。ガードレールで小型モデルの信頼性を底上げする。"),
    "https://github.com/teng-lin/notebooklm-py": (
        "notebooklm-py: Google NotebookLMの非公式Python API",
        "Google NotebookLMを非公式にプログラム制御するPython API・エージェントスキル。Web UIが公開しない機能までCLIやAIエージェントから扱える。"),
    "https://github.com/dotnet/skills": (
        "dotnet/skills: .NET/C#向けのAIエージェント支援スキル集",
        "AIコーディングエージェントの.NET・C#開発を支援するスキルを集めた公式リポジトリ。"),
    "https://github.com/ChromeDevTools/chrome-devtools-mcp": (
        "chrome-devtools-mcp: コーディングエージェント向けChrome DevTools",
        "コーディングエージェントがChrome DevToolsの機能を使えるようにするMCPサーバ。ブラウザのデバッグ情報をエージェントに橋渡しする。"),
}

# ─── Blog translations (url → title_ja, summary_ja) for new items ───
blogs_new = {
    "https://openai.com/index/adventhealth": (
        "AdventHealth、OpenAIで「全人的ケア」を推進",
        "医療機関AdventHealthがChatGPT for Healthcareを使い、業務を効率化し管理負担を減らして患者ケアに時間を戻す事例。"),
    "https://blog.google/innovation-and-ai/infrastructure-and-cloud/global-network/missouri-programs/": (
        "Google、ミズーリ州での地域投資を発表",
        "Googleがミズーリ州で次世代の人材育成とエネルギー計画への投資を発表。データセンター拡大に伴う地域貢献策。"),
    "https://openai.com/index/ramp": (
        "RampのエンジニアはCodexでコードレビューをどう加速しているか",
        "RampのエンジニアがGPT-5.5搭載のCodexでコードレビューを行い、数時間かかっていた実質的なフィードバックを数分で得ている事例。"),
    "https://huggingface.co/blog/allenai/olmoearth-v1-1": (
        "OlmoEarth v1.1: より効率的な地球観測モデル群",
        "AllenAIによる地球観測モデルOlmoEarthの更新版v1.1。効率を高めたモデルファミリーを公開する。"),
    "https://blog.google/innovation-and-ai/technology/developers-tools/google-io-2026-collection/": (
        "I/O 2026",
        "Google I/O 2026の発表をまとめたコレクションページ。AIをより役立つものにする取り組みを総覧する。"),
    "https://blog.google/products-and-platforms/products/search/ai-mode-us-insights/": (
        "AIモードは米国の検索の仕方をどう変えているか",
        "Google検索の「AIモード」が米国でどう使われているかの分析。検索行動の変化のデータを示す。"),
    "https://blog.google/products-and-platforms/products/workspace/workspace-updates/": (
        "Google Workspaceでの新しい作成・作業のかたち",
        "Google WorkspaceにI/O 2026で発表された新機能群。AIによる作成支援や作業効率化のアップデート。"),
    "https://blog.google/innovation-and-ai/sundar-pichai-io-2026/": (
        "I/O 2026: エージェント的Geminiの時代へようこそ",
        "スンダー・ピチャイによるI/O 2026の基調。GeminiがエージェントとしてAIをより役立つものにする「エージェント的Geminiの時代」を打ち出す。"),
    "https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/": (
        "Gemini 3.5: 行動を伴うフロンティアの知能",
        "GoogleのフラッグシップモデルGemini 3.5。単なる応答でなく「行動を伴う」エージェント能力を前面に出した最新世代。"),
    "https://blog.google/products-and-platforms/products/search/search-io-2026/": (
        "AI検索の新時代",
        "検索エンジンの良さとAIの良さを融合するという、Google検索のI/O 2026での刷新発表。"),
    "https://blog.google/products-and-platforms/products/google-one/google-ai-subscriptions/": (
        "I/O 2026発、Google AIサブスクの刷新",
        "I/O 2026に合わせたGoogle AIサブスクリプションの更新。同価格でより多くの機能・特典を提供するという。"),
    "https://huggingface.co/blog/ettin-reranker": (
        "Ettinリランカーファミリーの紹介",
        "検索結果を再順位付けするリランカーモデル「Ettin」ファミリーの公開。検索拡張パイプライン向けの部品。"),
    "https://huggingface.co/blog/nvidia/cosmos-fine-tuning-for-robot-video-generation": (
        "NVIDIA Cosmos Predict 2.5をLoRA/DoRAでファインチューニング",
        "ロボット動画生成のため、NVIDIAの世界モデルCosmos Predict 2.5をLoRA/DoRAで微調整する手法の解説。"),
    "https://huggingface.co/blog/PaddlePaddle/paddleocr-transformers": (
        "PaddleOCR 3.5: Transformersバックエンドで文書解析",
        "OCR・文書解析ツールPaddleOCR 3.5が、Hugging Face Transformersバックエンドで動かせるようになった。"),
    "https://huggingface.co/blog/ibm-research/open-agent-leaderboard": (
        "Open Agent Leaderboard",
        "IBM Researchによる、エージェントの性能を比較するオープンなリーダーボードの紹介。"),
    "https://openai.com/index/dell-codex-enterprise-partnership": (
        "OpenAIとDell、Codexをハイブリッド・オンプレ環境へ",
        "OpenAIとDellが提携し、コーディングエージェントCodexをハイブリッドやオンプレミスの企業環境に展開。データを社内に保ったままAIコーディングを使えるようにする。"),
    "https://openai.com/index/malta-chatgpt-plus-partnership": (
        "OpenAIとマルタ、全国民にChatGPT Plusを提供",
        "OpenAIがマルタと提携し、全国民にChatGPT Plusと研修を提供。国家規模でのAIアクセス拡大の事例。"),
    "https://openai.com/academy/codex-for-work/how-sales-teams-use-codex": (
        "営業チームはCodexをどう使うか",
        "営業チームがCodexを使い、パイプライン要約や商談準備資料、予測レビュー、停滞案件の診断などを実務データから作る方法の解説。"),
    "https://openai.com/index/databricks": (
        "Databricks、GPT-5.5を企業のエージェントワークフローへ",
        "DatabricksがGPT-5.5を企業のエージェントワークフローに採用。同モデルがOfficeQA Proベンチで新たなSOTAを記録したことを受けたもの。"),
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
        "source": "hn",
        "title": "Qwen3.7-Max: The Agent Frontier",
        "title_ja": "Qwen3.7-Max登場——Alibabaの新フラッグシップが「エージェントのフロンティア」を掲げる",
        "url": "https://qwen.ai/blog?id=qwen3.7",
        "hot_take_ja": "中国勢の追い上げが「エージェント」の土俵で本格化した。AlibabaのQwenチームが新フラッグシップ「Qwen3.7-Max」を公開し、キャッチコピーはずばり『The Agent Frontier』——単発のチャット性能ではなく、ツールを呼び自律的に多段タスクをこなす力を主戦場に据えた。Gemini 3.5やGPT-5.5が並ぶフロンティア争いに、Qwenが正面から名乗りを上げた格好だ。",
        "detail_ja": "AlibabaのQwenチームが、新たなフラッグシップ大規模言語モデル「Qwen3.7-Max」を発表した。Hacker Newsには「Qwen3.7-Max: The Agent Frontier」という見出しで投稿され、686ポイントを集めて1日の上位に入った。注目すべきはその打ち出し方だ。モデル名に冠された「Max」はQwenシリーズの最上位ティアを指し、サブタイトルの「エージェントのフロンティア(The Agent Frontier)」は、このモデルが単発の質問応答や文章生成ではなく、ツールを呼び出し複数ステップにわたって自律的にタスクを遂行する「エージェント」用途に主眼を置いていることを示す。これは業界全体の潮流と一致する。Google I/Oが「エージェント的Geminiの時代」を掲げ、Gemini 3.5を「行動を伴う知能」と位置づけたのと同じ方向で、フロンティアモデルの競争軸が「賢く答える」から「自律的に動く」へと移っていることの表れだ。Qwenはオープンウェイトのモデル群でも知られ、米国のクローズドなフロンティアモデルに対する強力な対抗馬と見なされてきた。その最上位モデルがエージェント能力を前面に出したことは、エージェント性能が今後のモデル評価の中心的な指標になりつつあることを裏づける。注意点として、これは公開直後の発表であり、ベンチマークの具体的な数値や他モデルとの厳密な優劣は、第三者による独立評価を待って判断するのが妥当だ。誇大な自己申告と実力の乖離は、この分野で繰り返し起きてきた。",
        "detail_en": "Alibaba's Qwen team has announced a new flagship large language model, \"Qwen3.7-Max.\" It was posted to Hacker News under the headline \"Qwen3.7-Max: The Agent Frontier\" and drew 686 points, landing among the day's top stories. What stands out is the framing. The \"Max\" in the name denotes the top tier of the Qwen series, and the subtitle \"The Agent Frontier\" signals that the model is aimed not at one-shot question answering or text generation but at \"agentic\" use — calling tools and autonomously carrying out multi-step tasks. This aligns with an industry-wide trend. It points in the same direction as Google I/O's \"agentic Gemini era\" framing and its positioning of Gemini 3.5 as \"intelligence with action\": the competitive axis for frontier models is shifting from \"answer smartly\" to \"act autonomously.\" Qwen is also known for its open-weight model lineup and has been seen as a strong challenger to the closed frontier models from the US. Its top model now leading with agentic capability reinforces the idea that agentic performance is becoming the central metric for evaluating models. One caveat: this is a fresh announcement, and the specific benchmark numbers and rigorous comparisons against other models are best judged after independent third-party evaluation. The gap between inflated self-reported claims and real-world capability has recurred repeatedly in this field.",
        "key_points_ja": [
            "AlibabaのQwenが新フラッグシップ「Qwen3.7-Max」を公開",
            "「The Agent Frontier」を掲げ、エージェント用途を主眼に",
            "競争軸が「賢く答える」から「自律的に動く」へ",
            "Google I/Oの「エージェント的Gemini」と同じ潮流",
            "Qwenはオープンウェイト勢の有力な対抗馬",
            "ベンチ数値は独立評価を待って判断するのが妥当",
        ],
        "key_points_en": [
            "Alibaba's Qwen unveils new flagship 'Qwen3.7-Max'",
            "Framed as 'The Agent Frontier' — agentic use is the focus",
            "Competitive axis shifts from 'answer' to 'act autonomously'",
            "Same trend as Google I/O's 'agentic Gemini' framing",
            "Qwen is a strong open-weight challenger to closed models",
            "Benchmark numbers best judged after independent evaluation",
        ],
    },
    {
        "source": "hn",
        "title": "OpenAI Is Preparing to File for an IPO Soon",
        "title_ja": "OpenAI、近くIPOを申請へ——AI時代を象徴する上場が現実味",
        "url": "https://www.wsj.com/tech/ai/openai-is-preparing-to-file-for-an-ipo-very-soon-0ec95af5",
        "hot_take_ja": "ついに、という話だ。OpenAIが近く新規株式公開(IPO)の申請準備に入っているとWSJが報じた。非営利として始まり営利再編で揺れたあの会社が、公開市場に株式を出す——AIブームの資金を一般投資家にも開く節目であり、同時に「AIバブル」論争の最大の試金石になる。IPOで付く値段が、そのまま市場が今のAI熱狂をどう評価しているかの答えになる。",
        "detail_ja": "ウォール・ストリート・ジャーナルが、OpenAIが近く新規株式公開(IPO)の申請準備を進めていると報じた。Hacker Newsでもこの記事が168ポイント・369コメントを集め、活発な議論を呼んだ。OpenAIは2015年に非営利団体として設立され、その後営利子会社を抱える独特の構造を経て、近年は営利企業としての再編を進めてきた。ChatGPTを擁し、世界で最も注目されるAI企業のひとつであるOpenAIが公開市場に上場すれば、それはAIブームの象徴的な出来事になる。意味合いは大きく三つある。第一に、これまで一部の大口投資家やマイクロソフトなどの戦略的パートナーに限られていたOpenAIへの出資機会が、一般投資家にも開かれる。第二に、IPOで付く時価総額は、市場が現在のAI熱狂をどう値付けするかの最も明確な答えになる——「AIバブル」かどうかの議論に、株価という具体的な数字が突きつけられる。第三に、上場企業になれば四半期ごとの開示義務が生じ、これまで不透明だったOpenAIの収益構造やコスト(特に巨額の計算インフラ支出)が公の監視下に置かれる。注意したいのは、これはあくまで「申請準備」段階の報道であり、実際の上場時期・規模・評価額・株式構造はまだ確定していない点だ。市況や規制対応次第でスケジュールは前後しうる。それでも、AI業界の中核企業が公開市場へ向かうという方向性自体が、この分野が実験段階から本格的な資本市場の対象へと移りつつあることを示している。",
        "detail_en": "The Wall Street Journal has reported that OpenAI is preparing to file for an initial public offering (IPO) soon. The article also drew 168 points and 369 comments on Hacker News, sparking lively debate. OpenAI was founded in 2015 as a nonprofit, later operated through a distinctive structure with a for-profit subsidiary, and in recent years has been moving toward a restructuring as a for-profit company. If OpenAI — the maker of ChatGPT and one of the most closely watched AI companies in the world — lists on the public markets, it would be a symbolic moment for the AI boom. There are three big implications. First, the opportunity to invest in OpenAI, until now limited to certain large investors and strategic partners such as Microsoft, would open up to retail investors. Second, the market capitalization set at the IPO would be the clearest answer yet to how the market prices the current AI frenzy — the \"AI bubble\" debate would be confronted with a concrete number, the share price. Third, as a public company OpenAI would face quarterly disclosure obligations, placing its previously opaque revenue structure and costs (especially its massive compute infrastructure spending) under public scrutiny. One caveat: this is reporting at the \"preparing to file\" stage, and the actual timing, size, valuation, and share structure of the offering are not yet fixed. The schedule could shift depending on market conditions and regulatory matters. Even so, the very direction — a core AI company heading for the public markets — shows that the field is moving from an experimental phase toward becoming a serious object of the capital markets.",
        "key_points_ja": [
            "OpenAIが近くIPO申請準備とWSJが報道",
            "非営利で発足、営利再編を経ての上場観測",
            "一般投資家にもOpenAIへの出資機会が開く",
            "IPO時価総額が「AIバブル」論争の試金石に",
            "上場で収益・コスト構造が四半期開示の対象に",
            "時期・規模・評価額は未確定、市況次第で前後も",
        ],
        "key_points_en": [
            "WSJ reports OpenAI preparing to file for an IPO soon",
            "Founded as a nonprofit; listing follows for-profit restructuring",
            "Retail investors would gain access to invest in OpenAI",
            "IPO market cap becomes a test of the 'AI bubble' debate",
            "Listing puts revenue and cost structure under disclosure",
            "Timing, size, valuation still unfixed; schedule may shift",
        ],
    },
    {
        "source": "hn",
        "title": "AI is just unauthorised plagiarism at a bigger scale",
        "title_ja": "「AIは規模を拡大した盗用」——HNでAIへの反発が一気に噴き出した日",
        "url": "https://axelk.ee/ai-is-just-unauthorised-plagiarism-at-a-bigger-scale/",
        "hot_take_ja": "この日のHacker Newsは、まるでAIへの不満の見本市だった。「AIは規模を拡大した無断盗用にすぎない」が701点、「AIを避けるのが人間的な選択だ」が332点、「AI生成の長文を会話に投げ込むな」が389点、卒業式でのAI礼賛にブーイング——技術好きが集まるはずのHNですら、AIへの反発が前向きな話題を上回った。熱狂のサイクルが、ついに逆回転を始めている。",
        "detail_ja": "2026年5月21日のHacker Newsは、AIに対する反発・疲弊・懐疑を扱った記事が同時多発的に上位を占めるという、象徴的な一日になった。最も注目を集めたのは「AI is just unauthorised plagiarism at a bigger scale(AIは規模を拡大した無断盗用にすぎない)」というエッセイで、701ポイントを獲得した。筆者は、AIが原作者の同意なくあらゆる入力を取り込み、出所に報いることなく利益を上げていると批判する。実体験として、自分が書いたECサイト構築のチュートリアルを、ChatGPT生成のほぼ同内容のコピーが検索結果で上回り、リンクまで写し取られていたと述べ、派生コンテンツを優遇するGoogleの検索順位にも矛先を向けた。同じ日には、「Shunning AI is the human choice(AIを避けることこそ人間的な選択)」が332ポイント、「Stop throwing AI-generated walls of text into conversations(AI生成の長文の塊を会話に投げ込むな)」が389ポイント、米大学の卒業式でAIを称賛する祝辞に学生がブーイングを浴びせたという記事が368ポイントを集めた。重要なのは、Hacker Newsが本来テクノロジーに肯定的な、エンジニアや起業家中心のコミュニティだという点だ。そのHNですら、この日はAIへの肯定的な話題よりも反発・疲弊の声が上位を占めた。背景には複数の要因が絡む——AI生成の低品質コンテンツ(スロップ)の氾濫、創作物の無断学習をめぐる著作権の不満、相次ぐAI絡みの解雇による雇用不安、そして「とにかくAIを足せ」という売り込みへの食傷だ。これは単発の炎上ではなく、誇大宣伝サイクルが反転し、文化的な揺り戻しが可視化された局面と読むべきだろう。注意点として、HNのスコアは一部の利用者の熱量を反映するもので社会全体の世論ではない。とはいえ、技術受容の最前線にいる層の空気が変わりつつあることは、AI企業にとって軽視できないシグナルだ。",
        "detail_en": "May 21, 2026 became a symbolic day on Hacker News: articles about backlash, fatigue, and skepticism toward AI simultaneously dominated the top of the front page. The most attention went to an essay titled \"AI is just unauthorised plagiarism at a bigger scale,\" which earned 701 points. The author argues that AI ingests all kinds of input without the consent of original creators and profits without rewarding the sources. Drawing on personal experience, the author describes how a near-identical ChatGPT-generated copy of their own e-commerce tutorial outranked the original in search results — even copying the links — and also takes aim at Google's search rankings for favoring derivative content. The same day, \"Shunning AI is the human choice\" drew 332 points, \"Stop throwing AI-generated walls of text into conversations\" drew 389 points, and an article about US college students booing AI-praising commencement speeches drew 368 points. The key point is that Hacker News is normally a technology-friendly community centered on engineers and founders. Yet even on HN, that day, voices of backlash and fatigue outranked positive AI topics. Several factors are intertwined in the background: a flood of low-quality AI-generated content (\"slop\"), copyright grievances over the unauthorized training on creative works, job anxiety from a string of AI-related layoffs, and exhaustion with the \"just add AI\" sales pitch. This should be read not as a one-off flare-up but as a moment when the hype cycle turned and a cultural backlash became visible. One caveat: HN scores reflect the intensity of a subset of users, not society-wide public opinion. Even so, the shift in mood among those at the frontier of technology adoption is a signal AI companies cannot afford to ignore.",
        "key_points_ja": [
            "HNでAI反発系の記事が同時に上位を独占",
            "「AIは規模を拡大した盗用」が701点で筆頭",
            "「AIを避けるのが人間的」「長文スロップを投げるな」も上位",
            "技術好きのHNですら反発が肯定的話題を上回った",
            "背景はスロップ氾濫・著作権不満・雇用不安・売り込み疲れ",
            "スコアは世論そのものではないが無視できないシグナル",
        ],
        "key_points_en": [
            "AI-backlash articles simultaneously dominated HN's top",
            "'AI is unauthorised plagiarism' led with 701 points",
            "'Shunning AI is human' and 'no walls of text' also ranked high",
            "Even tech-friendly HN saw backlash outrank positive topics",
            "Drivers: slop, copyright grievances, job fear, pitch fatigue",
            "Scores aren't public opinion, but a signal worth heeding",
        ],
    },
    {
        "source": "hn",
        "title": "Intuit to lay off over 3k employees to refocus on AI",
        "title_ja": "Intuitが3,000人解雇、Cloudflare CEOは「誰をAIに置き換えるか」を公言——AI解雇が手順化した",
        "url": "https://techcrunch.com/2026/05/20/intuit-to-lay-off-over-3000-employees-to-refocus-on-ai/",
        "hot_take_ja": "もはや言い訳しない、という段階に入った。Intuitは好決算のさなかに全社員の17%・3,000人超を「AIへの注力」のために解雇。同じ日、CloudflareのプリンスCEOはWSJ寄稿で「どの従業員をAIで置き換えるか、私はこう選ぶ」と判断基準まで公開した。AIによる人員削減は、もはや経営者がこっそりやることではなく、手順として堂々と語られるものになった。",
        "detail_ja": "AIを理由とした人員削減が、企業の「公然たる経営手法」へと変質しつつあることを示す二つの動きが、同じ日に重なった。ひとつはIntuitだ。TurboTaxやQuickBooks、Credit Karmaを擁する財務ソフト大手のIntuitは、全世界の従業員の約17%にあたる3,000人超の解雇を発表した。CEOのササン・グダルジは、組織構造を簡素化して複雑さを減らし、AI製品開発に資源を集中させるためだと説明している。注目すべきは、これが業績不振による削減ではない点だ。同社の四半期売上は前年比17%増の46.5億ドル、純利益も48%増と好調で、それでも人を切ってAIに振り向けている。背景には、従来型のSaaS企業がAIネイティブの新興勢に対抗できなくなるのではという業界の不安がある。もうひとつはCloudflareだ。同社のマシュー・プリンスCEOは、ウォール・ストリート・ジャーナルへの寄稿で「どのCloudflareの従業員をAIで置き換えるかを、私はどう選ぶか」を率直に論じた。解雇そのものより、経営トップが置き換えの判断基準を公の場で言語化したことに重みがある。この二件が示すのは、AIによる人員削減がもはや遠回しに語られる「副作用」ではなく、明示的な経営戦略・手順として正面から語られる段階に入ったということだ。5月20日にはMetaが好決算下で約8,000人を解雇しており、Intuit・Cloudflareはその流れの上にある。報道によれば、2026年のテック業界の人員削減は累計で10万人を超えた。ただし注意したいのは、「AIのため」という説明が常に額面通りとは限らないことだ。景気減速や過剰採用の調整、株価対策といった従来型のリストラ動機を、より前向きに聞こえる「AIシフト」の語で包んでいる側面もありうる。それでも、解雇を語る言葉そのものが変わったことは、労働市場におけるAIの位置づけの変化を映している。",
        "detail_en": "Two developments on the same day show how AI-driven headcount cuts are shifting into an openly stated management practice. The first is Intuit. The financial-software giant — maker of TurboTax, QuickBooks, and Credit Karma — announced the layoff of more than 3,000 employees, about 17% of its global workforce. CEO Sasan Goodarzi explained that the goal is to reduce complexity by simplifying the corporate structure and to concentrate resources on AI product development. What stands out is that this is not a cut driven by poor performance: the company's quarterly revenue was $4.65 billion, up 17% year over year, and net profit rose 48% — and it is still cutting people to redirect toward AI. Behind it lies an industry fear that traditional SaaS companies may no longer be able to compete against AI-native upstarts. The second is Cloudflare. CEO Matthew Prince, in an op-ed for The Wall Street Journal, candidly discussed \"how I choose which Cloudflare employees to replace with AI.\" More than the cuts themselves, the weight lies in a chief executive publicly articulating the criteria for replacement. Together, these two cases show that AI-driven headcount reduction has entered a phase where it is discussed head-on as an explicit management strategy and procedure, not as an obliquely mentioned \"side effect.\" On May 20, Meta cut about 8,000 jobs amid strong earnings, and Intuit and Cloudflare sit on that same trend; per reporting, tech-industry layoffs in 2026 have cumulatively passed 100,000. One caveat, however: the explanation \"for AI\" is not always to be taken at face value. Traditional restructuring motives — an economic slowdown, correcting over-hiring, propping up the share price — may in part be wrapped in the more upbeat language of an \"AI shift.\" Even so, the very fact that the language used to describe layoffs has changed reflects a shift in AI's place in the labor market.",
        "key_points_ja": [
            "Intuitが全社員17%・3,000人超を「AI注力」で解雇",
            "売上17%増・純利益48%増の好決算下での削減",
            "Cloudflare CEOは「誰をAIで置き換えるか」をWSJで公言",
            "経営者が置き換え基準を公の場で言語化した点が重い",
            "5月20日のMeta約8,000人解雇に続く流れ",
            "「AIのため」が従来型リストラの建前を含む可能性に留意",
        ],
        "key_points_en": [
            "Intuit cuts 3,000+ (17% of staff) to 'refocus on AI'",
            "Cuts come amid strong results: revenue +17%, profit +48%",
            "Cloudflare CEO publicly states how he picks who AI replaces",
            "Weight is in a CEO articulating replacement criteria openly",
            "Follows Meta's ~8,000 cuts on May 20",
            "'For AI' framing may partly mask traditional restructuring",
        ],
    },
    {
        "source": "arxiv",
        "title": "Quality and Security Signals in AI-Generated Python Refactoring Pull Requests",
        "title_ja": "AIが書いたリファクタリングPRを実プロジェクトで検証——73.5%がマージ、でも4分の1が新たな不具合の種を埋め込む",
        "url": "https://arxiv.org/abs/2605.21453v1",
        "hot_take_ja": "AIエージェントのコードを「実際にマージした後」どうなったかを追った、珍しく地に足のついた研究だ。エージェントのリファクタリングPRの22.5%は品質指標を改善する一方、24%は新たなLint違反を、4.7%は新たなセキュリティ指摘を生む。それでも73.5%がマージされる——不具合の種ごと取り込まれている。「賢いエージェント」より「マージ前のゲート」が要る、と数字が言っている。",
        "detail_ja": "AIエージェントが書いたコードは、レビューを通り実プロジェクトにマージされた後、実際のところ品質やセキュリティにどう影響するのか——この素朴だが重要な問いに実証的に答えた研究だ。著者らは、AIエージェントによるコード貢献を集めたデータセット「AIDev」から、Pythonのリファクタリング目的のプルリクエスト(PR)を抽出して分析した。評価には、Python向けのML品質評価ツール「PyQu」で5つの品質属性の変化を測り、加えてドメイン非依存の静的解析ツールPylint(コード品質)とBandit(セキュリティ)で、変更の前後を比較した。結果は両義的だ。良い面として、エージェントのコミットは平均して調査対象の22.5%で何らかの品質属性を改善し、特に「使いやすさ(usability)」が36.5%と最も頻繁に向上した。一方で悪い面として、変更されたファイルの24.17%が新たなPylintの指摘を生み(その多くは長すぎる行などの規約レベルの違反)、4.7%が新たなBanditのセキュリティ指摘を導入した。著者らは観測された差分から24種類の頻出変更操作の分類体系を作り、それぞれがどのLint・セキュリティ指摘に結びつきやすいかを対応づけた。最も示唆的なのは開発者の受け入れ態度だ。分析対象PRの73.5%がマージされており、その中には新たなLint違反やセキュリティ指摘を持ち込んだものも含まれる——既存の問題の除去と引き換えに、新たな問題ごと取り込まれているのだ。著者らはこれを「エージェント的リファクタリングの有望さと現時点の限界の両方」を示すものと位置づけ、AI駆動開発には「ツールをループに組み込んだ品質・セキュリティのゲーティング」がより強く必要だと結論づける。これは今週のHacker Newsで話題になった「AIコーディングループのための形式検証ゲート」や、前日のハイライト「ガードレールで小型モデルを底上げするForge」と同じ思想——人間やCIによる検証の足場こそが要、という潮流の、実データによる裏づけといえる。",
        "detail_en": "This research empirically answers a simple but important question: once code written by AI agents passes review and is merged into real projects, how does it actually affect quality and security? The authors extracted Python refactoring-oriented pull requests (PRs) from \"AIDev,\" a dataset of code contributions made by AI agents. For evaluation, they used \"PyQu,\" an ML-based quality-assessment tool for Python, to measure changes across five quality attributes, and complemented it with domain-independent static analyzers — Pylint (code quality) and Bandit (security) — comparing each change before and after. The results are mixed. On the positive side, agentic commits improved some quality attribute in 22.5% of the studied changes on average, with \"usability\" improving most frequently, at 36.5%. On the negative side, 24.17% of modified files introduced new Pylint findings (many of them convention-level violations such as overly long lines), and 4.7% introduced new Bandit security findings. From the observed diffs, the authors built a taxonomy of 24 recurring change operations and mapped each to the lint and security findings it most commonly affects. The most telling result is developer acceptance: 73.5% of the analyzed PRs were merged — including ones that introduced new lint or security findings, often alongside the removal of existing issues. In other words, new problems are being taken in along with the change. The authors frame this as showing \"both the promise and the current limitations of agentic refactoring,\" and conclude that AI-driven development needs stronger \"tool-in-the-loop quality and security gating.\" This is empirical backing for the same idea behind this week's Hacker News discussion of \"formal verification gates for AI coding loops\" and the prior day's highlight on \"Forge,\" which boosts small models with guardrails — the trend that the scaffolding of human or CI verification is what matters.",
        "key_points_ja": [
            "AIエージェントのPythonリファクタリングPRを実証分析",
            "22.5%が品質属性を改善、使いやすさが最頻(36.5%)",
            "24.17%のファイルが新たなLint指摘を導入",
            "4.7%が新たなセキュリティ指摘(Bandit)を持ち込む",
            "それでも73.5%がマージ——不具合の種ごと取り込み",
            "結論は「マージ前の品質・セキュリティゲートが必要」",
        ],
        "key_points_en": [
            "Empirical study of AI agents' Python refactoring PRs",
            "22.5% improve a quality attribute; usability most often (36.5%)",
            "24.17% of files introduce new Pylint findings",
            "4.7% introduce new Bandit security findings",
            "Yet 73.5% get merged — new problems taken in too",
            "Conclusion: need quality/security gating before merge",
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
