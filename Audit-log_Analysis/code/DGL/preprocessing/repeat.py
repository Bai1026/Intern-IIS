input_filename = "../data/embedded_merged_data.jsonl"
output_filename = "../data/repeated_embedded_merged_data.jsonl"
repetitions = 200  # or however many times you want to repeat

# Read the entire content of the original file
with open(input_filename, 'r') as f:
    content = f.read()

# Write the content multiple times to the output file
with open(output_filename, 'w') as f:
    for _ in range(repetitions):
        f.write(content)
