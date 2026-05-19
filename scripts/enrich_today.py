#!/usr/bin/env python3
"""Enrichment for 2026-05-19 (fresh page).

arXiv set is fully new (50 items, all translated below).
HN/Reddit/GitHub/blogs reuse prior Japanese translations for overlapping
URLs (from data/2026-05-18.json) and translate new items inline.
Five fresh highlights are selected for the day.
"""
import json
from pathlib import Path

DATE = "2026-05-19"
PREV = "2026-05-18"
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
    "2605.18754v1": (
        "これらの視点は一つのシーンになりうるか——3D基盤モデルが幻覚するときの多視点整合性評価",
        "多視点3D評価は採点対象画像が一つの静的シーンの観測だと前提するが、新規視点合成や疎視点復元ではアーティファクトや外れフレームを含んでも高い整合性スコアが付く。学習型復元事前分布と古典的幾何検証を比較してこの信頼性問題を検証する。"),
    "2605.18753v1": (
        "DashAttention: 微分可能で適応的な疎な階層的アテンション",
        "top-k選択に頼る既存の階層的アテンションは関連トークン数を固定とみなし、疎・密の段階間で勾配を遮断する。適応的に疎なα-entmax変換で可変個のブロックを選び勾配を流す手法を提案。"),
    "2605.18750v1": (
        "実行時のばらつきに対応するパイプライン並列学習の準備度駆動ランタイム",
        "静的にコミットされた実行順は実際のタスク準備状況とずれると遊休バブルを生む。準備のできたタスクを優先実行するランタイムRRFPで段間のずれと利用率低下を解消する。"),
    "2605.18749v1": (
        "WavFlow: 波形空間での音声生成",
        "潜在空間圧縮に頼る現代の音声生成に対し、中間表現なしに生波形空間で高忠実度音声を直接生成。波形のパッチ化と振幅リフティングでスケールを揃え安定に最適化する。"),
    "2605.18748v1": (
        "Aurora: ツールを使うエージェントによる統一動画編集",
        "統一動画編集モデルはユーザがモデル向けの整ったテキスト・参照画像・空間指定を用意済みと前提する。ツール拡張した視覚言語エージェントを組み合わせ、それらを省いた現実的な要求にも対応する。"),
    "2605.18747v1": (
        "コードをエージェントのハーネスとして",
        "エージェントシステムでコードは出力対象にとどまらず、推論・行動・環境モデリング・実行検証の運用基盤になりつつある。この転換を『エージェント・ハーネス』の観点で体系化する。"),
    "2605.18746v1": (
        "ESI-Bench: 知覚-行動ループを閉じる身体化空間知能へ",
        "空間知能は『行動して観測を得る』知覚-行動ループで展開する。観測を所与とする従来の定式化を超え、観測者を行為者として捉える身体化空間知能の包括的ベンチマーク。"),
    "2605.18745v1": (
        "SURGE: 拡散代理モデルのための近似なし・学習不要なパーティクルフィルタ",
        "推論時ガイダンスは繰り返しのスコア・勾配評価でバイアスや計算コストを生む。ジルサノフの測度変換による経路ごとの重要度再重み付けで、微分なしの推論時スケーリングを実現する。"),
    "2605.18743v1": (
        "行為可能な世界表現",
        "物理世界モデルでは物体が基本要素だが、物体は静的でなく内在的性質によって状態が変わる『行為可能な』存在だ。その動的に変わる状態を扱える物体表現を提案する。"),
    "2605.18740v1": (
        "Vision-OPD: オンポリシー自己蒸留でマルチモーダルLLMに細部を見せる",
        "MLLMは画像中の小さく決定的な手がかりを捉えるのが苦手。証拠中心の切り抜きを条件にすると精度が上がる現象を利用し、領域から全体への自己蒸留で細粒度理解を改善する。"),
    "2605.18739v1": (
        "LongLive-2.0: 長尺動画生成のためのNVFP4並列インフラ",
        "長尺動画生成の速度・メモリのボトルネックに対し、学習から推論まで一貫したNVFP4ベースの並列インフラを提案。シーケンス並列の自己回帰学習でGPUメモリを削減し高速化する。"),
    "2605.18738v1": (
        "AI医師は何を重んじるか——言語モデルの臨床倫理における多元性の監査",
        "医療は本質的に多元的で、自律・善行・無危害・正義の原則はしばしば衝突する。LLMが医療助言に持ち込む倫理的価値観を、臨床医が検証したジレンマ集と帰属法で体系的に監査する。"),
    "2605.18736v1": (
        "効率的な画像・動画生成のためのスペクトル漸進拡散",
        "拡散モデルは周波数領域で低周波を先に、高周波の細部を後に生成する。この構造を活かし、ノイズ支配の高周波の高解像度計算の冗長性を省き解像度を漸進的に上げる枠組み。"),
    "2605.18735v1": (
        "PIXLRelight: 内在的条件付けによる制御可能なリライティング",
        "単一画像の物理的に制御可能なリライティングを順伝播で実現。実写とPBRレンダの双方から得られる共有の内在的条件で、物理ベースレンダと学習合成を橋渡しする。"),
    "2605.18734v1": (
        "EgoExoMem: 同期した一人称・三人称動画にまたがる記憶推論",
        "一人称視点の記憶だけでは網羅的な時空間推論に不十分。同期した一人称・三人称動画にわたる記憶推論の初のベンチマークと、学習不要のフレーム選択法を提案する。"),
    "2605.18733v1": (
        "学習不要のアイデンティティ認識記憶による物語的長尺動画生成",
        "自己回帰動画生成は長期の不整合や記憶劣化に苦しむ。変化するプロンプトでの登場人物の同一性ドリフトや重複を防ぐ、学習不要のアイデンティティ追跡記憶IAMFlowを提案。"),
    "2605.18732v1": (
        "予測可能な作話——LLMの事実想起はモデルサイズと話題頻度でスケールする",
        "38モデルを8,900件超の学術文献で評価し、事実想起の質がモデルパラメータ数と訓練データ中の話題出現量の対数線形結合のシグモイドに従うと発見。この2変数だけで分散の60%、同一系列内では74-94%を説明する。"),
    "2605.18729v1": (
        "Robo-Cortex: 二粒度の認知記憶と自律的な知識帰納で自己進化する身体化エージェント",
        "未知環境のナビゲーションは過去の経験を一般化できない『経験的健忘』で難しい。成功・失敗パターンを自然言語のヒューリスティックに抽象化し、反省-適応ループで自己進化する枠組み。"),
    "2605.18727v1": (
        "DexHoldem: 器用な身体化システムでテキサスホールデムをプレイ",
        "ShadowHandでのテキサスホールデム操作を中心に据えた実世界のシステムレベル・ベンチマーク。14の操作プリミティブにわたる1,470件のテレオペ実演と、物理方策・エージェント的知覚の評価を提供。"),
    "2605.18722v1": (
        "Dexora: 高自由度の両手器用操作のためのオープンソースVLA",
        "既存のVLAは両グリッパー制御か片腕の器用操作に限られる。両腕・両手の高自由度操作をネイティブに対象とする初のオープンソースVLAシステムを提案する。"),
    "2605.18721v1": (
        "一般選好強化学習",
        "検証可能報酬のオンラインRLは数学・コードで推論を引き出すが開放的タスクに届かず、選好最適化は探索を欠く。スカラー報酬は多次元の品質を測るには不適切だとして、選好で両者の溝を埋める。"),
    "2605.18720v1": (
        "腱駆動連続体ロボットのデータ駆動な動力学モデリング",
        "非線形・高次元・摩擦支配の腱駆動連続体ロボットに対し、N4SID・ARX・SINDYcなどのデータ駆動同定法を比較。CERN開発のロボットで2自由度モデルが動力学を正確に捉えると示す。"),
    "2605.18719v1": (
        "SafeDiffusion-R1: 安全な拡散モデル事後学習のためのオンライン報酬ステアリング",
        "不安全コンテンツの除去は高価な教師データを要し、オフライン手法は破滅的忘却で生成品質が落ちる。データ希少と劣化の両方に対処するオンライン強化学習の事後学習枠組み。"),
    "2605.18714v1": (
        "統一マルチモーダルモデルのための意味的生成チューニング",
        "統一モデルは理解を疎なテキスト信号、生成を密なピクセル目的で別々に最適化し表現空間がずれる。階層的視覚タスクを生成代理として両者を橋渡しする初の体系的研究。"),
    "2605.18704v1": (
        "ロバストなUAV状態推定のためのSage-Husaカルマンフィルタにおける学習型記憶減衰",
        "動的環境のUAVはテレメトリ断や振動で古典カルマンフィルタの定常仮定が崩れる。スカラーの忘却係数をベクトル値の記憶減衰方策に置き換え、階層的再帰NNで学習する。"),
    "2605.18703v1": (
        "EnvFactory: 実行可能環境の合成と頑健なRLでツール使用エージェントを拡張",
        "ツール使用のエージェントRLは堅牢な実行環境とリアルな訓練データの不足が課題。実行可能な環境を合成し、指示列のような過剰指定でない自然な人間の意図を捉える。"),
    "2605.18702v1": (
        "構造化された健康データのための表形式基盤モデルの蒸留",
        "表形式基盤モデルは健康データで高性能だが推論コストとインフラ要件が実用を阻む。文脈リークを層化アウトオブフォールド教師ラベルで防ぎつつ軽量モデルへ蒸留する。"),
    "2605.18701v1": (
        "血液バイオマーカーの正常表現の学習",
        "固定の集団基準範囲は個人内の安定したばらつきを無視し、個人のベースラインからの逸脱を見逃す。疎なデータに過適合せず偽陽性を抑える個別化解釈の表現学習を提案。"),
    "2605.18700v1": (
        "細粒度画像認識における学習・評価設定の精度対コストの大規模研究",
        "2000を超える実験で6つの学習・評価設定、9つの事前学習バックボーン、17データセットを横断。細粒度学習でのデータ拡張の有効性と、精度対コストのトレードオフを検証する。"),
    "2605.18697v1": (
        "PopPy: Python製の複合AIアプリで並列性を日和見的に活用",
        "複合AIアプリの実行時間は外部のML呼び出しが支配し、従来のコンパイラ最適化が効かない。Pythonアプリ中に潜む並列化の機会を自動的に見つけ出して活用するシステム。"),
    "2605.18696v1": (
        "表形式基盤モデルのアンサンブル——多様性の天井と較正の罠",
        "6つの現代の表形式基盤モデルは平均Q統計量0.961とほぼ冗長で、最良のアンサンブル(二段カスケード積層)でも単体比わずか+0.18%の精度を253倍の計算で買うだけだと実証する。"),
    "2605.18694v1": (
        "適応的勾配法は重い裾のノイズ下で収束するか——AdaGradの事例研究",
        "現代の機械学習では重い裾を持つ勾配ノイズが観測される。クリッピングや正規化の追加操作なしで、AdaGradのような適応的勾配法がこの設定で収束しうるかを理論的に解析する。"),
    "2605.18693v1": (
        "SkillGenBench: LLMエージェントのスキル生成パイプラインのベンチマーク",
        "課題はもはやエージェントが与えられたスキルを使えるかでなく、リポジトリや文書から正しく再利用可能で実行できるスキルを生成できるか。これを統一プロトコルで評価する。"),
    "2605.18692v1": (
        "LLM誘導のモデルパッチで大規模な再最適化を民主化",
        "ORの最適化モデルは現場のルール変化や見落とした制約で素早い再最適化を迫られる。LLMがOR専門家として自然言語対話で利用者の再最適化を動的に支援する枠組み。"),
    "2605.18689v1": (
        "量子ガス実験のための機械学習は説明可能になりうるか",
        "冷却原子の量子シミュレータが生む画像データに対し、生画像のノイズ除去とソリトン同定にMLを適用。多体原子物理におけるMLの説明可能性を二つの応用で探る。"),
    "2605.18684v1": (
        "Reversa: レガシーソフトをAIエージェント向けの運用仕様へ変換する逆ドキュメント工学",
        "レガシー系にはコードや設定に暗黙的に埋もれた業務ルールが集中する。それらを、AIコーディングエージェントが頼れる追跡可能な運用仕様へ変換する多エージェント・パイプライン。"),
    "2605.18681v1": (
        "正解データなしで定量化可能な視覚的説明を学習",
        "XAI手法は比較すべき良質な正解がなく評価が難しい。連続的な入力摂動に基づき、帰属された情報のモデル判断への十分性と必要性を形式的に測る定量指標を提案する。"),
    "2605.18680v1": (
        "CMAG: マーケットプレイス向けアバター生成のための概念足場検索",
        "メタバースのアバターは分類ラベル付きの3D素材から厳しい制約下で組まれる。曖昧な自然言語と雑なメタデータに弱いテキスト検索を、概念の足場と検証付き合成で改善する。"),
    "2605.18678v1": (
        "Lance: マルチタスク相乗による統一マルチモーダルモデリング",
        "画像・動画の理解・生成・編集を支える軽量なネイティブ統一モデル。容量のスケールに頼らず、協調的なマルチタスク学習で実用的な統一モデリングのパラダイムを探る。"),
    "2605.18675v1": (
        "COOPO: 循環型のオフライン-オンライン方策最適化アルゴリズム",
        "オフラインRLは分布シフト、オンラインRLは膨大な相互作用が課題で、両者を橋渡しする手法も移行時のドリフトや忘却に悩む。制約付きオフライン学習とオンライン微調整を繰り返し循環する枠組み。"),
    "2605.18674v1": (
        "古典的プランニングの汎用方策学習のための効率的な先読み符号化と抽象化された幅",
        "反復幅(IW)方策は先読み探索で複数遷移を飛び越えるが、各遷移を個別評価するため計算が非効率で表現力にも限界がある。効率的な符号化と抽象化された幅でこれを改善する。"),
    "2605.18673v1": (
        "信頼できる商業的介入の問題としての生成AI広告",
        "LLM出力に直接織り込まれた広告は利用者に気づかれにくい。生成AIは広告枠でなく生成過程そのものへの介入を可能にし、広告を『コンテンツ配置』でなく『信頼できる介入』の問題として捉え直す。"),
    "2605.18672v1": (
        "安全なLLMエージェント展開には三層の確率的アシューム-ギャランティ構造が構造的に必須",
        "LLMエージェントの安全性を単一の抽象層で担保するのは原理的に不十分。意味的意図・環境妥当性・動的実現可能性はそれぞれ別段階で得られる別の情報に依存すると論じる立場論文。"),
    "2605.18667v1": (
        "より良く共に——地球埋め込みモデルの相補性の評価",
        "地球観測データの埋め込みモデルは単独で評価されがちだが、空間的に整合した埋め込みは融合でき位置あたりの情報を豊かにできる。融合による性能向上で相補性を測る評価法を提案。"),
    "2605.18666v1": (
        "ML型侵入検知への勾配ベース敵対的攻撃に対する『無防御の防御』——少ないほど良いか",
        "約2200の実験で、浅いネットワーク・少ない特徴・ReLU活性化が、明示的な防御を一切加えずともML型侵入検知を一貫して敵対的に頑健にすることを示す。"),
    "2605.18663v1": (
        "GIM: 複数の認知領域を統合するタスクでモデルを評価",
        "知識量を増やすか除くかで難化させる従来ベンチに対し、難しさを複数の認知操作の『統合』から生む820問のオリジナル・ベンチマーク。記憶でも抽象推論でもない実践的な難しさを測る。"),
    "2605.18662v1": (
        "多クラス線形分類器の効率的でノイズ耐性のあるPAC学習",
        "二値の線形しきい値関数のノイズ耐性学習は進んだが、3クラス以上で悪意ある汚染下に計算効率的なPAC学習アルゴリズムがあるかは未解明だった。本論文はこれに取り組む。"),
    "2605.18661v1": (
        "自動研究のためのAI——ロードマップと利用ガイド",
        "完全自動システムがわずか15ドルで論文を生成でき、長期エージェントが実験から執筆まで担う時代に。その生産性の前進が、捏造や誤りの見落としという研究の完全性の問題を露わにすると分析する。"),
    "2605.18657v1": (
        "KairosHope: 二重記憶構造による専門分類向けの次世代時系列基盤モデル",
        "時系列基盤モデルは汎用予測で成功するが専門的分類への適応は二次アテンションの計算ボトルネックで制約される。アテンションを二重記憶系に置き換えるHOPEブロックを導入する。"),
    "2605.18656v1": (
        "差分プライバシー連合学習の統計的限界と効率的アルゴリズム",
        "差分プライバシー下の連合M推定で、推定精度・プライバシー・通信コストのトレードオフを研究。FedAvg推定量で初期化を改善したFedSGDであるFedHybridを提案する。"),
}

# ─── New HN / Reddit / GitHub / blog items (url → title_ja, summary_ja) ───
new_url_map = {
    # ── HN ──
    "https://simonwillison.net/2026/May/19/5-minute-llms/": (
        "直近6か月のLLMを5分で——Simon Willisonの総まとめ",
        "ここ半年のLLMの主要な動きを、信頼される観察者Simon Willison氏が5分で読める形に凝縮した解説。HNで694ポイントを集め、変化の速さを物語る。"),
    "https://andonlabs.com/blog/andon-fm": (
        "AIにラジオ局を運営させてみた",
        "Andon LabsがAIエージェントに実際のラジオ局(選曲・進行・トーク)を任せた実験記録。エージェントが連続稼働で何ができ、どこで破綻するかを観察する。"),
    "https://krebsonsecurity.com/2026/05/cisa-admin-leaked-aws-govcloud-keys-on-github/": (
        "CISAの管理者がAWS GovCloudの鍵をGitHubに流出",
        "米サイバーセキュリティ機関CISAの管理者が、政府向けクラウドAWS GovCloudのアクセス鍵を誤って公開GitHubリポジトリに流出させた事案をKrebsが報じる。"),
    "https://cursor.com/blog/composer-2-5": (
        "Cursorが新コーディングモデルComposer 2.5を発表",
        "コードエディタCursorが自社のコーディングモデルComposer 2.5を公開。エージェント的なコーディングの速度と精度の向上を謳う。"),
    "https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/": (
        "Gemini 3.5——行動を伴うフロンティア知能",
        "GoogleがI/O 2026でGemini 3.5を発表。単に答えるだけでなく、エージェント的にタスクを実行する『行動を伴う知能』を前面に打ち出す。"),
    "https://walkinglabs.github.io/learn-harness-engineering/en/": (
        "ハーネスエンジニアリングを学ぶ",
        "AIエージェントを動かす『ハーネス』(足回りの基盤)を設計する技術を体系的に学ぶための教材サイト。"),
    "https://spectrum.ieee.org/voice-ai-audio-attacks": (
        "音声AIシステムは隠れた音声攻撃に脆弱",
        "人間には聞き取れない形で埋め込まれた音声指示によって音声AIシステムを操作できる脆弱性を、IEEE Spectrumが報じる。"),
    "https://www.wsj.com/tech/ai/the-american-rebellion-against-ai-is-gaining-steam-94b72529": (
        "AIへの米国の『反乱』が勢いを増している",
        "雇用不安や生成物への不信を背景に、米国でAIへの反発・抵抗が広がっている現象をWSJが取材。卒業式でのブーイングなど世論の変化を伝える。"),
    "https://www.wheresyoured.at/ai-is-too-expensive/": (
        "AIは高すぎる",
        "Ed Zitron氏が、AI企業の収益とコスト構造を細かく分析し、現在のAIブームが経済的に持続不可能だと論じる長文記事。"),
    "https://gizmodo.com/the-worst-leak-that-ive-witnessed-u-s-cybersecurity-agency-leaves-its-digital-keys-out-in-public-on-github-2000760330": (
        "米サイバー機関、デジタルの鍵を公開状態でGitHubに放置",
        "CISAのAWS鍵流出について、Gizmodoが『これまで見た中で最悪の流出』との関係者の声とともに報じる。"),
    "https://apnews.com/article/ai-college-commencement-anxiety-boo-35aec9bac660eaeb05c5b8d392db2cac": (
        "卒業生がAI礼賛のはなむけにブーイング",
        "複数の大学の卒業式で、AIを称えるスピーチに学生がブーイングする現象をAPが取材。雇用不安を抱える世代の反発が表面化している。"),
    # ── Reddit ──
    "https://www.reddit.com/r/artificial/comments/1th2m6p/whats_the_most_useful_thing_an_llm_does_for_you/": (
        "文章・コード作成以外でLLMが一番役立つことは? [r/artificial]",
        "文章生成やコーディング以外で、LLMが実生活で本当に役立っている使い方を募るスレッド。220件の実用談義が集まった。"),
    "https://www.reddit.com/r/artificial/comments/1tgy0j4/cloudflare_just_published_what_they_found_after/": (
        "Cloudflareが自社50超のリポジトリにAnthropicのMythos Previewを走らせた結果 [r/artificial]",
        "CloudflareがAnthropicのセキュリティ解析ツール『Mythos Preview』を自社の50を超えるリポジトリに適用し、その発見を公開したという投稿。"),
    "https://www.reddit.com/r/MachineLearning/comments/1the441/a_simple_solution_to_improve_broken_peer_review/": (
        "AI学会の壊れた査読制度を改善する簡単な解決策 [R]",
        "AI系学会の査読の質の低下に対し、シンプルな改善案を提案する投稿。"),
    "https://www.reddit.com/r/artificial/comments/1thvyif/give_back_my_emdashes/": (
        "私のem-dashを返して [r/artificial]",
        "AIがem-dash(—)を多用するため、人間が使うと『AIが書いた』と疑われてしまう、という嘆きの投稿。"),
    "https://www.reddit.com/r/MachineLearning/comments/1thb8xf/how_to_get_rejected_by_ieee_tpami_with_excellent/": (
        "『優』評価でもIEEE T-PAMIに落ちる方法 [D]",
        "高い査読スコアを得ても権威ある論文誌に却下された経験を巡る、皮肉混じりの議論スレッド。"),
    "https://www.reddit.com/r/MachineLearning/comments/1th4po3/released_a_free_98m_doc_indic_multilingual_corpus/": (
        "980万文書のインド系多言語コーパスを無償公開 [P]",
        "ヒンディー・ベンガル・タミル・テルグなど10言語超を含む980万文書のコーパスを、CC0ライセンスでHugging Faceに公開した告知。"),
    "https://v.redd.it/56ct17atm12h1": (
        "Claude DesignとElevenLabsで1ドル未満で作った解説動画 [r/artificial]",
        "Claude DesignとElevenLabsを組み合わせ、1ドル未満のコストで解説動画を制作したという作例の投稿。"),
    "https://www.reddit.com/r/artificial/comments/1th1jkt/the_just_add_more_compute_argument_for_ai/": (
        "『計算を増やせばいい』というAI推論論はもう疲れる [r/artificial]",
        "AIの推論能力を『計算資源を足せば解決する』とする主張への疲労感を綴り、議論を呼んだスレッド。"),
    "https://www.reddit.com/r/artificial/comments/1th1v4h/elon_musk_will_appeal_to_the_ninth_circuit/": (
        "イーロン・マスク、第9巡回区控訴裁に控訴へ [r/artificial]",
        "OpenAI訴訟の敗訴を受け、マスク氏が第9巡回区控訴裁判所に控訴する意向を示したことを伝える投稿。"),
    "https://www.reddit.com/r/artificial/comments/1thrz6z/i_think_people_are_underestimating_how_quickly/": (
        "AI生成コンテンツがネットに溶け込む速さを皆過小評価している [r/artificial]",
        "AI生成のテキストや画像が見分けられないままネット上に浸透していく速度を、人々が軽視しているとの問題提起。"),
    "https://www.reddit.com/r/MachineLearning/comments/1thofoe/what_do_you_think_about_tabular_foundation_models/": (
        "表形式基盤モデルをどう思うか [D]",
        "表形式データ向けの基盤モデルの実用性や将来性を巡る議論スレッド。"),
    # ── GitHub ──
    "https://github.com/multica-ai/andrej-karpathy-skills": (
        "andrej-karpathy-skills: Karpathyの知見に基づくCLAUDE.md",
        "Andrej Karpathy氏のLLMコーディングの落とし穴に関する観察をまとめ、Claude Codeの挙動を改善する単一のCLAUDE.mdファイル。1日で約1900スターを集めた。"),
    "https://github.com/rohitg00/agentmemory": (
        "agentmemory: AIコーディングエージェント向けの永続メモリ",
        "実世界ベンチマークに基づくと謳う、AIコーディングエージェント用の永続的メモリ実装。文脈の保持・再利用を狙う。"),
    "https://github.com/obra/superpowers": (
        "superpowers: 機能するエージェント的スキルのフレームワーク",
        "エージェント的なスキルのフレームワークと、それに基づくソフトウェア開発手法を提供するツール。"),
    "https://github.com/msitarzewski/agency-agents": (
        "agency-agents: AIエージェントで作る完全な『代理店』",
        "フロントエンドの達人からRedditコミュニティ運用の手練れまで、人格と手順を持つ専門特化のAIエージェント群を揃えたセット。"),
    "https://github.com/rtk-ai/rtk": (
        "rtk: 開発コマンドのLLMトークン消費を60-90%削減するCLIプロキシ",
        "一般的な開発コマンドのLLMトークン消費を60-90%削減すると謳う、Rust製の依存ゼロな単一バイナリのCLIプロキシ。"),
    "https://github.com/HKUDS/ViMax": (
        "ViMax: 監督・脚本・制作を一手に担うエージェント的動画生成",
        "監督・脚本家・プロデューサー・動画生成器を一体化した、エージェント的な動画生成システム。"),
    "https://github.com/anthropics/claude-plugins-official": (
        "claude-plugins-official: Claude Code公式プラグインディレクトリ",
        "Anthropicが管理する、高品質なClaude Codeプラグインの公式ディレクトリ。"),
    # ── blogs ──
    "https://huggingface.co/blog/allenai/olmoearth-v1-1": (
        "OlmoEarth v1.1: より効率的な地球観測モデル群",
        "AllenAIの地球観測基盤モデルOlmoEarthの効率を改善した新版v1.1。"),
    "https://blog.google/innovation-and-ai/technology/developers-tools/google-io-2026-collection/": (
        "Google I/O 2026",
        "Google I/O 2026での発表をまとめたコレクションページ。Gemini 3.5や検索のAI化など今年の主要発表が並ぶ。"),
    "https://blog.google/products-and-platforms/products/search/ai-mode-us-insights/": (
        "AIモードが米国の検索の仕方をどう変えているか",
        "Google検索の『AIモード』が米国ユーザの検索行動をどう変えたかを、利用データとともに紹介する記事。"),
    "https://blog.google/products-and-platforms/products/workspace/workspace-updates/": (
        "Google Workspaceで作業をこなす新しい方法",
        "Google WorkspaceにI/O 2026で追加された、AIによる作成・タスク遂行の新機能の紹介。"),
    "https://blog.google/innovation-and-ai/sundar-pichai-io-2026/": (
        "I/O 2026: エージェント的Geminiの時代へようこそ",
        "スンダー・ピチャイ氏によるI/O 2026の基調メッセージ。エージェント的なGeminiの時代の到来を告げる。"),
    "https://blog.google/products-and-platforms/products/search/search-io-2026/": (
        "AI検索の新時代",
        "Google検索がAIによって生まれ変わる『新時代』を打ち出す発表。検索エンジンの最良とAIの最良を組み合わせると謳う。"),
    "https://blog.google/products-and-platforms/products/google-one/google-ai-subscriptions/": (
        "I/O 2026発、Google AIサブスクの刷新",
        "I/O 2026に合わせて発表された、Google AIサブスクリプションの新機能・特典のまとめ。"),
    "https://openai.com/index/advancing-content-provenance": (
        "OpenAI、AIコンテンツの来歴技術を前進",
        "OpenAIがContent Credentials・SynthID・検証ツールを通じて、AI生成メディアの識別と信頼を支援する取り組みを発表。"),
    "https://huggingface.co/blog/ettin-reranker": (
        "Ettinリランカー・ファミリーを発表",
        "検索結果の再順位付け(リランキング)を行うモデル群Ettinの紹介。"),
}

# ─── Apply translations ───
for it in d["sources"].get("arxiv", []):
    tj = arxiv_map.get(it.get("id"))
    if tj:
        it["title_ja"], it["summary_ja"] = tj

for src in ("hn", "reddit", "github", "blogs"):
    for it in d["sources"].get(src, []):
        url = it.get("url")
        tj = new_url_map.get(url) or prev_url.get(url)
        if tj and tj[0]:
            it["title_ja"], it["summary_ja"] = tj

# ─── Highlights (5 fresh picks for 2026-05-19) ───
d["highlights"] = [
    {
        "source": "blogs",
        "title": "Gemini 3.5: frontier intelligence with action (Google I/O 2026)",
        "title_ja": "Gemini 3.5発表——Google I/O 2026は『行動するAI』を前面に",
        "url": "https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/",
        "hot_take_ja": "GoogleはI/O 2026の旗印を『エージェント的Geminiの時代』に定めた。Gemini 3.5のキャッチコピーは『行動を伴うフロンティア知能』——もう賢く答えるだけでは売りにならず、勝負どころは『代わりにやってくれるか』に移った。検索もWorkspaceもまるごとAIエージェントに作り替える、その本気度が見える基調だ。",
        "detail_ja": "Googleは年次開発者会議I/O 2026で、新フラッグシップAIモデルGemini 3.5を発表した。スンダー・ピチャイCEOの基調メッセージは『エージェント的Geminiの時代へようこそ』であり、Gemini 3.5自体も『行動を伴うフロンティア知能(frontier intelligence with action)』と位置づけられた。ここでの『行動』とは、ユーザの質問に答えるだけでなく、複数ステップのタスクを自分で計画・実行するエージェント的な能力を指す。発表は単体のモデルにとどまらず、Google検索の『AIモード』の全面刷新、Google Workspaceでの作成・タスク遂行機能、Google AIサブスクリプションの再編まで広範に及び、Googleが主力製品をまるごとエージェント時代向けに作り替えようとしていることがうかがえる。高速・低コスト版のGemini 3.5 Flashも同時に提供され、用途に応じた使い分けを想定している。背景には、OpenAIやAnthropicと並ぶ最先端モデル競争の激化がある。とりわけ『単に賢いか』から『実際にタスクをこなせるか(エージェント性能)』へと評価軸が移りつつあり、各社のメッセージングはそろって『エージェント』に収束している。一方で『行動するAI』という宣伝文句は、エージェントが自律的に操作を行うときの信頼性・安全性・誤操作のリスクという未解決の課題も同時に背負う。ベンチマーク上の数値は各社の公表値であり、実運用での信頼性は独立した検証を待つ必要がある点には注意したい。",
        "detail_en": "At its annual developer conference, Google I/O 2026, Google announced its new flagship AI model, Gemini 3.5. CEO Sundar Pichai's keynote message was 'Welcome to the agentic Gemini era,' and Gemini 3.5 itself was positioned as 'frontier intelligence with action.' Here, 'action' refers to agentic capability — not just answering a user's question, but planning and executing multi-step tasks on its own. The announcements went well beyond a single model: a full revamp of Google Search's 'AI Mode,' new creation and task-completion features in Google Workspace, and a reorganization of Google AI subscriptions — signaling that Google is rebuilding its core products wholesale for the agentic era. A faster, lower-cost Gemini 3.5 Flash variant was offered alongside it, intended for use-case-dependent selection. The backdrop is intensifying competition at the frontier alongside OpenAI and Anthropic. In particular, the axis of evaluation is shifting from 'is it smart' to 'can it actually get tasks done' (agentic performance), and every company's messaging is converging on 'agents.' At the same time, the 'AI that acts' slogan also carries unresolved challenges around the reliability, safety, and risk of mis-operation when an agent autonomously takes actions. Note that benchmark figures are vendor-reported, and real-world reliability awaits independent verification.",
        "key_points_ja": [
            "GoogleがI/O 2026でGemini 3.5を発表",
            "テーマは『エージェント的Geminiの時代』",
            "『行動を伴う知能』——多段タスクの自律実行を強調",
            "検索AIモード・Workspace・サブスクも全面刷新",
            "高速・低コスト版のGemini 3.5 Flashも提供",
            "評価軸が『賢さ』から『タスク遂行』へ移行",
        ],
        "key_points_en": [
            "Google unveils Gemini 3.5 at I/O 2026",
            "Theme: 'the agentic Gemini era'",
            "'Intelligence with action' — autonomous multi-step tasks",
            "Search AI Mode, Workspace, subscriptions all revamped",
            "A fast, low-cost Gemini 3.5 Flash also offered",
            "Evaluation shifts from 'smart' to 'gets tasks done'",
        ],
    },
    {
        "source": "reddit",
        "title": "For the first time in years, ChatGPT falls to second place behind Anthropic's Claude",
        "title_ja": "数年ぶり——ChatGPTが2位に転落、首位はAnthropicのClaude",
        "url": "https://www.reddit.com/r/fivethirtyeight/comments/1tg0i25/for_the_first_time_in_years_chatgpt_falls_to/",
        "hot_take_ja": "生成AIの代名詞だったChatGPTが、ある集計で初めて2位に落ちた。抜いたのはAnthropicのClaude。新規ARR、アプリDL、法人採用、DAUと、勢いを測る指標が軒並み入れ替わったという。総量ではまだChatGPTが巨大でも、『どっちが伸びているか』の答えが変わった——これが効いてくる。",
        "detail_ja": "数年にわたり生成AI市場の象徴的存在だったOpenAIのChatGPTが、ある市場分析でついに2位に後退し、首位をAnthropicのClaudeに譲った、という話がRedditで大きく拡散した。投稿によれば、ChatGPTが2位に落ちたのは単一の指標ではなく、新規純増ARR(年間経常収益)、モバイルアプリのダウンロード数、法人での採用、デイリーアクティブユーザー数、年換算売上など、勢いを測る複数の主要指標にわたるとされる。ここで重要なのは『総量』と『勢い』の区別だ。利用者総数や累積収益といったストックの面では、ChatGPTは依然として圧倒的な規模を持つ可能性が高い。だが『新規』『純増』を測るフロー指標で逆転が起きているなら、それは市場の重心がどちらに動いているかを示すシグナルになる。Anthropicは特にコーディング支援や法人・開発者向け用途で評価を高めてきており、この種の用途は収益性と定着率が高い。一方でこうした集計は出典・指標の定義・対象期間によって結論が変わりやすく、ひとつの分析を鵜呑みにするのは禁物だ。それでも、長らく『生成AI=ChatGPT』だった構図が崩れ、複数の強豪が首位を争う多極的な市場になったこと自体は、注目に値する転換点である。",
        "detail_en": "A claim that OpenAI's ChatGPT — for years the symbolic face of the generative AI market — has finally slipped to second place, ceding the lead to Anthropic's Claude, spread widely on Reddit. According to the post, ChatGPT's drop to second is not on a single metric but across several key momentum indicators: net new ARR (annual recurring revenue), mobile app downloads, business adoption, daily active users, and annualized revenue. The important distinction here is between 'total volume' and 'momentum.' On stock measures such as total user count or cumulative revenue, ChatGPT very likely still holds an overwhelming scale. But if a reversal is happening on flow metrics that measure 'new' and 'net new,' that is a signal of which way the market's center of gravity is moving. Anthropic has built its reputation especially in coding assistance and enterprise/developer use cases — segments with high profitability and retention. At the same time, such aggregations can shift conclusions depending on the source, the definition of each metric, and the time window, so one analysis should not be taken at face value. Even so, the breakdown of the long-standing 'generative AI = ChatGPT' framing into a multipolar market where several strong players contend for the lead is itself a notable turning point.",
        "key_points_ja": [
            "ある集計でChatGPTが数年ぶりに2位へ後退",
            "首位を奪ったのはAnthropicのClaude",
            "新規ARR・DL数・法人採用・DAUなど複数指標で逆転",
            "総量ではChatGPTがなお巨大な可能性",
            "Anthropicはコーディング・法人用途で評価を獲得",
            "『生成AI=ChatGPT』の単極構図が崩れた転換点",
        ],
        "key_points_en": [
            "In one analysis, ChatGPT falls to 2nd after years",
            "Anthropic's Claude takes the top spot",
            "Reversal across net new ARR, downloads, adoption, DAU",
            "ChatGPT likely still huge on total volume",
            "Anthropic earns trust in coding and enterprise use",
            "A turning point: the ChatGPT monopoly framing breaks",
        ],
    },
    {
        "source": "hn",
        "title": "The last six months in LLMs in five minutes (Simon Willison)",
        "title_ja": "直近6か月のLLMを5分で——Simon Willisonの総まとめ",
        "url": "https://simonwillison.net/2026/May/19/5-minute-llms/",
        "hot_take_ja": "LLMの世界は、半年も経つと『何が起きたか』を誰かにまとめてもらわないと追えない。Simon Willisonの『6か月を5分で』がHN首位に立った事実こそ、この分野の異常な速度の証明だ。情報の供給より、整理する人の価値が上がっている。",
        "detail_ja": "ソフトウェア開発者でAI分野の観察者として知られるSimon Willison氏が、『直近6か月のLLMを5分で』と題した総まとめを公開し、Hacker Newsで694ポイントを集めて首位に立った。内容は、ここ半年に起きたLLM関連の主要な動き——新モデルのリリース、エージェント的なコーディングツールの台頭、価格competition、マルチモーダルやコンテキスト長の拡大など——を、短時間で俯瞰できるよう凝縮したものだ。注目すべきは、この記事の人気それ自体が示すメタな事実である。LLMの分野は変化が速すぎて、たった6か月でも専門家でなければ全体像を見失う。だからこそ『信頼できる誰かが要点を整理してくれること』に高い価値が生まれる。Willison氏は長年、過度な誇張も過度な悲観もせず、自分で実際に試した一次情報に基づいて淡々と記録してきた人物であり、その『キュレーターとしての信頼』がこの記事の価値を支えている。情報そのものは無料で大量に出回る時代に、希少なのはむしろ取捨選択と文脈づけだ。AIニュースを毎日追うことの難しさを感じている読者にとって、半年単位の定点観測は、個々の発表を追うのとは別種の見通しを与えてくれる。逆に言えば、この『5分のまとめ』が話題になること自体が、いまのAI業界の情報過多と加速の症状そのものだといえる。",
        "detail_en": "Simon Willison, a software developer well known as an observer of the AI field, published a roundup titled 'The last six months in LLMs in five minutes,' which reached the top of Hacker News with 694 points. The piece condenses the major LLM-related developments of the past half year — new model releases, the rise of agentic coding tools, price competition, expansions in multimodality and context length — into a form you can survey quickly. What is notable is the meta-fact the article's popularity itself demonstrates. The LLM field moves so fast that even six months is enough for a non-specialist to lose the big picture. That is precisely why high value accrues to 'a trusted someone organizing the key points.' Willison has for years recorded developments plainly, based on first-hand information he actually tested himself, without excessive hype or excessive doom — and that 'trust as a curator' underpins the article's value. In an era when information itself circulates freely and in vast quantities, what is scarce is rather selection and contextualization. For readers who feel the difficulty of tracking AI news daily, a half-year fixed-point observation offers a kind of perspective different from following individual announcements. Conversely, the very fact that this 'five-minute summary' becomes a talking point is itself a symptom of the current AI industry's information overload and acceleration.",
        "key_points_ja": [
            "Simon Willisonが半年のLLM動向を5分で総括",
            "新モデル・エージェント的コーディング等を凝縮",
            "記事がHN首位に——分野の速度を象徴",
            "希少なのは情報でなく取捨選択と文脈づけ",
            "誇張せぬ一次情報の記録者としての信頼が価値",
            "『5分まとめ』の人気自体が情報過多の症状",
        ],
        "key_points_en": [
            "Simon Willison sums up 6 months of LLMs in 5 minutes",
            "Condenses new models, agentic coding, and more",
            "Article tops HN — symbolizing the field's speed",
            "Scarce resource: not info but selection and context",
            "Value rests on trust as a non-hype first-hand recorder",
            "The summary's popularity is itself an overload symptom",
        ],
    },
    {
        "source": "arxiv",
        "title": "Predictable Confabulations: Factual Recall by LLMs Scales with Model Size and Topic Frequency",
        "title_ja": "予測可能な作話——LLMの事実想起はモデルサイズと話題頻度でスケールする",
        "url": "https://arxiv.org/abs/2605.18732v1",
        "hot_take_ja": "LLMが事実をでっち上げる『作話』は、ランダムな事故ではなく予測できる現象だった。モデルの大きさと、その話題が訓練データにどれだけ出てきたか——この2つだけで想起の質の6割が説明できる。つまり『何を聞けばハルシネーションするか』は、事前にかなり当てられる。",
        "detail_ja": "LLM全体の性能はスケーリング則に従うことが知られているが、『事実の想起』の正確さをモデルサイズと訓練データの構成の両方に結びつけたスケーリング則はこれまで存在しなかった。この研究はそこに踏み込んだ。著者らは4つのモデルファミリーにわたる38のモデルを、8,900件を超える学術文献の参照情報で評価した。文献参照を選んだのは、自動の参照検証システムで『その引用が実在し正確か』を機械的に判定できるからだ。その結果、想起の質は、モデルのパラメータ数と訓練データ中での話題の出現量という2つの量の『対数線形結合』に対してシグモイド曲線を描くことが分かった。驚くべきはその説明力で、このたった2つの変数だけで16の密モデルにわたる性能分散の60%を説明し、同一ファミリー内に限れば74-94%にまで上がる。著者らは、この関数形が『重ね合わせ(superposition)』に着想を得た理論——少ない頻度の事実は重ね合わされた表現の中で干渉を受けやすい——と整合的だと論じる。実務的な含意は大きい。LLMが事実をでっち上げる『作話(コンファビュレーション)』は、これまで予測不能なランダムエラーのように扱われがちだったが、本研究はそれが体系的で予測可能であることを示した。つまり、ある話題についてどのサイズのモデルなら信頼できるか、どのあたりで作話が始まるかを、事前にある程度見積もれる。マイナーな話題ほど、そして小さいモデルほど作話が起きやすい——という直感を、定量的な法則として裏づけた成果である。",
        "detail_en": "While scaling laws are known to govern overall LLM performance, no scaling law had previously linked the accuracy of 'factual recall' to both model size and the composition of training data. This study addresses exactly that gap. The authors evaluated 38 models across four model families on over 8,900 scholarly references. They chose scholarly references because an automated reference-verification system can mechanically judge whether a citation actually exists and is accurate. The result: recall quality follows a sigmoid curve in the 'log-linear combination' of two quantities — the model's parameter count and how much the topic is represented in the training data. Strikingly, these two variables alone explain 60% of the performance variance across 16 dense models, rising to 74-94% within a single family. The authors argue this functional form is consistent with a 'superposition'-inspired account, in which low-frequency facts are more susceptible to interference within superposed representations. The practical implications are significant. 'Confabulation' — where an LLM fabricates facts — has tended to be treated as an unpredictable, random error, but this study shows it is systematic and predictable. That means one can estimate in advance, to some degree, which model size can be trusted on a given topic and where confabulation begins. The work backs the intuition that the more obscure the topic, and the smaller the model, the more likely confabulation becomes — turning it into a quantitative law.",
        "key_points_ja": [
            "事実想起をモデルサイズと話題頻度で結ぶ初の法則",
            "38モデルを8,900件超の文献参照で評価",
            "想起の質は2変数の対数線形結合のシグモイド",
            "2変数だけで分散の60%、同系列で74-94%を説明",
            "『重ね合わせ』理論——稀な事実は干渉を受けやすい",
            "作話はランダムでなく体系的・予測可能と示す",
        ],
        "key_points_en": [
            "First law linking factual recall to size and topic frequency",
            "38 models tested on 8,900+ scholarly references",
            "Recall quality: a sigmoid in a log-linear combination",
            "Two variables explain 60% variance, 74-94% within a family",
            "Superposition account: rare facts suffer interference",
            "Confabulation is systematic and predictable, not random",
        ],
    },
    {
        "source": "hn",
        "title": "The American rebellion against AI is gaining steam",
        "title_ja": "AIへの米国の『反乱』が勢いを増している",
        "url": "https://www.wsj.com/tech/ai/the-american-rebellion-against-ai-is-gaining-steam-94b72529",
        "hot_take_ja": "卒業式でAI礼賛のスピーチがブーイングを浴び、『AIは高すぎる』という記事がHN上位に並ぶ。業界が『不可避だ』と語るほど、世論はその物言いに反発している。AIへの抵抗は、もはや一部の懐疑論ではなく、一つの社会的うねりになりつつある。",
        "detail_ja": "ウォール・ストリート・ジャーナルは『AIへの米国の反乱が勢いを増している』と題し、米国社会でAIへの反発・抵抗が広がっている現象を報じた。同じ日のHacker Newsには、複数の大学の卒業式でAIを称えるスピーチに学生がブーイングを浴びせたというAP・NBCの報道や、Ed Zitron氏による『AIは高すぎる』——AI企業の収益とコスト構造を分析し現在のブームが経済的に持続不可能だと論じる長文——が同時に上位に並んだ。これらは別々の出来事だが、束ねると一つの空気が見えてくる。第一に雇用不安。多くの企業が人員削減の理由として入門レベルの職をAIで代替できることを挙げており、特に2026年卒の世代はその矢面に立っている。卒業式での祝辞は、AIの恩恵を語る業界の重鎮と、その恩恵の裏で職を失いつつある若者との溝が可視化される象徴的な場になった。第二にコストと持続可能性への疑念。Zitron氏のような論者は、AIへの巨額投資が見合うリターンを生んでいるのかを問う。第三に生成物への不信——AIが書いた文章や画像がネットに溶け込むことへの警戒感だ。注目すべきは、業界がAIを『不可避(inevitable)』だと繰り返すほど、その断定的な物言い自体が反発を招いている点だ。技術そのものへの評価とは別に、『選択の余地なく押しつけられる』という感覚が抵抗を生む。むろん、AIの導入は実際には急速に進んでおり、反発と普及は同時に起きている。だが、AIへの懐疑が一部の専門家の議論から一般世論のうねりへと移りつつあること自体が、2026年春の重要な社会的シグナルである。",
        "detail_en": "The Wall Street Journal reported, under the headline 'The American rebellion against AI is gaining steam,' on the spreading pushback and resistance to AI in American society. On the same day, Hacker News featured, side by side near the top, AP and NBC reports of students booing AI-praising speeches at multiple university commencements, and Ed Zitron's long essay 'AI is too expensive,' which analyzes AI companies' revenue and cost structures and argues the current boom is economically unsustainable. These are separate events, but bundled together they reveal a single mood. First, job anxiety. Many companies cite the ability to replace entry-level roles with AI as a reason for headcount cuts, and the class of 2026 in particular stands in the firing line. Commencement addresses became a symbolic stage where the gap is made visible — between industry leaders touting AI's benefits and young people losing jobs behind those benefits. Second, doubt about cost and sustainability. Commentators like Zitron question whether the enormous investment in AI is generating commensurate returns. Third, distrust of AI-generated output — wariness about AI-written text and images blending into the web. What is notable is that the more the industry repeats that AI is 'inevitable,' the more that very assertiveness invites backlash. Apart from any judgment of the technology itself, the feeling of 'being forced on us with no choice' breeds resistance. Of course, AI adoption is in fact advancing rapidly, and backlash and uptake are happening at once. But the shift of AI skepticism from a debate among a few experts toward a groundswell of general public opinion is itself an important social signal of spring 2026.",
        "key_points_ja": [
            "WSJが『AIへの米国の反乱が勢いを増す』と報道",
            "卒業式でAI礼賛スピーチへのブーイングが続出",
            "『AIは高すぎる』論——持続可能性への疑念",
            "雇用不安——入門職をAIに奪われる2026年卒世代",
            "業界が『不可避』と言うほど反発が強まる構図",
            "AI懐疑が専門家の議論から世論のうねりへ",
        ],
        "key_points_en": [
            "WSJ reports 'rebellion against AI is gaining steam'",
            "Students keep booing AI-praising commencement speeches",
            "'AI is too expensive' — doubts over sustainability",
            "Job anxiety — class of 2026 losing entry-level roles to AI",
            "The more industry says 'inevitable,' the more backlash",
            "AI skepticism shifts from expert debate to public mood",
        ],
    },
]

OUT.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT}")
print(f"Highlights: {len(d['highlights'])}")
for src, items in d["sources"].items():
    enriched = sum(1 for it in items if it.get("title_ja"))
    print(f"  {src}: {enriched}/{len(items)} enriched")
