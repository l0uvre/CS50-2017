import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""

        self.positives = set()
        self.negatives = set()
        self.tokenizer = nltk.tokenize.TweetTokenizer()
        with open(positives, "r") as f_positives:
            for line in f_positives:
                if line.startswith(";") and line.startswith(""):
                    continue
                else:
                    self.positives.add(line.strip())
        with open(negatives, "r") as f_negatives:
            for line in f_negatives:
                if line.startswith(";") and line.startswith(""):
                    continue
                else:
                    self.negatives.add(line.strip())




    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        tokens = self.tokenizer.tokenize(text)
        score = 0
        for words in tokens:
            if words.lower() in self.positives:
                score += 1
            elif words.lower() in self.negatives:
                score -= 1
            else:
                pass
        return score
