# -*- coding: utf-8 -*-
"""Enrich raw-2026-06-17.json -> 2026-06-17.json with JP/EN summaries + highlights."""
import json
from pathlib import Path

DATE = "2026-06-17"
DATA = Path(__file__).resolve().parent.parent / "data"

raw = json.load(open(DATA / f"raw-{DATE}.json", encoding="utf-8"))
s = raw["sources"]

# ---- arXiv (top 25) ----
arxiv = {
    0: ("「Value軸」：LMは自分が正しい軌道にいるかを内部表現する",
        "Qwen3-8Bの活性化に、現在の戦略が目標達成に至る見込み（=トラジェクトリのvalue）を符号化する1本の軸を発見。この軸は高/低confidence、バックトラックの有無、正/誤コードを区別し、高value方向へ操作すると自己修正が抑制され、低value方向では探索・やり直しが誘発される。DPOがこの内部valueを高められることも示した。"),
    1: ("T-Rex：触覚反応型の器用なマニピュレーション",
        "触覚信号にリアルタイムで反応する器用さは人間並み操作の鍵だが、既存のVLAは触覚を無視するか静的な手掛かりに留まる。多様な触覚データ不足を補い、触覚反応型の器用操作を実現する手法を提案。"),
    2: ("Human Universal Grasping：任意物体への人間的な把持生成",
        "ロボットの汎用把持データの最も自然な源は、毎日無数の物体を掴む人間だと主張。1枚のRGB-Dから任意物体に対し多様な人間の把持姿勢を生成するflow-matchingモデルHUGを提案。"),
    3: ("Context-Aware RL：エージェント/マルチモーダルLLMの長文脈推論を強化",
        "長く複雑な文脈の中の決定的な1行・1箇所の手掛かりをLLMが見落とす問題に対し、文脈を意識した強化学習ContextRLを提案。長期推論とマルチモーダル理解を改善する。"),
    4: ("BRDFusion：物理と生成を融合した都市シーンの逆レンダリング",
        "撮影動画からの都市シーン逆レンダリングで、物理ベース手法のアーティファクトと生成モデルの制御性不足を両取りで克服。コンテンツ生成や自動運転シミュレーションに応用。"),
    5: ("線形逆問題を解くための厳密な事後スコア推定",
        "拡散/フローモデルが学ぶのは無条件スコアで、逆問題を解くには事後スコアが必要というギャップに対し、厳密な事後スコア推定法を提案。"),
    6: ("Geometric Action Model：3D幾何を踏まえたロボット方策学習",
        "既存VLA/世界モデルは主に2Dで動作するが、物体・カメラ・行動の3D相互作用を推論する幾何的な行動モデルを提案し、汎用ロボット方策の性能を高める。"),
    7: ("疎なエピソード結果からのVLAオンラインRL微調整のための階層的アドバンテージ重み付け",
        "VLA方策のオンラインRLでは1ロールアウトが成功/失敗の二値しか返さないが、行動更新には遷移ごとの教師が要る。この疎さを階層的なアドバンテージ重み付けで補い、効率的に微調整する。"),
    8: ("Nature系のメタ分析論文でLLMエージェントをベンチマーク",
        "文献検索・PICO選定・統計的統合からなるメタ分析は、体系的な科学的推論の検証に最適。検索-スクリーニング-統合の全工程に正解を持つベンチマークでLLMエージェントを評価。"),
    9: ("R2RDreamer：空間汎化する2D操作方策のための3D対応データ拡張",
        "模倣学習の操作方策には物体姿勢・カメラ視点を跨ぐ多数のデモが要る。少数デモから3Dを意識したデータ拡張で空間汎化を実現する。"),
    10: ("ニューラル表現における位相の重要性：画像分類器の内部Oppenheim-Limテスト",
        "自然画像はフーリエ位相だけで認識可能（振幅は同一性をほぼ持たない）という古典的事実が、学習済み分類器の隠れ層内部でも再現されるかを、位相の入れ替えで因果的に検証。"),
    11: ("Your Privacy My Cloak：差分プライバシー連合学習へのバックドア攻撃",
        "差分プライバシー(DP)は連合学習のバックドア耐性を高めるとされてきたが、本研究はその前提に反論。DP-FLに潜む根本的な緊張関係を実証的に暴く。"),
    12: ("KVEraser：効率的な局所文脈消去のためのKVキャッシュ操作学習",
        "KVキャッシュ上の事後的な文脈消去は、局所編集が後続トークンのキャッシュ全体に波及するため難しい。古い検索事実や誤ったツール観測を効率的に消すための学習的なKV操作を提案。"),
    13: ("Qwen-RobotWorld：言語条件付き動画生成で身体性世界モデルを統一",
        "自然言語を統一的な行動インタフェースとし、現在の観測から物理的に妥当な未来映像を予測する言語条件付き動画世界モデル。ロボット操作・自動運転・屋内ナビ・人→ロボット移転を横断し、合成データ生成・方策評価・言語誘導プランニングに使える。"),
    14: ("DeepRubric：深層リサーチエージェントを効率的にRL学習する証拠木ルーブリック監督",
        "深層リサーチエージェントのルーブリック報酬RLは、基準が情報ニーズを取りこぼすと効率が落ちる。クエリから逆向きに信頼できるクエリ-ルーブリック監督を構築するデータ生成枠組みを提案。"),
    15: ("HAMON：長期予測のための受動光学的シーケンス混合",
        "長期時系列予測では単純な線形/周波数モデルが依然強く、Transformerの密な重ね合わせ表現が不要かもしれない。基盤レベルでこの問いに迫る。"),
    16: ("MeshLoom：メッシュ系列の順伝播型・非剛体レジストレーション",
        "頂点変形を直接再構成する順伝播型ネットで、従来の高コストな個別最適化や狭いカテゴリ・ペア限定といった制約を超える非剛体レジストレーションを実現。"),
    17: ("ExpRL：LLM中間学習のための探索的RL",
        "疎報酬RLの成否はベースモデルのカバレッジに依存する。分解・検証などの基礎スキルを教えるmid-trainingを探索的RLで行い、後続RLの土台を広げる。"),
    18: ("データの幾何を学ぶ：Shape Space解析の数学的レビュー",
        "観測が豊かな幾何形状を持つデータ（生物学などの形状空間）を扱う機械学習について、形状空間解析の数学的基盤を概観するレビュー。"),
    19: ("FusionRS：二モーダル視覚言語基盤モデル向け大規模RGB-赤外リモセンデータセット",
        "リモセンの視覚言語モデルはRGB中心で赤外情報が未活用。熱強度・物体境界・照明不変な手掛かりを含む赤外を加えた大規模RGB-赤外データセットを構築。"),
    20: ("TokenPilot：LLMエージェント向けキャッシュ効率的な文脈管理",
        "長時間セッションで文脈が膨張し推論コストが増す問題に対し、プレフィックス不整合やキャッシュ無効化を避けつつ文脈を圧縮するキャッシュ効率的な管理法を提案。"),
    21: ("グラフネイティブ時系列のためのフィルタ付きコンフォーマル楕円体",
        "多変量時系列の同時予測集合で、座標間依存に適応しつつ単一イベントを制御。状態空間フィルタの予測平均・共分散にsplit-conformalを適用する。"),
    22: ("深層NNの勾配爆発・消失：残差接続の効果",
        "勾配爆発・消失を乗法的エルゴード理論で解析し、残差接続を加える効果をリアプノフ指数の観点から正確に説明。"),
    23: ("ROVE：強化学習でヒューマノイド操作の人間介入を活用",
        "全身運動学と器用な手制御ゆえにヒューマノイドへの人間介入はシステム上難しく、収集軌道も準最適になりがち。これをRLで活かしVLA後学習に繋げる。"),
    24: ("トークンから方策へ：因果的で解釈可能な異質処置効果の同定",
        "異質処置効果(HTE)の同定は表現力と解釈性のトレードオフに陥り、未測定の駆動因があると偽のHTEを生む。因果的に妥当なHTE同定法を提案。"),
}
for i, (tja, sja) in arxiv.items():
    s["arxiv"][i]["title_ja"] = tja
    s["arxiv"][i]["summary_ja"] = sja

# ---- HN (all 20) ----
hn = {
    0: ("LinkedInの求人オファーに仕込まれたバックドア",
        "暗号通貨スタートアップの採用担当（実在の美術ジャーナリストの身元を盗用）を装い、LinkedIn経由でコードレビューを依頼。npm installのprepareスクリプトで自動実行されるバックドアを、コメントアウトされたテストの壁に紛れ込ませる巧妙なサプライチェーン攻撃。"),
    1: ("Ask HN：日常のコーディングでClaude/GPTをローカルモデルに置き換えられた人は？",
        "ローカルLLMが日々の開発でフロンティアモデルを代替できるかを問うスレッド。コミュニティの実感（性能・コスト・プライバシーのトレードオフ）が集まり、ローカル運用の成熟度を測る定点観測になっている。"),
    2: ("Fabrice Bellardは尊敬に値する——ほぼ間違いなく総合力で上位のプログラマ",
        "FFmpegやQEMU等を生んだ伝説的開発者Bellardへの賛辞。AI時代に『個人の卓越した工学』がなお重要だという議論を呼んだ。"),
    3: ("自分のホームラボAI開発プラットフォーム",
        "自宅サーバ上にAI開発環境を構築した事例。ローカルでのモデル運用・実験基盤への関心の高まりを反映。"),
    4: ("Claude Corps：Anthropicの全米AIフェローシップ",
        "Anthropicが1.5億ドルを投じ、社会人経験2年未満の人材を最終的に1000人、非営利団体に12か月配属しAIスキルを実装させるフェローシップ。年俸8.5万ドル、2026年10月開始。"),
    5: ("MicrosoftがAWSに頼る——GitHubがAI能力逼迫に直面",
        "GitHubのAIワークロード需要が逼迫し、MicrosoftがAzureだけでなく競合AWSの計算資源に頼っているという報道。自社クラウドを持つMSがライバルから借りる構図が話題に。"),
    6: ("Show HN：AIなしでゼロから書いたC++レイトレーサ",
        "生成AIを一切使わずスクラッチで実装したレイトレーサ。AI全盛期に『手で書く』価値を示す作品として注目された。"),
    7: ("Claude：多数のモデルでエラー増加（障害）",
        "Anthropicのステータスページに掲載された障害。複数モデルでエラー率が上昇し、フロンティアLLMへの依存が増す中での可用性リスクを改めて意識させた。"),
    8: ("RustとC/C++でメモリ安全性CVEはどう違うか",
        "Rustと C/C++のメモリ安全性関連CVEの差異を分析。セキュアな言語選択の議論を喚起。"),
    9: ("Show HN：Garden of Flowers——ASCIIアート以前の絵画的タイポグラフィのアーカイブ",
        "ASCIIアート以前の絵画的タイポグラフィを集めたアーカイブ。計算機文化史の資料として人気。"),
    10: ("だが yak shaving（前準備の脱線）は楽しい",
        "本題に辿り着く前の周辺作業（yak shaving）の楽しさを論じたエッセイ。開発者の共感を集めた。"),
    11: ("欧州は自前の計算資源だけでフロンティアAIを訓練できるか",
        "欧州が域内で所有する計算資源だけでフロンティアモデルを訓練できるかを検討するプロジェクト(euromesh)。AI主権と計算インフラの地政学という論点。"),
    12: ("Fableのban、本当はジェイルブレイクが理由ではなかった？",
        "米政府によるAnthropic Fable 5/Mythos 5の輸出規制は、ジェイルブレイクという技術的理由は口実で、実態は政治的・報復的だったとTechCrunchが報道。Katie Moussourisも『輸出規制の対象になるべきではない』と指摘。"),
    13: ("米空軍のB-52爆撃機が離陸後に墜落（エドワーズ空軍基地）",
        "離陸直後にB-52が墜落したとの速報。AIとの直接の関係は薄いがHN上位に。"),
    14: ("Show HN：machine0——CLIから制御する永続NixOS VM",
        "CLIから操作できる永続的なNixOS VMツール。再現可能な開発・エージェント実行環境への関心を反映。"),
    15: ("JWTの使用をやめよう",
        "JWTをセッション管理に使うことの落とし穴を論じ、よりシンプルな代替を勧める記事。"),
    16: ("SubQ 1.1 Small（技術レポート）",
        "新興のSubQによる小型モデル1.1 Smallの技術レポート。小型・効率モデル競争の一端。"),
    17: ("After AI Takes Everything（AIが全てを奪った後で）",
        "AIが多くの仕事を担う未来における人間の意味・生き方を考察するエッセイ。"),
    18: ("Qwen-Robot Suite：物理世界知能のための基盤モデル群",
        "Qwenが公開した身体性AI向け基盤モデル群。言語条件付き世界モデルや操作方策を含み、ロボティクスの基盤モデル化を推し進める。"),
    19: ("Show HN：獣医から起業——AIによる芝生診断",
        "獣医出身の創業者が作った、芝生の状態をAIで診断するサービス。ニッチ領域へのAI応用例。"),
}
for i, (tja, sja) in hn.items():
    s["hn"][i]["title_ja"] = tja
    s["hn"][i]["summary_ja"] = sja

# ---- GitHub (all 3) ----
gh = {
    0: ("iptv-org/iptv：世界中の公開IPTVチャンネル集",
        "世界各国の公開IPTVチャンネルを集約したリポジトリ。AIとは直接無関係だが定番の人気プロジェクト。"),
    1: ("TeslaMate：自前ホスティングのTeslaデータロガー",
        "Tesla車のデータを自宅サーバに記録・可視化するセルフホスト型ロガー。"),
    2: ("軽量・超高速なインプロセス・ベクトルデータベース",
        "プロセス内で動く軽量・高速なベクトルDB。RAGや埋め込み検索の組み込み用途で注目。"),
}
for i, (tja, sja) in gh.items():
    s["github"][i]["title_ja"] = tja
    s["github"][i]["summary_ja"] = sja

# ---- Blogs (all 14) ----
blogs = {
    0: ("デプロイをシミュレートしてリリース前にモデル挙動を予測",
        "OpenAIが、実デプロイを模擬することでリリース前にモデルの振る舞いを予測する手法を紹介。問題挙動を事前に検出する狙い。"),
    1: ("Google DeepMind：アラバマ州での投資・地域支援を強化",
        "DeepMindがアラバマ州への投資と地域貢献を拡大。AI企業の地方インフラ・雇用投資の一例。"),
    2: ("OpenAI Partner Networkを発表",
        "OpenAIが導入・実装支援のためのパートナーネットワークを発表。エンタープライズ展開を後押し。"),
    3: ("olmo-eval：モデル開発ループ向け評価ワークベンチ",
        "Hugging Faceが、モデル開発の反復に使える評価ワークベンチolmo-evalを公開。"),
    4: ("OpenAI Academy：次世代の働き方に向けた新講座",
        "OpenAIが、AI時代の働き方に向けた新たな学習講座を提供開始。"),
    5: ("Preply：AIと人間チューターを組み合わせ学習を個別化",
        "語学学習PreplyがAIと人間講師を併用してパーソナライズを実現した事例。"),
    6: ("Google DeepMind：バージニア州への地域投資で雇用とエネルギーを支援",
        "DeepMindがバージニア州で雇用創出とエネルギー手頃化を支援する地域投資を発表。"),
    7: ("OpenAIがOnaを買収",
        "OpenAIが開発者向けエージェント企業Onaを買収。コーディングエージェント領域への布石。"),
    8: ("天体物理学者がCodexでブラックホールのシミュレーションを支援",
        "研究者がOpenAI Codexを使ってブラックホールのシミュレーション作業を効率化した事例。"),
    9: ("BBVA：OpenAIで銀行業務の中核にAIを据える",
        "スペインの銀行BBVAがOpenAIを業務の中核に据えた導入事例。"),
    10: ("OpenAI：信頼できるAIエコシステムに向け欧州の取り組みを支援",
        "OpenAIが欧州の信頼性あるAIエコシステム構築を支援すると表明。"),
    11: ("PyTorchプロファイリング(Part2)：nn.LinearからFused MLPへ",
        "Hugging FaceによるPyTorch性能チューニング解説。nn.LinearをFused MLPに最適化する実践。"),
    12: ("OracleクラウドからOpenAIモデルとCodexを利用可能に",
        "Oracleクラウドの利用枠でOpenAIモデルとCodexにアクセスできるように。マルチクラウド展開。"),
    13: ("中国関連の影響工作が米国のAI論争を標的に",
        "OpenAIが、PRC（中国）関連の影響工作が米国内のAI政策論争を標的にしていると報告。"),
}
for i, (tja, sja) in blogs.items():
    s["blogs"][i]["title_ja"] = tja
    s["blogs"][i]["summary_ja"] = sja

# ---- Highlights ----
raw["highlights"] = [
    {
        "source": "TechCrunch / HN",
        "title": "The US government's Anthropic models ban was never about an AI jailbreak",
        "title_ja": "米政府のAnthropic禁輸、本当はジェイルブレイクが理由ではなかった",
        "url": "https://techcrunch.com/2026/06/15/the-us-governments-anthropic-models-ban-was-never-about-an-ai-jailbreak/",
        "hot_take_ja": "「セキュリティガードレールの不備」は口実で、実態は政治的報復——という見立てが補強されてきた。コードを『レビューして』と『直して』で挙動が変わる程度のことが輸出規制の根拠になるなら、規制は技術ではなく感情で動いている。AI企業が政権との関係次第で潰される前例になりかねない。",
        "detail_ja": "6/14にWSJが報じたAnthropic Fable 5 / Mythos 5の米政府による輸出規制・運用停止について、TechCrunchが「技術的理由は薄い」とする続報を出した。発端とされた『ガードレール回避』は、セキュリティ研究者によればFable 5に『コードのセキュリティ問題をレビューして』と頼むのと『このコードを直して』と頼むのとで応答が変わる、という程度の挙動差に過ぎなかったという。著名なセキュリティ研究者Katie Moussourisは、この挙動は『輸出規制を発動させるようなものでは決してない』とし、さらに『論文に書かれた挙動は本質的に修正不可能で、無理に直せばモデルの防御能力をむしろ削ぐだけだ』と指摘した。Axiosは、規制の真因はAnthropicと政権の『人間関係・性格の不一致』にあり、Amazon CEOのAndy Jassyの関与も取り沙汰されると報じている。記事は、これが『米国のAI企業は干渉なしには運営できない』というシグナルになり、政権が個人的・政治的な好みで勝者を選んでいるとの疑念を生む、と警告する。技術的根拠の乏しい規制が前例化すれば、フロンティアAIの開発・公開が政治リスクに直接さらされることになる。",
        "detail_en": "Following the WSJ report (June 14) that the US government forced Anthropic to suspend its Fable 5 / Mythos 5 models via an export directive, TechCrunch published a follow-up arguing the technical rationale was thin. The supposed 'guardrail bypass' amounted, per security researchers, to Fable 5 responding differently when asked to 'review this code for security issues' versus 'fix this code.' Prominent security researcher Katie Moussouris said this behavior 'should never have triggered an export control,' adding that 'the behavior described in the paper cannot meaningfully be fixed, and any attempt would only weaken the model for defense.' Axios reported the real driver was 'personality differences' between Anthropic and the Trump administration, with possible involvement from Amazon CEO Andy Jassy, on top of an already fractious relationship. The piece warns this signals that 'AI companies in the United States can't be trusted to operate without interference' and fuels suspicion that officials are 'picking favorites based on personal and political factors.' If export controls with such weak technical grounding become precedent, frontier AI development and release are exposed directly to political risk.",
        "key_points_ja": [
            "『ガードレール回避』はレビュー/修正で応答が変わる程度の挙動差",
            "Moussouris：輸出規制を発動させるものでは決してない",
            "論文の挙動は本質的に修正不能、直せば防御力が落ちる",
            "Axios：真因は政権との人間関係・性格不一致",
            "Amazon CEO Andy Jassyの関与が取り沙汰される",
            "政治的好みでAI企業の勝者を選ぶ前例化への懸念",
        ],
        "key_points_en": [
            "'Bypass' was just review-vs-fix response difference",
            "Moussouris: should never trigger an export control",
            "Paper's behavior is unfixable; fixing weakens defense",
            "Axios: real cause was personality clash with admin",
            "Possible involvement of Amazon CEO Andy Jassy",
            "Fear of precedent: politics picking AI winners",
        ],
    },
    {
        "source": "Anthropic",
        "title": "Claude Corps",
        "title_ja": "Claude Corps：1.5億ドル投じる全米AIフェローシップ",
        "url": "https://www.anthropic.com/news/claude-corps",
        "hot_take_ja": "Anthropicが1.5億ドルを投じ、若手1000人を非営利に送り込んでAIスキルを実装させる。『AIの恩恵を経済移行期にどう分配するか』を、寄付ではなく人材配置という形でやろうとしている点が新しい。Teach For America のAI版という設計だ。",
        "detail_ja": "AnthropicがClaude Corpsという全米フェローシップ制度を発表した。社会人経験2年未満の若手を中心に最終的に1000人のフェローを、初年度で少なくとも400の非営利団体に12か月のフルタイムで配属し、現場でAIスキルを実装させる。開始は2026年10月、年俸は8.5万ドルに福利厚生・メンターシップ・潤沢なClaudeアクセスが付く。応募要件は18歳以上・米国就労資格・必要なら転居可で、学歴・専攻は不問。仕組みとしては非営利のCodePathが雇用主(employer of record)兼研修提供者、Social Financeが効果測定・評価とスケール基盤を担い、Anthropicが資金提供と戦略を担う三者構成だ。受け入れ団体は教育・食料支援・退役軍人支援・海洋保全・人材育成など多分野にわたる。総額1.5億ドルのコミットメントで、単発の支援に留まらず『経済移行期にAIの便益を分配する再現可能なモデル』を作ることを掲げている点が特徴。AI普及が雇用に与える影響への不安が高まる中、企業がスキル移転と社会実装を同時に狙う設計として注目される。",
        "detail_en": "Anthropic announced Claude Corps, a national fellowship that will place up to 1,000 fellows—mostly early-career people with under two years of full-time experience—into at least 400 nonprofits in the first 12 months, as full-time 12-month roles applying AI skills on the ground. Fellowships begin October 2026 with an $85,000 salary plus benefits, mentorship, and extensive Claude access. Eligibility is broad: 18+, authorized to work in the US, willing to relocate, with no required education or major. The structure is tripartite: nonprofit CodePath acts as employer of record and trainer, Social Finance handles measurement and scaling infrastructure, and Anthropic funds and directs strategy. Host nonprofits span education, food security, veteran support, marine conservation, and workforce development. Backed by a $150 million commitment, the program explicitly aims to build a 'replicable model for distributing AI benefits during economic transition,' rather than a one-off grant. As anxiety grows over AI's labor-market impact, it stands out as a corporate attempt to pair skills transfer with real-world deployment.",
        "key_points_ja": [
            "最終的に1000人のフェローを非営利に配属",
            "初年度で最低400団体、12か月フルタイム",
            "年俸8.5万ドル+福利厚生・Claudeアクセス、2026年10月開始",
            "総額1.5億ドルのコミットメント",
            "CodePath=雇用主/研修、Social Finance=測定、Anthropic=資金",
            "経済移行期のAI便益分配の再現可能モデルを標榜",
        ],
        "key_points_en": [
            "Up to 1,000 fellows placed in nonprofits",
            "400+ host orgs in year one, 12-month full-time",
            "$85k salary + benefits + Claude access, starts Oct 2026",
            "$150M total commitment",
            "CodePath employs/trains, Social Finance measures, Anthropic funds",
            "Aims at a replicable AI-benefit distribution model",
        ],
    },
    {
        "source": "arXiv",
        "title": "The Value Axis: Language Models Encode Whether They're on the Right Track",
        "title_ja": "「Value軸」：LMは自分が正しい軌道にいるかを内部で表現している",
        "url": "https://arxiv.org/abs/2606.17056v1",
        "hot_take_ja": "LMの内部には『今の自分の戦略は上手くいきそうか』を表す1本の軸が存在する——しかもその軸を押すだけで、自己修正を消したり逆に探索・やり直しを誘発できる。reasoningモデルの『粘り』や『諦め』が、たった1次元の操作でコントロールできるという話で、解釈可能性と制御の両面で示唆が大きい。",
        "detail_ja": "言語モデルが、自分の現在のトラジェクトリの『価値（=今の戦略が目標達成に至る見込み）』を内部で追跡しているかを調べた研究。著者らは合成のin-context強化学習データを使い、Qwen3-8Bの活性化空間に1本の『value軸』を構成した。この軸に沿った活性化は、(1)言語化された自信の高低、(2)バックトラック（やり直し）の有無、(3)正しいコードと壊れたコードを区別できた。さらに因果的な操作実験として、高value方向に活性化をステアリングすると自己修正が抑制され説明も簡素になり、逆に低value方向へsteerするとバックトラックや探索が誘発された。つまりモデルの『粘り強さ／諦め』のような挙動が、単一方向の内部表現で制御できることを示している。加えて、DPO（直接選好最適化）でこの内部valueを引き上げられることも確認した。reasoning系モデルが過剰に自己修正して冗長になったり、逆に早々に諦めたりする挙動を、内部表現レベルで理解・調整できる可能性を開く点が重要だ。一方で、こうした軸は『正しさ』ではなく『成功の見込みについての自己評価』であり、過信を強める方向にも操作できるため、安全性の観点では諸刃の剣でもある。",
        "detail_en": "This work asks whether language models internally track the 'value' of their current trajectory—the likelihood their ongoing strategy reaches its goal. Using synthetic in-context reinforcement-learning data, the authors construct a single 'value axis' in Qwen3-8B's activation space. Activations along this axis distinguish (1) high vs. low verbalized confidence, (2) rollouts with vs. without backtracking, and (3) correct vs. corrupted code. Crucially, causal steering shows the axis is functional: pushing toward high value suppresses self-correction and shortens explanations, while pushing toward low value induces backtracking and exploration. In other words, behaviors like 'persistence' vs. 'giving up' can be controlled via a single internal direction. They further show that direct preference optimization (DPO) can raise this internal value. The result opens a path to understanding and tuning—at the representation level—why reasoning models over-correct and become verbose, or quit too early. The caveat: this axis encodes a self-assessment of success likelihood, not ground-truth correctness, and can be steered toward overconfidence—making it a double-edged tool for safety.",
        "key_points_ja": [
            "Qwen3-8Bに『今の戦略の見込み』を表すvalue軸を発見",
            "自信の高低・やり直し有無・正誤コードを区別",
            "高value方向に操作→自己修正を抑制・説明を簡素化",
            "低value方向に操作→バックトラック・探索を誘発",
            "DPOで内部valueを引き上げ可能",
            "正しさではなく自己評価なので過信操作のリスクも",
        ],
        "key_points_en": [
            "Found a 'value axis' in Qwen3-8B for trajectory prospects",
            "Separates confidence, backtracking, correct vs. corrupt code",
            "Steer high → suppresses self-correction, shorter output",
            "Steer low → induces backtracking and exploration",
            "DPO can raise the internal value",
            "Encodes self-assessment, not truth — overconfidence risk",
        ],
    },
    {
        "source": "arXiv / Qwen",
        "title": "Qwen-RobotWorld: Unifying Embodied World Modeling through Language-Conditioned Video Generation",
        "title_ja": "Qwen-RobotWorld：言語条件付き動画生成で身体性の世界モデルを統一",
        "url": "https://arxiv.org/abs/2606.17030v1",
        "hot_take_ja": "『自然言語＝行動インタフェース』で、ロボット操作も自動運転も屋内ナビも1つの動画世界モデルに統一してしまう。未来の映像を予測できれば、合成データ生成・方策評価・行動プランニングが全部その上で回る——LLMの次はこの『行動の世界モデル』が基盤になる、というQwenの賭けが見える。",
        "detail_ja": "Qwen（Alibaba）が、身体性AI向けの言語条件付き動画世界モデルQwen-RobotWorldを発表した。自然言語を統一的な行動インタフェースとして、現在の観測から物理的に妥当な『未来の視覚的トラジェクトリ（映像）』を予測する。特徴は、ロボット操作・自動運転・屋内ナビ・人間からロボットへの転移という複数ドメインを単一の定式化で扱う点だ。これにより3つの応用が開ける——(1)方策学習を補強する合成データ生成、(2)方策を評価するスケーラブルな仮想環境、(3)下流のロボット制御に与える言語誘導のプランニング信号。技術的には、60層規模のDouble-Stream MMDiTにMLLM（マルチモーダルLLM）の行動エンコーディングを組み合わせる設計が核とされる。同日にHNで話題になった『Qwen-Robot Suite』は、こうした世界モデルや操作方策を含む基盤モデル群の総称で、ロボティクスをLLM同様に『基盤モデル化』しようという動きの一環だ。実機データ収集が高コストなロボティクスにおいて、映像予測モデルを『シミュレータ兼データ生成器兼プランナー』として使い回す設計は、スケール則をロボットにも持ち込む現実的な経路として注目される。",
        "detail_en": "Qwen (Alibaba) introduced Qwen-RobotWorld, a language-conditioned video world model for embodied intelligence. Using natural language as a unified action interface, it predicts physically grounded future visual trajectories (video) from current observations. Its distinguishing feature is handling multiple domains—robotic manipulation, autonomous driving, indoor navigation, and human-to-robot transfer—within a single formulation. This enables three applications: (1) synthetic data generation to augment policy training, (2) scalable virtual environments for policy evaluation, and (3) language-guided planning signals for downstream robot control. Technically, the core is a 60-layer Double-Stream MMDiT combined with MLLM action encoding. The 'Qwen-Robot Suite' that trended on HN the same day is the umbrella for these foundation models—world model plus manipulation policies—part of a broader push to give robotics the same 'foundation model' treatment as LLMs. In robotics, where real-world data collection is expensive, reusing a video-prediction model as simulator, data generator, and planner is a pragmatic route to bringing scaling laws to robots.",
        "key_points_ja": [
            "自然言語を統一の行動インタフェースにした動画世界モデル",
            "観測から物理的に妥当な未来映像を予測",
            "操作・自動運転・屋内ナビ・人→ロボット転移を統一",
            "合成データ生成/方策評価/言語誘導プランニングに活用",
            "60層Double-Stream MMDiT + MLLM行動エンコーディング",
            "ロボティクスの『基盤モデル化』を進める一手",
        ],
        "key_points_en": [
            "Video world model with language as unified action interface",
            "Predicts physically grounded future video from observations",
            "Unifies manipulation, driving, indoor nav, human-to-robot",
            "Powers synthetic data, policy eval, and planning signals",
            "Core: 60-layer Double-Stream MMDiT + MLLM action encoding",
            "Pushes 'foundation model' treatment into robotics",
        ],
    },
]

raw["date"] = DATE
out = DATA / f"{DATE}.json"
json.dump(raw, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("Wrote", out)
print("highlights:", len(raw["highlights"]))
