from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import OrderedDict
from hashlib import md5
import string
import sys

import numpy as np
from six.moves import range  # pylint: disable=redefined-builtin
from six.moves import zip  # pylint: disable=redefined-builtin

from tensorflow.python.platform import tf_logging as logging
from tensorflow.python.util.tf_export import tf_export


if sys.version_info < (3,):
  maketrans = string.maketrans
else:
  maketrans = str.maketrans


def text_to_word_sequence(text,
                          filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
                          lower=True,
                          split=' '):
    """Converts a text to a sequence of words (or tokens).
    # 过滤掉filters，并且用split分割text

    Arguments:
        text: Input text (string).
        filters: Sequence of characters to filter out.
        lower: Whether to convert the input to lowercase.
        split: Sentence split marker (string).

    Returns:
        A list of words (or tokens).
    """
    if lower:
        text = text.lower()

    if sys.version_info < (3,) and isinstance(text, unicode):
        translate_map = dict((ord(c), unicode(split)) for c in filters)
    else:
        translate_map = maketrans(filters, split * len(filters))

    text = text.translate(translate_map)
    seq = text.split(split)
    return [i for i in seq if i]

class MyVocabulary(object):
    """
    参照了tf.text.Tokenizer的实现
    """
    def __init__(self,
                 num_words=None,
                 filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
                 lower=True,
                 split=' ',
                 char_level=False,
                 oov_token=None,
                 **kwargs):
        # Legacy support

        self.word_counts = OrderedDict()
        self.word_docs = {}
        self.filters = filters
        self.split = split
        self.lower = lower
        self.num_words = num_words
        self.document_count = 0
        self.char_level = char_level
        self.oov_token = oov_token
        self.index_docs = {}

    def fit_on_vocab_file(self, vocab_path):
        """
        从已存在的字典文件中读取单词数据。
        格式：单词 频数
        """
        with open(vocab_path, 'r', encoding='utf8') as vocab_f:
            # 保留idx=0。用来padding
            current_idx = 1
            for line in vocab_f:
                # pieces[0]是单词, pieces[1]是词频
                pieces = line.split()
                # 两个异常处理
                if len(pieces) != 2:
                    sys.stderr.write('Bad line: %s\n' % line)
                    continue
                if pieces[0] in self.word_index:
                    raise ValueError('Duplicated word: %s.' % pieces[0])
                # 存入word_to_id
                self.word_index[pieces[0]] = current_idx
                current_idx += 1
        # 添加oov词
        if self.oov_token is not None:
            i = self.word_index.get(self.oov_token)
            if i is None:
                self.word_index[self.oov_token] = len(self.word_index) + 1

    def fit_on_texts(self, texts):
        """Updates internal vocabulary based on a list of texts.
        word_index从下标1开始映射单词。0不用，留给padding。
        如果设置了oov_token, 则在word_index最末尾添加一个下标映射oov_token

        In the case where texts contains lists, we assume each entry of the lists
        to be a token.

        Required before using `texts_to_sequences` or `texts_to_matrix`.

        Arguments:
            texts: can be a list of strings,
                a generator of strings (for memory-efficiency),
                or a list of list of strings.
        """
        for text in texts:
            self.document_count += 1
            if self.char_level or isinstance(text, list):
                seq = text
            else:
                seq = text_to_word_sequence(text, self.filters, self.lower, self.split)
            for w in seq:
                if w in self.word_counts:
                    self.word_counts[w] += 1
                else:
                    self.word_counts[w] = 1
            for w in set(seq):
                if w in self.word_docs:
                    self.word_docs[w] += 1
                else:
                    self.word_docs[w] = 1

        wcounts = list(self.word_counts.items())
        wcounts.sort(key=lambda x: x[1], reverse=True)
        sorted_voc = [wc[0] for wc in wcounts]
        # note that index 0 is reserved, never assigned to an existing word
        self.word_index = dict(
            list(zip(sorted_voc, list(range(1,
                                            len(sorted_voc) + 1)))))

        if self.oov_token is not None:
            i = self.word_index.get(self.oov_token)
            if i is None:
                self.word_index[self.oov_token] = len(self.word_index) + 1

        for w, c in list(self.word_docs.items()):
            self.index_docs[self.word_index[w]] = c

    def texts_to_sequences(self, texts):
        """Transforms each text in texts in a sequence of integers.

        Only top "num_words" most frequent words will be taken into account.
        Only words known by the tokenizer will be taken into account.

        Arguments:
            texts: A list of texts (strings).

        Returns:
            A list of sequences.
        """
        res = []
        for vect in self.texts_to_sequences_generator(texts):
            res.append(vect)
        return res

    def texts_to_sequences_generator(self, texts):
        """Transforms each text in `texts` in a sequence of integers.

        Each item in texts can also be a list, in which case we assume each item of
        that list
        to be a token.

        Only top "num_words" most frequent words will be taken into account.
        Only words known by the tokenizer will be taken into account.

        Arguments:
            texts: A list of texts (strings).

        Yields:
            Yields individual sequences.
        """
        num_words = self.num_words
        for text in texts:
            if self.char_level or isinstance(text, list):
                seq = text
            else:
                seq = text_to_word_sequence(text, self.filters, self.lower, self.split)
            vect = []
            for w in seq:
                i = self.word_index.get(w)
                if i is not None:
                    if num_words and i >= num_words:    # 直接跳过 在词典里但是超过num_words 的词！
                        continue
                    else:
                        vect.append(i)
                elif self.oov_token is not None:    # 将OOV词替换为相应的Id！
                    i = self.word_index.get(self.oov_token)
                    if i is not None:
                        vect.append(i)
            yield vect

    def add_on_texts(self):
        """
        增加新的语料(text of list)。 扩充word_index, 并且需要确保新语料的词出现在num_words之内。
        """
        pass

    def get_word2index(self):
        return self.word_index[:self.num_words]

    def get_index2word(self):
        w2i = self.get_word2index()
        i2w = {}
        for word,idx in w2i.items():
            i2w[idx] = word
        return i2w