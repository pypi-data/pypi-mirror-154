from .apriori import apriori
from .cumulate import _vertical_cumulate
from .Parser import Parser
from .HTAR import HTAR_BY_PG
from .utility import flatten_list


class TGAR(object):

    def apriori(self, filepath, min_supp, min_conf, parallel_count=False):
        """
        :param filepath: A dataset filepath
        :param min_supp: User-defined minimum support
        :param min_conf: User-defined minimum confidence
        :param parallel_count: Optional parameter to perform candidate count in parallel
        :return: Set of association rules
        """
        apriori_database = Parser().parse(filepath=filepath)
        rules = apriori(database=apriori_database, min_support=min_supp,
                        min_confidence=min_conf,
                        parallel_count=parallel_count)
        for rule in rules:
            print(apriori_database.printAssociationRule(rule))

    def cumulate(self, filepath, taxonomy_filepath, min_supp, min_conf, min_r, parallel_count=False):
        """
        :param filepath: A dataset filepath
        :param taxonomy_filepath: A taxonomy filepath
        :param min_supp: User-defined minimum support
        :param min_conf: User-defined minimum confidence
        :param min_r: User-defined minimum R interesting measure
        :param parallel_count: Optional parameter to set parallel counting for supports
        :return: Set of association rules
        """
        cumulate_database = Parser().parse(filepath=filepath, taxonomy_filepath=taxonomy_filepath)
        rules = _vertical_cumulate(vertical_database=cumulate_database,
                                   min_supp=min_supp,
                                   min_conf=min_conf,
                                   min_r=min_r,
                                   parallel_count=parallel_count)
        for rule in rules:
            print(cumulate_database.printAssociationRule(rule))

    def htar(self, filepath, min_supp, min_conf, lam = -1):
        """
        :param filepath: A dataset filepath
        :param min_supp: Minimum support to consider frequent in inner time granules
        :param min_conf: Minimum confidence to consider a frequent rule
        :param lam: Minimum support to consider frequent in leaf time granules
        :return: A set of Association rules indexed by time granule.
        """
        htar_database = Parser().parse(filepath=filepath, usingTimestamp=True)
        final_lam = lam
        if(final_lam == -1):
            final_lam = min_supp
        rules = HTAR_BY_PG(database=htar_database,
                           min_rsup=min_supp,
                           min_rconf=min_conf,
                           lam=final_lam)
        for pg in rules:
            print('                          ')
            print('Time Granule: ' + str(pg))
            print('=========================')
            for rule in rules[pg]:
                print(htar_database.printAssociationRule(rule))

    def htgar(self, filepath, taxonomy_filepath, min_supp, min_conf, min_r, lam = -1):
        """
        :param filepath: A dataset filepath
        :param taxonomy_filepath: A taxonomy filepath
        :param min_supp: Minimum support to consider frequent in inner time granules
        :param min_conf: Minimum confidence to consider a frequent rule
        :param min_r: User-defined minimum R interesting measure
        :param lam: Minimum support to consider frequent in leaf time granules

        :return: A set of Association rules indexed by time granule.
        """
        htgar_database = Parser().parse(filepath=filepath, taxonomy_filepath=taxonomy_filepath, usingTimestamp=True)
        final_lam = lam
        if (final_lam == -1):
            final_lam = min_supp
        rules = HTAR_BY_PG(database=htgar_database,
                           min_rsup=min_supp,
                           min_rconf=min_conf,
                           lam=final_lam,
                           generalized_rules=True,
                           min_r=min_r)
        all_rules = flatten_list(list(rules.values()))
        for rule in all_rules:
            print(htgar_database.printAssociationRule(rule))
