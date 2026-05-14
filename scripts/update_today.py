#!/usr/bin/env python3
"""Update enrichment for 2026-05-15.

Pattern: re-fetch raw, merge new items into existing enriched JSON, refresh highlights.
"""
import json
from pathlib import Path

DATE = "2026-05-15"
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw-2026-05-14.json"
OUT = ROOT / "data" / f"{DATE}.json"

raw = json.loads(RAW.read_text(encoding="utf-8"))
existing = json.loads(OUT.read_text(encoding="utf-8"))

# index existing enriched items by URL
existing_by_url = {}
for src, items in existing.get("sources", {}).items():
    for it in items:
        key = it.get("url") or it.get("id") or it.get("title")
        existing_by_url[key] = it

# Japanese enrichments for NEW items only (keyed by URL or title fragment)
NEW_JA = {
    # ── HN ──
    "https://scottjg.com/posts/2026-05-05-egpu-mac-gaming/": (
        "RTX 5090とM4 MacBook Airの組み合わせはゲームに使えるか",
        "TB5接続のeGPUでM4 MacBook AirにRTX 5090を繋ぎ、macOS上でのゲーミングを実験する記事。Appleシリコン+外付けNVIDIAという禁断の組み合わせがHNでバズった。"
    ),
    "https://www.tomshardware.com/tech-industry/cryptocurrency/bitcoin-trader-recovers-usd400-000-using-claude-ai-after-losing-wallet-password-11-years-ago-bot-tried-3-5-trillion-passwords-before-decrypting-an-old-wallet-backup": (
        "Claudeが3.5兆通りのパスワード試行で40万ドルのBitcoin復元",
        "11年前にパスワードを失った男性が、Claudeに古いウォレットバックアップを解析させ復元に成功。AIによるパターン生成+総当たりという新しい暗号攻撃のユースケース。"
    ),
    "https://arkadiyt.com/2026/05/13/removing-the-modem-and-gps-from_rav4/": (
        "2024年RAV4ハイブリッドからモデムとGPSを物理的に除去した記録",
        "コネクテッドカーのテレメトリ送信を嫌い、ECUを開けてセルラーモジュールとGPSアンテナを物理的に外した詳細な改造記録。プライバシー観点でHNで人気。"
    ),
    "https://arkadiyt.com/2026/05/13/removing-the-modem-and-gps-from-my-rav4/": (
        "2024年RAV4ハイブリッドからモデムとGPSを物理的に除去した記録",
        "コネクテッドカーのテレメトリ送信を嫌い、ECUを開けてセルラーモジュールとGPSアンテナを物理的に外した詳細な改造記録。プライバシー観点でHNで人気。"
    ),
    "https://jpain.io/god-damn-ai-is-making-me-dumb/": (
        "AIが俺をバカにしている — エンジニアの告白",
        "コーディングをAIに任せきりになった結果、自分の問題解決能力・記憶力・集中力が落ちている実感を綴るエッセイ。多くのエンジニアが共感し、HNで議論を呼んでいる。"
    ),
    "https://github.com/DepthFirstDisclosures/Nginx-Rift": (
        "Nginxの新しいエクスプロイトコード公開",
        "Nginxに対する新たな攻撃手法を実証するPoCリポジトリ。AIではないが世界のWebインフラの大半に影響するため緊急性が高くHNトップに。"
    ),
    "https://www.anthropic.com/news/gates-foundation-partnership": (
        "Anthropicとゲイツ財団が2億ドル規模で提携、AIをグローバルヘルスへ",
        "AnthropicとBill & Melinda Gates Foundationが2億ドル規模の戦略提携を発表。Claudeを感染症対策・母子保健・栄養改善などのグローバルヘルス課題に投入する。"
    ),

    # ── Reddit ──
    "https://blocknow.com/anthropic-claude-bitcoin-wallet-recovery/": (
        "Anthropic Claudeが11年前に失われた40万ドルのBitcoinウォレットを復元",
        "Claudeの推論+パスワード生成で巨大候補空間を絞り込み、40万ドルのウォレットを復元したヒューマンストーリー。同じ技術は悪用もできるため両刃の剣。"
    ),
    "https://www.reddit.com/r/artificial/comments/1tbf0p9/the_ai_labs_whose_models_are_eroding_democratic/": (
        "民主主義を蝕むAIラボがそのまま政府に食い込んでいる、という批判",
        "選挙偽情報・世論操作の温床になっているLLMを作る大手AIラボが、同時に政府の規制策定にも入り込んでいる構造的な利益相反を指摘するRedditでの議論。"
    ),
    "https://www.reddit.com/r/artificial/comments/1tco80m/does_anyone_else_feel_most_ai_tooling_is_becoming/": (
        "AIツールはむしろどんどん使いにくくなっていないか？",
        "ChatGPT、Claude、Geminiなど主要AIツールがアップデートのたびに『安全のため断る』『指示を読まない』方向に劣化しているという不満が共有され共感を集めたスレッド。"
    ),

    # ── Blogs ──
    "https://huggingface.co/blog/ibm-granite/granite-embedding-multilingual-r2": (
        "IBM Granite Embedding Multilingual R2: 100M未満で最高水準の多言語埋め込み",
        "IBMがApache 2.0で公開した多言語埋め込みモデル。32Kコンテキスト・パラメータ100M未満ながら、検索品質でこのサイズ帯のSOTAを取った。"
    ),
    "https://openai.com/index/work-with-codex-from-anywhere": (
        "Codexがどこでも動く — ChatGPTモバイルアプリと連携",
        "ChatGPTモバイルアプリからCodexのコーディングタスクをリアルタイムで監視・指示・承認できるように。リモート環境を跨いで作業継続できる新フロー。"
    ),
    "https://openai.com/index/chatgpt-recognize-context-in-sensitive-conversations": (
        "ChatGPTがセンシティブな会話の文脈をより的確に認識",
        "自殺念慮など長期的にリスクが累積する会話パターンをChatGPTがより早く検知し、安全な応答ができるようにする安全アップデートをOpenAIが発表。"
    ),
}

# Merge: for each source in raw, walk items, copy existing JA if present else apply NEW_JA
merged_sources = {}
new_count = 0
for src, items in raw["sources"].items():
    out_items = []
    for it in items:
        key = it.get("url") or it.get("id") or it.get("title")
        if key in existing_by_url:
            prev = existing_by_url[key]
            # carry over JA fields from prev onto fresh raw item (in case raw fields refreshed)
            new_item = dict(it)
            for ja_key in ("title_ja", "summary_ja"):
                if prev.get(ja_key):
                    new_item[ja_key] = prev[ja_key]
            out_items.append(new_item)
        elif key in NEW_JA:
            title_ja, summary_ja = NEW_JA[key]
            new_item = dict(it)
            new_item["title_ja"] = title_ja
            new_item["summary_ja"] = summary_ja
            out_items.append(new_item)
            new_count += 1
        else:
            # unknown new item — keep without JA, just so it doesn't disappear
            out_items.append(it)
            new_count += 1
            print(f"WARN: no JA for [{src}] {it.get('title','')[:80]} ({key})")
    merged_sources[src] = out_items

print(f"Merged. {new_count} new items got fresh JA.")

# ── Refresh highlights ──
# Reuse existing highlights 0,1,2,4 (still strong); replace [3] Meta morale with
# Anthropic × Gates Foundation $200M partnership — bigger, more directly AI.
prev_h = existing["highlights"]

def find_item(src, url):
    for it in merged_sources.get(src, []):
        if it.get("url") == url:
            return it
    return None

gates_item = find_item("hn", "https://www.anthropic.com/news/gates-foundation-partnership")

new_highlight_gates = {
    "source": "hn",
    "title": gates_item["title"] if gates_item else "Anthropic forms $200M partnership with the Gates Foundation",
    "title_ja": "Anthropicとゲイツ財団が2億ドルで提携、ClaudeをグローバルヘルスへAI投入",
    "url": "https://www.anthropic.com/news/gates-foundation-partnership",
    "hot_take_ja": "AIの『次の用途』は雑談やコード生成ではなく、地球規模の公衆衛生という宣言。Anthropicが2億ドルでゲイツ財団と組み、Claudeを感染症・母子保健・栄養問題に投入する。フロンティアAIの正当性をビジネスではなく社会インパクトで証明しに行く動きとして、業界の物語を大きく書き換える可能性。",
    "detail_ja": "AnthropicとBill & Melinda Gates Foundationが2億ドル規模の戦略パートナーシップを発表した。中身は単純な寄付ではなく、Claudeをグローバルヘルス課題に応用する共同プログラムで、感染症の発見・対応、母子保健、栄養、低所得国の医療従事者教育などが対象になる。技術面では、現場の臨床ガイドライン・公衆衛生データへのRAG、現地語対応、限られたインターネット環境でも動かせる軽量デプロイなどが想定される。商業AIラボがフロンティアモデルを大規模に公益用途へ投入する例としては最大級で、AIの正当性証明（社会的ライセンス）の取り合いがOpenAI・Google DeepMindとの間で本格化する号砲とも読める。一方で『フロンティアAIラボが公衆衛生の方針決定にどこまで踏み込んでよいか』『途上国データの主権』『現地の医療職を支援するのか置換するのか』といった倫理面の論点も同時に立ち上がる。短期的にはClaudeを使うNGOやWHO系プロジェクトが増え、中期的には『AI for Global Health』が独立した投資カテゴリになる可能性が高い。",
    "detail_en": "Anthropic and the Bill & Melinda Gates Foundation announced a $200M strategic partnership aimed at applying Claude to global health problems including infectious disease detection and response, maternal and child health, nutrition, and the training of frontline health workers in low-income countries. The collaboration is structured as a multi-year program rather than a one-off grant, with technical workstreams that likely include RAG over clinical guidelines and public-health datasets, multilingual support for local languages, and lightweight deployment that can survive intermittent connectivity. This is one of the largest commitments yet by a frontier AI lab to public-interest deployment of its flagship model, and it reframes the industry narrative from pure commercial competition to social-license competition with OpenAI and Google DeepMind. At the same time it raises sharp questions: how much influence should a frontier lab have over public-health policy, who owns the data generated in low-income settings, and does this augment or displace already-stretched local clinicians. In the short term expect a wave of NGO and WHO-adjacent projects standardizing on Claude; over the next year 'AI for Global Health' is likely to harden into a distinct funding category.",
    "key_points_ja": [
        "Anthropic×ゲイツ財団、2億ドル規模の戦略提携",
        "Claudeを感染症対策・母子保健・栄養に投入",
        "途上国の医療従事者教育・現地語対応も射程",
        "フロンティアラボの『社会的ライセンス』獲得競争へ",
        "途上国データの主権・倫理面の論点も同時発生",
        "AI for Global Healthが独立カテゴリ化する号砲"
    ],
    "key_points_en": [
        "Anthropic × Gates Foundation: $200M multi-year deal",
        "Claude targeted at infectious disease, MCH, nutrition",
        "Includes training frontline health workers in LMICs",
        "Marks frontier labs racing for social license, not just revenue",
        "Raises data-sovereignty and clinician-displacement concerns",
        "Likely catalyst for 'AI for Global Health' as a category"
    ]
}

# Update other highlights with minor refinements where helpful.
# [4] Bitcoin recovery — refresh detail to reflect that Tom's Hardware now reports 3.5 trillion passwords tried (a striking number worth surfacing).
def refresh_bitcoin(h):
    h = dict(h)
    h["hot_take_ja"] = "Claudeが3.5兆通りものパスワード候補を生成・試行し、11年眠っていた40万ドルのBitcoinウォレットを開けた話。AIが個人の『過去の自分』を救うという新しいユースケースであると同時に、同じ手法は他人のウォレットを狙う側にも使えるという両刃の現実をくっきり示した一件。"
    h["detail_ja"] = "ある男性は11年前、ハイになっていた時にBitcoinウォレットのパスワード（一部）を書き留め損ね、40万ドル相当のBTCにアクセスできなくなっていた。男性は本人の当時のクセ・好きなフレーズ・記憶している部分パターンをClaudeに伝え、Claudeはそれを元に膨大な候補パスワードを生成。最終的に約3.5兆通りを試行した結果、古いウォレットバックアップを復号できたとTom's Hardwareなどが報じている。技術的にはClaudeは『暗号解読』を直接行ったわけではなく、本人特有のパスワード生成戦略（先頭大文字、末尾数字、特定の置換、よく使う単語など）を文脈に沿って優先順位付きで列挙する『候補生成器』として機能した。これにGPUベースの試行が組み合わさることで、ブルートフォースでは現実的でない空間を実用時間で攻略できる。重要なのは、同じ手法は他人のウォレットや漏洩済みパスワードハッシュを狙う攻撃側にも使えることで、AI×総当たりが暗号資産保管のセキュリティモデルを根本から見直させる可能性がある。"
    h["detail_en"] = "A man who lost access to ~$400K in BTC eleven years ago — after failing to fully record his wallet password during a 'high' episode — recovered it with help from Anthropic's Claude. He shared his personal password habits, favorite phrases and partial fragments he still remembered; Claude generated prioritized candidate passwords reflecting his personal generation strategy (capitalization, trailing digits, character substitutions, favored words). Combined with GPU-accelerated trials, Tom's Hardware reports roughly 3.5 trillion candidates were attempted before the wallet backup was decrypted. Technically Claude was not breaking cryptography; it was acting as a personalized, context-aware candidate generator that makes an otherwise intractable brute-force tractable. The exact same recipe also works in the opposite direction — against other people's wallets or leaked password hashes — which has serious implications for how we think about long-tail crypto-asset custody and password-only security."
    h["key_points_ja"] = [
        "11年眠った40万ドルのBitcoinウォレットを復元",
        "Claudeが本人のクセを学び候補パスワードを優先列挙",
        "Tom's Hardware報道では試行回数は約3.5兆通り",
        "AIは『暗号解読』ではなく『人格化された候補生成器』",
        "GPU試行と組み合わせると非現実空間が現実時間に",
        "悪用も可能で、暗号資産保管モデル見直しを迫る"
    ]
    h["key_points_en"] = [
        "$400K BTC recovered after 11 years of lockout",
        "Claude learned the owner's personal password habits",
        "Tom's Hardware: ~3.5 trillion candidates tried",
        "Claude acted as a personalized candidate generator, not a cryptanalyst",
        "GPU brute force made the intractable space tractable",
        "Same trick weaponizes for attackers — rethink crypto custody"
    ]
    return h

new_highlights = [
    prev_h[0],                  # Claude knows it's being tested
    prev_h[1],                  # Altman GOP scrutiny
    prev_h[2],                  # Agentic weight-update friends
    new_highlight_gates,        # NEW: Anthropic × Gates Foundation
    refresh_bitcoin(prev_h[4])  # Bitcoin recovery, refreshed
]

existing["sources"] = merged_sources
existing["highlights"] = new_highlights

# update stats
stats = {}
for k, items in merged_sources.items():
    stats[k] = len(items)
existing["stats"] = stats

OUT.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT}")
print(f"Highlights: {len(new_highlights)}")
for i, h in enumerate(new_highlights):
    print(f"  [{i}] {h.get('source')}: {h.get('title','')[:80]}")
