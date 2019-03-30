from json import load
import re

from unidecode import unidecode


class NameNormalizer(object):
    """The NameNormalizer class is used to cleanse names before they
    are compared.
    """
    ABBREVIATIONS = 'abbreviations.json'
    TITLES = 'titles.json'
    NAME_SPLITTER = re.compile(r'[A-Za-z]+')

    def __init__(self, abbreviations=ABBREVIATIONS, titles=TITLES):
        abbreviations_dict = NameNormalizer.__load(abbreviations)
        self.abbreviations = abbreviations_dict['abbreviations']
        self.titles = set(NameNormalizer.__load(titles))

    @staticmethod
    def __load(file_path):
        """Loads JSON files during the object's instantiation."""
        with open(file_path, 'r') as f:
            return load(f)

    def normalize_name(self, name):
        """This method is designed to cleanse a name so that it may be
        compared with others in a normalized way. The cleansing process:
            - re-encodes the name in ASCII
            - converts all characters to lower case
            - extracts and sorts the name components in alphabetical order
            - removes titles found in the name
            - expands name abbreviations to their full form
            - concatenates the components into a string

        Parameters
        ----------
        str
            Corresponds to a name.

        Returns
        -------
        str
            A string representing the normalized form of the name parameter.
            Returns an empty string if the value is None or is not a string.
        """
        if name is None or not isinstance(name, str):
            return ''

        name = self._normalize_unicode_to_ascii(name)

        name = self._to_lower(name)

        names = self._split_name_into_components(name)

        names = sorted(names)

        names = self._remove_titles(names)

        names = self._expand_name_abbreviations(names)

        return ' '.join(name for name in names)

    def _expand_name_abbreviations(self, name_components):
        """This method yields a generator of values corresponding
        to the expanded forms of name abbreviations or the name
        itself if not an abbreviation.

        Parameters
        ----------
        name_components : Iterable
            Corresponds to a collection of name components.

        Yields
        ------
        str
            Yields name components in their expanded form if the
            name components were in abbreviated form or the name
            component otherwise.
        """
        for name in name_components:
            if name in self.abbreviations:
                yield self.abbreviations[name]
            else:
                yield name

    def _normalize_unicode_to_ascii(self, name):
        """Re-encodes a string to ASCII."""
        return unidecode(name)

    def _remove_titles(self, name_components):
        """This method yields a generator whose
        values do not correspond to titles given
        a list of name components.

        Parameters
        ----------
        name_components : Iterable
            An iterable list whose elements correspond
            to name components.

        Yields
        ------
        str
            A name component if it is not a title.
        """
        for name in name_components:
            if name not in self.titles:
                yield name

    def _split_name_into_components(self, name):
        """This method yields the name components of a name string."""
        for match in NameNormalizer.NAME_SPLITTER.finditer(name):
            yield match.group(0)

    def _to_lower(self, name):
        """Converts a name to lower case."""
        return name.lower()


if __name__ == '__main__':
    pass
