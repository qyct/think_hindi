#!/usr/bin/env python3
"""
Advanced Hindi Words Compiler with real dataset integration
Requires: pip install datasets huggingface_hub requests beautifulsoup4
"""

import os
import sys
import re
from pathlib import Path
from typing import Set, List
import json

try:
    from datasets import load_dataset
    HAS_DATASETS = True
except ImportError:
    HAS_DATASETS = False
    print("Warning: 'datasets' library not installed. Install with: pip install datasets")

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("Warning: 'requests' or 'beautifulsoup4' not installed. Install with: pip install requests beautifulsoup4")

# Configuration
THRAW_DIR = Path(__file__).parent.parent / "thraw"
THRAW_DIR.mkdir(exist_ok=True)

HINDI_UNICODE_START = 0x0900
HINDI_UNICODE_END = 0x097F

class HindiWordsCompiler:
    def __init__(self):
        self.all_words = set()

    def is_hindi_text(self, text: str) -> bool:
        """Check if text contains Hindi characters"""
        return any(HINDI_UNICODE_START <= ord(char) <= HINDI_UNICODE_END for char in text)

    def extract_hindi_words_from_text(self, text: str, min_length: int = 2) -> Set[str]:
        """Extract Hindi words from text"""
        if not text:
            return set()

        # Pattern for Hindi words (Devanagari)
        hindi_pattern = re.compile(r'[\u0900-\u097F]+')
        words = hindi_pattern.findall(text)

        # Filter and clean words
        cleaned_words = set()
        hindi_stopwords = self.get_hindi_stopwords()

        for word in words:
            word = word.strip()
            # Remove punctuation
            word = word.strip('।.,;:?!()[]{}"\'-')

            if (len(word) >= min_length and
                word not in hindi_stopwords and
                not word.isdigit() and
                self.is_hindi_text(word)):
                cleaned_words.add(word)

        return cleaned_words

    def get_hindi_stopwords(self) -> Set[str]:
        """Common Hindi stopwords to exclude"""
        return {
            'और', 'अथवा', 'कि', 'के', 'का', 'की', 'को', 'में', 'पर', 'है', 'हैं',
            'था', 'थे', 'हो', 'होता', 'होती', 'होते', 'यह', 'ये', 'वह', 'वे',
            'कर', 'करता', 'करते', 'करना', 'करने', 'होना', 'होने', 'जा', 'जाता',
            'जाती', 'जाते', 'जाना', 'जाने', 'से', 'तक', 'साथ', 'भी', 'नहीं',
            'हाँ', 'ना', 'एक', 'दो', 'तीन', 'चार', 'पाँच', 'छः', 'सात', 'आठ',
            'नौ', 'दस', 'इस', 'उस', 'जिस', 'जिससे', 'किसी', 'किसीसे', 'कौन',
            'कौनसा', 'क्या', 'कहाँ', 'कब', 'कैसा', 'कैसे', 'कितना', 'कितने',
            'हर', 'हरेक', 'सब', 'सभी', 'कुछ', 'बहुत', 'थोड़ा', 'ज्यादा', 'बाद',
            'पहले', 'बाद में', 'अभी', 'फिर', 'तब', 'जब', 'तब तक', 'जब तक',
            'क्योंकि', 'इसलिए', 'नहीं', 'मात्र', 'ही', 'तो', 'व', 'लेकिन'
        }

    def process_oscar_corpus(self, num_samples: int = 100):
        """Process OSCAR corpus for Hindi"""
        if not HAS_DATASETS:
            print("Skipping OSCAR corpus: datasets library not available")
            return

        try:
            print("Processing OSCAR Corpus...")
            dataset = load_dataset("oscar-corpus/OSCAR-2201", "hi", split="train", streaming=True)

            count = 0
            for item in dataset:
                if count >= num_samples:
                    break

                text = item.get('text', '')
                words = self.extract_hindi_words_from_text(text)
                self.all_words.update(words)

                count += 1
                if count % 10 == 0:
                    print(f"  Processed {count} samples, found {len(self.all_words)} unique words")

        except Exception as e:
            print(f"Error processing OSCAR corpus: {e}")

    def process_wikipedia_dump(self):
        """Process Hindi Wikipedia dump"""
        if not HAS_REQUESTS:
            print("Skipping Wikipedia: requests library not available")
            return

        try:
            print("Processing Hindi Wikipedia...")

            # List of Wikipedia pages to scrape
            pages = [
                "https://hi.wikipedia.org/wiki/%E0%A4%AD%E0%A4%BE%E0%A4%B0%E0%A4%A4",
                "https://hi.wikipedia.org/wiki/%E0%A4%B9%E0%A4%BF%E0%A4%A8%E0%A5%8D%E0%A4%A6%E0%A5%80",
                "https://hi.wikipedia.org/wiki/%E0%A4%B5%E0%A4%BF%E0%A4%9C%E0%A5%8D%E0%A4%9E%E0%A4%BE%E0%A4%A8",
                "https://hi.wikipedia.org/wiki/%E0%A4%B8%E0%A4%BE%E0%A4%B9%E0%A4%BF%E0%A4%A4%E0%A5%8D%E0%A4%AF",
            ]

            for url in pages:
                try:
                    response = requests.get(url, timeout=30)
                    response.raise_for_status()

                    soup = BeautifulSoup(response.content, 'html.parser')
                    # Extract text from paragraphs
                    paragraphs = soup.find_all('p')
                    text = ' '.join([p.get_text() for p in paragraphs])

                    words = self.extract_hindi_words_from_text(text)
                    self.all_words.update(words)

                    print(f"  Found {len(words)} words from {url}")

                except Exception as e:
                    print(f"  Error fetching {url}: {e}")

        except Exception as e:
            print(f"Error processing Wikipedia: {e}")

    def load_sample_words(self) -> Set[str]:
        """Load comprehensive sample Hindi words"""
        sample_words = set()

        # Common words
        common = [
            "नमस्ते", "धन्यवाद", "शुभकामनाएं", "प्रणाम", "स्वागत है", "कृपया", "माफ़ कीजिए",
            "जी हाँ", "जी नहीं", "बिल्कुल", "निश्चित रूप से", "अवश्य", "ज़रूर",
            "समझ गए", "समझ में आया", "मतलब", "उदाहरण", "विधि", "प्रक्रिया",
            "समस्या", "समाधान", "परिणाम", "विचार", "राय", "सुझाव", "सलाह",
            "निर्णय", "योजना", "लक्ष्य", "उद्देश्य", "उपलब्धि", "सफलता", "विफलता",
            "अनुभव", "ज्ञान", "शिक्षा", "प्रशिक्षण", "अभ्यास", "मेहनत", "लगन",
            "ईमानदारी", "सच्चाई", "सत्य", "झूठ", "धोखा", "विश्वास", "भरोसा",
            "प्यार", "प्रेम", "दुस्मन", "मित्रता", "संबंध", "रिश्ता", "ताल्लुकात",
            "खुशी", "गम", "उत्साह", "निराशा", "आशा", "निराश", "संतोष", "असंतोष"
        ]

        # Academic/Technical
        academic = [
            "विज्ञान", "भौतिकी", "रसायन", "जीवविज्ञान", "गणित", "अर्थशास्त्र", "�तिहास",
            "भूगोल", "नागरिकशास्त्र", "राजनीति", "समाजशास्त्र", "मनोविज्ञान", "दर्शन",
            "संस्कृत", "हिंदी", "अंग्रेज़ी", "भाषा", "साहित्य", "काव्य", "गद्य",
            "उपन्यास", "कहानी", "नाटक", "निबंध", "समीक्षा", "संपादन", "प्रकाशन",
            "पत्रकारिता", "संचार", "माध्यम", "प्रसारण", "विज्ञापन", "मार्केटिंग",
            "व्यापार", "उद्योग", "वाणिज्य", "वित्त", "लेखांकन", "प्रबंधन", "प्रशासन",
            "कानून", "न्याय", "अदालत", "वकील", "जज", "पुलिस", "सुरक्षा", "रक्षा"
        ]

        # Technology
        technology = [
            "कंप्यूटर", "प्रोग्रामिंग", "सॉफ्टवेयर", "हार्डवेयर", "इंटरनेट", "वेबसाइट",
            "एप्लिकेशन", "डेटाबेस", "सर्वर", "नेटवर्क", "ब्रॉडबैंड", "वाईफाई",
            "ब्लूटूथ", "मोबाइल", "टेबलेट", "लैपटॉप", "डेस्कटॉप", "प्रिंटर", "स्कैनर",
            "डिजिटल", "इलेक्ट्रॉनिक", "ऑटोमेशन", "रोबोटिक्स", "कृत्रिम बुद्धिमत्ता",
            "मशीन लर्निंग", "डेटा साइंस", "साइबर", "सुरक्षा", "प्राइवेसी", "एन्क्रिप्शन"
        ]

        # Nature/Environment
        nature = [
            "पर्यावरण", "प्रकृति", "पृथ्वी", "आकाश", "जल", "थल", "वायु", "अग्नि",
            "सूर्य", "चंद्रमा", "तारे", "ग्रह", "नक्षत्र", "ब्रह्मांड", "आकाशगंगा",
            "ऋतु", "वसंत", "ग्रीष्म", "वर्षा", "शरद", "शीत", "दिन", "रात", "सुबह",
            "शाम", "समुद्र", "नदी", "तालाब", "झील", "झरना", "पहाड़", "पर्वत",
            "घाटी", "मैदान", "रेगिस्तान", "जंगल", "वन", "उद्यान", "फूल", "पत्ती",
            "पेड़", "पौधा", "जानवर", "पक्षी", "कीट", "मछली", "सर्प", "हिरण"
        ]

        sample_words.update(common)
        sample_words.update(academic)
        sample_words.update(technology)
        sample_words.update(nature)

        return sample_words

    def categorize_and_save(self):
        """Categorize words and save to files"""
        # Ensure we have some words
        if not self.all_words:
            self.all_words = self.load_sample_words()

        word_list = list(self.all_words)

        categories = {
            'common': [],
            'literary': [],
            'technical': [],
            'scientific': [],
            'news': []
        }

        # Categorize based on word characteristics
        for word in word_list:
            word_lower = word.lower()

            # Common words (shorter, everyday)
            if len(word) <= 4:
                categories['common'].append(word)

            # Literary (longer, complex)
            elif len(word) >= 6:
                categories['literary'].append(word)

            # Technical (contains technical patterns)
            elif any(term in word for term in ['तंत्र', 'विधि', 'प्रौद्योगिकी', 'यंत्र', 'साधन', 'कंप्यूटर', 'प्रोग्राम']):
                categories['technical'].append(word)

            # Scientific (contains scientific patterns)
            elif any(term in word for term in ['विज्ञान', 'जीव', 'भौतिक', 'रसायन', 'गणित', 'तारा', 'ग्रह', 'प्रकृति']):
                categories['scientific'].append(word)

            # News/general
            else:
                categories['news'].append(word)

        # Ensure all categories have words
        for category in categories:
            if len(categories[category]) < 10:
                # Add some common words to fill
                categories[category].extend(word_list[:30])

        # Save to files
        for category, words in categories.items():
            filename = THRAW_DIR / f"words_{category}.txt"

            # Remove duplicates and sort
            unique_words = sorted(list(set(words)))

            if unique_words:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(unique_words))

                print(f"✓ Saved {len(unique_words)} words to words_{category}.txt")
            else:
                print(f"✗ No words to save for {category}")

        # Also save a master file
        master_file = THRAW_DIR / "words_all.txt"
        with open(master_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sorted(self.all_words)))

        print(f"✓ Saved {len(self.all_words)} total words to words_all.txt")

    def run(self, use_real_data: bool = False):
        """Run the compilation process"""
        print("=" * 60)
        print("Hindi Words Compiler - Advanced Edition")
        print("=" * 60)

        if use_real_data:
            print("\nFetching real data from sources...")
            self.process_oscar_corpus(num_samples=50)
            self.process_wikipedia_dump()
        else:
            print("\nUsing sample word database...")

        # Add sample words to ensure comprehensive coverage
        sample_words = self.load_sample_words()
        self.all_words.update(sample_words)

        print(f"\nTotal unique words collected: {len(self.all_words)}")

        print("\nCategorizing and saving words...")
        self.categorize_and_save()

        print("\n" + "=" * 60)
        print("Compilation complete!")
        print(f"All files saved to: {THRAW_DIR}")
        print("=" * 60)

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Compile Hindi words from various sources')
    parser.add_argument('--real-data', action='store_true',
                        help='Fetch real data from HuggingFace and Wikipedia (requires libraries)')
    parser.add_argument('--sample-only', action='store_true',
                        help='Use only sample data (no external fetching)')

    args = parser.parse_args()

    compiler = HindiWordsCompiler()

    use_real = args.real_data
    if args.sample_only:
        use_real = False

    compiler.run(use_real_data=use_real)

if __name__ == "__main__":
    main()
