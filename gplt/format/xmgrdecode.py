# coding: utf-8
import re


class XmgrDecode():
    """ @brief Decoding xmgrace characters to python """

    def __init__(self, s) -> None:
        self.list = s

    @staticmethod
    def _decoding_str(s):
        # match and replace string to python chars
        map = {
            r'\\s(.*?)\\N' : '_',
            r'\\S(.*?)\\N' : '^'
        }
        for pattern, rep in map.items():
            match = re.search(pattern, s)
            if match:
                return (s[:match.start()]+f'${rep}'+'{'+match.group(1)+'}$'+s[match.end():])
        return s

    def decoding(self):
        """ @brief retrun decoded characters in python """
        # is a str
        if isinstance(self.list, str):
            return self._decoding_str(self.list)
        # is str list
        return [self._decoding_str(s) for s in self.list]
