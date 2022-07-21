import requests
from requests.exceptions import HTTPError
from typing import Collection
import random


class WordHandler:
    _WORD_SITE: str = "https://www.mit.edu/~ecprice/wordlist.10000"
    _STATUS_CODE_OK: int = 200
    _MIN_WORD_SIZE: int = 3

    def __init__(self, max_size: int = 4):
        """Word handler for words smaller than a given maximum size.

        Args:
            max_size (int, optional): The maximum lenght of a word. Defaults to 4.

        Raises:
            ValueError: If the provided maximum size is lower than the minimum size length.
        """
        if max_size < self._MIN_WORD_SIZE:
            raise ValueError(
                f"ERROR: The provided max size '{max_size}' is not greater than or equal to the minimum size {self._MIN_WORD_SIZE}"
            )
        self.max_size = max_size
        word_list = self._request_new_word_list()
        self._words = self._randomize_words(word_list)

    def _request_new_word_list(self) -> Collection[str]:
        """Creates a word list with words smaller than the given maximum size.

        Returns:
            Collection[str]: A collection of words smaller than the maximum size.
        """
        try:
            response = requests.get(self._WORD_SITE)
        except HTTPError as http_err:
            print(f"ERROR: HTTPError occured: {http_err}")
        response.enconding = "utf-8"
        content = response.text.splitlines()

        return list(word for word in content if len(word) <= self.max_size)

    def _randomize_words(self, words: Collection[str]) -> Collection[str]:
        """Returns the same collection of words but shuffled.

        Args:
            words (Collection[str]): self-explanatory

        Returns:
            Collection[str]: A shuffled version of the 'words' parameter
        """
        return random.sample(words, len(words))

    def get_current_word(self) -> str:
        """Retrieve the current word

        Returns:
            str: The current word
        """
        return self._current_word

    def fetch_new_word(self) -> str:
        """Tries to retrieve a word from the word collection. If the collection is empty
        a new collection is created and the first word from that collection is returned.

        Returns:
            str: A new word
        """
        try:
            self._current_word = self._words.pop()
            return self._current_word
        except IndexError:
            print(f"INFO: Word list is empty, creating a new word list")
            word_list = self._request_new_word_list(self.max_size)
            self._words = self._randomize_words(word_list)
            self._current_word = self._words.pop()
            return self._current_word
