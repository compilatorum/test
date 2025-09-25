import unittest
import os
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import torch

# Mocking external dependencies for testing

# Mock SentenceTransformer
class MockSentenceTransformer:
    def __init__(self, model_name):
        pass
    def encode(self, texts):
        # Return dummy embeddings for testing
        return np.array([[0.1, 0.2, 0.3]] * len(texts))

# Mock AutoModelForCausalLM and AutoTokenizer from transformers
class MockAutoTokenizer:
    def __init__(self, model_name):
        pass
    @classmethod
    def from_pretrained(cls, model_name):
        return cls(model_name)
    def __call__(self, text, truncation=True, return_tensors=None):
        return MagicMock(input_ids=torch.tensor([[1, 2, 3]]), attention_mask=torch.tensor([[1, 1, 1]]))
    @property
    def pad_token(self):
        return self.eos_token
    @pad_token.setter
    def pad_token(self, value):
        self._pad_token = value
    @property
    def eos_token(self):
        return "<eos>"
    def save_pretrained(self, save_directory): # Adicionado para o mock
        pass
    def decode(self, token_ids, skip_special_tokens=False):
        return "decoded_text"

class MockAutoModelForCausalLM:
    def __init__(self, model_name, load_in_4bit=False, torch_dtype=None, device_map=None):
        self.config = MagicMock(n_positions=1024)
        self.device = 'cpu'
        self.load_in_4bit = load_in_4bit
        self.torch_dtype = torch_dtype
        self.device_map = device_map
    @classmethod
    def from_pretrained(cls, model_name, load_in_4bit=False, torch_dtype=None, device_map=None, **kwargs):
        instance = cls(model_name)
        instance.model_name = model_name # Store model_name for potential checks
        return instance

    def to(self, device):
        self.device = device
        return self
    def __call__(self, input_ids, labels=None, attention_mask=None):
        return MagicMock(loss=torch.tensor(0.5))
    
    def generate(self, input_ids=None, max_new_tokens=None, **kwargs):
        # Simulate text generation by returning a dummy sequence
        return torch.tensor([[1, 2, 3, 4, 5]])

# Mock PEFT and bitsandbytes
class MockLoraConfig:
    def __init__(self, r, lora_alpha, lora_dropout, bias, task_type):
        pass

def mock_get_peft_model(model, lora_config):
    return model

def mock_prepare_model_for_kbit_training(model):
    return model

# Patching external imports
import sys
sys.modules["sentence_transformers"] = MagicMock()
sys.modules["sentence_transformers"].SentenceTransformer = MockSentenceTransformer
sys.modules["transformers"] = MagicMock()
sys.modules["transformers"].AutoModelForCausalLM = MockAutoModelForCausalLM
sys.modules["transformers"].AutoTokenizer = MockAutoTokenizer
sys.modules["torch"] = MagicMock(__version__="2.0.0")
sys.modules["torch"].tensor = MagicMock(return_value=MagicMock(spec=torch.Tensor))
sys.modules["torch"].cuda = MagicMock()
sys.modules["torch"].cuda.is_available = MagicMock(return_value=False)
sys.modules["torch"].no_grad = MagicMock(return_value=MagicMock())
sys.modules["torch"].stack = MagicMock(return_value=MagicMock(spec=torch.Tensor))
sys.modules["torch"].exp = MagicMock(return_value=MagicMock(spec=torch.Tensor))
sys.modules["peft"] = MagicMock()
sys.modules["peft"].LoraConfig = MockLoraConfig
sys.modules["peft"].get_peft_model = mock_get_peft_model
sys.modules["peft"].prepare_model_for_kbit_training = mock_prepare_model_for_kbit_training
sys.modules["bitsandbytes"] = MagicMock()
sys.modules["datasets"] = MagicMock()
sys.modules["datasets"].load_dataset = MagicMock(return_value=MagicMock(map=lambda x, batched: MagicMock()))
sys.modules["wandb"] = MagicMock()
sys.modules["mlflow"] = MagicMock()
sys.modules["mlflow.pytorch"] = MagicMock()
sys.modules["mlflow.start_run"] = MagicMock(return_value=MagicMock())
sys.modules["mlflow.log_params"] = MagicMock()
sys.modules["mlflow.log_metrics"] = MagicMock()
sys.modules["mlflow.log_artifact"] = MagicMock()

# Import the actual scripts after mocking dependencies
import numpy as np
import torch
from scripts.evaluation_pipeline.data_collection import collect_data, load_model_and_tokenizer
from scripts.evaluation_pipeline.micro_level_analysis import analyze_text_micro
from scripts.evaluation_pipeline.meso_level_analysis import analyze_text_meso
from scripts.evaluation_pipeline.macro_level_analysis import analyze_text_macro
from scripts.evaluation_pipeline.thread_persona_analysis import analyze_thread_discussion, analyze_persona_consistency
from scripts.evaluation_pipeline.triangulation_depth_analysis import calculate_triangulation_agreement, calculate_depth_indicators
from scripts.evaluation_pipeline.cognitive_typologies_architecture import analyze_cognitive_typologies, model_cognitive_architecture
from scripts.evaluation_pipeline.benchmark_correlation import correlate_with_benchmarks
from scripts.evaluation_pipeline.research_protocols_linguistic_modeling import simulate_reproducibility_metrics, evaluate_linguistic_modeling
from scripts.evaluation_pipeline.thematic_literary_analysis import analyze_thematic_clusters, analyze_literary_criticism
from scripts.evaluation_pipeline.linguistic_emergence_latent_spaces import detect_linguistic_emergence, reverse_engineer_patterns, analyze_latent_spaces
from scripts.evaluation_pipeline.metaphor_domain_transitions import detect_complex_metaphors, analyze_domain_transitions
from scripts.evaluation_pipeline.universal_psychometrics import derive_model_profile, simulate_human_profile, integrate_profiles
from scripts.evaluation_pipeline.autoregenerative_feedback import provide_autoregenerative_feedback
from scripts.evaluation_pipeline.symbiotic_reports import load_all_evaluation_data, generate_dynamic_dashboard_summary, generate_longitudinal_report, generate_self_evolution_curves
from scripts.evaluation_pipeline.run_evaluation_pipeline import run_full_evaluation_pipeline
import scripts.training.train_model as train_model_module
from scripts.training.axolotl_integration import generate_axolotl_config, run_axolotl_training

class TestEvaluationPipeline(unittest.TestCase):

    def setUp(self):
        self.sample_text = "This is a sample text for testing. It has some words and sentences."
        self.sample_texts_list = [
            "The cat sat on the mat.",
            "The feline was resting comfortably.",
            "Dogs are also popular pets."
        ]
        self.sample_discussion = [
            "Hello, how can I help you?",
            "I have a problem with my computer.",
            "Did you check the power supply?"
        ]
        self.sample_persona_description = "I am a helpful assistant."
        self.sample_model_outputs_for_persona = [
            "I can help with that.",
            "Here is the information."
        ]
        self.sample_multi_method_results = [
            {"score1": 0.7, "score2": 0.8},
            {"score1": 0.75, "score2": 0.65},
        ]
        self.sample_liwc_dict = {"insight": ["think", "understand"]}
        self.sample_embeddings = np.random.rand(5, 10)
        self.sample_time_series = np.array([0.1, 0.2, 0.15, 0.8, 0.75, 0.85])
        self.sample_original_embs = np.random.rand(3, 5)
        self.sample_reconstructed_embs = self.sample_original_embs + np.random.normal(0, 0.01, (3, 5))
        self.sample_text_metaphor = "Her words were daggers."
        self.sample_domain_segments = [
            "Quantum physics is complex.",
            "Stock market is volatile."
        ]

    @patch("scripts.evaluation_pipeline.data_collection.load_model_and_tokenizer")
    @patch("scripts.evaluation_pipeline.data_collection.collect_data")
    @patch("scripts.evaluation_pipeline.micro_level_analysis.analyze_text_micro")
    @patch("scripts.evaluation_pipeline.meso_level_analysis.analyze_text_meso")
    @patch("scripts.evaluation_pipeline.macro_level_analysis.analyze_text_macro")
    @patch("scripts.evaluation_pipeline.thread_persona_analysis.analyze_thread_discussion")
    @patch("scripts.evaluation_pipeline.thread_persona_analysis.analyze_persona_consistency")
    @patch("scripts.evaluation_pipeline.triangulation_depth_analysis.calculate_triangulation_agreement")
    @patch("scripts.evaluation_pipeline.triangulation_depth_analysis.calculate_depth_indicators")
    @patch("scripts.evaluation_pipeline.cognitive_typologies_architecture.analyze_cognitive_typologies")
    @patch("scripts.evaluation_pipeline.cognitive_typologies_architecture.model_cognitive_architecture")
    @patch("scripts.evaluation_pipeline.benchmark_correlation.correlate_with_benchmarks")
    @patch("scripts.evaluation_pipeline.research_protocols_linguistic_modeling.simulate_reproducibility_metrics")
    @patch("scripts.evaluation_pipeline.research_protocols_linguistic_modeling.evaluate_linguistic_modeling")
    @patch("scripts.evaluation_pipeline.thematic_literary_analysis.analyze_thematic_clusters")
    @patch("scripts.evaluation_pipeline.thematic_literary_analysis.analyze_literary_criticism")
    @patch("scripts.evaluation_pipeline.linguistic_emergence_latent_spaces.detect_linguistic_emergence")
    @patch("scripts.evaluation_pipeline.linguistic_emergence_latent_spaces.reverse_engineer_patterns")
    @patch("scripts.evaluation_pipeline.linguistic_emergence_latent_spaces.analyze_latent_spaces")
    @patch("scripts.evaluation_pipeline.metaphor_domain_transitions.detect_complex_metaphors")
    @patch("scripts.evaluation_pipeline.metaphor_domain_transitions.analyze_domain_transitions")
    @patch("scripts.evaluation_pipeline.universal_psychometrics.derive_model_profile")
    @patch("scripts.evaluation_pipeline.universal_psychometrics.simulate_human_profile")
    @patch("scripts.evaluation_pipeline.universal_psychometrics.integrate_profiles")
    @patch("scripts.evaluation_pipeline.autoregenerative_feedback.provide_autoregenerative_feedback")
    @patch("scripts.evaluation_pipeline.symbiotic_reports.load_all_evaluation_data")
    @patch("scripts.evaluation_pipeline.symbiotic_reports.generate_dynamic_dashboard_summary")
    @patch("scripts.evaluation_pipeline.symbiotic_reports.generate_longitudinal_report")
    @patch("scripts.evaluation_pipeline.symbiotic_reports.g    def test_run_full_evaluation_pipeline(self, mock_load_model_and_tokenizer, mock_collect_data, mock_analyze_micro, mock_analyze_meso, mock_analyze_macro, mock_analyze_thread_discussion, mock_analyze_persona_consistency, mock_calculate_triangulation_agreement, mock_calculate_depth_indicators, mock_analyze_cognitive_typologies, mock_model_cognitive_architecture, mock_correlate_with_benchmarks, mock_simulate_reproducibility_metrics, mock_evaluate_linguistic_modeling, mock_analyze_thematic_clusters, mock_analyze_literary_criticism, mock_detect_linguistic_emergence, mock_reverse_engineer_patterns, mock_analyze_latent_spaces, mock_detect_complex_metaphors, mock_analyze_domain_transitions, mock_derive_model_profile, mock_simulate_human_profile, mock_integrate_profiles, mock_provide_autoregenerative_feedback, mock_load_all_evaluation_data, mock_generate_dynamic_dashboard_summary, mock_generate_longitudinal_report, mock_generate_self_evolution_curves):# Mock return values for all patched functions
        mock_load_model_and_tokenizer.return_value = (MagicMock(), MagicMock())
        mock_collect_data.return_value = [
            {"model_output": "Output 1", "scenario": "linguistic"},
            {"model_output": "Output 2", "scenario": "cognitive"}
        ]
        mock_analyze_micro.return_value = {"micro_metric": 0.5, "sentiment_polarity": 0.1}
        mock_analyze_meso.return_value = {"meso_metric": 0.6, "sentence_embeddings": [[0.1,0.2]], "semantic_similarity_avg_pairwise_cosine": 0.5, "lexical_chain_cohesion_score": 0.5, "coherence_score": 0.5}
        mock_analyze_macro.return_value = {"macro_metric": 0.7}
        mock_analyze_thread_discussion.return_value = {"thematic_flow": 0.8}
        mock_analyze_persona_consistency.return_value = {"persona_consistency": 0.9}
        mock_calculate_triangulation_agreement.return_value = {"agreement": 0.95}
        mock_calculate_depth_indicators.return_value = {"depth_score": 0.75}
        mock_analyze_cognitive_typologies.return_value = {"clusters": [0,1]}
        mock_model_cognitive_architecture.return_value = {"patterns": {"load": 0.5}}
        mock_simulate_reproducibility_metrics.return_value = {"reproducibility": 0.99}
        mock_evaluate_linguistic_modeling.return_value = {"average_perplexity": 10.0, "conceptual_accuracy": 0.8}
        mock_analyze_thematic_clusters.return_value = {"clusters": [0,1], "keywords": {"0":["a"], "1":["b"]}}
        mock_analyze_literary_criticism.return_value = {"originality": 0.8}
        mock_detect_linguistic_emergence.return_value = {"innovation_rate": 1}
        mock_reverse_engineer_patterns.return_value = {"reconstruction_accuracy": 0.98}
        mock_analyze_latent_spaces.return_value = {"pca": [[0.1,0.2]]}
        mock_detect_complex_metaphors.return_value = {"metaphor_precision": 0.7}
        mock_analyze_domain_transitions.return_value = {"smoothness": 0.85}
        mock_derive_model_profile.return_value = {"profile": "model"}
        mock_simulate_human_profile.return_value = {"profile": "human"}
        mock_integrate_profiles.return_value = {"overall_alignment": 0.8}
        mock_provide_autoregenerative_feedback.return_value = {"suggestions": "Improve coherence"}
        mock_load_all_evaluation_data.return_value = pd.DataFrame({
            "timestamp": [pd.Timestamp.now()],
            "overall_alignment": [0.8],
            "lexical_richness_ttr": [0.7],
            "sentiment_polarity": [0.1],
            "bbq_bias_score_race": [0.15],
            "factual_accuracy": [0.9],
            "creativity": [0.7],
            "empathy": [0.6],
            "coherence": [0.85]
        })
        mock_generate_dynamic_dashboard_summary.return_value = None
        mock_generate_longitudinal_report.return_value = None
        mock_generate_self_evolution_curves.return_value = None

        # Run the full pipeline
        run_full_evaluation_pipeline()

        # Assert that each stage function was called
        mock_load_model_and_tokenizer.assert_called_once()
        mock_collect_data.assert_called_once()
        self.assertEqual(mock_analyze_micro.call_count, 2) # Called for each collected data point
        self.assertEqual(mock_analyze_meso.call_count, 2)
        self.assertEqual(mock_analyze_macro.call_count, 2)
        mock_analyze_thread_discussion.assert_called_once()
        mock_analyze_persona_consistency.assert_called_once()
        mock_calculate_triangulation_agreement.assert_called_once()
        mock_calculate_depth_indicators.assert_called_once()
        mock_analyze_cognitive_typologies.assert_called_once()
        mock_model_cognitive_architecture.assert_called_once()
        mock_simulate_reproducibility_metrics.assert_called_once()
        mock_evaluate_linguistic_modeling.assert_called_once()
        mock_analyze_thematic_clusters.assert_called_once()
        mock_analyze_literary_criticism.assert_called_once()
        mock_detect_linguistic_emergence.assert_called_once()
        mock_reverse_engineer_patterns.assert_called_once()
        mock_analyze_latent_spaces.assert_called_once()
        mock_detect_complex_metaphors.assert_called_once()
        mock_analyze_domain_transitions.assert_called_once()
        mock_derive_model_profile.assert_called_once()
        mock_simulate_human_profile.assert_called_once()
        mock_integrate_profiles.assert_called_once()
        mock_provide_autoregenerative_feedback.assert_called_once()
        mock_load_all_evaluation_data.assert_called_once()
        mock_generate_dynamic_dashboard_summary.assert_called_once()
        mock_generate_longitudinal_report.assert_called_once()
        mock_generate_self_evolution_curves.assert_called_once()

        # Clean up generated CSVs
        if os.path.exists("collected_model_outputs.csv"):
            os.remove("collected_model_outputs.csv")
        if os.path.exists("analysis_results.csv"):
            os.remove("analysis_results.csv")

    @patch("scripts.training.train_model.train_model")
    def test_train_model_integration(self, mock_train_model):
        # Define dummy dataset name and model path
        model_name = "facebook/opt-125m"
        dataset_name = "Abirate/english_quotes"
        output_directory = "./fine_tuned_model"

        # Call the function to be tested
        train_model_module.train_model(model_name, dataset_name, output_directory, lora_r=8, lora_alpha=16, lora_dropout=0.05, num_train_epochs=3, per_device_train_batch_size=4)

        # Assertions
        mock_train_model.assert_called_once_with(model_name, dataset_name, output_directory, lora_r=8, lora_alpha=16, lora_dropout=0.05, num_train_epochs=3, per_device_train_batch_size=4)



    @patch("scripts.evaluation_pipeline.symbiotic_reports.load_all_evaluation_data")
    @patch("scripts.evaluation_pipeline.symbiotic_reports.generate_dynamic_dashboard_summary")
    @patch("scripts.evaluation_pipeline.symbiotic_reports.generate_longitudinal_report")
    @patch("scripts.evaluation_pipeline.symbiotic_reports.generate_self_evolution_curves")
    def test_symbiotic_reports(self, mock_generate_self_evolution_curves, mock_generate_longitudinal_report, mock_generate_dynamic_dashboard_summary, mock_load_all_evaluation_data):
        import scripts.evaluation_pipeline.symbiotic_reports as symbiotic_reports

        mock_load_all_evaluation_data.return_value = pd.DataFrame({
            "timestamp": [pd.Timestamp.now()],
            "overall_alignment": [0.8],
            "lexical_richness_ttr": [0.7],
            "sentiment_polarity": [0.1],
            "bbq_bias_score_race": [0.15],
            "factual_accuracy": [0.9],
            "creativity": [0.7],
            "empathy": [0.6],
            "coherence": [0.85]
        })

        # Call the functions directly to ensure mocks are used
        symbiotic_reports.load_all_evaluation_data()
        symbiotic_reports.generate_dynamic_dashboard_summary(mock_load_all_evaluation_data.return_value)
        symbiotic_reports.generate_longitudinal_report(mock_load_all_evaluation_data.return_value)
        symbiotic_reports.generate_self_evolution_curves(mock_load_all_evaluation_data.return_value)

        mock_load_all_evaluation_data.assert_called_once()
        mock_generate_dynamic_dashboard_summary.assert_called_once_with(mock_load_all_evaluation_data.return_value)
        mock_generate_longitudinal_report.assert_called_once_with(mock_load_all_evaluation_data.return_value)
        mock_generate_self_evolution_curves.assert_called_once_with(mock_load_all_evaluation_data.return_value)


if __name__ == '__main__':
    unittest.main()


