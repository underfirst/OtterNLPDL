def decode_input_ids(input_ids, tokenizer):
    return [tokenizer.decode(seq.squeeze(), skip_special_tokens=True, clean_up_tokenization_spaces=True)
            for seq in input_ids]
