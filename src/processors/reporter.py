import re
import string
import math
from collections import Counter
from .base_processor import BaseProcessor

class Reporter(BaseProcessor):
    def __init__(self, client, severity, source_lang, target_lang):
        super().__init__(client, severity, source_lang, target_lang)
        self.text = ""

    def output_suffix(self):
        return "report"

    def process_sections(self, sections):
        # Concatenate all sections into one big text
        full_text = []
        for sec in sections:
            section_full_text = (sec["title"] + "\n" + sec["content"]).strip()
            full_text.append(section_full_text)
        self.text = "\n\n".join(full_text)

        report = self.generate_report(self.text)
        return [report]

    def generate_report(self, text):
        words = self._tokenize_words(text)
        word_count = len(words)
        
        # Basic stats
        estimated_pages = word_count / 300 if word_count > 0 else 0
        sentences = self._split_into_sentences(text)
        sentence_count = len(sentences) if sentences else 0
        
        # Word frequencies
        word_counter = Counter([w.lower() for w in words if w])
        top_words_20 = word_counter.most_common(20)
        
        # Words with minimum lengths
        top_4_letter_words = self._get_top_words_by_length(word_counter, 4, 20)
        top_5_letter_words = self._get_top_words_by_length(word_counter, 5, 20)

        # Sentence frequencies
        # If all sentences are unique (count == 1), we'll note that.
        cleaned_sentences = [s.strip() for s in sentences if s.strip()]
        sentence_counter = Counter(cleaned_sentences)
        top_sentences = sentence_counter.most_common(20)
        all_sentences_unique = all(count == 1 for _, count in sentence_counter.items())

        # Letter frequencies
        letters = [ch.lower() for ch in text if ch.isalpha()]
        letter_counter = Counter(letters)
        top_letters = letter_counter.most_common(20)

        # Additional writer-friendly stats:
        # 1. Average sentence length (in words)
        avg_sentence_length = (word_count / sentence_count) if sentence_count > 0 else 0.0
        
        # 2. Lexical diversity (type-token ratio)
        unique_word_count = len(set([w.lower() for w in words]))
        lexical_diversity = (unique_word_count / word_count) if word_count > 0 else 0.0
        
        # 3. Flesch Reading Ease (approximation)
        #   Flesch Reading Ease = 206.835 - (1.015 * ASL) - (84.6 * ASW)
        #   ASL = Average Sentence Length (words per sentence)
        #   ASW = Average Syllables per Word (very rough approximation)
        asl = avg_sentence_length
        asw = self._average_syllables_per_word(words)
        flesch_score = 206.835 - (1.015 * asl) - (84.6 * asw)

        # 4. Most common bigrams (two-word combinations)
        bigrams = self._get_bigrams(words)
        bigram_counter = Counter(bigrams)
        top_bigrams = bigram_counter.most_common(10)

        # Build the report
        report_lines = []
        report_lines.append("===== DOCUMENT REPORT =====")
        report_lines.append(f"Total word count: {word_count}")
        report_lines.append(f"Estimated pages (300 words/page): {estimated_pages:.2f}")
        report_lines.append(f"Total sentence count: {sentence_count}")
        report_lines.append(f"Average sentence length (words): {avg_sentence_length:.2f}")
        report_lines.append(f"Lexical diversity (type/token ratio): {lexical_diversity:.2f}")
        report_lines.append(f"Flesch Reading Ease Score: {flesch_score:.2f} (Higher is easier to read)")
        report_lines.append("")
        
        report_lines.append("Top 20 most used words:")
        for w, c in top_words_20:
            report_lines.append(f"{w}: {c}")
        report_lines.append("")

        report_lines.append("Top 20 words (>=4 letters):")
        for w, c in top_4_letter_words:
            report_lines.append(f"{w}: {c}")
        report_lines.append("")
        
        report_lines.append("Top 20 words (>=5 letters):")
        for w, c in top_5_letter_words:
            report_lines.append(f"{w}: {c}")
        report_lines.append("")

        if all_sentences_unique:
            report_lines.append("All sentences are unique and only appear once.")
        else:
            report_lines.append("Top 20 most used sentences:")
            for s, c in top_sentences:
                if c > 1:
                    display_sentence = s if len(s) < 200 else s[:200] + "..."
                    report_lines.append(f"\"{display_sentence}\": {c}")
            # If we filtered out all sentences because they're all count==1, at least we have a note above.
        report_lines.append("")

        report_lines.append("Top 20 most used letters:")
        for ch, c in top_letters:
            report_lines.append(f"{ch}: {c}")
        report_lines.append("")

        report_lines.append("Top 10 most common bigrams:")
        for bg, c in top_bigrams:
            report_lines.append(f"{bg[0]} {bg[1]}: {c}")

        report_lines.append("")
        report_lines.append("===== END OF REPORT =====")
        
        return "\n".join(report_lines)

    def _tokenize_words(self, text):
        words = re.split(r"\W+", text)
        return [w for w in words if w]

    def _split_into_sentences(self, text):
        # This split is naive, but workable for a basic report
        sentences = re.split(r'(?<=[.?!])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    def _get_top_words_by_length(self, word_counter, min_length, top_n):
        # Filter words by minimum length and return top N
        filtered = [(w, c) for w, c in word_counter.items() if len(w) >= min_length]
        filtered.sort(key=lambda x: x[1], reverse=True)
        return filtered[:top_n]
    
    def _average_syllables_per_word(self, words):
        # A very rough approximation: count vowels as syllables
        # This is simplistic and not linguistically accurate.
        vowels = 'aeiou'
        total_syllables = 0
        for w in words:
            # count vowel groups as syllables; naive approach
            w_lower = w.lower()
            syllables = 0
            in_vowel_group = False
            for ch in w_lower:
                if ch in vowels:
                    if not in_vowel_group:
                        syllables += 1
                        in_vowel_group = True
                else:
                    in_vowel_group = False
            total_syllables += syllables
        return (total_syllables / len(words)) if len(words) > 0 else 0.0

    def _get_bigrams(self, words):
        # Return list of (word1, word2) bigrams
        return list(zip(words, words[1:]))

    def build_prompt(self):
        return ""

    def postprocess(self, response, section):
        return response