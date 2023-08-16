from tqdm import tqdm

# input_filename = "../data/test/test.jsonl"
# output_filename = "../data/test/repeated_train.jsonl"

input_filename = "../data/test_triplet/test_train.jsonl"
output_filename = "../data/test_triplet/repeated_test_train.jsonl"

# input_filename = "../data/embedded_transformed_data_v2.jsonl"
# output_filename = "../data/training_data/repeated_embedded_merged_data.jsonl"

repetitions = 10000  # or however many times you want to repeat

# Read the entire content of the original file
with open(input_filename, 'r') as f:
    content = f.read()

# Write the content multiple times to the output file
with open(output_filename, 'w') as f:
    for _ in tqdm(range(repetitions), desc="Processing", position=0, leave=True):
        f.write(content)
