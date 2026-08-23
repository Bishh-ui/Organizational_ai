import torch


def generate_with_retry(
    tokenizer,
    model,
    prompt: str,
    max_new_tokens: int = 512,
    deterministic_temp: float = 0.0,
    sampling_temp: float = 0.4,
) -> str:
    """Generate text from a prompt, falling back to sampling if greedy decoding fails.

    Attempts greedy (deterministic) decoding first. If the output is empty or too short,
    retries with temperature sampling.

    Args:
        tokenizer: HuggingFace tokenizer.
        model: HuggingFace causal LM.
        prompt: Input prompt string.
        max_new_tokens: Maximum tokens to generate.
        deterministic_temp: Temperature for greedy pass (0.0 = greedy).
        sampling_temp: Temperature for sampling fallback.

    Returns:
        Generated text string, or empty string on failure.
    """
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=tokenizer.model_max_length,
    ).to(model.device)

    input_len = inputs["input_ids"].shape[1]

    def _decode(output) -> str:
        return tokenizer.decode(
            output[0][input_len:], skip_special_tokens=True
        ).strip()

    # First pass: greedy decoding
    try:
        with torch.no_grad():
            out = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                min_new_tokens=50,
                temperature=deterministic_temp,
                top_p=0.95,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )
        text = _decode(out)
        if text and len(text) >= 10:
            return text
    except Exception:
        pass

    # Second pass: sampling fallback
    try:
        with torch.no_grad():
            out = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=sampling_temp,
                top_p=0.95,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )
        return _decode(out)
    except Exception:
        return ""
