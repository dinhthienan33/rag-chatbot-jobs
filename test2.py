from transformers import AutoModelForCausalLM, AutoTokenizer

# Initialize the Hugging Face model and tokenizer
model_name = "gpt2"  # You can replace this with any Hugging Face model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Prepare the input
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Write a haiku about recursion in programming."}
]

# Convert messages to a single string
input_text = "\n".join([msg["content"] for msg in messages])

# Tokenize the input
inputs = tokenizer(input_text, return_tensors="pt")

# Generate the completion
outputs = model.generate(inputs["input_ids"], max_length=50)

# Decode and print the generated text
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(generated_text)