# Run this code to generate a js file that contains an object
# with key-value pairs between words and their frequencies in Google Web Trillion Word Corpus.
# dataset from: https://www.kaggle.com/datasets/rtatman/english-word-frequency?resource=download

import csv

def read_csv():
    freq_array = []
    with open('data_handling/word_freq.csv', mode = 'r') as file:
        csv_file = csv.reader(file)
        for lines in csv_file:
            freq_array.append(lines)
    return freq_array

def make_frequencies():
    with open('mondegreen/src/word_freqs.js', 'w') as frequencies_file:
        frequencies_file.write('export default {\n')
        frequencies = read_csv()
        rows = []
        for r in frequencies:
            if [r[0], r[1]] not in rows:
                pair = [r[0], r[1]]
                rows.append(pair)
                frequencies_file.write('\t' + '"' + r[0] + '": "' + r[1] + '",\n')
        frequencies_file.write('};')

make_frequencies()