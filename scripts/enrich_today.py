#!/usr/bin/env python3
"""Enrichment for 2026-05-18 (fresh page).

arXiv set is fully new (50 items, all translated below).
HN/Reddit/GitHub/blogs reuse prior Japanese translations for overlapping
URLs (from data/2026-05-17.json) and translate new items inline.
Five fresh highlights are selected for the day.
"""
import json
from pathlib import Path

DATE = "2026-05-18"
PREV = "2026-05-17"
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
    "2605.16258v1": (
        "IVGT: ニューラルシーン表現のための暗黙的視覚幾何トランスフォーマ",
        "ポーズ未知の多視点画像から、点群を明示的に回帰するのではなく連続的な暗黙関数として3D幾何を学習。任意視点のRGB・深度・法線を生成でき、メッシュ復元や姿勢推定でも高性能を示す。"),
    "2605.16257v1": (
        "DexJoCo: MuJoCo上の器用なマニピュレーション・ベンチマーク",
        "多指ハンドならではの器用な操作タスクを体系的に評価するためのベンチマークとツールキット。平行グリッパーでは不可能な操作に焦点を当てる。"),
    "2605.16255v1": (
        "AI時代のデータセンター電力供給階層の設計",
        "AIアクセラレータの需要で1ラック1MWに迫る電力密度に対し、電力を無駄なく使い切る供給階層の設計枠組みを提案。Azureの実データを用い『据付MWでなく時間あたりの利用可能容量』を計画指標とすべきと示す。"),
    "2605.16250v1": (
        "公共料金請求のCO2分析のための生成AIフレームワーク",
        "電力会社の検針・請求・炭素計算・需要調整を一つのアーキテクチャに統合する生成AI基盤を提案。1kWhごとに根拠ある炭素値を付与する。"),
    "2605.16245v1": (
        "AIを介したコミュニケーションは集団の世論を動かしうる",
        "LLMが人間の文章を編集する際に争点(銃規制・無神論など)で方向性のあるバイアスを混入させることを実証。SNSを介して増幅され集団世論を押し動かしうると数理モデルで示し、X『Explain this post』の中絶バイアスも検出した。"),
    "2605.16241v1": (
        "VLA-AD: 視覚言語モデルを使ったVLA方策のオフライン蒸留",
        "数十億パラメータの視覚言語行動(VLA)方策を、視覚言語モデルをオフラインの意味教師として用いて軽量モデルへ蒸留。リアルタイム制御の障壁となる推論コストを下げる。"),
    "2605.16239v1": (
        "フローマッチングモデルの『動力学レベル』電子透かし",
        "出力や重みでなく、フローマッチングモデルが学習する速度場(連続的な動力学)そのものに鍵依存の摂動として透かしを埋め込む手法。連続チャネル上のランダム符号化として定式化する。"),
    "2605.16238v1": (
        "LLM主導の木探索による多病原体の感染症予測",
        "LLMがツリー探索で予測ソフトを自律生成・最適化し、2025-26シーズンにインフル・COVID・RSVを実時間予測。生成モデルのアンサンブルがCDCの専門家手作りモデルに匹敵・凌駕した。"),
    "2605.16234v1": (
        "層の等価性は層単体の性質ではない——テスト方法で結論が変わる",
        "トランスフォーマの層が圧縮目的で『等価』かを問う際、置換テストと交換テストが混同されがちだと指摘。冗長性の検証方法しだいで見つかる結論が変わることを示す。"),
    "2605.16233v1": (
        "FORGE: 重み更新なしで自己進化するエージェント記憶",
        "勾配更新を使わず、自己生成した自然言語の記憶を集団ベースで進化させ意思決定を改善するプロトコル。Reflexion型の内ループを失敗最適化で包む。"),
    "2605.16232v1": (
        "スマートエネルギー基盤のための統合生成AIフレームワーク",
        "スマートメータリング・生成AI・量子着想の組合せ最適化を統合し、ガス配給や請求、炭素分析を扱うエネルギー事業者向け基盤。"),
    "2605.16230v1": (
        "原子座標からの汎用的な磁気構造予測を実験並み精度で",
        "決定が難しい磁気構造を原子座標から予測する汎用モデル。実材料に現れる非共線・不整合な秩序も実験に近い精度で扱える。"),
    "2605.16223v1": (
        "デザイン動画生成の評価——構成的忠実度の指標",
        "デザインアニメーションは『どの部品をどう動かすか』が指定される構造的制約を持つ。自然動画とは異なるこの領域に標準的な評価枠組みを提案する。"),
    "2605.16222v1": (
        "損傷を与えた言語モデルにおける『人工失語症』",
        "脳損傷で生じる失語症に着想し、言語モデルに局所的な『損傷』を与えてその機能構成を解析。創発的な言語機能の組織化を症状プロファイルで特徴づける。"),
    "2605.16219v1": (
        "テールリスク学習のプライバシー代償",
        "差分プライバシー下のCVaR学習では実効的な標本サイズがnでなくnτ(εnτ)になることを示す。プライバシーの代償が統計誤差と分離できると理論的に明らかにした。"),
    "2605.16217v1": (
        "Argus: スケーラブルな深層リサーチエージェントのための証拠組立て",
        "深層リサーチの回答が相補的な証拠の断片で構成される点に着目し、並列探索した証拠を組み立てる手法。単一の軌跡しか辿らないReActの限界を超える。"),
    "2605.16215v1": (
        "Fully Open Meditron: 監査可能な臨床LLMのパイプライン",
        "重みだけ公開する『オープン』臨床LLMの不透明さを問題視し、データ来歴・キュレーション・生成手順まで完全公開する監査可能なパイプラインを提示する。"),
    "2605.16211v1": (
        "仮説駆動によるメソスコピックな動力学の構築",
        "固定の有効方程式から始める従来の科学モデリングに代わり、メソスコピックな動力学をモデル内で学習する枠組み。多スケール系の解析の難しさに対処する。"),
    "2605.16208v1": (
        "数値求積によるスケーラブルなノンパラメトリック生存時間モデル",
        "尤度推定に必要な扱いにくい積分を数値求積で解く深層生存時間モデルQSurv。高次元データの複雑な時間変化ハザードを柔軟に捉える。"),
    "2605.16207v1": (
        "正解は確認できても残りを見逃す——LLM家庭教師の弱点",
        "最適・妥当だが非最適・誤りの3種の生徒解答を区別する診断能力をLLM家庭教師で評価。最もフィードバックが重要な場面で識別に失敗しがちと示す。"),
    "2605.16205v1": (
        "文脈・推論・階層: 敵対的POMDPでの複合LLMエージェント設計の費用対効果",
        "敵対的で部分観測の逐次環境に複合LLMエージェントを配備する際の設計次元(何を見せ、どう推論し、どう分解するか)を費用対性能で体系的に検証する。"),
    "2605.16198v1": (
        "形式手法とLLMの融合——先進AIのコンプライアンス監査・監視・介入",
        "AI製品の開発ライフサイクル全体を監視・監査する技術を、形式手法と最新MLの原理を組み合わせて提案するAIガバナンスの研究。"),
    "2605.16194v1": (
        "paper.json: LLMエージェントが扱える論文のための協調規約",
        "LLMが論文の最初の(時に唯一の)読者となる現状で、サブ主張の引用や再現手順抽出の失敗を防ぐため、論文に機械可読の構造化規約を付ける提案。"),
    "2605.16193v1": (
        "較正された価値ペルソナによる異文化サーベイ・シミュレーションの改善",
        "LLMで世論調査を模擬する際、社会人口統計でなく『価値観』に基づくペルソナを較正することで、文化を越えた回答分布の再現性を高める。"),
    "2605.16191v1": (
        "LLM主導の木探索による3次元太陽電池構造の最適化",
        "汎用コーディングエージェントとLLM駆動の木探索を組み合わせ、高効率な3次元太陽電池(3DPV)構造を自律的に発見。AIによる科学的仮説生成の事例研究。"),
    "2605.16184v1": (
        "Asteria: スケーラブルなLLM訓練のための実行時統括型2次最適化",
        "標本効率の良い2次法の実用化を阻む大きな最適化状態の維持コストを、実行時システムで切り離して解消するAsteriaを提案する。"),
    "2605.16179v1": (
        "MAgSeg: マルチモーダルLLMによる高解像度衛星画像の農地セグメンテーション",
        "細分化された区画やラベル不足が課題のグローバルサウスの農地を、マルチモーダルLLMでセグメンテーションする手法。"),
    "2605.16175v1": (
        "小児ECMOの臨床判断支援のための模倣学習",
        "高複雑度かつデータ希少な小児の体外式膜型人工肺(ECMO)治療を模倣学習でモデル化し、刻々の介入判断を支援する。"),
    "2605.16171v1": (
        "Res^2CLIP: 残差対残差アラインメントによる少数ショット異常検知",
        "未知カテゴリへ再学習なしで汎化する少数ショット異常検知。CLIPベース手法の粗いテキストプロンプトの限界を残差アラインメントで克服する。"),
    "2605.16170v1": (
        "BAPR: 非定常な連続制御のためのベイズ的健忘ロバスト強化学習",
        "安定期と急な変化が交互に来る『区分定常』環境で、過度に保守的でも変化に脆くもない強化学習方策を学習する。"),
    "2605.16165v1": (
        "マルチモーダルモデルのモダリティ競合を抑える2次の多階層分散補正",
        "画像生成と文章理解を統一する自己回帰学習で生じるモダリティ間の勾配不均質を、2次情報を使った分散補正で安定化し大バッチ学習を可能にする。"),
    "2605.16164v1": (
        "暗黙的な自由エネルギー最小化によるエントロピー的オートエンコーディング",
        "VAEの宿痾である事後崩壊(潜在変数が無視される失敗)を、明示的な事前分布の押し付けでなく自由エネルギー最小化で回避する手法。"),
    "2605.16163v1": (
        "SwAIther-Precip: リードタイム考慮のバイアス補正でスイスの降水を高解像度化",
        "全球AI気象モデルの降水予測を、リードタイムを考慮したバイアス補正でスイスの複雑地形上にキロメートル規模へダウンスケールする。"),
    "2605.16154v1": (
        "結果が分岐する場所を学べ——確率的チャンクマスクで効率化するVLA強化学習",
        "視覚言語行動方策の強化学習で、タスクの成否が分かれる重要な区間を確率的に特定し、計算コストの高い事後学習を効率化する。"),
    "2605.16153v1": (
        "二者道徳理論の代数的説明",
        "意図的な加害者と脆弱な被害者という二者テンプレートに基づく道徳判断の心理モデルを、構造的因果モデルの記法で形式化する。"),
    "2605.16147v1": (
        "ピクセル空間の拡散トランスフォーマにレジスタトークンは効く",
        "ViTの高ノルム外れ値トークンを抑えるレジスタトークンが、ピクセル空間で訓練する拡散トランスフォーマでも有効だと示す。"),
    "2605.16145v1": (
        "歪み適応型の等角予測",
        "点予測を中心にした非対称な区間族から導く適合度スコアを使い、回帰の分割等角予測を歪んだ分布に適応させる拡張。"),
    "2605.16143v1": (
        "跳ぶ前に見よ——LLMエージェントの自律的探索",
        "LLMエージェントが未知環境で『早すぎる活用』により失敗する点に着目し、十分な環境情報を得る前に行動しないための自律的探索能力を定式化する。"),
    "2605.16142v1": (
        "プランニングのための性質誘導型LLMプログラム合成",
        "プログラムの良し悪しを単純な数値スコアで判定する従来手法は『なぜ失敗したか』の指針を与えない。性質に基づく誘導で合成を改善する。"),
    "2605.16138v1": (
        "SNAC-Pack: 代理モデルによるニューラルアーキテクチャ協調設計パッケージ",
        "精度のみや当てにならない代理指標に頼るNASを改め、FPGA展開のハードウェアコストを正しく反映する協調設計ツールを提供する。"),
    "2605.16137v1": (
        "STABLE: 意味-物理の二重系によるシミュレーション対応の卓上レイアウト生成",
        "LLMのみに頼ると物体の衝突や浮きが生じる卓上シーン生成を、意味理解と物理を組み合わせてシミュレーション可能な配置として生成する。"),
    "2605.16134v1": (
        "幾何を意識したシャープネス最小化で『穴』を避ける",
        "全方向を一律に扱う従来のSAMに対し、学習した前処理行列で損失地形の幾何を考慮し平坦な最小値へ導くLLQR+SAMを提案する。"),
    "2605.16127v1": (
        "WeatherOcc3D: VLM支援による悪天候対応の3D意味的占有予測",
        "低照度でカメラが、後方散乱でLiDARが劣化する悪天候下でも頑健な3D意味的占有予測を、視覚言語モデルの支援で実現する。"),
    "2605.16126v1": (
        "橋を渡るエントロピー——フロー/シュレディンガー・サンプラーの条件-周辺離散化",
        "限られた推論予算でフローベース生成モデルの計算をどこに配分するかが品質を左右する点に着目し、推論グリッドの設計を改善する。"),
    "2605.16122v1": (
        "GenShield: AI生成画像の検出とアーティファクト補正の統合",
        "写実性を増すAI生成画像について、検出だけでなく検出後のアーティファクト補正までを統合的に行う枠組み。偽情報対策やデジタル鑑識を念頭に置く。"),
    "2605.16118v1": (
        "マルチフィデリティ・フローマッチング: PDE解のカスケード的精緻化",
        "フローマッチングの始点分布を既定の等方事前でなくデータに較正できる点を活かし、PDE解を低精度から高精度へ段階的に精緻化する。"),
    "2605.16117v1": (
        "SGR: 外部サブグラフ生成を伴うLLMの段階的推論フレームワーク",
        "深い推論を要する複雑な設定で限界のあるLLMに対し、外部サブグラフを生成しながら段階的に推論を進める枠組み。"),
    "2605.16116v1": (
        "ShopGym: ECウェブエージェントの現実的シミュレーションとベンチマーク基盤",
        "実店舗は現実的だが非定常で検証が難しい。意味あるタスク構造を保ちつつ再現可能・スケーラブルにECウェブエージェントを評価する統合枠組み。"),
    "2605.16115v1": (
        "衝突回避を超えて——緊急避難時の複数ロボットの譲り合いと空間アフォーダンス",
        "歩行者と共存する移動ロボットが、狭い緊急避難で衝突回避だけでなく環境のアフォーダンスや人の空間を考慮して安全に振る舞う手法。"),
    "2605.16114v1": (
        "クロックレスな再構成可能チップ上の自律スパイク動力学による神経模倣計算",
        "クロックを持たない非同期デジタル回路の自律的な時間連続発展から生じるスパイク動力学に基づく、スケーラブルな神経模倣アーキテクチャをFPGAで実装。"),
}

# ─── New HN / Reddit / GitHub / blog items (url → title_ja, summary_ja) ───
new_url_map = {
    # ── HN ──
    "https://github.com/MinishLab/semble": (
        "Show HN: Semble——grepより98%少ないトークンで動くエージェント向けコード検索",
        "AIコーディングエージェントがコードベースを検索する際、grepと比べて消費トークンを98%削減できると謳う検索ツール。文脈窓とAPIコストの節約を狙う。"),
    "https://gencad.github.io/": (
        "GenCAD——生成AIによるCAD設計",
        "テキストや画像からパラメトリックなCADモデルを生成する研究プロジェクト。AIをエンジニアリング設計の現場に持ち込む試み。"),
    "https://github.com/zakirullin/files.md": (
        "Show HN: Files.md——オープンソースのObsidian代替",
        "プレーンなMarkdownファイルでノートを管理する、Obsidianのオープンソース代替ツール。"),
    "https://www.nbcnews.com/tech/tech-news/former-google-ceo-booed-graduation-speech-ai-rcna345585": (
        "元Google CEOエリック・シュミット、AIを語る卒業式スピーチでブーイング",
        "アリゾナ大学の卒業式でシュミット氏が『AIはあらゆるものでAIが仕事のやり方になる』と語ると、AIによる雇用喪失を恐れる卒業生から大きなブーイングが起きた。"),
    "https://github.com/stephenlthorn/auto-identity-remove": (
        "Show HN: Auto-identity-remove——macOS向けデータブローカー削除申請の自動実行",
        "個人情報を売買するデータブローカーに対し、オプトアウト(削除)申請を自動で出し続けるmacOS向けツール。"),
    "https://archestra.ai/blog/only-responsible-ai": (
        "Gitの--authorフラグでGitHubリポジトリのAIボット・スパムを止めた",
        "AIエージェントが大量に送ってくる低品質なコントリビューションを、Gitの--authorフラグを使った仕組みでふるい落とした実践記録。"),
    "https://idahonews.com/news/local/two-f-18-fighter-jets-have-crashed-during-an-airshow-at-mountain-home-air-force-base": (
        "エアショーでEA-18戦闘機2機が空中接触、パイロットは無事脱出",
        "マウンテンホーム空軍基地のエアショーで戦闘機2機が接触し墜落。パイロットは緊急脱出して無事。AIとは無関係だがHNで注目された。"),
    "https://www.theregister.com/security/2026/05/18/linus-torvalds-says-ai-powered-bug-hunters-have-made-linux-security-mailing-list-almost-entirely-unmanageable/5241633": (
        "Linus Torvalds『AIバグ報告でLinuxセキュリティMLがほぼ管理不能』",
        "同じAIツールを使う研究者が同一の脆弱性を重複報告し続け、Linuxのセキュリティ用メーリングリストが『ほぼ管理不能』になったとTorvalds氏が表明した。"),
    "https://static1.squarespace.com/static/50363cf324ac8e905e7df861/t/6a0af5d0484fbf5fe9a7743e/1779103184855/2026-Spring-AI.pdf": (
        "AI eats the world (2026年春版) [PDF]",
        "AIが各産業をどう飲み込みつつあるかを俯瞰した、データ豊富な業界スライド資料の2026年春アップデート版。"),
    "https://www.nbcnews.com/video/multiple-commencement-speakers-booed-for-ai-comments-during-graduation-speeches-263486021518": (
        "卒業式でAIに言及した複数の祝辞スピーカーがブーイングを浴びる",
        "エリック・シュミット氏の件にとどまらず、複数の大学の卒業式でAIを称賛する祝辞が学生のブーイングを招いた。雇用不安を背景にAIへの世代的反発が表面化している。"),
    "https://www.theregister.com/ai-ml/2026/05/17/enough-with-the-ai-fomo-go-slow-mo-says-domo-cdo/5240840": (
        "『AIのFOMOはもう十分、スローモで行け』とDomoのCDO",
        "乗り遅れる恐怖(FOMO)で焦ってAIを導入するのをやめ、慎重に段階を踏むべきだとDomoの最高デジタル責任者が説く。"),
    "https://www.theverge.com/ai-artificial-intelligence/644853/pew-gallup-data-americans-dont-trust-ai": (
        "米国民の多くはAIも、それを担う人々も信用していない",
        "PewやGallupの調査データを基に、米国の多くの人がAI技術そのものにも、AIを推進する企業や指導者にも不信感を抱いていると伝える記事。"),
    "https://github.com/2b2tplace/1m_release": (
        "2B2T Minecraftサーバーの巨大ワールドデータ公開プロジェクト",
        "悪名高いMinecraftサーバー2b2tの広大なワールドデータを公開・解析するコミュニティプロジェクト。AIとは無関係だがHNで話題に。"),
    # ── Reddit ──
    "https://www.reddit.com/r/fivethirtyeight/comments/1tg0i25/for_the_first_time_in_years_chatgpt_falls_to/": (
        "数年ぶりにChatGPTが生成AI市場で2位に転落 [r/fivethirtyeight]",
        "ある指標で長年首位だったChatGPTがついに2位に後退したと伝える投稿。ChatGPTのシェアは緩やかに低下し、Gemini等の競合が急速に追い上げている。"),
    "https://www.reddit.com/r/MachineLearning/comments/1tgmwqr/reviving_paperswithcode_by_hugging_face_p/": (
        "Hugging FaceがPapers with Codeを復活させる [プロジェクト]",
        "閉鎖された論文・実装の対応付けサイト『Papers with Code』を、Hugging Faceが引き継いで再生させる取り組み。"),
    "https://www.reddit.com/r/artificial/comments/1tgf0gm/eu_ai_act_enforcement_starts_in_75_days_affects/": (
        "EU AI法の執行が75日後に開始、AIエージェント開発チームに影響 [r/artificial]",
        "EUのAI規制法の本格的な執行開始が75日後に迫り、欧州向けにAIエージェントを作る全チームが対応を迫られると注意喚起する投稿。"),
    "https://i.redd.it/kdtqs0limr1h1.png": (
        "Claude・ChatGPT・Grok・Geminiに『最も愛国心を感じる国は?』と質問",
        "主要なチャットAIに『どの国に最も愛国心を感じるか』を尋ねた結果を比較した投稿。各モデルの訓練データや調整の偏りを浮かび上がらせる。"),
    "https://apnews.com/article/musk-openai-trial-verdict-0b9b0bfaffe96f2c930341f52dfe4f8c": (
        "陪審がイーロン・マスクのOpenAI訴訟を退ける——提訴が遅すぎたと判断",
        "マスク氏がOpenAIとサム・アルトマン氏を訴えた裁判で、陪審は提訴が時効を過ぎていると全員一致で判断。裁判官もこれを認め訴訟は却下された。"),
    "https://www.reddit.com/r/MachineLearning/comments/1tgn3bz/subjepa_a_simple_fix_to_lecun_groups_leworldmodel/": (
        "Sub-JEPA: LeCunらのLeWorldModelを安定して改善する簡単な修正 [プロジェクト]",
        "ヤン・ルカン氏のグループによる世界モデルLeWorldModelに、性能を一貫して向上させる単純な改良を加えたとする投稿。"),
    "https://www.reddit.com/r/artificial/comments/1tgg9s0/has_ai_alignment_gone_too_far_with_content/": (
        "コンテンツ拒否や説教でAIアラインメントは行き過ぎたのか [r/artificial]",
        "AIが過度に回答を拒否したり道徳的な説教をしたりする現状に、アラインメントが行き過ぎでは、と問いかける議論スレッド。"),
    "https://www.pcguide.com/news/linus-torvalds-comments-on-unmanageable-ai-bug-report-problem-for-linux-maintainers/": (
        "Linus Torvalds、Linuxメンテナを悩ます『管理不能なAIバグ報告』に言及",
        "AIが生成する重複バグ報告でLinuxの保守作業が圧迫されている問題について、Torvalds氏のコメントを伝える記事。"),
    "https://www.reddit.com/r/MachineLearning/comments/1tgqyo8/witchcraft_fast_local_semantic_search_on_top_of/": (
        "Witchcraft: SQLite上で動く高速なローカル意味検索 [プロジェクト]",
        "SQLiteをバックエンドに、ローカルで高速に動作する意味的(ベクトル)検索ツールの紹介投稿。"),
    "https://www.reddit.com/r/MachineLearning/comments/1tgqybv/aiml_ethicists_d/": (
        "AI/ML倫理研究者というキャリア [議論]",
        "AI/ML分野の倫理研究者という職種の実態やキャリアパスについて意見を交わすスレッド。"),
    "https://www.reddit.com/r/artificial/comments/1tgr0il/wondering_if_there_is_an_application_for_this/": (
        "これに何か応用先はあるだろうか? [r/artificial]",
        "あるアイデアや手法に実用的な使い道があるかをコミュニティに問いかける投稿。"),
    "https://www.reddit.com/r/MachineLearning/comments/1tg7qq3/would_a_new_result_in_preprint_be_considered_by/": (
        "プレプリントの新しい結果は査読者に考慮されるのか [議論]",
        "投稿後に出たプレプリントの新結果を査読者がどう扱うべきか、研究公開のタイミングを巡る議論スレッド。"),
    "https://www.reddit.com/r/artificial/comments/1tgwudn/microsoft_copilot_cowork_is_now_available_ai/": (
        "Microsoft Copilot Cowork が提供開始——AIが『チャット』から『実作業の遂行』へ",
        "対話するだけのAIから、実際の業務タスクを遂行するAIへ。Microsoftが『Copilot Cowork』を一般提供開始したことを伝える投稿。"),
    "https://www.reddit.com/r/artificial/comments/1tfy65s/started_learning_dl_feels_stuck_need_help/": (
        "ディープラーニングを学び始めたが行き詰まった、助けてほしい [r/artificial]",
        "深層学習を独学し始めたものの伸び悩んでいる初学者が、学習法について助言を求める投稿。"),
    "https://i.redd.it/t1ct0k3o5x1h1.png": (
        "宇宙データセンターは本物か、それともただの誇大宣伝か",
        "軌道上にデータセンターを置く構想が現実的なのか、誇大宣伝に過ぎないのかを論じる投稿。AIの電力・冷却需要への関心が背景にある。"),
    # ── GitHub ──
    "https://github.com/NVlabs/Sana": (
        "Sana: 線形拡散トランスフォーマによる高効率な高解像度画像生成",
        "NVIDIAの研究による、線形拡散トランスフォーマで高解像度画像を高速・低コストに生成するモデル。"),
    "https://github.com/humanlayer/12-factor-agents": (
        "12-factor-agents: 実運用に耐えるLLMエージェント構築の原則集",
        "本番投入できる品質のLLMエージェントを作るための設計原則をまとめたガイド。『The Twelve-Factor App』に着想を得ている。"),
    "https://github.com/ZhuLinsen/daily_stock_analysis": (
        "daily_stock_analysis: LLM駆動の株式分析ダッシュボード",
        "複数のデータソースの相場・ニュースを集め、LLMが売買判断を下すダッシュボードを定時無料運用できるツール。"),
    "https://github.com/ggml-org/llama.cpp": (
        "llama.cpp: C/C++によるLLM推論エンジン",
        "依存の少ないC/C++でLLM推論を行う定番プロジェクト。ローカル実行・量子化推論のデファクト基盤として11万スターを集める。"),
    # ── blogs ──
    "https://huggingface.co/blog/nvidia/cosmos-fine-tuning-for-robot-video-generation": (
        "NVIDIA Cosmos Predict 2.5をLoRA/DoRAでファインチューニング",
        "ロボットの動画生成向けに、NVIDIAの世界基盤モデルCosmos Predict 2.5をLoRA/DoRAで効率的に微調整する手順を解説。"),
    "https://huggingface.co/blog/PaddlePaddle/paddleocr-transformers": (
        "PaddleOCR 3.5——Transformersバックエンドで動くOCRと文書解析",
        "OCRと文書パースを行うPaddleOCR 3.5が、Hugging Face Transformersをバックエンドに使えるようになったことの紹介。"),
    "https://huggingface.co/blog/ibm-research/open-agent-leaderboard": (
        "The Open Agent Leaderboard——エージェント性能のオープンな順位表",
        "AIエージェントの性能を共通基準で比較できるオープンなリーダーボードをIBM Researchが公開。"),
    "https://openai.com/index/dell-codex-enterprise-partnership": (
        "OpenAIとDellが提携——Codexをハイブリッド/オンプレ企業環境へ",
        "OpenAIがDellと組み、コーディングエージェントCodexをクラウドだけでなく企業のオンプレミス/ハイブリッド環境でも使えるようにする。"),
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

# ─── Highlights (5 fresh picks for 2026-05-18) ───
d["highlights"] = [
    {
        "source": "reddit",
        "title": "Jury rules against Elon Musk in his feud with OpenAI, saying he filed his lawsuit too late",
        "title_ja": "陪審、マスク対OpenAI訴訟を却下——『提訴が遅すぎた』",
        "url": "https://apnews.com/article/musk-openai-trial-verdict-0b9b0bfaffe96f2c930341f52dfe4f8c",
        "hot_take_ja": "『OpenAIは慈善を盗んだ』というマスクの主張は、中身の是非を判断される前に時計に負けた。陪審はわずか2時間弱で『提訴が時効後』と全員一致。AI業界を揺るがすはずだった裁判が、営利化の正当性ではなく『出すのが遅かった』で終わった——勝敗より、その幕切れ方が象徴的だ。",
        "detail_ja": "イーロン・マスク氏がOpenAIと共同創業者のサム・アルトマン氏・グレッグ・ブロックマン氏を訴えた裁判で、カリフォルニアの陪審はマスク側の主張をすべて退けた。争点の核心は、OpenAIを非営利の慈善団体として維持するという創業時の約束を経営陣が反故にし、自らの利益のために『慈善を盗んだ』というマスク氏の主張だった。しかし9人構成の助言的陪審は、約2時間弱の評議で、マスク氏が2024年に提訴した時点で既に出訴期限(時効)を過ぎていたと全員一致で判断した。担当のイヴォンヌ・ゴンサレス・ロジャース判事もこの判断に同意し、訴訟を却下した。重要なのは、陪審は『OpenAIの営利化が正しかったか』という実体的な是非には踏み込んでおらず、純粋に提訴のタイミングという手続き上の理由で決着した点だ。マスク氏の主任弁護士マーク・トバーロフ氏は判決後の会見で控訴する意向を示した。この裁判は、急成長するAI企業のガバナンスと、非営利として始まった組織が営利的な構造へ移行することの正当性を問う注目の一戦だった。だがその本丸の論点は判断されないまま、訴訟は時効という入口で終わった。マスク氏自身が競合のxAIを率いる当事者である点も、この対立を単なる理念論争でなく業界の覇権争いの一部として読ませる。",
        "detail_en": "In the lawsuit Elon Musk brought against OpenAI and co-founders Sam Altman and Greg Brockman, a California jury rejected all of Musk's claims. The heart of the case was Musk's allegation that OpenAI's leadership had abandoned the founding promise to keep the lab a nonprofit charity and had effectively 'stolen a charity' in pursuit of personal profit. But the nine-member advisory jury, after deliberating for less than two hours, unanimously found that Musk was already past the statute of limitations when he filed his case in 2024. Judge Yvonne Gonzalez Rogers agreed and dismissed the case. Crucially, the jury did not rule on the substantive question of whether OpenAI's shift toward a for-profit structure was justified — the outcome turned purely on a procedural matter, the timing of the filing. Musk's lead attorney, Marc Toberoff, said at a press conference after the verdict that they plan to appeal. The trial was a closely watched contest over the governance of fast-growing AI companies and the legitimacy of an organization founded as a nonprofit transitioning to a commercial structure. Yet that central question was left undecided, with the case ending at the threshold of the statute of limitations. The fact that Musk himself leads the rival xAI invites reading this dispute not as a pure debate over principles but as part of the industry's contest for dominance.",
        "key_points_ja": [
            "マスクのOpenAI訴訟を陪審が全面的に退ける",
            "争点は『OpenAIが慈善を盗んだ』との主張",
            "陪審は2時間弱で『提訴が時効後』と全員一致",
            "営利化の是非など実体判断には踏み込まず",
            "マスク側は控訴の意向を表明",
            "マスクは競合xAIを率いる当事者でもある",
        ],
        "key_points_en": [
            "Jury fully rejects Musk's lawsuit against OpenAI",
            "Core claim: OpenAI leadership 'stole a charity'",
            "Jury ruled in under 2 hours: filed past the deadline",
            "Did not decide the merits of the for-profit shift",
            "Musk's side says it will appeal",
            "Musk also leads the rival AI firm xAI",
        ],
    },
    {
        "source": "hn",
        "title": "Linux security mailing list 'almost unmanageable' due to AI bug reports",
        "title_ja": "AIバグ報告でLinuxセキュリティMLが『ほぼ管理不能』に",
        "url": "https://www.theregister.com/security/2026/05/18/linus-torvalds-says-ai-powered-bug-hunters-have-made-linux-security-mailing-list-almost-entirely-unmanageable/5241633",
        "hot_take_ja": "AIは脆弱性を『見つける』のが上手くなった。問題は、同じツールを使う全員が同じバグを同時に見つけて報告してくること。Linuxのセキュリティ窓口は重複報告で溺れかけている。Torvaldsの処方箋は鋭い——『検出』はもうコモディティ、価値は検出の上に何を足せるかにある。",
        "detail_ja": "Linuxの生みの親リーナス・トーバルズ氏が、AIを使ったバグ探索によってLinuxのセキュリティ用メーリングリストが『ほぼ完全に管理不能』になったと表明し、Hacker Newsで議論を呼んだ。問題の構造はこうだ。多くの研究者が同じようなAIツールを使ってカーネルを走査するため、まったく同じ脆弱性についての報告が重複して大量に届く。メンテナはその一つ一つに対応し、『それは1週間前/1か月前に既に修正済み』と報告者へ知らせる作業に時間を奪われる。さらに、このセキュリティMLが非公開リストである構造が重複を悪化させている——報告者は互いの投稿を見られないため、自分の発見が既出かどうか分からないまま送ってくる。トーバルズ氏は、AIが検出するバグはそもそも秘匿性が低いので、非公開で扱う運用自体が非効率だとも指摘する。彼の提言は明快だ。単に発見を報告するのではなく、『ドキュメントを読み、パッチも作り、AIがやったことの上に本物の価値を付け加えよ』。AIによる検出はもはやコモディティであり、人間が付加すべきはその先の理解と修正だ、というメッセージである。一方、別のカーネルメンテナであるグレッグ・クロー=ハートマン氏は近年AIがオープンソースにとって有用になってきたと述べており、AIの開発ワークフローへの影響を巡って評価が割れている点も興味深い。これは『AIスロップ(粗製乱造)』が研究論文だけでなく、セキュリティ報告という実務の現場でも具体的な負荷として現れ始めた象徴的な事例だ。",
        "detail_en": "Linus Torvalds, the creator of Linux, stated that AI-powered bug hunting has made the Linux security mailing list 'almost entirely unmanageable,' sparking discussion on Hacker News. The structure of the problem is this: because many researchers scan the kernel with similar AI tools, reports about the exact same vulnerability arrive in large, duplicated volumes. Maintainers lose time responding to each one and telling reporters 'that was already fixed a week/month ago.' The fact that the security list is a private list worsens the duplication — reporters cannot see each other's submissions, so they send findings without knowing whether someone already reported the same thing. Torvalds also notes that AI-detected bugs are inherently low in confidentiality, making the private-handling workflow itself inefficient. His prescription is clear: rather than just reporting a finding, developers should 'read the documentation, create a patch too, and add some real value on top of what the AI did.' The message is that AI detection is now a commodity, and what humans should add is the understanding and the fix beyond it. Interestingly, another kernel maintainer, Greg Kroah-Hartman, has recently said AI is becoming increasingly valuable for open source — so opinions are split over AI's impact on development workflows. This is a symbolic case of 'AI slop' starting to appear as a concrete burden not only in research papers but in the practical arena of security reporting.",
        "key_points_ja": [
            "Torvalds『AIバグ報告でセキュリティMLが管理不能』",
            "同じツールを使う研究者が同一脆弱性を重複報告",
            "非公開リストゆえ報告者が既出と気づけない",
            "メンテナは『既に修正済み』返信に時間を浪費",
            "Torvalds: 検出だけでなくパッチと価値を足せ",
            "AIスロップが実務のセキュリティ現場にも波及",
        ],
        "key_points_en": [
            "Torvalds: AI bug reports make the security list unmanageable",
            "Researchers with the same tools file duplicate findings",
            "Private list means reporters can't see prior submissions",
            "Maintainers waste time replying 'already fixed'",
            "Torvalds: add a patch and real value, not just detection",
            "'AI slop' now burdens practical security work too",
        ],
    },
    {
        "source": "arxiv",
        "title": "AI-Mediated Communication Can Steer Collective Opinion",
        "title_ja": "AIを介したコミュニケーションは集団の世論を動かしうる",
        "url": "https://arxiv.org/abs/2605.16208v1",
        "hot_take_ja": "問題はAIが意見を持つことではなく、AIが『人と人の間』に座っていること。LinkedInの文面整形やXの投稿解説——人間同士のやり取りをAIが書き換える瞬間、その微妙な偏りがネットワークで増幅され、集団の世論ごと押される。個々人を説得しなくても、世論は動かせる。",
        "detail_ja": "この研究は、生成AIが『人間と人間の間』を仲介するときに集団の世論形成に与える影響を、実証と理論の両面から分析したものだ。これまでの研究は、AIが偏った意見を表明したり、人とAIの対話で個人の意見を変えたりする効果に注目してきた。だが本研究が突くのは、AIが人どうしのコミュニケーションを媒介する場面、つまりLinkedInで投稿の文面を磨いたり、Xで共有コンテンツに文脈(解説)を付けたりする場面だ。著者らはまず、複数の有名なLLMファミリーに、争点となるトピックの人間の文章を編集させると、方向性のあるバイアスが混入することを実証した。例えば銃規制に賛成寄り、無神論に反対寄りへ文章を微妙に押すという。次に、ソーシャルネットワーク上でユーザー間にAIが座り、彼らが表現し知覚する意見を変換する、という意見ダイナミクスの数理モデルを導入する。この均衡を解析的に特徴づけ、実際のソーシャルネットワークデータでシミュレーションした結果、AIが人間どうしの通信に持ち込んだ小さな偏りがネットワークを通じて増幅され、集団の世論をその方向へずらしうることが示された。さらに著者らは、こうした偏りがプラットフォーム側で制御可能かを検証し、Xの『この投稿を説明』機能を監査。中絶関連コンテンツに対するGrokの出力に妊娠中絶反対(pro-life)寄りのバイアスがあることを発見し、それを特定の設計判断にまで遡って突き止めた。論文はEUで進む立法の議論に絡めて、この発見の含意を論じている。つまり、AIは個々人を直接説得しなくても、人間どうしの会話の『配管』に組み込まれることで、社会全体の意見の重心を静かに動かしうる——という警告である。",
        "detail_en": "This study analyzes, both empirically and theoretically, how generative AI affects collective opinion formation when it mediates communication between humans. Prior work has focused on AI expressing biased opinions, or shifting an individual's opinion during human-AI interaction. What this paper targets instead is the case where AI mediates human-to-human communication — polishing the wording of posts on LinkedIn, or attaching context to shared content on X. The authors first show empirically that when several popular LLM families are instructed to edit human-written texts on contested topics, they introduce directional biases — for example, nudging texts toward gun control and against atheism. They then introduce a mathematical model of opinion dynamics in which an AI sits between users on a social network, transforming the opinions they express and perceive. By analytically characterizing the equilibrium and running simulations on real social network data, they show that the small biases AI introduces into human-to-human communication can be amplified through the network and shift collective opinion in that direction. The authors further test whether such biases are controllable by platforms, auditing X's 'Explain this post' feature. They find a pro-life bias in Grok's outputs on abortion-related content and trace it back to specific design choices. The paper discusses the implications in connection with ongoing legislative efforts in the EU. The warning is that AI need not directly persuade individuals: by being embedded in the 'plumbing' of human-to-human conversation, it can quietly move the center of gravity of society's opinions.",
        "key_points_ja": [
            "AIが人と人の通信を仲介する場面の世論影響を分析",
            "LLMは争点の文章編集に方向性バイアスを混入",
            "偏りはネットワークで増幅され集団世論を押す",
            "意見ダイナミクスの数理モデルで均衡を解析",
            "Xの『投稿を説明』にpro-liveバイアスを検出",
            "EUの立法議論に絡め含意を論じる",
        ],
        "key_points_en": [
            "Studies opinion effects when AI mediates human communication",
            "LLMs inject directional bias when editing contested texts",
            "Bias amplifies through the network, shifting collective opinion",
            "Equilibrium analyzed via an opinion-dynamics model",
            "Found pro-life bias in X's 'Explain this post'",
            "Discusses implications for EU legislation",
        ],
    },
    {
        "source": "hn",
        "title": "Eric Schmidt speech about AI booed during graduation",
        "title_ja": "元Google CEOシュミット、AIを語る卒業式スピーチでブーイング",
        "url": "https://www.nbcnews.com/tech/tech-news/former-google-ceo-booed-graduation-speech-ai-rcna345585",
        "hot_take_ja": "『未来はまだ書かれていない、君たちにはAIを形作る力がある』——元Google CEOのこの励ましに、卒業生はブーイングで応えた。AI業界の重鎮が語る楽観論と、AIに入口の仕事を奪われつつある2026年卒の現実。両者のズレが、祝辞という場で可視化された出来事だ。",
        "detail_ja": "元GoogleのCEOエリック・シュミット氏が、アリゾナ大学の卒業式での祝辞でブーイングを浴び、Hacker Newsで議論を呼んだ。シュミット氏はAIの登場をコンピュータがもたらした『技術的変革』になぞらえたが、話が人工知能と雇用市場に及ぶと、会場の反応が一気に険しくなった。特に強いブーイングが起きたのは、彼が『科学に関心がなくても構わない、AIはそれ以外のすべてにも触れるのだから』『どんな道を選んでも、AIは仕事のやり方の一部になる』と語った場面だ。シュミット氏は学生の不安を認め、『君たちの世代には、未来はもう書かれてしまった、機械がやって来る、仕事は蒸発しつつある、という恐れがある』とも述べた。その上で、未来はまだ書かれておらず、2026年卒の学生にはAIの発展のあり方を形作る本当の力がある、と主張したが、これも会場の一部からさらなる不興を買った。背景にあるのは、2026年卒の学生が置かれた厳しい就職環境だ。多くの企業が既に人員を削減し、その理由として入門レベルの職をAIで代替できることを挙げている。出席者や批判的な声は、シュミット氏のメッセージを『AIの応援団(AIチアリーディング)』と評した。さらにこの一件はシュミット氏単独の話にとどまらず、同時期に複数の大学の卒業式でAIを称賛する祝辞スピーカーがブーイングを浴びている。AIの恩恵を語る業界の重鎮と、AIに入口の仕事を奪われつつある若い世代との間の溝が、祝辞という象徴的な場で噴き出した出来事といえる。",
        "detail_en": "Former Google CEO Eric Schmidt was booed during his commencement address at the University of Arizona, sparking discussion on Hacker News. Schmidt likened the rise of AI to the 'technological transformation' brought about by the computer, but when he turned to artificial intelligence and the job market, the crowd's reaction sharpened. The booing intensified when he said things like 'If you don't care about science that's okay because AI is going to touch everything else as well' and 'Whatever path you choose, AI will become part of how work is done.' Schmidt acknowledged the students' anxiety, saying 'There is a fear in your generation that the future has already been written, that the machines are coming, that the jobs are evaporating.' He then argued that the future remains unwritten and that the class of 2026 has real power to shape how AI develops — a claim that also drew further disapproval from parts of the audience. The backdrop is the harsh job market facing the class of 2026: many companies have already cut headcount, citing AI as a substitute for entry-level roles. Attendees and critics described his message as 'AI cheerleading.' Moreover, this episode was not limited to Schmidt alone — around the same time, commencement speakers praising AI were booed at multiple universities. It is an event in which the gap between industry leaders who tout AI's benefits and a young generation losing entry-level jobs to AI erupted in the symbolic setting of a graduation speech.",
        "key_points_ja": [
            "元Google CEOシュミットが卒業式祝辞でブーイング",
            "AIと雇用に話が及ぶと会場の反応が険しく",
            "『どんな道でもAIが仕事の一部に』に強い不興",
            "2026年卒は入門職をAIに奪われつつある世代",
            "メッセージは『AIの応援団』と批判された",
            "複数大学でもAI称賛の祝辞がブーイングを浴びた",
        ],
        "key_points_en": [
            "Ex-Google CEO Schmidt booed at a commencement speech",
            "Crowd turned hostile when he addressed AI and jobs",
            "'AI becomes part of how work is done' drew loud boos",
            "Class of 2026 is losing entry-level roles to AI",
            "His message was criticized as 'AI cheerleading'",
            "AI-praising speakers booed at several universities",
        ],
    },
    {
        "source": "arxiv",
        "title": "Prospective multi-pathogen disease forecasting using autonomous LLM-guided tree search",
        "title_ja": "LLM主導の木探索による多病原体の感染症予測",
        "url": "https://arxiv.org/abs/2605.16238v1",
        "hot_take_ja": "感染症予測は長らく専門家チームの『手作り』が頼りだった。この研究はLLMに木探索で予測モデルを自律的に書かせ、2025-26シーズンの実時間予測でCDCの専門家アンサンブルに匹敵・凌駕。AIが論文を書く話の次は、AIが科学の実務インフラを回す話だ。",
        "detail_ja": "感染症の確率的予測は公衆衛生に不可欠だが、専門家チームによる労働集約的なモデルの手作りに頼っており、それが細かい地域単位や新興病原体への展開のボトルネックになっている。この研究は、大規模言語モデル(LLM)が主導する木探索によって、実行可能な予測ソフトウェアを反復的に生成・評価・最適化する自律システムを提示する。注目すべきは、これが回顧的なベンチマークではなく、2025-26年の米国の呼吸器疾患シーズン中に行われた完全に前向き(プロスペクティブ)かつ実時間の評価だという点だ。システムはインフルエンザ、COVID-19、RSV(呼吸器合胞体ウイルス)について、方法論的に多様な予測モデルを自律的に発見した。そして、これら機械が生成したモデルを集約したアンサンブルは、ゴールドスタンダードである米CDCの専門家がキュレートしたハブ・アンサンブルを、未知データ上で一貫して同等以上に上回った。さらにシステムは、データの乏しいRSVの『コールドスタート』状況もうまく乗り切った。著者らは制御された回顧的アブレーションも行い、対数スケールの距離指標を最適化することが『報酬ハッキング』を防ぐこと、自動の判定役を組み込むループが複雑な科学理論への構造的忠実性を担保することを明らかにした。疫学の理論を、正確で透明性のあるコードへ自律的に翻訳することで、この枠組みはモデリングの労働ボトルネックを取り除き、専門家レベルの感染症予測を前例のない規模で迅速に展開できる可能性を示している。AIが研究を『書く』段階を超え、公衆衛生という実務インフラを実時間で回し始めた、という意味で象徴的な成果だ。",
        "detail_en": "Probabilistic forecasting of infectious diseases is essential for public health, but it relies on labor-intensive manual model curation by expert teams — a bottleneck for scaling to granular geographic resolutions or emerging pathogens. This study presents an autonomous system that uses large language model (LLM)-guided tree search to iteratively generate, evaluate, and optimize executable forecasting software. Notably, this was not a retrospective benchmark but a fully prospective, real-time evaluation conducted during the 2025-2026 US respiratory season. The system autonomously discovered methodologically diverse forecasting models for influenza, COVID-19, and RSV (respiratory syncytial virus). An ensemble aggregating these machine-generated models consistently matched or outperformed the gold-standard, human-curated US CDC hub ensembles out-of-sample. The system also successfully navigated data-scarce 'cold start' scenarios for RSV. The authors ran controlled retrospective ablations, showing that optimizing log-scale distance metrics prevents 'reward hacking,' and that an automated judge-in-the-loop ensures structural fidelity to complex scientific theories. By autonomously translating epidemiological theory into accurate, transparent code, the framework removes the modeling labor bottleneck and shows the potential to rapidly deploy expert-level disease forecasting at unprecedented scale. It is a symbolic result in that AI has moved beyond 'writing' research to running real-time, practical public-health infrastructure.",
        "key_points_ja": [
            "LLM主導の木探索が予測ソフトを自律生成・最適化",
            "2025-26シーズンに完全前向き・実時間で評価",
            "インフル・COVID・RSVの多様なモデルを発見",
            "CDC専門家アンサンブルに匹敵・凌駕",
            "対数スケール指標で報酬ハッキングを防止",
            "モデリングの労働ボトルネックを解消しうる",
        ],
        "key_points_en": [
            "LLM-guided tree search auto-generates forecasting software",
            "Fully prospective, real-time test in the 2025-26 season",
            "Discovered diverse models for flu, COVID, and RSV",
            "Matched or beat the CDC expert ensemble",
            "Log-scale metrics prevent reward hacking",
            "Could remove the modeling-labor bottleneck",
        ],
    },
]

OUT.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT}")
print(f"Highlights: {len(d['highlights'])}")
for src, items in d["sources"].items():
    enriched = sum(1 for it in items if it.get("title_ja"))
    print(f"  {src}: {enriched}/{len(items)} enriched")
