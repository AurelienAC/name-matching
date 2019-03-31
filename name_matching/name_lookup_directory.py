from itertools import combinations

from name_normalizer import NameNormalizer
from double_metaphone import DoubleMetaphoneMatcher


class NameLookupDirectory(object):
    """The NameLookupDirectory class allows users to
    store add names in the goal of matching. Internally,
    the class uses the DoubleMetaphoneMatcher class to
    produce name matches. Users can retrieve matched names
    based on strong matches and weak matches by calling the
    instance's strong_matches or weak_matches methods.
    """

    class _NameLookupDirectory(object):

        def __init__(self):
            self.normalizer = NameNormalizer()
            self.metaphone_matcher = DoubleMetaphoneMatcher()
            self._lookup_dict = ({}, {})

        def strong_matches(self):
            """This method returns the name lookup directory
            where strong metaphone matches were produced. The
            keys of the returned dictionary correspond to the
            metaphone. The values correspond to the name identifiers
            whose name metaphones correspond to that particular
            metaphone.

            Returns
            -------
            dict {str: List of obj}
                Returns a dictionary where name ids are mapped
                to matching metaphones.
            """
            return self._lookup_dict[0]

        def weak_matches(self):
            """This method returns the name lookup directory
            where weak metaphone matches were produced. The
            keys of the returned dictionary correspond to the
            metaphone. The values correspond to the name identifiers
            whose name metaphones correspond to that particular
            metaphone.

            Returns
            -------
            dict {str: List of obj}
                Returns a dictionary where name ids are mapped
                to matching metaphones.
            """
            return self._lookup_dict[1]

        def add(self, name, name_id):
            """This method will add a given name and its name id to
            its lookup directory. Specifically, this method will
            normalize and produce metaphones for the names before
            adding them to the directory.

            Parameters
            ----------
            name : str
                A given name.
            named_id : obj
                The identifier of the name.
            """
            norm_name = self.normalizer.normalize_name(name)
            name_combs = self._generate_name_combinations(norm_name)

            self._add_combinations_to_directory(name_combs, name_id)

            return

        def add_names(self, names, name_ids):
            """Given two list, one containing names and the other
            of the ids corresponding to the names, this method will
            add each of those names to its name lookup directory.

            Parameters
            ----------
            names : Iterable of str
                An iterable of names.
            name_ids : Iterable of obj
                An iterable of the corresponding name ids.
            """
            for name, named_id in zip(names, name_ids):
                self.add(name, named_id)

            return

        def _add_combinations_to_directory(self, name_combs, name_id):
            """Given the name combinations for a name's components, this
            method adds each of those combinations' double metaphones
            to its name directory and seperate strong and weak matches.

            Parameters
            ----------
            name_combs : list of tuple
                Corresponds to the list of name combinations for a given
                name.
            name_id : obj
                Corresponds to the name's identifier.
            """
            for comb in name_combs:
                concat_name = ''.join(n for n in comb)
                metaphone_tuple = self.metaphone_matcher.double_metaphone(
                    concat_name
                )

                # Add strong match if not exists
                self._add_name_id_using_metaphone(
                    metaphone_tuple, name_id, 0
                )
                # Add weak match if not exists
                self._add_name_id_using_metaphone(
                    metaphone_tuple, name_id, 1
                )

            return

        def _add_name_id_using_metaphone(self, metaphone_tuple, name_id, key):
            """This method adds a name id to the instance's directory
            of name matches based on the metaphone tuple that is provided.
            The name id is matched to a metaphone based on the provided
            key parameter.
            If the metaphone does not exist within the name sub-directory,
            a new entry is created with that name id.

            Parameters
            ----------
            metaphone_tuple : tuple of str, str
                Corresponds to the double metaphone for a name.
            name_id : obj
                Corresponds to the name's identifier
            key : int
                Corresponds to the instance's sub name directory.
                0 for strong matches, 1 for weak matches.
            """
            if metaphone_tuple[key] in self._lookup_dict[key]:
                if name_id not in self._lookup_dict[key][metaphone_tuple[key]]:
                    self._lookup_dict[key][metaphone_tuple[key]].append(
                        name_id
                    )
            else:
                self._lookup_dict[key][metaphone_tuple[key]] = [name_id]

        def _generate_name_combinations(self, name):
            """This method generates a combination of names based
            on a name's name components. It returns a list of tuples
            where each tuple corresponds to a combination.

            Parameters
            ----------
            name : str
                A name to obtain the combinations from.

            Returns
            -------
            list of tuple
                Returns a list of tuples where each tuple is a name
                combination.
            """
            name_tuple = tuple(name.split(' '))

            combs = []
            combs.append(name_tuple)

            i = len(name_tuple) - 1
            while i > 0:
                combs.extend(combinations(name_tuple, i))

                i -= 1

            return combs

    __directory_instance = None

    def __init__(self):
        if NameLookupDirectory.__directory_instance is None:
            NameLookupDirectory.__directory_instance = \
                NameLookupDirectory._NameLookupDirectory()

    def add(self, name, name_id):
        """This method will add a given name and its name id to
        its lookup directory. Specifically, this method will
        normalize and produce metaphones for the names before
        adding them to the directory.

        Parameters
        ----------
        name : str
            A given name.
        named_id : obj
            The identifier of the name.
        """
        NameLookupDirectory.__directory_instance.add(name, name_id)

    def add_names(self, names, name_ids):
        """Given two list, one containing names and the other
        of the ids corresponding to the names, this method will
        add each of those names to its name lookup directory.

        Parameters
        ----------
        names : Iterable of str
            An iterable of names.
        name_ids : Iterable of obj
            An iterable of the corresponding name ids.
        """
        NameLookupDirectory.__directory_instance.add_names(
            names, name_ids
        )

    def strong_matches(self):
        """This method returns the name lookup directory
        where weak metaphone matches were produced. The
        keys of the returned dictionary correspond to the
        metaphone. The values correspond to the name identifiers
        whose name metaphones correspond to that particular
        metaphone.

        Returns
        -------
        dict {str: List of obj}
            Returns a dictionary where name ids are mapped
            to matching metaphones.
        """
        return NameLookupDirectory.__directory_instance.strong_matches()

    def weak_matches(self):
        """This method returns the name lookup directory
        where strong metaphone matches were produced. The
        keys of the returned dictionary correspond to the
        metaphone. The values correspond to the name identifiers
        whose name metaphones correspond to that particular
        metaphone.

        Returns
        -------
        dict {str: List of obj}
            Returns a dictionary where name ids are mapped
            to matching metaphones.
        """
        return NameLookupDirectory.__directory_instance.weak_matches()


if __name__ == "__main__":
    pass
