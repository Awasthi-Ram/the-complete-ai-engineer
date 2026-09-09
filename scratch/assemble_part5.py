import os
import re

HEADER = """<!-- ████████████████████████████████████████████████████████████████████████
     PART 5 — TRANSFORMERS, LARGE LANGUAGE MODELS & AGENTS
     ████████████████████████████████████████████████████████████████████████ -->

<div class="part-page">
  <div class="part-number">Part 5</div>
  <div class="part-title">Transformers, LLMs &amp; Multi-Agent Systems</div>
  <div class="part-subtitle">Attention, Hugging Face, Enterprise RAG, GraphRAG, QLoRA, DPO Alignment, LangChain, LangGraph &amp; vLLM</div>
  <div class="part-ornament">✦ ✦ ✦</div>
</div>

"""

CHAPTERS = [
    "book_builder/ch51_transformer_architecture.html",
    "book_builder/ch51b_bert_encoders.html",
    "book_builder/ch52_tokenization_huggingface.html",
    "book_builder/ch53_enterprise_rag.html",
    "book_builder/ch54_llamaindex_graphrag.html",
    "book_builder/ch55_lora_qlora.html",
    "book_builder/ch56_alignment_rlhf_dpo.html",
    "book_builder/ch57_langchain_lcel.html",
    "book_builder/ch58_langgraph_agents.html",
    "book_builder/ch59_coding_agents.html",
    "book_builder/ch510_llm_serving_vllm.html"
]

output_path = "book_builder/part5.html"

contents = [HEADER]
total_problems = 0

for ch in CHAPTERS:
    with open(ch, "r", encoding="utf-8") as f:
        text = f.read()
    problems = re.findall(r'<div class="problem">', text)
    total_problems += len(problems)
    contents.append(text)
    print(f"Loaded {ch}: {len(text)} bytes, {len(problems)} problems")

combined = "\n\n".join(contents)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(combined)

print(f"\nPart 5 successfully assembled into {output_path}!")
print(f"Total size: {len(combined)} bytes ({len(combined.splitlines())} lines)")
print(f"Total problems in Part 5: {total_problems}")
