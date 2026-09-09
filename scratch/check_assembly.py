# scratch/check_assembly.py
import os, glob

parts_config = {
    0: ['ch01_how_to_learn.html', 'ch02_python_a_to_z.html', 'ch03_ai_toolchain.html', 'ch04_large_scale_data.html'],
    1: ['ch11_linear_algebra.html', 'ch12_calculus_autograd.html', 'ch13_probability_bayes.html', 'ch14_information_theory.html', 'ch15_convex_optimization.html'],
    2: ['ch21_ml_paradigm.html', 'ch22_linear_regression.html', 'ch23_logistic_regression.html', 'ch24_decision_trees.html', 'ch25_random_forests.html', 'ch25b_gradient_boosting.html', 'ch26_svm.html', 'ch27_unsupervised_kmeans_pca.html', 'ch28_feature_engineering.html', 'ch29_model_evaluation.html', 'ch210_reinforcement_learning.html'],
    3: ['ch31_perceptron_xor.html', 'ch32_mlp_activations.html', 'ch33_backprop_scratch.html', 'ch34_deep_optimization.html', 'ch35_normalization_regularization.html', 'ch36_pytorch_production.html', 'ch37_jax_functional_dl.html', 'ch38_rnns_lstms.html'],
    4: ['ch41_cnns_resnets.html', 'ch42_segmentation_unet.html', 'ch43_vaes_gans.html', 'ch44_diffusion_models.html', 'ch45_vit_mae.html', 'ch46_audio_whisper.html', 'ch47_nlp_embeddings.html'],
    5: ['ch51_transformer_architecture.html', 'ch51b_bert_encoders.html', 'ch52_tokenization_huggingface.html', 'ch53_enterprise_rag.html', 'ch54_llamaindex_graphrag.html', 'ch55_lora_qlora.html', 'ch56_alignment_rlhf_dpo.html', 'ch57_langchain_lcel.html', 'ch58_langgraph_agents.html', 'ch59_coding_agents.html', 'ch510_llm_serving_vllm.html'],
    6: ['ch61_experiment_tracking.html', 'ch62_feature_stores.html', 'ch63_containerization_docker.html', 'ch64_triton_serving.html', 'ch65_drift_observability.html'],
    7: ['ch71_recsys_twotower.html', 'ch72_vector_search_scale.html', 'ch73_edge_ai_quantization.html'],
    8: ['ch81_mcp_standard.html', 'ch82_test_time_compute.html', 'ch83_energy_hardware_limits.html']
}

for part_num, chapters in parts_config.items():
    missing = [ch for ch in chapters if not os.path.exists(f'book_builder/{ch}')]
    if missing:
        print(f'Part {part_num} missing files:', missing)
    else:
        print(f'Part {part_num}: all {len(chapters)} chapter files exist.')
