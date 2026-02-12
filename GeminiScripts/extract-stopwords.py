
# extract-stopwords.py
# started Feb.12,2026
# Google Gemini for Rich W.
# with GitHub Copilot


import nltk
from nltk.corpus import stopwords
import spacy
from spacy.lang.en import English
from spacy.lang.fr import French
import json


def export_stop_words():
    # 1. Setup NLTK (Download necessary data)
    print("--- Downloading NLTK Stopwords ---")
    nltk.download('stopwords')
    
    # 2. Extract NLTK Lists
    nltk_en = set(stopwords.words('english'))
    nltk_fr = set(stopwords.words('french'))
    
    # 3. Extract spaCy Lists (Using the core language classes)
    # This avoids downloading the heavy 'en_core_web_sm' models
    spacy_en = English().Defaults.stop_words
    spacy_fr = French().Defaults.stop_words
    
    # Export to JSON file
    json_data = {
        "english": {
            "nltk": sorted(list(nltk_en)),
            "spacy": sorted(list(spacy_en)),
            "in_common": sorted(list(set(nltk_en) & set(spacy_en))),
            "nltk_unique": sorted(list(nltk_en - spacy_en)),
            "spacy_unique": sorted(list(spacy_en - nltk_en))
        },
        "french": {
            "nltk": sorted(list(nltk_fr)),
            "spacy": sorted(list(spacy_fr)),
            "in_common": sorted(list(set(nltk_fr) & set(spacy_fr))),
            "nltk_unique": sorted(list(nltk_fr - spacy_fr)),
            "spacy_unique": sorted(list(spacy_fr - nltk_fr))
        }
    }
    json_filename = "stop_words_comparison.json"
    with open(json_filename, "w", encoding="utf-8") as jf:
        json.dump(json_data, jf, ensure_ascii=False, indent=2)
    print(f"Success! Lists exported to {json_filename}")

if __name__ == "__main__":
    export_stop_words()
