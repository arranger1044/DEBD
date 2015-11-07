import numpy
from numpy.testing import assert_array_equal
import csv
import os
try:
    from time import perf_counter
except:
    from time import time
    perf_counter = time


DATA_PATH = "datasets"


def csv_2_numpy(filename, path=DATA_PATH, sep=',', type='int8'):
    """
    Utility to read a dataset in csv format into a numpy array
    """
    file_path = os.path.join(path, filename)
    reader = csv.reader(open(file_path, "r"), delimiter=sep)
    x = list(reader)
    array = numpy.array(x).astype(type)
    return array


def load_train_valid_test_csvs(dataset_name,
                               path=DATA_PATH,
                               sep=',',
                               type='int32',
                               suffix='data',
                               splits=['train',
                                       'valid',
                                       'test'],
                               verbose=True):
    """
    Loading training, validation and test splits by suffix from csv files
    """

    csv_files = ['{0}.{1}.{2}'.format(dataset_name, ext, suffix) for ext in splits]

    # dataset_subpath = os.path.join(path, dataset_name)

    load_start_t = perf_counter()
    dataset_splits = [csv_2_numpy(file, path, sep, type) for file in csv_files]
    load_end_t = perf_counter()

    if verbose:
        print('Dataset splits for {0} loaded in {1} secs'.format(dataset_name,
                                                                 load_end_t - load_start_t))
        for data, split in zip(dataset_splits, splits):
            print('\t{0}:\t{1}'.format(split, data.shape))

    return dataset_splits


def load_train_valid_test_npz(dataset_name,
                              path=DATA_PATH,
                              ext='.npz',
                              type='int32',
                              suffix='_data',
                              splits=['train',
                                      'valid',
                                      'test'],
                              verbose=True):
    """
    Loading training, validation and test splits from the npz archive
    """

    file_path = os.path.join(path, dataset_name + ext)
    uncompressed_data = numpy.load(file_path)

    load_start_t = perf_counter()
    dataset_splits = [uncompressed_data[key + suffix].astype(type) for key in splits]
    load_end_t = perf_counter()

    if verbose:
        print('Dataset splits for {0} loaded in {1} secs'.format(dataset_name,
                                                                 load_end_t - load_start_t))
        for data, split in zip(dataset_splits, splits):
            print('\t{0}:\t{1}'.format(split, data.shape))

    return dataset_splits


def compress_numpy_splits_made(dataset_name,
                               output_path,
                               dataset_splits,
                               splits=['train',
                                       'valid',
                                       'test'],
                               data_suffix='_data',
                               length_suffix='_length'):

    output_filename = os.path.join(output_path,  dataset_name)
    input_sizes = numpy.array([data.shape[1] for data in dataset_splits],
                              dtype='int32')
    #
    # check them to have the same sizes
    assert_array_equal(input_sizes,
                       numpy.array([input_sizes[0] for i in range(input_sizes.shape[0])],
                                   dtype='int32'))

    dataset_dict = {}
    dataset_dict['inputsize'] = numpy.array(input_sizes[0], dtype='int32')

    for data, prefix in zip(dataset_splits, splits):
        dataset_dict[prefix + data_suffix] = data.astype('float32')
        dataset_dict[prefix + length_suffix] = numpy.array(data.shape[0], dtype='int32')

    #
    # serializing
    numpy.savez(output_filename, **dataset_dict)

if __name__ == '__main__':

    DATASET_NAMES = ['accidents',
                     'ad',
                     'baudio',
                     'bbc',
                     'bnetflix',
                     'book',
                     'c20ng',
                     'cr52',
                     'cwebkb',
                     'dna',
                     'jester',
                     'kdd',
                     'msnbc',
                     'msweb',
                     'nltcs',
                     'plants',
                     'pumsb_star',
                     'tmovie',
                     'tretail']

    NPZ_OUTPUT = '../MADE/datasets/'

    for dataset in DATASET_NAMES:

        print('Processing dataset', dataset)
        #
        # loading from csv
        train, valid, test = load_train_valid_test_csvs(dataset,
                                                        path=os.path.join(DATA_PATH, dataset))

        #
        # compressing into npz
        compress_numpy_splits_made(dataset, NPZ_OUTPUT, [train, valid, test])

        #
        # loading them back
        train_npz, valid_npz, test_npz = load_train_valid_test_npz(dataset, NPZ_OUTPUT)

        #
        # check for exactnetss
        assert_array_equal(train, train_npz)
        assert_array_equal(valid, valid_npz)
        assert_array_equal(test, test_npz)
