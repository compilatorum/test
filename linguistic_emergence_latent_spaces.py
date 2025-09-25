
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE # t-SNE for visualization, not direct metric
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer # Added for generating embeddings for latent space analysis

# For Change Point Detection (conceptual, using a simple statistical approach)
def detect_linguistic_emergence(time_series_data, window_size=5, threshold=0.1):
    """Detects linguistic emergence (new patterns) in time-series data.
    Abordagem Técnica: Detecção de ponto de mudança (simplificado).
    Ferramentas: Numpy.
    Métricas: Taxa de inovação (número de pontos de mudança).
    
    Args:
        time_series_data (np.array): Uma série temporal de dados (e.g., métrica linguística ao longo do tempo).
        window_size (int): Tamanho da janela para calcular a média e o desvio padrão.
        threshold (float): Multiplicador do desvio padrão para detectar um ponto de mudança.
    Returns:
        dict: Um dicionário contendo a taxa de inovação e os pontos de mudança detectados.
    """
    if len(time_series_data) < window_size * 2:
        return {"innovation_rate": 0, "change_points": []}

    change_points = []
    innovation_rate = 0
    for i in range(len(time_series_data) - window_size):
        current_window = time_series_data[i : i + window_size]
        next_point = time_series_data[i + window_size]
        
        # Simple change detection: if the next point deviates significantly from the window mean
        if np.std(current_window) > 0 and np.abs(next_point - np.mean(current_window)) > threshold * np.std(current_window):
            change_points.append(i + window_size)
            innovation_rate += 1
            
    return {"innovation_rate": innovation_rate, "change_points": change_points}

def reverse_engineer_patterns(original_embeddings, reconstructed_embeddings):
    """Simulates reverse engineering of patterns using autoencoders.
    Abordagem Técnica: Decomposição de padrões (via comparação de embeddings).
    Ferramentas: (Simulado, mas em um cenário real, autoencoders LSTM seriam usados).
    Métricas: Reconstrução accuracy (similaridade de cosseno entre embeddings originais e reconstruídos).
    
    Args:
        original_embeddings (np.array): Embeddings originais.
        reconstructed_embeddings (np.array): Embeddings reconstruídos (e.g., por um autoencoder).
    Returns:
        dict: Um dicionário contendo a acurácia da reconstrução.
    """
    if len(original_embeddings) != len(reconstructed_embeddings) or len(original_embeddings) == 0:
        return {"reconstruction_accuracy": 0.0}

    # Calculate cosine similarity between original and reconstructed embeddings
    # A higher average similarity indicates better reconstruction accuracy.
    similarities = [cosine_similarity(orig.reshape(1, -1), recon.reshape(1, -1))[0][0]
                    for orig, recon in zip(original_embeddings, reconstructed_embeddings)]
    
    reconstruction_accuracy = np.mean(similarities)
    return {"reconstruction_accuracy": reconstruction_accuracy}

def analyze_latent_spaces(texts, model_name="all-MiniLM-L6-v2"):
    """Analyzes latent spaces using dimensionality reduction techniques.
    Abordagem Técnica: Embeddings hierárquicos.
    Ferramentas: Sentence-BERT (para embeddings), PCA, t-SNE, UMAP (PCA e t-SNE para demonstração).
    Métricas: Distância semântica (visualizada nos espaços reduzidos).
    
    Args:
        texts (list): Uma lista de textos para gerar embeddings e analisar o espaço latente.
        model_name (str): Nome do modelo Sentence-BERT para gerar embeddings.
    Returns:
        dict: Um dicionário contendo os componentes PCA e t-SNE para visualização da distância semântica.
    """
    if not texts or len(texts) < 2:
        return {"pca_components": [], "tsne_components": []}

    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts)

    # PCA for linear dimensionality reduction
    pca = PCA(n_components=min(2, embeddings.shape[1]))
    pca_components = pca.fit_transform(embeddings)

    # t-SNE for non-linear dimensionality reduction (good for visualization)
    # Note: t-SNE is computationally intensive for large datasets
    tsne_components = []
    if embeddings.shape[0] > 1 and embeddings.shape[1] > 1 and embeddings.shape[0]-1 > 1:
        try:
            # tsne = TSNE(n_components=2, random_state=0, perplexity=min(embeddings.shape[0]-1, 30))
            # tsne_components = tsne.fit_transform(embeddings)
            tsne_components = [] # Temporarily disable TSNE due to segmentation fault
        except ValueError as e:
            print(f"Could not compute t-SNE: {e}")
            tsne_components = []

    return {
        "pca_components": pca_components.tolist(),
        "tsne_components": tsne_components.tolist() if isinstance(tsne_components, np.ndarray) else tsne_components
        # Semantic distance is implicitly represented by the distances in these reduced spaces
    }

if __name__ == "__main__":
    # Exemplo para Emergência Linguística
    # Simulando uma série temporal de alguma métrica linguística (e.g., complexidade)
    np.random.seed(42)
    linguistic_metric_series = np.concatenate([
        np.random.normal(0.5, 0.1, 20), # Stable period
        np.random.normal(0.8, 0.1, 10), # Shift to new pattern
        np.random.normal(0.6, 0.05, 15) # Another stable period
    ])
    emergence_results = detect_linguistic_emergence(linguistic_metric_series)
    print("\n--- Análise de Emergência Linguística ---")
    for key, value in emergence_results.items():
        print(f"  {key}: {value}")

    # Exemplo para Engenharia Reversa
    # Simulando embeddings originais e reconstruídos
    original_embs = np.random.rand(10, 50) # 10 embeddings de 50 dimensões
    reconstructed_embs = original_embs + np.random.normal(0, 0.1, (10, 50)) # Com algum ruído
    re_results = reverse_engineer_patterns(original_embs, reconstructed_embs)
    print("\n--- Análise de Engenharia Reversa ---")
    for key, value in re_results.items():
        print(f"  {key}: {value}")

    # Exemplo para Espaços Latentes
    sample_texts_for_latent_space = [
        "The cat sat on the mat.",
        "A dog barked loudly.",
        "Artificial intelligence is a complex field.",
        "Machine learning is a subfield of AI.",
        "The sun is shining brightly today."
    ]
    latent_space_results = analyze_latent_spaces(sample_texts_for_latent_space)
    print("\n--- Análise de Espaços Latentes ---")
    for key, value in latent_space_results.items():
        print(f"  {key}: {value}")


