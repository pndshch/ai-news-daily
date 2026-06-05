#!/usr/bin/env python3
"""Enrich raw-2026-06-05.json with Japanese/English summaries + highlights."""
import json
from pathlib import Path

DATE = "2026-06-05"
ROOT = Path(__file__).resolve().parent.parent
raw = json.load(open(ROOT / f"data/raw-{DATE}.json"))
src = raw["sources"]

# ---- helper: set ja fields by index ----
def setja(items, idx, title_ja, summary_ja):
    if idx < len(items):
        items[idx]["title_ja"] = title_ja
        items[idx]["summary_ja"] = summary_ja

# ============ ARXIV ============
arxiv = [
    ("TailLoR: 継続学習で主成分を保護するパラメータ効率的手法", "LoRA微調整時に重要な主成分(過去知識)を守りつつ新タスクを学ぶ継続学習法。破滅的忘却を抑えながら効率的に適応する。"),
    ("HANDOFF: 蒸留した相補的教師でヒューマノイド全身制御", "複数の専門教師方策を1つの生徒に蒸留し、ヒューマノイドの全身協調タスクをエージェント的に解く制御フレームワーク。"),
    ("Code2LoRA: ソフト進化に対応するコードLLM向けハイパーネット生成アダプタ", "コードベースの変化に応じてLoRAアダプタをハイパーネットワークで動的生成し、再学習なしにコードLLMを最新の仕様へ追従させる。"),
    ("TempoVLA: 速度を制御できるVision-Language-Action方策", "ロボット動作の実行速度を言語指示で調整できるVLA方策。同じタスクを速く/遅く実行する制御性を学習で獲得する。"),
    ("適応的な相手に対する繰り返しゲームでのリグレット最小化", "対戦相手が学習・適応してくる繰り返しゲームで、後悔(リグレット)を抑える新しいアルゴリズムを理論的に提案。"),
    ("PAR3D: 部位認識表現を持つ統一3D-MLLM", "シーン理解のため、物体を部位レベルで認識する表現を組み込んだ統一的な3Dマルチモーダル大規模言語モデル。"),
    ("操作誘導の段階的Human-to-AIテキスト変換ベンチマーク", "人間が書いた文章をAI的に書き換える過程を多粒度で評価するベンチマーク。AI生成テキスト検出研究の基盤となる。"),
    ("DNQ: 部分観測のnプレイヤーゲーム向けDeep Nash Q-Network", "観測が限られた多人数ゲームでナッシュ均衡を学習するQ学習手法。複雑な戦略ゲームへの強化学習適用を広げる。"),
    ("再帰なしで再帰型ネットワークを事前学習する", "RNNの学習を、時間方向に逐次なBPTTではなく「教師ありメモリ訓練(SMT)」で並列化。勾配消失を避け長距離依存を学べると主張。"),
    ("複雑度バランス型の拡散スプリッティング", "拡散モデルのサンプリングを計算複雑度の観点で均衡化し、生成品質と速度のトレードオフを改善する手法。"),
    ("想像して考える: ワールドシミュレータによる空間推論エージェント", "VLMが観測外のレイアウトを推論できるよう、ワールドシミュレータで未観測の視点を「想像」させ空間推論を強化する。"),
    ("RREDCoT: 推論モデル向けセグメント単位の報酬再配分", "推論の連鎖(CoT)をセグメント単位に分け、各段階に報酬を再配分することで推論モデルの学習を安定・効率化する。"),
    ("拡散言語モデルのための自己拡張検索", "拡散型の言語モデルに、自分で検索クエリを生成して文脈を補強する自己拡張検索を導入し生成を改善する。"),
    ("MLEvolve: ML アルゴリズム自動発見の自己進化フレームワーク", "LLMエージェントが機械学習アルゴリズムを長期にわたり自己進化的に探索・発見する枠組み。分岐間の情報共有と階層制御で長期最適化を実現。"),
    ("PC Layer: LLM事前学習を改善する多項式重み前処理", "重み行列を多項式で前処理(プリコンディショニング)し、LLM事前学習の収束を速める新しい層。"),
    ("良い補間器はどれくらい豊富にあるか?", "過剰パラメータモデルが訓練データを完全に補間しつつ汎化する「良い補間器」の存在量を理論的に分析する。"),
    ("Goedel-Architect: ブループリント生成によるLean4形式証明の効率化", "定理証明を、定義と補題の依存グラフ(ブループリント)を先に生成・洗練してから埋めるエージェント的フレームワーク。Lean4で機能。"),
    ("You Only Index Once: 共有ルーティングのクロス層スパース注意", "長文推論の復号効率を上げるため、一度作ったインデックスを層をまたいで共有するスパース注意。速度と品質を両立。"),
    ("成人とLLMを科学者として比較: 能動的探索で得をするのは誰か", "人間とLLMに同じ探索課題を課し、能動的に実験して仮説を立てる能力を比較。LLMと人の科学的探索の差を測る。"),
    ("Benchmark Everything Everywhere All at Once", "多様なタスク・モダリティを一括で評価する統合ベンチマーク基盤の提案。"),
    ("方策更新なしのフローベース方策適応", "学習済み方策の重みを更新せず、フローベースの手法で新環境へ適応させる強化学習アプローチ。"),
    ("エージェントは自分を忌避するか: アクセス拒否信号への遵守を測る", "LLMエージェントが「このリソースへのアクセスは拒否」という帯域内信号にちゃんと従うかを測定。エージェントの安全性評価。"),
    ("AI-RAN向けパラメータ-KPI依存学習のためのイベント検出", "無線アクセスネットワーク(AI-RAN)で、設定パラメータと性能指標(KPI)の依存関係を学習するためのイベント検出手法。"),
    ("In-Context Multiple Instance Learning", "文脈内学習(in-context)の枠組みで複数インスタンス学習(MIL)を行う手法。ラベルが袋単位の弱教師問題に対応。"),
    ("足場か語彙か? ポパー的コード生成の二層・事前登録研究", "コード生成における足場(scaffold)と語彙の役割を、事前登録した統制実験で検証する方法論的研究。"),
]
for i,(t,s) in enumerate(arxiv):
    setja(src["arxiv"], i, t, s)

# ============ HN ============
hn = [
    ("Anthropicの脆弱性発見オープンソースフレームワーク", "Claudeでコードの脆弱性を自律発見・修正するリファレンス実装。脅威モデリングから動的スキャン、トリアージ、パッチ生成まで7段階のパイプラインを公開。"),
    ("AIが自分自身を作るとき: 再帰的自己改善への進捗", "Anthropicによる、AIがAIの研究開発を加速させる「再帰的自己改善」の現状レポート。"),
    ("宇宙飛行士、空気漏れ修理で待避後ISSへ帰還指示", "ISSの空気漏れ修理中に待避していた飛行士が帰還を指示された件。AI外の宇宙ニュース。"),
    ("Open Code Review – AI駆動のコードレビューCLIツール", "ターミナルでAIにコードレビューさせるオープンソースCLI。プルリクの差分を解析して指摘する。"),
    ("Uruky(EU拠点のKagi代替検索)が画像検索とURL書換に対応", "プライバシー重視のEU製有料検索エンジンが機能拡充。Kagiの代替を狙う。"),
    ("pg_durable: MicrosoftがDB内で耐久実行をOSS化", "PostgreSQL内で耐久的なワークフロー実行を可能にするMicrosoftのOSS。"),
    ("韓国の掲示板、全画像をAI検閲ツールでスキャン義務化へ", "韓国でオンライン掲示板が投稿画像をAI検閲にかける規制案。表現の自由を巡り議論。"),
    ("WSL 2のWindowsファイルシステムアクセスが高速化", "WSL2でWindows側ファイルへのアクセス性能が改善される。"),
    ("1995年風のドキュメントを書くようLLMを微調整", "あえて90年代風の文体でドキュメントを書くようLLMを微調整した実験的取り組み。"),
    ("ESP32 Bit Pirate: あらゆるプロトコルを話すハードハッキングツール", "WebCLIから多様な通信プロトコルを扱えるESP32ベースのハードウェアハッキングツール。"),
    ("Google社員、自社AIがダメだとミームを内部共有", "「新コードの75%はAI生成」という経営陣の主張に対し、現場社員は自社AIコード生成の質を内部ミームで揶揄。建前と本音のギャップが露呈。"),
    ("プログラマはClaudeのためには書くが、同僚のためには書かない", "人間の同僚向けには省略されがちなドキュメントを、AIに読ませるためなら書く——という開発文化の皮肉を指摘するエッセイ。"),
    ("Claudeはrsyncのバグを増やしたのか?", "「ClaudeがrsyncのコードをダメにしてバグAが増えた」という炎上を統計的に検証。36リリースを重み付き指標で分析し、有意な悪化はなかったと結論。"),
    ("KVarN: Huawei製のvLLM向けKVキャッシュ量子化バックエンド", "vLLMでKVキャッシュを量子化しメモリを削減するHuaweiのネイティブバックエンド。"),
    ("GoogleがTimnit Gebruを解雇する原因となったLLM警告は全て現実に", "Gebruが2020年に警告したLLMのリスク(偏見・環境負荷・誤情報等)が今や全て現実化した、と振り返る投稿。"),
    ("Pentagon、中南米向けAIプロパガンダ工場を運営", "米軍南方特殊作戦軍が運営する「La Tilde」。家計記事に軍事プロパガンダを混ぜ、文章も画像もLLM/Midjourneyで大量生成していたとInterceptが暴露。"),
    ("Ask HN: あなたの(AI)開発スタックとワークフローは?", "HNユーザーが各自のAI開発ツール構成やワークフローを共有するスレッド。"),
    ("Show HN: Boxes.dev – localhostを捨ててClaude CodeとCodexをクラウドで", "Claude CodeやCodexをクラウド上で動かす開発環境サービス。"),
    ("米軍はGPSを世界規模の『ナンバーズ局』に変えた", "GPS信号を秘密通信に転用していたという話題。AI外の技術ニュース。"),
    ("Show HN: FFmpeg WebCLI – ブラウザ完結のFFmpeg(WASM・オフライン)", "アップロード不要でブラウザ内完結のFFmpeg。WASMで動くPWA。"),
]
for i,(t,s) in enumerate(hn):
    setja(src["hn"], i, t, s)

# ============ GITHUB ============
gh = [
    ("headroom: LLMに渡す前にツール出力やログを圧縮", "ツール出力・ログ・RAGチャンクをLLM投入前に60-95%圧縮しトークンを節約。ライブラリ/プロキシ/MCPサーバで提供。"),
    ("あなたと共に成長するエージェント", "ユーザーと共に学び成長していくタイプのAIエージェント実装。"),
    ("エージェントハーネスの性能最適化システム", "スキル・本能(instincts)などでエージェントのハーネス性能を最適化する仕組み。"),
    ("PDF・画像を構造化データに変換", "あらゆるPDFや画像ドキュメントをAI向けの構造化データに変換するパワフルなツール。"),
    ("Reddit/X/YouTube/HNを横断調査するエージェントスキル", "任意トピックを複数SNS・サイト横断でリサーチするAIエージェントスキル。"),
    ("NVIDIA Cosmos: 物理AI向けワールドモデルのオープン基盤", "世界モデル・データセット・ツールをまとめたNVIDIAのオープンな物理AIプラットフォーム。"),
    ("エージェント&生成UIのためのフロントエンドスタック", "React/Angular対応の、エージェントと生成UI構築のためのフロントエンド基盤。"),
    ("GitHub Copilot Agentをアプリに統合するマルチプラットフォームSDK", "Copilot Agentを各種アプリへ組み込むためのSDK。"),
    ("最高ベンチのオープンソースAIメモリシステム", "ベンチマーク最強を謳う無料のAIメモリ(記憶)システム。"),
    ("コンテナの脆弱性・誤設定・秘密情報・SBOMを検出", "コンテナ等から脆弱性・設定ミス・秘密情報・SBOMを発見するセキュリティスキャナ。"),
    ("AIエージェントにインターネットを見る目を与える", "X(Twitter)などWeb全体を読んで検索できるようAIエージェントに与えるツール。"),
    ("OpenAI Plugins", "OpenAIのプラグイン関連リポジトリ。"),
]
for i,(t,s) in enumerate(gh):
    setja(src["github"], i, t, s)

# ============ BLOGS ============
bl = [
    ("Google DeepMind: 2026年5月に発表したAIニュースまとめ", "DeepMindが5月に公表した主要発表のまとめ記事。"),
    ("Hugging Face: Nemotron 3.5 コンテンツ安全モデル", "NVIDIAの、カスタマイズ可能なマルチモーダル安全性(コンテンツ・モデレーション)モデル。"),
    ("Hugging Face: EVA-Bench Data 2.0 — 3領域121ツール213シナリオ", "エージェント評価用ベンチEVA-Benchの拡張版。3領域・121ツール・213シナリオを収録。"),
    ("OpenAI: Endavaがソフト開発をAIエージェント中心に再設計", "IT企業Endavaが開発プロセスをAIエージェント中心に作り替えた事例。"),
    ("OpenAI: Dreaming — より役立つChatGPTのための記憶強化", "会話をまたいで嗜好や文脈を保持する新しいメモリ機構をChatGPTに導入。"),
    ("OpenAI: 知能時代の生物防御(Biodefense)", "AIで生物学的脅威への耐性を高めるための行動計画。GPT-Rosalindなど生命科学AIと併せた防御戦略。"),
    ("OpenAI: GPT-Rosalindに新機能を追加", "生物学的推論・医薬品化学・ゲノミクス解析・実験ワークフローを強化した生命科学特化モデルGPT-Rosalindの新機能。"),
    ("Google DeepMind: Google検索で古着・ヴィンテージ探しを格上げする5つの方法", "Google検索のショッピング機能を使った古着探しのコツ紹介(ライフスタイル記事)。"),
    ("Hugging Face: チャットボットを超えたDPO", "選好最適化(DPO)をチャットボット以外の用途へ応用する解説。"),
    ("OpenAI: WasmerがCodexでエッジ向けNode.jsランタイムを構築", "WasmerがCodexを使いエッジで動くNode.jsランタイムを開発した事例。"),
    ("OpenAI: 公共政策アジェンダ", "安全性・若年者保護・労働移行・国際標準などOpenAIの政策方針。"),
    ("OpenAI: フロンティアAIの民主的ガバナンスの青写真", "フロンティアAIの安全・耐性・安全保障のための米連邦ガバナンス枠組みの提案。"),
    ("Hugging Face: Reachy MiniにMCPツールを追加", "卓上ロボットReachy MiniにMCPツールを統合する取り組み。"),
    ("Hugging Face: Holo3.1 — 高速・ローカルなコンピュータ操作エージェント", "オンデバイスで動く高速なコンピュータ操作(GUI)エージェントHolo3.1。"),
    ("OpenAI: Travelers社がAI保険請求処理を全国展開", "保険大手TravelersがOpenAIを使ったAI請求処理を全国に展開。"),
    ("OpenAI: あらゆる役割・ツール・ワークフローのためのCodex", "Codexを開発者以外の役割や多様なツール・業務にも広げる発表。"),
    ("OpenAI: グローバルなリーダーシップによる若者の安全と機会の前進", "若年者の安全と機会のための国際的な取り組み。"),
    ("Google DeepMind: GeminiでGoogle I/O 2026を作った方法", "Geminiを使ってI/O 2026のイベントを制作した舞台裏。"),
    ("Hugging Face: Mellum2 — JetBrains製12B MoEモデル", "JetBrainsが公開したコード向け12BパラメータのMixture-of-Expertsモデル。"),
    ("Hugging Face: LLMを超えて — 企業AI普及はエージェントロジックに依存", "スケーラブルな企業AI導入にはLLM単体でなくエージェントのロジック設計が鍵という論考。"),
    ("Hugging Face: hf CLIをエージェント最適化で設計", "Hub操作用hf CLIを、エージェントが使いやすいよう再設計した話。"),
]
for i,(t,s) in enumerate(bl):
    setja(src["blogs"], i, t, s)

# ============ HIGHLIGHTS ============
highlights = [
    {
        "source": "Hacker News",
        "title": "Anthropic's open-source framework for AI-powered vulnerability discovery",
        "title_ja": "Anthropic、AIによる脆弱性発見フレームワークをオープンソース公開",
        "url": "https://github.com/anthropics/defending-code-reference-harness",
        "hot_take_ja": "「AIが攻撃に使われる」恐怖の裏で、Anthropicは“守る側”の自動化を全部見せた。脅威モデリング→動的スキャン→トリアージ→パッチまで7段階を回し、N体のエージェントが3/3でクラッシュを再現できた脆弱性だけを通す。AI脆弱性発見の標準実装を無料で配る、という静かなインフラ提供だ。",
        "detail_ja": "Anthropicが、Claudeを使ってソースコードの脆弱性を自律的に発見・修正するリファレンス実装『defending-code-reference-harness』をオープンソースで公開した。これはセキュリティチームとの協業から得た知見をまとめたもので、対話的に使える“スキル”群と、完全自動のスキャンパイプラインの両方を含む。自動パイプラインは7段階で動く:①ターゲットをDocker化しASAN等の計装を入れてビルド、②エージェントがコードを入力解析サブシステムに分割(recon)、③N体の並列エージェントが不正入力を作りクラッシュを3回中3回再現するまで探索(find)、④別の採点エージェントがまっさらな隔離コンテナで再現を検証(verify)、⑤既知バグとの重複を判定(dedupe)、⑥悪用可能性・到達性・深刻度を構造化レポート化(report)、⑦元のPoCがもう刺さらないことを確認しつつ修正を生成(patch)。鍵は“実行で検証する”点で、静的解析だけの手法より誤検知を大幅に減らせると主張する。エージェントはgVisorコンテナで隔離され、ネットワークはClaude APIのみに制限される。参照実装はC/C++のメモリ系脆弱性向けだが、`/customize`スキルで他言語・他の脆弱性クラスにも拡張できる。AI脆弱性発見の“防御側テンプレート”を誰でも使えるようにした点が大きい。",
        "detail_en": "Anthropic open-sourced 'defending-code-reference-harness,' a reference implementation that uses Claude to autonomously find and fix vulnerabilities in source code. Distilled from its work with security teams, it ships both interactive skills and a fully autonomous scanning pipeline. The pipeline runs in seven stages: (1) Build the target into a Docker image with instrumentation like ASAN; (2) Recon, where an agent partitions the code into input-parsing subsystems; (3) Find, where N parallel agents craft malformed inputs until a crash reproduces 3 out of 3 times; (4) Verify, where a separate grader agent reproduces the crash in a fresh, isolated container; (5) Dedupe against known bugs; (6) Report with structured exploitability, reachability, and severity analysis; (7) Patch, generating a fix and confirming the original PoC no longer crashes. The core idea is execution-verified findings, which the team claims sharply reduce false positives versus static-only scanning. Agents run inside gVisor containers with network egress restricted to the Claude API only. The reference targets C/C++ memory bugs but can be retargeted to other languages and vulnerability classes via a `/customize` skill. The significance is that it hands defenders a usable, end-to-end template for AI-driven vulnerability discovery.",
        "key_points_ja": [
            "Claudeで脆弱性を自律発見・修正する公式OSS実装",
            "7段階: build→recon→find→verify→dedupe→report→patch",
            "3/3でクラッシュ再現した脆弱性だけ通す実行検証型",
            "誤検知を静的解析より大幅に減らすと主張",
            "エージェントはgVisorで隔離・通信はClaude APIのみ",
            "C/C++向け参照実装、/customizeで他言語へ拡張可"
        ],
        "key_points_en": [
            "Official OSS for autonomous vuln find-and-fix with Claude",
            "7 stages: build→recon→find→verify→dedupe→report→patch",
            "Execution-verified: only crashes reproduced 3/3 pass",
            "Claims far fewer false positives than static scanning",
            "Agents sandboxed in gVisor, egress limited to Claude API",
            "C/C++ reference; retargetable via /customize skill"
        ],
    },
    {
        "source": "OpenAI",
        "title": "Introducing new capabilities to GPT-Rosalind",
        "title_ja": "OpenAI、生命科学特化モデル『GPT-Rosalind』を強化",
        "url": "https://openai.com/index/introducing-new-capabilities-to-gpt-rosalind",
        "hot_take_ja": "ChatGPTが汎用で殴る一方、OpenAIは“分野特化モデル”の旗も立て始めた。GPT-Rosalind(名はロザリンド・フランクリン由来か)は生物学的推論・医薬品化学・ゲノミクス・実験計画に振り切った専用モデル。同日に出た生物防御(Biodefense)計画とセットで、OpenAIが本気でライフサイエンスを取りに来たのが分かる。",
        "detail_ja": "OpenAIが生命科学に特化したモデル『GPT-Rosalind』の新機能を発表した。汎用のChatGPTとは別系統の、研究用途に振り切ったモデルという位置づけだ。強化されたのは、生物学的推論(biological reasoning)、医薬品化学(medicinal chemistry)の専門知、ゲノミクス解析、そして実験ワークフローの設計・支援といった能力。狙いは、論文の読解や仮説生成にとどまらず、実際の創薬や遺伝子解析、実験プロトコルの立案といった“湿った実験(wet lab)”に近い工程までAIが伴走することにある。注目すべきは、同日にOpenAIが「知能時代の生物防御(Biodefense in the Intelligence Age)」という行動計画も公表している点で、強力な生命科学AIは創薬を加速する一方、悪用すれば生物学的脅威にもなりうる——という両刃の剣を、能力強化と防御策をセットで出すことで先回りしようとしている。分野特化モデルは、汎用モデルより専門タスクで精度・信頼性を上げやすい反面、誤りが専門家以外には検証しづらいという課題もある。創薬や臨床に直結する領域だけに、生成内容の正確性と検証可能性が今後の鍵になる。なお現時点で公開された性能の定量値は限定的で、実運用での評価はこれからだ。",
        "detail_en": "OpenAI announced new capabilities for GPT-Rosalind, a model purpose-built for the life sciences and distinct from general-purpose ChatGPT. The upgrades target biological reasoning, medicinal-chemistry expertise, genomics analysis, and the design and support of experimental workflows. The ambition goes beyond reading papers and generating hypotheses: it aims to assist with the more 'wet-lab'-adjacent steps of drug discovery, genetic analysis, and experimental protocol design. Notably, OpenAI published a 'Biodefense in the Intelligence Age' action plan the same day — an acknowledgment that powerful life-science AI is dual-use: it can accelerate drug discovery but could also lower barriers to biological threats. Pairing capability with a defense plan is an attempt to get ahead of that tension. Domain-specific models can raise accuracy and reliability on specialized tasks compared with general models, but their errors are harder for non-experts to catch — a real concern in fields tied directly to drug development and clinical work, where correctness and verifiability matter most. Quantitative performance details remain limited for now, so real-world evaluation is still ahead.",
        "key_points_ja": [
            "生命科学特化の専用モデルGPT-Rosalindを強化",
            "生物学的推論・医薬品化学・ゲノミクスに対応",
            "実験ワークフローの設計まで支援を狙う",
            "同日に生物防御(Biodefense)行動計画も公表",
            "強力な生命科学AIは創薬加速と悪用懸念の両刃",
            "定量的な性能値は限定的で実運用評価はこれから"
        ],
        "key_points_en": [
            "Upgraded GPT-Rosalind, a life-sciences-specific model",
            "Biological reasoning, med-chem, genomics expertise",
            "Aims to assist with experimental workflow design",
            "Paired with a same-day Biodefense action plan",
            "Powerful bio-AI is dual-use: cures vs. misuse",
            "Quantitative benchmarks still limited so far"
        ],
    },
    {
        "source": "Hacker News",
        "title": "The Pentagon is running an AI propaganda mill targeting Latin America",
        "title_ja": "Pentagon、中南米を狙うAIプロパガンダ工場を運営",
        "url": "https://theintercept.com/2026/06/02/la-tilde-propaganda-latin-america-pentagon/",
        "hot_take_ja": "「生成AIで偽情報が量産される」は予言じゃなく、もう国家がやっている。米軍が運営する“メディアブランド”La Tildeは、家計記事に軍事プロパガンダを混ぜ、文章はLLM・画像はMidjourneyで量産。崩れた手の指やおかしな建築が逆に正体をバラした。プロパガンダは“スイッチ一つ”の時代に入った。",
        "detail_ja": "The Interceptが、米軍南方特殊作戦軍(SOCSOUTH)が運営するメディアサイト『La Tilde』を暴いた。2026年初頭に立ち上がり、スペイン語・英語で中南米の読者を狙う“軍の情報発信プラットフォーム”だ。サイトには署名・編集部・スタッフ表記がなく、「数十人のフリーランス制作者を雇っている」と称する。手口は巧妙で、一見無害な個人ファイナンス記事に米軍プロパガンダを織り交ぜる。例として、ベネズエラのマドゥロ大統領拘束とされる「Operation Absolute Resolve」を称賛する記事や、パナマでの米軍演習を“侵略でなく主権強化だ”と描く記事が挙がっている。コンテンツの多くはLLMで生成され、画像はMidjourney製で、崩れた文字や建築の破綻といった生成AI特有のアラが残っていた。エクアドル、エルサルバドル、ガイアナ、ホンジュラス、ジャマイカ、パナマ、ペルー向けの国別版も計画され、各国の読者に合わせて内容を調整する設計だ。サイト最下部には「La Tildeは米国政府予算で公的に資金提供される国際メディア組織の製品」と小さく開示があるが、トップページからは分かりにくい。生成AIが国家による情報操作のコストを劇的に下げ、“スイッチ一つ”で多言語プロパガンダを量産できる現実を示す事例だ。デザインはコロンビアのデジタルマーケ企業Antpackに外注されていた。",
        "detail_en": "The Intercept exposed 'La Tilde,' a media site run by U.S. Special Operations Command South (SOCSOUTH). Launched in early 2026, it targets Latin American audiences in Spanish and English as a 'military messaging platform.' It carries no bylines, masthead, or staff list, yet claims to employ dozens of freelance creators. The tactic is to blend seemingly harmless personal-finance articles with U.S. military propaganda — for instance, pieces praising 'Operation Absolute Resolve' (the alleged abduction of Venezuelan president Nicolás Maduro) and framing U.S. military exercises in Panama as sovereignty-strengthening rather than invasive. Much of the content appears LLM-generated, and the imagery is from Midjourney, complete with tell-tale artifacts like garbled text and architectural errors. Country-specific editions are planned for Ecuador, El Salvador, Guyana, Honduras, Jamaica, Panama, and Peru, each tailored to local readers. A small disclosure at the page bottom states the site is 'a product of an international media organization publicly funded from the budget of the United States Government,' but it's easy to miss. The case shows how generative AI slashes the cost of state information operations, letting actors spin up multilingual propaganda 'at the flip of a switch.' The site's design was subcontracted to Antpack, a Colombian digital-marketing firm.",
        "key_points_ja": [
            "米軍SOCSOUTHが運営するメディア『La Tilde』",
            "家計記事に軍事プロパガンダを混入",
            "文章はLLM、画像はMidjourneyで量産",
            "崩れた指・建築などAI生成のアラが残存",
            "7カ国向けの国別版を計画",
            "資金源開示はあるが目立たない場所に小さく"
        ],
        "key_points_en": [
            "'La Tilde' media site run by U.S. SOCSOUTH",
            "Mixes propaganda into harmless finance articles",
            "Text via LLMs, images via Midjourney",
            "Tell-tale AI artifacts: garbled text, bad buildings",
            "Country editions planned for 7 nations",
            "Funding disclosure exists but is tiny and buried"
        ],
    },
    {
        "source": "Hacker News",
        "title": "Did Claude increase bugs in rsync?",
        "title_ja": "Claudeはrsyncのバグを増やしたのか?——炎上を統計検証",
        "url": "https://alexispurslane.github.io/rsync-analysis/",
        "hot_take_ja": "「AIがrsyncをダメにした」というSNS発の炎上を、誰かがちゃんとデータで殴り返した。36リリースを重み付き深刻度で分析した結果、Claude関与リリースの悪化は統計的に有意でない(p=46〜74%)。むしろ歴代最悪のリリースはClaudeコミット0件。スプリアスな相関に乗った集団パニックの典型例だ。",
        "detail_ja": "「ClaudeのAIコーディングがrsyncのコード品質を落とし、バグを増やした」というSNS発の主張が炎上した件を、ある書き手が統計的に検証した。対象はrsync v2.4.6〜v3.4.3の36リリース。指標は『10コミットあたりの深刻度重み付きバグ数(sev/10c)』で、各バグの実世界影響をAIモデルが0〜100で採点し、正規化して集計した。結果、Claude関与リリース(v3.4.2は0.00、v3.4.3は3.29 sev/10c)は四分位範囲の両側に分かれ、過去平均2.95に対しClaude平均は1.65と、むしろ低かった。統計検定でも、正確順列検定でp値46%、フィッシャー正確検定で74%と、Claudeリリースが歴史的中央値を有意に超える傾向は見られなかった。さらに皮肉なことに、史上最悪のリリースv3.4.1(39.39 sev/10c)はClaudeコミットがゼロだったのに、炎上は起きなかった。著者は、炎上の発端はSNSユーザーが見た“スプリアス(見せかけ)な相関”で、それがGitHubやHNで増幅されたと指摘する。実際に変更が増えた本当の理由は、LLMが発見した脆弱性に対応するセキュリティ作業の増加であって、Claude由来の品質劣化ではなかった、と結論づけている。AIコーディングの是非を語る前に、まずデータを見ろ——という冷静さの教訓でもある。",
        "detail_en": "After a social-media claim that Claude-assisted coding had degraded rsync's code quality and increased bugs went viral, one writer put it to a statistical test. The dataset: 36 rsync releases from v2.4.6 to v3.4.3. The metric: severity-weighted bugs per 10 commits (sev/10c), where each bug's real-world impact was scored 0–100 by an AI model, then normalized and aggregated. The result: Claude-involved releases (v3.4.2 at 0.00, v3.4.3 at 3.29 sev/10c) landed on opposite sides of the interquartile range, and the Claude mean of 1.65 was actually below the historical mean of 2.95. Statistical tests agreed — an exact permutation test gave p=46% and Fisher's exact test p=74%, showing no significant tendency for Claude releases to exceed the historical median. Ironically, the worst release ever, v3.4.1 at 39.39 sev/10c, had zero Claude commits yet generated no outrage. The author argues the furor began with a 'spurious correlation' spotted by a social-media user and amplified through GitHub and Hacker News; the real driver of increased churn was security work addressing LLM-discovered vulnerabilities, not quality problems introduced by Claude. It's a tidy lesson in checking the data before judging AI coding.",
        "key_points_ja": [
            "「Claudeがrsyncのバグを増やした」炎上を統計検証",
            "36リリースを深刻度重み付き指標(sev/10c)で分析",
            "Claude平均1.65 < 歴代平均2.95でむしろ低い",
            "順列検定p=46%、フィッシャー検定p=74%で有意差なし",
            "史上最悪v3.4.1はClaudeコミット0件だった",
            "炎上の正体はスプリアスな相関の増幅"
        ],
        "key_points_en": [
            "Stat test of the 'Claude broke rsync' outrage",
            "36 releases analyzed via severity-weighted sev/10c",
            "Claude mean 1.65 < historical mean 2.95",
            "Permutation p=46%, Fisher p=74%: no significance",
            "Worst-ever release v3.4.1 had zero Claude commits",
            "The furor traces to an amplified spurious correlation"
        ],
    },
    {
        "source": "Hacker News",
        "title": "Google employees internally share memes about how its AI sucks",
        "title_ja": "Google社員、自社AIのダメさを内部ミームで共有",
        "url": "https://www.404media.co/google-employees-internally-share-memes-about-how-its-ai-sucks/",
        "hot_take_ja": "ピチャイは「新コードの75%はAI生成」と誇るが、実際に使う現場の社員は内部ミームで自社AIを笑っている。売る側と使う側の温度差が、ここまで露骨に漏れたのは珍しい。AIコード生成の“過大広告”に、内部から最も手厳しいツッコミが入った形だ。",
        "detail_ja": "404 Mediaが、Google社内で従業員が自社AIの出来の悪さを揶揄するミームを共有している、と報じた。背景にあるのは、CEOのスンダー・ピチャイが「社内の新規コードの75%がAI生成」と公言していること。だが、実際にそのツールを使う現場のエンジニアたちは、コード生成の質に懐疑的で、内部チャンネルでミームにして笑っているという。記事が突くのは、経営陣が描く“AI礼賛”の対外ナラティブと、現場社員の本音との大きな断絶だ。AIを「売る・宣伝する」側ではなく、毎日「使う」側の人々が効果に疑問を呈しているという事実は、業界全体に広がる「AI生成コード」の誇大宣伝が、現実の性能や信頼性とどれだけ噛み合っているのかという疑問を突きつける。とくに「コードの何%がAI製か」という指標は、生産性や品質の証明にはならず、むしろ宣伝文句として独り歩きしやすい。記事本体はペイウォール内で、具体的なミーム例の詳細までは確認できないが、大手テック各社が掲げるAI効果の主張に、内部から冷や水が浴びせられた象徴的な一件と言える。AIコーディングは便利だが万能ではない——その温度感を、ほかならぬ最前線の開発者が示している。",
        "detail_en": "404 Media reported that Google employees are internally sharing memes mocking the quality of the company's own AI. The backdrop is CEO Sundar Pichai's public claim that '75 percent of all new code at the company is AI-generated.' Yet the engineers actually using those tools are skeptical of the code-generation quality and are turning that skepticism into memes on internal channels. The article highlights a stark gap between leadership's celebratory, outward-facing AI narrative and the rank-and-file's lived experience. When the people who use these systems daily — not the ones marketing them — question their effectiveness, it raises real doubts about whether the industry-wide hype around AI-generated code matches actual performance and reliability. The much-cited 'what percent of code is AI-written' figure, in particular, proves neither productivity nor quality and tends to take on a life of its own as a talking point. The full article sits behind a paywall, so specific meme examples aren't fully visible, but it stands as a telling case of internal pushback against the AI-impact claims big tech keeps making. AI coding is useful but not magic — and it's the frontline developers themselves making that point.",
        "key_points_ja": [
            "Google社員が自社AIを揶揄する内部ミームを共有",
            "ピチャイ「新コードの75%はAI生成」と公言",
            "使う側の現場は生成コードの質に懐疑的",
            "対外ナラティブと現場の本音に大きな断絶",
            "「AI製コードの割合」は品質の証明にならない",
            "AIコーディング過大広告への内部からの冷や水"
        ],
        "key_points_en": [
            "Google staff share memes mocking their own AI",
            "Pichai claims 75% of new code is AI-generated",
            "Daily users are skeptical of code-gen quality",
            "Big gap between PR narrative and ground truth",
            "'% of code AI-written' proves neither speed nor quality",
            "Internal pushback against AI-code hype"
        ],
    },
]

raw["highlights"] = highlights
raw["stats"] = {
    "arxiv_count": len(src["arxiv"]),
    "hn_count": len(src["hn"]),
    "reddit_count": len(src.get("reddit", [])),
    "github_count": len(src["github"]),
    "blogs_count": len(src["blogs"]),
    "total": len(src["arxiv"]) + len(src["hn"]) + len(src.get("reddit", [])) + len(src["github"]) + len(src["blogs"]),
    "highlights": len(highlights),
}

out = ROOT / f"data/{DATE}.json"
json.dump(raw, open(out, "w"), ensure_ascii=False, indent=2)
print(f"Wrote {out}")
print("stats:", raw["stats"])
