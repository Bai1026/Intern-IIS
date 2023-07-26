'''
This file is to filter out the technique to have a more clear observation
'''

def filter_rows(input_file, output_file, keyword):
    with open(input_file, 'r') as input_txt, open(output_file, 'w') as output_txt:
        for line in input_txt:
            if keyword not in line:
                output_txt.write(line)

input_txt_file = '/workdir/home/bai/data_processing/data_euni/train2id_label.txt'
output_txt_file = '/workdir/home/bai/data_processing/data/filtered_data_v2.csv'

keyword_to_filter = 'benign'

# delete the rows including "benign"
filter_rows(input_txt_file, output_txt_file, keyword_to_filter)
print('done!')