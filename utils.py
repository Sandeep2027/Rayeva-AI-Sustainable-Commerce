# ==================== utils.py ====================
import json
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
import nltk
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime
import sqlite3
# NLTK setup
try: nltk.data.find('corpora/stopwords')
except: nltk.download("stopwords", quiet=True)
try: nltk.data.find('tokenizers/punkt')
except: nltk.download("punkt", quiet=True)
try: nltk.data.find('sentiment/vader_lexicon')
except: nltk.download("vader_lexicon", quiet=True)

stop_words = set(stopwords.words("english"))
sia = SentimentIntensityAnalyzer()

# ML TRAINING
training_data = [
    ("bamboo spoon reusable eco kitchen", "Kitchenware"),
    ("compostable takeaway food packaging box", "Packaging"),
    ("organic vegan soap natural skincare", "Personal Care"),
    ("recycled office notebook sustainable paper", "Office Supplies"),
    ("organic millet healthy snack food", "Food & Beverage"),
    ("biodegradable cleaning cloth home eco", "Home Essentials")
]
texts = [x[0] for x in training_data]
labels = [x[1] for x in training_data]
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)
model = LogisticRegression(max_iter=200)
model.fit(X, labels)

SUBCATEGORIES = {
    "Kitchenware": "Reusable Kitchen Tools",
    "Packaging": "Eco Food Containers",
    "Personal Care": "Natural Skincare",
    "Office Supplies": "Recycled Paper Goods",
    "Food & Beverage": "Organic Foods",
    "Home Essentials": "Eco Cleaning Products"
}

PRODUCT_CATALOG = [
    {"name": "Bamboo Cutlery Set", "cost": 5, "plastic_saved": 50},
    {"name": "Compostable Box", "cost": 2, "plastic_saved": 30},
    {"name": "Recycled Notebook", "cost": 3, "plastic_saved": 20},
    {"name": "Organic Hamper", "cost": 10, "plastic_saved": 40}
]

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def advanced_keyword_extraction(text):
    text = clean_text(text)
    cv = CountVectorizer(ngram_range=(1,3), stop_words='english')
    matrix = cv.fit_transform([text])
    freqs = zip(cv.get_feature_names_out(), matrix.toarray()[0])
    sorted_terms = sorted(freqs, key=lambda x: x[1], reverse=True)
    important_terms = [term for term, score in sorted_terms if len(term.split()) <= 3 and len(term) > 3][:8]
    boost = ["eco", "organic", "biodegradable", "recycled", "compostable", "vegan"]
    return list(set(important_terms + [w for w in boost if w in text]))[:10]

def sustainability_filters(text):
    text = text.lower()
    rules = {
        "plastic-free": ["plastic free", "no plastic"],
        "compostable": ["compostable"],
        "vegan": ["vegan"],
        "recycled": ["recycled"],
        "biodegradable": ["biodegradable"],
        "organic": ["organic"]
    }
    return [k for k, v in rules.items() if any(word in text for word in v)]

def classify_category(text):
    X_test = vectorizer.transform([text])
    return model.predict(X_test)[0]

def generate_product_module(description):
    primary = classify_category(description)
    sub = SUBCATEGORIES.get(primary, "General Sustainable Goods")
    tags = advanced_keyword_extraction(description)
    filters = sustainability_filters(description)
    result = {"primary_category": primary, "sub_category": sub, "seo_tags": tags, "sustainability_filters": filters}
    conn = sqlite3.connect("data/database.db")
    conn.execute("INSERT INTO products(description,ai_output,created_at) VALUES(?,?,?)",
                 (description, json.dumps(result), str(datetime.now())))
    conn.commit()
    conn.close()
    return result

def generate_proposal_module(company, budget):
    selected = []
    total_cost = 0
    for product in PRODUCT_CATALOG:
        qty = int((budget * 0.25) // product["cost"])
        cost = qty * product["cost"]
        if qty > 0 and total_cost + cost <= budget:
            selected.append({"name": product["name"], "quantity": qty, "unit_cost": product["cost"]})
            total_cost += cost
    plastic_saved = sum(p["quantity"] * next((prod["plastic_saved"] for prod in PRODUCT_CATALOG if prod["name"] == p["name"]), 0) for p in selected)
    sentiment = sia.polarity_scores(company)["compound"]
    tone = "Strong positive sustainability positioning" if sentiment >= 0 else "Improved eco-conscious brand perception"
    result = {
        "recommended_products": selected,
        "total_cost": total_cost,
        "remaining_budget": budget - total_cost,
        "impact_summary": f"Estimated plastic reduction: {plastic_saved} grams. {tone} for {company}."
    }
    conn = sqlite3.connect("data/database.db")
    conn.execute("INSERT INTO proposals(company,budget,ai_output,created_at) VALUES(?,?,?,?)",
                 (company, budget, json.dumps(result), str(datetime.now())))
    conn.commit()
    conn.close()
    return result

def generate_impact_module(order_summary: str):
    items = {}
    for line in order_summary.splitlines():
        match = re.search(r'(?i)(.+?)\s*(?:x|\*|\s)\s*(\d+)', line.strip())
        if match:
            name = match.group(1).strip().lower()
            qty = int(match.group(2))
            items[name] = qty
    total_plastic = 0
    for name, qty in items.items():
        for prod in PRODUCT_CATALOG:
            if name in prod["name"].lower():
                total_plastic += qty * prod["plastic_saved"]
                break
    carbon_avoided = round((total_plastic / 1000) * 2.8, 1)
    local_sourcing = "Supporting local artisans in Kadapa, Andhra Pradesh (68% of products sourced within 150km)"
    human_readable = f"""🌱 Impact Report for your order\n\nYou helped save **{total_plastic} grams** of single-use plastic.\nThis equals **{carbon_avoided} kg** of CO₂ avoided.\n{local_sourcing}\n\nThank you for choosing sustainable commerce!"""
    result = {
        "plastic_saved": total_plastic,
        "carbon_avoided": carbon_avoided,
        "local_sourcing": local_sourcing,
        "human_readable": human_readable
    }
    conn = sqlite3.connect("data/database.db")
    conn.execute("INSERT INTO impacts(order_summary,ai_output,created_at) VALUES(?,?,?)",
                 (order_summary, json.dumps(result), str(datetime.now())))
    conn.commit()
    conn.close()
    return result