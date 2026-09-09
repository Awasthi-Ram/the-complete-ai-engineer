# scratch/build_all_parts.py
import os, sys

parts_definition = {
    2: [
        'ch21_ml_paradigm.html',
        'ch22_linear_regression.html',
        'ch23_logistic_regression.html',
        'ch24_decision_trees.html',
        'ch25_random_forests.html',
        'ch25b_gradient_boosting.html',
        'ch26_svm.html',
        'ch27_unsupervised_kmeans_pca.html',
        'ch28_feature_engineering.html',
        'ch29_model_evaluation.html',
        'ch210_reinforcement_learning.html'
    ],
    3: [
        'ch31_perceptron_xor.html',
        'ch32_mlp_activations.html',
        'ch33_backprop_scratch.html',
        'ch34_deep_optimization.html',
        'ch35_normalization_regularization.html',
        'ch36_pytorch_production.html',
        'ch37_jax_functional_dl.html',
        'ch38_rnns_lstms.html'
    ],
    4: [
        'ch41_cnns_resnets.html',
        'ch42_segmentation_unet.html',
        'ch43_vaes_gans.html',
        'ch44_diffusion_models.html',
        'ch45_vit_mae.html',
        'ch46_audio_whisper.html',
        'ch47_nlp_embeddings.html'
    ],
    5: [
        'ch51_transformer_architecture.html',
        'ch51b_bert_encoders.html',
        'ch52_tokenization_huggingface.html',
        'ch53_enterprise_rag.html',
        'ch54_llamaindex_graphrag.html',
        'ch55_lora_qlora.html',
        'ch56_alignment_rlhf_dpo.html',
        'ch57_langchain_lcel.html',
        'ch58_langgraph_agents.html',
        'ch59_coding_agents.html',
        'ch510_llm_serving_vllm.html'
    ]
}

for p, chapter_files in parts_definition.items():
    part_path = f'book_builder/part{p}.html'
    with open(part_path, 'r', encoding='utf-8') as f:
        content = f.read()

    first_ch = content.find('<div class="chapter"')
    header = content[:first_ch].strip()

    capstone_pos = content.rfind('<div class="project-section">')
    comment_pos = content.rfind('<!-- ===', 0, capstone_pos)
    if comment_pos != -1 and 'HANDS-ON' in content[comment_pos:capstone_pos]:
        capstone = content[comment_pos:].strip()
    else:
        capstone = content[capstone_pos:].strip()

    chapters_html = []
    for ch_name in chapter_files:
        with open(f'book_builder/{ch_name}', 'r', encoding='utf-8') as ch_f:
            chapters_html.append(ch_f.read().strip())

    assembled_part = header + '\n\n' + '\n\n'.join(chapters_html) + '\n\n' + capstone + '\n'
    with open(part_path, 'w', encoding='utf-8') as out_f:
        out_f.write(assembled_part)

    print(f"[BUILT] Part {p}: {len(chapter_files)} chapters -> {len(assembled_part):,} chars ({os.path.getsize(part_path):,} bytes)")
