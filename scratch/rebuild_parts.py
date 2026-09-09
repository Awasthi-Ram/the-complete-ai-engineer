# scratch/rebuild_parts.py
import os, sys, re

parts_definition = {
    2: {
        'chapters': [
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
        ]
    },
    3: {
        'chapters': [
            'ch31_perceptron_xor.html',
            'ch32_mlp_activations.html',
            'ch33_backprop_scratch.html',
            'ch34_deep_optimization.html',
            'ch35_normalization_regularization.html',
            'ch36_pytorch_production.html',
            'ch37_jax_functional_dl.html',
            'ch38_rnns_lstms.html'
        ]
    },
    4: {
        'chapters': [
            'ch41_cnns_resnets.html',
            'ch42_segmentation_unet.html',
            'ch43_vaes_gans.html',
            'ch44_diffusion_models.html',
            'ch45_vit_mae.html',
            'ch46_audio_whisper.html',
            'ch47_nlp_embeddings.html'
        ]
    },
    5: {
        'chapters': [
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
}

for part_num, conf in parts_definition.items():
    old_part_file = f'book_builder/part{part_num}.html'
    with open(old_part_file, 'r', encoding='utf-8') as f:
        old_content = f.read()

    # Extract part header (everything before the first <div class="chapter")
    first_ch_idx = old_content.find('<div class="chapter"')
    header = old_content[:first_ch_idx].strip()

    # Extract capstone project (from <div class="project-section"> that has "Hands-On Capstone Project")
    capstone_match = re.search(r'(<!-- =*[\r\n\s]*HANDS-ON CAPSTONE PROJECT[\s\S]*|<div class="project-section">[\s\S]*?<span class="project-tag">Hands-On Capstone Project[\s\S]*$)', old_content)
    if capstone_match:
        capstone = capstone_match.group(0).strip()
    else:
        # Fallback: search for last <div class="project-section">
        last_proj_idx = old_content.rfind('<div class="project-section">')
        capstone = old_content[last_proj_idx:].strip()

    # Read each chapter file
    chapter_contents = []
    for ch in conf['chapters']:
        ch_path = f'book_builder/{ch}'
        with open(ch_path, 'r', encoding='utf-8') as f:
            ch_data = f.read().strip()
            chapter_contents.append(ch_data)
        print(f'Part {part_num}: Included {ch} ({len(ch_data):,} chars)')

    # Assemble new part content
    new_part_content = header + '\n\n' + '\n\n'.join(chapter_contents) + '\n\n' + capstone + '\n'

    with open(old_part_file, 'w', encoding='utf-8') as f:
        f.write(new_part_content)

    print(f'==> Successfully rebuilt {old_part_file} ({len(new_part_content):,} chars, {os.path.getsize(old_part_file):,} bytes)')
