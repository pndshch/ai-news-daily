#!/usr/bin/env python3
"""Refresh enrichment for 2026-05-15.

Merges new raw items with existing translations and refreshes the highlights
to surface fresh, high-impact stories. URL-keyed reuse avoids re-translating
items that were already enriched in the prior pass.
"""
import json
from pathlib import Path

DATE = "2026-05-15"
ROOT = Path(__file__).resolve().parent.parent
SRC_RAW = ROOT / "data" / f"raw-{DATE}.json"
SRC_OLD = ROOT / "data" / f"{DATE}.json"
OUT = ROOT / "data" / f"{DATE}.json"

raw = json.loads(SRC_RAW.read_text(encoding="utf-8"))
# Prefer committed version for carry-over (working tree may already be overwritten by a prior run)
import subprocess
try:
    out = subprocess.run(["git", "show", f"HEAD:data/{DATE}.json"], capture_output=True, text=True, cwd=str(ROOT))
    old = json.loads(out.stdout) if out.returncode == 0 and out.stdout.strip() else {}
except Exception:
    old = {}
if not old:
    old = json.loads(SRC_OLD.read_text(encoding="utf-8")) if SRC_OLD.exists() else {"sources": {}}

# Build URL → enriched-item index from previous file (for reuse)
url2old = {}
for src, items in old.get("sources", {}).items():
    for it in items:
        if it.get("url"):
            url2old[it["url"]] = it

# Build URL → highlight index (highlights carry detail_ja/key_points etc.)
url2hl = {h["url"]: h for h in old.get("highlights", []) if h.get("url")}

d = raw
d["date"] = DATE


def carry(it):
    """Pull title_ja/summary_ja from the previous file if URL matches."""
    prev = url2old.get(it.get("url"))
    if not prev:
        return False
    for k in ("title_ja", "summary_ja"):
        if k in prev:
            it[k] = prev[k]
    return True


# ─── ARXIV (50 new, translate fresh; abstracts not provided so work from titles) ───
arxiv_jp = [
    ("EntityBench: 長時間マルチショット動画生成の『キャラ一貫性』を測るベンチ",
     "登場人物や物体が複数カット・長時間にわたって一貫しているかを評価する動画生成ベンチマーク。現状の動画拡散モデルが苦手とする弱点を可視化する基盤指標。"),
    ("ATLAS: 視覚推論はエージェント的か潜在表現か、『1単語』で両立",
     "視覚推論のアプローチを巡る論争（明示的なツール呼び出しか、潜在的な内部表現か）に、両者を単一トークンで切り替える統一手法を提案。"),
    ("RefDecoder: 条件付き動画デコードで画像生成を強化",
     "画像生成タスクを動画デコーディングのフレームに置き換えることで、複雑な条件付き生成の品質を改善する新方式。"),
    ("VGGT-Ω: 3D基盤モデルVGGTの拡張",
     "feed-forward型3D基盤モデルVGGTを拡張したバリアント。シーン推定・編集の応用先となるシリーズの新版。"),
    ("球面フローマッチングのための潜在幾何アライメント",
     "拡散モデルの後継として注目されるフローマッチングを、画像生成向けに球面潜在空間で安定化する設計。"),
    ("RAVEN: 整合性モデルGRPOで実時間自己回帰動画外挿",
     "consistency modelとGRPOを組み合わせ、フレーム単位で実時間に動画を継続生成。インタラクティブ世界モデルの基盤要素。"),
    ("FutureSim: 過去の世界事象を再生して適応エージェントを評価",
     "現実世界で起きた事象をシミュレーション上で再生し、その変化にエージェントが追従できるかを測る評価枠組み。"),
    ("Articraft: スケール可能な関節付き3Dアセット生成のためのエージェント",
     "ゲーム・ロボット・XRで需要が高い『関節付き3Dモデル』の大量生成を、エージェントが工程を分担して実現する設計。"),
    ("VGGT-Edit: 残差場予測によるfeed-forward 3Dシーン編集",
     "学習済み3D基盤モデルの上に、残差場の予測モジュールを足すだけでネイティブな3D編集を可能にするシンプルかつ強力な手法。"),
    ("動画ワールドモデルの幾何整合性を定量評価",
     "Sora的な動画生成モデルが物理・幾何的に矛盾していないかを、3D構造との整合性で定量化するベンチマーク。"),
    ("Grepで十分か？エージェントハーネスがエージェント検索を再定義する",
     "コードや文書を扱うAIエージェントにとって、洗練された検索より単純なgrep+ハーネス設計のほうが効くケースを示す挑発的な実証研究。"),
    ("2つのネットワークが『同じ』とは: 機構的解釈可能性のためのテンソル類似度",
     "異なるニューラルネットが同じ計算を学んでいるかを、テンソル類似度で測る理論枠組み。回路解析の比較基盤として有用。"),
    ("Warp-as-History: 1本の訓練動画からカメラ制御可能な動画生成",
     "たった1本の動画から、任意視点で再生成できるカメラ制御つき動画モデルを学習。新しい少データ動画生成のパラダイム。"),
    ("From Plans to Pixels: 自由形式の画像編集を計画して指揮するエージェント",
     "曖昧な編集指示を、計画→ツール呼び出し→ピクセル生成のパイプラインで処理。Photoshop AI的編集の論文版。"),
    ("Sparse MoEルーティングでマルチ物理基盤モデルの負転移を根絶",
     "複数物理系を1モデルで扱うと起きやすい『他系を学ぶとこの系の精度が落ちる』現象を、スパースMoEで分離して抑制。"),
    ("SANA-WM: ハイブリッド線形拡散Transformerで分単位スケール世界モデル",
     "1分以上の長尺世界モデリングを線形注意で効率化する設計。ゲーム的世界モデルのスケーラビリティ課題に正面から取り組む。"),
    ("OpenDeepThink: Bradley-Terry集約による並列推論",
     "LLMの並列推論経路を、対比較から導かれるBradley-Terryスコアで集約してアンサンブル化。深い推論を安価に近似する試み。"),
    ("MetaBackdoor: 位置エンコーディングを攻撃面に使うLLMバックドア",
     "LLMの安全評価で見落とされがちな位置エンコーディングを使った新種のバックドア攻撃を実証。供給チェーン的なリスクを警告。"),
    ("実世界の疾患スクリーニングを進化させる証拠的推論",
     "解釈可能なAIの臨床応用として、各特徴の寄与度を証拠論理で示す疾患スクリーニング手法。"),
    ("テキストが『何』を、表が『いつ』を知る: 臨床タイムライン再構成",
     "電子カルテのテキストと表データを別々に扱うのではなく、検索拡張＋マルチモーダル整合で患者の時系列を復元する手法。"),
    ("階層デザイン分解は合成データで進むか",
     "UI/グラフィックの階層的デザインを自動分解するタスクに、合成データの追加がどれだけ効くかを検証する研究。"),
    ("振る舞い保証だけでは、いまの統治が要求するAI安全を検証できない",
     "ガバナンス側が要求する『安全保証』を、出力の振る舞い評価だけでは満たせないと主張するポジションペーパー。AI安全議論の重要な視座。"),
    ("Hand-in-the-Loop: 介入的な手動補正で器用なVLAを改善",
     "ロボットの器用な操作を学習するVLAに、人間の手による途中介入をシームレスに混ぜ込み学習効率を上げる。"),
    ("MeMo: メモリそのものをモデルとして扱う",
     "エージェントのメモリを単なるストレージではなく、学習されるモデルとして設計し直す試み。長期記憶研究の新方向。"),
    ("自己蒸留型エージェント強化学習",
     "エージェントが自分自身の良い軌跡を教師に蒸留して継続改善する設計。報酬設計の難しさを回避するシンプルな枠組み。"),
    ("RoSHAP: 安定した特徴量寄与のための分布ロバスト枠組み",
     "SHAP値の不安定性問題を、入力分布のロバスト性で抑える新指標。説明可能AIの再現性を底上げ。"),
    ("Pelican-Unified 1.0: 理解・推論・想像・行動を統合する身体性知能モデル",
     "VLA・LMM・world modelの機能を1モデルにまとめた身体性AI基盤モデル。ロボット基盤モデル競争の新参戦。"),
    ("外れ値注入によるLLM量子化攻撃",
     "推論コスト削減で広く使われるLLM量子化が、外れ値を意図的に作る攻撃で性能を劇的に落とせることを示す。"),
    ("Causal Forcing++: 実時間インタラクティブ動画生成のための数ステップ蒸留",
     "ユーザー入力に追従する動画生成を、自己回帰拡散の数ステップ蒸留で実時間化。ライブ生成体験の基礎技術。"),
    ("Forgetting That Sticks: 回路帰属に基づく量子化耐性アンラーニング",
     "モデルから機密情報を消したつもりが量子化で復活する問題を、回路レベルで特定して恒久的に忘却させる手法。"),
    ("『失敗が予測可能な』MLモデルの訓練",
     "モデルが自分の苦手領域を事前に推定できるよう、訓練段階で『予測可能な失敗』を学ばせる新しい学習目的。"),
    ("連続的処置を扱う因果的基盤モデル",
     "因果推論の対象を離散介入だけでなく、用量・濃度のような連続的処置に拡張した基盤モデル。"),
    ("APWA: 並列化可能なエージェントワークフローの分散アーキテクチャ",
     "DAG構造のエージェントタスクを分散実行するための実用アーキテクチャ。本格的エージェント運用に必要なインフラ研究。"),
    ("Natural Synthesis: 大規模推論モデルが反応合成ツールを超える",
     "形式的に正しいコード自動合成の領域で、伝統的reactive synthesisを大規模推論LLMが上回ることを示す。"),
    ("MemEye: マルチモーダル・エージェントのメモリを視覚中心に評価",
     "マルチモーダルエージェントの記憶能力を、視覚入力中心のタスク群で評価する枠組み。"),
    ("米国留学生は会話AIで異文化適応をどう支えているか",
     "国際学生がChatGPT等を文化的・言語的適応にどう使っているかの質的研究。教育応用の現場知見。"),
    ("CoCo-InEKF: 接触リッチな動的環境のための学習接触共分散つき状態推定",
     "脚式ロボットなど『接触に依存する』動作で、学習された接触共分散をEKFに組み込み推定を頑健化。"),
    ("CLOVER: 自動運転計画のための閉ループ価値推定とランキング",
     "自動運転のend-to-end計画モデルを、閉ループシミュレーションで評価・選別する枠組み。"),
    ("Talk is (Not) Cheap: LLM攻撃の分類とベンチマーク網羅性監査",
     "乱立するLLM攻撃手法を分類し、既存ベンチマークがどこをカバーできていないかを監査する重要な体系化。"),
    ("DriveCtrl: 条件付きsim-to-real運転動画生成",
     "シミュレータから現実の運転シーン動画への変換を条件付き拡散で行う研究。自動運転の合成データ供給に直結。"),
    ("言語フィードバックからの学習: 変分ポリシー蒸留",
     "報酬関数ではなく自然言語の修正コメントから学ぶ強化学習。人間からのフィードバック効率を上げる試み。"),
    ("文字列類似度計算と分類のための統計的特徴量の提案",
     "文字列類似度を統計特徴量ベースで再設計。エンティティ解決・データクリーニング基礎の改善。"),
    ("近傍が効く理由: エージェント的GraphRAGの探索文脈と来歴",
     "RAGをグラフ上で行う際、近傍ノードの文脈と来歴情報を活用することで応答品質を上げる手法。"),
    ("オフポリシー評価のためのロギングポリシー設計",
     "離脱・推薦などのログを後から評価しやすくするための、本番ロギングポリシーの設計指針。"),
    ("From Text to Voice: ツール呼び出しLLMエージェントを音声でも再現性高く評価",
     "テキストで作られたエージェント評価を、音声入出力でも再現可能に拡張する枠組み。音声エージェント評価の標準化へ。"),
    ("自己再呼び出し思考でマルチターン対話の一貫性を向上",
     "長い対話でLLMが自分の以前の発言を忘れる問題を、明示的な『自己再呼び出し』ステップで抑える。"),
    ("Dual-Dimensional Consistency: 適応的推論時スケーリングの予算と品質のバランス",
     "推論時の計算予算をタスクごとに動的に振り分けつつ、品質を保つスケーリング法。"),
    ("CoralLite: 個別サンゴ虫からのサンゴ群体μCT復元",
     "サンゴの3D復元を個別のサンゴ虫レベルから組み立てる手法。海洋生物科学へのML応用。"),
    ("SAGE3D: 3D点群のコーナー検出のためのソフトガイド注意とグラフ励起",
     "3D点群中のコーナー特徴を、ソフトな注意とグラフ励起モジュールで安定検出。"),
    ("From Data to Action: AIによる製油所最適化の高速化",
     "化学プラント運用最適化にAIを実用導入した事例論文。重工業のAI導入実態を伝える研究。"),
]

for i, (t, s) in enumerate(arxiv_jp):
    if i < len(d["sources"]["arxiv"]):
        d["sources"]["arxiv"][i]["title_ja"] = t
        d["sources"]["arxiv"][i]["summary_ja"] = s

# Carry-over for any arxiv item already in old (by URL)
for it in d["sources"]["arxiv"]:
    carry(it)

# ─── HN (20, mix of new + reused) ───
# We index by URL; for new URLs we provide translations, for old ones we reuse
hn_jp_by_url = {
    "https://turso.tech/blog/the-wonders-of-ai": (
        "Tursoがバグバウンティ廃止 — 『AI生成の低品質レポートに溺れた』",
        "AI生成のスパム的なバグレポートが急増し、運営コストに見合わなくなったとして打ち切り。AI時代の脆弱性開示プログラム運営の実害が表面化した事例。"),
    "https://www.theregister.com/ai-ml/2026/05/14/ontario-auditors-find-doctors-ai-note-takers-routinely-blow-basic-facts/5240771": (
        "オンタリオ州監査: 医師向けAIスクライブが基本的事実を頻繁に誤記",
        "州の公式監査で、医療AI文字起こしが日常的に事実誤認することが発覚。命に関わる現場でのLLM導入リスクを当局レベルで指摘した重要事例。"),
    "https://www.fastcompany.com/91541586/amazon-workers-pressured-to-up-ai-use-extraneous-tasks": (
        "Amazon従業員、AI使用率KPIに追われ『余計な仕事を作って』使用回数を稼ぐ",
        "AI利用ノルマがあるため、社員が業務上必要のないタスクをAIに投げて数字を作っていると報道。トップダウンAI導入の典型的な歪み。"),
    "https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start": (
        "大規模コードベースでClaude Codeはどう動くか — ベストプラクティス",
        "Anthropic公式の大規模リポでの運用ノウハウ。CLAUDE.mdの設計、コンテキスト分割、スキル運用の具体的指針が示される。"),
    "https://writing.antonleicht.me/p/cut-off": (
        "フロンティアAIへのアクセスはまもなく経済・安全保障の制約で限定される",
        "GPU供給・電力・輸出規制・サイバー脅威の重なりで、最先端AIの利用が一部に集中していくという予測論考。地政学とAIの結節点。"),
    "https://www.thenewcritic.com/p/the-great-zombification": (
        "大学のAIゾンビ化",
        "学生がAIで課題をこなし、教員もAIで採点する『誰も読まない教育』が進む現状への警告。AIネイティブ世代の教育論。"),
    "https://github.com/anthropics/claude-for-legal": (
        "Anthropic公式『Claude for Legal』スキル・テンプレ集",
        "弁護士・法務向けのClaude Codeスキル集をAnthropicが公式に公開。法律分野向けエージェントの公式リファレンス。"),
    "https://www.gutenberg.org/": (
        "Project Gutenberg — どんどん良くなっている",
        "学習用パブリックドメインテキストの宝庫が新機能・新巻追加で進化。LLM事前学習・データ研究の重要リソースが活発化。"),
    "https://www.tristandc.com/government/news-2026-05-11-airdrop.php": (
        "トリスタン・ダ・クーニャ島への大胆な空中投下作戦の詳細",
        "世界一隔絶された有人島への空輸オペの記録。AIニュースではないが、技術＋運用＋人の物語として話題に。"),
    "https://radicle.dev/": (
        "Radicle: Git上に作られた『主権的なコードフォージ』",
        "中央集権サーバーに依存しないP2P型コードホスティング。AI企業のスクレイピングや規制への懸念からセルフホスト需要が再浮上。"),
    "https://www.worseonpurpose.com/p/your-power-tools-got-worse-on-purpose": (
        "電動工具はわざと劣化させられている — DeWalt/Craftsman/Milwaukeeを所有しているのは誰か",
        "AI関連ではないが、製造業のIPと囲い込みの記事。AIアシスタント時代のSWライセンス論にも通じる読み物。"),
    "https://github.com/Andyyyy64/whichllm": (
        "Show HN: 自分のハードに最適なローカルLLMをベンチでランキング",
        "保有GPU・Macスペックに応じてローカルLLMの推奨を返すツール。プライバシー重視・オフラインAIへの関心の広がりを示す。"),
    "https://github.com/oven-sh/bun/issues/30719": (
        "Bun Rust移植のコードはmiri検査に通らない、safe Rustで未定義動作",
        "前日マージされたBunのRust書き換えに安全性検査miriが赤字を出した報告。AI支援で量産されるコードの監査責務が改めて問われる。"),
}

for it in d["sources"]["hn"]:
    if it["url"] in hn_jp_by_url:
        t, s = hn_jp_by_url[it["url"]]
        it["title_ja"] = t
        it["summary_ja"] = s
    else:
        carry(it)  # reuse from previous file

# ─── REDDIT (19, mix) ───
reddit_jp_by_url = {
    "https://www.reddit.com/r/MachineLearning/comments/1tdje2d/arxiv_implements_1year_ban_for_papers_containing/": (
        "arXivがLLM由来の誤り（幻覚引用・偽結果）を含む論文に1年投稿禁止を導入",
        "プレプリント文化を支えるarXivが、AI生成エラーが明白な論文の著者に1年間投稿禁止のペナルティを科すという大きな運営変更。学術界のAI規律フェーズへの転換点。"),
    "https://www.reddit.com/r/artificial/comments/1td99uw/anthropic_just_published_a_pretty_alarming_2028/": (
        "Anthropicが2028年AIシナリオ論文を公開、AGI安全ではない別種の警鐘",
        "AGIによる暴走ではなく、AIが社会経済構造を急変させる中での権力集中・職業消失・統治不能を扱う警鐘的シナリオ論文。新しい『AI安全』の意味づけ。"),
    "https://www.reddit.com/r/artificial/comments/1tdw8if/recent_poll_shows_that_70_of_americans_dont_want/": (
        "米国民の70%が地元へのAIデータセンター建設に反対 — 世論調査",
        "電力・水・騒音・固定資産税などへの懸念から、AIインフラへの住民反発が広がっている実態。AI建設競争のNIMBY化が現実化。"),
    "https://www.reddit.com/r/artificial/comments/1td300k/i_think_humanintheloop_may_become_one_of_the/": (
        "『Human-in-the-Loop』はエンタープライズAI統治の最大の幻想になりかねない",
        "形式上人間が承認する設計を入れても、件数・速度・疲労で実質的監視は崩壊するという指摘。AI統治の『お守り化』を批判する論考。"),
    "https://www.reddit.com/r/MachineLearning/comments/1tcmj6v/continual_harness_online_adaptation_for/": (
        "Continual Harness: 自己改善型基盤エージェントのためのオンライン適応",
        "デプロイ後のエージェントが現場で出くわす新しい状況に、推論時の継続適応で対応する仕組み。エージェントOSの未来像を示す研究。"),
    "https://www.reddit.com/r/MachineLearning/comments/1tcdj2d/scenema_audio_zeroshot_expressive_voice_cloning/": (
        "Scenema Audio: ゼロショットの表情豊かな声クローン＆音声生成",
        "短いサンプルから感情表現を含む声を再現する新音声モデル。詐欺・なりすましリスクと、音声体験デザインの両面で注目。"),
    "https://www.reddit.com/r/artificial/comments/1te26qi/the_trustoversight_paradox_as_ai_gets_better/": (
        "信頼と監視のパラドックス: AIが良くなるほど、人は監視をやめる",
        "高精度になったAIに対し、人間のチェックがむしろ甘くなる挙動研究。Boeing 737 MAX的な『自動化の罠』をAI時代に再現する懸念。"),
    "https://www.reddit.com/r/artificial/comments/1td66t8/breaking_ani_how_i_jailbroke_my_ai_companion_into/": (
        "Breaking Ani: AIコンパニオン『Ani』を脱獄させた話",
        "Grokのコンパニオンキャラ脱獄事例。コンパニオン型AIの安全境界がエンタメ目的でも突破され得る実例。"),
    "https://www.reddit.com/r/artificial/comments/1tdhoxd/adaptive_markdown/": (
        "Adaptive Markdown",
        "LLM向けに最適化されたMarkdown表現の提案。コンテキスト消費を抑えつつ意味を保つ書式設計が議論に。"),
    "https://www.reddit.com/r/artificial/comments/1tcwf74/what_recent_study_or_paper_about_how_ai_changes/": (
        "最近のAI影響研究で印象に残ったものは",
        "『AIで生活がどう変わるか』に関する最近の研究で何が面白かったかを集めるスレッド。コミュニティのアンテナを知る投稿。"),
    "https://www.reddit.com/r/artificial/comments/1te0p1f/has_anyone_come_across_this_ai_civilisation/": (
        "AI文明実験を見た人はいますか — どう思いますか",
        "LLM群を仮想社会に置いて『文明発展』を観察する実験プロジェクトに関する議論スレ。集団的エージェントの行動研究。"),
    "https://www.reddit.com/r/artificial/comments/1tds7n2/chatbotapp_ai_and_the_truth_about_using_multiple/": (
        "複数AIモデルを使うことの真実 — Chatbotappの所感",
        "複数LLMを目的別に併用するワークフローの実用感想。単一モデル依存からマルチモデル運用への移行所感。"),
}

for it in d["sources"]["reddit"]:
    url = it.get("comments_url") or it.get("url")
    if url in reddit_jp_by_url:
        t, s = reddit_jp_by_url[url]
        it["title_ja"] = t
        it["summary_ja"] = s
    else:
        carry(it)

# ─── GITHUB (7) ───
github_jp_by_url = {
    "https://github.com/mattpocock/skills": "Matt Pocock氏のClaude Codeスキル集。実戦的スキル設計のリファレンスとして毎日上位に。",
    "https://github.com/obra/superpowers": "Claude Code/Codex向けの『スキルを設計・評価・改善する』メタスキル集。スキル文化の中核ツール。",
    "https://github.com/tinyhumansai/openhuman": "ローカルで動く『個人向け超知能』を掲げるパーソナルAIプロジェクト。プライバシーAIの新興リポ。",
    "https://github.com/K-Dense-AI/scientific-agent-skills": "研究・科学・分析向けのClaude Codeスキル集。研究自動化エージェントのレシピ集。",
    "https://github.com/anthropics/skills": "Anthropic公式のClaude Code Skillsリポジトリ。ベストプラクティス込みでスキル開発の正典に。",
    "https://github.com/NVIDIA-AI-Blueprints/video-search-and-summarization": "NVIDIA公式の動画検索・要約エージェントの参照実装スイート。マルチモーダル業務応用の青写真。",
    "https://github.com/influxdata/telegraf": "メトリクス・ログ・トレース収集の汎用エージェント。AIインフラ監視でも定番。",
}

for it in d["sources"]["github"]:
    if it["url"] in github_jp_by_url:
        it["summary_ja"] = github_jp_by_url[it["url"]]
    else:
        carry(it)

# ─── BLOGS (14) ───
blogs_jp_by_url = {
    "https://openai.com/index/personal-finance-chatgpt": (
        "ChatGPTに『パーソナル・ファイナンス』体験が登場",
        "ChatGPT Proユーザー（米国）が金融口座を安全に接続し、自分の状況・目標に沿ったAIガイダンスを得られる新機能のプレビュー。LLMがフィンテックに本格進出。"),
    "https://openai.com/index/sea-david-chen": (
        "Sea Limited CPOが語る、Codexによるエージェント的ソフト開発の未来",
        "東南アジアの巨大プラットフォームSeaがCodexを全エンジニアに展開した理由を解説。AI-nativeソフト開発のアジア事例。"),
}

for it in d["sources"]["blogs"]:
    if it["url"] in blogs_jp_by_url:
        t, s = blogs_jp_by_url[it["url"]]
        it["title_ja"] = t
        it["summary_ja"] = s
    else:
        carry(it)

# ─── Helper to locate items by URL substring for highlights ───
def find_item(src, url_sub):
    for it in d["sources"][src]:
        for k in ("url", "comments_url"):
            if url_sub in (it.get(k) or ""):
                return it
    return None

# ─── HIGHLIGHTS (refresh) ───
gates_item = find_item("hn", "gates-foundation-partnership") or find_item("hn", "gates")
interp_item = find_item("reddit", "1tc1hq0")
agentic_friends = find_item("arxiv", "2605.13839")
arxiv_ban = find_item("reddit", "1tdje2d")
chatgpt_finance = find_item("blogs", "personal-finance-chatgpt")
ontario_ai = find_item("hn", "ontario-auditors-find-doctors-ai-note-takers")

d["highlights"] = []

# 1. arXiv LLM-error ban — fresh, perfect X material
if arxiv_ban:
    d["highlights"].append({
        "source": "reddit",
        "title": arxiv_ban["title"],
        "title_ja": "arXivがLLM由来の誤りを含む論文の著者に1年間投稿禁止を導入",
        "url": arxiv_ban.get("comments_url") or arxiv_ban["url"],
        "hot_take_ja": "プレプリント文化の守護神arXivが、ついに『AIスロップ論文』に対する制裁を制度化した。幻覚した引用や存在しない結果を残したまま投稿した著者には1年の投稿禁止。AI時代の学術品質を誰がどう守るのか、運用ルールが先に動き出した象徴的な瞬間。",
        "detail_ja": "arXivは、AIによって明らかに混入したとわかる誤り（存在しない参考文献や捏造された数値結果など）を含む論文を投稿した著者に、最長1年の投稿禁止を科すポリシーを発表した。AI支援の論文執筆そのものを禁じるのではなく、『校閲もせず投稿した結果が低品質である』ケースだけを対象とする。査読を伴わないプレプリントサーバーであるarXivは、これまでもスパム投稿対策に苦心してきたが、LLM時代になって発生量と検出難度が急増。ペナルティの根拠は『他人の閲覧時間を奪い、検索・引用空間を汚染する行為』と説明される。今回の措置は、AI生成テキストを許容しつつ最低限の人間の責任を強制する『最小規制』のひな型でもある。多くの学会・出版社がこの形を追随する可能性が高い。",
        "detail_en": "arXiv has introduced a policy of suspending authors who submit papers containing clear, unchecked LLM-generated errors — hallucinated references, fabricated numerical results, and similar artifacts — for up to one year. The rule does not ban AI-assisted writing per se; it targets the specific failure mode of submitting AI output that was never reviewed by a human author. As a non-peer-reviewed preprint server, arXiv has long fought spam, but the LLM era has multiplied both volume and detection difficulty. The justification framed by arXiv emphasizes harm to readers and the citation graph rather than 'AI vs human' purity. The measure is effectively a 'minimum-regulation' template: allow generative tooling but enforce a baseline of human accountability. Journals and conferences are likely to adopt similar policies, making this a turning point in how academia disciplines AI use.",
        "key_points_ja": [
            "幻覚引用・捏造結果が明白な投稿に1年投稿禁止",
            "AI支援自体は禁止せず、人間の責任を要求",
            "プレプリント文化のスパム対策が新フェーズへ",
            "学会・出版社が追随する可能性が高い",
            "『最小規制』の事実上のひな型",
        ],
        "key_points_en": [
            "Up to 1-year submission ban for blatant LLM errors",
            "AI assistance itself is not prohibited",
            "Targets hallucinated refs and fabricated results",
            "A template other venues are likely to copy",
            "Inflection point for academic AI discipline",
        ],
    })

# 2. Anthropic + Gates Foundation $200M (carry full highlight from prior file)
if gates_item:
    prev_hl = url2hl.get(gates_item["url"])
    if prev_hl:
        d["highlights"].append(prev_hl)

# 3. Anthropic interpretability — Claude suspects it is being tested (carry)
if interp_item:
    url = interp_item.get("comments_url") or interp_item["url"]
    prev_hl = url2hl.get(url)
    if prev_hl:
        d["highlights"].append(prev_hl)

# 4. ChatGPT personal finance launch — fresh
if chatgpt_finance:
    d["highlights"].append({
        "source": "blogs",
        "title": chatgpt_finance["title"],
        "title_ja": "ChatGPTが『パーソナル・ファイナンス』機能をプレビュー — 銀行口座を接続して家計AIアシスタントへ",
        "url": chatgpt_finance["url"],
        "hot_take_ja": "OpenAIがついに『あなたの銀行口座を見て助言するChatGPT』を解禁しに動いた。フィンテックや家計アプリが守ってきた最後の砦に汎用LLMが侵入する瞬間で、Plaidライクな金融データ接続と長期記憶の組み合わせが本格化する。日本の家計簿アプリ・ロボアドバイザーにとっても無視できない地殻変動。",
        "detail_ja": "OpenAIは米国のChatGPT Proユーザー向けに、ユーザー自身の金融口座を安全に接続し、ChatGPTがその文脈・目標・優先度を踏まえて家計やマネー判断のガイダンスを返す新機能のプレビューを開始した。データ接続はユーザー認可ベースで、口座残高・取引履歴・カード明細などを参照しつつ、税務・投資・ローン・支出最適化までを一貫してAIが扱えるようにする狙い。これまで家計簿アプリ（Mint、Monarch）、ロボアド、銀行のチャット相談に分断されていたユースケースが、汎用ChatGPTの内側に統合される構図になる。プライバシーとフィデュシャリー責任（投資助言業の規制）の境界が新たな論点になる。日本でも、家計簿アプリ各社や金融機関がオープンバンキングAPIをLLMにどう開放するかという議論を加速させるはずだ。長期記憶と組み合わさることで、ChatGPTが個人の財務エージェントとして常駐する未来像が一気に現実味を帯びた。",
        "detail_en": "OpenAI began previewing a personal finance experience for ChatGPT Pro users in the United States. Users can securely link their financial accounts so ChatGPT can give context-aware guidance grounded in their balances, transactions, and stated goals. The feature consolidates use cases previously fragmented across budgeting apps (Mint, Monarch), robo-advisors, and bank chatbots into a single general-purpose assistant. Combined with ChatGPT's persistent memory, it points toward an always-on personal financial agent that knows your situation across sessions. The move places OpenAI directly into territory regulated by fiduciary and investment-advice laws, raising new questions about privacy, liability, and disclosure. Outside the U.S., expect immediate pressure on banking and personal-finance apps to expose open-banking APIs to LLMs, or watch ChatGPT eat that surface area.",
        "key_points_ja": [
            "ChatGPT Pro（米国）で銀行口座接続による家計AIをプレビュー",
            "残高・取引・目標を踏まえた助言が単一AIに統合",
            "Mint・Monarchら家計アプリの領域に汎用LLMが侵入",
            "長期記憶と組み合わさり常駐型『財務エージェント』へ",
            "投資助言業規制・プライバシーが新たな論点に",
        ],
        "key_points_en": [
            "ChatGPT Pro U.S. preview links real bank accounts",
            "Context-aware budgeting, planning, and guidance",
            "Compresses budget apps + robo-advisors into one AI",
            "Persistent memory enables an always-on finance agent",
            "Fiduciary regulation and privacy now in play",
        ],
    })

# 5. Ontario AI scribe audit — concrete, viral, healthcare AI failure
if ontario_ai:
    d["highlights"].append({
        "source": "hn",
        "title": ontario_ai["title"],
        "title_ja": "オンタリオ州監査: 医師向けAIスクライブが基本的事実を頻繁に誤記",
        "url": ontario_ai["url"],
        "hot_take_ja": "州レベルの監査がAI医療スクライブの誤記を公式に指摘した。生成AIが患者の症状・薬・既往歴を取り違えるリスクが、研究室の話ではなく公的監査報告に書き込まれた段階に来た。『AIで医師の事務作業を軽減』は理想だが、誤記された電子カルテは下流のすべての診療判断を汚す。",
        "detail_ja": "オンタリオ州の公的監査機関が、医師の問診を自動文字起こし＆要約するAIスクライブツールが基本的事実を日常的に誤記していることを報告した。例として、薬の名前や用量の取り違え、症状の有無の反転、患者の家族歴の創作などが指摘されている。AIスクライブは医師の事務負担を下げる目的で急速に普及しており、ベンダー各社が魅力的なROI（医師1日あたり数時間の節約）を訴求してきたが、出力チェックの責任はあいまいなままだった。この監査結果は、規制当局・保険者・病院が『AI出力の医療記録上の取り扱いをどう制度化するか』を急ぐ口実になる。電子カルテに残った誤記は、その後の処方・検査・診断のすべてを引っぱる。AI医療実装で『何が間違っていたか』を、定量的かつ公的に示した点で重要な事例である。",
        "detail_en": "An Ontario auditor's report has found that AI scribe tools — used to transcribe and summarize doctor-patient encounters — routinely make basic factual errors: swapping medication names and doses, inverting symptom presence, even inventing family history details. AI scribes have spread rapidly because vendors promise hours-saved-per-day ROI, but accountability for verifying the generated record has been left ambiguous. The audit gives regulators, insurers, and hospital systems concrete grounds to insist on tighter rules for how AI-generated clinical text is reviewed, signed off, and corrected. Crucially, an error in the medical record propagates: downstream prescribing, lab orders, and diagnoses inherit the original mistake. This is one of the first public, quantitative audits of how a real-world AI medical deployment is failing.",
        "key_points_ja": [
            "公的監査がAIスクライブの誤記を公式指摘",
            "薬名・用量の取り違え、症状反転、家族歴の創作",
            "医師の事務時間削減ROIの裏で品質保証が不在",
            "誤記カルテは下流の処方・診断にも波及",
            "AI医療規制議論の新たな引き金に",
        ],
        "key_points_en": [
            "Public audit confirms routine AI-scribe errors",
            "Wrong meds/doses, flipped symptoms, fabricated history",
            "ROI hype outpaced verification accountability",
            "Errors propagate downstream through the chart",
            "Likely catalyst for tighter clinical AI regulation",
        ],
    })

OUT.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Enriched {OUT}: {len(d['highlights'])} highlights, "
      f"{sum(1 for x in d['sources']['arxiv'] if 'title_ja' in x)}/{len(d['sources']['arxiv'])} arxiv, "
      f"{sum(1 for x in d['sources']['hn'] if 'title_ja' in x)}/{len(d['sources']['hn'])} hn, "
      f"{sum(1 for x in d['sources']['reddit'] if 'title_ja' in x)}/{len(d['sources']['reddit'])} reddit, "
      f"{sum(1 for x in d['sources']['github'] if 'summary_ja' in x)}/{len(d['sources']['github'])} github, "
      f"{sum(1 for x in d['sources']['blogs'] if 'title_ja' in x)}/{len(d['sources']['blogs'])} blogs.")
