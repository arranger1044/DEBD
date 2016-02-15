import numpy

import os

import itertools

from utils import load_train_valid_test_csvs
from utils import dataset_to_instances_set
from utils import split_union

RND_SEED = 1337


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
                 'tretail',
                 'bin-mnist']

DATA_PATH = './datasets'
OUTPUT_PATH = './datasets'

SPLIT_NAMES = ['train', 'valid', 'test']


def only_shuffle_split_train_valid_test(data, percs=[0.75, 0.1, 0.15], rand_gen=None):

    if rand_gen is None:
        rand_gen = numpy.random.RandomState(RND_SEED)

    n_instances = data.shape[0]

    samples_ids = numpy.arange(n_instances)
    #
    # shuffle the ids
    shuffled_ids = rand_gen.permutation(samples_ids)

    #
    # getting slices
    n_splits = len(percs)
    nb_split_samples = [int(n_instances * p) for p in percs[:-1]]
    nb_split_samples += [n_instances - sum(nb_split_samples)]
    assert sum(nb_split_samples) == len(samples_ids)

    split_samples_ids = [0] * (n_splits + 1)
    for i in range(n_splits):
        split_samples_ids[i + 1] = nb_split_samples[i] + split_samples_ids[i]

    # print('Splits', split_samples_ids)
    sample_splits = [shuffled_ids[split_samples_ids[i]:split_samples_ids[i + 1]]
                     for i in range(n_splits)]
    # print('unique splits', unique_sample_splits)

    #
    # extracting samples
    data_splits = []
    for split_ids in sample_splits:
        # print(split_ids)
        extracted_split = data[split_ids]
        data_splits.append(extracted_split)

    assert len(data_splits) == n_splits

    return data_splits


def shuffle_split_train_valid_test(data,
                                   percs=[0.75, 0.1, 0.15],
                                   only_uniques=False,
                                   rand_gen=None):

    if rand_gen is None:
        rand_gen = numpy.random.RandomState(RND_SEED)

    n_instances = data.shape[0]

    ids_dict = {}

    samples_ids = numpy.ones(n_instances, dtype=numpy.int)

    #
    # collecting unique samples ids
    counter = 0
    for i, s in enumerate(data):
        #
        # making it hashable
        sample_tuple = tuple(s)

        if sample_tuple not in ids_dict:
            ids_dict[sample_tuple] = counter
            counter += 1

        samples_ids[i] = ids_dict[sample_tuple]

    print('There are {} unique samples'.format(counter))
    # print(samples_ids)
    unique_samples_ids = list(sorted(set(samples_ids)))
    assert len(unique_samples_ids) == counter

    #
    # shuffle the ids
    shuffled_ids = rand_gen.permutation(unique_samples_ids)

    #
    # getting slices
    n_splits = len(percs)
    nb_split_samples = [int(counter * p) for p in percs[:-1]]
    nb_split_samples += [counter - sum(nb_split_samples)]
    assert sum(nb_split_samples) == len(unique_samples_ids)

    split_samples_ids = [0] * (n_splits + 1)
    for i in range(n_splits):
        split_samples_ids[i + 1] = nb_split_samples[i] + split_samples_ids[i]

    # print('Splits', split_samples_ids)
    unique_sample_splits = [
        shuffled_ids[split_samples_ids[i]:split_samples_ids[i + 1]] for i in range(n_splits)]
    # print('unique splits', unique_sample_splits)

    #
    # extracting samples
    data_splits = []
    for u_split in unique_sample_splits:
        split_ids = set(u_split)
        # print(split_ids)
        samples_mask = numpy.zeros(n_instances, dtype=bool)
        for i in range(n_instances):
            if samples_ids[i] in split_ids:
                # print(samples_ids[i])
                samples_mask[i] = True
        # print(samples_mask)
        extracted_split = data[samples_mask]
        data_splits.append(extracted_split)

    assert len(data_splits) == n_splits

    #
    # collapsing to uniques
    if only_uniques:
        unique_data_sets = [dataset_to_instances_set(split) for split in data_splits]
        for i, split in enumerate(unique_data_sets):
            data_array_list = [numpy.array(s) for s in split]
            data_splits[i] = numpy.array(data_array_list)

    return data_splits


def print_split_stats(dataset_splits, split_names=SPLIT_NAMES, out_log=None):

    unique_splits = [dataset_to_instances_set(split) for split in dataset_splits]

    uniq_str = 'Unique instances in splits:'
    print(uniq_str)
    if out_log:
        out_log.write(uniq_str + '\n')
    for orig_split, unique_split, split_name in zip(dataset_splits, unique_splits, split_names):
        uniq_str = '\t# all instances {2}: {0} -> {1}'.format(len(orig_split),
                                                              len(unique_split),
                                                              split_name)
        print(uniq_str)
        if out_log:
            out_log.write(uniq_str + '\n')

    over_str = 'Overlapping instances:'
    print(over_str)
    if out_log:
        out_log.write(over_str + '\n')
    split_pairs = itertools.combinations(unique_splits, 2)
    split_names = itertools.combinations(SPLIT_NAMES, 2)
    for (name_1, name_2), (split_1, split_2) in zip(split_names, split_pairs):
        n_over_instances = len(split_1 & split_2)
        over_str = '\toverlapping instances from {0} to {1}:\t{2}'.format(name_1,
                                                                          name_2,
                                                                          n_over_instances)
        print(over_str)
        if out_log:
            out_log.write(over_str + '\n')

    n_over_instances = len(set.intersection(*unique_splits))
    over_str = '\toverlapping instances among {0}: {1}\n'.format(SPLIT_NAMES, n_over_instances)
    print(over_str)
    if out_log:
        out_log.write(over_str)


import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('dataset', type=str,
                        help='Name of the dataset to process (e.g. nltcs)')
    parser.add_argument('-o', '--output', type=str, nargs='?',
                        default=OUTPUT_PATH,
                        help='Output dir path')
    parser.add_argument('--prefix', type=str, nargs='?',
                        default='no-over',
                        help='Prefix for the new dataset name')
    parser.add_argument('--perc', type=float, nargs='+',
                        default=[0.75, 0.1, 0.15],
                        help='Percentages of split')
    parser.add_argument('--unique', action='store_true',
                        help='Whether to remove all duplicate instances')
    parser.add_argument('--shuffle', action='store_true',
                        help='Whether to shuffle data')
    parser.add_argument('--no-overlap', action='store_true',
                        help='No overlapping instances among splits')
    parser.add_argument('-v', '--verbose', type=int, nargs='?',
                        default=0,
                        help='Verbosity level')
    parser.add_argument('--seed', type=int, nargs='?',
                        default=1337,
                        help='Seed for the random generator')

    args = parser.parse_args()
    print("Starting with arguments:", args)

    rand_gen = numpy.random.RandomState(args.seed)

    new_dataset_name = '{0}-{1}'.format(args.prefix,
                                        args.dataset)
    out_path = os.path.join(args.output, new_dataset_name)
    os.makedirs(out_path, exist_ok=True)
    out_log_path = os.path.join(out_path, '{0}.exp.log'.format(new_dataset_name))
    print(out_path, out_log_path)

    split_names = SPLIT_NAMES

    with open(out_log_path, 'w') as out_log:

        #
        # loading dataset
        dataset_splits = load_train_valid_test_csvs(args.dataset,
                                                    os.path.join(DATA_PATH, args.dataset),
                                                    verbose=False)

        train, valid, test = dataset_splits
        split_shape_str = 'Data splits shapes:\n\ttrain: '\
            '{0}\n\tvalid: {1}\n\ttest: {2}'.format(train.shape,
                                                    valid.shape,
                                                    test.shape)
        print(split_shape_str)
        out_log.write(split_shape_str + '\n')

        print_split_stats(dataset_splits, split_names, out_log)

        #
        # merging them
        merged_data = split_union((train, valid, test))
        merge_shape_str = 'Merged splits shape: {}'.format(merged_data.shape)
        print(merge_shape_str)
        out_log.write(merge_shape_str + '\n')

        resampled_splits = None

        if args.shuffle and not args.unique and not args.no_overlap:
            print('shuffling only')
            resampled_splits = only_shuffle_split_train_valid_test(merged_data,
                                                                   percs=args.perc,
                                                                   rand_gen=rand_gen)

        else:
            #
            # resampling
            resampled_splits = shuffle_split_train_valid_test(merged_data,
                                                              percs=args.perc,
                                                              only_uniques=args.unique,
                                                              rand_gen=rand_gen)

        re_train, re_valid, re_test = resampled_splits
        split_shape_str = 'Shapes after resampling:\n\ttrain: ' \
            '{0}\n\tvalid: {1}\n\ttest: {2}'.format(re_train.shape,
                                                    re_valid.shape,
                                                    re_test.shape)
        print(split_shape_str)
        out_log.write(split_shape_str + '\n')

        print_split_stats(resampled_splits, split_names, out_log)

        numpy.savetxt(os.path.join(out_path, '{}.train.data'.format(new_dataset_name)),
                      re_train, delimiter=',', fmt='%d')
        numpy.savetxt(os.path.join(out_path, '{}.valid.data'.format(new_dataset_name)),
                      re_valid, delimiter=',', fmt='%d')
        numpy.savetxt(os.path.join(out_path, '{}.test.data'.format(new_dataset_name)),
                      re_test, delimiter=',', fmt='%d')
