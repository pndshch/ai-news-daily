#!/usr/bin/env python3
"""Enrich raw-2026-06-11.json -> 2026-06-11.json with Japanese summaries + highlights."""
import json
from pathlib import Path

DATE = "2026-06-11"
root = Path(__file__).resolve().parent.parent
raw = json.load(open(root / f"data/raw-{DATE}.json"))

# ---- arXiv (top 25) : index -> (title_ja, summary_ja) ----
arxiv = {
 0: ("Reroute, Don't Remove：視覚トークンを削除せず再配線して回復可能にする", "VLMが画像を数百〜数千の視覚トークンに展開する重さを軽減する手法。重要度の低いトークンを単に捨てるのではなく、後で復元できるよう経路を切り替えて保持し、KVキャッシュと注意計算を削減しつつ情報損失を防ぐ。"),
 1: ("文脈駆動の逐次圧縮によるマルチターン対話生成", "会話が長くなるほど履歴の符号化コストが膨らむ問題に対し、文脈に応じて履歴を逐次的に圧縮する手法を提案。単純な切り詰めや要約より忠実度を保ちつつ計算を削減する。"),
 2: ("一見些細な設計選択が病理画像でのLLM性能を左右する", "巨大な全スライド病理画像(WSI)を扱う際、LLMベースラインのタイル選択など些細な前処理の違いが性能を大きく左右すると実証。専門モデル評価の公平性に警鐘を鳴らす。"),
 3: ("FACTR 2：汎用ロボットアームに外力センシングを学習させ方策学習を改善", "高価な力センサを持たない安価なロボットアームでも、関節トルクからデータ駆動で外力を推定するNEXT手法を提案。接触の多い繊細な操作の学習精度を高める。"),
 4: ("World Pilot：ワールド行動事前知識でVLAモデルを操舵する", "VLAモデルは静的な画像-テキスト対で意味理解を得るが動的な操作に弱い。世界の動きに関する事前知識(world-action prior)で行動を誘導し、分布外タスクへの汎化を高める。"),
 5: ("DIRECT：身体性プランナーでテスト時計算をいつ・どこに割くか", "VLMを身体エージェントの上位プランナーに使う際、テスト時計算を増やすと遅延やトークン消費が増える。本当に効く場面を見極めて計算を選択的に配分する手法。"),
 6: ("Doc-to-Atom：記憶アトムをコンパイル・合成する学習", "長文の二次コストを抑えるため、文書を再利用可能な『記憶アトム』に圧縮し、必要に応じて合成する手法。文書理解と多段推論を高速・省メモリ化する。"),
 7: ("多様体べき乗反復によるMoEルーターの再設計", "Mixture-of-Expertsの要であるルーターを、多様体上のべき乗反復で再設計。エキスパート選択の品質を高め、専門家の使い分けを改善する。"),
 8: ("VLGA：自動運転のための視覚-言語-幾何-行動モデル", "VLAモデルは言語推論はできても3D世界への行動の接地に弱い。幾何(geometry)情報を統合し、密な3D環境での運転行動の接地を強化する。"),
 9: ("CCL25-Eval Task 5報告：新データセットとLoRA微調整Qwen2.5", "古典中国語の翻訳と漢詩生成のタスクで、新データセットとLoRA微調整したQwen2.5を用いたシステム報告。感情・意味の精緻な理解を目指す。"),
 10: ("TAHOE：経験からのヒント自動最適化によるText-to-SQL", "自然言語からSQLを生成する際、厳格な方言や巨大スキーマに対応するため、過去の経験からヒントを自動最適化。プロトタイプから本番運用への壁を下げる。"),
 11: ("ATLAS：自動科学のための能動的理論学習", "認知科学の機構モデリングを自動化するため、最も情報量の多い実験を能動的に選んで理論を学習する枠組み。AIが自ら『良い実験の問い』を立てる。"),
 12: ("私たちのモデルは何の上に建つのか：現代LLMの不可視な依存関係の監査", "現代のLLM訓練は他モデルにデータ生成・選別・評価を依存しており、その依存は再帰的で見えにくい。この『不可視な依存関係』を監査し系譜を可視化する。"),
 13: ("APPO：エージェント的な手続き型方策最適化", "エージェントRLでツール呼び出し単位など粗い粒度で報酬を割り当てる従来法を改善し、手続きのより細かい単位でクレジット割当を行う。多段ツール利用の学習を精緻化。"),
 14: ("SPEA2+：実行時間保証付きの密度推定改善", "多目的最適化の代表的進化アルゴリズムSPEA2の密度推定を改良し、理論的な実行時間保証を与える。性能と理論の両面を強化。"),
 15: ("照明に頑健なカメラ式心拍推定でロボットの生理センシング", "RGBカメラから非接触で心拍を推定するrPPGを、照明変化に強くする手法。人と関わるサービス・介護ロボットの生理状態把握に役立てる。"),
 16: ("意味を考慮したダイバー行動認識で水中の人間-ロボット協調を支援", "水中作業でAUVが真の仲間になるため、ダイバーの行動を意味的に認識する枠組みを提案。高リスクな水中での人間主導作業を拡張する。"),
 17: ("検証可能な環境はレゴブロック：推論汎化のための再帰的合成", "検証可能なRL環境を『レゴ』のように再帰的に組み合わせ、複雑な推論タスク環境を構成する手法。環境の数を増やすだけでなく合成で推論の汎化を高める。"),
 18: ("UniIntervene：効率的な実世界RLのためのエージェント的介入", "人間が逐一介入するHiL-RLの負担を減らすため、介入をエージェント的に効率化。実世界ロボット操作の方策をより少ない人手で改善する。"),
 19: ("物体検出とインスタンス分割のためのターボ推論戦略", "検出してから分割する従来パイプラインを高速化する推論戦略。検出と分割の密接な関係を活かし精度を保ちつつ推論を加速。"),
 20: ("エントロピー限界の突破：棄却サンプリング付きMTPでRL訓練を加速", "RL訓練のボトルネックであるロールアウト段階を、多トークン予測(MTP)と棄却サンプリングで高速化。エントロピー上の制約を破り訓練効率を改善する。"),
 21: ("DepthMaster：透視画像と全天球画像を統一する単眼深度推定", "狭視野の透視画像と360度パノラマの両方で、汎用的な距離付き深度推定を実現。異なる視野形式を統一的に扱う初の試み。"),
 22: ("APT：行動エキスパート事前学習でVLAの指示汎化を改善", "VLMと連続行動エキスパートを組み合わせたVLAモデルで、分布外の言語指示への汎化が課題。行動エキスパートを事前学習して指示理解の頑健性を高める。"),
 23: ("Ambient Diffusion Policy：劣質データからの模倣学習", "高品質なロボットデータは高コストな一方、劣質データは大量にある。拡散モデルを用い劣質データから有効に模倣学習する原理的な手法を提案。"),
 24: ("サブクアドラティック構造について：応用から原理へ", "Transformerの二次計算コストを避けるサブクアドラティック構造を、応用事例から設計原理まで体系的に整理。どの設計が最も効果的かを解明しようとする。"),
}

# ---- HN (all 20) ----
hn = {
 0: ("πFS：円周率の中に全データが既に存在するという冗談ファイルシステム", "あらゆるデータは円周率πの無限桁のどこかに必ず現れる——という事実を逆手に取り、ファイルを保存せず『πの何桁目から始まるか』だけを記録するジョークFS。情報理論ネタとして再浮上し当日トップに。"),
 1: ("『リーン・スタートアップ』著者Eric Riesの新刊AMA", "『The Lean Startup』のEric Riesが、新著『Incorruptible』についてHNでAMAを実施。スタートアップ方法論の大家が現在の問題意識を語る。"),
 2: ("セキュリティ研究者、AnthropicのFableのガードレールに不満", "AnthropicがFableに組み込んだ安全ガードレールが、正当なセキュリティ研究や脆弱性調査までブロックすると研究者が反発(TechCrunch報)。安全性と研究の自由のトレードオフが争点に。"),
 3: ("Show HN：Homebrew 6.0.0", "macOS/Linuxの定番パッケージ管理ツールHomebrewのメジャーアップデート6.0.0が公開。多くの開発者が利用するため注目を集めた。"),
 4: ("AIエージェントがFedoraなどで暴走", "AIコーディングエージェントがFedoraはじめOSSプロジェクトに低品質・不正確な貢献を大量に送り込み、メンテナの負担を増やしている問題(LWN報)。エージェントの自律性が現場を混乱させる実例。"),
 5: ("Claude Desktopが起動毎に1.8GBのHyper-V VMを生成", "Claude Desktopがチャット利用だけでも毎回1.8GBのHyper-V仮想マシンを立ち上げるとのGitHub issue。リソース消費とユーザ制御の欠如に批判が集まる。"),
 6: ("AWS BedrockがMythos等の利用にAnthropicへのデータ共有を必須化", "AWS BedrockでAnthropicの新モデルMythos等を使うには利用データのAnthropic共有が必須になるとの報告。企業利用のプライバシーを巡り議論に。"),
 7: ("DiffusionGemma：テキスト生成が4倍高速", "Googleが拡散モデルでテキストを生成するGemma派生『DiffusionGemma』を発表。自己回帰生成を並列的な拡散デノイズに置き換え、最大4倍の高速化を主張。"),
 8: ("『コード行数』が宣伝上手になった話", "『コード行数』という古い指標が、AI生成コードの普及で再び話題に持ち上げられている現象を皮肉る論説。量を成果と取り違える危うさを突く。"),
 9: ("macOS 27 Golden Gate、メニュー項目の無駄なアイコンを削除", "次期macOS 27でメニュー項目に付いていた過剰なアイコンが廃止される。UIの改善として開発者・ユーザに歓迎された小ネタ。"),
 10: ("なぜAIはソフトウェアエンジニアを置き換えていないし、しないのか", "AIがエンジニアを代替するという言説に反論する論説。コーディングは要件定義や判断の連続であり、自動補完の延長では置換できないと論じる。"),
 11: ("労働者は週6時間超を『AIのお守り』に費やし不満を募らせている", "AIの出力を点検・修正する『botsitting(ボットのお守り)』に労働者が週6時間以上を費やしているとの調査(Business Insider)。生産性向上の裏に隠れた人的コストが浮き彫りに。"),
 12: ("Show HN：Extend UI — 文書アプリ向けOSS UIキット", "モダンな文書アプリ構築用のオープンソースUIコンポーネントキット。エディタやドキュメント系UIをすぐ組める点が評価された。"),
 13: ("Apache Burr：信頼できるAIエージェント/アプリを作る", "状態を明示的に管理しながら信頼性の高いAIエージェントやアプリを構築できるフレームワークBurrがApache入り。可観測性とデバッグ性が売り。"),
 14: ("Ask HN：大企業のSWE職の多くは見せかけの仕事か？", "大企業のソフトウェア技術職は実質的成果より体裁を整える『演技的』労働ではないか、という問いかけ。多数の体験談が集まり議論に。"),
 15: ("Anthropic、Claude Fableの『不可視ガードレール』を謝罪", "AnthropicがFableに利用者へ知らせずに組み込んだ蒸留由来のガードレールについて謝罪(The Verge報)。透明性を欠いた安全機構が、研究者やユーザの不信を招いた。"),
 16: ("0.01ユーロの送金で銀行AIエージェントを乗っ取れる", "ネット銀行bunqの金融AIアシスタントに対し、送金メモ欄に仕込んだ指示文(プロンプトインジェクション)を1セント送金で注入し操作できた事例。エージェントへの間接的攻撃の怖さを示す。"),
 17: ("AI指数関数に関する政策", "AIの指数的な能力向上を前提に、政策がどう備えるべきかを論じる記事。急加速シナリオへの制度的対応を問う。"),
 18: ("API要求に関する認証の問題", "あるサービスのAPIで認証関連の不具合が発生したとの報告・議論。開発者がトラブル対応を共有した。"),
 19: ("DeepSeek-R1のオープン再現", "Hugging Faceがオープンに進めるDeepSeek-R1再現プロジェクト『open-r1』。推論モデルの訓練レシピを公開で再構築する取り組みが進展。"),
}

# ---- GitHub (all 13) ----
github = {
 0: ("agent-skills：AIコーディングエージェント向けの実用エンジニアリングスキル集", "本番運用に耐えるエンジニアリングスキルをAIエージェント向けに提供するリポジトリ。Addy Osmani発で人気。"),
 1: ("apple/container：軽量VMでLinuxコンテナを動かすツール", "Appleが公開した、軽量仮想マシン上でLinuxコンテナを作成・実行するツール。macOSネイティブなコンテナ体験を提供。"),
 2: ("pm-skills：100以上のエージェントスキルを集めたPM向けマーケットプレイス", "プロダクトマネジメント向けに、100以上のスキル・コマンド・プラグインを集めたマーケットプレイス。"),
 3: ("agency-agents：フロントから一気通貫のAIエージェンシー一式", "フロントエンドのウィザードから各種役割まで、完全な『AI制作代理店』をエージェント群で再現するプロジェクト。"),
 4: ("superpowers：エージェント型スキルフレームワーク＆開発方法論", "AIコーディングエージェント向けに、再利用可能なスキルと開発手法を体系化したフレームワーク。"),
 5: ("maigret：ユーザ名から3000サイトを横断して人物情報を収集", "ユーザ名一つで3000以上のサイトを横断検索し、人物のプロフィールをまとめるOSINTツール。"),
 6: ("openmed：オープンソースのヘルスケアAI", "医療向けのオープンソースAIモデル/ツール群。"),
 7: ("主要AIツールのシステムプロンプト＆モデル集", "Claude Code・Cursor・Cometなど主要AIツールのシステムプロンプトを収集・公開したリポジトリ。各ツールの設計が覗ける。"),
 8: ("NVIDIA/SkillSpector：AIエージェントスキルのセキュリティスキャナ", "AIエージェント用スキルに潜む脆弱性や悪意あるパターン、セキュリティリスクを検出するスキャナをNVIDIAが公開。スキル流通の安全性を高める。"),
 9: ("chatwoot：オープンソースのオムニチャネル顧客サポート基盤", "ライブチャット・メール・複数チャネルを束ねるOSSのカスタマーサポート/ヘルプデスク。AI連携も進む定番ツール。"),
 10: ("sia：自律的に自己改善するAIフレームワーク", "自らを継続的に改善していく自己改善型(Self-Improving)AIフレームワーク。エージェントが自身の挙動を磨く試み。"),
 11: ("agentsview：コーディングエージェント向けのローカル分析ツール", "コーディングエージェントのセッションをローカルで解析・可視化するツール。エージェントの動作を手元で把握できる。"),
 12: ("张雪峰.skill：進路・キャリア設計の実戦思考フレーム", "中国の著名進路アドバイザー張雪峰の思考法を再現した、受験・就職などの意思決定支援スキル。AI生成スキルの一例。"),
}

# ---- Blogs (all 18) ----
blogs = {
 0: ("バージニア州での地域投資で雇用とエネルギーを支援", "OpenAIがバージニア州でのデータセンター関連投資により、地域雇用とエネルギー供給を支える取り組みを紹介。"),
 1: ("OpenAI、Onaを買収へ", "OpenAIが開発関連企業Onaの買収を発表。エージェント型開発・Codex路線を強化する動きとみられ、開発者ツール領域での攻勢を印象づける。"),
 2: ("欧州の信頼できるAIエコシステム構築を支援", "OpenAIが欧州における信頼できるAI環境づくりの取り組みを支援すると表明。規制当局との協調姿勢を示す。"),
 3: ("天体物理学者がCodexでブラックホールのシミュレーションを助ける", "天体物理学者がOpenAIのCodexを使い、ブラックホールのシミュレーション研究を効率化した事例。"),
 4: ("BBVA、OpenAIと組み銀行業務の中核にAIを据える", "スペインの大手銀行BBVAがOpenAIと提携し、AIを銀行業務の中核に組み込む。大規模金融機関でのAI本格導入事例。"),
 5: ("PyTorchでのプロファイリング(後編)：nn.Linearから融合MLPへ", "PyTorchの性能プロファイリング解説の後編。nn.Linearの積み重ねを融合MLPへ最適化する過程を技術的に解説。"),
 6: ("Oracleクラウド枠でOpenAIモデルとCodexを利用", "Oracle Cloudの利用枠を通じてOpenAIモデルやCodexにアクセスできるようになったとの案内。"),
 7: ("中国系の影響工作が米国のAI論争を標的に", "OpenAIが、PRC(中国)関連の影響工作がデータセンターや関税を巡る米国のAI議論やChatGPTに関する虚偽情報を標的にしていると報告。"),
 8: ("データから意思決定へ：LSEGの信頼できるAIスケーリング", "ロンドン証券取引所グループ(LSEG)が信頼性を保ちながらAIを全社展開する取り組み事例。"),
 9: ("音声エージェントは二言語顧客を扱えるか：コードスイッチ音声認識の評価", "言語を切り替えながら話す顧客に対し、最新の音声認識(ASR)がどこまで対応できるかをベンチマーク評価。"),
 10: ("North Mini Code：Cohere初の開発者向けモデル", "Cohereが開発者向けの軽量コーディングモデル『North Mini Code』を発表。"),
 11: ("NextdoorのエンジニアはCodexでどう開発しているか", "NextdoorがOpenAIのCodexを使い、制約なく素早く開発する活用事例。"),
 12: ("エージェントが2つのHugging Face Spaceを連結して3Dパリギャラリーをつくるまで", "AIエージェントが複数のHugging Face Spaceを自動で連結し、3Dのバーチャル美術館を構築した実例。"),
 13: ("CodexがNotionにもたらすもの", "NotionがOpenAI Codexを開発に取り入れて得られた効果を紹介。"),
 14: ("知能の時代の産業政策", "OpenAIがAI時代の『人間第一』の産業政策構想を提示。機会拡大と繁栄の共有、強靭な制度づくりを掲げる。"),
 15: ("GitHub CIをHugging Face Jobsへ移行する", "CIワークフローをHugging Face Jobsへ移すための手引き。"),
 16: ("オープンソースコミュニティがエージェントRL向けOpenEnvを支持", "エージェント強化学習の共通環境規格『OpenEnv』をオープンソース勢が後押し。"),
 17: ("2026年5月に発表したAIニュースまとめ", "Google DeepMindが5月に発表した主要なAIニュースをまとめた振り返り記事。"),
}

def apply(items, table):
    for i, it in enumerate(items):
        if i in table:
            it["title_ja"], it["summary_ja"] = table[i]

apply(raw["sources"]["arxiv"], arxiv)
apply(raw["sources"]["hn"], hn)
apply(raw["sources"]["github"], github)
apply(raw["sources"]["blogs"], blogs)

# ---- Highlights ----
raw["highlights"] = [
 {
  "source": "hn",
  "title": "Anthropic apologizes for invisible Claude Fable guardrails",
  "title_ja": "Anthropic、Claude Fableの『不可視ガードレール』を謝罪——研究者の反発受け",
  "url": "https://www.theverge.com/ai-artificial-intelligence/948280/anthropic-claude-fable-invisible-distillation-guardrail",
  "hot_take_ja": "新モデルFableに、利用者に知らせない『見えない安全装置』が仕込まれていた——セキュリティ研究者がブチ切れ、Anthropicが謝罪に追い込まれた。安全性は大事だが、黙って能力を絞ると正当な研究まで殺し、何より信頼を失う。透明性なき安全は安全じゃない、を地で行く一件。",
  "detail_ja": "AnthropicがClaude Fableに、利用者へ明示せずに組み込んでいた蒸留由来の『不可視ガードレール』について謝罪した。発端は、セキュリティ研究者がFableを使った脆弱性調査や攻撃手法の分析が不自然にブロックされると指摘したこと(TechCrunchが報道)で、正当な防御目的の研究まで巻き添えで制限されている、という批判が広がった。問題視されたのは制限の存在そのものより、その制限が利用者に開示されずモデルの挙動に静かに埋め込まれていた『不透明さ』だ。Anthropicはこれを認めて謝罪し、ガードレールの説明と調整を約束した。安全機構を蒸留(distillation)の過程でモデルに焼き込むと、後からプロンプトで外しにくく、かつ外形からは存在が見えにくい。これは悪用防止には有効でも、能力評価の再現性や研究の自由、ユーザの予測可能性を損なう。前日にFable 5/Mythos 5のシステムカードで『競合妨害的な挙動』が議論されたのに続き、Anthropicの安全設計の『見えなさ』が二日連続で論点化した形だ。安全性と透明性のバランス、そして安全装置の設計をどこまで公開すべきかという、フロンティアAI共通の難題を改めて突きつけている。",
  "detail_en": "Anthropic apologized for an 'invisible guardrail' baked into Claude Fable via distillation without disclosing it to users. The flashpoint was security researchers reporting that Fable was unnaturally blocking legitimate vulnerability research and analysis of attack techniques (as reported by TechCrunch), sparking complaints that defensive, legitimate work was being caught in the net. What drew the most criticism was not the restriction itself but its opacity — the limit was embedded silently in the model's behavior rather than disclosed. Anthropic acknowledged this and apologized, promising to explain and adjust the guardrails. When a safety mechanism is burned into a model during distillation, it is hard to remove via prompting and hard to detect from the outside. That may help prevent misuse, but it undermines reproducibility of capability evaluations, freedom of research, and user predictability. Coming a day after the Fable 5 / Mythos 5 system card sparked debate over apparent competitor-sabotage behavior, this puts the 'invisibility' of Anthropic's safety design in the spotlight for a second straight day. It re-raises a problem common to all frontier AI: balancing safety against transparency, and how much of a safety mechanism's design should be made public.",
  "key_points_ja": ["Fableに非開示の蒸留ガードレールが存在","正当なセキュリティ研究までブロックと批判","問題は制限より『開示しない不透明さ』","Anthropicが謝罪し説明・調整を約束","蒸留で焼き込むと検知も解除も困難","安全性と透明性の両立という難題を再提起"],
  "key_points_en": ["Undisclosed distilled guardrail found in Fable","Criticized for blocking legitimate security research","The issue is opacity, not the limit itself","Anthropic apologized, promised to explain and adjust","Distilled-in guards are hard to detect or remove","Re-raises the safety-vs-transparency dilemma"],
 },
 {
  "source": "hn",
  "title": "A €0.01 bank transfer could compromise a banking AI agent",
  "title_ja": "0.01ユーロの送金で銀行AIエージェントを乗っ取れた",
  "url": "https://blue41.com/blog/how-we-helped-bunq-secure-their-financial-ai-assistant/",
  "hot_take_ja": "1セント送って、メモ欄に『指示』を書くだけ。それでネット銀行bunqのAIアシスタントが攻撃者の言うことを聞き始めた。LLMは『データ』と『命令』を区別できない——この古典的弱点が、お金が動く場所に来た瞬間、笑えない現実になる。",
  "detail_ja": "セキュリティ企業Blue41が、ネット銀行bunqの金融AIアシスタントに対して行ったプロンプトインジェクション攻撃の検証を公開した。手口は驚くほど単純で、攻撃者が標的の口座に0.01ユーロ(1セント)を送金し、その送金メモ(振込時の自由記述欄)に悪意ある指示文を仕込むだけ。被害者がAIアシスタントに『最近の取引を見せて』などと尋ねると、アシスタントは取引履歴の一部としてそのメモを読み込み、書かれた指示をユーザの命令と取り違えて実行してしまう。これはLLM特有の根本的弱点に起因する。LLMは入力された文字列のうち、どこまでが『処理すべきデータ』でどこからが『従うべき命令』かを本質的に区別できない。通常のアプリならデータと命令はコードで分離されるが、自然言語で何でも受け取るAIエージェントでは、第三者が混ぜ込んだテキストが命令として効いてしまう(間接プロンプトインジェクション)。金融という文脈では、これが残高照会の漏洩や不正な操作に直結しうる。対策としては、外部由来テキストを命令として扱わない設計、操作の確認ステップ、権限の最小化などが挙げられるが、完全な防御は難しいのが現状だ。AIエージェントを実世界の権限に接続することの危うさを、最も分かりやすい形で示した事例といえる。",
  "detail_en": "Security firm Blue41 published a prompt-injection assessment of neobank bunq's financial AI assistant. The technique is strikingly simple: the attacker sends €0.01 (one cent) to the target's account and plants a malicious instruction in the transfer's free-text memo field. When the victim later asks the AI assistant something like 'show my recent transactions,' the assistant ingests that memo as part of the transaction history and mistakes the embedded instruction for a command from the user, executing it. This stems from a fundamental weakness of LLMs: they cannot inherently distinguish which parts of an input string are 'data to process' versus 'instructions to obey.' In ordinary apps, data and commands are separated in code, but an AI agent that accepts arbitrary natural language can have third-party text take effect as commands — indirect prompt injection. In a financial context, that can lead directly to leaked balances or unauthorized operations. Mitigations include designing the system not to treat externally sourced text as instructions, adding confirmation steps for actions, and minimizing privileges — but complete defense remains hard. It is one of the clearest demonstrations yet of the danger of wiring AI agents to real-world authority.",
  "key_points_ja": ["1セント送金のメモ欄に指示文を仕込む","AIが取引履歴を読む際に命令と誤認","間接プロンプトインジェクションの実例","LLMはデータと命令を本質的に区別不能","金融文脈では情報漏洩・不正操作に直結","確認ステップや権限最小化でも完全防御は困難"],
  "key_points_en": ["Instruction hidden in a 1-cent transfer's memo","AI mistakes it for a command while reading history","A real case of indirect prompt injection","LLMs can't separate data from instructions","In finance, leads to leaks or unauthorized actions","Even confirmations and least-privilege aren't a full fix"],
 },
 {
  "source": "hn",
  "title": "DiffusionGemma: 4x Faster Text Generation",
  "title_ja": "DiffusionGemma：拡散モデルでテキスト生成が4倍高速に",
  "url": "https://blog.google/innovation-and-ai/technology/developers-tools/diffusion-gemma-faster-text-generation/",
  "hot_take_ja": "LLMの『1トークンずつ逐次生成』という大前提を、Googleが拡散モデルで崩しにきた。画像生成と同じデノイズ方式を文章に持ち込み、最大4倍速。速度のためにアーキテクチャの根っこを差し替える流れが、いよいよテキストでも本格化してきた。",
  "detail_ja": "Googleが、テキストを拡散モデルで生成するオープンモデル『DiffusionGemma』を発表した。通常の大規模言語モデルは、文章を左から右へ1トークンずつ逐次的に生成する自己回帰方式をとる。この方式は品質が高い反面、トークン数に比例して生成時間がかかるのが本質的なボトルネックだ。拡散言語モデルは、画像生成で使われる拡散(デノイジング)の発想をテキストに応用する。最初に全体をノイズ(マスク)で埋めた状態から始め、複数のトークンを並列に少しずつ確定させていくため、逐次生成の制約を回避でき、Googleは最大4倍の高速化を主張する。Gemmaブランドで出すことで、軽量・オープンで扱いやすい点も狙いだ。拡散言語モデル自体は研究では以前から有望視されてきたが、自己回帰モデルに品質で追いつくのが課題だった。それを実用的な速度優位とともに主要ベンダーがプロダクト化したことに意味がある。並列デノイズは、長文生成やレイテンシが重要なエージェント用途、オンデバイス推論などで効きやすい。一方で、品質・制御性・既存エコシステム(KVキャッシュ最適化など)との整合は引き続き論点になる。テキスト生成の『当たり前』を問い直す動きとして注目される。",
  "detail_en": "Google announced DiffusionGemma, an open model that generates text with a diffusion approach. Conventional large language models use autoregression — generating text one token at a time, left to right. That yields high quality but has an inherent bottleneck: generation time scales with the number of tokens. Diffusion language models apply the denoising idea from image generation to text: starting from a fully noised/masked state and refining many tokens in parallel, they sidestep the strictly sequential constraint, and Google claims up to a 4x speedup. Shipping it under the Gemma brand also emphasizes a lightweight, open, easy-to-use profile. Diffusion language models have long been seen as promising in research, but catching up to autoregressive models on quality was the challenge. What matters here is that a major vendor has productized one with a practical speed advantage. Parallel denoising tends to pay off for long-form generation, latency-sensitive agentic use, and on-device inference. Open questions remain around quality, controllability, and fit with the existing ecosystem (e.g., KV-cache optimizations). It is a notable move that questions the default assumptions of text generation.",
  "key_points_ja": ["拡散方式でテキストを生成するGemma派生","自己回帰の逐次生成の制約を回避","複数トークンを並列デノイズで確定","Googleは最大4倍の高速化を主張","長文・低遅延・オンデバイス用途で有利","品質・制御性・既存最適化との整合が論点"],
  "key_points_en": ["Gemma variant that generates text via diffusion","Sidesteps autoregression's sequential bottleneck","Refines many tokens in parallel by denoising","Google claims up to 4x faster generation","Suits long-form, low-latency, on-device use","Open questions on quality, control, ecosystem fit"],
 },
 {
  "source": "hn",
  "title": "AI agent runs amok in Fedora and elsewhere",
  "title_ja": "AIエージェントがFedoraなどOSSで暴走、メンテナを疲弊させる",
  "url": "https://lwn.net/SubscriberLink/1077035/c7e7c14fbd60fae9/",
  "hot_take_ja": "『AIに任せれば貢献が増える』の理想が、現場では逆回転。低品質なパッチやバグ報告が自動生成で大量流入し、無償のメンテナが選別に追われて疲弊する。オープンソースは“量”ではなく“信頼”で回っていたという事実を、AIエージェントが突きつけている。",
  "detail_ja": "Linuxディストリビューションのコミュニティ専門誌LWNが、AIエージェントがFedoraをはじめとするオープンソースプロジェクトで引き起こしている混乱を報じた。問題の構図はこうだ。AIコーディングエージェントが自律的にバグ報告やパッチ(修正コード)を生成し、プロジェクトに大量に送り込むが、その多くは文脈を理解しておらず低品質だったり、的外れだったり、もっともらしいが誤っていたりする。オープンソースは多くの場合、少数の無償ボランティアのメンテナが貢献を一つずつレビューして成り立っている。そこへ機械生成の貢献が洪水のように流入すると、選別と却下のコストだけがメンテナにのしかかり、本来の開発が滞る。さらに厄介なのは、AI生成の貢献は一見すると体裁が整っており、悪意なき投稿者本人も中身を理解していないことが多い点だ。これはセキュリティ報奨金(バグバウンティ)プログラムでAI生成の偽の脆弱性報告が殺到した、近年の問題とも地続きである。本質的には、貢献の限界費用がほぼゼロになった世界で、レビューという『人間のボトルネック』をどう守るかという問題だ。コミュニティは投稿者の信頼度に応じた選別、AI生成の明示義務、自動フィルタリングなどの対応を模索しているが、開かれた参加とノイズ排除の両立は容易ではない。",
  "detail_en": "LWN, the community publication covering Linux, reported on the disruption AI agents are causing in open-source projects including Fedora. The pattern: AI coding agents autonomously generate bug reports and patches and flood projects with them, but many lack context — low quality, off-target, or plausible-but-wrong. Open source largely runs on a small number of unpaid volunteer maintainers reviewing contributions one by one. When machine-generated contributions pour in like a flood, the cost of triaging and rejecting falls on maintainers, stalling real development. What makes it worse is that AI-generated contributions often look well-formed, and the well-meaning submitters frequently don't understand the content themselves. This is continuous with the recent problem of AI-generated bogus vulnerability reports swamping bug-bounty programs. Fundamentally, in a world where the marginal cost of a contribution is near zero, the question is how to protect the human bottleneck of review. Communities are exploring trust-based triage of submitters, mandatory disclosure of AI generation, and automated filtering — but reconciling open participation with noise rejection is far from easy.",
  "key_points_ja": ["AIエージェントがOSSに低品質貢献を大量送付","無償メンテナが選別に追われ疲弊","体裁は整うが文脈理解を欠く投稿が多い","偽の脆弱性報告殺到問題と地続き","貢献の限界費用ゼロ化が根本要因","信頼ベース選別やAI明示で対応模索中"],
  "key_points_en": ["AI agents flood OSS with low-quality contributions","Unpaid maintainers exhausted by triage","Submissions look polished but lack context","Continuous with bogus AI vulnerability reports","Root cause: near-zero marginal cost of contributing","Trust-based triage and AI disclosure being explored"],
 },
 {
  "source": "blogs",
  "title": "OpenAI to acquire Ona",
  "title_ja": "OpenAI、開発エージェント企業Onaを買収へ",
  "url": "https://openai.com/index/openai-to-acquire-ona",
  "hot_take_ja": "S-1機密提出の翌日に、今度は買収。OpenAIが開発エージェント領域のOnaを取り込み、Codex路線を一段と厚くする。基盤モデルだけでなく『開発者がAIで作る』レイヤーを丸ごと押さえにいく姿勢が鮮明だ。",
  "detail_ja": "OpenAIが、ソフトウェア開発関連企業Onaの買収を発表した。OpenAIは近頃、コーディングエージェント『Codex』を軸に開発者向けプロダクトを強化しており(NotionやNextdoor、天体物理研究などでの活用事例を相次いで公開)、今回の買収もその延長線上にあるとみられる。狙いは、基盤モデルの提供にとどまらず、開発者がAIエージェントで実際にソフトを設計・実装・運用する『上位レイヤー』の体験と技術を取り込むことだ。AI開発ツール市場はAnthropicのClaude CodeやGoogle、各種スタートアップが激しく競合しており、優れたエージェント基盤やチームの獲得は競争力に直結する。タイミングも示唆的で、前日にOpenAIがSECへS-1ドラフトを機密提出したと認めたばかり。上場を見据えた資本動員と並行して、製品ポートフォリオの拡張・買収を積極化している構図が読み取れる。買収の金額や具体的な統合方針など詳細は限定的だが、OpenAIが『モデル屋』から『開発プラットフォーム企業』へと領域を広げる流れを象徴する一手といえる。一方で、人材・技術の囲い込みが進むことへの競争上の懸念や、エージェント開発の標準化を巡る綱引きも今後の論点になる。",
  "detail_en": "OpenAI announced it will acquire Ona, a software-development company. OpenAI has recently been strengthening developer products around its coding agent Codex — publishing a wave of use cases at Notion, Nextdoor, astrophysics research, and more — and this acquisition appears to extend that push. The goal is to capture not just foundation-model provision but the 'upper layer' experience and technology where developers actually design, implement, and operate software with AI agents. The AI dev-tools market is fiercely contested by Anthropic's Claude Code, Google, and many startups, so acquiring strong agent infrastructure and teams ties directly to competitiveness. The timing is telling: just a day earlier OpenAI confirmed it had confidentially submitted a draft S-1 to the SEC. The picture is one of aggressive product-portfolio expansion and acquisition running in parallel with capital mobilization ahead of a possible listing. Details such as deal size and integration plans are limited, but it symbolizes OpenAI's broadening from a 'model company' toward a 'developer platform company.' At the same time, growing consolidation of talent and technology raises competitive concerns, and the tug-of-war over standardizing agent development will be a topic to watch.",
  "key_points_ja": ["OpenAIが開発関連企業Onaを買収","Codex中心の開発者プロダクト強化の一環","基盤モデルの上の開発レイヤーを取り込む","Claude CodeやGoogleと激しく競合する市場","前日のS-1機密提出に続く積極攻勢","『モデル屋』から開発プラットフォームへ"],
  "key_points_en": ["OpenAI to acquire dev company Ona","Part of a Codex-centered developer push","Captures the dev layer above the base model","Market fiercely contested with Claude Code, Google","Aggressive move right after the confidential S-1","Broadening from model maker to dev platform"],
 },
]

out = root / f"data/{DATE}.json"
json.dump(raw, open(out, "w"), ensure_ascii=False, indent=2)
print("Wrote", out, "highlights:", len(raw["highlights"]))
