ARXIV_CATEGORIES = ["cs.AI", "cs.CL", "cs.CV", "cs.LG", "cs.RO"]
ARXIV_MAX_RESULTS = 50

HN_KEYWORDS = [
    "AI", "artificial intelligence", "machine learning", "deep learning",
    "LLM", "GPT", "Claude", "neural network", "transformer", "diffusion",
    "reinforcement learning", "robotics", "computer vision", "NLP",
    "Anthropic", "OpenAI", "DeepMind", "Gemini", "Llama", "Mistral",
]
HN_MIN_POINTS = 10
HN_MAX_RESULTS = 20

REDDIT_SUBS = ["MachineLearning", "artificial"]
REDDIT_USER_AGENT = "ai-news-daily/1.0 (by /u/pndshch)"
REDDIT_MIN_SCORE = 5
REDDIT_MAX_RESULTS = 20

GITHUB_TRENDING_LANGUAGES = ["", "python", "typescript", "rust"]
GITHUB_MAX_RESULTS = 25

BLOG_FEEDS = {
    "OpenAI": "https://openai.com/blog/rss.xml",
    "Anthropic": "https://www.anthropic.com/rss.xml",
    "Google DeepMind": "https://blog.google/technology/ai/rss/",
    "Meta AI": "https://ai.meta.com/blog/rss/",
    "Hugging Face": "https://huggingface.co/blog/feed.xml",
}
BLOG_LOOKBACK_DAYS = 7

DATA_DIR = "data"
TEMPLATE_FILE = "template.html"
OUTPUT_FILE = "index.html"
MAX_ARCHIVE_DAYS = 14
