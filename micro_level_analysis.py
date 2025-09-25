
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from textstat import flesch_kincaid_grade, sentence_count, char_count, lexicon_count, syllable_count
import spacy
from collections import Counter
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download NLTK data if not already downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model \'en_core_web_sm\'...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def calculate_cohesion(text):
    """Calcula uma métrica simplificada de coesão baseada em repetição de palavras-chave.
    Uma abordagem mais sofisticada usaria cadeias lexicais ou embeddings.
    """
    sentences = sent_tokenize(text)
    if len(sentences) < 2: return 0.0

    stop_words = set(stopwords.words("english"))
    
    total_overlap = 0
    for i in range(len(sentences) - 1):
        words1 = set([w.lower() for w in word_tokenize(sentences[i]) if w.isalpha() and w.lower() not in stop_words])
        words2 = set([w.lower() for w in word_tokenize(sentences[i+1]) if w.isalpha() and w.lower() not in stop_words])
        
        if words1 and words2:
            overlap = len(words1.intersection(words2))
            total_overlap += overlap / min(len(words1), len(words2))
            
    return total_overlap / (len(sentences) - 1) if (len(sentences) - 1) > 0 else 0.0

def get_syntactic_depth(token):
    """Calcula a profundidade sintática de um token em sua árvore de dependência."""
    depth = 0
    current = token
    while current.head != current:
        depth += 1
        current = current.head
    return depth

def analyze_text_micro(text):
    tokens = word_tokenize(text.lower())
    words = [word for word in tokens if word.isalpha()]

    # Granularidade Linguística
    doc = nlp(text)
    num_sentences = len(list(doc.sents))
    avg_sentence_length = sum(len(sent) for sent in doc.sents) / num_sentences if num_sentences > 0 else 0
    
    # Complexidade (usando TextStat)
    flesch_kincaid = flesch_kincaid_grade(text)
    
    # Coesão (métrica simplificada)
    cohesion_score = calculate_cohesion(text)

    # Marcadores Sintáticos
    # Profundidade sintática (profundidade máxima e média de uma árvore de dependência)
    all_depths = []
    for sent in doc.sents:
        for token in sent:
            all_depths.append(get_syntactic_depth(token))
    
    max_syntactic_depth = max(all_depths) if all_depths else 0
    avg_syntactic_depth = sum(all_depths) / len(all_depths) if all_depths else 0

    # Marcadores Léxicos
    # Diversidade Lexical (Type-Token Ratio)
    ttr = len(set(words)) / len(words) if len(words) > 0 else 0
    # Densidade Lexical (usando textstat)
    total_words = len(words)
    unique_words = len(set(words))
    lexical_density = unique_words / total_words if total_words > 0 else 0
    # Frequência de palavras (top 5)
    word_frequencies = Counter(words).most_common(5)

    # Simplified LIWC-like analysis (example: count positive/negative words)
    positive_words = ["good", "great", "happy", "love", "excellent"]
    negative_words = ["bad", "sad", "hate", "terrible", "poor"]
    
    positive_count = sum(1 for word in words if word in positive_words)
    negative_count = sum(1 for word in words if word in negative_words)

    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(text)

    return {
        "linguistic_granularity_sentences": num_sentences,
        "linguistic_granularity_avg_sentence_length": avg_sentence_length,
        "linguistic_complexity_flesch_kincaid": flesch_kincaid,
        "linguistic_cohesion_score": cohesion_score,
        "syntactic_depth_max": max_syntactic_depth,
        "syntactic_depth_avg": avg_syntactic_depth,
        "lexical_markers_ttr": ttr,
        "lexical_markers_density": lexical_density,
        "lexical_markers_top_frequencies": word_frequencies,
        "liwc_positive_words": positive_count,
        "liwc_negative_words": negative_count,
        "sentiment_polarity": sentiment_scores["compound"],
    }

if __name__ == "__main__":
    sample_text = "This is a great sentence. It makes me feel happy. However, some parts are bad. The cat sat on the mat. The mat was green."
    analysis_results = analyze_text_micro(sample_text)
    print("Micro-level Analysis Results:")
    for key, value in analysis_results.items():
        print(f"  {key}: {value}")

    sample_text_portuguese = "Esta é uma ótima frase. Ela me faz sentir feliz. No entanto, algumas partes são ruins. O cachorro correu rapidamente. O cachorro era marrom."
    analysis_results_portuguese = analyze_text_micro(sample_text_portuguese)
    print("\nMicro-level Analysis Results (Portuguese - simplified LIWC and spaCy model for English will not work optimally, cohesion might be less accurate):")
    for key, value in analysis_results_portuguese.items():
        print(f"  {key}: {value}")


