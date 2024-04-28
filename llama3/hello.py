import time
import transformers
import termcolor
import torch

# model_id = "meta-llama/Meta-Llama-3-8B"
model_id = "/Users/AlexG/data/llama3"

start = time.time()
print(termcolor.colored(f"Loading model {model_id}...", "grey"))
pipeline = transformers.pipeline(
"text-generation", model=model_id, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto"
)
print(termcolor.colored(
    f"Loaded model {model_id} in {time.time() - start:.1f} seconds.", "grey"))
# pipeline("Hey how are you doing today?")
start = time.time()
prompt = "In this text: 'How G.M. Tricked Millions of Drivers Into Being Spied On (Including Me)', is it news title? Your answer(Y/N):"
seq = pipeline(prompt,
        do_sample=True,
        top_k=5,
        top_p=0.9,
        num_return_sequences=1,
        repetition_penalty=1.5,
        max_new_tokens=5,)

print(termcolor.colored(f"Generated sequence in {time.time() - start:.1f} seconds.", "grey"))
print(termcolor.colored('generated seq:', 'green'))
print(seq)