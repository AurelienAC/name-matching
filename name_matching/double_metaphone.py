from enum import Enum

from metaphone import doublemetaphone


class Threshold(Enum):
    WEAK = 0
    NORMAL = 1
    STRONG = 2

    @staticmethod
    def from_string(threshold):
        if threshold is None or not isinstance(threshold, str):
            raise NotImplementedError()

        if threshold.upper() == 'WEAK':
            return Threshold.WEAK
        elif threshold.upper() == 'NORMAL':
            return Threshold.NORMAL
        elif threshold.upper() == 'STRONG':
            return Threshold.STRONG

        raise NotImplementedError()

    @staticmethod
    def from_int(threshold):
        if threshold == 0:
            return Threshold.WEAK
        elif threshold == 1:
            return Threshold.NORMAL
        elif threshold == 2:
            return Threshold.STRONG

        raise NotImplementedError()


class DoubleMetaphoneMatcher(object):
    """The DoubleMetaphoneMatcher class is designed to provide
    a means to compare names using the double metaphone matching
    algorithm.
    """
    def __init__(self):
        pass

    def is_double_metaphone_match(self, name1, name2,
                                  threshold=Threshold.STRONG):
        """This method compares the double metaphone tuples produced
        for each of the name parameters using the double metaphone
        algorithm and given a leniency threshold.

        Parameters
        ----------
        name1 : str
            A name to compare another name against.
        name2 : str
            A name to compare another name with.
        threshold : Union[Threshold, int, str], optional
            The leniency threshold to allow when comparing both names.
            If the supplied parameter is not of the Threshold type,
            values must be 0/WEAK, 1/NORMAL, or 2/STRONG.

        Returns
        -------
        bool
            Returns True if the name parameters match; False otherwise.

        Raises
        ------
        ValueError
            If either of the name parameters are None or if the value
            contained by the threshold parameter is not implemented by
            the Threshold Enum class.
        """
        if name1 is None or name2 is None:
            raise ValueError('Neither of the name parameters can be None.')

        thresh = self._ensure_threshold_is_enum(threshold)

        metaphone1 = self._double_metaphone(name1)
        metaphone2 = self._double_metaphone(name2)

        is_a_match = self._compare_metaphones(metaphone1, metaphone2, thresh)

        return is_a_match

    def _ensure_threshold_is_enum(self, threshold):
        """This method ensures that the threshold parameter
        supplied to the is_double_metaphone_match method is
        an adequate Threshold enumeration.

        Parameters
        ----------
        threshold : Union[Threshold, int, str]
            A threshold enumeration supplied as a Threshold
            Enum instance, an int or a str representation.

        Returns
        -------
        Threshold
            Returns the Threshold Enumeration value corresponding
            to the threshold parameter.

        Raises
        ------
        ValueError
            Raises a ValueError if the threshold parameter does
            not correspond to an implemented Threshold enumeration.
        """
        if isinstance(threshold, Threshold):
            return threshold

        thresh = None

        if isinstance(threshold, str):
            try:
                thresh = Threshold.from_string(threshold)
            except NotImplementedError:
                pass

        if isinstance(threshold, int):
            try:
                thresh = Threshold.from_int(threshold)
            except NotImplementedError:
                pass

        if thresh is None:
            raise ValueError('The threshold value you gave is invalid.')
        else:
            return thresh

    def _double_metaphone(self, name):
        """This method returns the metaphone values
        associated with a name as a tuple. See the
        metaphone.doublemetaphone method for implementation
        details.

        Parameters
        ----------
        name : str
            A name as a string.

        Returns
        -------
        tuple of str, str
            The metaphone values associated with the
            name parameter.
        """
        return doublemetaphone(name)

    def _compare_metaphones(self, m1, m2, threshold):
        """This method compares the metaphones associated
        with two names given a leniency threshold. Depending
        on the threshold value, the comparisons will be more
        or less lenient.

        Parameters
        ----------
        m1 : tuple of str, str
            A tuple corresponding to the metaphones for a
            given name.
        m2 : tuple of str, str
            A tuple corresponding to the metaphones for a
            given name.
        threshold : Threshold
            The threshold value to use for comparing the
            metaphone values.

        Returns
        -------
        bool
            True if the metaphones match given the threshold;
            False otherwise.
        """
        if threshold == Threshold.WEAK:
            if m1[1] == m2[1]:
                return True
        elif threshold == Threshold.NORMAL:
            if m1[0] == m2[1] or m1[1] == m2[0]:
                return True
        else:
            if m1[0] == m2[0]:
                return True

        return False


if __name__ == "__main__":
    pass
