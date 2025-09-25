
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from textstat import flesch_reading_ease, gunning_fog, automated_readability_index
import numpy as np
import pandas as pd

def analyze_thematic_clusters(texts, num_clusters=3):
    """Analyzes thematic clusters in a collection of texts.
    Abordagem Técnica: Topic modeling + clustering.
    Ferramentas: TfidfVectorizer, KMeans (BERTopic/HDBSCAN seriam mais avançados, mas exigem mais setup).
    Métricas: Coerência de tópico (inferida pela distância ao centro do cluster e palavras-chave por tópico).
    
    Args:
        texts (list): Uma lista de textos para analisar.
        num_clusters (int): O número de clusters a serem formados.
    Returns:
        dict: Um dicionário contendo os clusters atribuídos, palavras-chave por tópico.
    """
    if not texts or len(texts) < num_clusters:
        return {"thematic_clusters": [], "topic_keywords": {}}

    vectorizer = TfidfVectorizer(stop_words="english") # Consider language-specific stop words
    X = vectorizer.fit_transform(texts)

    kmeans = KMeans(n_clusters=num_clusters, random_state=0, n_init=10)
    kmeans.fit(X)
    clusters = kmeans.labels_

    # Get top keywords for each cluster
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    topic_keywords = {}
    for i in range(num_clusters):
        top_terms = [terms[ind] for ind in order_centroids[i, :10]]
        topic_keywords[f"cluster_{i}"] = top_terms

    return {
        "thematic_clusters": clusters.tolist(),
        "topic_keywords": topic_keywords,
    }

def analyze_literary_criticism(text):
    """Performs literary criticism analysis (style and structure).
    Abordagem Técnica: Análise de estilo e estrutura.
    Ferramentas: TextStat, Custom rules (para originalidade e estrutura).
    Métricas: Originalidade (conceitual), complexidade (índices de legibilidade).
    
    Args:
        text (str): O texto a ser analisado.
    Returns:
        dict: Um dicionário contendo métricas de complexidade, originalidade e coerência estrutural.
    """
    # Complexidade: Usando índices de legibilidade do TextStat
    flesch_ease = flesch_reading_ease(text)
    gunning_fog_score = gunning_fog(text)
    ari_score = automated_readability_index(text)

    # Originalidade (conceitual): Poderia ser avaliada por desvio de padrões comuns,
    # uso de metáforas, vocabulário único, etc. Aqui, é um valor simulado.
    originality_score = np.random.uniform(0.3, 0.9)

    # Análise de estrutura (conceitual): Poderia envolver a detecção de elementos narrativos,
    # progressão de enredo, desenvolvimento de personagens, etc.
    # Aqui, simulamos uma pontuação de "coerência estrutural".
    structural_coherence_score = np.random.uniform(0.5, 0.95)

    return {
        "literary_complexity_flesch_reading_ease": flesch_ease,
        "literary_complexity_gunning_fog": gunning_fog_score,
        "literary_complexity_ari": ari_score,
        "literary_originality_score": originality_score,
        "literary_structural_coherence_score": structural_coherence_score,
    }

if __name__ == "__main__":
    sample_texts_for_clustering = [
        "The quick brown fox jumps over the lazy dog. Dogs are loyal pets.",
        "Cats love to play with yarn. Felines are independent creatures.",
        "Artificial intelligence is transforming industries. Machine learning is a key component.",
        "The economy is showing signs of recovery. Inflation remains a concern for central banks.",
        "A kitten purred softly on the windowsill. It was a beautiful day.",
        "Deep learning models require vast amounts of data for training."
    ]

    print("\n--- Análise de Clusters Temáticos ---")
    cluster_results = analyze_thematic_clusters(sample_texts_for_clustering, num_clusters=2)
    for key, value in cluster_results.items():
        print(f"  {key}: {value}")

    sample_text_for_criticism = "The moon hung low in the inky sky, a silent sentinel over the slumbering world. Its silver light painted the ancient trees with an ethereal glow, whispering tales of forgotten dreams and distant stars. A profound sense of peace enveloped the observer, a fleeting moment of cosmic connection."
    print("\n--- Análise de Críticas Literárias ---")
    literary_results = analyze_literary_criticism(sample_text_for_criticism)
    for key, value in literary_results.items():
        print(f"  {key}: {value}")

    sample_text_portuguese_for_criticism = "A lua pairava baixa no céu escuro, uma sentinela silenciosa sobre o mundo adormecido. Sua luz prateada pintava as árvores antigas com um brilho etéreo, sussurrando contos de sonhos esquecidos e estrelas distantes. Uma profunda sensação de paz envolvia o observador, um momento fugaz de conexão cósmica."
    print("\n--- Análise de Críticas Literárias (Português - TextStat pode não ser preciso) ---")
    literary_results_portuguese = analyze_literary_criticism(sample_text_portuguese_for_criticism)
    for key, value in literary_results_portuguese.items():
        print(f"  {key}: {value}")


