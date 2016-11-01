"""This module contains utility functions to handle strings."""
import re


class Text:
    """
    **Text** class provides utility methods to handle strings.
    """
    @staticmethod
    def condensate(txt):
        """
        Returns a condensed version of the given string, trimming, removing line breaks and multiple spaces.

        :param txt: input text
        :return: condensed version of the given string, trimming, removing line breaks and multiple spaces.
        """
        s = txt.strip()
        s = Text.remove_line_breaks(s)
        s = Text.remove_multiple_spaces(s)
        return s

    @staticmethod
    def remove_line_breaks(txt):
        """
        Returns a one-line version of the given string, removing line breaks.

        :param txt: input text.
        :return: one-line version of the given string, removing line breaks.
        """
        return txt.replace('\n', ' ').replace('\r', '')

    @staticmethod
    def remove_multiple_spaces(txt):
        """
        Returns a new version of the given string, removing duplicated spaces.

        :param txt: input text.
        :return: new version of the given string, removing duplicated spaces.
        """
        return re.sub("[\s]+", " ", txt)