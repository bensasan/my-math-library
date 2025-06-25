import os
from huggingface_hub import login
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
import faiss
import torch

# Authenticate with Hugging Face Hub using an environment variable
HF_TOKEN = os.getenv('HF_TOKEN')
if HF_TOKEN:
    login(token=HF_TOKEN)
else:
    print('HF_TOKEN environment variable is not set. Skipping login.')

# Load a subset of the finance dataset (first 100k rows)
print('Loading dataset...')
dataset = load_dataset('Josephgflowers/Finance-Instruct-500k', split='train[:100000]')

# Use a sentence transformer to create embeddings for retrieval
print('Embedding corpus...')
embed_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
corpus_embeddings = embed_model.encode(dataset['instruction'], show_progress_bar=True)

# Build FAISS index
index = faiss.IndexFlatL2(corpus_embeddings.shape[1])
index.add(corpus_embeddings)

# Load the Typhoon model and tokenizer
print('Loading language model...')
tokenizer = AutoTokenizer.from_pretrained('typhoon-v2.1-12b-instruct')
model = AutoModelForCausalLM.from_pretrained('typhoon-v2.1-12b-instruct', device_map='auto')


def retrieve(query, top_k=5):
    query_emb = embed_model.encode([query])
    distances, indices = index.search(query_emb, top_k)
    return '\n'.join(dataset['instruction'][i] for i in indices[0])


def generate_answer(query):
    context = retrieve(query)
    prompt = f"You are a helpful finance assistant. Use the following context to answer.\n\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"
    inputs = tokenizer(prompt, return_tensors='pt').to(model.device)
    output = model.generate(**inputs, max_new_tokens=200)
    return tokenizer.decode(output[0], skip_special_tokens=True)


def math_tool(expression):
    try:
        return str(eval(expression, {'__builtins__': {}}, {}))
    except Exception as e:
        return f'Error: {e}'


class FinanceAgent:
    def __init__(self):
        pass

    def run(self, task):
        if task.lower().startswith('calculate '):
            expr = task[len('calculate '):]
            return math_tool(expr)
        else:
            return generate_answer(task)


if __name__ == '__main__':
    agent = FinanceAgent()
    while True:
        user_input = input('> ')
        if user_input.lower() in {'quit', 'exit'}:
            break
        response = agent.run(user_input)
        print(response)
