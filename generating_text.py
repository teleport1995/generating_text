from generating_model import EMPTY_SYMBOL
import pickle
import random
import textwrap


def get_next_token(model, first_token, second_token):
    prob = .0
    need_prob = random.random()
    for third_token, frequency in model[first_token, second_token]:
        prob += frequency
        if prob >= need_prob:
            return third_token


def generate_sentence(model):
    sentence = ""
    first_token, second_token = EMPTY_SYMBOL, EMPTY_SYMBOL
    while True:
        first_token, second_token = second_token, get_next_token(model, first_token, second_token)
        if second_token == EMPTY_SYMBOL:
            break
        if second_token not in ".!?,:;" and first_token != EMPTY_SYMBOL:
            sentence += " "
        sentence += second_token
    return sentence.capitalize()


def get_sentences_count():
    return random.randint(4, 10)


def generate_paragraph(model):
    sentences_count = get_sentences_count()
    return "\n".join(textwrap.wrap("\t" + " ".join([generate_sentence(model) for _ in xrange(sentences_count)])))


def main():
    model = pickle.load(open("model"))
    paragraphs_count = 500
    with open("text.txt", "w") as stream:
        for _ in xrange(paragraphs_count):
            stream.write(generate_paragraph(model))
            stream.write("\n")

if __name__ == "__main__":
    main()
