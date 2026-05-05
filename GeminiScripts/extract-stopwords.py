
# extract-stopwords.py
# started Feb.12,2026
# Google Gemini for Rich W.
# with GitHub Copilot
#
# license MSL.l

import nltk
from nltk.corpus import stopwords
import spacy
from spacy.lang.en import English
from spacy.lang.fr import French
import json
from datetime import datetime


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
    
    # Process English
    en_nltk = sorted(list(nltk_en))
    en_spacy = sorted(list(spacy_en))
    en_in_common = sorted(list(set(nltk_en) & set(spacy_en)))
    en_nltk_unique = sorted(list(nltk_en - spacy_en))
    en_spacy_unique = sorted(list(spacy_en - nltk_en))
    en_distinct = sorted(list({*nltk_en, *spacy_en}))

    # Process French
    fr_nltk = sorted(list(nltk_fr))
    fr_spacy = sorted(list(spacy_fr))
    fr_in_common = sorted(list(set(nltk_fr) & set(spacy_fr)))
    fr_nltk_unique = sorted(list(nltk_fr - spacy_fr))
    fr_spacy_unique = sorted(list(spacy_fr - nltk_fr))
    fr_distinct = sorted(list({*nltk_fr, *spacy_fr}))

    # Export to JSON file
    json_data = {
        "sourceFile": 'extract-stopwords.py',
        "timestamp": datetime.now().isoformat(),
        "english": {
            "nltk": en_nltk,
            "nltk_count": len(en_nltk),
            "spacy": en_spacy,
            "spacy_count": len(en_spacy),
            "in_common": en_in_common,
            "in_common_count": len(en_in_common),
            "nltk_unique": en_nltk_unique,
            "nltk_unique_count": len(en_nltk_unique),
            "spacy_unique": en_spacy_unique,
            "spacy_unique_count": len(en_spacy_unique),
            "distinct": en_distinct,
            "distinct_count": len(en_distinct)
        },
        "french": {
            "nltk": fr_nltk,
            "nltk_count": len(fr_nltk),
            "spacy": fr_spacy,
            "spacy_count": len(fr_spacy),
            "in_common": fr_in_common,
            "in_common_count": len(fr_in_common),
            "nltk_unique": fr_nltk_unique,
            "nltk_unique_count": len(fr_nltk_unique),
            "spacy_unique": fr_spacy_unique,
            "spacy_unique_count": len(fr_spacy_unique),
            "distinct": fr_distinct,
            "distinct_count": len(fr_distinct)
        }
    }
    json_filename = "stop_words_comparison.json"
    with open(json_filename, "w", encoding="utf-8") as jf:
        json.dump(json_data, jf, ensure_ascii=False, indent=2)
    print(f"Success! Lists exported to {json_filename}")

if __name__ == "__main__":
    export_stop_words()
