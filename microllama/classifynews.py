import time
import torch
import transformers
import termcolor
from transformers import AutoTokenizer, LlamaForCausalLM

MODEL_PATH = '/Users/AlexG/Documents/GitHub/web_tools/microllama/model'
def generate_text(prompt, model, tokenizer):
    text_generator = transformers.pipeline(
        "text-generation",
        model=model,
        torch_dtype=torch.float16,
        device_map="auto",
        tokenizer=tokenizer
    )

    # formatted_prompt = f"Question: {prompt} Answer:"
    formatted_prompt = f"{prompt}, is this a news? My answer is "

    sequences = text_generator(
        formatted_prompt,
        do_sample=True,
        top_k=5,
        top_p=0.9,
        num_return_sequences=1,
        repetition_penalty=1.5,
        max_new_tokens=32,
    )

    for seq in sequences:
        print(f"Result: {termcolor.colored(seq['generated_text'], 'green')}")


start = time.time()
print(termcolor.colored('loading model...', 'red'))
# use the same tokenizer as TinyLlama
# tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-step-50K-105b")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

# load model from huggingface
# question from https://www.reddit.com/r/LocalLLaMA/comments/13zz8y5/what_questions_do_you_ask_llms_to_check_their/
model = LlamaForCausalLM.from_pretrained(MODEL_PATH)
print('time to load model: ', time.time() - start)

start = time.time()
generate_text("In this text: 'How G.M. Tricked Millions of Drivers Into Being Spied On (Including Me)'", model, tokenizer)
print('time to generate text: ', time.time() - start)