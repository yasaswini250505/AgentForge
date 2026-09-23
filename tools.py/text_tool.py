# tools/text_tool.py
# Text processing tool with multiple operations.
# Demonstrates: inheritance, @staticmethod, polymorphism via subclasses

from email.mime import text

from core.base_tool import BaseTool

class TextTool(BaseTool):
    """
    Performs text analysis: word count, sentiment, reversal, summary.
    """

    POSITIVE_WORDS = {
    "good","great","excellent","amazing","wonderful","fantastic",
    "superb","best","awesome","love","brilliant","helpful","fast",
    "easy","clean","clear","perfect","happy","success","win",
    }
    NEGATIVE_WORDS = {
    "bad","terrible","awful","worst","horrible","poor","hate",
    "slow","broken","difficult","hard","confusing","fail","error",
    }

    @property
    def name(self):
        return "text_analyser"
    
    @property
    def description(self):
        return "Analyse text: word count, sentiment, keywords, reverse. Input: any text."

    def run(self, input_text):
        """Detect what kind of analysis is needed and run it."""
        lower = input_text.lower()
        if "reverse" in lower or "backwards" in lower:
            return self._reverse(input_text)
        if "sentiment" in lower or "feeling" in lower or "tone" in lower:
            return self._sentiment(input_text)
        if "count" in lower or "words" in lower or "length" in lower:
            return self._word_stats(input_text)
        if "keyword" in lower or "important" in lower:
            return self._keywords(input_text)
        # Default: full analysis
        return self._full_analysis(input_text)

    def _reverse(self, text):
        words = text.split()
        return " ".join(reversed(words))

    def _sentiment(self, text):
        words = text.lower().split()
        pos   = sum(1 for w in words if w.strip(".,!?") in self.POSITIVE_WORDS)
        neg   = sum(1 for w in words if w.strip(".,!?") in self.NEGATIVE_WORDS)
        total = pos + neg
        if total == 0:
            return "Sentiment: Neutral (no strong signals)"
        score = (pos - neg) / total
        label = ("Positive" if score > 0.2 else "Negative" if score < -0.2 else "Neutral")
        return (f"Sentiment: {label} (score={score:.2f}, " f"positive={pos}, negative={neg})")

    def _word_stats(self, text):
        words   = text.split()
        unique  = set(w.lower().strip(".,!?") for w in words)
        avg_len = round(sum(len(w) for w in words) / max(1, len(words)), 1)
        return (f"Words: {len(words)}, Unique: {len(unique)}, " f"Avg length: {avg_len}")
    
    def _keywords(self, text):
        stop = {"the","a","an","and","or","is","was","in","on","at","to","of","be"}
        words = text.lower().split()
        freq = {}
        for w in words:
            clean = w.strip(".,!?;:")
            if clean and clean not in stop and len(clean) > 3:
                freq[clean] = freq.get(clean, 0) + 1
        top5 = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:5]
        return "Keywords: " + ", ".join(f"{w}({c})" for w, c in top5)
    
    def _full_analysis(self, text):
        stats = self._word_stats(text)
        sent  = self._sentiment(text)
        keys  = self._keywords(text)
        return f"{stats} | {sent} | {keys}"

    @staticmethod
    def clean_text(text):
        """Remove extra whitespace and normalise."""
        return " ".join(text.split())