from unittest import TestCase
from unittest.mock import Mock, call

from app_types import PageData
from utils import merge_hyphenated_words, fix_newlines, clean_text, remove_multiple_newlines


class TestMergeHyphenatedWords(TestCase):
    def test_single_hyphenated_word(self):
        text = "This is a hyphen-\nated word."
        expected = "This is a hyphenated word."
        self.assertEqual(merge_hyphenated_words(text), expected)

    def test_multiple_hyphenated_words(self):
        text = "This is a hyphen-\nated word and anoth-\ner hyphenated word."
        expected = "This is a hyphenated word and another hyphenated word."
        self.assertEqual(merge_hyphenated_words(text), expected)

    def test_no_hyphenated_words(self):
        text = "This is a text without any hyphenated words."
        expected = "This is a text without any hyphenated words."
        self.assertEqual(merge_hyphenated_words(text), expected)


class TestFixNewlines(TestCase):
    def test_single_newline(self):
        text = "This is a line with\na single newline."
        expected = "This is a line with a single newline."
        self.assertEqual(fix_newlines(text), expected)

    def test_double_newline(self):
        text = "This is a line with\n\na double newline."
        expected = "This is a line with\n\na double newline."
        self.assertEqual(fix_newlines(text), expected)

    def test_mixed_newlines(self):
        text = "This is a line with\na single newline and\n\na double newline."
        expected = "This is a line with a single newline and\n\na double newline."
        self.assertEqual(fix_newlines(text), expected)


class TestRemoveMultipleNewlines(TestCase):
    def test_remove_multiple_newlines_case1(self):
        input_text = "page one\n\npage two\n\n\npage three"
        expected_output = "page one\npage two\npage three"
        result = remove_multiple_newlines(input_text)
        self.assertEqual(result, expected_output)

    def test_remove_multiple_newlines_case2(self):
        input_text = "page one\n\n\n\npage two"
        expected_output = "page one\npage two"
        result = remove_multiple_newlines(input_text)
        self.assertEqual(result, expected_output)

    def test_remove_multiple_newlines_case3(self):
        input_text = "page one\npage two\npage three"
        expected_output = "page one\npage two\npage three"
        result = remove_multiple_newlines(input_text)
        self.assertEqual(result, expected_output)

    def test_remove_multiple_newlines_case4(self):
        input_text = ""
        expected_output = ""
        result = remove_multiple_newlines(input_text)
        self.assertEqual(result, expected_output)


class TestCleanText(TestCase):
    def test_clean_text(self):
        fake_function_1 = Mock(side_effect=lambda text: text)
        fake_function_2 = Mock(side_effect=lambda text: text)
        fake_function_3 = Mock(side_effect=lambda text: text)

        result = clean_text(
            pages=[
                PageData(num=1, text='page one'),
                PageData(num=2, text='page two'),
                PageData(num=3, text='page three'),
            ],
            cleaning_functions=[
                fake_function_1,
                fake_function_2,
                fake_function_3
            ]
        )

        expected_calls = [call('page one'), call('page two'), call('page three')]

        self.assertEqual(fake_function_1.call_args_list, expected_calls)
        self.assertEqual(fake_function_2.call_args_list, expected_calls)
        self.assertEqual(fake_function_3.call_args_list, expected_calls)

        expected_result = [
            PageData(num=1, text='page one'),
            PageData(num=2, text='page two'),
            PageData(num=3, text='page three'),
        ]
        self.assertEqual(result, expected_result)
