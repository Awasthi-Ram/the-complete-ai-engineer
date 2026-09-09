import os
import re

targets = [
    ('book_builder/ch03_ai_toolchain.html', 'numpy_strides_diagram.png', ['Strided Offset', 'Memory Layout', 'NumPy']),
    ('book_builder/ch11_linear_algebra.html', 'svd_geometry_diagram.png', ['Singular Value Decomposition', 'SVD', 'Low-Rank']),
    ('book_builder/ch12_calculus_autograd.html', 'autograd_dag_diagram.png', ['Automatic Differentiation', 'Autograd', 'Computational Graph']),
    ('book_builder/ch15_convex_optimization.html', 'optimization_ravine_diagram.png', ['Momentum', 'Condition Number', 'Gradient Descent']),
    ('book_builder/ch26_svm.html', 'svm_margin_kernel_diagram.png', ['Margin', 'Support Vector', 'Kernel']),
    ('book_builder/ch210_reinforcement_learning.html', 'rl_agent_environment.jpg', ['Markov Decision Process', 'Reinforcement Learning', 'MDP']),
    ('book_builder/ch31_perceptron_xor.html', 'xor_linear_separability_diagram.png', ['XOR', 'Perceptron', 'Linear']),
    ('book_builder/ch33_backprop_scratch.html', 'backprop_matrix_flow_diagram.png', ['Backpropagation', 'Chain Rule', 'Matrix']),
    ('book_builder/ch35_normalization_regularization.html', 'normalization_cubes_diagram.png', ['Normalization', 'BatchNorm', 'LayerNorm']),
    ('book_builder/ch41_cnns_resnets.html', 'resnet_block_diagram.png', ['ResNet', 'Residual', 'Skip']),
    ('book_builder/ch42_segmentation_unet.html', 'unet_architecture_diagram.png', ['U-Net', 'Segmentation', 'Contracting']),
    ('book_builder/ch44_diffusion_models.html', 'diffusion_process_diagram.png', ['Diffusion', 'Forward', 'Reverse']),
    ('book_builder/ch45_vit_mae.html', 'vit_architecture_diagram.png', ['Vision Transformer', 'ViT', 'Patch']),
    ('book_builder/ch55_lora_qlora.html', 'lora_architecture_diagram.png', ['LoRA', 'Low-Rank', 'Adapter']),
    ('book_builder/ch58_langgraph_agents.html', 'langgraph_swarm_diagram.png', ['LangGraph', 'Multi-Agent', 'StateGraph']),
    ('book_builder/ch510_llm_serving_vllm.html', 'paged_attention_diagram.png', ['PagedAttention', 'KV-Cache', 'vLLM']),
    ('book_builder/ch64_triton_serving.html', 'triton_architecture_diagram.png', ['Triton', 'Dynamic Batch', 'Serving']),
    ('book_builder/ch71_recsys_twotower.html', 'two_tower_recsys_diagram.png', ['Two-Tower', 'Retrieval', 'Recommendation']),
    ('book_builder/ch73_edge_ai_quantization.html', 'quantization_mapping_diagram.png', ['Quantization', 'INT8', 'Scale']),
    ('book_builder/ch81_mcp_standard.html', 'mcp_topology_diagram.png', ['Model Context Protocol', 'MCP', 'Architecture'])
]

for fpath, img, keywords in targets:
    if not os.path.exists(fpath):
        print(f"MISSING: {fpath}")
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    headings = re.findall(r'<h[234][^>]*>(.*?)</h[234]>', text)
    matched = None
    for kw in keywords:
        for h in headings:
            clean_h = re.sub(r'<[^>]+>', '', h)
            if kw.lower() in clean_h.lower():
                matched = h
                break
        if matched:
            break
    clean_matched = re.sub(r'<[^>]+>', '', matched) if matched else "NO MATCH"
    # Print safe ascii
    safe_m = clean_matched.encode('ascii', 'replace').decode()
    print(f"{os.path.basename(fpath)} -> {safe_m}")
