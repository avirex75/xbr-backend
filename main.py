from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import feedparser

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # autorise tout pour test
    allow_methods=["*"],
    allow_headers=["*"],
)

keywords_by_category = {
    "Finance": ["sogelife"],
    "TMC": ["C2PA", "watermarking"],
    "Cyber": ["phishing", "malware", "cybersécurité"],
    "News": ["BCE", "europe", "économie"]
}

RSS_FEEDS = [
    "https://news.google.com/rss/search?q={}",
    "https://www.bleepingcomputer.com/feed/",
    "https://hnrss.org/frontpage"
]

@app.get("/news")
def get_news():
    results = []
    for category, keywords in keywords_by_category.items():
        for kw in keywords:
            for feed_url in RSS_FEEDS:
                url = feed_url.format(kw) if "{}" in feed_url else feed_url
                parsed = feedparser.parse(url)
                for entry in parsed.entries[:5]:
                    if kw.lower() in entry.title.lower() or kw.lower() in entry.get("summary", "").lower():
                        results.append({
                            "category": category,
                            "title": entry.title,
                            "source": entry.get("source", {}).get("title", "Source inconnue"),
                            "date": entry.get("published", "Date inconnue"),
                            "summary": entry.get("summary", ""),
                            "url": entry.link
                        })
    return results
