from BackEnd import get_oil_prices, get_oil_indices
from keras.preprocessing.sequence import pad_sequences
import argparse


def train(index_to_train: str):
    indices = get_oil_indices()
    index_id = None
    for ind in indices:
        if ind.index_name == index_to_train:
            index_id = ind.index_id
    if index_id is None:
        print("index name: %s is not found in database" % index_to_train)
        return
    prices = get_oil_prices(index_id)
    # TODO finish rest


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('index_to_train', 'index', required=True, type=str)
