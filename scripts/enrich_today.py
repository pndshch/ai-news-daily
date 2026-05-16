#!/usr/bin/env python3
"""Enrichment for 2026-05-16 (fresh page).

Reads raw-2026-05-16.json, adds Japanese title/summary to every item,
selects 5 highlights with bilingual deep-dive material, and writes
data/2026-05-16.json.
"""
import json
from pathlib import Path

DATE = "2026-05-16"
ROOT = Path(__file__).resolve().parent.parent
SRC_RAW = ROOT / "data" / f"raw-{DATE}.json"
OUT = ROOT / "data" / f"{DATE}.json"

d = json.loads(SRC_RAW.read_text(encoding="utf-8"))
d["date"] = DATE

# ─── arXiv: id → (title_ja, summary_ja) ───
arxiv = {
    "2605.15199v1": (
        "EntityBench: 長尺マルチショット動画生成の『登場人物の一貫性』を測るベンチ",
        "実写ナラティブ作品から作った140エピソード(2,491ショット)で、複数カットをまたいだキャラ・物体・場所の一貫性を評価。再登場の間隔が空くほど一貫性が崩れる現状を可視化し、永続メモリ方式EntityMemをベースラインに提示。"),
    "2605.15198v1": (
        "ATLAS: 視覚推論は『エージェント的』か『潜在表現』か——1トークンで両立",
        "推論中に画像を明示生成する手法と内部潜在表現で済ます手法の論争に対し、単一トークンの切り替えで両方を扱う統一フレームを提案。"),
    "2605.15196v1": (
        "RefDecoder: 条件付き動画デコードで視覚生成を強化",
        "潜在拡散モデルのデコーダが無条件のままという構造的非対称性に着目し、デコーダにも条件を入れることで生成品質を改善。"),
    "2605.15195v1": (
        "VGGT-Ω: フィードフォワード3D復元はモデル・データ規模で予測通りスケール",
        "VGGTのようなフィードフォワード復元モデルの品質が、モデルサイズとデータ量に対し予測可能な形でスケールすることを示した研究。"),
    "2605.15193v1": (
        "球面フローマッチング: 潜在空間の幾何を揃えて画像生成を改善",
        "ノイズもVAE潜在も球殻状に分布するのに、直線経路だと殻から外れてしまう問題を指摘。球面に沿った輸送経路で画像生成を改善する。"),
    "2605.15190v1": (
        "RAVEN: 一貫性モデルGRPOによるリアルタイム自己回帰動画外挿",
        "因果的自己回帰動画拡散をリアルタイム配信向けに蒸留する際の品質ギャップを、一貫性モデル＋GRPOで埋める手法。"),
    "2605.15188v1": (
        "FutureSim: 実世界イベントを再生して『適応するエージェント』を評価",
        "新情報が順次到着する動的環境で、エージェントが適応できるかを、実世界の出来事を時系列で再生するシミュレーションで測る。"),
    "2605.15187v1": (
        "Articraft: 関節付き3Dアセットを大規模生成するエージェント型システム",
        "可動部を持つ3Dオブジェクトの学習データ不足を、LLMを使って関節付きアセットを大量生成することで解消するパイプライン。"),
    "2605.15186v1": (
        "VGGT-Edit: 残差場予測によるフィードフォワード3Dシーン編集",
        "フィードフォワード3D復元モデルが苦手としていたシーン編集を、残差場の予測で1パス実現する。"),
    "2605.15185v1": (
        "幾何一貫性のための定量的な動画ワールドモデル評価",
        "生成動画が物理的に妥当な3D構造・運動を作れているかを、人間や学習済み採点器に頼らず定量評価するパイプライン。"),
    "2605.15184v1": (
        "Grepだけで十分か？——エージェントの『ハーネス』が検索を作り変える",
        "LLMエージェントの情報検索性能が、モデル本体よりもツール実行環境(ハーネス)の設計に大きく左右されることを実証的に分析。"),
    "2605.15183v1": (
        "2つのネットワークはいつ『同じ』か——機構解釈のためのテンソル類似度",
        "モデル部品が同じ計算をしているかを検証するため、挙動ベースでも基底ベースでもない、テンソル類似度による新指標を提案。"),
    "2605.15182v1": (
        "Warp-as-History: 1本の学習動画からカメラ制御動画を汎化生成",
        "カメラ専用のエンコーダや制御分岐を学習する代わりに、ワーピング履歴を手がかりに1本の動画から視点制御を汎化する。"),
    "2605.15181v1": (
        "プランからピクセルへ: オープンエンドな画像編集を計画・統括して学習",
        "「広告をもっとベジタリアン向けに」のような抽象的・多段の編集指示を、手作りパイプラインに頼らず計画立案して実行する手法。"),
    "2605.15179v1": (
        "スパースMoEルーティングでマルチ物理基盤モデルの『負の転移』を根絶",
        "異なる偏微分方程式レジームを同時学習すると勾配が衝突し性能が落ちる問題を、スパースなMixture-of-Expertsルーティングで解消。"),
    "2605.15178v1": (
        "SANA-WM: ハイブリッド線形拡散Transformerによる分単位ワールドモデル",
        "2.6Bパラメータのオープンソースワールドモデルで、720p・1分尺の高品質動画をカメラ制御付きで生成。大規模商用モデルに匹敵する品質を効率的に達成。"),
    "2605.15177v1": (
        "OpenDeepThink: Bradley-Terry集約による並列推論",
        "推論を深さ方向に伸ばすのではなく、複数候補を並列サンプリングし、Bradley-Terryモデルで集約して選択ボトルネックを解消。"),
    "2605.15172v1": (
        "MetaBackdoor: 位置エンコーディングをLLMのバックドア攻撃面として悪用",
        "従来の内容ベースのトリガーと異なり、位置エンコーディングを操作してバックドアを仕込む新たな攻撃面を提示。"),
    "2605.15171v1": (
        "証拠推論で実世界の疾患スクリーニングを解釈可能に",
        "医用画像のスクリーニングモデルの低い解釈性と性能を、過去症例を参照する証拠推論の仕組みで同時に改善。"),
    "2605.15168v1": (
        "テキストは『何を』、表は『いつ』を知る——検索拡張マルチモーダルで臨床タイムライン再構築",
        "敗血症など複雑な病態の患者経過を、自由記述の臨床記録と構造化テーブルを整合させて精密なタイムラインに再構築。"),
    "2605.15167v1": (
        "合成レイヤードデザインデータはレイヤー分解に役立つか",
        "生成画像は前景・背景・テキストが平坦に絡み合う問題があり、レイヤー分解学習に合成データが有効かを検証。"),
    "2605.15164v1": (
        "提言: 行動的アシュアランスは、いまガバナンスが要求する安全主張を検証できない",
        "2019〜2026年に成立したAIガバナンス枠組みが要求する『隠れた目的の不在』等の証拠を、行動テストでは原理的に検証できないと論じる立場論文。"),
    "2605.15157v1": (
        "Hand-in-the-Loop: シームレスな介入修正で器用なVLAを改善",
        "高次元の動作空間と接触の多い動作で誤差が累積するVLAモデルを、人間が滑らかに介入修正できる対話的模倣学習で安定化。"),
    "2605.15156v1": (
        "MeMo: モデルとしてのメモリ",
        "事前学習後に固定されるLLMへ、新しいドメイン知識を効率的に取り込むため、メモリ自体を1つのモデルとして扱う仕組み。"),
    "2605.15155v1": (
        "自己蒸留型エージェント強化学習",
        "軌跡単位の粗い報酬しか得られないRLを、トークン単位の密な指導を加えるオンポリシー自己蒸留で補強し、長期相互作用を改善。"),
    "2605.15154v1": (
        "RoSHAP: 安定した特徴寄与のための分布的枠組みとロバスト指標",
        "学習データ分割や乱数シードで揺らぐ特徴寄与度を、分布として捉えてロバストに評価する枠組み。"),
    "2605.15153v1": (
        "Pelican-Unified 1.0: 理解・推論・想像・行動を統合した身体性基盤モデル",
        "単一のVLMを統合理解モジュールとして使い、シーン・指示・行動履歴を共有意味空間にマッピングする初の統合型身体性基盤モデル。"),
    "2605.15152v1": (
        "Widening the Gap: 外れ値注入によるLLM量子化の悪用",
        "FP精度では無害に見えるが、ユーザーが量子化した途端に悪意ある挙動を示すモデルを、外れ値注入でより強力に作れることを示す。"),
    "2605.15141v1": (
        "Causal Forcing++: リアルタイム対話型動画生成のための少ステップAR拡散蒸留",
        "低遅延・ストリーミング・制御可能な動画ロールアウトを、双方向ベースモデルから少ステップAR学生へ蒸留してスケーラブルに実現。"),
    "2605.15138v1": (
        "消しても残る忘却: 回路寄与に基づく『量子化耐性のあるアンラーニング』",
        "4ビット量子化で機械的アンラーニングが巻き戻る問題に対し、回路寄与分析を使い量子化後も忘却が保たれる手法を提案。"),
    "2605.15134v1": (
        "予測可能な失敗を持つMLモデルの学習",
        "実運用規模での失敗頻度を、小さな評価セットの上位失敗から外挿して事前に安全評価する手法。"),
    "2605.15133v1": (
        "連続的介入を扱う因果基盤モデル",
        "介入変数が連続値を取る難しい設定を対象に、観測データから因果効果を推定する基盤モデル。"),
    "2605.15132v1": (
        "APWA: 並列化可能なエージェントワークフローのための分散アーキテクチャ",
        "LLMマルチエージェントが直面する推論・協調・計算スケーリングのボトルネックを、分散アーキテクチャで解消。"),
    "2605.15131v1": (
        "自然な合成: 大規模推論モデルがリアクティブ合成ツールを上回る",
        "論理仕様からハードウェア回路を自動構成するリアクティブ合成を、大規模推論モデルが既存ツールより高性能に解くことを示す。"),
    "2605.15128v1": (
        "MemEye: マルチモーダルエージェント記憶の視覚中心評価フレームワーク",
        "従来の評価はキャプションや文字記録だけで答えられてしまう問題を指摘し、視覚証拠の保持を真に問う評価枠組みを提案。"),
    "2605.15127v1": (
        "米国の留学生は会話AIをどう異文化適応に使っているか",
        "大学の支援体制や非公式ネットワークの隙間を、留学生が会話AIで埋めている実態を調査した研究。"),
    "2605.15122v1": (
        "CoCo-InEKF: 学習した接触共分散による動的・接触豊富な状態推定",
        "脚ロボットの高速運動の状態推定で、二値の接触状態では捉えられない部分接触や滑りを学習共分散で扱う。"),
    "2605.15120v1": (
        "CLOVER: エンドツーエンド自動運転計画の閉ループ価値推定とランキング",
        "単一の記録軌跡を模倣する学習と、ルールベース指標による評価のミスマッチを、閉ループ価値推定とランキングで解消。"),
    "2605.15118v1": (
        "Talk is (Not) Cheap: LLM攻撃ベンチマークの分類体系とカバレッジ監査",
        "STRIDEに基づく4×6のターゲット×手法マトリクスと507葉の分類体系で、既存のLLM攻撃ベンチマークが脅威空間をどれだけ覆っているか監査。"),
    "2605.15116v1": (
        "DriveCtrl: 条件付きSim-to-Real運転動画生成",
        "合成と実世界の運転動画のドメインギャップを縮め、自動運転学習用のラベル付きデータを実用的に生成。"),
    "2605.15113v1": (
        "言語フィードバックからの学習: 変分方策蒸留",
        "検証可能報酬RLの疎な報酬による探索ボトルネックを、言語フィードバックを密なトークン信号に変換する変分方策蒸留で緩和。"),
    "2605.15110v1": (
        "文字列類似度計算・分類のための統計的特徴量の提案と検証",
        "画像処理で使われる共起行列・ランレングス行列を、単語・文・コード・テキストの類似度計算へ応用する特徴量を提案。"),
    "2605.15109v1": (
        "近傍が重要な理由——エージェント型GraphRAGにおける探索文脈と来歴",
        "知識グラフを探索してから答えるエージェント型GraphRAGで、引用の『忠実さ』をどう担保するかを近傍文脈と来歴の観点で分析。"),
    "2605.15108v1": (
        "オフポリシー評価のためのロギング方策設計",
        "推薦システム等の目標方策の価値を別方策のログから推定するOPEで、推定精度を左右するロギング方策の設計を扱う。"),
    "2605.15104v1": (
        "テキストから音声へ: ツール呼び出しLLMエージェントの再現可能な評価枠組み",
        "テキストベースのツール呼び出しベンチマークを、再アノテーションなしで音声ベースの評価へ変換できるかを検証。"),
    "2605.15102v1": (
        "自己想起思考でマルチターン対話の一貫性を改善",
        "離れたターン間の依存を見失うLLM対話の弱点を、過去の重要情報を自ら想起させる『自己想起思考』で改善。"),
    "2605.15100v1": (
        "双次元一貫性: 適応的推論時スケーリングで予算と品質を両立",
        "サンプリング予算と推論品質のトレードオフを、品質と予算の両面で一貫性を取りながら適応的に最適化。"),
    "2605.15093v1": (
        "CoralLite: 個々のサンゴ虫からサンゴ群体をμCT復元",
        "数百年生きるサンゴ群体の生育史を、個々のコラライト(サンゴ虫の骨格)からμCTで復元する手法。"),
    "2605.15088v1": (
        "SAGE3D: ソフト誘導アテンションとグラフ励起による3D点群コーナー検出",
        "航空LiDAR点群のコーナー検出を、階層型エンコーダ・デコーダとグラフ励起を組み合わせたTransformerで実現。"),
    "2605.15085v1": (
        "データから行動へ: AIで製油所最適化を加速",
        "巨大な線形計画モデルの結果を解釈し現場適用する難しさに対し、AIで意思決定を支援するアプローチ。"),
}

for it in d["sources"].get("arxiv", []):
    tj = arxiv.get(it.get("id"))
    if tj:
        it["title_ja"], it["summary_ja"] = tj

# ─── HN / Reddit / GitHub / blogs: url → (title_ja, summary_ja) ───
url_map = {
    # HN
    "https://twitter.com/mitchellh/status/2055380239711457578": (
        "「いま丸ごと“AI精神病”に陥っている会社が確実に存在する」",
        "HashiCorp創業者Mitchell Hashimoto氏の投稿。AIへの過剰な期待や非現実的な判断に組織ぐるみで取り憑かれた『AI psychosis(AI精神病)』状態の企業が実在する、という指摘がHNで1700超の支持を集めバズった。"),
    "https://www.gutenberg.org/": (
        "Project Gutenberg——着実に良くなり続けている",
        "無料電子書籍の老舗Project Gutenbergへの再評価スレッド。AI学習データの議論が盛り上がる中、人手でキュレートされた公共ドメイン資産の価値が改めて注目された。"),
    "https://github.com/oven-sh/bun/issues/30719": (
        "BunのRust書き換え、「miriの基本チェックを通らず、安全なRustでUBを許す」",
        "JavaScriptランタイムBunのRust移行に対し、安全なRustコードのはずがメモリ未定義動作(UB)を起こしうると指摘するIssue。Rust採用の品質保証を巡る議論を呼んだ。"),
    "https://www.fastcompany.com/91541586/amazon-workers-pressured-to-up-ai-use-extraneous-tasks": (
        "AI利用率を上げろと迫られたAmazon社員、不要なタスクを『でっち上げ』",
        "AI活用のノルマ的なプレッシャーを受けた従業員が、本来不要なタスクをわざわざ作ってAIに通している実態を報じた記事。AI導入の指標化が逆効果になっている例。"),
    "https://turso.tech/blog/the-wonders-of-ai": (
        "Tursoがバグバウンティ制度を廃止",
        "データベース企業Tursoが、AI生成の低品質な脆弱性報告(スロップ)の洪水に耐えかねてバグバウンティを終了。AIが既存のセキュリティ運用を圧迫している象徴的な事例。"),
    "https://kabir.au/blog/the-ctf-scene-is-dead": (
        "フロンティアAIがオープンなCTF形式を壊した",
        "AIモデルがCTF(セキュリティ競技)の問題を高速で解けるようになり、従来のオープン参加型CTFが競技として成立しなくなったという主張のブログ。"),
    "https://github.com/Andyyyy64/whichllm": (
        "Show HN: 自分のハードに最適なローカルLLMをベンチマークでランキング",
        "手元のGPU/メモリ構成を入力すると、動かせるローカルLLMをベンチマーク順に提示してくれるツール。"),
    "https://nvlabs.github.io/Sana/WM/": (
        "SANA-WM: 1分尺720p動画を生成する2.6Bのオープンソースワールドモデル",
        "NVIDIAが公開した2.6Bパラメータの軽量ワールドモデル。カメラ制御付きで720p・1分尺の動画を生成でき、大規模商用モデルに迫る品質をオープンに提供する。"),
    "https://radicle.dev/": (
        "Radicle: Gitの上に構築された主権的コードフォージ",
        "GitHubのような中央集権型ホスティングに依存しない、P2P・自己主権型のコード共有プラットフォーム。"),
    "https://www.fastcompany.com/91542655/bitwarden-scrubs-always-free-and-inclusion-values-from-its-website-as-longtime-execs-step-down": (
        "Bitwarden、サイトから『Always free』と『Inclusion』の文言を削除",
        "パスワードマネージャーBitwardenが、長年の幹部退任に合わせ『常に無料』『包摂』といった企業価値の表現をサイトから削除。方針転換への懸念が広がった。"),
    "https://github.com/chiennv2000/orthrus": (
        "Orthrus-Qwen3: Qwen3で1フォワードあたり最大7.8倍のトークン、出力分布は同一",
        "デュアルビュー拡散による並列トークン生成で、Qwen3の出力分布を変えずに1回の順伝播で最大7.8倍のトークンを得る高速化手法。"),
    "https://www.revswap.ai/": (
        "他のスタートアップとドルを交換し、それを売上に計上",
        "スタートアップ同士が互いの製品を購入し合い『売上』として計上する仕組みを提供するサービス。AIバブル下の見せかけ成長を皮肉る話題に。"),
    "https://github.com/neilsonnn/image-blaster": (
        "Image-blaster: 1枚の画像から3D環境・SFX・メッシュを生成",
        "単一の画像入力から3Dシーン、特殊効果、メッシュを一気に生成するツール。"),
    "https://www.worseonpurpose.com/p/your-power-tools-got-worse-on-purpose": (
        "電動工具はわざと劣化した——DeWalt・Craftsman・Milwaukeeを所有するのは誰か",
        "主要電動工具ブランドの品質低下と寡占的な所有構造を追った記事。AIとは別だがHNで広く議論された。"),
    "https://kingy.ai/ai/too-dangerous-to-release-or-just-too-expensive-the-real-reason-anthropic-is-hiding-its-most-powerful-ai/": (
        "「危険すぎて出せない」のか、それとも「高すぎる」だけか",
        "最強モデルを未公開にする理由は安全性なのかコストなのか、を論じたブログ。AIラボの『安全性』言説への懐疑的な視点。"),
    "https://www.seangoedecke.com/steering-vectors/": (
        "DeepSeek-V4-Flashで、LLMの『ステアリング』が再び面白くなった",
        "DeepSeek-V4-Flashの登場で、ステアリングベクトル(内部表現を操作してモデル挙動を誘導する技術)が再び実用的に注目されているという解説。"),
    "https://github.com/ThroatyMumbo/WinCE64": (
        "WinCE64——N64向けWindows CE 2.11",
        "ニンテンドウ64上でWindows CE 2.11を動かすホビープロジェクト。"),
    "https://github.com/gdevic/FPGA-Calculator": (
        "Verilogでニブル指向CPUを設計し関数電卓を自作",
        "4ビット(ニブル)単位で動くCPUをVerilogで設計し、科学計算電卓を構築したハードウェアプロジェクト。"),
    "https://www.bloomberg.com/news/articles/2026-05-15/us-is-starting-to-see-heavy-job-losses-in-roles-exposed-to-ai": (
        "米国、AIの影響を受けやすい職種で大幅な雇用減が始まる",
        "Bloombergが、AIに代替されやすい職種で米国の雇用が目に見えて減り始めたと報道。AIの労働市場への影響が統計データに表れ始めた節目の記事。"),
    "https://github.com/dtnewman/burn-baby-burn": (
        "Show HN: Burn, baby, burn(トークンを燃やせ)",
        "LLM APIのトークンをわざと大量消費するジョークツール。AIコストの異常な燃焼を皮肉る。"),
    # Reddit
    "https://www.reddit.com/r/MachineLearning/comments/1tdje2d/arxiv_implements_1year_ban_for_papers_containing/": (
        "arXiv、LLM生成エラーが明白な論文に1年の投稿禁止を導入",
        "幻覚した参考文献や結果など、未チェックのLLM生成エラーが明白な論文に対し、arXivが1年間の投稿禁止措置を導入。研究界で大きな反響を呼んだ。"),
    "https://www.pcguide.com/pro/news-pro/recent-poll-shows-that-70-of-americans-dont-want-ai-data-centers-being-built-near-their-homes/": (
        "世論調査: 米国人の70%が自宅近くへのAIデータセンター建設に反対",
        "AIデータセンターの電力・水消費や騒音への懸念から、米国人の7割が近隣建設に反対しているという調査結果。AIインフラ拡大への住民の抵抗を示す。"),
    "https://www.reddit.com/r/MachineLearning/comments/1tens5n/backlash_against_arxivs_proposed_1_year_ban_is/": (
        "arXivの1年禁止案への反発は本当に理解しがたい [議論]",
        "arXivのLLMエラー論文禁止への反発に対し、むしろ反発の方が不可解だと論じる議論スレッド。研究の質をどう守るかを巡る対立。"),
    "https://www.reddit.com/r/artificial/comments/1tebiq4/stanford_studied_51_real_ai_deployments_and_found/": (
        "Stanfordが実AI導入51件を調査、生産性向上71%と40%の差を分析",
        "Stanfordが現実のAI導入51事例を調査し、生産性が大きく上がったグループ(71%)と伸び悩んだグループ(40%)を分けた要因を特定。"),
    "https://www.reddit.com/r/MachineLearning/comments/1tevot1/do_you_agree_with_judea_that_learning_from_data/": (
        "『データからの学習が全てではない』というJudea Pearlの主張に同意するか [議論]",
        "因果推論の大家Judea Pearlの「データ学習だけでは不十分」という主張を巡るML研究者の議論スレッド。"),
    "https://www.reddit.com/r/artificial/comments/1te0p1f/has_anyone_come_across_this_ai_civilisation/": (
        "このAI文明実験を見た人はいる？感想を知りたい",
        "AIエージェントに仮想社会を運営させる『AI文明』実験についての話題スレッド。"),
    "https://www.reddit.com/r/artificial/comments/1tew6gr/we_keep_saying_ai_understands_things_does_it_or/": (
        "AIが物事を『理解する』と言うが、本当か？それとも擬人化のパターンマッチか",
        "AIが『理解している』という表現の妥当性を問い、人間側の擬人化バイアスではないかと議論するスレッド。"),
    "https://www.reddit.com/r/artificial/comments/1te26qi/the_trustoversight_paradox_as_ai_gets_better/": (
        "信頼と監督のパラドックス: AIが良くなるほど人間は本気で監督しなくなる",
        "AIの性能が上がるほど人間が監督を怠るようになるという逆説を論じた投稿。"),
    "https://www.reddit.com/r/MachineLearning/comments/1tedjwo/rocm_with_pytorch_and_pytorch_lightning_seems_to/": (
        "ROCmはPyTorch/PyTorch Lightningでの研究にまだ厳しい [議論]",
        "AMD GPU向けROCmが、研究用途のPyTorchワークフローでまだ実用上の問題を抱えているという体験談スレッド。"),
    "https://www.reddit.com/r/artificial/comments/1tejpmh/techs_push_to_be_the_next_public_utility/": (
        "テック業界の『次の公共インフラ』になろうとする動き",
        "AIや大手テックが電気・水道のような公共インフラの地位を狙う動きを論じた投稿。"),
    "https://www.reddit.com/r/MachineLearning/comments/1teito1/kdd_2026_cycle_2_results_d/": (
        "KDD 2026 Cycle 2 採否結果 [議論]",
        "データマイニング国際会議KDD 2026の第2サイクル採否結果を共有・議論するスレッド。"),
    "https://www.reddit.com/r/MachineLearning/comments/1te2x04/orthrus_memoryefficient_parallel_token_generation/": (
        "Orthrus: デュアルビュー拡散によるメモリ効率の良い並列トークン生成 [研究]",
        "出力分布を保ったまま並列にトークンを生成し、メモリ効率と速度を改善する研究の紹介スレッド。"),
    "https://www.reddit.com/r/artificial/comments/1tedx7o/a_working_multiagent_architecture_in_large/": (
        "大企業で実際に機能するマルチエージェント・アーキテクチャ",
        "大規模企業で実運用に耐えるLLMマルチエージェント構成についての知見共有スレッド。"),
    "https://www.sfchronicle.com/tech/article/tech-jobs-ai-applicants-22261320.php": (
        "AI応募者を見破る新手: 『カエルについて詩を書け』",
        "求人にAIで自動応募してくるボットを、無関係な指示(カエルの詩を書け等)を仕込んで見破る採用側の対抗策を報じた記事。"),
    "https://www.reddit.com/r/MachineLearning/comments/1te0tpg/pinn_is_predicting_trivial_solution_for_stiff_ode/": (
        "PINNが硬いODEで自明解を予測してしまう [議論]",
        "物理情報ニューラルネット(PINN)が、硬い常微分方程式で自明解に収束してしまう問題の相談スレッド。"),
    "https://www.reddit.com/r/artificial/comments/1tdhoxd/adaptive_markdown/": (
        "Adaptive Markdown",
        "読者や文脈に応じて表示を変える『適応的Markdown』のアイデアを紹介する投稿。"),
    "https://www.reddit.com/r/artificial/comments/1tevqds/most_enterprises_are_trying_to_scale_ai_on_top_of/": (
        "多くの企業は『組織的な混乱』の上にAIをスケールさせようとしている",
        "業務プロセスが整理されないままAIを拡大導入しようとして失敗する企業が多い、という指摘の投稿。"),
    "https://www.reddit.com/r/artificial/comments/1telhki/would_ai_make_future_game_difficulty_better/": (
        "AIは将来のゲーム難易度をより良くするか",
        "AIがプレイヤーに合わせてゲームの難易度を動的調整する未来についての議論スレッド。"),
    "https://www.reddit.com/r/artificial/comments/1tef6n5/a_sobering_tale_of_ai_governance/": (
        "AIガバナンスを巡る、考えさせられる話",
        "AIガバナンスの難しさを実例から考えさせる投稿。"),
    "https://www.reddit.com/r/artificial/comments/1te12a7/ai_community_buckets/": (
        "AIコミュニティの『バケツ』分類",
        "AIに関わる人々をいくつかの類型に分けて整理する投稿。"),
    # GitHub
    "https://github.com/tinyhumansai/openhuman": (
        "openhuman: プライベートで強力な個人向けAIスーパーインテリジェンス",
        "プライベート・シンプル・高性能を掲げる個人用AIアシスタント。1万超のスターを集め急上昇中。"),
    "https://github.com/obra/superpowers": (
        "superpowers: 実際に機能するエージェント型スキルフレームワークと開発方法論",
        "エージェントにスキルを与えるフレームワークとソフトウェア開発方法論。19万スター超を集める注目リポジトリ。"),
    "https://github.com/K-Dense-AI/scientific-agent-skills": (
        "scientific-agent-skills: 研究・科学・工学・分析・金融・執筆向けの実用エージェントスキル集",
        "そのまま使える研究・科学向けのエージェントスキルをまとめたリポジトリ。"),
    "https://github.com/Anil-matcha/Open-Generative-AI": (
        "Open-Generative-AI: 200+モデル対応のオープンソースAI画像・動画生成スタジオ",
        "Flux・Midjourney系など200以上のモデルを使える、商用AI動画プラットフォームのオープンソース代替。"),
    # blogs
    "https://openai.com/index/malta-chatgpt-plus-partnership": (
        "OpenAIとマルタが提携、全国民にChatGPT Plusを提供",
        "OpenAIがマルタ政府と提携し、全国民にChatGPT Plusと実践的なAIスキル研修を提供。国家規模でのAIアクセス拡大の取り組み。"),
    "https://openai.com/academy/codex-for-work/how-business-operations-teams-use-codex": (
        "業務オペレーションチームはCodexをどう使うか",
        "イニシアチブ概要や戦略アップデート、経営判断用資料の作成にCodexを活用する事例紹介。"),
    "https://openai.com/index/databricks": (
        "DatabricksがGPT-5.5をエンタープライズのエージェントワークフローに導入",
        "GPT-5.5がOfficeQA Proベンチで新たな最高性能を記録したことを受け、Databricksが企業向けエージェント基盤に採用。"),
    "https://openai.com/academy/codex-for-work/how-data-science-teams-use-codex": (
        "データサイエンスチームはCodexをどう使うか",
        "根本原因の分析メモ、影響レポート、KPIメモ、データパイプライン構築にCodexを使う事例紹介。"),
    "https://openai.com/index/personal-finance-chatgpt": (
        "ChatGPTに新しい個人資産管理(パーソナルファイナンス)機能",
        "米国のProユーザー向けプレビューとして、金融口座を安全に連携し、支出分析や資産管理をChatGPT上で行える新体験を提供。"),
    "https://openai.com/academy/codex-for-work/how-sales-teams-use-codex": (
        "セールスチームはCodexをどう使うか",
        "パイプライン概要、商談準備資料、予測レビュー、アカウントプラン作成へのCodex活用事例。"),
    "https://openai.com/index/sea-david-chen": (
        "Sea社が語る、Codexによるエージェント型ソフトウェア開発の未来",
        "Sea Limitedの最高製品責任者が、AIネイティブ開発を加速するためエンジニアリング全体にCodexを展開する理由を解説。"),
    "https://huggingface.co/blog/ibm-granite/granite-embedding-multilingual-r2": (
        "Granite Embedding Multilingual R2: 32Kコンテキストのオープン多言語埋め込み",
        "IBMがApache 2.0で公開した多言語埋め込みモデル。32Kコンテキスト対応で、100M未満クラスでは最高の検索品質を謳う。"),
    "https://openai.com/index/work-with-codex-from-anywhere": (
        "どこからでもCodexと作業する",
        "ChatGPTモバイルアプリからCodexのコーディングタスクを監視・操作・承認できるようになった。"),
    "https://openai.com/index/chatgpt-recognize-context-in-sensitive-conversations": (
        "ChatGPTがセンシティブな会話の文脈をより良く認識",
        "リスクを時間をかけて検知するなど、デリケートな会話での文脈認識を高める安全アップデート。"),
    "https://huggingface.co/blog/continuous_async": (
        "連続バッチングにおける非同期性の解放",
        "LLM推論の連続バッチング処理に非同期性を導入し、スループットを高める技術解説。"),
    "https://openai.com/index/building-codex-windows-sandbox": (
        "Windows上でCodexを動かす安全なサンドボックスの構築",
        "ファイルアクセスを制御した安全なサンドボックスをWindows向けに構築し、コーディングエージェントを安全に動かす取り組み。"),
    "https://huggingface.co/blog/amazon/foundation-model-building-blocks": (
        "AWS上での基盤モデル学習・推論のビルディングブロック",
        "AWS上で基盤モデルの学習・推論を構築するための要素技術を解説したブログ。"),
    "https://blog.google/products-and-platforms/products/search/ai-powered-google-finance-in-europe/": (
        "AI搭載の新しいGoogle Financeが欧州に拡大",
        "AIを組み込んだ刷新版Google Financeが欧州でも利用可能に。資産情報の検索・分析体験をAIで強化。"),
}

for src in ("hn", "reddit", "github", "blogs"):
    for it in d["sources"].get(src, []):
        tj = url_map.get(it.get("url"))
        if tj:
            it["title_ja"], it["summary_ja"] = tj

# ─── Highlights ───
d["highlights"] = [
    {
        "source": "hn",
        "title": "I believe there are entire companies right now under AI psychosis",
        "title_ja": "「いま丸ごと“AI精神病”に陥っている会社が確実に存在する」",
        "url": "https://twitter.com/mitchellh/status/2055380239711457578",
        "hot_take_ja": "HashiCorp創業者の一言が刺さったのは、誰もが思い当たる節があるから。AIで全部解決すると信じ込んだ経営層が、現実離れした計画を走らせ、現場が疲弊する——その構図に名前がついた瞬間だった。技術そのものより、組織がAIに飲み込まれる病理が本題。",
        "detail_ja": "HashiCorp創業者のMitchell Hashimoto氏が投稿した「いま丸ごとAI精神病(AI psychosis)に陥っている会社が確実に存在すると思う」という短い一文が、Hacker Newsで1,700以上の支持を集めて大きな話題になった。ここでの『AI精神病』とは医学用語ではなく、組織がAIの能力を過大評価し、現実と乖離した期待や意思決定に集団で取り憑かれた状態を指す比喩だ。具体的には、AIで人員を大幅削減できると信じて先に解雇を進めたり、まだ実現していない自動化を前提に事業計画を立てたり、AI利用率というKPIを掲げて現場に無意味なタスクを作らせたりするケースが挙げられる。コメント欄では、経営層がベンダーのデモやSNSの誇張に影響され、実際の検証を飛ばして全社方針を決めてしまう力学が繰り返し指摘された。重要なのは、これがAI技術の欠陥の話ではなく、不確実な新技術に対する組織の意思決定の歪みの話だという点だ。同じ日に報じられた『AI利用ノルマで不要なタスクをでっち上げるAmazon社員』の記事とも響き合い、トップダウンのAI導入圧力が逆効果を生む構造を浮き彫りにした。一方で、本物の生産性向上を実現している組織も存在するため、問題はAIそのものではなく、期待値の設定と検証プロセスの欠如にある。バズワードとして消費されがちだが、自社が『AI精神病』に陥っていないかを点検する問いとしては有用だ。",
        "detail_en": "A short post by HashiCorp co-founder Mitchell Hashimoto — 'I believe there are entire companies right now under AI psychosis' — drew over 1,700 upvotes on Hacker News and sparked wide discussion. 'AI psychosis' here is not a medical term but a metaphor for an organization that has collectively become detached from reality, overestimating what AI can do and making decisions on that distorted basis. Concrete examples raised include companies laying off staff first on the belief AI will replace them, building business plans around automation that does not yet exist, and setting 'AI usage' KPIs that push employees to invent pointless tasks. Commenters repeatedly pointed to the dynamic where executives, swayed by vendor demos and exaggerated social-media claims, skip real validation and set company-wide policy. The key point is that this is not a story about flaws in AI technology — it is about distorted organizational decision-making in the face of an uncertain new technology. It resonated with a same-day report about Amazon workers fabricating tasks to meet AI-usage pressure, highlighting how top-down adoption mandates can backfire. At the same time, some organizations are achieving genuine productivity gains, so the real issue is not AI itself but the absence of calibrated expectations and validation processes. Though easily consumed as a buzzword, it is a useful prompt for asking whether your own company has caught the condition.",
        "key_points_ja": [
            "HashiCorp創業者の投稿がHNで1,700超の支持",
            "『AI精神病』=組織がAIへの過大評価に集団で取り憑かれた状態",
            "先行解雇・非現実的な計画・無意味なAI利用KPIが症状",
            "技術の欠陥ではなく組織の意思決定の歪みの問題",
            "Amazon社員の『タスクでっち上げ』報道とも符合",
            "問題は期待値設定と検証プロセスの欠如",
        ],
        "key_points_en": [
            "HashiCorp founder's post drew 1,700+ HN upvotes",
            "'AI psychosis' = orgs collectively detached from reality on AI",
            "Symptoms: premature layoffs, unrealistic plans, hollow AI KPIs",
            "Not a tech flaw — a flaw in organizational decision-making",
            "Echoes report of Amazon workers fabricating AI tasks",
            "Root cause is missing expectation-setting and validation",
        ],
    },
    {
        "source": "arxiv",
        "title": "SANA-WM: Efficient Minute-Scale World Modeling with Hybrid Linear Diffusion Transformer",
        "title_ja": "SANA-WM: 1分尺720p動画を生成する2.6Bのオープンソース・ワールドモデル",
        "url": "https://nvlabs.github.io/Sana/WM/",
        "hot_take_ja": "『ワールドモデル』はこれまで巨大・非公開・重いの三重苦だった。SANA-WMはたった2.6Bで720p・1分尺をカメラ制御付きで生成し、しかもオープンソース。研究者が手元で世界モデルを回せる時代の入口になりうる。",
        "detail_ja": "NVIDIAの研究チームが、SANA-WMという2.6Bパラメータのオープンソース・ワールドモデルを発表した(論文はarXiv 2605.15178、HNでも250超の支持)。ワールドモデルとは、環境のダイナミクスを学習し、行動やカメラ操作に応じて未来の映像を生成できるモデルで、ロボティクスやゲーム、シミュレーション学習の基盤として注目されている。SANA-WMの特徴は『分単位』の生成を最初から想定して学習されている点で、720p解像度・約1分尺の高精細動画を、精密なカメラ制御付きで合成できる。中核にあるのはハイブリッド線形拡散Transformerというアーキテクチャで、計算コストが系列長に対して急増する通常の注意機構の代わりに線形注意的な仕組みを組み合わせ、長尺生成を現実的なコストに抑えている。論文によれば、視覚品質は大規模な商用ベースラインに匹敵する一方、わずか2.6Bという小ささで動く。これが重要なのは、従来のワールドモデルや長尺動画生成が、数十Bクラスの非公開モデルに偏っていて、研究者が再現・改造しにくかったからだ。オープンソースかつ軽量という組み合わせは、世界モデルの研究を一気に民主化しうる。注意点として、1分という尺は依然短く、物理的整合性や長期の一貫性は今後の評価課題で、同日公開の『幾何一貫性のための動画ワールドモデル評価』のような定量ベンチと組み合わせた検証が必要になる。",
        "detail_en": "NVIDIA researchers released SANA-WM, a 2.6B-parameter open-source world model (paper at arXiv 2605.15178; 250+ upvotes on Hacker News). A world model learns the dynamics of an environment and can generate future video conditioned on actions or camera motion, making it a key building block for robotics, games, and simulation-based learning. SANA-WM's distinguishing feature is that it is natively trained for minute-scale generation: it synthesizes roughly one-minute, 720p high-fidelity video with precise camera control. At its core is a hybrid linear diffusion Transformer architecture that pairs a linear-attention-style mechanism with diffusion, instead of standard attention whose cost grows sharply with sequence length, keeping long-form generation at a practical cost. The paper reports visual quality comparable to large-scale industrial baselines while running at just 2.6B parameters. This matters because prior world models and long-video generators have skewed toward tens-of-billions-parameter closed models that researchers cannot reproduce or modify easily. Being both open-source and lightweight could rapidly democratize world-model research. Caveats remain: one minute is still short, and physical plausibility and long-range consistency are open evaluation questions — best checked against quantitative benchmarks like the same-day 'video world model evaluation for geometric consistency' work.",
        "key_points_ja": [
            "NVIDIAが2.6Bのオープンソース・ワールドモデルを公開",
            "720p・約1分尺をカメラ制御付きで生成",
            "ハイブリッド線形拡散Transformerで長尺を低コスト化",
            "視覚品質は大規模商用ベースラインに匹敵",
            "従来は数十Bの非公開モデル中心→研究の民主化に寄与",
            "1分尺・物理整合性は今後の評価課題",
        ],
        "key_points_en": [
            "NVIDIA releases a 2.6B open-source world model",
            "Generates 720p, ~1-minute video with camera control",
            "Hybrid linear diffusion Transformer makes long-form cheap",
            "Visual quality on par with large industrial baselines",
            "Prior models were tens-of-B closed — this democratizes research",
            "One-minute length and physical consistency still open",
        ],
    },
    {
        "source": "hn",
        "title": "Frontier AI has broken the open CTF format",
        "title_ja": "フロンティアAIがオープンなCTF(セキュリティ競技)を壊した",
        "url": "https://kabir.au/blog/the-ctf-scene-is-dead",
        "hot_take_ja": "AIが人間の趣味の競技を『破壊』する一例。CTFはセキュリティ人材育成の入口だったが、フロンティアモデルが問題を高速で解いてしまい、オープン参加型では実力が測れなくなった。次に壊れる『人間の競技』はどこか、という普遍的な問いを突きつける。",
        "detail_ja": "セキュリティ研究者のブログ記事『The CTF scene is dead(CTFシーンは死んだ)』が、フロンティアAIモデルの台頭でオープン参加型のCTF(Capture The Flag)が競技として成立しなくなった、と主張しHNで広く議論された。CTFとは、脆弱性のあるプログラムやサーバーを解析して隠された『フラグ』を奪うセキュリティ競技で、ハッカーの腕試しであると同時に、実務的なセキュリティスキルを学ぶ重要な登竜門でもある。問題は、最新のLLMやエージェントが、リバースエンジニアリング・暗号・Web脆弱性といった典型的なCTF課題を、人間の上位陣に匹敵する速度と精度で解けるようになったことだ。オンラインで誰でも参加できる形式では、AIを使ったチームと使わないチームを区別できず、運営側も検知しきれない。結果として、純粋に人間の実力を測る競技としての信頼性が崩れた、というのが筆者の見立てだ。これはAIによる『不正』というより、競技フォーマットそのものの前提が崩れた問題に近い。対策として、その場限りのオフライン会場で開催する、AI利用を前提に新しい採点軸を作る、人間とAIの混成チーム戦に再設計する、といった方向が議論されている。CTFという比較的ニッチな領域の話に見えて、AIが人間の技能評価・採用試験・教育課題を次々と無効化していく、より大きな現象の縮図と言える。",
        "detail_en": "A blog post by a security researcher, 'The CTF scene is dead,' argued that the rise of frontier AI models has made open-participation CTF (Capture The Flag) competitions unviable, and it drew wide discussion on Hacker News. CTF is a security contest where players analyze vulnerable programs or servers to steal hidden 'flags'; it is both a test of hacker skill and an important entry point for learning practical security skills. The problem is that modern LLMs and agents can now solve typical CTF tasks — reverse engineering, cryptography, web vulnerabilities — at a speed and accuracy rivaling top human players. In a format anyone can join online, organizers cannot distinguish AI-assisted teams from unassisted ones, nor reliably detect the difference. As a result, the author argues, CTF's credibility as a pure measure of human skill has collapsed. This is less a story of AI 'cheating' and more one where the format's core assumptions no longer hold. Proposed responses include running ephemeral offline venues, designing new scoring axes that assume AI use, or redesigning events as mixed human-AI team contests. Though CTF is a relatively niche domain, it is a microcosm of a larger phenomenon: AI steadily invalidating human skill assessments, hiring tests, and educational exercises.",
        "key_points_ja": [
            "ブログ『CTFシーンは死んだ』がHNで広く議論",
            "CTF=脆弱性を解析しフラグを奪うセキュリティ競技",
            "フロンティアAIが典型課題を上位人間並みに高速突破",
            "オンライン形式ではAI利用を検知・区別できない",
            "対策案: オフライン開催・新採点軸・人間×AI混成戦",
            "AIが人間の技能評価を無効化する大きな流れの縮図",
        ],
        "key_points_en": [
            "Blog 'The CTF scene is dead' widely discussed on HN",
            "CTF = security contest of analyzing flaws to steal flags",
            "Frontier AI solves typical tasks at top-human speed",
            "Online formats can't detect or separate AI assistance",
            "Fixes floated: offline venues, new scoring, human-AI teams",
            "A microcosm of AI invalidating human skill tests",
        ],
    },
    {
        "source": "hn",
        "title": "US is starting to see heavy job losses in roles exposed to AI",
        "title_ja": "米国、AIの影響を受けやすい職種で大幅な雇用減が始まる",
        "url": "https://www.bloomberg.com/news/articles/2026-05-15/us-is-starting-to-see-heavy-job-losses-in-roles-exposed-to-ai",
        "hot_take_ja": "『AIで仕事がなくなる』という抽象的な不安が、ついに労働統計の数字として現れ始めた。注目すべきは、AIに『触れる』職種ほど雇用が減っているという相関。生産性向上の物語の裏で、調整コストを誰が負担するのかが問われる局面に入った。",
        "detail_ja": "Bloombergが、米国でAIの影響を受けやすい職種を中心に、目に見える規模の雇用減が始まったと報じ、HNでも議論を呼んだ。これまでAIによる雇用への影響は、将来予測や個別企業のレイオフ発表として語られることが多く、マクロな労働統計に明確な形では表れていなかった。今回の記事のポイントは、AIへの『曝露度(exposure)』が高い職種——文章作成、データ入力、初級のコーディング、カスタマーサポート、一部のアナリスト業務など——で、他の職種より雇用が弱含んでいるという相関が観測され始めた、という点だ。これは因果関係を断定するものではなく、景気循環や金利、コロナ後の過剰採用の調整といった他の要因と切り分ける必要がある。それでも、AIの能力向上と雇用データの動きが同じ方向を向き始めたことは、政策・企業・働き手のいずれにとっても重要なシグナルだ。とくに影響が初級・エントリーレベルの職に集中する場合、若年層がキャリアの最初の足場を失い、スキルを積む経路が細るという長期的な懸念が生じる。同日には『米国人の70%が近隣へのAIデータセンター建設に反対』という調査や、Amazonの『AI利用ノルマ』報道も出ており、AIの社会的コストへの世論の警戒が強まっている文脈とあわせて読むべきニュースだ。一方で、Stanfordの導入調査が示すように生産性を大きく伸ばす組織もあり、雇用の純増減は今後の調整次第という不確実性も残る。",
        "detail_en": "Bloomberg reported that the US has begun to see job losses of a visible scale, concentrated in roles exposed to AI, and the story drew discussion on Hacker News. Until now, AI's labor-market impact has mostly been discussed as future forecasts or individual company layoff announcements, without showing up clearly in macro employment data. The article's key point is that a correlation is starting to appear: occupations with high AI 'exposure' — writing, data entry, junior coding, customer support, some analyst work — are showing weaker employment than other roles. This does not prove causation, and other factors such as the business cycle, interest rates, and the unwinding of post-pandemic over-hiring must be separated out. Still, the fact that improving AI capabilities and employment data are starting to point the same way is an important signal for policymakers, companies, and workers alike. If the impact is concentrated in junior, entry-level roles, there is a longer-term concern that young people lose their first career foothold and the path to building skills narrows. The same day brought a poll showing 70% of Americans oppose nearby AI data centers and reporting on Amazon's 'AI usage' quotas, so this should be read alongside a broader hardening of public wariness toward AI's social costs. On the other hand, as Stanford's deployment study shows, some organizations achieve large productivity gains, so the net change in jobs remains uncertain and dependent on how the adjustment unfolds.",
        "key_points_ja": [
            "AIの影響を受けやすい職種で米国の雇用減が顕在化",
            "従来は予測や個別レイオフ→マクロ統計に表れ始めた",
            "『AI曝露度』の高い職種ほど雇用が弱含む相関",
            "景気・金利など他要因との切り分けは依然必要",
            "影響がエントリー職に集中すると若年層のキャリアに長期的懸念",
            "データセンター反対やAI利用ノルマ報道とあわせて読むべき",
        ],
        "key_points_en": [
            "Visible US job losses emerging in AI-exposed roles",
            "Was forecasts/layoffs — now showing in macro data",
            "Roles with high 'AI exposure' show weaker employment",
            "Still must separate cycle, rates and other factors",
            "Entry-level concentration risks young workers' careers",
            "Read with data-center backlash and AI-quota reports",
        ],
    },
    {
        "source": "blogs",
        "title": "A new personal finance experience in ChatGPT",
        "title_ja": "ChatGPTに新しい個人資産管理(パーソナルファイナンス)機能",
        "url": "https://openai.com/index/personal-finance-chatgpt",
        "hot_take_ja": "ChatGPTが銀行口座とつながる——便利さと引き換えに、最も繊細な個人データをAIに預けることになる。家計簿アプリの代替を狙う動きだが、本当の論点は『資産情報をLLMに連携する』という前例が一気に広がることだ。",
        "detail_ja": "OpenAIが、ChatGPTに個人資産管理(パーソナルファイナンス)の新体験を追加すると発表した。まず米国のProユーザー向けプレビューとして提供され、ユーザーが自分の金融口座を安全に連携すると、ChatGPTが支出の傾向分析、予算の整理、資産状況の把握などを対話形式で支援する。これは、Mintのような従来の家計簿・資産管理アプリが担ってきた領域に、会話型AIが本格的に踏み込むことを意味する。強みは明白で、表やグラフを自分で読み解く代わりに『今月使いすぎた項目は』『この支出は削れるか』と自然言語で聞けば、文脈を踏まえた答えが返ってくる。一方で論点も大きい。資産・取引履歴は個人データの中でも最も機微な部類で、それをLLMサービスに連携することのプライバシー・セキュリティ上の含意は重い。OpenAIは『安全に連携』と強調しているが、データの保存範囲、学習利用の有無、第三者連携の仕組みは利用者が必ず確認すべき点だ。また、AIによる家計アドバイスが誤った数値や一般論を自信ありげに提示する『幻覚』のリスクは、金融という領域では実害に直結しうる。同日にはGoogleがAI搭載のGoogle Financeを欧州に拡大するニュースもあり、大手が『AI×個人金融』を次の主戦場と見ていることがうかがえる。金融という最も慎重さが求められる領域に会話型AIが入ってくる、その入口を示すニュースだ。",
        "detail_en": "OpenAI announced a new personal finance experience in ChatGPT. It launches first as a preview for Pro users in the US: once a user securely connects their financial accounts, ChatGPT helps with spending-pattern analysis, budgeting, and understanding their overall financial picture through conversation. This means conversational AI is moving in earnest into the territory long held by personal finance apps like Mint. The appeal is clear — instead of reading tables and charts yourself, you can ask in natural language ('what did I overspend on this month?', 'can I cut this expense?') and get context-aware answers. But the issues are significant too. Financial accounts and transaction history are among the most sensitive categories of personal data, and connecting them to an LLM service carries weighty privacy and security implications. OpenAI emphasizes 'secure' connection, but users should verify exactly what data is stored, whether it is used for training, and how third-party integrations work. There is also the risk of 'hallucination' — AI confidently presenting wrong numbers or generic advice — which in the financial domain can translate directly into real harm. The same day brought news of Google expanding its AI-powered Google Finance to Europe, suggesting major players see 'AI x personal finance' as the next battleground. This news marks the entry point of conversational AI into one of the domains that demands the most caution.",
        "key_points_ja": [
            "ChatGPTに個人資産管理機能、米国Proユーザー向けプレビュー",
            "金融口座を連携し支出分析・予算整理を対話で支援",
            "従来の家計簿・資産管理アプリ領域に会話型AIが本格参入",
            "資産情報は最も機微なデータ、プライバシー含意が大きい",
            "保存範囲・学習利用・第三者連携は要確認",
            "金融での『幻覚』は実害に直結、同日Googleも欧州拡大",
        ],
        "key_points_en": [
            "ChatGPT adds personal finance, preview for US Pro users",
            "Connect bank accounts for conversational spending analysis",
            "Conversational AI enters the personal-finance-app space",
            "Financial data is highly sensitive — big privacy stakes",
            "Check data storage, training use, third-party integration",
            "Hallucination risks real harm; Google also expands in EU",
        ],
    },
]

OUT.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT}")
print(f"Highlights: {len(d['highlights'])}")
for src, items in d["sources"].items():
    enriched = sum(1 for it in items if it.get("title_ja"))
    print(f"  {src}: {enriched}/{len(items)} enriched")
