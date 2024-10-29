import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

device = "cuda"
model_name = "Skywork/Skywork-Reward-Llama-3.1-8B-v0.2"
rm = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map=device,
    num_labels=1,
    attn_implementation="eager",
)
rm_tokenizer = AutoTokenizer.from_pretrained(model_name)

def reward(prompt, responses):
    conversations = []
    for response in responses:
        conversation = [{"role": "user", "content": prompt}, {"role": "assistant", "content": response}]
        conversations.append(conversation)

    convs_formatted = []
    for conversation in conversations:
        conv_formatted = rm_tokenizer.apply_chat_template(conversation, tokenize=False)
        convs_formatted.append(conv_formatted)

    convs_tokenized = []
    for conv_formatted in convs_formatted:
        convs_tokenized.append(rm_tokenizer(conv_formatted, return_tensors="pt").to(device))

    # Get the reward scores
    scores = []
    with torch.no_grad():
        for conv_tokeinized in convs_tokenized:
            score = rm(**conv_tokeinized).logits[0][0].item()
            scores.append(score)

    return scores