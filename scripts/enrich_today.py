#!/usr/bin/env python3
"""Enrich raw-2026-05-28.json with Japanese summaries and highlights."""
import json
from pathlib import Path

DATE = "2026-05-28"
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / f"raw-{DATE}.json"
OUT = ROOT / "data" / f"{DATE}.json"

with open(RAW) as f:
    d = json.load(f)

# -------- arXiv (index-aligned with raw order) --------
arxiv = [
    ("ピクセルから言葉へ：大規模ネイティブOne-Visionモデルへ",
     "別々の画像エンコーダと言語デコーダを多段で接続する従来VLMをやめ、ピクセルと言葉の相互作用を最初から一体で学ぶネイティブ型VLMを大規模に目指す研究。"),
    ("PEFT-Arena：安定性-可塑性の視点でPEFTを評価する",
     "LoRAなどのパラメータ効率的微調整を、下流精度だけでなく事前学習能力の保持(安定性)と適応(可塑性)のバランスで評価し直すベンチマーク。"),
    ("VLMは自然読解で人間との整合をLLMより高めるとは限らない",
     "視覚-言語学習がテキスト表現を読解時により人間らしくするかを検証し、全体としては必ずしも向上しないことを示した研究。"),
    ("Gamma-World：2人を超える多エージェント生成ワールドモデル",
     "単一の制御信号から未来を生成する従来のワールドモデルを拡張し、複数プレイヤー/ロボットが相互作用する環境を生成できるようにした研究。"),
    ("双方向進化探索による自己改善型言語モデル",
     "best-of-Nや木探索の限界を超えるため、双方向の進化的探索でサンプル生成と推論を強化し、LLMを自己改善させる手法。"),
    ("HarmoVid：再照明対応の動画ポートレート調和",
     "前景の人物動画の照明を背景シーンに合わせ、影・色調・明るさを自然に馴染ませる(リライティング込みの)動画調和手法。"),
    ("Beyond Binary：物理に基づく接触表現で器用なSim-to-Real操作",
     "接触の多い操作タスクで、触覚など情報密度の高いモダリティを活かせる物理整合な接触表現を用い、シミュレーションから実機への転移を改善。"),
    ("感情に基づく音楽推薦：オフライン選好最適化のロールアウト型ワールドモデル",
     "聴き手の感情状態を成功指標とする音楽推薦で、感情の実オンライン実験が倫理的に難しい問題を、オフラインのワールドモデルで回避する手法。"),
    ("AREA：CLIPベース継続学習のための属性抽出と集約",
     "『a photo of a [CLASS]』式の単純プロンプトに頼るCLIP継続学習を、クラスの属性を抽出・集約することで強化する手法。"),
    ("スケーラブルな監視のための保守性のキャリブレーション",
     "人間を超えうる自律エージェントをどう監督するかという制御問題に対し、監督側の保守性(慎重さ)を適切に調整するアプローチ。"),
    ("明示・暗黙の証拠から作る個人向け視覚メモリ",
     "テキスト中心だった個人化エージェントの長期記憶を、画像からしか得られない個人固有情報まで扱えるよう拡張するベンチマークと手法。"),
    ("OmniVerifier-M1：構造的再較正を伴うマルチモーダル・メタ検証器",
     "マルチモーダルLLMの出力を検証する際、検証器の根拠生成を明示的に構造化して再較正し、より細かく信頼性を評価する手法。"),
    ("Ω-QVLA：合成回転と段階別スケーリングによるVLAの頑健量子化",
     "視覚-言語-行動(VLA)モデルをオンデバイスで動かすため、合成回転とステップ別スケーリングで精度劣化を抑えた量子化手法。"),
    ("人間のラベル揺らぎを安定信号として使う",
     "アノテーター間選好最適化により、注釈者ごとのラベル付け・説明の癖をLLMに学習・再現させられるかを検証した研究。"),
    ("CaMBRAIN：因果的状態空間モデルによるリアルタイム連続EEG推論",
     "数秒〜数時間に及ぶ脳波(EEG)を、因果的な状態空間モデルでリアルタイムかつ連続的に推論する手法。"),
    ("スキル条件付きゲート自己蒸留でLLM推論を強化",
     "教師側の特権情報(参照解答など)が信頼できない場合でも機能するよう、スキル条件付きのゲートで自己蒸留を行いLLMの推論を改善。"),
    ("エージェントに意味メタデータは必要か？データ検索の比較研究",
     "schema.orgのような意味メタデータが、自律エージェントのデータ検索に実際どれだけ役立つかを比較検証した研究。"),
    ("LLMは談話小辞を扱えるか？口語マレー語の事例研究",
     "『lah』のような談話小辞(感情や意図を伝える語)をLLMが適切に扱えるかを、口語マレー語を題材に検証した研究。"),
    ("バイアスは勾配の痕跡を残す：概念分解への勾配プローブで無ラベル検出",
     "ラベルやグループ注釈、再学習に頼らず、概念分解への勾配プローブで分類器の擬似相関(バイアス)を見つける手法。"),
    ("視覚-言語の因果推論における『抽象化のギャップ』",
     "VLMの流暢な因果説明が、言語的もっともらしさなのか忠実な因果推論なのかを切り分ける二重プローブ手法。"),
    ("LLMは言語的な不確実性マーカーで内的確信度を正しく反映できるか",
     "『おそらく』のような言葉での確信表現が、モデル自身の内部的な不確実性と一致しているかを検証した研究。"),
    ("弱点から学ぶ：小型コンピュータ操作エージェントの自動ドメイン特化",
     "ドメインごとに巨大な専門モデルを用意するのは高コストなので、小型のコンピュータ操作エージェントを弱点起点で安く特化させる手法。"),
    ("マルチモーダル・エージェント推論のための探索的方策最適化",
     "思考と外部ツール利用を交互に行うマルチモーダル・エージェントを、探索的な方策最適化で強化する手法。"),
    ("記憶を『継続的に進化する結合』として捉え直す",
     "LLMエージェントの記憶を静的なリポジトリではなく、フィードバックで絶えず再編される進化的な結合として扱う枠組み。"),
    ("Multi-Mixer Models：共有表現による柔軟な系列モデリング",
     "計算が二乗で増えるソフトマックス注意と線形再帰モデルを、共有表現のもとで柔軟に組み合わせる系列モデリング。"),
    ("マルチラベル学習で一般化メトリクスを最適化する原理的アルゴリズム",
     "F値やJaccard係数など複雑な評価指標を、マルチラベル分類で原理的に最適化するアルゴリズムを提案。"),
    ("SwarmHarness：分散・インセンティブ整合型エージェント網によるスキルベースのタスク振り分け",
     "個人PCや遊休サーバの計算資源を安全かつ報酬付きで共有するため、インセンティブ整合の分散エージェント網でタスクを振り分ける仕組み。"),
    ("CubePart：オープン語彙でパーツ制御可能な3D生成器",
     "アニメや物理に使えるよう、意味的パーツに分解しつつ制御可能な3Dアセットをオープン語彙で生成するモデル。"),
    ("LLMの0次微調整は実は推論ワークロードである",
     "逆伝播を前方評価で置き換えるゼロ次(ZO)微調整は、主要計算が前方パス=推論であり、推論基盤上で実行すべきだと論じる研究。"),
    ("外挿的な重み平均がコードRLの正確性-効率フロンティアを明らかにする",
     "微調整チェックポイント間の重みを外挿平均することで、追加学習なしにコードRLのパレートフロンティアを推論時に拡張できるかを検証。"),
    ("選好整形した期待ハイパーボリューム/R2改善：厳密計算と単調性",
     "ベイズ多目的最適化で、利用者の選好を反映した獲得関数(期待ハイパーボリューム改善等)の厳密計算と単調性を理論的に整理。"),
    ("予測市場のスタンス検出：反実仮想拡張と市場文脈で不均衡コメントに対処",
     "Polymarketなど予測市場でトレーダーのコメントから賛否(スタンス)を読み取る際、不均衡データを反実仮想拡張と市場文脈で補う手法。"),
    ("CORE：対照的リフレクションで推論を高速に改善",
     "RLVRやプロンプト最適化が遅い問題に対し、対照的なリフレクション(振り返り)で推論能力を素早く向上させる手法。"),
    ("Self-Prophetic Decoding：LVLMの視覚探索を引き出すデコード",
     "『画像で考える』パラダイムの一形態である視覚探索を、自己予言的なデコードで大規模視覚言語モデルから引き出す手法。"),
    ("Reverse Probing：臨床テキスト向けトークン単位の教師あり不確実性定量化",
     "臨床テキストでLLMが自らの不確実性を確実に示せるよう、トークン単位で教師あり学習した不確実性定量化(UQ)手法。"),
    ("BIRDNet：ブール含意知識グラフを解釈可能な深層網として符号化",
     "表データに潜む特徴間のブール含意関係を抽出し、解釈可能な深層ニューラルネットとして符号化する手法。"),
    ("開腹手術ロボット支援の模倣学習：縫合追従の複数方策評価",
     "外科医とロボットが協働する開腹手術の『縫合追従』動作を対象に、汎用模倣学習を初めて評価した研究。"),
    ("SeeGroup：自己決定グルーピングによる透明表面の多層深度推定",
     "透明な物体の表面とその奥にある物体の多層深度を、自己決定的なグルーピングで推定する手法。"),
    ("Code as a Weapon：コーディングモデルの悪意あるコード要求への応諾を測る合意ラベル付きプロンプト集",
     "汎用LLMの有害回答は文章だが、コーディングモデルが応じれば動くマルウェアになりうる——その応諾度を測る合意ラベル付きベンチマーク。"),
    ("効用を意識したマルチモーダル対照学習による商品画像生成",
     "テキスト整合だけでなく購買への効用も考慮して、ECで効果的な商品画像を生成するマルチモーダル対照学習。"),
    ("MemTrace：LLM記憶システムの誤りを追跡・帰属する",
     "長期推論に不可欠だが壊れやすく原因究明が難しいLLMの記憶システムについて、誤りの動的な発生過程を追跡・帰属する手法。"),
    ("AlphaTransit：都市規模の公共交通ルートを学習で設計",
     "路線網は全体を組み上げて初めて良し悪しが分かる遅延フィードバック問題——これを強化学習で解き、都市規模の交通ルートを設計。"),
    ("Beyond Lipschitz：離散連続率によるデータ駆動の頑健性",
     "局所/大域リプシッツ定数では粗すぎる/厳しすぎる頑健性評価を、データ駆動の離散的な連続率(modulus)で精緻化する手法。"),
    ("VLAはどう壊れるか：ブラックボックス行動監視で構造別の故障シグネチャを発見",
     "VQ-BeT・Diffusion Policy・ACTを同一条件で動かすと、アーキテクチャごとに予測可能な異なる故障の仕方を示すことを発見。"),
    ("エネルギー較正によるマルチアダプタ表現介入",
     "重みを変えずにLLMの挙動を整える表現介入を、複数アダプタをエネルギー較正で動的に組み合わせて強化する手法。"),
    ("LiveBrowseComp：検索エージェントは本当に検索しているのか、知識の確認をしているだけか",
     "BrowseCompに3つの診断を導入し、LLM検索エージェントの多くが真に探索するのではなく既知の知識をWebで確認しているだけだと示した研究。"),
    ("OpenURMA：統一バスプロトコルのクリーンルーム・オープン実装",
     "データセンタのRDMAはNICで律速される——接続ごとの状態保持がボトルネックになる問題に対するオープンなクリーン実装。"),
    ("IPO-Mine：長大なマルチモーダルIPO文書のセクション構造解析ツールキットとデータセット",
     "新規上場(IPO)目論見書を、章立て構造を踏まえて解析するためのツールキットとデータセット。"),
    ("Thinking as Compression：推論モデルは実は文脈圧縮器である",
     "長文入力を情報損失少なく短縮する文脈圧縮を、複雑な専用機構ではなく既存の推論モデル自体で実現できることを示した研究。"),
    ("拡散モデルによるゼロショット逆問題での段階的な歪み-知覚トラバース",
     "ベイズ逆問題に固有の歪みと知覚品質のトレードオフを、拡散モデルで段階的にたどって調整する手法。"),
]

# -------- HN (index-aligned) --------
hn = [
    ("AIと話すのに疲れた",
     "どこもかしこもAI生成の回答ばかりで、人間味のあるやり取りに飢えているという疲労感を綴ったエッセイ。AI疲れの空気を象徴し1900超のスコアを集めた。"),
    ("YouTube、AI生成動画を自動でラベル付け",
     "写実的なAI動画を内部シグナルで自動検出しラベルを貼る方針を発表。クリエイターの自己申告任せから一歩踏み込んだ出所表示の強化策。"),
    ("Googleの『皆AIモードを愛用』発言後、DuckDuckGoの訪問が約28%増",
     "Googleが『ユーザーはAIモードを気に入っている』と強調した直後の週、AIなし検索を掲げるDuckDuckGoへの訪問が約28%増加。AI検索への静かな反発が数字に。"),
    ("Claude Opus 4.8",
     "Anthropicが新フラッグシップを公開。コードの欠陥見逃しが約1/4に減るなど『正直さ』を強化し、価格据え置きでFast modeは3倍安に。"),
    ("テックCEOが『AIサイコーシス』に罹っている",
     "Box CEOのAaron Leviが命名。現場の泥臭い作業から遠い経営者ほどAIの能力を過大評価しやすく、根拠の薄い大量解雇につながっていると指摘。"),
    ("最先端LLM同士、実世界のファクトチェックで意見が割れる",
     "実際の事実確認依頼1000件を5つの最先端モデルに判定させると67%で不一致。AIを単独の真実判定者にする危うさを定量化した研究。"),
    ("Show HN：Hallucinate – 大規模多人数同時参加オンライン・レイヴ",
     "ブラウザ上で大勢が同時に参加する『レイヴ』体験を作るお遊び系Webプロジェクト。Show HNで話題に。"),
    ("メッシュネットワーク(Meshtastic, MeshCore, Reticulum)に入門中",
     "インフラに依存しない分散型のメッシュ通信に入門した体験記。AIとは別軸だが、自律分散への関心の高まりを映す。"),
    ("GitHubで障害：PR・Issue・Git操作・APIに影響",
     "プルリク、Issue、Git操作、APIリクエストに影響する障害が発生。多くの開発が依存するインフラの脆さが改めて話題に。"),
    ("Go：ジェネリックメソッドのサポート提案",
     "Go言語にジェネリックなメソッドを導入する提案。長年の要望で、設計上のトレードオフを巡り活発な議論に。"),
    ("自前のAIモデルを学習させる(PostHog)",
     "PostHogが既製LLMに頼らず自社用モデルを学習させた取り組みを公開。製品にAIを組み込む側の現実的な判断が読める記事。"),
    ("Show HN：Continue? Y/N——AIエージェントの権限疲れを描く60秒ゲーム",
     "AIエージェントの『許可しますか?Y/N』連打にうんざりする権限疲れを題材にした60秒の風刺ゲーム。"),
    ("AIの請求額ショックが米企業を直撃",
     "AI支出の費用対効果に疑問符——導入コストが想定を超え、ROIが見えないという企業の悲鳴をAxiosが報道。"),
    ("ロンバルディア州、緑地でのデータセンター建設に最大200%の課徴金",
     "イタリア・ロンバルディア州が緑地・農地でのデータセンター建設費を最大200%引き上げ。AIインフラ拡張と土地利用の対立が表面化。"),
    ("自然のように考え、AIが探れない領域を探る『エウレカ・マシン』",
     "インド理科大学院(IISc)発の、自然界の発見プロセスを模してAIが届かない探索を狙う研究。"),
    ("MacBookを温めよう(2019)",
     "寒いとMacBookの挙動が変わる現象を扱った2019年の小ネタ記事が再浮上。技術系の遊び心が刺さった。"),
    ("Bttf：コマンドラインの日時『万能ナイフ』",
     "ripgrep作者BurntSushiによる、日時操作を何でもこなすCLIツール。実用的で評判に。"),
    ("Claude Codeの動的ワークフロー",
     "Claude Codeで数百のサブエージェントを並列実行する『Dynamic workflows』の紹介。Opus 4.8と同時に投入された新機能。"),
    ("ripgrepのAIポリシー",
     "ripgrepリポジトリが掲げたAI生成コントリビューションに関する方針。OSSがAI寄与とどう向き合うかの一例として注目。"),
    ("Labubuとハイパーリアルについて",
     "人気キャラLabubuを題材に、ボードリヤール的なハイパーリアル(現実より現実的な記号)を論じた文化エッセイ。"),
]

# -------- GitHub (index-aligned) --------
github = [
    ("MoneyPrinterTurbo：AIでワンクリック短尺動画生成",
     "大規模言語モデルを使い、テーマを入れるだけで高解像度の短尺動画を一発生成するツール。本日+4685スターと急騰。"),
    ("taste-skill：AIに『良いセンス』を与えるスキル",
     "AIが生成しがちな退屈で平板なスロップ(slop)を抑え、センスの良い出力を促すためのスキル集。"),
    ("FreeDomain：誰でも使える無料ドメイン",
     "DigitalPlatが提供する無料ドメインのリポジトリ。AIとは別だが17万スター超で根強い人気。"),
    ("superpowers：エージェント型スキル・開発方法論フレームワーク",
     "Claude Codeなどで機能する、エージェントのスキルと開発方法論をまとめた枠組み。21万スター超の注目株。"),
    ("ECC：エージェント・ハーネスの性能最適化システム",
     "Claude Code・Codex・Cursor等向けに、スキル・記憶・セキュリティ・リサーチ優先の開発を束ねるハーネス最適化システム。"),
    ("anthropics/skills：Agent Skills公式リポジトリ",
     "Anthropic公式のエージェント・スキル公開リポジトリ。スキルという仕組みが一気に普及しつつある流れを象徴。"),
    ("stop-slop：文章からAIっぽさを除くスキル",
     "生成テキスト特有のAIの匂い(定型句や不自然な言い回し)を取り除くためのスキルファイル。"),
    ("twenty：AI前提のオープンソース版Salesforce",
     "Salesforceの代替を目指す、AIを前提に設計されたオープンソースCRM。"),
    ("crawl4ai：LLMに優しいOSSウェブクローラー",
     "LLMでの利用を前提に設計された、オープンソースのウェブクローラー/スクレイパー。RAG構築などで人気。"),
    ("harness：ドメイン特化のエージェントチームを設計するメタスキル",
     "目的に応じた専門エージェント群とそのスキルを自動設計するメタスキル。エージェント設計の自動化を狙う。"),
    ("MOSS-TTS：高表現力のオープン音声生成モデル群",
     "OpenMOSSによる、長文・多話者・効果音・リアルタイム配信まで高忠実度で扱えるオープンソースの音声生成モデルファミリー。"),
]

# -------- Blogs (index-aligned) --------
blogs = [
    ("Google I/O 2026の主要12モーメントを振り返る",
     "Google I/O 2026のキーノートから重要な12の発表を映像付きで総括。今年のGoogleのAI戦略を一望できるまとめ。"),
    ("OpenAIのフロンティア・ガバナンス枠組み",
     "OpenAIが、AIの安全性・セキュリティ・リスク運用をEUやカリフォルニアの新規制と整合させるガバナンス枠組みを公開。"),
    ("ITBench-AA：最先端モデルもエンタープライズITのエージェント業務で50%未満",
     "Artificial AnalysisとIBMによる、実務的なIT運用タスクを測る初のエージェント・ベンチマーク。最先端でもスコア50%未満と判明。"),
    ("CiscoとOpenAI、Codexでエンタープライズ開発を刷新",
     "CiscoがCodexでAIネイティブ開発を拡大し、防御業務の加速や欠陥修正の自動化を進める事例。"),
    ("Codexで自己改善する税務エージェントを構築",
     "OpenAI・Thrive・Creteが、申告を自動化し精度を高めて自己改善する税務エージェントをCodexで作った事例。"),
    ("Warp、GPT-5.5でオープンソース開発に大きく賭ける",
     "ターミナルのWarpがGPT-5.5やOpenAIモデルを使い、ローカル・クラウド・OSSにまたがるコーディングエージェントを協調させる事例。"),
    ("2026年の選挙情報と安全策",
     "世界的な選挙を控え、OpenAIが情報アクセス支援・サイバー防御者の支援・AI透明性の強化策を公表。"),
    ("Reachy Mini、完全ローカルで動作",
     "Hugging Faceの小型ロボットReachy Miniが、クラウド非依存の完全ローカルで会話できるようになった事例。"),
    ("Hubバケットで1兆パラメータを配る：TRLのデルタ重み同期",
     "巨大モデルのRL学習で、重みの差分(デルタ)だけをHubバケット経由で同期し、1兆パラメータ規模の配布を可能にする工夫。"),
    ("OpenAI、Grupo Folha・UOLとコンテンツ提携",
     "OpenAIがブラジルの大手メディアと提携し、出典・透明性付きで信頼できる報道をChatGPTに取り込む取り組み。"),
    ("Harness、Scaffold——AIエージェント用語を正しく押さえる",
     "『ハーネス』『スキャフォールド』などエージェント周辺の紛らわしい用語を整理し、定義を揃えるための解説。"),
    ("Nemotron-Labs拡散言語モデルで『光速』テキスト生成へ",
     "NVIDIAが、自己回帰ではなく拡散方式の言語モデルでテキスト生成を大幅高速化する取り組みを公開。"),
    ("Google I/O 2026の対話ステージを振り返る",
     "I/O 2026の『Dialogues』ステージの対話セッション(Sundar Pichai登壇など)を総括した記事。"),
    ("規模より特化：AI調達が見落としがちな戦略変数",
     "AI調達では巨大モデルの規模より、用途への特化が成果を左右しうる——見落とされがちな観点を論じた記事。"),
    ("OpenAI、Gartnerでエンタープライズ・コーディングエージェントのリーダーに",
     "2026年GartnerのエンタープライズAIコーディングエージェントのMagic QuadrantでCodexがリーダーと評価された。"),
    ("Virgin Atlantic、Codexで開発を高速化",
     "Virgin Atlanticが固定の繁忙期締切に向け、Codexでアプリ刷新をほぼ全ユニットテスト網羅・P1障害ゼロで出荷した事例。"),
]


def apply(src_key, pairs):
    items = d["sources"].get(src_key, [])
    assert len(items) == len(pairs), f"{src_key}: {len(items)} items vs {len(pairs)} pairs"
    for it, (tja, sja) in zip(items, pairs):
        it["title_ja"] = tja
        it["summary_ja"] = sja


apply("arxiv", arxiv)
apply("hn", hn)
apply("github", github)
apply("blogs", blogs)

# -------- Highlights --------
highlights = [
    {
        "source": "hn",
        "title": "Claude Opus 4.8",
        "title_ja": "Claude Opus 4.8 リリース",
        "url": "https://www.anthropic.com/news/claude-opus-4-8",
        "hot_take_ja": "Anthropicが4.7から間を置かずOpus 4.8を投入。目玉は能力ではなく『正直さ』で、コードの欠陥を見逃す確率が約4分の1に低下。価格は据え置きのままFast modeは3倍安、しかもClaude Codeで数百のサブエージェントを回す『Dynamic workflows』まで同時公開——静かに、しかし確実に距離を広げにきた。",
        "detail_ja": "AnthropicがフラッグシップのClaude Opus 4.8を公開した。前世代4.7から各種ベンチマークが底上げされ、同社は『より有能な協働者』と位置づける。最大の改善は性能数値よりも『正直さ』で、コードの欠陥を見逃す確率が4.7比で約4分の1に低下したという。エージェント用途も強く、ブラウザ操作のOnline-Mind2Webで84%を記録しOpus 4.7やGPT-5.5を上回り、法務エージェントの『全項目合格』基準を10%超えた初のモデルとされる。同じ能力をより少ないステップで達成する『ツール効率』も上がった。価格は入力$5/出力$25(100万トークンあたり)で据え置きだが、高速版Fast modeは入力$10/出力$50と従来比3倍安い。APIは claude-opus-4-8 で即日利用できる。同時に、Claude Codeで数百のサブエージェントを並列実行する『Dynamic workflows』、claude.aiで応答ごとの計算量を選べる『Effort controls』、Messages APIでメッセージ配列内にsystem項目を置ける更新も発表された。非整合な挙動の割合も下がったとされ、性能・安全・コスト効率を同時に押し上げた構成だ。",
        "detail_en": "Anthropic has released its flagship Claude Opus 4.8. It improves on 4.7 across benchmarks and is framed as 'a more effective collaborator.' The headline gain is honesty rather than raw capability: it is roughly four times less likely than 4.7 to overlook a flaw in code. Agentic results are strong too — it scored 84% on Online-Mind2Web browser automation, beating Opus 4.7 and GPT-5.5, and is described as the first model to clear the Legal Agent Benchmark's all-pass bar by more than 10%. 'Tool efficiency' also improved, achieving equivalent capability in fewer steps. Pricing is unchanged at $5 input / $25 output per million tokens, while Fast mode is now $10 / $50 — three times cheaper than before. The API is available immediately via claude-opus-4-8. Launching alongside it: 'Dynamic workflows' in Claude Code (running hundreds of parallel subagents), 'Effort controls' on claude.ai (adjusting compute per response), and a Messages API update allowing system entries inside the message array. Anthropic also reports lower rates of misaligned behavior, pushing capability, safety, and cost-efficiency at once.",
        "key_points_ja": [
            "4.7から短期間でOpus 4.8投入、価格は据え置き",
            "コード欠陥の見逃しが約1/4に(正直さ向上)",
            "Online-Mind2Web 84%でGPT-5.5を上回る",
            "法務ベンチの全項目合格基準を10%超えた初モデル",
            "Fast modeが従来比3倍安、Dynamic workflowsも同時公開",
            "APIは claude-opus-4-8 で即日提供、非整合挙動も低下"
        ],
        "key_points_en": [
            "Opus 4.8 lands soon after 4.7; pricing unchanged",
            "~4x less likely to miss code flaws (honesty gain)",
            "84% on Online-Mind2Web, beating GPT-5.5",
            "First to clear Legal Agent Benchmark all-pass by 10%+",
            "Fast mode now 3x cheaper; Dynamic workflows shipped too",
            "Available immediately via claude-opus-4-8; less misalignment"
        ],
    },
    {
        "source": "hn",
        "title": "YouTube to automatically label AI-generated videos",
        "title_ja": "YouTube、AI生成動画を自動でラベル付け",
        "url": "https://blog.youtube/news-and-events/improving-ai-labels-viewers-creators/",
        "hot_take_ja": "プラットフォームが『自己申告任せ』をやめにきた。内部シグナルで写実的なAI動画を自動検出し、未申告でもYouTube側がラベルを貼る。Veo製やC2PA付きは剥がせない恒久ラベル。一方で『ラベルは推薦も収益化も変えない』と明言——出所の透明化と動画への罰を切り離した、慎重な設計だ。",
        "detail_ja": "YouTubeが、写実的なAI生成・改変動画を自動で識別してラベルを付ける機能を2026年5月から展開すると発表した。これまではクリエイターの自己申告に依存していたが、新たに『内部シグナル』を導入し、未申告でも写実的AIと判定すればプラットフォーム側が自動でラベルを貼る。ラベルは長尺動画ではプレイヤー直下・説明欄の上、ショートでは動画上にオーバーレイ表示される。非写実的・アニメ・軽微な加工は説明欄内の控えめな開示に留める。誤判定にはYouTube Studioから異議申し立てができる。一方、YouTubeのVeoやDream Screenで作った動画、完全生成を示すC2PAメタデータ付きの動画は、開示を外せない『恒久ラベル』扱いになる。重要なのは、ラベル自体は推薦アルゴリズムや収益化資格を変えないと明言している点で、出所の透明化と動画への罰を意図的に切り離している。ただし具体的な検出技術は非公開で、精度と誤検知(本物を誤ってAI判定する等)のバランスが今後の論点になる。",
        "detail_en": "YouTube says it will start automatically identifying and labeling photorealistic AI-generated or meaningfully altered videos, rolling out in May 2026. Until now the system relied on creator self-disclosure; now 'new internal signals' let the platform apply a label automatically when it detects photorealistic AI even if the creator didn't disclose it. On long-form videos the label sits directly below the player, above the description; on Shorts it overlays the video. Unrealistic, animated, or lightly edited content only gets a quieter disclosure in the expanded description. Creators can challenge misidentifications via YouTube Studio. Crucially, disclosures cannot be removed for content made with YouTube's own tools (Veo, Dream Screen) or carrying C2PA metadata indicating fully generative AI. YouTube was explicit that a label alone does not change how a video is recommended or whether it can earn money — deliberately separating provenance transparency from any penalty. The detection method itself is undisclosed, so accuracy and false positives (real footage flagged as AI) will be the things to watch.",
        "key_points_ja": [
            "2026年5月から写実的AI動画を自動検出しラベル付け",
            "自己申告任せをやめ、未申告でも自動でラベル",
            "Veo製・C2PA付きは剥がせない恒久ラベル",
            "ラベルは推薦・収益化に影響しないと明言",
            "誤判定はYouTube Studioから異議申し立て可",
            "検出技術は非公開、誤検知の精度が今後の論点"
        ],
        "key_points_en": [
            "Auto-detects & labels photorealistic AI video from May 2026",
            "Moves beyond self-disclosure; labels even undisclosed AI",
            "Veo / C2PA content gets a permanent, non-removable label",
            "Labels don't affect recommendations or monetization",
            "Creators can dispute misIDs via YouTube Studio",
            "Detection method undisclosed; false positives a key risk"
        ],
    },
    {
        "source": "hn",
        "title": "DuckDuckGo search saw 28% more visits after Google said people love AI mode",
        "title_ja": "Googleの『皆AIモードを愛用』発言後、DuckDuckGoの訪問が約28%増",
        "url": "https://www.pcgamer.com/hardware/duckduckgos-ai-free-search-saw-nearly-28-percent-more-visits-in-the-week-following-googles-insistence-that-people-love-ai-mode/",
        "hot_take_ja": "語るに落ちた、の典型。Googleが「ユーザーはAIモードを気に入っている」と強調した直後の1週間で、AIなし検索を掲げるDuckDuckGoの訪問が約28%増えた。AI体験の押し付けに対する静かな反発が、ついに数字に表れた格好。プラットフォームが『みんな好き』と言うほど、逃げ場の需要が見えてくる。",
        "detail_ja": "Googleが『ユーザーはAIモードを気に入っている』と公に強調した直後の1週間で、AIを使わない検索を売りにするDuckDuckGoの訪問数が約28%増えた、とPC Gamerが報じた。DuckDuckGoは生成AI要約を前面に出すGoogleのAIモードに対し、従来型の青リンク中心の検索を明確な対抗軸として打ち出している。皮肉なのは、Googleの強気な発言そのものが反発の引き金になった可能性が高いことだ。AI要約は誤情報や出典不明の混入、サイトへの遷移(クリック)減少といった不満を抱えており、一定数のユーザーはAIなしの選択肢を求めていたとみられる。28%はあくまで週次の相対的な伸びで、検索市場の絶対シェアを覆すものではない。それでも、検索におけるAI体験の押し付けに対する静かな反発が数字として可視化された点が示唆的だ。プラットフォームが『みんな気に入っている』と語るほど、逃げ場への需要が顕在化する——という逆説を端的に示す事例といえる。",
        "detail_en": "PC Gamer reports that in the week after Google publicly insisted that 'people love AI mode,' DuckDuckGo — which markets itself on 'AI-free search' — saw roughly 28% more visits. DuckDuckGo positions traditional blue-link search as a clear counterpoint to Google's AI-summary-forward mode. The irony is that Google's own confident messaging may have been the trigger for the backlash. AI summaries draw complaints about misinformation, unsourced claims, and fewer click-throughs to websites, and a meaningful slice of users evidently wanted an AI-free option. The 28% is a relative weekly bump, not something that overturns absolute search market share. Still, it's notable that quiet resistance to having an AI experience pushed on users finally showed up in the numbers. It neatly illustrates a paradox: the louder a platform claims 'everyone loves it,' the more it surfaces demand for an escape hatch.",
        "key_points_ja": [
            "Googleの『皆AIモードを愛用』発言の直後の週",
            "『AIなし検索』のDuckDuckGo訪問が約28%増",
            "AI要約への不満(誤情報・遷移減)が背景",
            "あくまで週次の相対増、絶対シェア逆転ではない",
            "AI体験の押し付けへの静かな反発が可視化",
            "『みんな好き』と言うほど逃げ場需要が顕在化"
        ],
        "key_points_en": [
            "Came the week after Google said 'people love AI mode'",
            "AI-free DuckDuckGo saw ~28% more visits",
            "Driven by gripes with AI summaries (misinfo, fewer clicks)",
            "A relative weekly bump, not a share reversal",
            "Quiet backlash to forced AI search became visible",
            "The louder 'everyone loves it,' the clearer the demand to opt out"
        ],
    },
    {
        "source": "hn",
        "title": "Tech CEOs are apparently suffering from AI psychosis",
        "title_ja": "テックCEOが『AIサイコーシス』に——Box CEOが命名",
        "url": "https://techcrunch.com/2026/05/27/tech-ceos-are-apparently-suffering-from-ai-psychosis/",
        "hot_take_ja": "Box CEOのAaron Leviが『AIサイコーシス』と命名。経営者は価値創出の『最後の1マイル』の泥臭い作業から遠いから、プロトタイプで遊んだだけで能力を過大に外挿してしまう。ClickUpは3000体のエージェント導入後に22%解雇——『100x組織』の夢の裏で、根拠の薄い人員削減が静かに進んでいる。",
        "detail_ja": "Box CEOのAaron Levi氏が、経営者がAIの能力を過大評価する現象を『AIサイコーシス(AI psychosis)』と名付け、話題になっている。Levi氏いわく、CEOは価値創出に必要な『最後の1マイル』の泥臭い作業から距離があるため、プロトタイプを少し触っただけで能力を過大に外挿しやすい。バグ修正、幻覚したライブラリ呼び出しの検証、自社データでの学習、契約書のニュアンス確認といった現場仕事を、CEO自身はほとんど経験しないからだ。記事はClickUpを例に挙げる。同社は社内に3000体のAIエージェントを導入した後に従業員の22%を解雇し、人間は主にエージェント出力をレビューする『100x組織』を構想したという。だが研究はこうした楽観に冷や水を浴びせており、AI導入と生産性向上の間に『頑健な相関』は見られず、現状のエージェントは基礎的な能力水準にとどまるとされる。結果として、2026年前半だけで11万5430件の人員削減が『未実証のAI効率』を口実に進み、変革どころか組織の混乱を招きかねないと警告している。経営判断と現場実態の乖離こそが、このバブル的熱狂の本質だという指摘だ。",
        "detail_en": "Box CEO Aaron Levie has coined the term 'AI psychosis' for the way executives overestimate what AI can do, and it's resonating. Levie argues CEOs are uniquely prone to it because they're far from the 'last mile' of work where most AI value is actually realized — they rarely fix buggy code, verify hallucinated library calls, train models on company data, or pick apart contract nuances themselves, so they extrapolate wildly from a quick prototype. The article points to ClickUp, which laid off 22% of staff after deploying 3,000 internal AI agents and envisioned a '100x org' where humans mostly review agent output. Research undercuts that optimism: studies find no robust relationship between AI adoption and productivity gains, and today's agents perform at only baseline competence. The upshot, per the piece, is that 115,430 layoffs in early 2026 were justified by unproven AI efficiency, risking organizational chaos rather than transformation. The core problem is the gap between executive belief and ground-level reality.",
        "key_points_ja": [
            "Box CEO Aaron Leviが『AIサイコーシス』と命名",
            "CEOは『最後の1マイル』から遠く能力を過大評価",
            "ClickUpは3000体導入後に従業員22%を解雇",
            "研究はAI導入と生産性の頑健な相関を否定",
            "2026前半だけで11.5万件超の人員削減",
            "経営判断と現場実態の乖離が熱狂の本質"
        ],
        "key_points_en": [
            "Box CEO Aaron Levie coins 'AI psychosis'",
            "CEOs are far from the 'last mile,' so they overestimate AI",
            "ClickUp cut 22% of staff after 3,000 internal agents",
            "Studies find no robust AI-to-productivity link",
            "115,430 layoffs in early 2026 on unproven AI gains",
            "Gap between exec belief and reality drives the hype"
        ],
    },
    {
        "source": "hn",
        "title": "Disagreement among frontier LLMs on real-world fact-checks",
        "title_ja": "最先端LLM、実世界のファクトチェックで67%が不一致",
        "url": "https://lenz.io/research/llm-disagreement",
        "hot_take_ja": "実際のファクトチェック依頼1000件を5つの最先端モデルに判定させたら、67%で意見が割れた。完全一致はわずか33%。『真/偽』の両極は4割超が一致する一方、『概ね真/誤解を招く』の中間判定はほぼ一致ゼロ。AIを単独の『真実の裁定者』にするのは危うい、という具体的データだ。",
        "detail_ja": "Lenz Researchが、実際にユーザーから寄せられた直近のファクトチェック依頼1000件を、GPT-5.4・Claude Opus 4.7・Gemini 3 Pro・Gemini 3 Pro+検索・Sonar Proの5モデルに『真/概ね真/誤解を招く/偽』の4段階で判定させた。結果、67%(672件)で少なくとも1モデルが他と食い違い、全モデル一致はわずか33%だった。内訳は、1モデルだけ反対が22%、2モデル反対が32%、明確な多数派なしが13%。評価者間信頼性を示すKrippendorffのαは0.639にとどまり、構造化された選択肢を与えてもなお一致度は限定的だった。特に『概ね真』『誤解を招く』といった中間判定では全員一致がわずか0〜5%なのに対し、『真/偽』の両極では43〜47%が一致しており、グレーゾーンほど判定が割れる傾向が鮮明だ。モデル別では、GPT-5.4が他モデルとの一致率81%で最も高く、Claude Opus 4.7が70%で最も低かった。検索を付けたモデルでも一致が劇的に上がるわけではない点も示唆的だ。これは単一モデルの判定を真実として扱う危うさを定量的に示しており、特に微妙な主張ほど複数モデルや人間による検証が欠かせないことを物語る。",
        "detail_en": "Lenz Research had five frontier models — GPT-5.4, Claude Opus 4.7, Gemini 3 Pro, Gemini 3 Pro + Search, and Sonar Pro — classify 1,000 recent real-world fact-check submissions into True / Mostly True / Misleading / False. The result: 67% of claims (672 of 1,000) had at least one model disagreeing with the rest, and only 33% saw full agreement. The breakdown: 22% with one dissenter, 32% with two, and 13% with no clear majority. Krippendorff's α was just 0.639, indicating limited inter-rater reliability even with structured options. Disagreement was sharpest in the middle: unanimity on 'Mostly True' / 'Misleading' verdicts was only 0–5%, versus 43–47% for the polar True/False verdicts — the grayer the claim, the more they split. By model, GPT-5.4 had the highest agreement with peers at 81%, while Claude Opus 4.7 was lowest at 70%. Notably, adding search did not dramatically raise consensus. The study quantifies the risk of treating any single model's verdict as 'truth,' and argues that borderline claims especially need multiple models or human verification.",
        "key_points_ja": [
            "実ファクトチェック1000件×最先端5モデルで検証",
            "67%で不一致、完全一致はわずか33%",
            "Krippendorff α=0.639で一致度は限定的",
            "中間判定は一致0〜5%、両極は43〜47%",
            "一致率はGPT-5.4が最高(81%)、Opus 4.7が最低(70%)",
            "単一モデルを『真実の裁定者』にする危うさを定量化"
        ],
        "key_points_en": [
            "1,000 real fact-checks judged by 5 frontier models",
            "67% showed disagreement; only 33% unanimous",
            "Krippendorff α = 0.639: limited agreement",
            "Mid verdicts agree 0–5%; polar ones 43–47%",
            "GPT-5.4 highest peer agreement (81%), Opus 4.7 lowest (70%)",
            "Quantifies the risk of one model as sole 'arbiter of truth'"
        ],
    },
]

d["highlights"] = highlights

# Stats
stats = d.get("stats", {})
stats["counts"] = {
    "arxiv": len(d["sources"]["arxiv"]),
    "hn": len(d["sources"]["hn"]),
    "reddit": len(d["sources"].get("reddit", [])),
    "github": len(d["sources"]["github"]),
    "blogs": len(d["sources"]["blogs"]),
}
stats["highlights"] = len(highlights)
d["stats"] = stats

with open(OUT, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f"Wrote {OUT}")
print(f"Highlights: {len(highlights)}")
for h in highlights:
    print(f"  - [{h['source']}] {h['title_ja']}")
