r"""Test `lmp.tokenizer.CharListTokenizer.decode`.

Usage:
    python -m unittest \
        test/lmp/tokenizer/_base_list_tokenizer/test_decode.py
"""

# built-in modules

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import inspect
import gc
import math
import unittest

from typing import List

# self-made modules

from lmp.tokenizer import CharListTokenizer


class TestDecode(unittest.TestCase):
    r"""Test Case for `lmp.tokenizer.CharListTokenizer.decode`."""

    def setUp(self):
        r"""Setup both cased and uncased tokenizer instances."""
        self.cased_tokenizer = CharListTokenizer()
        self.uncased_tokenizer = CharListTokenizer(is_uncased=True)
        self.tokenizers = [self.cased_tokenizer, self.uncased_tokenizer]

    def tearDown(self):
        r"""Delete both cased and uncased tokenizer instances."""
        del self.tokenizers
        del self.cased_tokenizer
        del self.uncased_tokenizer
        gc.collect()

    def test_signature(self):
        r"""Ensure signature consistency."""
        msg = 'Inconsistent method signature.'

        self.assertEqual(
            inspect.signature(CharListTokenizer.decode),
            inspect.Signature(
                parameters=[
                    inspect.Parameter(
                        name='self',
                        kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    ),
                    inspect.Parameter(
                        name='token_ids',
                        kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                        annotation=List[int],
                        default=inspect.Parameter.empty
                    ),
                    inspect.Parameter(
                        name='remove_special_tokens',
                        kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                        annotation=bool,
                        default=False
                    )
                ],
                return_annotation=str
            ),
            msg=msg
        )

    def test_invalid_input_token_ids(self):
        r"""Raise `TypeError` when input is invalid."""
        msg1 = 'Must raise `TypeError` when input is invalid.'
        msg2 = 'Inconsistent error message.'
        examples = (
            0, 1, -1, 0.0, 1.0, math.nan, math.inf, True, False, b'',
            (), {}, set(), object(), lambda x: x, type, None,
        )

        for invalid_input in examples:
            for tokenizer in self.tokenizers:
                with self.assertRaises(TypeError, msg=msg1) as cxt_man:
                    tokenizer.decode(token_ids=invalid_input)

                self.assertEqual(
                    cxt_man.exception.args[0],
                    '`token_ids` must be instance of `List[int]`.',
                    msg=msg2
                )

    def test_invalid_input_remove_special_tokens(self):
        r"""Raise `TypeError` when input is invalid."""
        msg1 = 'Must raise `TypeError` when input is invalid.'
        msg2 = 'Inconsistent error message.'
        examples = (
            0, 1, -1, 0.0, 1.0, math.nan, math.inf, b'',
            [], (), {}, set(), object(), lambda x: x, type, None,
        )

        for invalid_input in examples:
            for tokenizer in self.tokenizers:
                with self.assertRaises(TypeError, msg=msg1) as cxt_man:
                    tokenizer.decode(
                        token_ids=[0, 1, 2, 3, 4],
                        remove_special_tokens=invalid_input
                    )

                self.assertEqual(
                    cxt_man.exception.args[0],
                    '`remove_special_tokens` must be instance of `bool`.',
                    msg=msg2
                )

    def test_return_type(self):
        r"""Return `str`."""
        msg = 'Must return `str`.'
        examples = (
            [0, 1, 2, 3, 4],
            [],
        )

        for token_ids in examples:
            for tokenizer in self.tokenizers:
                sequence = tokenizer.decode(token_ids=token_ids)
                self.assertIsInstance(sequence, str, msg=msg)

    def test_remove_special_tokens(self):
        r"""Return str must remove special token."""
        msg = (
            'Return result must remove special token.'
        )
        examples = (
            (
                [0, 3, 3, 3, 3, 3, 1],
                '[UNK][UNK][UNK][UNK][UNK]'
            ),
        )

        for token_ids, ans_sequence in examples:
            for tokenizer in self.tokenizers:
                self.assertEqual(
                    tokenizer.decode(
                        token_ids=token_ids,
                        remove_special_tokens=True
                    ),
                    ans_sequence,
                    msg=msg
                )


if __name__ == '__main__':
    unittest.main()