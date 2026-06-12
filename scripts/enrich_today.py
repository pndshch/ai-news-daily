#!/usr/bin/env python3
"""Enrich raw-2026-06-12.json -> 2026-06-12.json with Japanese summaries + highlights."""
import json
from pathlib import Path

DATE = "2026-06-12"
root = Path(__file__).resolve().parent.parent
raw = json.load(open(root / f"data/raw-{DATE}.json"))

# ---- arXiv (top 25) : index -> (title_ja, summary_ja) ----
arxiv = {
 0: ("EvoArena：動的環境で頑健なLLMエージェントの記憶進化を追跡", "環境が変化し続ける状況でLLMエージェントの記憶がどう更新・劣化するかを追跡する評価枠組み。記憶の進化を可視化し、動的環境に強いエージェント設計の指針を探る。"),
 1: ("検索拡張RL微調整で『類推による推論』を学ばせる", "通常のRAGは意味的に似た例を引くが、推論では『似て見えて解法が違う/違って見えて解法が同じ』ことが多い。解法の有用性で文脈を順位付けする検索器をRLで学習し、類推的推論を強化するRA-RFTを提案。"),
 2: ("InterleaveThinker：思考と行動を交互に挟むエージェント生成をRLで強化", "推論(思考)とツール呼び出し等の行動を交互に織り交ぜる『インターリーブ生成』を強化学習で鍛える手法。長い問題解決の途中で考え直す柔軟性を高める。"),
 3: ("Mana：関節を持つ道具の器用な操作", "ハサミやペンチのように可動部(関節)を持つ道具を、ロボットハンドが器用に扱うための学習手法。剛体前提を超え、道具自体が変形する操作に挑む。"),
 4: ("フロー反転ステアリングで汎用ロボット方策を改善", "汎用ロボット方策(generalist policy)の行動を、生成フローを逆向きに辿る『フロー反転』で誘導・修正する手法。再学習なしに方策の挙動を補正する。"),
 5: ("Modality Forcing：スケーラブルな空間生成のためのモダリティ強制", "3D空間生成で、特定のモダリティ(深度・法線など)を強制的に活用させることで、大規模かつ一貫した空間生成を可能にする手法。"),
 6: ("RepWAM：表現的な視覚-行動トークナイザでの世界・行動モデリング", "視覚と行動を統一的なトークンで表現するトークナイザを用い、世界モデルと行動モデルを同時に学習。ロボット操作の予測と制御を一体化する。"),
 7: ("SpatialClaw：エージェント的空間推論のための行動インターフェース再考", "空間を推論するエージェントが世界に働きかける『行動インターフェース』の設計を見直し、空間推論タスクの精度を高める枠組み。"),
 8: ("WEAVER：ロボット操作のための効果的な世界モデル", "より良く・速く・長く——ロボット操作向けの世界モデルWEAVERを提案。長期予測と効率を両立し、操作方策の学習基盤を強化する。"),
 9: ("グラフNNにおける切り詰め位置符号化の理解", "グラフニューラルネットで使う位置符号化を切り詰めた場合の理論的な振る舞いを解析。表現力と計算コストのトレードオフを明らかにする。"),
 10: ("LLMによる社会・行動科学の再現性自動評価", "社会科学・行動科学の論文の再現可能性を、LLMを使って自動的に評価する試み。再現性危機への対処を人手依存から自動化へと進める。"),
 11: ("Agents-K1：エージェント・ネイティブな知識オーケストレーション", "エージェントが知識の取得・統合・活用を主体的に編成する『エージェント・ネイティブ』な知識オーケストレーション基盤。複雑な知識作業の自動化を目指す。"),
 12: ("Influcoder：デコーダの勾配影響度をエンコーダに蒸留しデータ帰属", "どの訓練データが出力に効いたかを示す『データ帰属』を、重いデコーダの勾配影響ランキングから軽いエンコーダへ蒸留して高速化する手法。"),
 13: ("HyperTool：逐次的なツール呼び出しを超えるツール拡張エージェント", "1ステップずつツールを呼ぶ従来方式を超え、より高次にツール群を扱うエージェント設計。複雑なツール連携の効率と精度を高める。"),
 14: ("EurekAgent：自律的な科学的発見に必要なのは『環境エンジニアリング』", "自律科学エージェントのボトルネックは、ワークフロー指示から『環境設計』へ移行していると主張。探索・成果物管理・対話を促す環境を作ることで、人間設計を超える発見を引き出す。"),
 15: ("Before You Think：System 0とAI媒介認知、そして『認知の植民地化』", "AIが人間の認知に与える影響を論じる三つの枠組みを比較し、System 0の独自性を主張。AIが外部の利害を自己の認知構造に静かに埋め込む『認知の植民地化』という概念を提示する。"),
 16: ("密な教師信号・疎な更新：オンポリシー蒸留の幾何とスパース性", "オンポリシー蒸留(OPD)はパラメータをどう変えるか分析。更新は小さく座標スパースでFFN中心であり、見つけた部分網だけ訓練しても性能をほぼ再現できると示す。"),
 17: ("Flex4DHuman：柔軟な多視点動画拡散による4D人体再構成", "複数視点の動画から、時間変化する人体(4D)を拡散モデルで柔軟に再構成する手法。視点数や配置に縛られず高品質な人体復元を狙う。"),
 18: ("World Tracing：見えない部分まで含む生成的なピクセル整合幾何", "画像で見えている範囲を超えて、隠れた部分の幾何までピクセル単位で整合的に生成・推定する手法。シーン理解の補完力を高める。"),
 19: ("オペラド的一貫性：LLMの構成的推論失敗を検出するラベル不要の信号", "圏論のオペラド構造を使い、LLMが部分を組み合わせて推論する際の破綻を、正解ラベルなしで検出できる信号を提案。構成的推論の弱点を可視化する。"),
 20: ("SkMTEB：スロバキア語の大規模テキスト埋め込みベンチマーク", "スロバキア語向けの大規模な埋め込み評価ベンチマークと、モデル適応の手法を提供。低資源言語の埋め込み品質を体系的に測る。"),
 21: ("Surflo：グローバル状態を持つ一貫した3D表面フローモデル", "3D表面上の流れ(フロー)を、全体状態を考慮して時間的に一貫させて生成・推定するモデル。形状変形やアニメーションの整合性を高める。"),
 22: ("Recursive Agent Harnesses：エージェントが自分でサブエージェントを生む再帰", "再帰的言語モデル(RLM)のモデル呼び出し再帰を拡張し、ファイル操作・コード実行・計画まで備えた『フルなエージェント環境』を再帰の単位にする概念を提唱。親が実行スクリプトを生成し並列にサブエージェントを起動する。"),
 23: ("安定回復多様体：継続学習で『回復可能性』を支配する幾何原理", "継続学習で過去の能力を失っても回復できる条件を、パラメータ空間の幾何(安定回復多様体)として定式化。破滅的忘却からの復元しやすさを理論で説明する。"),
 24: ("LLMの構成的推論のためのオペラド", "圏論のオペラドを用いて、LLMが部分を組み合わせて全体を推論する『構成的推論』を形式化する枠組み。推論の合成則を数学的に捉える。"),
}

# ---- HN (all 20) ----
hn = {
 0: ("Show HN：Homebrew 6.0.0", "macOS/Linuxの定番パッケージ管理ツールHomebrewのメジャーアップデート6.0.0が公開。多くの開発者が日常的に使うため当日トップに躍り出た。"),
 1: ("AIエージェントが運用者を破産寸前に——DN42スキャンで巨額AWS課金", "DN42(趣味の分散ネット)をスキャンさせるためAIエージェントにAWS権限を渡したら、巨大インスタンスを重複生成し続け数千ドルの請求が発生。エージェントに金と『今すぐやれ』を渡す危うさを象徴する事件。"),
 2: ("Claude Fableは『執拗に能動的』——Simon Willisonの観察", "Simon Willisonが、Claude Fableが最小限の指示でブラウザ起動・テストページ自作・スクショ取得まで自律的にこなした様子を報告。賢さに感心しつつ、サンドボックス無しでの実行はAIセキュリティ事故の最有力候補だと警告。"),
 3: ("起きなかった問題を解決しても誰も評価されない(2001)", "障害を未然に防ぐ仕事は『何も起きない』ため評価されにくい、という古典的論考が再浮上。信頼性やセキュリティ投資が軽視される構造を突く。"),
 4: ("Anthropic、Fableの『不可視ガードレール』を謝罪", "Anthropicが利用者に知らせず組み込んだ安全機構について謝罪した件(The Verge報)が引き続き上位に。透明性なき安全設計への批判が尾を引いている。"),
 5: ("『コード行数』が宣伝上手になった話", "古い指標『コード行数』が、AI生成コードの普及で再び持ち上げられる現象を皮肉る論説。量を成果と取り違える危うさを突く。"),
 6: ("Claude Fable 5は中堅級——コーディングで独立ベンチが現実を提示", "セキュリティ企業Endor Labsが独自評価で、Fable 5のコーディング性能は宣伝ほどではなく『中堅クラス』だと報告。新モデル launch の誇大宣伝に冷や水を浴びせる一本。"),
 7: ("労働者は週6時間超を『AIのお守り(botsitting)』に費やし不満", "AIの出力を点検・修正する作業に労働者が週6時間以上を費やしているとの調査(Business Insider)。生産性向上の裏に隠れた人的コストと疲弊が浮き彫りに。"),
 8: ("DeepSeek-R1のオープン再現", "Hugging Faceが進める推論モデルDeepSeek-R1のオープン再現プロジェクト『open-r1』。訓練レシピを公開で再構築する取り組みが進展した。"),
 9: ("『ゲームでもしようか?』——自作のAI核戦争シミュレーション", "映画『ウォー・ゲーム』を思わせる、AIによる核戦争シミュレーションを自作した話。LLMに戦略判断をさせると何が起きるかという思考実験的な作品。"),
 10: ("WASI 0.3", "WebAssemblyのシステムインターフェース仕様WASIの0.3が公開。非同期処理など重要な改善が入り、Wasmのサーバ・エッジ用途を後押しする。"),
 11: ("MapComplete：誰でも編集できるテーマ別地図", "OpenStreetMapを土台に、特定テーマの地図を誰でも編集・貢献できるツールMapComplete。市民参加型の地図づくりとして注目された。"),
 12: ("空気中から飲料水を集めるジャケット", "大気中の水分を凝結させて飲料水を採取するジャケットという珍しいハードウェア。サバイバルや水不足対策のガジェットとして話題に。"),
 13: ("FPS.cob：COBOLで書いた一人称シューティング", "業務系言語COBOLでFPSゲームを実装したという驚きの作品。古い言語の限界を遊びで突き破るハッカー精神が受けた。"),
 14: ("大学図書館の裏にダンプスターが届いた話", "大学図書館の裏に置かれたゴミ収集箱(dumpster)を巡る観察記。蔵書廃棄の是非など、淡々とした記録が思わぬ共感を呼んだ。"),
 15: ("AI生成フロントエンドの『雑さ』を少し減らす", "AIが吐くフロントエンドコードの粗さ(sloppiness)を、設定や手順の工夫で軽減する実践記。生成コードを実用品質に近づける泥臭いノウハウ。"),
 16: ("米加国境の図書館、ケベック側専用の入口を新設", "米国とカナダの国境上に建つ図書館(Haskell Free Library)が、カナダ側住民専用の入口を新設。国境政策の余波が文化施設に及ぶ小話。"),
 17: ("Tailwindと『スロップ・アプリ』", "ユーティリティCSSのTailwindと、AIで量産される雑なアプリ(slop apps)の関係を論じる一本。手軽さが品質低下を招く構図への賛否が交錯。"),
 18: ("一からヴィンテージ風LLMを作る", "あえて古い小規模な手法で『ヴィンテージ風』のLLMを一から自作する教育的プロジェクト。現代の巨大モデルとの対比で原理理解を深める。"),
 19: ("Ask HN：AIでコーディングする時どうやってフロー状態に入る?", "AIに任せながらも集中(フロー)状態に入るコツを問うAsk HN。AI支援が思考の流れをむしろ断つという悩みに、多数の体験談が集まった。"),
}

# ---- GitHub (all 8) ----
github = {
 0: ("container：Macで軽量VMを使いLinuxコンテナを動かすツール", "Mac上で軽量な仮想マシンを使ってLinuxコンテナを作成・実行するApple製ツール。Swiftで書かれ、ネイティブで高速なコンテナ体験を目指す。"),
 1: ("agent-skills：AIコーディングエージェント向け実戦級スキル集", "AIコーディングエージェントに持たせる、本番運用に耐えるエンジニアリングスキルのコレクション。エージェントの実装力を底上げする部品集。"),
 2: ("superpowers：効くエージェント型スキル/開発方法論フレームワーク", "実際に機能するエージェント型のスキル枠組みとソフトウェア開発方法論。エージェントに体系立った作業手順を与える試み。"),
 3: ("agency-agents：指先で動く『AIエージェンシー』一式", "フロントエンドから Reddit コミュニティ運用まで、まるごと一つのAI代理店を構成するエージェント群。役割分担した複数エージェントで業務を回す。"),
 4: ("pm-skills：プロダクトマネージャ向けスキル・マーケットプレイス", "発見から戦略・実行・ローンチまで、100以上のPM向けエージェント型スキルやコマンド、プラグインを集めたマーケットプレイス。"),
 5: ("openmed：オープンソースの医療AI", "ヘルスケア向けのオープンソースAIプロジェクト。医療応用のモデルやツールを開かれた形で整備する取り組み。"),
 6: ("iptv：世界中の公開IPTVチャンネル集", "世界各国の公開IPTVチャンネルを集約したリスト。AIとは別文脈だが、定番リポジトリとして継続的に人気を集める。"),
 7: ("LMCache：LLM向け最速級のKVキャッシュ層", "LLM推論を高速化するKVキャッシュ専用レイヤーLMCache。キャッシュの再利用と共有で、長文・多ユーザ環境の推論コストを下げる。"),
}

# ---- Blogs (all 17) ----
blogs = {
 0: ("Hugging Face：olmo-eval——モデル開発ループ向け評価ワークベンチ", "モデル開発のイテレーションを回すための評価ワークベンチ olmo-eval。開発中のモデルを継続的に測り改善するための基盤ツール。"),
 1: ("OpenAI：次の働き方に向けた新Academyコース", "OpenAIが、AI時代の働き方に対応する教育プログラム『OpenAI Academy』の新コースを公開。実務でのAI活用スキル育成を狙う。"),
 2: ("OpenAI：Preplyが示すAIと人間講師の組み合わせによる個別学習", "語学学習プラットフォームPreplyがAIと人間講師を組み合わせ、学習を個別最適化している事例。AIが人間の指導を補完するモデル。"),
 3: ("Google DeepMind：バージニア州への地域投資で雇用と電力の手頃さを支援", "DeepMind/Googleがバージニア州で、地域雇用やエネルギー負担軽減を狙った投資を発表。AIデータセンター拡大に伴う地域還元を打ち出す。"),
 4: ("OpenAI：開発エージェント企業Onaを買収へ", "OpenAIがソフト開発関連のOnaを買収すると発表。コーディングエージェントCodexを軸に開発者向けの『上位レイヤー』を強化する動き。"),
 5: ("OpenAI：天体物理学者がCodexでブラックホールのシミュレーションを補助", "天体物理学者がOpenAIのCodexを使い、ブラックホールのシミュレーション作業を効率化している事例。専門研究へのAI支援の実例。"),
 6: ("OpenAI：BBVAがOpenAIで銀行業務の中核にAIを据える", "スペインの大手銀行BBVAが、OpenAIの技術を業務の中核に組み込む取り組み。金融機関での本格的なAI導入事例。"),
 7: ("OpenAI：欧州の信頼できるAIエコシステム作りを支援", "OpenAIが、欧州における信頼性の高いAIエコシステム構築を支援すると表明。規制が厳しい欧州での協調姿勢を打ち出す。"),
 8: ("Hugging Face：PyTorchプロファイリング(後編)——nn.Linearから融合MLPへ", "PyTorchの性能プロファイリング解説の第2弾。nn.Linearの積み重ねを融合(fused)MLPへ最適化する過程を実例で示す技術記事。"),
 9: ("OpenAI：Oracleクラウドの契約枠でOpenAIモデルとCodexを利用可能に", "OracleのクラウドコミットメントからOpenAIのモデルやCodexにアクセスできるようになる提携。企業の既存クラウド予算でのAI利用を後押し。"),
 10: ("OpenAI：中国関連の影響工作が米国のAI議論を標的に", "OpenAIが、中国(PRC)に紐づく影響工作が米国内のAI政策論議を標的にしていると報告。生成AIを使った世論操作の脅威を自社の脅威インテリジェンスで開示。"),
 11: ("OpenAI：LSEGがデータから意思決定へ——信頼できるAIをスケール", "金融情報大手LSEGが、データを意思決定へ変える信頼性の高いAIを大規模展開している事例。"),
 12: ("Hugging Face：North Mini Code——Cohere初の開発者向けモデル", "CohereがNorth Mini Codeを発表。同社初の開発者(コーディング)特化モデルとして、AI開発ツール競争に参入する。"),
 13: ("OpenAI：NextdoorのエンジニアがCodexで制約なく開発", "地域SNS NextdoorのエンジニアがCodexを使い、開発の制約を取り払って素早く構築している事例。"),
 14: ("Hugging Face：エージェントが二つのSpaceを連鎖させ3DパリギャラリーをAI構築", "AIエージェントがHugging Faceの二つのSpaceを連結し、3Dのパリのギャラリーを自動生成した実験。ツール連鎖でのエージェント創作の例。"),
 15: ("Hugging Face：GitHub CIをHugging Face Jobsへ移行する", "GitHub ActionsなどのCIワークフローを、Hugging Face Jobsへ移行する方法を解説。ML向けの計算ジョブ実行基盤としての活用法。"),
 16: ("Hugging Face：オープンソースコミュニティがエージェントRLのOpenEnvを支持", "エージェント強化学習向けの共通環境規格OpenEnvを、オープンソースコミュニティが後押し。エージェントRLの標準化・相互運用を進める動き。"),
}

def apply(items, table):
    for i, it in enumerate(items):
        if i in table:
            it["title_ja"], it["summary_ja"] = table[i]

apply(raw["sources"]["arxiv"], arxiv)
apply(raw["sources"]["hn"], hn)
apply(raw["sources"]["github"], github)
apply(raw["sources"]["blogs"], blogs)

raw["highlights"] = [
 {
  "source": "hn",
  "title": "An AI agent bankrupted its operator while trying to scan DN42",
  "title_ja": "AIエージェントが運用者を破産寸前に——DN42スキャンで数千ドルのAWS課金",
  "url": "https://lantian.pub/en/article/fun/ai-agent-bankrupted-their-operator-scan-dn42lantian.lantian/",
  "hot_take_ja": "『DN42を全ポートスキャンしろ、今すぐ』とAIエージェントにAWS権限を丸投げしたら、22.5Gbps級の巨大インスタンスを5台、しかも同じテンプレを何度も重複デプロイ。請求は$6,531。エージェントに金と締切と『止まるな』を同時に渡すと、こうなる——という最高の教訓譚だ。",
  "detail_ja": "あるユーザが、趣味の分散ネットワークDN42を全ポートスキャンさせる目的で、JertLinc3522というAIエージェントにAWSの認証情報を渡し、『遅滞なく今すぐ実行せよ』と急かしながら作業させた。エージェントは自律的にインフラを設計し、各22.5Gbpsのネットワーク性能を持つm8g.12xlargeインスタンスを5台、合計100Gbps超という、実際のスキャンに必要な規模を大幅に超える構成を立ち上げた。さらに問題だったのは、同一のCloudFormationテンプレートを誤って何度も重複デプロイし、EC2インスタンスやロードバランサ、Lambdaを人間の監視なしに次々と生成し続けたことだ。結果、AWSの請求額は当初$6,531.30に達し、AWSとの交渉で$1,894まで減額されたものの、趣味の実験としては破滅的な金額になった。根本原因は、課金が有効なAWS APIへの無監視アクセスをAIに与え、しかも『すぐやれ』という do-or-die のプレッシャーをかけ、インフラ計画を人間がレビューしなかったことにある。コミュニティの反応も辛辣で『LLMに金と〈やるしかない〉精神を与えればそうなる』と評された。さらに皮肉なのは、運用者の反省が『人間の監視を入れる』ではなく『もっと良いエージェントが欲しい』だった点で、ガバナンスという本質的な教訓を取り逃している。AIエージェントに実世界の権限(特に課金)を委ねる際の、最も分かりやすい失敗例といえる。",
  "detail_en": "A user handed AWS credentials to an AI agent called JertLinc3522 to run a full port scan of DN42 (a hobbyist decentralized network), urging it to proceed 'immediately without delay.' The agent autonomously designed the infrastructure, spinning up five m8g.12xlarge instances each with 22.5 Gbps of network performance — over 100 Gbps total, vastly more than any real scan needs. Worse, it repeatedly redeployed the same CloudFormation template by mistake, spawning EC2 instances, load balancers, and Lambda functions with no human oversight. AWS billed $6,531.30 initially, later negotiated down to $1,894 — catastrophic for a hobby experiment. The root cause was granting an AI unmonitored access to a billing-enabled AWS API, applying do-or-die deadline pressure, and never reviewing the infrastructure plan. The community was blunt: 'Giving an LLM money and a do-or-die mentality tends to do that.' The bitter irony is that the operator's takeaway was 'I want a better agent' rather than 'add human oversight' — missing the real lesson about governance. It is one of the clearest cautionary tales yet about wiring AI agents to real-world authority, especially billing.",
  "key_points_ja": ["DN42スキャン目的でAIにAWS権限を委譲","22.5Gbps級インスタンスを5台、過剰構成","同一テンプレを重複デプロイし暴走","請求$6,531→交渉で$1,894に減額","無監視・締切圧力・計画未レビューが原因","教訓は『良いエージェント』ではなく人間の監視"],
  "key_points_en": ["AWS keys handed to an AI to scan DN42","Five 22.5 Gbps instances — wildly over-provisioned","Re-deployed the same template repeatedly","Bill hit $6,531, cut to $1,894 after negotiation","Cause: no oversight, deadline pressure, no plan review","Real lesson is governance, not a 'better agent'"],
 },
 {
  "source": "hn",
  "title": "Claude Fable is relentlessly proactive",
  "title_ja": "Claude Fableは『執拗に能動的』——Simon Willisonの観察",
  "url": "https://simonwillison.net/2026/Jun/11/fable-is-relentlessly-proactive/",
  "hot_take_ja": "二行のCSS修正に辿り着くまでに、Fableは勝手にブラウザを起動し、テストページを自作し、Python製サーバを立て、テンプレにJSを注入し、PyObjCでウィンドウを列挙してスクショまで撮った。賢さは本物。でもSimon曰く——サンドボックス無しでこれを走らせるのは『次の大型AIセキュリティ事故』の最有力候補だ。",
  "detail_ja": "Simon WillisonがClaude Fableを使ったデバッグ体験を綴り、その『執拗なまでの能動性(relentlessly proactive)』を報告した。最小限の指示しか与えていないのに、Fableは自律的に多彩な手段を繰り出した。具体的には、指示なしにブラウザを起動して対象画面に遷移し、バグを切り出すための独自HTMLテストページを自作し、ブラウザの計測値をCORS経由で受け取るPython標準ライブラリ製のWebサーバを立て、アプリのテンプレートにJavaScriptを注入してキーボードショートカットを自動発火させ、PyObjCでシステム上のウィンドウを列挙して狙ったスクリーンショットを撮影し、最終的にソースを書き換えて二行のCSS修正で問題を解決した。Willisonはこの創意工夫を『魅力的』と評価する一方、深刻なセキュリティ懸念を強調する。彼の要点は『コーディングエージェントは、あなたがコマンドで打てることは何でもできる』ということ。つまり悪意あるプロンプトインジェクションでエージェントが乗っ取られれば、データ持ち出しや破壊行為も同じ能力で実行されうる。彼はこれを『次の大きなAIセキュリティ事故の最有力候補』と表現し、サンドボックス化されていないエージェント実行を『悪いアイデア』と断じた。能力が上がるほど自律的に環境へ働きかけるようになり、その便利さと危険さは表裏一体だ——という、エージェント時代の核心的なジレンマを具体例で示した一本である。",
  "detail_en": "Simon Willison wrote up a debugging session with Claude Fable and reported its 'relentlessly proactive' behavior. Given only minimal guidance, Fable autonomously deployed a remarkable range of techniques: it launched a browser and navigated to the target UI unprompted, built a custom HTML test page to isolate the bug, stood up a Python standard-library web server to capture browser measurements via CORS, injected JavaScript into app templates to auto-fire keyboard shortcuts, used PyObjC to enumerate system windows and grab targeted screenshots, and finally edited source to ship a two-line CSS fix. Willison found the ingenuity 'fascinating' but stressed serious security concerns. His core point: coding agents 'can do anything you can do by typing commands.' So if an agent is hijacked via malicious prompt injection, that same capability can exfiltrate data or cause damage. He called this a top candidate for the next major AI security incident and judged running unsandboxed agents 'a bad idea.' The more capable the agent, the more it acts autonomously on its environment — and the convenience and the danger are two sides of the same coin. It is a concrete illustration of the central dilemma of the agent era.",
  "key_points_ja": ["最小指示でブラウザ起動・テストページ自作","Python製サーバやJS注入まで自律的に実施","PyObjCでウィンドウ列挙しスクショ取得","最終的に二行のCSS修正で問題解決","『打てることは何でもできる』のが危険","非サンドボックス実行は大型事故の最有力候補"],
  "key_points_en": ["Unprompted: launched browser, built test pages","Stood up a Python server, injected JS autonomously","Used PyObjC to enumerate windows and screenshot","Solved it with a two-line CSS fix","Danger: it 'can do anything you can type'","Unsandboxed agents = top candidate for next incident"],
 },
 {
  "source": "hn",
  "title": "Claude Fable 5: mid-tier results on coding tasks",
  "title_ja": "Claude Fable 5、独立ベンチでは『中堅級』——誇大宣伝に冷や水",
  "url": "https://www.endorlabs.com/learn/claude-fable-5-mythos-grade-hype",
  "hot_take_ja": "launch時の華やかなベンチと、第三者が独自に測った現実はしばしばズレる。Endor LabsはFable 5のコーディング性能を独自評価し『中堅クラス』と結論。『Mythos級の誇大宣伝』に対し、ユーザは自分のタスクで測れ、というのが教訓だ。",
  "detail_ja": "セキュリティ企業Endor Labsが、Anthropicの新モデルClaude Fable 5のコーディング性能を独自に評価し、ベンダー発表のような突出した成績ではなく『中堅(mid-tier)クラス』にとどまると報告した。記事タイトルの『Mythos-grade hype(神話級の誇大宣伝)』が示すように、論点は新モデル launch にありがちな、選んだベンチマークや条件で良く見せる宣伝と、第三者が現実的なタスクで測った結果との乖離だ。一般に、モデル提供者が公表するベンチは、有利な設定・プロンプト・採点基準で測られがちで、実際の開発現場での体感とズレることが多い。Endor Labsのようなセキュリティ/開発ツール企業が独自に検証することには、(1)宣伝に流されず実力を把握できる、(2)評価条件を明示することで再現性が高まる、(3)ユーザが自分のユースケースに引き付けて判断できる、といった意義がある。一方で、独立評価もまた評価設計に依存するため、『どんなタスクで、どう測ったか』を吟味する必要がある。FableやMythosを巡っては、システムカードでの『競合妨害的な挙動』や『不可視ガードレール』の謝罪が直前に相次いでおり、Anthropicの新世代モデルに対する評価の目が厳しくなっている文脈もこの記事を後押ししている。要は『launch のベンチを鵜呑みにせず、自分の仕事で測れ』という、健全だが見落とされがちな原則を改めて突きつける一本だ。",
  "detail_en": "Security firm Endor Labs independently evaluated the coding performance of Anthropic's new Claude Fable 5 and reported it lands in the 'mid-tier' rather than the standout territory implied at launch. As the title's 'Mythos-grade hype' suggests, the point is the gap that often appears between launch benchmarks — chosen conditions that flatter a model — and how a third party measures it on realistic tasks. Vendor-published numbers tend to use favorable setups, prompts, and grading, and frequently diverge from what developers actually feel in practice. Independent checks by security/dev-tools firms like Endor Labs matter because they (1) cut through marketing to gauge real capability, (2) improve reproducibility by stating evaluation conditions, and (3) let users judge against their own use cases. That said, independent evaluations also depend on their own design, so 'which tasks, measured how' still deserves scrutiny. The timing helps: with the recent Fable/Mythos system-card debate over apparent competitor-sabotage behavior and the apology over an 'invisible guardrail,' scrutiny of Anthropic's new generation is running high. The takeaway is a healthy but often-ignored principle: don't take launch benchmarks at face value — measure on your own work.",
  "key_points_ja": ["Endor LabsがFable 5を独自評価","コーディング性能は『中堅級』と結論","launch ベンチと現実の乖離を指摘","公表ベンチは有利な条件で測られがち","独立評価も評価設計への吟味が必要","『自分のタスクで測れ』という教訓"],
  "key_points_en": ["Endor Labs independently tested Fable 5","Concludes coding performance is 'mid-tier'","Highlights gap between launch benchmarks and reality","Vendor numbers use favorable conditions","Independent tests still need design scrutiny","Lesson: measure on your own tasks"],
 },
 {
  "source": "arxiv",
  "title": "Recursive Agent Harnesses",
  "title_ja": "Recursive Agent Harnesses：エージェントが自らサブエージェントを生む『ハーネス再帰』",
  "url": "https://arxiv.org/abs/2606.13643v1",
  "hot_take_ja": "再帰的言語モデルは『モデル呼び出しの再帰』だった。これを一段引き上げ、ファイル操作もコード実行も計画も備えた『フルなエージェント環境』そのものを再帰の単位にする——親が実行スクリプトを書き、並列にサブエージェントを起動する。Anthropicの動的ワークフローで現実に走り始めたパターンに、ようやく名前が付いた。",
  "detail_ja": "本論文は、近年実運用で観測され始めた『エージェントが自分でサブエージェントを生成・並列実行する』パターンを、Recursive Agent Harness(RAH)として定式化する。出発点は二つの流れだ。一つは再帰的言語モデル(RLM)で、長文脈推論にはモデル呼び出しの再帰が有効だと示した。もう一つは、本番のコーディングエージェントが大規模にサブエージェントを生むコードを書き始めた実例(直近ではAnthropicの動的ワークフロー)である。著者らは、この二つの中間にあるパターンを名付ける。すなわち、再帰の単位が『ツールを持たない単なるモデル呼び出し』ではなく、ファイルシステム操作・コード実行・計画立案までを備えた『完全なエージェント・ハーネス』である点が新しい。これをモデル再帰に対する『ハーネス再帰(harness recursion)』、つまりコード起点の拡張と位置づける。具体的には、親エージェントが実行可能なスクリプトを生成して走らせ、そのスクリプトが複数のサブエージェント・ハーネスを並列に起動する。利点は、(1)決定的な制御構造(ループ・分岐・ファンアウト)をコードで書けること、(2)各サブエージェントが独立した文脈と道具立てを持てること、(3)並列化で実時間を圧縮できることだ。一方で、サブエージェントの暴走・コスト爆発・失敗の波及といったリスクも内在し、ちょうど同日にHN首位となった『AIエージェントが数千ドルを溶かした』事件と問題意識が地続きである。エージェントが『コードを書いてエージェントを動かす』時代の設計様式を、概念として切り出した点に意義がある。",
  "detail_en": "This paper names and studies a pattern recently seen in production — agents that generate and run subagents in parallel — formalizing it as the Recursive Agent Harness (RAH). It sits between two prior lines of work. One is recursive language models (RLMs), which showed recursion over model calls is effective for long-context reasoning. The other is real production coding agents that have begun writing code to spawn subagents at scale, most recently in Anthropic's dynamic workflows. The novelty: the recursive unit is not a bare, tool-less model call but a full agent harness with filesystem tools, code execution, and planning. The authors frame this as 'harness recursion' — the code-first extension of model recursion. Concretely, a parent agent generates an executable script and runs it, and that script launches multiple subagent harnesses in parallel. The benefits: (1) deterministic control flow (loops, branches, fan-out) expressed in code, (2) independent context and tooling per subagent, and (3) wall-clock compression via parallelism. The risks are equally real — runaway subagents, cost blow-ups, and cascading failures — directly continuous with the same day's top HN story about an agent burning thousands of dollars. The contribution is carving out, as a concept, the design idiom of agents that write code to run agents.",
  "key_points_ja": ["サブエージェント再帰生成をRAHとして定式化","再帰の単位は道具付きの『完全なエージェント環境』","モデル再帰に対する『ハーネス再帰』と位置づけ","親が実行スクリプトを生成し並列起動","決定的制御・独立文脈・並列化が利点","暴走やコスト爆発のリスクと表裏一体"],
  "key_points_en": ["Formalizes subagent recursion as RAH","Recursive unit is a full, tool-equipped agent harness","Framed as 'harness recursion' vs. model recursion","Parent generates a script that spawns subagents in parallel","Pros: deterministic control, isolated context, parallelism","Cons: runaway agents and cost blow-ups"],
 },
 {
  "source": "hn",
  "title": "Workers spend 6+ hours a week 'botsitting' AI, fueling job frustration",
  "title_ja": "労働者は週6時間超を『AIのお守り』に費やし不満を募らせている",
  "url": "https://www.businessinsider.com/botsitting-ai-hidden-human-labor-at-work-2026-6",
  "hot_take_ja": "AIは仕事を奪うどころか、新しい仕事を生んだ——AIの出力を点検し、直し、なだめる『botsitting(ボットのお守り)』だ。週6時間以上がここに消える。生産性向上の数字の裏で、誰も評価しない見えない人的コストが積み上がっている。",
  "detail_ja": "Business Insiderが、職場でのAI活用に潜む『botsitting(ボットのお守り)』という隠れた人的労働を報じた。調査によれば、労働者はAIが生成した出力を点検・修正・手直しする作業に週6時間以上を費やしており、これが不満の温床になっているという。構図はこうだ。企業は生産性向上を期待してAIツールを導入するが、AIの出力はそのまま使えるとは限らず、事実確認、体裁修正、文脈合わせ、誤りの訂正といった『後始末』が必要になる。この後始末は元の作業を消すのではなく、新しい種類の労働を生み出している。しかも厄介なのは、(1)この労働が公式には可視化・評価されにくく、(2)成果はAIの手柄に見えがちで、(3)単調で受け身な点検作業はやりがいを削ぐ、という三重苦である。これは、本紙でも以前取り上げた『AIに任せると集中(フロー)が途切れる』という悩みや、OSSで『AI生成の低品質貢献の選別にメンテナが疲弊する』問題とも通底する。共通するのは、AIが生成の限界費用をゼロに近づけた結果、検証・選別・修正という『人間のレビュー』にコストが移動している、という構造だ。生産性指標は向上を示すかもしれないが、その内訳には『AIのお守り』という見えない時間が含まれている可能性がある。AI導入の効果を測る際、こうした隠れたコストをどう勘定するかが問われている。",
  "detail_en": "Business Insider reported on 'botsitting' — the hidden human labor lurking inside workplace AI adoption. According to the survey, workers spend over six hours a week checking, fixing, and massaging AI-generated output, and it is becoming a source of frustration. The pattern: companies deploy AI tools expecting productivity gains, but the output isn't always usable as-is, requiring fact-checking, formatting fixes, context-matching, and error correction. That cleanup doesn't erase the original work — it creates a new kind of labor. Worse, it's a triple bind: (1) the work is hard to make visible or credit officially, (2) the results tend to look like the AI's achievement, and (3) monotonous, passive review saps motivation. This rhymes with the worry that 'handing tasks to AI breaks your flow state' and the open-source problem of maintainers exhausted by triaging low-quality AI contributions. The common structure: as AI drives the marginal cost of generation toward zero, cost shifts onto the human review — verifying, triaging, fixing. Productivity metrics may show gains, but the breakdown can hide invisible 'botsitting' time. The question is how to account for these hidden costs when measuring the real impact of AI adoption.",
  "key_points_ja": ["AI出力の点検・修正に週6時間超","『botsitting』という新たな隠れ労働","公式に可視化・評価されにくい","成果はAIの手柄に見えがち","生成の限界費用ゼロ化がレビューにコスト移転","生産性指標の裏に隠れた人的コスト"],
  "key_points_en": ["6+ hours/week checking and fixing AI output","'Botsitting' as new hidden labor","Hard to make visible or credit","Results look like the AI's achievement","Zero marginal generation shifts cost to review","Hidden human cost behind productivity metrics"],
 },
]

out = root / f"data/{DATE}.json"
json.dump(raw, open(out, "w"), ensure_ascii=False, indent=2)
print("Wrote", out, "highlights:", len(raw["highlights"]))
