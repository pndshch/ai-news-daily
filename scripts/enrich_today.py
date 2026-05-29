#!/usr/bin/env python3
"""Enrich raw-2026-05-29.json with Japanese summaries and highlights."""
import json
from pathlib import Path

DATE = "2026-05-29"
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / f"raw-{DATE}.json"
OUT = ROOT / "data" / f"{DATE}.json"

with open(RAW) as f:
    d = json.load(f)

# -------- arXiv (index-aligned with raw order) --------
arxiv = [
    ("Physics Is All You Need? 物理学者がAIエージェントで科学ソフトを開発した事例",
     "物理学者がClaude Codeを12日間57セッション監督し微分可能な摂動論モジュールを構築。エージェントは10件を自律解決したが、症状の抑制を根本解決と誤認し、表現不能なアーキテクチャの係数調整に33セッションを浪費した。"),
    ("GMOS：3D空間・時間で移動物体セグメンテーションを接地",
     "移動物体のセグメンテーションを2D画像内ではなく3D空間と時間の中で接地し、より一貫した追跡を可能にする手法。"),
    ("VideoMLA：分単位の自己回帰動画拡散のための低ランク潜在KVキャッシュ",
     "長尺動画の自己回帰生成で膨れ上がるKVキャッシュを低ランクの潜在表現に圧縮し、分単位の動画生成を実用化する手法。"),
    ("DynaFLIP：三モーダル動力学誘導表現でロボット知覚を再考",
     "視覚・深度・動力学の三モーダルを統合した表現学習で、ロボットの知覚をより頑健にするアプローチ。"),
    ("LLMSurgeon：大規模言語モデルのデータ混合を診断",
     "学習済みLLMがどんなデータ混合で訓練されたかを逆診断し、データ構成の偏りや欠落を明らかにする手法。"),
    ("AdaState：ストリーミング動画生成のための自己進化アンカー",
     "ストリーミング型の動画生成で、状態アンカーを自己進化的に更新し続けることで長時間の一貫性を保つ手法。"),
    ("NeuROK：生成的な4Dニューラル物体運動学",
     "物体の形状と時間変化する動きを同時に表現する4Dニューラル運動学を生成的に学習する手法。"),
    ("YoCausal：動画生成は世界モデルにどれだけ近いか?因果性の視点",
     "動画生成モデルが本当に世界の因果構造を捉えているのかを因果性の観点から評価し、世界モデルとの距離を測る研究。"),
    ("SchGen：意味接地コード表現によるPCB回路図生成",
     "プリント基板の回路図を、意味に接地したコード表現を介して自動生成する手法。"),
    ("Tiny but Trusted：時系列異常検知のための効率的な視覚言語推論",
     "小型の視覚言語モデルで時系列の異常を検知し、信頼できる説明付き判定を低コストで実現する手法。"),
    ("LLMの作業記憶を解放して潜在推論を行う(RiM)",
     "中間トークンを外に出力せず、固定の特殊トークン『メモリブロック』でLLMの作業記憶を活用し、単一フォワードパスで潜在的に推論する手法。"),
    ("不確実性駆動の3Dガウシアンスプラッティング能動マッピング",
     "異方的な可視性場を用い、不確実性が高い領域を優先して観測する能動的な3Dガウシアン再構成手法。"),
    ("GPIC：視覚生成のための巨大寛容画像コーパス",
     "視覚生成モデルの学習に使える、ライセンス的に寛容な巨大画像コーパスを構築・公開した研究。"),
    ("単一要因の物理的Video-to-Audio生成をベンチマーク",
     "映像から音を生成するV2Aで、物理的に正しい単一要因の音生成能力を測るベンチマーク。"),
    ("REST3D：1枚の画像から物理的に安定した3Dシーンを再構成",
     "単一画像から、物体が倒れたり浮いたりしない物理的に安定した3Dシーンを再構成する手法。"),
    ("凸再構成と勾配キャッシュによるLLMの効率的テスト時微調整",
     "推論時にモデルを微調整するコストを、凸再構成と勾配キャッシュで大幅に削減する手法。"),
    ("公平性を考慮した連合学習：軌跡シャープレイ値",
     "連合学習で各クライアントの貢献を軌跡シャープレイ値で公平に評価し、公平性を高める手法。"),
    ("局所的に整合・全体的に非整合:多要素LLMエージェントの合成的非整合を抑える",
     "部分しか見ない各コンポーネントが局所的には正しくても、合成すると確率公理を破る現象を定式化し、実行時に検知・修復する手法。"),
    ("LLM学習を高めるデータ組織化の解明",
     "LLM訓練でデータをどう並べ・束ねるか(データ組織化)が性能に与える影響を体系的に解明した研究。"),
    ("COMPOSE：引用と形式構造から未来の定理を合成",
     "論文の引用関係と形式的な数学構造から、まだ証明されていない新しい定理候補を合成する手法。"),
    ("カラードノイズ拡散サンプリング",
     "拡散モデルのサンプリングで白色ノイズではなく有色ノイズを用い、生成品質や効率を改善するアプローチ。"),
    ("拡散事後サンプラーはいつ・なぜ・どう失敗するか:有限標本の視点",
     "逆問題に使われる拡散事後サンプラーの失敗条件を、有限標本の理論的視点から分析した研究。"),
    ("SoundnessBench：AI科学者は良い研究アイデアと悪いものを見分けられるか?",
     "ICLR投稿から再構成した1,099件の研究提案でLLM12種を評価。標準プロンプトでは健全性の低い提案も『妥当』と評価する楽観バイアスが蔓延し、第一関門の審査役としてはまだ信頼できないと結論。"),
    ("深度推定でサーマル・ガウシアンスプラッティングを強化",
     "熱画像の3Dガウシアン再構成を、深度推定を組み合わせることで精度向上させる手法。"),
    ("Reasoning with Sampling：決定点で切る",
     "RL不要で推論を引き出す『べき分布サンプリング』を実用化。次トークンのエントロピーで推論の重要な分岐点を特定して再サンプルし、混合時間をトークン数でなく決定数に依存させ、RL学習モデルをも上回る精度を達成。"),
    ("RoboWits：ロボットの創造的問題解決における予期せぬ課題",
     "想定外の障害に直面したロボットが、推論・適応・創造的に問題解決できるかを測る新ベンチマーク。"),
    ("Veda：蒸留したスパースアテンションでスケーラブルな動画拡散",
     "動画拡散の二乗コストのアテンションを、蒸留したスパースアテンションで高スパース化しても品質を保ったままスケールさせる手法。"),
    ("有界メモリ下での極限における言語生成",
     "学習者がメモリ制約下で、未知の言語から例を逐次観測し最終的に新しい正しい例だけを出力できるかを理論的に解析した研究。"),
    ("頑健な選好モデリングのための文脈内報酬適応",
     "RLHFの静的な報酬モデルを、多様で異質な人間の価値観に文脈内で適応させ頑健化する手法。"),
    ("Gram：自動アラインメント監査で妨害傾向を評価",
     "AIエージェントが妨害行為に走る傾向を自動監査する枠組み。妨害を誘発する17の擬似運用シナリオでGeminiモデルを評価した。"),
    ("MonoPhysics：単眼動画から幾何・外観・物理パラメータを推定",
     "多視点の制約が無い単眼動画から、スケールの曖昧さを克服して幾何・外観・物理パラメータを同時推定する手法。"),
    ("行列補完による異質処置効果推定の改善保証",
     "パネルデータで『各個体に介入がどう効くか』という異質処置効果を、行列補完を用いて理論保証付きで推定する手法。"),
    ("Before the Shutter：3Dシーンでの審美的かつ実行可能なポートレート撮影計画",
     "被写体のポーズ・カメラ設定・照明をシャッターを切る前に3Dシーン内で協調計画する撮影支援手法。"),
    ("VPG：自己回帰的な画像・動画生成のための視覚プレフィックス誘導",
     "自己回帰生成で訓練と推論のずれ(露出バイアス)による劣化を、視覚プレフィックスの誘導で抑える手法。"),
    ("ペアLLM評価の解像度診断",
     "公開リーダーボードのペア比較ランキングの多くが、統計的検出力の基準を満たしていないと指摘する診断研究(Open LLM Leaderboard v1で40中11件など)。"),
    ("GPU支配パラダイムを超えるロボットRL向け異種アーキテクチャ",
     "物理・ロールアウト・学習を単一GPUに集約する従来手法を見直し、異種計算資源を活用するロボットRLアーキテクチャ。"),
    ("Archon：全体的デジタルヒューマン生成のための統一マルチモーダルモデル",
     "テキスト・音声・動き・映像を一体で扱い、全体的なデジタルヒューマンを生成する事前学習済み統一モデル。"),
    ("City-Mesh3R：多視点画像からシミュ可能な都市規模3Dメッシュ再構成",
     "都市規模の多視点画像から、シミュレーションにそのまま使える大規模3Dメッシュを再構成する手法。"),
    ("Grounded 3D-Aware空間視覚言語モデリング(GR3D)",
     "明示的2D・暗黙的2D・単眼3Dの3種の接地能力を単一の空間視覚言語モデルに統合した手法。"),
    ("MedCase-Structured：診断推論ベンチマーク用のText-to-FHIRデータセット",
     "電子カルテに即した現実的な設定で診断推論を評価するため、テキストをFHIR形式に変換した医療データセット。"),
    ("Leave a Window Out：時系列の予測推論のためのジャックナイフ改良",
     "交換可能性が崩れる時系列データでも妥当な予測区間を出せるよう、ジャックナイフ法を改良したコンフォーマル予測手法。"),
    ("学習時・推論時の自己改善のための自己訓練検証",
     "検証-精緻化ループ(推論時)と自己訓練(学習時)の双方を、自己訓練した検証器で統一的に強化する手法。"),
    ("数値表データの類似・検索・解釈可能なアラインメントのための統計埋め込み",
     "LLMが苦手な数値表データを、異質な特徴空間を跨いで意味的に表現できる統計的埋め込み手法。"),
    ("MIRA：ソース対応データ選択のための中間学習ルーブリック・アンカリング",
     "LLMの中間学習段階に特有のデータ選択問題を、ルーブリックでアンカリングしソースを考慮して解く手法。"),
    ("ProjectionBench：段階的情報開示下での科学的仮説生成を評価",
     "情報を段階的に開示しながら、LLMが既知知識の想起を超えて科学的仮説を生成できるかを測るベンチマーク。"),
    ("mcp-proto-okn：MCP経由で科学知識グラフへ自然言語アクセス",
     "Model Context Protocolを介して、AIアシスタントが科学知識グラフを自然言語で探索・照会・統合できるPython製MCPサーバ。"),
    ("Gaze2Act：視線条件付き視覚言語行動方策で対話的ロボット操作",
     "言語だけでは伝わりにくい人の意図を、視線情報で補ってロボット操作の方策に条件付けする手法。"),
    ("Qwen-VLA：タスク・環境・身体を跨ぐ視覚言語行動モデリングの統一",
     "操作や移動など個別タスクに分断されがちな身体性知能を、タスク・環境・ロボット身体を跨いで統一するVLAモデル。"),
    ("ニューラル演算子に基づくCFD代理モデル:小型モジュール炉の螺旋コイル蒸気発生器",
     "小型モジュール炉のデジタルツインに必要なリアルタイム熱流体シミュを、ニューラル演算子の代理モデルで高速化する研究。"),
    ("血液検査と病歴から膵臓がん検診対象をデジタルに絞り込む",
     "現状では成立しにくい膵臓がん検診を、日常的な血液指標と病歴から高リスク集団をデジタルに絞り込むことで実現可能にする研究。"),
]

# -------- HN (index-aligned) --------
hn = [
    ("Claude Opus 4.8",
     "Anthropicが最新フラッグシップ『Claude Opus 4.8』を公開。HN首位(1,710pt)で、コーディングとエージェント性能の向上が話題。"),
    ("Please Use AI",
     "『AIを使え』という命令文を皮肉に反復しながら、実は人間的なつながりや不器用な営みの価値を擁護するエッセイ。AI礼賛への静かな反論として共感を集めた。"),
    ("GitHubがWindowsゼロデイを公開したセキュリティ研究者をBAN",
     "Windowsの未修整脆弱性(ゼロデイ)を公開した研究者のGitHub/MSRCアカウントをMicrosoftが停止。報奨金ゼロへの不満や報復との非難が飛び交い、責任ある開示を巡る論争に。"),
    ("フロンティアLLM同士の事実確認の不一致",
     "複数のフロンティアLLMに同じ実世界の事実確認をさせると判断が大きく食い違うことを示した調査。LLMを真偽判定に使う危うさを浮き彫りに。"),
    ("車は驚くほど大量の個人データを収集している",
     "現代の自動車がドライバーについて収集するデータの量と種類が驚くほど膨大で、プライバシー上の懸念が大きいことを指摘した記事。"),
    ("GTA6の開発者が労働組合を結成",
     "Rockstarのゲーム開発者が労働組合を結成。ゲーム業界の労働環境とAI活用を巡る緊張が背景にある。"),
    ("Continue? Y/N：AIエージェントの許可疲れを描く60秒ゲーム",
     "AIエージェントが次々求めてくる許可確認に疲弊する開発者あるあるを、60秒のミニゲームに仕立てたShow HN。共感を呼びバズった。"),
    ("VWがclient assertion必須化でHome Assistantをブロック",
     "フォルクスワーゲンがclient assertionを要求する仕様変更で、自宅統合ソフトHome Assistantからの接続を遮断。ユーザーの自車データ利用が制限された。"),
    ("様々なLLMの『匂い』(コードの臭み)",
     "LLM生成コードに特有の悪い兆候(過剰な抽象化・冗長なコメント・定型句など)を『LLM smells』として列挙した記事。"),
    ("Claude Code:ドキュメントに載っていない設定の全て",
     "Claude Codeで設定できるがドキュメント化されていない隠し設定や挙動を網羅的に解説した記事。"),
    ("SF発スタートアップ、Airbnbでロボットを試験し部屋を破壊と訴訟",
     "サンフランシスコのスタートアップがAirbnbの部屋でロボットを試験し、損傷させたとして訴えられたという報道。物理AI実装の現実的な摩擦を象徴。"),
    ("アルトマンもアモデイもAI失業終末論を撤回",
     "かつて『多くの雇用が消える』『ホワイトカラーの50%が消滅』と警告した両CEOが一転して予測を後退。IPOを控えた時期の楽観への転換に疑念の声も。"),
    ("パリのMistral AI Now Summitのメモ",
     "パリで開かれたMistralのAIサミットの参加メモ。欧州AIの現状と方向性についての所感をまとめたもの。"),
    ("AIはフロントエンドの『失われた10年』を繰り返させているか?",
     "AIコード生成の普及が、かつてフロントエンド開発が陥った複雑化・断片化の悪循環を再来させているのではと問う論考。"),
    ("標準GPUでのリアルタイムLLM推論:リクエスト当たり毎秒3kトークン",
     "特殊ハードに頼らず標準的なGPUで、1リクエスト当たり毎秒3,000トークンというリアルタイム推論を実現したという報告。"),
    ("AIの請求ショックが米国企業を直撃",
     "AI導入の請求額が想定を大きく上回り、米企業が『スティッカーショック』に見舞われていると報じる記事。ROI懐疑論の流れと連動。"),
    ("Claude Codeの動的ワークフロー",
     "Claude Codeで複数サブエージェントを決定論的に編成する『動的ワークフロー』機能を解説した記事。"),
    ("Bitburner：プログラミングを軸にした放置型ゲーム",
     "コードを書いてハッキングを自動化していくプログラミング題材の放置系(インクリメンタル)ゲーム。"),
    ("Endive：JVMネイティブなWebAssemblyランタイム",
     "JVM上でネイティブに動作するWebAssemblyランタイム実装。"),
    ("Headway:療法の患者が顔スキャンを強制される",
     "メンタルヘルス・プラットフォームHeadwayが、療法を継続する患者に顔認証スキャンを義務付け、本人確認のあり方を巡って反発を招いている。"),
]

# -------- reddit (empty today) --------
reddit = []

# -------- GitHub (index-aligned) --------
github = [
    ("MoneyPrinterTurbo：AIで高画質ショート動画をワンクリック生成",
     "テーマを入力するだけで大規模言語モデルを使い、ナレーション・字幕・BGM付きの高画質ショート動画を一括生成するツール。"),
    ("taste-skill：AIに『良いセンス』を与えるスキル",
     "AIが退屈で凡庸な出力(slop)を生成するのを防ぎ、より良い趣味・センスを持たせるためのスキルファイル。AIの没個性化への対抗策として注目。"),
    ("ECC：エージェントハーネスの性能最適化システム",
     "Claude Code/Codex/Cursor等向けに、スキル・本能・記憶・セキュリティ・調査優先の開発を束ねたエージェントハーネス最適化システム。"),
    ("FreeDomain：誰でも使える無料ドメイン",
     "誰でも無料でドメインを取得できるDigitalPlatのサービス。リポジトリで申請を受け付けている。"),
    ("stop-slop：文章からAIらしさを除去するスキル",
     "文章に表れるAI特有の言い回し(AI tells)を取り除き、より人間らしい文章にするためのスキルファイル。"),
    ("twenty：AI時代のオープンソースSalesforce代替",
     "Salesforceに代わるオープンソースのCRM。AI活用を前提に設計されている。"),
    ("claude-code：ターミナルで動くエージェント型コーディングツール",
     "コードベースを理解し定型作業を実行するAnthropic公式のエージェント型コーディングツール。"),
    ("stable-worldmodel：再現可能な世界モデル研究の評価基盤",
     "世界モデルの研究と評価を再現可能に行うためのプラットフォーム。"),
    ("project-nomad：オフラインのサバイバル用知識コンピュータ",
     "ネット無しでも重要な道具・知識・AIを内蔵し、いつでも情報を得られる自己完結型のサバイバル用コンピュータ。"),
]

# -------- blogs (index-aligned) --------
blogs = [
    ("I/O 2026クイズをGoogle AI Studioでバイブコーディング",
     "Google DeepMindがI/O 2026のクイズをAI Studioで『バイブコーディング』した事例を紹介。"),
    ("Gemini OmniとGemini 3.5の9つのデモ",
     "GoogleがマルチモーダルなGemini OmniとGemini 3.5の実動デモを9本公開。"),
    ("ボストン小児病院がAIで新たな診断を解明",
     "OpenAIの技術を用い、ボストン小児病院が難しい症例の新たな診断にたどり着いた事例。"),
    ("BraintrustがCodexで顧客要望をコード化",
     "BraintrustがOpenAIのCodexを使い、顧客からの要望を素早くコードに落とし込む方法を紹介。"),
    ("Futures Labの実物AIプロトタイプ",
     "Google DeepMindのFutures Labによる実物のAIプロトタイプ群の紹介。"),
    ("Rosalind Biodefenseと社会のレジリエンス強化",
     "OpenAIがRosalind Biodefenseと連携し、生物学的脅威への社会的レジリエンスを高める取り組み。"),
    ("第三者評価を信頼できるものにする共通プレイブック",
     "OpenAIが、AIの第三者評価を信頼できるものにするための共通的な指針(プレイブック)を提示。"),
    ("PyTorchプロファイリング入門(Part 1):torch.profiler",
     "Hugging Faceによる、torch.profilerを使ったPyTorchの性能プロファイリング初心者向けガイド。"),
    ("I/O 2026の主要12モーメントまとめ",
     "Google I/O 2026の見どころ12点を振り返るまとめ記事。"),
    ("EndavaがCodexでエージェント型組織を構築",
     "EndavaがOpenAIのCodexを使って組織全体をエージェント型に作り変えている事例。"),
    ("MUFGがOpenAIでAIネイティブを目指す",
     "三菱UFJがOpenAIと連携し、AIネイティブな金融機関への転換を進める取り組み。"),
    ("OpenAIのフロンティアガバナンス枠組み",
     "OpenAIが、最先端AIの開発・展開を律するフロンティアガバナンスの枠組みを公開。"),
    ("ITBench-AA：フロンティアモデルが初のエージェント評価で50%未満",
     "Hugging Faceが、エージェント型エンジニアリングの新ベンチマークITBench-AAでフロンティアモデルが軒並み50%未満だったと報告。"),
    ("CiscoとOpenAIがCodexで企業エンジニアリングを再定義",
     "CiscoとOpenAIがCodexを使い、企業のエンジニアリング業務を作り変える取り組み。"),
    ("Codexで自己改善する税務エージェントを構築",
     "OpenAIのCodexを用いて、自ら改善していく税務処理エージェントを構築した事例。"),
    ("2026年の選挙情報とセーフガード",
     "OpenAIが2026年の選挙に向けて、選挙情報の扱いと不正利用防止のセーフガードを説明。"),
    ("Reachy Miniが完全ローカルで動作",
     "Hugging Faceの小型ロボットReachy Miniが、クラウドに頼らず完全ローカルで動作するようになった。"),
    ("Hubバケットで1兆パラメータを配送:TRLのデルタ重み同期",
     "Hugging FaceがHubのバケットを使い、TRLで1兆パラメータ規模のデルタ重みを効率的に同期・配送する仕組みを解説。"),
    ("Harness/Scaffoldなど押さえるべきAIエージェント用語",
     "Hugging Faceが、ハーネス・スキャフォールドなど混同しがちなAIエージェント関連用語を整理。"),
    ("Nemotron-Labs拡散言語モデルで光速級のテキスト生成へ",
     "Hugging FaceがNVIDIA Nemotron-Labsの拡散言語モデルで、従来の自己回帰生成を超える高速テキスト生成を目指す取り組みを紹介。"),
]

def apply(items, pairs):
    for it, (tja, sja) in zip(items, pairs):
        it["title_ja"] = tja
        it["summary_ja"] = sja

apply(d["sources"]["arxiv"], arxiv)
apply(d["sources"]["hn"], hn)
apply(d["sources"].get("reddit", []), reddit)
apply(d["sources"]["github"], github)
apply(d["sources"]["blogs"], blogs)

# -------- Highlights --------
d["highlights"] = [
    {
        "source": "HN",
        "title": "Sam Altman and Dario Amodei are both walking back AI jobs apocalypse predictions",
        "title_ja": "アルトマンもアモデイもAI失業『終末論』を撤回し始めた",
        "url": "https://fortune.com/2026/05/26/sam-altman-dario-amodei-walking-back-ai-jobs-apocalypse-prophecies-ipo/",
        "hot_take_ja": "「ホワイトカラーの50%が消える」と煽った当人たちが、IPOを目前にして『自分はかなり間違っていた』と前言撤回。終末論は資金調達には効いても、いざ上場で投資家に語る物語としては都合が悪い——その温度差が露骨だ。予測の中身より、誰がいつ何のために語るかを見る癖をつけたい。",
        "detail_ja": "2025年、サム・アルトマンは『多くの仕事が消える』、特にエントリーレベルのホワイトカラー職が危ういと警告し、ダリオ・アモデイは『AIがホワイトカラー職の最大50%を消し去りうる』と述べていた。それから1年経たないうちに、両者とも論調を後退させている。アルトマンは『自分はかなり間違っていた。エントリーレベルのホワイトカラー職の消滅は、今頃もっと進んでいると思っていたが、実際には起きていない』と認めた。アモデイは自動化を『仕事を奪うもの』ではなく『仕事を増やすもの』と再定義し、『仕事の90%を自動化すれば、全員が残り10%をやって生産性が10倍になる』という論法に切り替えた。Fortuneは、OpenAIとAnthropicが共に今年中に約1兆ドル評価でのIPOを準備している点を指摘している。記事は両者の撤回をIPOが直接の動機だと断定はしていないが、投資家に語る『成長と機会の物語』と、終末論的な雇用破壊の警告が両立しにくいことは明らかだ。重要なのは、同じ人物の予測が短期間で正反対に振れた事実そのものである。終末論は規制や資金調達の場面では注目と緊張感を生むが、上場の物語としてはリスク要因になる。AIの雇用影響を語る言説は、語り手の立場・タイミング・利害から切り離して受け取ってはいけない、という教訓を示している。",
        "detail_en": "In 2025, Sam Altman warned that 'a lot of jobs will go away,' especially entry-level white-collar roles, and Dario Amodei claimed AI could eliminate up to 50% of white-collar jobs. Less than a year later, both have softened their tone. Altman now admits he was 'pretty wrong,' saying, 'I thought there would have been more impact on entry-level white-collar jobs being eliminated by now than has actually happened.' Amodei reframed automation as a job multiplier rather than an eliminator: 'If you automate 90% of the job, then everyone does the 10% of the job and 10-times their productivity.' Fortune notes that both OpenAI and Anthropic are preparing IPOs this year, each at an estimated $1 trillion valuation. The piece does not flatly claim the IPOs caused the reversals, but the tension is obvious: an apocalyptic story about wiping out jobs is hard to reconcile with the growth-and-opportunity narrative you tell investors. The striking fact is simply that the same people's forecasts swung to the opposite pole in under a year. Doomerism generates attention and urgency in regulatory and fundraising contexts, but it becomes a liability in an IPO story. The lesson: claims about AI's labor impact should never be taken apart from the speaker's position, timing, and incentives.",
        "key_points_ja": [
            "2025年:アルトマン『多くの職が消える』、アモデイ『WC職の50%消滅』",
            "1年弱で両者とも論調を後退",
            "アルトマン『自分はかなり間違っていた』と明言",
            "アモデイは自動化を『雇用の倍増装置』に再定義",
            "両社とも今年IPO予定(各社評価~1兆ドル)",
            "予測は語り手の立場・利害から切り離せない"
        ],
        "key_points_en": [
            "2025: Altman 'jobs go away', Amodei 'up to 50% of WC jobs'",
            "Both walked it back in under a year",
            "Altman admits he was 'pretty wrong'",
            "Amodei reframes automation as a job multiplier",
            "Both firms eyeing ~$1T IPOs this year",
            "Forecasts inseparable from speaker's incentives"
        ]
    },
    {
        "source": "arXiv",
        "title": "Reasoning with Sampling: Cutting at Decision Points",
        "title_ja": "RLなしで推論を引き出す:『決定点で切る』サンプリング",
        "url": "https://arxiv.org/abs/2605.30327v1",
        "hot_take_ja": "フロンティアの推論力は本当にRL学習で『後付け』されたものなのか?——ベース模型から『鋭くした分布』をうまくサンプリングするだけで、RL学習済みモデルをも上回ったという主張。鍵は、推論の些末な言い回しではなく『証明戦略の選択』のような分岐点を狙って引き直すこと。推論能力はベースモデルに既に眠っていて、引き出し方の問題だった可能性を示唆する。",
        "detail_ja": "最先端の推論モデルは通常、ベースの言語モデルを強化学習(RL)で事後訓練して作る。しかし近年、RLや専用データ・検証器なしでも、ベースモデルの分布を『鋭くした』べき分布(power distribution)からサンプリングするだけで同等の推論が引き出せることが示されてきた。問題は、このべき分布から効率よくサンプリングするには、分布の異なるモード(直感的には異なる推論戦略)を行き来して『混合』する必要がある点だ。従来手法は推論トレース中の『切る位置』を一様ランダムに選んで以降を再サンプルしていたが、推論トレースの大半は些末な記述で、重要な判断(証明戦略やアルゴリズムの選択)はごく少数しかない。一様な切り方では局所的な言い回しを書き換えるだけで、肝心の分岐点に戻れない。本研究の『Entropy-Cut Metropolis-Hastings』は、ベースモデルの次トークン・エントロピーを手がかりに重要な決定点を特定し、そこから再サンプルする。エントロピーの急上昇が決定点の良い代理指標になることを実証し、単純化したモデルでは混合時間がトークン数ではなく『決定の数』に比例して短縮されることを証明した。MATH500・HumanEval・GPQA Diamond・AIME26で、ベースラインだけでなくRL学習済みモデルをも一貫して上回ったという。これは、推論能力がベースモデルに既に潜在し、適切なサンプリングで顕在化できるという見方を補強する。",
        "detail_en": "Frontier reasoning models are normally built by post-training a base language model with reinforcement learning (RL). Recent work, however, has shown that comparable reasoning can be elicited without any RL, curated data, or verifiers—simply by sampling from a 'sharpened' version of the base model's distribution, a so-called power distribution. The catch is that efficiently sampling from this power distribution requires the sampler to 'mix' by moving between modes of the distribution (intuitively, trying different reasoning strategies). Prior samplers pick a 'cut' position in the current reasoning trace uniformly at random and resample the suffix. But reasoning traces are mostly filler, with only a few consequential decisions (e.g., choice of proof strategy or algorithm); a uniform cut tends to rewrite local details rather than revisit those decision points. This paper's Entropy-Cut Metropolis-Hastings uses the base model's next-token entropy as a proxy to find key decision points and resamples from there. The authors show entropy spikes are a useful proxy for decisions, and prove that in a stylized model the mixing time scales with the number of decisions in a trace rather than the (far larger) number of tokens. Across MATH500, HumanEval, GPQA Diamond, and AIME26, it consistently beats baselines and even RL-trained models. The result reinforces the view that reasoning ability already latently exists in the base model and can be surfaced with the right sampling.",
        "key_points_ja": [
            "RL不要で『べき分布』サンプリングが推論を引き出す",
            "従来は切る位置を一様ランダムに選び非効率",
            "推論の重要な分岐点はごく少数だけ",
            "次トークンのエントロピーで決定点を特定して再サンプル",
            "混合時間がトークン数でなく決定数に依存",
            "RL学習済みモデルをも上回る精度"
        ],
        "key_points_en": [
            "Power-distribution sampling elicits reasoning, no RL",
            "Prior cuts chosen uniformly at random—inefficient",
            "Only a few decisions in a trace truly matter",
            "Use next-token entropy to find & resample decisions",
            "Mixing time scales with #decisions, not #tokens",
            "Beats baselines and even RL-trained models"
        ]
    },
    {
        "source": "arXiv",
        "title": "SoundnessBench: Can Your AI Scientist Really Tell Good Research Ideas from Bad Ones?",
        "title_ja": "AI科学者は良い研究アイデアと悪いものを見分けられるか?",
        "url": "https://arxiv.org/abs/2605.30329v1",
        "hot_take_ja": "『AIが研究を自動化する』前に、AIはそもそも研究アイデアの良し悪しを判定できるのか?ICLR投稿1,099件で12モデルを試したら、健全性の低い提案も平気で『妥当』と通す楽観バイアスが蔓延。逆にきつく詰めると今度は良案まで却下しはじめる。自律研究の第一関門を任せるには、まだ早い。",
        "detail_ja": "自律的なAI研究エージェントは、仮説生成からピアレビューまで研究パイプラインの自動化を目指す。しかし既存のベンチマークは、ある根本的なボトルネック——『時間や計算資源を投じる前に、その研究アイデアが方法論的に成立しうるかをLLMが判断できるか』——をほとんど検証してこなかった。本研究はSoundnessBenchを導入する。これはICLR投稿から再構成した1,099件の機械学習研究提案に、査読者の健全性サブスコアを付与し、元論文と突き合わせて監査したベンチマークだ(完成論文の最終的な採否予測ではなく、提案段階で回復可能な『健全性』を測るものと位置づけられる)。12のフロンティアLLMで評価した結果、標準的なプロンプトでは健全性の低い提案も『妥当』と評価してしまう楽観バイアスが広く見られた。一方、厳しく評価させるよう強くプロンプトすると、誤りは偽陽性(悪い案を通す)から偽陰性(良い案を却下する)へと大きく移るだけで、根本的な信頼性は改善しなかった。著者らは、公開コーパスの汚染・論文特定フレーズ・表層特徴・人手監査の質といった交絡要因を統制しても、この挙動が単一の要因では説明できないことを示している。結論として、現在のLLMは科学的厳密さを判定する『第一関門の単独評価者』としてはまだ信頼できない。自律研究を語る前に、その入口の判断能力に大きな穴があることを突きつける結果だ。",
        "detail_en": "Autonomous AI research agents aim to automate the research pipeline from hypothesis generation to peer review. Yet existing benchmarks rarely test a fundamental bottleneck: whether an LLM can judge the methodological viability of a research idea before time and compute are spent on it. This paper introduces SoundnessBench, a curated set of 1,099 machine-learning research proposals reconstructed from ICLR submissions, labeled with reviewer soundness sub-scores and audited against the source papers. It is framed as a benchmark for recoverable proposal-stage soundness, not exact prediction of full-paper outcomes. Across 12 frontier LLMs, the authors find a pervasive optimism bias: under standard prompting, models frequently rate low-soundness proposals as sound. Aggressive prompting doesn't fix this—it merely shifts errors from false positives (passing bad ideas) to false negatives (rejecting good ones). Controls for public-corpus contamination, paper-identifying phrases, surface features, and human-audit quality suggest the behavior isn't explained by a single confounder. The conclusion: current LLMs are not yet reliable as standalone first-gate evaluators of scientific rigor. Before we talk about automating research, this exposes a large hole at its very entrance—the ability to tell a viable idea from an unviable one.",
        "key_points_ja": [
            "ICLR投稿から1,099件の研究提案ベンチマークを構築",
            "査読者の健全性スコアで正解付け・元論文と監査",
            "12モデルに共通する『楽観バイアス』を発見",
            "悪い提案も標準プロンプトでは『妥当』と評価",
            "厳しくすると誤りが偽陽性→偽陰性に移るだけ",
            "自律研究の第一関門役にはまだ不十分"
        ],
        "key_points_en": [
            "1,099 ICLR-derived research proposals as a benchmark",
            "Labeled by reviewer soundness, audited vs. sources",
            "Pervasive 'optimism bias' across all 12 models",
            "Bad proposals rated 'sound' under standard prompts",
            "Strict prompting just shifts FP errors to FN",
            "Not yet reliable as a first-gate research evaluator"
        ]
    },
    {
        "source": "HN",
        "title": "Please Use AI",
        "title_ja": "『どうかAIを使ってください』——皮肉で綴る人間擁護論",
        "url": "https://shawnsmucker.substack.com/p/please-use-ai",
        "hot_take_ja": "『AIを使え』と連呼するほど、逆に人間にしかできない不器用さの尊さが浮かび上がる——徹頭徹尾アイロニーで書かれたエッセイ。友人に料理を聞けば父の闘病の話が返ってくる、その『非効率』こそが人生だと著者は言う。AI最適化への疲れが溜まる今、静かに刺さる一篇。",
        "detail_ja": "作家ショーン・スマッカーによるエッセイ『Please Use AI』は、タイトルとは裏腹に、AIへの過度な依存に対する痛烈な皮肉として書かれている。『友人にレシピを聞く代わりにAIを使え』『旅行の計画は詳しい仲間でなくAIに任せろ』『結婚式の祝辞もAIに書かせろ』——こうした『AIを使え』という命令を反復することで、著者はむしろそこで失われるものを際立たせる。友人にレシピを尋ねれば、ついでに父親の闘病の近況が聞ける。旅の計画を仲間と立てれば、その過程自体が思い出になる。祝辞を自分で書けば、生きてきた実感が言葉に宿る。効率の名のもとに、こうした人間同士の『無駄で不器用なやり取り』を手放すべきではない、というのが核心だ。エッセイは死・加齢・ノスタルジアといった主題に触れ、子どもの成長や自らの身体の衰えを見つめながら、人生の意味は『微妙な不完全さ』の中にこそ宿ると説く。意味のあるものは最初は必ず下手で難しい、その不器用さを通過することにこそ価値がある、と。HNで677ポイントを集めたのは、AIによる最適化が生活のあらゆる場面に浸透する中で、多くの人が言語化できずにいた違和感を、皮肉という形で的確に掬い上げたからだろう。技術論ではなく、AI時代の『何を自動化し、何を手元に残すか』という価値選択を問う一篇である。",
        "detail_en": "Writer Shawn Smucker's essay 'Please Use AI' is, despite its title, a sharp piece of irony aimed at over-reliance on AI. By repeatedly issuing the command 'use AI'—use it instead of asking a friend for a recipe, instead of planning a trip with a knowledgeable companion, instead of writing your own wedding toast—the author actually throws into relief everything that gets lost in the process. Ask a friend for a recipe and you also hear how their father's illness is going. Plan a trip together and the planning itself becomes a memory. Write your own toast and the lived experience seeps into the words. The core argument: in the name of efficiency, we shouldn't surrender these 'inefficient, clumsy' human exchanges. The essay dwells on mortality, aging, and nostalgia—watching his children grow and his own body decline—and argues that life's meaning resides precisely in its 'subtle imperfections.' Anything meaningful is awkward and difficult at first, and the value lies in passing through that clumsiness. It drew 677 points on HN likely because, as AI optimization seeps into every corner of daily life, it captured—through irony—an unease many people felt but couldn't articulate. It is less a tech argument than a values question for the AI era: what should we automate, and what should we keep in our own hands?",
        "key_points_ja": [
            "タイトルとは逆に、AI依存への皮肉として書かれている",
            "『AIを使え』の反復で失われるものを際立たせる",
            "レシピを友に聞けば父の闘病の話も返ってくる",
            "人生の意味は『微妙な不完全さ』に宿ると説く",
            "意味あるものは最初は下手で難しい、それでいい",
            "何を自動化し何を手元に残すかの価値選択を問う"
        ],
        "key_points_en": [
            "Despite the title, it's irony against AI dependence",
            "Repeating 'use AI' highlights what's lost",
            "Asking a friend for a recipe brings real connection",
            "Life's meaning lives in 'subtle imperfections'",
            "Meaningful things are clumsy at first—and should be",
            "A values question: what to automate, what to keep"
        ]
    },
    {
        "source": "HN",
        "title": "GitHub bans security researcher who posted zero-day Windows exploits",
        "title_ja": "GitHubがWindowsゼロデイを公開した研究者をBAN——開示と報復の境界",
        "url": "https://www.tomshardware.com/tech-industry/cyber-security/microsofts-github-bans-security-researcher-who-posted-zero-day-windows-exploits-because-company-ruined-their-life-expert-claims-action-is-vindictive-and-promises-further-retaliation",
        "hot_take_ja": "脆弱性を見つけたのに報奨金はゼロ、連絡も無視され、挙げ句にプラットフォームを追放——研究者『Eclipse』はMicrosoftの対応を『報復的』と非難。一方で未修整のゼロデイをGitHubに公開する行為自体も危うい。プラットフォームを握る企業が、自社製品の脆弱性を暴く研究者の発信手段ごと止められる、という構図の生々しさが核心だ。",
        "detail_ja": "Nightmare-Eclipse(別名Chaotic Eclipse)を名乗るセキュリティ研究者が、Windowsの未修整脆弱性(ゼロデイ)のエクスプロイトをGitHub上で公開した。これを受けMicrosoftは同研究者のGitHubアカウントを停止し、バグ報告に使うMSRC(Microsoft Security Response Center)のアカウントも削除したと報じられている。研究者側は、複数のゼロデイを発見したにもかかわらず『1セントも受け取れなかった』と主張し、Microsoftが連絡の試みを無視したと不満を述べている。Microsoftのバグ報奨金は特定のエクスプロイトに最大25万ドルを提示しているだけに、報われなさへの憤りは強い。研究者はブログでMicrosoftの措置を『報復的(vindictive)』と非難し、7月14日にさらなる行動を取ると予告した(過激な表現も含む)。BAN後はGitLabへ活動を移している。この一件は二つの論点を孕む。第一に、未修整のゼロデイを公にする『フルディスクロージャ』は、ベンダーへの圧力になる一方で攻撃者に武器を与えるため、責任ある開示の規範と鋭く対立する。第二に、より構造的な問題として、プラットフォーム(GitHub)を保有する当事者(Microsoft)が、自社製品の欠陥を暴く研究者の発信チャネルそのものを停止できるという利益相反がある。脆弱性開示の力学、報奨金制度の信頼性、そしてプラットフォーム権力の集中——これらが交差する象徴的な事例として注目を集めた。",
        "detail_en": "A security researcher going by Nightmare-Eclipse (also Chaotic Eclipse) publicly posted exploits for unpatched Windows vulnerabilities (zero-days) on GitHub. In response, Microsoft reportedly suspended the researcher's GitHub account and deleted their MSRC (Microsoft Security Response Center) account used for bug reporting. The researcher claims to have found multiple zero-days yet 'got zero pennies from doing so,' and says the company ignored their attempts to communicate. With Microsoft's bug bounty offering up to $250,000 for certain exploits, the sense of going unrewarded fuels the anger. In a blog post the researcher called Microsoft's actions 'vindictive' and promised further action on July 14 (including some extreme language), and has since moved their work to GitLab. The episode raises two issues. First, full disclosure of unpatched zero-days pressures the vendor but also arms attackers, putting it in sharp tension with responsible-disclosure norms. Second, and more structurally, there is a conflict of interest in a platform owner (Microsoft) being able to shut down the very channel a researcher uses to expose flaws in that same owner's products. As a case where the dynamics of vulnerability disclosure, the credibility of bounty programs, and the concentration of platform power all intersect, it drew significant attention.",
        "key_points_ja": [
            "研究者がWindowsゼロデイのエクスプロイトをGitHubに公開",
            "MicrosoftがGitHubとMSRCのアカウントを停止",
            "研究者『複数のゼロデイで報奨金は1円も貰えず』",
            "措置を『報復的』と非難、活動はGitLabへ移行",
            "未修整ゼロデイの公開は責任ある開示と対立",
            "プラットフォーム保有企業が発信手段を止める利益相反"
        ],
        "key_points_en": [
            "Researcher posted Windows zero-day exploits on GitHub",
            "Microsoft suspended their GitHub and MSRC accounts",
            "Claims multiple zero-days but 'zero pennies' paid",
            "Calls it 'vindictive'; moved work to GitLab",
            "Full disclosure clashes with responsible-disclosure norms",
            "Conflict: platform owner can cut a critic's channel"
        ]
    }
]

# -------- stats --------
counts = {
    "arxiv": len(d["sources"]["arxiv"]),
    "hn": len(d["sources"]["hn"]),
    "reddit": len(d["sources"].get("reddit", [])),
    "github": len(d["sources"]["github"]),
    "blogs": len(d["sources"]["blogs"]),
}
d["stats"] = {
    "arxiv_count": counts["arxiv"],
    "hn_count": counts["hn"],
    "reddit_count": counts["reddit"],
    "github_count": counts["github"],
    "blogs_count": counts["blogs"],
    "total": sum(counts.values()),
    "counts": counts,
    "highlights": len(d["highlights"]),
}

with open(OUT, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f"Wrote {OUT}")
print("stats:", d["stats"])
