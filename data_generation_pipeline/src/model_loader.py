import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


def load_model_tokenizer(model_name: str, quant_config: dict):
    """Load a causal LM and its tokenizer with optional 4-bit quantization.

    Args:
        model_name: HuggingFace model identifier.
        quant_config: Quantization settings from model_config.yaml.

    Returns:
        (tokenizer, model) tuple ready for inference.
    """
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=quant_config.get("load_in_4bit", True),
        bnb_4bit_use_double_quant=quant_config.get("bnb_4bit_use_double_quant", True),
        bnb_4bit_quant_type=quant_config.get("bnb_4bit_quant_type", "nf4"),
        bnb_4bit_compute_dtype=getattr(
            torch, quant_config.get("bnb_4bit_compute_dtype", "float16")
        ),
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )
    model.config.pad_token_id = tokenizer.eos_token_id
    return tokenizer, model
