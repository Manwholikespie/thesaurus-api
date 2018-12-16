from __future__ import absolute_import, division, print_function, unicode_literals
import itertools
import pprint

from thesaurus import Word
import argparse


PARSER = argparse.ArgumentParser(description='')
PARSER.add_argument('word', nargs='*', help='World to search for')
PARSER.add_argument('-a', '--antonym', action='store_true', default=False)
PARSER.add_argument('--depth', '-d', default=1, type=int, help='For each result found find synonyms up to a given depth. (Useful for discerning meanings)')

def get_matches(w, antonym):
    results = []
    obj = Word(w)
    if antonym:
        results.extend(obj.antonyms())
    else:
        results.extend(obj.synonyms())
    return results

def main():
    args = PARSER.parse_args()
    all_words = set(args.word)

    children = dict()

    for x in range(args.depth):
        for x in set(all_words):
            if x in children:
                continue
            else:
                children[x] = get_matches(x, args.antonym)
                all_words |= set(children[x])

    roots = list(itertools.chain.from_iterable(children[w] for w in args.word))
    print(dump_tree(roots, children, args.depth - 1))

def dump_tree(roots, children, depth):
    if depth < 0:
        raise ValueError(depth)
    elif depth == 0:
        return '\n'.join(roots)
    else:
        return '\n'.join(c + '\n' + indent(dump_tree(children[c], children, depth - 1)) for c in children)

def indent(x):
    return '\n'.join('    ' + y for y in  x.splitlines()) 
