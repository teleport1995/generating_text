import re
from os import listdir, path
from collections import defaultdict, Counter
import pickle

alphabet = re.compile(r"[A-Za-z0-9]+|[.!?,:;]+")

EMPTY_SYMBOL = '#'


def get_lines(file_name):
    for line in open(file_name):
        yield line.lower()


def get_tokens(lines):
    for line in lines:
        for token in alphabet.findall(line):
            yield token


def get_trigrams(tokens):
    first_token, second_token = EMPTY_SYMBOL, EMPTY_SYMBOL
    for token in tokens:
        yield first_token, second_token, token
        if token in ".!?":
            yield second_token, token, EMPTY_SYMBOL
            yield token, EMPTY_SYMBOL, EMPTY_SYMBOL
            first_token, second_token = EMPTY_SYMBOL, EMPTY_SYMBOL
        else:
            first_token, second_token = second_token, token


def get_file_names(directory_name):
    for name in listdir(directory_name):
        if name.endswith(".txt"):
            yield path.join(directory_name, name)
        else:
            for file_name in get_file_names(path.join(directory_name, name)):
                yield file_name


def generate_model(directory_name):
    bigrams_counter = Counter()
    trigrams_dict = defaultdict(lambda: .0)

    for file_name in get_file_names(directory_name):
        lines = get_lines(file_name)
        tokens = get_tokens(lines)
        trigrams = get_trigrams(tokens)

        for first_token, second_token, third_token in trigrams:
            bigrams_counter[first_token, second_token] += 1
            trigrams_dict[first_token, second_token, third_token] += 1

    model = defaultdict(lambda: [])

    for (first_token, second_token, third_token), frequency in trigrams_dict.iteritems():
        element = (third_token, frequency / bigrams_counter[first_token, second_token])
        model[first_token, second_token].append(element)

    return model


def main():
    model = generate_model("corpus")
    pickle.dump(dict(model), open("model", "w"))

if __name__ == "__main__":
    main()
