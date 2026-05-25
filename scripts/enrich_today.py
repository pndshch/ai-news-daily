#!/usr/bin/env python3
"""Enrich raw-2026-05-25.json with Japanese summaries and highlights."""
import json
from pathlib import Path

DATE = "2026-05-25"
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / f"raw-{DATE}.json"
OUT = ROOT / "data" / f"{DATE}.json"

with open(RAW) as f:
    d = json.load(f)

# -------- arXiv --------
arxiv_map = {
    "2605.23904v1": (
        "SkillOpt：自己進化エージェントスキルの『執行戦略』",
        "凍結したエージェントの『外部状態』としてスキルそのものを学習対象として最適化する初の体系的フレームワーク。手書き／一発生成／緩い自己改稿といった既存手法と異なり、再現可能な勾配最適化のような規律でスキルを改善することを目指す。"
    ),
    "2605.23903v1": (
        "Geo-Align：メトリック幾何を報酬にして動画生成をアライン",
        "カメラ制御動画生成の汎化を改善する手法。合成データでのSFTに依存せず、現実世界での幾何整合性を報酬として用いることで、out-of-distributionな実写でも物理スケールとカメラ挙動を保つ。"
    ),
    "2605.23902v1": (
        "PiD：ピクセル拡散による高速・高解像ラテントデコーディング",
        "潜在拡散モデルのlatent→pixelデコーダを、再構成志向のVAEから拡散ベースに置き換える提案。メガピクセル級でも質を保ちつつ高速化、生成パイプラインのボトルネック解消を狙う。"
    ),
    "2605.23901v1": (
        "LLMをShannon的『ノイジーチャネル』として捉え直すスケーリング則",
        "従来の単調パワーローでは説明できないカタストロフィックなオーバートレーニング・量子化劣化を、Shannon-Hartley定理ベースの新スケーリング則で統一的に説明。モデルパラメータをチャネル帯域に対応付ける枠組み。"
    ),
    "2605.23899v1": (
        "モデル生成エージェントスキルを体系的に解剖",
        "言語エージェントが再利用するための『スキル』を、どう抽出・どう編成・どう使うべきかを横断的に評価。ドメインレベル・モデル生成スキルの強み・弱みを統一指標で初めて整理。"
    ),
    "2605.23898v1": (
        "SPACENUM：VLMの空間数値理解を本気で検証",
        "VLMが出すアクション量や座標などの数値出力が、本当に空間知覚に根ざしているのかを評価する統一フレームワーク。表面的に『数値が出る』だけのVLMの限界を可視化。"
    ),
    "2605.23897v1": (
        "ETCHR：画像を編集して推論を明確化するMLLM",
        "純テキストの思考連鎖だけでは細部や視点変換に弱いMLLMに対し、専用画像編集モデルと理解モデルを分離する設計。固定ツールキットや雑なマルチモーダル中間画像の問題を回避。"
    ),
    "2605.23895v1": (
        "活性から因果へ——ヒト脳の因果的視覚表現の発見",
        "fMRI×AIで、ある視覚概念を『本当に表現している』脳領域を、単なる強い活性ではなく因果的介入で特定する手法。神経科学とAI解釈性研究の橋渡し。"
    ),
    "2605.23893v1": (
        "Complete-muE：MoEモデルでも効くハイパーパラメータ転移",
        "μPやSDEではカバーしきれなかった、Denseから/MoE間でのハイパーパラメータ転移をtwo-bridge設計で実現。MoE時代のスケーリング実験コストを大幅に下げる枠組み。"
    ),
    "2605.23892v1": (
        "Visual Geometry Transformerのトークン選別ガイド",
        "多視点3D再構成向けTransformerの自己注意コストを抑えるため、KVトークンを賢く選別する一般戦略を提案。シンプルだが汎用的に効く。"
    ),
    "2605.23891v1": (
        "Smart-Insertion-V：参照スタイルの差を吸収する動画オブジェクト挿入",
        "ソース動画と参照画像のスタイル差が大きい場合でも自然に統合する、デュアルストリーム×閉ループ動画挿入フレームワーク。動画挿入とスタイル転送を同時実行。"
    ),
    "2605.23889v1": (
        "HorizonStream：ストリーミング3D再構成のための長時間アテンション",
        "オンライン3D再構成のドリフト・ジッタを、時間スケールが異質な手がかりを統合する長尺アテンション設計で抑制。因果＆有限メモリ制約の下で安定。"
    ),
    "2605.23888v1": (
        "GenRecon：生成的3D事前分布を多視点再構成に橋渡し",
        "多視点RGBから高品質3Dシーンを得るために、強力な生成3D事前モデル（Trellis.2等）の条件付き生成として再構成を定式化。大規模シーンでもtile型に拡張可能。"
    ),
    "2605.23887v1": (
        "CHRONOS：進化するデータマーケット向け時系列対応マルチエージェント",
        "時系列ナレッジグラフのデータ市場で、(1)古びる索引、(2)分布変化後のShapleyの誤帰属、(3)DPバジェットの過消費を同時に解決する3層アーキテクチャ。"
    ),
    "2605.23885v1": (
        "低リソース言語への知識転移を語彙介入で",
        "低リソース言語向けLLMで必要な科学・常識・世界知識を、軽量な語彙レベル介入で高リソース言語から転移する手法。重い再学習を要さず実用的。"
    ),
    "2605.23883v1": (
        "PGT：手続き生成タスクでMLLMの視覚グラウンディングを改善",
        "幾何プリミティブを画像に重ねるシンプルな手続き生成タスクで、MLLMのfine-grained視覚理解を強化しつつ、知覚失敗の原因を診断する低コスト道具にも転用。"
    ),
    "2605.23879v1": (
        "球面Hellinger-Kantorovichフローの安定性と差分プライバシー",
        "輸送と反応を結合するSHK勾配流の摂動論を構築。Gibbs分布サンプリングの理論基盤を差分プライバシー実装に応用するための一歩。"
    ),
    "2605.23878v1": (
        "LaMo：自己教師あり潜在運動事前で動画生成に物理らしさを",
        "外部シミュレータや教師モデルに頼らず、未ラベル動画から運動の手がかりを抽出して動画拡散モデルに事前分布として与える自己教師あり手法。"
    ),
    "2605.23872v1": (
        "学習不要なループ型Transformer",
        "事前学習済みTransformerの中間ブロックを推論時にループさせる軽量ラッパで、再学習なしに再帰計算を導入。素朴な実装より工夫が必要だが効果あり。"
    ),
    "2605.23871v1": (
        "Muonオプティマイザを確率測度上のハミルトン勾配流として捉え直す",
        "正則化Muonの直交化マップが核ノルムの平滑Fenchel双対の勾配であることを示し、Muon更新を鏡像／近接ステップとして再解釈。理論的に整理。"
    ),
    "2605.23868v1": (
        "Vision Transformerには『より良いトークン相互作用』が必要",
        "ViTの密予測性能が長く訓練するほど劣化する現象を『意味的拡散』として特徴付け、原因の単純化（高ノルムアーティファクト説）に異議。改善の方向性を示す。"
    ),
    "2605.23867v1": (
        "LLMの説得的・物語的説明が人間の判断に与える影響",
        "LLMが生成する物語的な説明は理解されやすく説得力もある一方、判断の客観的正しさを必ずしも向上させない。説明の語り口バイアスを実験的に評価。"
    ),
    "2605.23863v1": (
        "ロバストビジョン×Sim-to-Real DRLで自動イチゴ収穫",
        "高解像分岐＋セグ注意＋エッジ教師付きYOLO26-segと、シミュ訓練DRL制御を組み合わせた閉ループのロボットイチゴ収穫システム。"
    ),
    "2605.23861v1": (
        "基盤モデルを使った因果生成モデリング",
        "事前学習基盤モデルのゼロショット推論力を、因果生成モデル構築に体系的に取り込むモジュラ枠組みFM-CGM。視覚因果推論を一気通貫で。"
    ),
    "2605.23857v1": (
        "事前学習での蒸留に強い教師は本当に必要か",
        "事前学習段階での蒸留において、教師→生徒の強弱関係を体系的に検証。適切な混合があれば、教師は必ずしも『より強い』必要はない、という反直観的結果。"
    ),
}

for it in d["sources"]["arxiv"]:
    aid = it.get("id") or ""
    if aid in arxiv_map:
        t, s = arxiv_map[aid]
        it["title_ja"] = t
        it["summary_ja"] = s

# -------- HN --------
hn_map = {
    "48256953": (
        "DeepSeek Reasonix：高キャッシュ・低コストの純正コーディングエージェント",
        "DeepSeekが純正コーディングエージェント『Reasonix』を発表。プロンプトキャッシュの徹底活用と超低コスト推論を売りに、Claude Code/Codex対抗のエージェント直接競争へ。"
    ),
    "48263238": (
        "Eternal Sloptember——geohotによるAI洪水時代の警句",
        "George Hotz(geohot)が、AI生成スロップに埋め尽くされる現代のウェブを『永遠のSeptember』になぞらえて批判。"
    ),
    "48258684": (
        "AIチップのコスト、約2/3がメモリへ",
        "Epoch AIの分析で、AIアクセラレータの部品コストに占めるメモリ（HBM等）比率が約2/3に到達。GPUダイ本体よりHBM寡占の構造リスクが鮮明に。"
    ),
    "48266485": (
        "教皇レオ14世『AIは少数の権力者ではなく人類に奉仕すべき』——初の回勅",
        "教皇レオ14世が就任後初の回勅でAIに言及。『不透明なAIが少数の企業に握られることは新たな非人間化のリスク』だと警鐘。カトリック世界からの強い倫理的シグナル。"
    ),
    "48256912": (
        "Constraint Decay：LLMエージェントはバックエンドコードで『制約を忘れる』",
        "arXiv論文。LLMエージェントが長尺・多ファイル・多ターンのバックエンド生成で、初期制約をターン進行とともに忘却・違反していく現象を定量化。"
    ),
    "48259784": (
        "『Claudeはアーキテクトではない』——役割を分離せよ",
        "Claude Codeに『設計判断』までさせると、辻褄合わせのコードが量産されアーキテクチャが壊れるという現場ブログ。LLMには『実装』、設計判断は人間が握れと主張。"
    ),
    "48266906": (
        "オランダ警察、Botnet運用サーバ800台押収・2名逮捕",
        "サイバー攻撃支援に使われていたサーバ800台をオランダ警察が押収、2名を逮捕。大規模ボットネット解体作戦の最新事例。"
    ),
    "48257410": (
        "DeepSeek、フラッグシップAIを75%恒久値下げへ",
        "BloombergによるとDeepSeekは旗艦モデルを期間限定ではなく恒久的に75%値下げ。米中フロンティアの価格競争がさらに加速。"
    ),
    "48257980": (
        "『AIウォッシング』——PR会社がこぞって『AI企業』にリブランド",
        "ガーディアン報道。本質的にAIをほとんど使っていないPR・コンサル各社が、社名やパッケージを『AI〜』に改名する動きが加速。ドットコム前夜と酷似。"
    ),
    "48259861": (
        "Jujutsuで『Git厳格疲れ』を克服する",
        "Gitの厳しさで疲弊した開発者向けに、Jujutsu(jj)による軽量で寛容なバージョン管理ワークフローを紹介するブログ。"
    ),
    "48268871": (
        "Uber COO『AIトークン消費の正当化が日に日に難しくなっている』",
        "UberのCOOがAIエージェントによる『tokenmaxxing』の経済合理性に疑問を呈す発言。エンタープライズ側からAI支出の効果検証圧力が強まる兆候。"
    ),
    "48266435": (
        "教皇レオ『少数企業の不透明AIは新しい非人間化を生む』",
        "カトリック教会トップがAI集中の倫理的危険を回勅で明示。AIガバナンス議論に宗教的・道徳的アクセントを加える。"
    ),
    "48256565": (
        "Apple PICo：実用的な学習型画像圧縮で本当に効くものを整理",
        "AppleのML研究『PICo』。学習ベース画像コーデックを、知覚品質・速度・ハードウェア親和性の観点から再整理。"
    ),
    "48267126": (
        "C拡張・ポータビリティ・代替コンパイラ事情",
        "C言語の独自拡張・他コンパイラ移植・標準準拠の現状を整理した記事。"
    ),
    "48257058": (
        "Microsoft 6502 BASIC、ついにオープンソース化",
        "Apple II・Commodore・Atari等に搭載されたMS製の歴史的6502 BASICインタプリタが公式OSS化。レトロ計算史にとっての大ニュース。"
    ),
    "48265745": (
        "ChatGPTに『1から100まででどれを選ぶ？』と聞いた結果",
        "ChatGPTの『ランダムな数』の偏りを大規模実験で記録。LLMの確率的挙動の癖を可視化する小ネタ。"
    ),
    "48264635": (
        "Geomatic：自動微分搭載のコマンド駆動ジオメトリスタジオ",
        "コマンドベースで形状を構築できる新しいジオメトリスタジオ。自動微分で形状最適化に応用可能。"
    ),
    "48264290": (
        "『AIに文章を書かせるな』——文章とは何かを問い直すエッセイ",
        "AIに自分の代わりに文章を書かせる行為を強く否定するエッセイ。AI執筆を許容するか否かの議論にカウンターを投じる。"
    ),
    "48261753": (
        "『今ほどコンピュータサイエンスを学ぶのに良い時はない』",
        "AI時代こそCS基礎を学ぶ意義が高まっているというAtlantic論考。コーディング能力の希少化議論に対する反論。"
    ),
    "48259761": (
        "Eternal Sloptember（重複投稿）",
        "geohotのAIスロップ批判ブログのHN別スレッド。"
    ),
}

for it in d["sources"]["hn"]:
    if it["id"] in hn_map:
        t, s = hn_map[it["id"]]
        it["title_ja"] = t
        it["summary_ja"] = s

# -------- Reddit --------
reddit_map = {
    "1tmffqn": (
        "『高価なAI・ロボットがなぜ人間より安くなると考えられているのか分からない』",
        "高額なAI／ロボット投資が結局人件費より安く済むという業界の前提に、r/artificialのユーザが素朴に異議を唱えるスレッド。"
    ),
    "1tmawv5": (
        "Papers With Code、復活後の新機能ハイライト",
        "閉鎖から復活したPapers With Codeのアップデート週次第1回。OSS実装と論文の紐付けを再強化。"
    ),
    "1tn3e7k": (
        "『AI生成だが現実的に見える映像』が普通になる時代",
        "現実とAI生成の区別がほぼ不可能なレベルに到達した動画の例を共有するスレッド。"
    ),
    "1tmprdm": (
        "自己教師あり表現学習の非単調損失でHPをどう選ぶか",
        "損失が単調に下がらない自己教師あり学習でのHP・アーキ選定の実務知見を求めるスレ。"
    ),
    "1tndgv8": (
        "Uber COO『AIトークン課金の正当化が難しくなっている』",
        "UberのAndrew MacDonald COOが、AIエージェント運用のトークン消費に対する効果検証の難しさを語る記事のRedditスレ。"
    ),
    "1tlzy43": (
        "VLM vs OCR：長文ドキュメントQAでどちらが強い？",
        "図表・画像・テーブルを含む長文QAについて、Vision LLMと従来OCRパイプラインのトレードオフを実務目線で議論するスレッド。"
    ),
    "1tnarvu": (
        "AIエージェントに必要なのは自律性より監査ログ",
        "エージェントに自律性をさらに与える前に、すべての判断と外部呼び出しの監査トレイルを整備すべき、というオピニオン。"
    ),
    "1tmnb54": (
        "冷戦時代のAIを衛星画像データセットでテスト",
        "古典的AI手法を現代の衛星画像分類タスクに当てて性能を観察する小実験。"
    ),
    "1tmb7c6": (
        "MS PaintをAIに見せたら——AIが架空美術運動を捏造、Googleもそれを実在扱い",
        "ユーザのラクガキにAIが架空のアートムーブメント名を割り当て、さらにGoogle検索のAIサマリーがその架空ムーブメントを実在扱い、というハルシネーション伝播事例。"
    ),
    "1tmpfa9": (
        "Claudeの利用上限を1クリックで叩く方法",
        "Claudeのレート/利用上限に1クリックで到達するというデモ動画。利用設計の限界を皮肉る投稿。"
    ),
    "1tltq6b": (
        "『AIの未来について誰を信じればいいのか分からない』",
        "業界リーダーの言説が真っ二つに割れる中で、どこを信じるべきかというユーザの率直な問いかけ。"
    ),
    "1tm6mpt": (
        "次に完全に破壊される業界はどこか？",
        "AIによる次の主要破壊対象業界を予想するディスカッションスレ。"
    ),
    "1tn73ve": (
        "一つだけAIプロバイダを契約するならどこ？",
        "OpenAI、Anthropic、Google、DeepSeek等の中で1社だけ契約するなら、というアンケート的スレッド。"
    ),
    "1tme23u": (
        "マルチエージェントの失敗は『プロンプト問題』ではなく『組織設計問題』",
        "マルチエージェントループの失敗は、プロンプトを直すよりも役割分担・責任範囲を再設計するほうが効くという視点の投稿。"
    ),
    "1tn8uoq": (
        "ICMLワークショップは参加する価値があるか？",
        "ICMLのワークショップ採択論文を出すこと・現地参加の価値についての議論スレ。"
    ),
    "1tmq1eb": (
        "MergeNB：Jupyter Notebook向けマージ衝突解決UI(VS Code)",
        "VS Code拡張でJupyter Notebookのマージ衝突を視覚的に解決できるOSSプロジェクト。"
    ),
    "1tmshey": (
        "AI時代における『プラットフォーム提供者のブランド』問題",
        "OpenAI/Anthropic等のプラットフォーム提供者が、AIに対する文化的態度の変化の中でブランドをどう保つかを論じる投稿。"
    ),
    "1tnhnh5": (
        "有名なMETRの『AI時系列ホライズン』グラフに重大な誤りが多数",
        "AI能力推移を視覚化したMETRの著名グラフに、データソース・スケール・分類など多数の重大誤りがあるとする批判スレ。"
    ),
    "1tn1rtk": (
        "NVIDIA Isaac SimをRLで使う人、Isaac Labも併用してる？",
        "RLでIsaac Simを使う実務者が、Isaac Labとの併用が一般的かどうかを確認するスレッド。"
    ),
    "1tne1m4": (
        "Wix、AI関連で人員削減",
        "Wixが社内体制をAI中心に切り替える中で人員削減を行っているという話題。"
    ),
}

for it in d["sources"]["reddit"]:
    if it["id"] in reddit_map:
        t, s = reddit_map[it["id"]]
        it["title_ja"] = t
        it["summary_ja"] = s

# -------- GitHub --------
github_map = {
    "colbymchenry/codegraph": (
        "codegraph：エージェント向けにコードを事前インデックス化するナレッジグラフ",
        "Claude Code / Codex / Cursor / OpenCode等が共通で使える、ローカル100%のコードナレッジグラフ。事前にコード構造をグラフ化しておくことで、毎回のツール呼び出しとトークン消費を大幅削減。本日急上昇1位。"
    ),
    "rohitg00/ai-engineering-from-scratch": (
        "ai-engineering-from-scratch：ゼロから学ぶAIエンジニアリング",
        "プロダクション級AIアプリを『学んで→作って→届ける』までのフルパス教材。RAG、エージェント、評価まで網羅で急成長中。"
    ),
    "multica-ai/andrej-karpathy-skills": (
        "andrej-karpathy-skills：KarpathyのLLM落とし穴をCLAUDE.mdに凝縮",
        "Karpathyが指摘してきたLLMコーディングの典型的失敗パターンを1つのCLAUDE.mdに集約。Claude Code等のエージェント挙動を1ファイルで矯正できる。"
    ),
    "affaan-m/ECC": (
        "ECC：エージェント基盤の性能最適化システム",
        "スキル・直感・メモリ・セキュリティ・リサーチファーストな開発を提供する、Claude Code/Codex/Cursor等向けエージェントハーネス最適化システム。"
    ),
    "anthropics/knowledge-work-plugins": (
        "knowledge-work-plugins：Claude Cowork向け公式プラグイン集",
        "Claude Coworkで知識労働者が使う想定の、Anthropic公式オープンソースプラグイン集。"
    ),
    "mukul975/Anthropic-Cybersecurity-Skills": (
        "Anthropic-Cybersecurity-Skills：AIエージェント向けセキュリティスキル754本",
        "MITRE ATT&CK / NIST CSF 2.0 / ATLAS / D3FEND / NIST AI RMFにマップした、AIエージェント向け構造化サイバーセキュリティスキル集（754本）。"
    ),
    "manaflow-ai/cmux": (
        "cmux：縦タブ＋通知のGhostty製macOSターミナル、AIコーディングエージェント向け",
        "Ghostty基盤のmacOSターミナル。縦タブとプッシュ通知を備え、Claude Code等の並列エージェント運用に最適化。"
    ),
    "Leonxlnx/taste-skill": (
        "Taste-Skill：AIに『良い趣味』を与えるスキル",
        "Claude等のAIが生成する文章を、ありきたりなテンプレート出力ではなく洗練された質感に近づける『センス』を与えるスキル。"
    ),
    "hardikpandya/stop-slop": (
        "stop-slop：散文から『AIっぽさ』を消すスキル",
        "AI生成テキスト特有の言い回し（『一方で〜』『重要なのは〜』等）を検出・除去するためのスキルファイル。"
    ),
    "Fincept-Corporation/FinceptTerminal": (
        "FinceptTerminal：モダンなファイナンスターミナル",
        "市場分析・投資調査・経済データツールを統合した、Bloomberg風モダン金融ターミナル。"
    ),
    "anthropics/claude-cookbooks": (
        "claude-cookbooks：Claude活用Tipsを集めた公式ノートブック集",
        "AnthropicによるClaudeの面白く効果的な使い方をまとめたサンプルノートブック集。"
    ),
    "moeru-ai/airi": (
        "airi：セルフホスト型Grokコンパニオン",
        "セルフホスト・所有可能なAIキャラクターコンパニオン基盤。アニメ的キャラを自分のサイバー空間に置く実験プロジェクト。"
    ),
}

for it in d["sources"]["github"]:
    if it.get("full_name") in github_map:
        t, s = github_map[it["full_name"]]
        it["title_ja"] = t
        it["summary_ja"] = s

# -------- Blogs --------
blog_map = {
    "https://openai.com/index/grupo-folha-grupo-uol-partnership": (
        "OpenAI、ブラジルGrupo Folha/UOLとコンテンツ戦略提携",
        "ブラジル大手メディアGrupo Folha／UOLとOpenAIがコンテンツ提携。ChatGPTへ高品質ポルトガル語ニュースを供給する、メディア×AIモデル提携の南米拡張。"
    ),
    "https://huggingface.co/blog/agent-glossary": (
        "Harness／Scaffold他——AIエージェント用語集",
        "ハーネス、スキャフォルド、エージェント、ハンドオフなど、AIエージェント領域で乱用される用語の定義を整理する記事。"
    ),
    "https://huggingface.co/blog/nvidia/nemotron-labs-diffusion": (
        "Nemotron拡散言語モデルで『光速テキスト生成』へ",
        "NVIDIA Nemotron Labsの拡散言語モデル解説。トークン並列生成で長文を高速化、自己回帰の限界を突破する設計思想。"
    ),
    "https://blog.google/innovation-and-ai/technology/ai/io-2026-dialogues-recap/": (
        "Google I/O 2026 Dialoguesステージのリキャップ",
        "Sundar PichaiらがI/O 2026のDialoguesステージで議論した内容のまとめ。"
    ),
    "https://huggingface.co/blog/Dharma-AI/specialization-beats-scale": (
        "『スケールより専門化』——AI調達で見落としがちな戦略変数",
        "大規模汎用モデル一辺倒ではなく、特定タスクに特化したモデルの方が費用対効果で勝つ場面が増えてきた、というAI調達戦略の論考。"
    ),
    "https://openai.com/index/virgin-atlantic": (
        "Virgin Atlantic、Codexでモバイルアプリ刷新を期日内出荷",
        "ホリデー商戦の固定期日に向けて、Virgin AtlanticがCodexを活用しモバイルアプリを刷新。テストカバレッジほぼ100%、P1欠陥ゼロを達成。"
    ),
    "https://openai.com/index/gartner-2026-agentic-coding-leader": (
        "OpenAI、Gartner『エンタープライズAIコーディングエージェント』でリーダーに",
        "Gartner Magic Quadrant 2026で、OpenAI Codexがエンタープライズコーディングエージェント領域のリーダーに指定。"
    ),
    "https://openai.com/index/adventhealth": (
        "AdventHealth、ChatGPT for Healthcareで医療事務を圧縮",
        "米AdventHealthがChatGPT for Healthcareを導入し、事務作業を圧縮して患者ケアの時間を確保。"
    ),
    "https://blog.google/innovation-and-ai/infrastructure-and-cloud/global-network/missouri-programs/": (
        "Google、ミズーリ州への新規コミュニティ投資を発表",
        "次世代労働力育成とエネルギープログラムを軸にした、ミズーリ州への新規投資。AIデータセンター需要を背景にした地域投資の一環。"
    ),
    "https://blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/": (
        "Google I/O 2026で発表された100項目まとめ",
        "I/O 2026で発表されたGemini 3.5、AI Search、Workspace刷新などを含む100項目の公式まとめ。"
    ),
    "https://blog.google/innovation-and-ai/models-and-research/google-research/google-beam-group-meetings/": (
        "Google Beam、グループ会議に対応する新実験",
        "立体映像会議『Google Beam』が複数人グループミーティングに対応する実験を開始。"
    ),
    "https://openai.com/index/model-disproves-discrete-geometry-conjecture": (
        "OpenAIモデル、離散幾何学の重要予想を反証",
        "OpenAIのモデルが、離散幾何学における長年の中心予想を反証する証明を発見。AI主導の数学発見の象徴的成果。"
    ),
    "https://openai.com/index/ramp": (
        "Ramp、Codexでコードレビューを高速化",
        "Fintech RampのエンジニアがCodexで本格コードレビューを実施。所要時間が数時間から数分へ短縮。"
    ),
    "https://openai.com/index/the-next-phase-of-education-for-countries": (
        "OpenAI『Education for Countries』、次フェーズへ",
        "学校向けAI展開・教師研修・学習成果改善ツールを拡大する『Education for Countries』新フェーズ発表。"
    ),
    "https://openai.com/index/introducing-openai-for-singapore": (
        "OpenAI for Singapore発表——複数年の国家AI戦略パートナー",
        "シンガポール政府とOpenAIが、複数年のAI展開・人材育成・公共サービス支援パートナーシップを発表。"
    ),
    "https://huggingface.co/blog/allenai/olmoearth-v1-1": (
        "OlmoEarth v1.1：より効率的な地球観測モデル群",
        "AllenAI（Ai2）の地球観測基盤モデルOlmoEarthがv1.1へ。同等品質で計算量を抑えた効率重視アップデート。"
    ),
    "https://blog.google/innovation-and-ai/technology/developers-tools/google-io-2026-collection/": (
        "Google I/O 2026 コレクションページ",
        "I/O 2026で『AIをすべての人に役立つものにする』ためのアップデートを一覧化したコレクション。"
    ),
    "https://blog.google/products-and-platforms/products/search/ai-mode-us-insights/": (
        "Google AI Modeが米国の検索体験をどう変えているか",
        "Google検索のAIモードが米国ユーザの検索行動をどう変化させたかのインサイト記事。クエリの長文化・対話化の傾向。"
    ),
    "https://blog.google/products-and-platforms/products/workspace/workspace-updates/": (
        "Google Workspace、新しい作成・タスク機能",
        "GeminiベースのGoogle Workspaceに、ドキュメント作成・タスク管理の新機能を追加。"
    ),
    "https://blog.google/innovation-and-ai/sundar-pichai-io-2026/": (
        "I/O 2026：『エージェント版Gemini時代へようこそ』",
        "Sundar Pichaiによる基調メッセージ。Geminiをエージェントとして全プロダクトに統合する『エージェンティックGemini時代』を宣言。"
    ),
    "https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/": (
        "Gemini 3.5：『行動するフロンティア知性』",
        "Google DeepMindの新世代モデルGemini 3.5を発表。ベンチマーク更新に加え、ツール利用・エージェント実行を統合した『行動する知性』として位置付け。"
    ),
    "https://blog.google/products-and-platforms/products/search/search-io-2026/": (
        "AI Searchの新時代——『検索エンジンの最良の部分』とAIを融合",
        "Google検索のAI Modeをデフォルト体験に近づけるアップデート。"
    ),
    "https://openai.com/index/advancing-content-provenance": (
        "OpenAI、Content CredentialsとSynthIDでAIコンテンツの来歴強化",
        "AI生成コンテンツの来歴情報をContent CredentialsとSynthIDで付与し、検証ツールも提供。AIメディアの信頼性確保に向けた取り組み。"
    ),
    "https://huggingface.co/blog/ettin-reranker": (
        "Ettin Rerankerファミリー発表",
        "RAG・検索向けの新リランカーモデル群『Ettin』。サイズと精度のトレードオフを整理。"
    ),
}

for it in d["sources"]["blogs"]:
    if it["url"] in blog_map:
        t, s = blog_map[it["url"]]
        it["title_ja"] = t
        it["summary_ja"] = s

# -------- Highlights --------
def hn_item(id_):
    return next((x for x in d["sources"]["hn"] if x["id"] == id_), None)

def reddit_item(id_):
    return next((x for x in d["sources"]["reddit"] if x["id"] == id_), None)

def blog_item(url):
    return next((x for x in d["sources"]["blogs"] if x["url"] == url), None)

highlights = []

# 1. Gemini 3.5 launch - the biggest news today
i = blog_item("https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/")
highlights.append({
    "source": "blog",
    "title": i["title"],
    "title_ja": "Gemini 3.5発表——Googleが『行動するフロンティア知性』で全プロダクトをエージェント化",
    "url": i["url"],
    "hot_take_ja": "Google I/O 2026の主役はやはりGemini 3.5。ベンチマーク更新だけでなく、ツール利用・エージェント実行を中核機能として統合し、Pichaiは『エージェンティックGemini時代』と宣言した。ポイントは『チャットの王様』から『行動するOS』への移行であり、検索・Workspace・Androidが全部Geminiエージェント前提に再設計されたこと。OpenAIやAnthropicがAPIファーストでエンタープライズに食い込む間に、Googleはディストリビューション全体を一気にエージェント化する作戦に出た。",
    "detail_ja": "Google I/O 2026で発表されたGemini 3.5は、単なるベンチマーク更新ではなく『ツール呼び出しとエージェント実行を一級市民として組み込んだフロンティアモデル』として位置付けられた。同時にSundar Pichaiは基調メッセージで『エージェンティックGemini時代』を明示し、検索（AI Mode）、Workspace（ドキュメント・タスク自動化）、Android、開発者向けAPIにGeminiエージェントを横断的に統合する戦略を打ち出した。検索のAI Modeは米国でデフォルト体験に近づき、クエリは長文・対話化が進んでいるとの利用データも同日公開された。Workspaceでは、ユーザの指示一つで複数アプリをまたぐ作業をエージェントが完遂する新機能を投入。立体会議『Google Beam』のグループ対応など周辺プロダクトの発表100件もまとめて公開され、I/Oが『大量機能発表』から『プロダクト全体のエージェント化宣言』へとシフトしたことを示す。差別化は『どのチャットボットが賢いか』ではなく、『どこに既にユーザがいて、そこにAIをどう滑り込ませるか』。OpenAIやAnthropicがAPIとパートナーシップ（Dell・Singapore・Virgin Atlantic等）で勝負する一方、Googleはディストリビューションを武器に全方向同時にエージェント化を仕掛けている。",
    "detail_en": "Gemini 3.5, the centerpiece of Google I/O 2026, is positioned not as a benchmark bump but as a frontier model that treats tool use and agentic execution as first-class capabilities. In the same keynote, Sundar Pichai framed the moment as the 'agentic Gemini era' and announced cross-product integration of Gemini agents into Search (AI Mode), Workspace (document and task automation), Android, and developer APIs. The Search AI Mode is moving closer to the default US experience, with new usage data showing that queries are getting longer and more conversational. Workspace gains new features where a single user instruction can drive an agent across multiple apps end-to-end. Adjacent product launches — Google Beam group meetings, 100+ I/O announcements bundled together — show the shift from 'feature firehose' to 'whole product surface, re-architected around agents'. The strategic point is no longer 'which chatbot is smartest', it is 'where users already live, and how AI slips into that surface'. While OpenAI and Anthropic are competing through APIs and enterprise partnerships (Dell, Singapore, Virgin Atlantic), Google is leaning on distribution to make every Google touchpoint agentic at once.",
    "key_points_ja": [
        "Gemini 3.5は『行動する知性』としてエージェント実行を標準装備",
        "Pichaiが『エージェンティックGemini時代』を宣言",
        "Search・Workspace・Android全部にGeminiエージェント統合",
        "AI Modeが米国検索のデフォルト体験に近づく",
        "Googleの武器はモデル単体ではなくディストリビューション"
    ],
    "key_points_en": [
        "Gemini 3.5 ships with first-class tool use and agentic execution",
        "Pichai declares the 'agentic Gemini era'",
        "Gemini agents integrated into Search, Workspace, Android",
        "AI Mode moving toward default US Search experience",
        "Google's moat is distribution, not model raw IQ"
    ]
})

# 2. DeepSeek Reasonix - top HN story
i = hn_item("48256953")
highlights.append({
    "source": "hn",
    "title": i["title"],
    "title_ja": "DeepSeek Reasonix——フラッグシップ75%恒久値下げと同時に投入された純正コーディングエージェント",
    "url": i["url"],
    "hot_take_ja": "DeepSeekが純正コーディングエージェント『Reasonix』を発表、同タイミングで旗艦モデルAPIを75%恒久値下げ。Claude Code/Codex/Cursorが繰り広げる『高機能・高価格』エージェント戦争に、中国側が真っ正面から価格破壊で殴り込んだ格好だ。プロンプトキャッシュを徹底活用した超低コスト推論を売りにしており、エージェント設計のコスト前提を根底から書き換えにくる。",
    "detail_ja": "DeepSeek ReasonixはDeepSeekが自社モデル向けに最適化した純正コーディングエージェントで、HNで673ポイントを獲得し首位級に。最大の特徴は『プロンプトキャッシュ前提の超低コスト推論』で、エージェントが長い文脈を何度も読み直すコーディングワークフローでも、キャッシュにより実効単価が劇的に下がる設計。同日に報じられたDeepSeek旗艦APIの75%恒久値下げと組み合わせると、トークン単価の絶対値でClaude Code/Codex/Cursorに対して明確な価格優位が生まれる。重要なのは『安いから乗り換える』だけでなく、エージェント設計の前提条件が変わる点。単価が下がれば、これまで採算が合わなかった『超長時間・超大量推論を前提にした検証エージェント』『毎ターン制約を再注入する設計』（今週のConstraint Decay論文が推奨）も現実的になる。エコシステム的には、米中フロンティアが同じ方向に価格圧縮しており、勝負はもはや『価格』ではなく『エージェント設計とディストリビューション』へと移っている。Reasonix単体での実力はClaude Codeに比肩するか未知数だが、米国勢が無視できない圧力であることは明らかだ。",
    "detail_en": "DeepSeek Reasonix is DeepSeek's own native coding agent, tuned for its own models and built around aggressive prompt caching for low effective cost-per-call. It hit the top of HN with 673 points, on the same day Bloomberg reported DeepSeek's flagship API getting a permanent 75% price cut. Together the two moves frame a deliberate price-and-product attack on Claude Code, Codex, and Cursor: aggressive token economics plus a first-party agent designed to exploit them. The deeper consequence is that the cost premise of agent design changes. With unit prices down and caching cheap, designs that were previously uneconomic — long-horizon multi-turn agents, verifier subagents, and re-injecting constraints every turn (as recommended this week by the Constraint Decay paper) — become realistic at scale. Strategically, both US and Chinese frontier labs are now compressing price in the same direction, which pushes the competitive battle from price to agent design and distribution. Whether Reasonix matches Claude Code in raw capability is still an open question, but the pressure on the US incumbents to defend their margins is now explicit.",
    "key_points_ja": [
        "DeepSeekが純正コーディングエージェントReasonixを発表",
        "プロンプトキャッシュ前提で超低コスト推論を実現",
        "同タイミングで旗艦API 75%恒久値下げと組み合わせ",
        "Claude Code・Codex・Cursorへの価格＋プロダクト両面攻撃",
        "エージェント設計の経済前提が書き換わる"
    ],
    "key_points_en": [
        "DeepSeek launches first-party coding agent Reasonix",
        "Built around aggressive prompt caching for low cost-per-call",
        "Paired with permanent 75% cut on flagship API price",
        "Direct price + product attack on Claude Code / Codex / Cursor",
        "Cost premise of agent design starts to shift"
    ]
})

# 3. Pope Leo XIV AI encyclical
i = hn_item("48266485")
highlights.append({
    "source": "hn",
    "title": i["title"],
    "title_ja": "教皇レオ14世、初の回勅でAIを正面論——『AIは少数の権力者ではなく人類に奉仕すべき』",
    "url": i["url"],
    "hot_take_ja": "ローマ教皇レオ14世が就任後初の回勅で、AIを中心テーマに据えて『不透明なAIが少数企業に握られることは新たな非人間化を生む』と警告した。テック業界の自主規制と各国規制の狭間で言葉が空回りしてきたAIガバナンス議論に、世界14億人のカトリック信徒を代表する道徳的な発話が初めて公式に加わった意味は大きい。EU AI Act、UK AI Bill、米州法と並ぶ『第4の規範軸』として、企業の社内倫理ポリシーに思いのほか強く効いてくる可能性がある。",
    "detail_ja": "教皇レオ14世は就任後初の回勅でAIを中心議題に据え、(1)AIは特定の権力集団や少数企業ではなく『人類全体』に奉仕すべき、(2)不透明なAIが少数の企業に集中することは『新たな形の非人間化』を生む、(3)アルゴリズムが人間の尊厳と労働を侵食するリスクを軽視してはならない、と明示した。教皇職の回勅は法的拘束力を持たないが、カトリック教会の社会教説の中核文書として、各国の教育機関・医療機関・労組・倫理委員会のガイドライン作成に長期間影響する。直近の業界文脈とも噛み合う：今週の他のニュースでもUber COOがAIトークン消費の正当化に疑問を呈し、Amnesty InternationalがNHSデータのPalantirへの『無制限アクセス』を告発、AI搾取／AI集中の問題が立て続けに表面化している。EU AI Actは執行段階に入り、UKもAI Bill審議に入る局面で、宗教的・道徳的アクセントが加わったことは、企業の社内倫理ポリシー・調達基準・データ提供契約に実質的に効いてくる可能性がある。技術側の反応は『また精神論か』と『歴史的に重要な発話だ』に二分するだろうが、本質的な争点は『AIの便益を誰が所有するか』であり、これは今後数年のAI政策の核心テーマだ。",
    "detail_en": "Pope Leo XIV used his first papal encyclical to put AI at the center of Catholic social teaching, with three main claims: (1) AI must serve humanity as a whole, not a narrow set of corporations or political powers; (2) opaque AI concentrated in the hands of a few firms creates 'new forms of dehumanization'; (3) algorithmic systems that erode human dignity and labor must not be tolerated. Encyclicals are not legally binding, but they are core documents of Catholic social teaching that shape institutional ethics policy across Catholic-affiliated schools, hospitals, unions, and ethics boards for decades. The timing dovetails with several other AI-power stories this week: Uber's COO publicly questioning whether 'tokenmaxxing' spend is justified, Amnesty International alleging that the NHS gave Palantir effectively unlimited access to identifiable patient data, and growing scrutiny of AI concentration in general. With the EU AI Act in enforcement and the UK preparing its own AI Bill, the addition of an explicit religious-moral axis to the debate is more than symbolic — it is likely to influence corporate ethics statements, procurement criteria, and data-sharing contracts. The underlying contested question is 'who owns the upside of AI', and that question is going to dominate AI policy for the next several years.",
    "key_points_ja": [
        "レオ14世が初の回勅でAIを中心議題に据える",
        "『不透明なAIの少数企業集中』を新たな非人間化と批判",
        "EU AI Act・UK AI Billと並ぶ第4の規範軸として作用しうる",
        "Uber COO発言・Palantir/NHS問題と問題意識が共鳴",
        "本質的争点は『AIの便益を誰が所有するか』"
    ],
    "key_points_en": [
        "Pope Leo XIV centers his first encyclical on AI",
        "Warns that concentrated, opaque AI creates new dehumanization",
        "Adds a moral/religious axis alongside EU AI Act and UK AI Bill",
        "Resonates with Uber COO pushback and Palantir/NHS scandal",
        "Underlying question: who owns the upside of AI?"
    ]
})

# 4. Uber COO on AI tokenmaxxing
i = hn_item("48268871")
highlights.append({
    "source": "hn",
    "title": i["title"],
    "title_ja": "Uber COO『AIトークン消費の正当化が日に日に難しくなっている』——大企業側からの効果検証圧力",
    "url": i["url"],
    "hot_take_ja": "UberのCOOが、エージェントによる大量トークン消費（『tokenmaxxing』）の経済合理性を真顔で疑問視した、というのが今週の地味だが効く一撃。AI支出を聖域にしてきた米メガテックの中から、初めて『費用対効果が見えない』と言葉にした幹部が出てきた格好で、これは個別の予算カット話ではなくエンタープライズ全体のセンチメントが変わる前触れだ。DeepSeekの値下げと表裏一体で、『安くしないと使ってもらえない』フェーズが本格化する。",
    "detail_ja": "UberのAndrew MacDonald COOがBusiness Insiderのインタビューで、社内のAIエージェント運用に伴うトークン消費の急増と、それに対する効果検証の難しさを率直に語った。発言の含意は二つ。第一に、これまで『AIに金を出せば自動的に生産性が上がる』という前提でAI予算は青天井に近かったが、それが普通のIT支出と同じく『単位コストあたりの成果』を問われるフェーズに入ったということ。第二に、Uberほど規模があり社内データもあるテック企業ですら正当化が難しいのなら、それより小さい企業は更に厳しいということ。市場的にはDeepSeekの75%恒久値下げと完全に整合し、ベンダ側が価格を圧縮しないと企業側のROIモデルが崩壊する局面に来た。同日のHNで人気を集めた『Claudeはアーキテクトじゃない』論や、『マルチエージェント失敗は組織設計問題』論とも噛み合い、業界全体が『AIをばらまけば良い』から『どこに効くか厳密にやる』へ振り子が振れつつあることを示すサンプルだ。",
    "detail_en": "Uber COO Andrew MacDonald told Business Insider that the company is finding it increasingly hard to justify the token spend that comes with running AI agents at scale — a remarkably plain statement of cost discipline from a hyperscale tech company. Two implications stand out. First, the assumption that AI spend will pay back automatically because 'AI raises productivity' is being replaced with normal unit-economics scrutiny: cost per outcome, not gross AI budget. Second, if Uber — with its scale, data, and reasonably mature AI integration — finds the math hard, smaller companies will find it even harder. That mood-shift dovetails directly with DeepSeek's permanent 75% price cut: the supply side already understands that vendors need to compress prices, or enterprise ROI models break. It also resonates with the same-week HN narratives: 'Claude is not your architect' (don't let agents drive design), 'multi-agent failures are org-design failures, not prompt failures', and the Constraint Decay paper. The industry pendulum is swinging from 'sprinkle AI everywhere' toward 'measure where it actually pays back, and design accordingly'.",
    "key_points_ja": [
        "Uber COOがAIトークン消費の正当化を疑問視",
        "メガテック内部からAI支出の効果検証圧力",
        "DeepSeek値下げと同じセンチメントの裏表",
        "『Claudeはアーキテクトじゃない』論とも共鳴",
        "業界の振り子が『ばらまき』から『精緻運用』へ"
    ],
    "key_points_en": [
        "Uber COO questions justification for AI token spend",
        "Cost discipline starting inside hyperscale tech firms",
        "Mirrors DeepSeek's permanent 75% price cut",
        "Aligns with 'Claude is not your architect' narrative",
        "Industry pendulum swings from spray to precision"
    ]
})

# 5. Eternal Sloptember by geohot - cultural critique going viral
i = hn_item("48263238")
highlights.append({
    "source": "hn",
    "title": i["title"],
    "title_ja": "geohot『Eternal Sloptember』——AIスロップが永遠化したウェブへの宣戦布告",
    "url": i["url"],
    "hot_take_ja": "George Hotz(geohot)が、AI生成スロップに埋め尽くされる現代のウェブを『永遠のSeptember』（Usenetが大衆化で一気に劣化した1993年の事件）になぞらえて批判した文章。技術者側の身内発話だが、AI業界の主要幹部が読み逃せない一本になっている。問題は『AIを使うこと』ではなく『AIで雑に量産すること』にある、というメッセージが、同時期の『AIに文章を書かせるな』論や教皇回勅と共鳴して効いてくる。",
    "detail_ja": "geohot(tinygradのGeorge Hotz)が自ブログで、AI生成コンテンツでウェブが劣化していく状況を、Usenet史上の有名なエピソード『Eternal September』（1993年9月にAOLが大量のネット初心者を流入させ、Usenetの文化が永遠に変質した事件）になぞらえて論じた。主張は三段：(1)AIが文章・画像・コードを量産可能にしたことで、ウェブの一次情報密度が急激に薄まっている、(2)もはや高品質な情報を見つける作業より、低品質スロップを濾過する作業のほうがコストが高い、(3)この変化はもう逆戻りしない『eternal』であり、それを前提に技術・社会の設計を立て直す必要がある。重要なのは、geohot自身がAI開発者でありAI否定派ではない点で、議論の核は『AIをどう使うか』の規律論だ。同時期にHN上位に上がった『AIに文章を書かせるな』エッセイ、教皇レオ14世の回勅、そして『AI Washing』批判記事と共鳴する。実利的な示唆としては、(a)AI生成コンテンツの来歴情報（OpenAIが同日発表したContent Credentials/SynthID）の重要度が上がる、(b)個人サイト・小規模コミュニティの『人間っぽさ』が改めて差別化要素になる、(c)ベンダ側にもユーザ側にも『大量生成の自制』が求められる、という流れになる。",
    "detail_en": "George Hotz (geohot, of tinygrad) wrote a blog post arguing that the AI-saturated web is the equivalent of Usenet's 'Eternal September' — the 1993 event when AOL flooded Usenet with newcomers and permanently degraded the culture. His three-part argument: (1) AI-driven mass generation of text, images, and code is collapsing the density of original signal on the web; (2) finding high-quality information is now cheaper than filtering out low-quality slop; (3) the change is irreversible — 'eternal' — and society needs to redesign infrastructure on that assumption. The piece carries weight because Hotz is himself a serious AI builder, not an AI skeptic; his point is about discipline of use, not abolition. It resonates with several same-week pieces: the 'don't let AI do your writing' essay, Pope Leo XIV's encyclical on AI dehumanization, and the Guardian's 'AI washing' story. Practical implications: (a) content provenance schemes (OpenAI announced new Content Credentials / SynthID work on the same day) become much more important, (b) handmade small sites and communities regain differentiation value, (c) both vendors and users have to develop genuine restraint about mass-generation. Slop as a load-bearing critique is moving from joke to industry concern.",
    "key_points_ja": [
        "geohotがAIスロップ氾濫を『Eternal September』に喩える",
        "現実問題：高品質情報の探索より濾過のほうが高コストに",
        "AI開発者本人による警鐘という重み",
        "OpenAIのContent Credentials/SynthIDなど来歴対策の重要度UP",
        "『大量生成の自制』が業界の共通課題に"
    ],
    "key_points_en": [
        "geohot frames the AI slop web as an Eternal September",
        "Filtering low-quality content now costs more than finding good content",
        "Notable because it comes from an AI builder, not an AI skeptic",
        "Boosts the case for content provenance (e.g. OpenAI SynthID)",
        "Restraint on mass generation becomes an industry question"
    ]
})

d["highlights"] = highlights

with open(OUT, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f"Wrote {OUT}")
print(f"Highlights: {len(highlights)}")
