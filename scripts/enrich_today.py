#!/usr/bin/env python3
"""Enrichment for 2026-05-17 (fresh page).

arXiv + blogs in raw-2026-05-17.json are identical to 2026-05-16's set,
so their Japanese translations are reused verbatim from data/2026-05-16.json.
HN/Reddit/GitHub carry many new items, which are translated below.
Five fresh highlights are selected for the day.
"""
import json
from pathlib import Path

DATE = "2026-05-17"
PREV = "2026-05-16"
ROOT = Path(__file__).resolve().parent.parent
SRC_RAW = ROOT / "data" / f"raw-{DATE}.json"
SRC_PREV = ROOT / "data" / f"{PREV}.json"
OUT = ROOT / "data" / f"{DATE}.json"

d = json.loads(SRC_RAW.read_text(encoding="utf-8"))
d["date"] = DATE
prev = json.loads(SRC_PREV.read_text(encoding="utf-8"))

# ─── Reuse prior translations (arxiv by id, others by url) ───
prev_arxiv = {it["id"]: (it.get("title_ja"), it.get("summary_ja"))
              for it in prev["sources"].get("arxiv", [])}
prev_url = {}
for src in ("hn", "reddit", "github", "blogs"):
    for it in prev["sources"].get(src, []):
        if it.get("url"):
            prev_url[it["url"]] = (it.get("title_ja"), it.get("summary_ja"))

# ─── New HN / Reddit / GitHub items (url → title_ja, summary_ja) ───
new_url_map = {
    # HN
    "https://frederickvanbrabant.com/blog/2026-05-15-i-dont-think-ai-will-make-your-processes-go-faster/": (
        "AIは『プロセス』を速くしない——遅さの原因はもっと上流にある",
        "プロジェクトが遅いのは実装が遅いからではなく、要件定義が曖昧だから。AIで実装を高速化しても、詳細を書き出す前工程の作業は消えず場所が移るだけ、と論じるブログ。"),
    "https://www.thestateofbrand.com/news/ai-subscription-time-bomb": (
        "すべてのAIサブスクは企業にとって『時限爆弾』",
        "企業が各部署で無秩序にAIツールを契約する状況を警告する記事。データの所在・契約・ベンダーロックインが管理不能になり、いずれ大きなコストとリスクとして表面化すると指摘。"),
    "https://www.williamangel.net/blog/2026/05/17/offline-llm-energy-use.html": (
        "Apple Siliconでローカル推論する方がOpenRouterより高くつく",
        "MacのApple SiliconでローカルにLLMを動かす電力コストを実測し、OpenRouter経由のクラウドAPI利用と比較。電気代を含めるとローカル実行は必ずしも安くないと示した検証。"),
    "https://daringfireball.net/2026/05/ai_is_technology_not_a_product": (
        "AIは『製品』ではなく『技術』である",
        "John Gruberの論考。AppleはAIを単独の目玉製品として売るのではなく、無線通信のように全製品へ静かに溶け込ませるべきだと主張する。"),
    "https://github.com/tech4bot/rk3562deb": (
        "80ドルのRK3562 AndroidタブレットをDebian Linuxワークステーション化",
        "安価な中華Androidタブレットを改造し、Debian Linuxの実用環境に仕立てたホビープロジェクト。"),
    "https://sfstandard.com/pacific-standard-time/2026/05/15/meta-employee-gets-real-horror-working-right-now/": (
        "Meta社員が語る『いま社内で働く恐怖』",
        "AI競争のプレッシャーやレイオフ不安の中で働くMeta社員の本音を伝えた記事。大手テックの内部で高まるストレスを浮き彫りにする。"),
    "https://arnaud-carre.github.io/2026-05-15-ym-fast-emu/": (
        "CPUを一切使わずAmigaでAtari STの音楽を再生する",
        "AmigaのハードウェアだけでAtari STのYM音源曲を鳴らす、CPU負荷ゼロのレトロハック。"),
    "https://www.businessinsider.com/mistral-ceo-warns-europe-2-years-avoid-us-ai-dependence-2026-5": (
        "Mistral CEO『欧州には米国のAI属国にならない猶予が2年しかない』",
        "仏Mistralのアルチュール・マンシュCEOが、欧州が独自のAI基盤を築かなければ米国のAIに従属する『属国(vassal state)』になると警告。残された時間は約2年だと訴えた。"),
    "https://github.com/AccelerateHS/accelerate": (
        "Accelerate: 高性能配列計算のための組み込み言語",
        "Haskellに埋め込まれた配列計算向けDSL。GPUなど並列ハードウェア向けに高速なコードを生成する。"),
    "https://github.com/alternbits/awesome-cuda-books": (
        "CUDA Books——CUDA学習のための書籍まとめ",
        "GPUプログラミング言語CUDAを学ぶための書籍を集めたリスト。AI計算の基盤技術への関心の高さを示す。"),
    "https://blog.andymasley.com/p/the-ai-water-issue-is-fake": (
        "『AIの水問題』は誇張されている",
        "AIデータセンターの水消費が環境破壊だという言説を、実データで反証するブログ。全米淡水のごく一部に過ぎず、ゴルフ場などと比べても小さいと論じる。"),
    "https://news.ycombinator.com/item?id=48164173": (
        "Ask HN: コンピュータはいつ『楽しくない』ものになったのか",
        "かつてのコンピュータいじりの楽しさが失われたのはいつか、を問うHNの議論スレッド。AI時代の開発体験への複雑な感情も滲む。"),
    "https://opencivics-labs.github.io/dontsurveil.me/c22.html": (
        "Dontsurveil.me——監視に抵抗するための市民向けリソース",
        "デジタル監視に対抗するための情報や手段をまとめた市民向けプロジェクト。"),
    "https://petapixel.com/2026/05/14/someone-shared-a-real-monet-painting-as-ai-and-asked-for-critiques/": (
        "本物のモネを『AI生成』と偽って投稿、批評が殺到",
        "あるユーザーが本物のモネの絵を『AI製』と偽ってXに投稿したところ、何百人もが『AIだから空間表現が破綻している』等と批評。AIへの偏見を炙り出した一件。"),
    "https://www.bbc.com/future/article/20260514-how-hallucinogenic-ibogaine-helps-veterans-overcome-ptsd": (
        "幻覚剤イボガインが退役軍人のPTSD克服を助ける可能性",
        "幻覚作用を持つイボガインがPTSDの治療に有効かもしれない、という退役軍人を対象にした研究の紹介。AIとは別だがHNで広く読まれた。"),
    "https://twitter.com/elonmusk/status/2055277918633562153": (
        "最新のXアルゴリズムがGitHubに公開された",
        "イーロン・マスク氏が、Xの最新の推薦アルゴリズムをGitHubで公開したと告知。SNSのレコメンドの透明性を巡る話題に。"),
    "https://github.com/ztc00/algora-scout/blob/main/POST.md": (
        "Claudeにオープンソースの賞金稼ぎをさせて稼げるか試した",
        "AIエージェントのClaudeにオープンソースのバウンティ(賞金付きIssue)を解かせて収益化できるか実験した記録。AIエージェントの実用性を試す試み。"),
    # Reddit
    "https://www.reddit.com/r/MachineLearning/comments/1tfh2s9/program_misleading_high_school_students_into/": (
        "高校生を誤誘導し『有料で学術不正』に加担させるプログラムへの告発 [議論]",
        "高校生にお金を払わせてML研究の名義参加をさせる、実質的な学術不正を助長するプログラムを問題視するスレッド。研究倫理を巡る議論を呼んだ。"),
    "https://www.reddit.com/r/MachineLearning/comments/1tfv0vh/slop_is_making_me_feel_disconnected_from_ai/": (
        "AI生成の『スロップ』でAI研究から心が離れていく [議論]",
        "粗製乱造のAI生成論文(スロップ)が増え、研究分野への熱意が冷めていくという研究者の本音スレッド。arXivの投稿禁止議論とも地続きの話題。"),
    "https://www.reddit.com/r/artificial/comments/1tfm5ns/a_minicomputer_you_run_from_a_folder_on_your/": (
        "フォルダから動かせて小型LLMを学習できる『ミニコンピュータ』",
        "PC上のフォルダ単位で動き、小さなLLMの学習まで行える自己完結型ツールの紹介投稿。"),
    "https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures": (
        "最近のLLMアーキテクチャの動向: KV共有・mHC・圧縮アテンション [解説]",
        "Sebastian Raschka氏による解説。KVキャッシュ共有や圧縮アテンションなど、近年のLLM構造の効率化トレンドを整理する。"),
    "http://ppc.land/publicis-buys-liveramp-for-2-5-billion-in-agentic-ai-data-play": (
        "Publicis、エージェント型AIデータ戦略でLiveRampを25億ドルで買収",
        "広告大手Publicisがデータ連携企業LiveRampを25億ドルで買収。エージェント型AIに供給する『データ基盤』の確保を狙った動き。"),
    # GitHub
    "https://github.com/tech-leads-club/agent-skills": (
        "agent-skills: AIコーディングエージェント向けの検証済みスキルレジストリ",
        "Claude Code・Cursor・Copilotなどを拡張する、安全性を検証済みのスキル集。プロ用途を意識した配布基盤。"),
    "https://github.com/BigBodyCobain/Shadowbroker": (
        "Shadowbroker: 富豪のジェット機や偵察衛星を追うOSINT統合ツール",
        "プライベートジェットや偵察衛星、地震イベントなどの公開情報を一画面に集約。AIエージェントを接続して未知の相関を見つけられるOSINTツール。"),
    "https://github.com/HKUDS/CLI-Anything": (
        "CLI-Anything: あらゆるソフトを『エージェント・ネイティブ』にする",
        "既存ソフトウェアをCLI経由でAIエージェントから操作可能にするプロジェクト。3.5万スター超を集め急上昇中。"),
    "https://github.com/dograh-hq/dograh": (
        "dograh: オープンソースの音声エージェント・プラットフォーム",
        "音声で対話するAIエージェントを構築するためのオープンソース基盤。"),
    "https://github.com/NirDiamant/agents-towards-production": (
        "agents-towards-production: 本番品質のGenAIエージェント構築チュートリアル",
        "試作から企業導入まで、本番運用に耐えるAIエージェントを作るためのコード重視の実践チュートリアル集。"),
    "https://github.com/knadh/listmonk": (
        "listmonk: 高性能なセルフホスト型ニュースレター/メール配信ツール",
        "単一バイナリで動く、自前運用できる高性能なメーリングリスト管理ソフト。"),
    "https://github.com/KeygraphHQ/shannon": (
        "Shannon Lite: ソースコードを読む自律型ホワイトボックスAIペンテスター",
        "Webアプリ/APIのソースコードを解析して攻撃経路を特定し、実際にエクスプロイトを実行して脆弱性を本番前に証明する自律型AIペネトレーションテスター。"),
    "https://github.com/microsoft/ai-agents-for-beginners": (
        "ai-agents-for-beginners: AIエージェント入門の12レッスン",
        "Microsoftが公開した、AIエージェント構築を学ぶ12回構成の入門教材。6万スター超。"),
    "https://github.com/Light-Heart-Labs/DreamServer": (
        "DreamServer: クラウド不要のローカルAIオールインワン",
        "LLM推論・チャットUI・音声・エージェント・RAG・画像生成を、クラウドもサブスクも無しでローカルに動かす統合ソフト。"),
}

# ─── Apply translations ───
for it in d["sources"].get("arxiv", []):
    tj = prev_arxiv.get(it.get("id"))
    if tj and tj[0]:
        it["title_ja"], it["summary_ja"] = tj

for src in ("hn", "reddit", "github", "blogs"):
    for it in d["sources"].get(src, []):
        url = it.get("url")
        tj = new_url_map.get(url) or prev_url.get(url)
        if tj and tj[0]:
            it["title_ja"], it["summary_ja"] = tj

# ─── Highlights (5 fresh picks for 2026-05-17) ───
d["highlights"] = [
    {
        "source": "hn",
        "title": "I don't think AI will make your processes go faster",
        "title_ja": "AIは『プロセス』を速くしない——遅さの原因はもっと上流にある",
        "url": "https://frederickvanbrabant.com/blog/2026-05-15-i-dont-think-ai-will-make-your-processes-go-faster/",
        "hot_take_ja": "「AIを入れれば速くなる」は、ボトルネックの場所を誤読している。プロジェクトが遅いのは実装が遅いからではなく、何を作るかが曖昧なまま走り出すから。AIは実装を速くしても、その曖昧さを詰める前工程の手間を消してはくれない——むしろそこを直視させる。",
        "detail_ja": "ソフトウェア開発者Frederick Van Brabant氏のブログ記事が、AIによる『プロセス高速化』への期待に冷水を浴びせ、Hacker Newsで約400の支持を集めた。主張の核心は、組織はボトルネックの場所を取り違えている、という指摘だ。プロジェクトが遅いのは多くの場合、コードを書く速度が遅いからではなく、そもそも『何を作るべきか』の問題定義が曖昧なまま着手するからだ、と筆者は言う。例として「販売が完了したらユーザーにメールを送る」といった一見明快な要件を挙げ、実際にはどのメール、どの条件、どの例外、という膨大な確認作業が実装前に必要になることを示す。ここでAIコード生成に話を移し、AIに速く正確なコードを書かせるには「すべての機能とバグ修正を細部まで書き出す」必要があり、それは結局、開発者が昔から求めてきた詳細仕様そのものだと指摘する。つまりAIは作業を消すのではなく、作業の場所をタイムライン上で前にずらすだけだ。筆者は生産管理の古典『ザ・ゴール』を引き、ボトルネックには『予測可能で高品質な入力』を与えるべきだと述べる。結論として、本当の改善はAIという技術的ショートカットではなく、着手前に問題を明確化し、情報と段取りを整えることにあるとする。AIツールを入れる前に、自社の遅さがどこから来ているのかを正しく診断せよ、というメッセージだ。",
        "detail_en": "A blog post by software developer Frederick Van Brabant poured cold water on expectations that AI will speed up processes, drawing roughly 400 upvotes on Hacker News. The core argument is that organizations misidentify where their bottleneck actually is. A project is slow, the author says, usually not because writing code is slow, but because work starts while the definition of what to build is still vague. He uses a seemingly clear requirement — 'send mail to the user once a sale is completed' — to show how much clarification (which email, which conditions, which exceptions) is really needed before coding can begin. Turning to AI code generation, he argues that getting fast, correct code out of AI requires 'writing out every feature and bug fix down to the tiniest detail' — which is exactly the detailed specification developers have always asked for. In other words, AI does not eliminate the work; it merely shifts it earlier in the timeline. The author cites the classic operations book The Goal, noting that bottlenecks should receive 'predictable, high-quality inputs.' His conclusion: real improvement comes not from the technical shortcut of AI but from clarifying the problem and preparing information before work starts. The message is to diagnose where your slowness truly comes from before reaching for an AI tool.",
        "key_points_ja": [
            "AIによるプロセス高速化への期待に反論、HNで約400支持",
            "遅さの原因は実装速度でなく曖昧な問題定義",
            "AIに速く書かせるには結局『詳細仕様』が必要",
            "AIは作業を消さず前工程へ移すだけ",
            "『ザ・ゴール』を引きボトルネックへの良質な入力を重視",
            "ツール導入前に遅さの所在を正しく診断せよ",
        ],
        "key_points_en": [
            "Rebuts AI process-speedup hype; ~400 HN upvotes",
            "Slowness comes from vague problem definition, not coding speed",
            "Fast AI code still requires detailed specifications",
            "AI doesn't remove work — it shifts it upstream",
            "Cites The Goal: feed bottlenecks high-quality inputs",
            "Diagnose the source of slowness before adopting tools",
        ],
    },
    {
        "source": "hn",
        "title": "AI is a technology not a product",
        "title_ja": "AIは『製品』ではなく『技術』である",
        "url": "https://daringfireball.net/2026/05/ai_is_technology_not_a_product",
        "hot_take_ja": "「AppleにはAIの目玉製品が必要」という批判への、John Gruberの反論が鋭い。無線通信に『キラー無線製品』が無いのと同じで、AIもいずれ全製品に溶け込む基盤技術になる。技術そのものを売るのではなく体験に埋め込む——それがAppleのやり方だ、という整理。",
        "detail_ja": "著名なApple系ブロガーJohn Gruber氏が、『AIは製品ではなく技術だ』と題した論考を発表し、Hacker Newsで議論を呼んだ。きっかけは、ジャーナリストSteven Levy氏による「Appleには独自の目立つAI製品が必要だ」という趣旨の主張だ。Gruber氏はこれに真っ向から反論する。Appleの一貫した哲学は、基盤となる技術そのものを宣伝するのではなく、それを魅力的なユーザー体験へ統合することにある、というのが論点だ。例えばiPhoneが成功したのは、タッチスクリーンやネットワーク技術を売り込んだからではなく、モバイル通信の『体験』に集中したからだ。同様に、無線接続はいまやAppleの全製品に当たり前に存在するが、Appleが『キラー無線製品』を発表したことは一度もない——技術が単に至るところへ溶け込んだだけだ。Gruber氏は、AIも同じ軌道をたどると見る。「すべてがある程度AIデバイスになる。いますべてが無線接続デバイスであるのと同じように」。さらに彼は、自律AIエージェントがスマホを置き換えるというLevy氏の未来像を、実現性に乏しい『熱に浮かされた空想』と切り捨てる。2030年になっても人々は配車を電話(音声かタップか)で呼ぶだろうし、より小さなデバイスがカメラや画面や計算力をスマホに依存し続ける限り、スマホを完全に置き換えることはない、と論じる。含意は明快だ。Appleは派手なAI発表を追うのではなく、無線通信でやってきたように、AIを製品ライン全体へ着実に埋め込むべきだ。技術ではなく体験を売る、というAppleの実証済み戦略の再確認である。",
        "detail_en": "Prominent Apple-focused blogger John Gruber published an essay titled 'AI is a technology not a product,' sparking discussion on Hacker News. The trigger was journalist Steven Levy's argument that Apple needs its own distinctive, headline AI product. Gruber pushes back directly. His point is that Apple's consistent philosophy is not to advertise an underlying technology itself, but to integrate it into a compelling user experience. The iPhone succeeded not by selling touchscreens or networking technology, but by focusing on the experience of mobile communication. Likewise, wireless connectivity is now ubiquitous across every Apple product, yet Apple never shipped a 'killer wireless product' — the technology simply became embedded everywhere. Gruber sees AI following the same trajectory: 'Everything is going to be an AI device, to some extent, just like how everything today is a wireless connectivity device.' He further dismisses Levy's vision of autonomous AI agents replacing the phone as an implausible 'fever dream.' In 2030, he argues, people will still hail rides with a phone — by voice or by tapping — and smaller devices will not fully replace the phone as long as they remain tethered to it for cameras, screens, and compute. The implication is clear: rather than chasing flashy AI announcements, Apple should steadily embed AI throughout its product line, just as it did with wireless. It is a restatement of Apple's proven strategy of shipping experiences, not technologies.",
        "key_points_ja": [
            "John Gruberが『AIは製品でなく技術』と論じHNで議論に",
            "『Appleに目玉AI製品が必要』との主張へ反論",
            "無線通信に『キラー製品』が無いのと同じ構図",
            "Appleは技術でなく体験を売るのが一貫した哲学",
            "『すべてがAIデバイスになる』——無線と同じ軌道",
            "AIエージェントがスマホを置き換える未来像には懐疑的",
        ],
        "key_points_en": [
            "Gruber argues 'AI is a technology, not a product'",
            "Rebuts the claim Apple needs a headline AI product",
            "Parallel: there is no 'killer wireless product' either",
            "Apple's philosophy: ship experiences, not technologies",
            "'Everything will be an AI device' — same path as wireless",
            "Skeptical that AI agents will replace the phone",
        ],
    },
    {
        "source": "hn",
        "title": "The AI water issue is fake",
        "title_ja": "『AIの水問題』は誇張されている",
        "url": "https://blog.andymasley.com/p/the-ai-water-issue-is-fake",
        "hot_take_ja": "「AIは水をがぶ飲みする」という話は、ほぼ修辞のために生きている。実際は全米淡水の0.008%。ゴルフ場の方が桁違いに使う。批判するなら正しい数字で——感情的なヘッドラインが環境議論の足を引っ張る、という耳の痛い指摘。",
        "detail_ja": "ブロガーAndy Masley氏が『AIの水問題はフェイクだ』と題した記事を公開し、AIデータセンターの水消費を環境危機として語る言説に、実データで反論してHacker Newsで議論を呼んだ。氏の主張は、AIの水使用量は実際の規模に比べて著しく誇張されている、というものだ。全米レベルで見ると、AIは2023年に米国の総淡水のおよそ0.008%を消費したに過ぎず、これは約2万5千人分の水需要、米国の年間人口増加の約4%に相当する量だ。2030年に使用量が10倍に増えるという強気の予測を当てはめても、AIの消費は全米淡水の0.08%、現在のゴルフ場の水使用の約5%に収まる。重要な内訳として、AIが使うと報じられる水の約8割は、データセンターの直接運用ではなく発電の段階で生じる——つまり他の電力消費産業と本質的に変わらない。地域レベルでも、データセンターは開発協定を通じて複数の地域で水インフラを改善しており、アリゾナのような乾燥地域では『使う水の単位あたりでゴルフ場の50倍の税収』を生むという。個人レベルでは、1人の1日の水フットプリント422ガロンに対し、年間1万回のチャット利用は総消費の30万分の1に過ぎない。Masley氏は、世間のニュース記事が誤解を招くヘッドラインや切り取った統計でデータを意図的に歪めていると批判する。結論は、この『問題』は実体ある環境上の脅威というより、主に修辞的な道具として存在している、というものだ。ただし、これは『どこでも水を気にしなくてよい』という話ではなく、本当に水ストレスの高い特定地域での立地は依然として個別に検討すべき論点として残る。",
        "detail_en": "Blogger Andy Masley published a piece titled 'The AI water issue is fake,' rebutting with hard data the narrative that AI data center water use is an environmental crisis, and it drew discussion on Hacker News. His claim is that AI's water usage is dramatically overstated relative to its actual scale. Nationally, AI consumed roughly 0.008% of total US freshwater in 2023 — equivalent to the water needs of about 25,000 people, or about 4% of annual US population growth. Even applying an aggressive 10x growth projection by 2030, AI would consume only 0.08% of national freshwater, comparable to about 5% of current golf course water use. A key breakdown: about 80% of the water reported as 'used by AI' occurs during electricity generation, not direct data center operation — making it essentially no different from other power-consuming industries. Locally, data centers have improved water infrastructure in several communities through development agreements, and in dry regions like Arizona generate '50x as much tax revenue per unit of water' as golf courses. At the personal level, against an individual's daily water footprint of 422 gallons, 10,000 chatbot prompts a year amount to just 1/300,000th of total consumption. Masley argues that mainstream news articles deliberately distort the data with misleading headlines and cherry-picked statistics. His conclusion is that this 'problem' exists mainly as a rhetorical device rather than a substantive environmental threat. That said, this is not a claim that water never matters anywhere — siting in genuinely water-stressed regions still warrants case-by-case scrutiny.",
        "key_points_ja": [
            "AIの水消費を環境危機とする言説に実データで反論",
            "AIは2023年に全米淡水の約0.008%を消費",
            "10倍成長でも0.08%、ゴルフ場使用の約5%相当",
            "報じられる水の8割は発電段階で生じる",
            "個人の年間1万回チャットは総水消費の30万分の1",
            "誇張ヘッドラインが環境議論を歪めるとの批判",
        ],
        "key_points_en": [
            "Rebuts the AI-water-crisis narrative with hard data",
            "AI used ~0.008% of US freshwater in 2023",
            "Even at 10x growth: 0.08%, ~5% of golf course use",
            "~80% of 'AI water' occurs during power generation",
            "10,000 chats/year = 1/300,000th of personal water use",
            "Argues exaggerated headlines distort the debate",
        ],
    },
    {
        "source": "hn",
        "title": "Someone Shared a Real Monet Painting as AI and Asked for Critiques",
        "title_ja": "本物のモネを『AI生成』と偽って投稿、批評が殺到した一件",
        "url": "https://petapixel.com/2026/05/14/someone-shared-a-real-monet-painting-as-ai-and-asked-for-critiques/",
        "hot_take_ja": "本物のモネに『AI製』のラベルを貼って出したら、何百人もが『空間表現が破綻』『色彩に調和がない』と自信満々に批評した。作品の評価は、絵そのものではなく『誰が描いたか』のラベルで決まる——AI時代の批評バイアスを完璧に可視化した社会実験。",
        "detail_ja": "あるXユーザー(@SHL0MS)が、クロード・モネの有名な『睡蓮』連作の本物の絵を投稿し、それを『AI生成だ』と偽り、さらにXの『Made with AI(AIで作成)』ラベルまで付けた。投稿は、この『AIアート』が本物のモネに比べてなぜ劣るのかを詳しく批評してほしい、と呼びかけるものだった。すると何百人もが嬉々として応じ、「空間的な深みの一貫性がない」「色彩選択が荒い」「感情的な共鳴に欠ける」「水面への光の反射の理解が不十分」といった詳細な分析を次々と投稿した。あるコメントは「深さと色彩選択に統一感がない。木の反射が、空間的な深度やコントラストを無視して睡蓮の葉に滲み出ている」とまで述べた。つまり、世界的名画に対して、人々は『AI製』というラベルを信じた瞬間に欠点を『発見』してしまった。この即席の社会実験は、科学的研究が裏付ける事実を鮮やかに示している。2024年のNature誌の研究では、出自を知らされない参加者はAIアートをむしろ好む一方、AI製だと知らされると——実際の出自に関わらず——評価を下げた。今回の件は、芸術的価値の知覚が、作品そのものの美的価値だけでなく『どう作られたか』という属性に強く依存することを示す。AIが作ったかどうかを人は見抜けるという思い込みと、AIへの先入観の強さの両方を、一枚の名画が暴いてしまった。",
        "detail_en": "An X user (@SHL0MS) posted a genuine painting from Claude Monet's famous 'Water Lilies' series, falsely claimed it was AI-generated, and even tagged it with X's 'Made with AI' label. The post invited people to critique in detail why this 'AI artwork' fell short of a real Monet. Hundreds eagerly obliged, posting elaborate analyses: 'no consistency to the spatial depth,' 'harsh color choices,' 'lacks emotional resonance,' 'inadequate understanding of light reflecting on water.' One commenter wrote: 'There is no cohesion to the depth and color choices. The reflection of the tree bleeds into the lilypads with no regard for spatial depth or contrast.' In other words, faced with a world-famous masterpiece, people 'discovered' flaws the moment they believed the 'AI-made' label. This impromptu social experiment vividly illustrates what scientific research has confirmed. A 2024 Nature study found that participants who were not told the origin actually preferred AI artworks, but rated them lower once told AI had made them — regardless of the true origin. The episode shows that the perception of artistic value depends strongly not just on a work's aesthetic merit but on the attribute of how it was made. A single masterpiece exposed both the assumption that people can spot AI art and the strength of bias against AI.",
        "key_points_ja": [
            "本物のモネ『睡蓮』を『AI生成』と偽ってXに投稿",
            "X公式の『Made with AI』ラベルまで付与",
            "何百人もが『空間表現が破綻』等と詳細に批評",
            "名画でも『AI製』ラベルで欠点を『発見』してしまう",
            "2024年Nature研究: 出自を知ると評価が下がる",
            "作品の評価が『どう作られたか』に強く依存",
        ],
        "key_points_en": [
            "A real Monet 'Water Lilies' posted as 'AI-generated' on X",
            "Even tagged with X's official 'Made with AI' label",
            "Hundreds critiqued 'broken spatial depth' and more",
            "Even a masterpiece gets flaws 'found' under an AI label",
            "2024 Nature study: ratings drop once AI origin is known",
            "Perceived value depends heavily on how a work was made",
        ],
    },
    {
        "source": "hn",
        "title": "Mistral's CEO: Europe has 2 years to stop becoming America's AI 'vassal state'",
        "title_ja": "Mistral CEO『欧州が米国のAI属国にならない猶予は2年』",
        "url": "https://www.businessinsider.com/mistral-ceo-warns-europe-2-years-avoid-us-ai-dependence-2026-5",
        "hot_take_ja": "AIの覇権争いは、もはや企業間ではなく『主権』の問題になった。仏MistralのマンシュCEOは、欧州が自前のモデル・計算基盤を持たなければ米国のAI属国になると警告。残り時間は2年——AIインフラを誰が握るかという、地政学のニュースである。",
        "detail_ja": "フランスのAI企業Mistralの最高経営責任者アルチュール・マンシュ氏が、欧州には米国のAIへの従属を避けるための時間が約2年しか残されていない、と警告し、Hacker Newsで議論を呼んだ。氏が用いた『vassal state(属国)』という強い言葉は、欧州が独自のAI基盤を築けなければ、基盤モデル・計算インフラ・主要なAIサービスのすべてを米国(および中国)の企業に依存する立場に陥る、という危機感を表している。背景には、フロンティアモデルの開発が、巨額の資本・大規模なGPUクラスタ・データを握る一握りの米国企業に集中しているという現実がある。AIが経済・行政・防衛・メディアのインフラとして社会の隅々に組み込まれていく以上、その基盤を外国企業に握られることは、価格・規約・データ主権・規制適用のすべてで欧州が交渉力を失うことを意味する。マンシュ氏の主張は、欧州が自前のモデル開発、計算資源(ソブリン・クラウドやGPU調達)、人材、そして域内市場での採用を、今後2年という短い窓の中で本気で進めなければ、後からの巻き返しは構造的に困難になる、というものだ。Mistral自身が欧州発の数少ない有力AI企業であり、この発言にはポジショントークの側面もある点は割り引いて読む必要がある。とはいえ、AIをめぐる競争が個社の優劣ではなく国家・地域の『主権』の問題として語られ始めたこと自体が、この技術の段階が変わったことを示している。同じ週には米国でAI由来の雇用減やデータセンター反対の世論が報じられており、AIの社会的・地政学的なコストへの議論が各地で同時に強まっている。",
        "detail_en": "Arthur Mensch, CEO of the French AI company Mistral, warned that Europe has only about two years left to avoid dependence on American AI, sparking discussion on Hacker News. His pointed phrase 'vassal state' captures the fear that, without building its own AI foundations, Europe will end up dependent on US (and Chinese) firms for foundation models, compute infrastructure, and key AI services. The backdrop is the reality that frontier model development is concentrated in a handful of US companies that command vast capital, large GPU clusters, and data. As AI becomes embedded throughout society — in the economy, government, defense, and media — having that foundation controlled by foreign firms would mean Europe loses leverage over pricing, terms, data sovereignty, and the reach of its own regulation. Mensch's argument is that Europe must seriously pursue its own model development, compute resources (sovereign cloud and GPU procurement), talent, and adoption within its internal market during this short two-year window, or a later catch-up becomes structurally difficult. It should be read with the caveat that Mistral is itself one of Europe's few significant AI companies, so the statement carries an element of self-interest. Even so, the fact that AI competition is now framed as a matter of national and regional sovereignty rather than corporate rivalry signals that the stage of this technology has shifted. The same week brought US reports of AI-linked job losses and public opposition to data centers, with debate over AI's social and geopolitical costs intensifying in many places at once.",
        "key_points_ja": [
            "Mistral CEOが欧州のAI従属に2年の猶予と警告",
            "『vassal state(属国)』という強い表現を使用",
            "フロンティアモデルは少数の米企業に集中",
            "基盤を外国企業に握られれば交渉力・データ主権を喪失",
            "自前のモデル・計算資源・人材の確保が急務",
            "Mistral自身が当事者でポジショントークの側面も",
        ],
        "key_points_en": [
            "Mistral CEO warns Europe has a 2-year window",
            "Uses the stark term 'vassal state'",
            "Frontier models concentrated in a few US firms",
            "Foreign-controlled base means lost leverage, data sovereignty",
            "Urgent need for own models, compute, and talent",
            "Mistral is an interested party — note the self-interest",
        ],
    },
]

OUT.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT}")
print(f"Highlights: {len(d['highlights'])}")
for src, items in d["sources"].items():
    enriched = sum(1 for it in items if it.get("title_ja"))
    print(f"  {src}: {enriched}/{len(items)} enriched")
