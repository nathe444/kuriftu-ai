from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingService:
    def __init__(self, model_name="all-mpnet-base-v2"):
        # This model outputs 768-dimensional embeddings
        self.model = SentenceTransformer(model_name)
    
    def get_embedding(self, text):
        """Generate embedding for a single text"""
        return self.model.encode(text)
    
    def get_embeddings(self, texts):
        """Generate embeddings for a list of texts"""
        return self.model.encode(texts)
    
    def calculate_similarity(self, embedding1, embedding2):
        """Calculate cosine similarity between two embeddings"""
        return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

# Create a singleton instance
embedding_service = EmbeddingService()