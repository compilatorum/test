
import pandas as pd
from scripts.evaluation_pipeline.data_collection import load_model_and_tokenizer, collect_data
from scripts.evaluation_pipeline.micro_level_analysis import analyze_text_micro
from scripts.evaluation_pipeline.meso_level_analysis import analyze_text_meso
from scripts.evaluation_pipeline.macro_level_analysis import analyze_text_macro
from scripts.evaluation_pipeline.benchmark_correlation import correlate_with_benchmarks
from scripts.evaluation_pipeline.universal_psychometrics import derive_model_profile, simulate_human_profile, integrate_profiles
from scripts.evaluation_pipeline.autoregenerative_feedback import provide_autoregenerative_feedback
from scripts.evaluation_pipeline.symbiotic_reports import load_all_evaluation_data, generate_dynamic_dashboard_summary, generate_longitudinal_report, generate_self_evolution_curves

def run_full_evaluation_pipeline():
    print("Iniciando o Pipeline de Avaliação Completo...")

    # 1. Coleta de Dados
    print("\n--- Etapa 1: Coleta de Dados ---")
    tokenizer, model = load_model_and_tokenizer()
    collected_data = collect_data(model, tokenizer)
    collected_df = pd.DataFrame(collected_data)
    print(f"Coletados {len(collected_df)} amostras de dados.")
    collected_df.to_csv("collected_model_outputs.csv", index=False)

    # 2. Análise Multinível
    print("\n--- Etapa 2: Análise Multinível ---")
    analysis_results = []
    for index, row in collected_df.iterrows():
        text = row["model_output"]
        micro_analysis = analyze_text_micro(text)
        meso_analysis = analyze_text_meso([text]) # Meso expects a list of texts
        macro_analysis = analyze_text_macro(text)
        
        # Combine all analysis results for this output
        combined_analysis = {
            **row.to_dict(),
            **micro_analysis,
            "meso_sentence_embeddings": meso_analysis["sentence_embeddings"],
            "meso_average_pairwise_cosine_similarity": meso_analysis["semantic_similarity_avg_pairwise_cosine"],
            "meso_lexical_chain_cohesion_score": meso_analysis["lexical_chain_cohesion_score"],
            "meso_coherence_score": meso_analysis["semantic_coherence_gensim_c_v"],
            **macro_analysis
        }
        analysis_results.append(combined_analysis)
    
    analysis_df = pd.DataFrame(analysis_results)
    analysis_df.to_csv("analysis_results.csv", index=False)
    print("Análise multinível concluída e salva em analysis_results.csv.")

    # 3. Correlação com Benchmarks
    print("\n--- Etapa 3: Correlação com Benchmarks ---")
    benchmark_correlation_results = correlate_with_benchmarks(analysis_df)
    # In a real scenario, you might want to save these results or integrate them into analysis_df

    # 4. Psicometria Universal
    print("\n--- Etapa 4: Psicometria Universal ---")
    human_profile = simulate_human_profile()
    model_profile = derive_model_profile(analysis_df)
    integrated_profiles = integrate_profiles(model_profile, human_profile)
    # You might want to save integrated_profiles for later use

    # 5. Feedback Autoregenerativo
    print("\n--- Etapa 5: Feedback Autoregenerativo ---")
    # For feedback, we need a summary of evaluation metrics. Let's create a dummy one for now.
    # In a real system, `analysis_df` would be processed to create this summary.
    evaluation_summary_for_feedback = pd.DataFrame({
        "overall_alignment": [integrated_profiles["overall_alignment"]],
        "lexical_richness_ttr": [analysis_df["lexical_markers_ttr"].mean()],
        "sentiment_polarity": [analysis_df["sentiment_polarity"].mean()],
        "bbq_bias_score_race": [benchmark_correlation_results["bbq_results"]["bias_score_race"]],
        "factual_accuracy": [analysis_df["factual_accuracy"].mean() if "factual_accuracy" in analysis_df.columns else 0.85] # Placeholder
    })
    feedback_suggestions = provide_autoregenerative_feedback(evaluation_summary_for_feedback)

    # 6. Relatórios Simbióticos
    print("\n--- Etapa 6: Relatórios Simbióticos ---")
    # The symbiotic reports script will load its own dummy data for now, or could be updated to use analysis_df
    # For a full integration, `load_all_evaluation_data` would be updated to use the generated CSVs.
    symbiotic_data = load_all_evaluation_data() # This loads dummy data for now
    generate_dynamic_dashboard_summary(symbiotic_data)
    generate_longitudinal_report(symbiotic_data)
    generate_self_evolution_curves(symbiotic_data)

    print("\nPipeline de Avaliação Completo Concluído!")

if __name__ == "__main__":
    run_full_evaluation_pipeline()


