#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains tools for operating with road weather station database
using condition strings and aliases.

This module shall be imported by Dash ``app.py``.
"""
import pandas

def eliminate_umlauts(x):
    """
    Converts ä and ö into a and o.
    """
    umlauts = {
        'ä': 'a',
        'Ä': 'A',
        'ö': 'o',
        'Ö': 'O'
    }
    for k in umlauts.keys():
        x = x.replace(k, umlauts[k])

    return x

def to_pg_identifier(x):
    """
    Converts x (string) such that it can be used as table or column 
    identifier in PostgreSQL.
    Raises error if x contains fatally invalid parts, e.g.
    whitespaces or leading digit.

    .. note:: Pg identifier length max is 63 characters.
        To avoid too long final identifiers, max length of x here
        is 40 characters, which should be enough for site names too.
    """
    x = x.strip()
    old_x = x
    x = x.lower()
    x = eliminate_umlauts(x)

    if x[0].isdigit():
        errtext = 'String starts with digit:\n'
        errtext += old_x + '\n'
        errtext += '^'
        raise ValueError(errtext)

    for i, c in enumerate(x):
        if not (c.isalnum() or c == '_'):
            errtext = 'String contains whitespace or non-alphanumeric character:\n'
            errtext += old_x + '\n'
            errtext += '~' * i + '^'
            raise ValueError(errtext)

    return x

class PrimaryBlock:
    """
    Represents a logical condition of sensor value
    with information of site name and station id.
    A Block eventually renders as boolean column in temporary db tables.
    For PostgreSQL compatibility, umlauts convert to a and o,
    and all strings are made lowercase.

    # TODO example
    :Example:
        >>> Block('AbcÄÖ_Location', 'D2', 3, 's1122#KITKA3_LUKU >= 0.30')
        {'site': 'abcao_location',
        'alias': 'd2_3',
        'master_alias': 'd2',
        'station_id': 's1122',
        'sensor_name': 'kitka3_luku',
        'logical_operator': '>=',
        'value_str': '0.3',
        }

    # TODO params
    """
    def __init__(self, site_name, master_alias, order_nr, raw_condition):
        self.site = eliminate_umlauts(site_name).lower()
        self.master_alias = master_alias.lower()
        self.alias = self.master_alias + '_' + str(order_nr)

def make_aliases(raw_cond, master_alias):
    """
    Convert raw condition string into SQL clause of alias blocks
    and detect condition type (primary or secondary).

    Primary condition consists of station#sensor logicals only.
    Secondary condition contains existing primary conditions.

    Master alias must be a valid SQL table name,
    preferably of format letter-number, e.g. "A1".
    Subaliases will be suffixed like _1, _2, ...
    
    :Example:
        >>> make_aliases(raw_cond='(s1122#TIENPINNAN_TILA3 = 8 \
            OR (s1122#KITKA3_LUKU >= 0.30 AND s1122#KITKA3_LUKU < 0.4)) \
            AND s1115#TIE_1 < 2', 
            master_alias='D2')
        {
        'type': 'primary',
        'alias_condition': '(D2_1 OR (D2_2 AND D2_3)) AND D2_4',
        'aliases': {
            'D2_1': {'st': 's1122', 'lgc': 'TIENPINNAN_TILA3 = 8'},
            'D2_2': {'st': 's1122', 'lgc': 'KITKA3_LUKU >= 0.30'},
            'D2_3': {'st': 's1122', 'lgc': 'KITKA3_LUKU < 0.4'}
            'D2_4': {'st': 's1115', 'lgc': 'TIE_1 < 2'}
            }
        }

        >>> make_aliases(raw_cond='D2 AND C33', master_alias='DC')
        {
        'type': 'secondary',
        'alias_condition': 'D2 AND C33'
        'aliases': {
            'D2': {'st': None, 'lgc': 'D2'}
            'C33': {'st': None, 'lgc': 'C33'}
            }
        }
    
    :param raw_cond: raw condition string
    :type raw_cond: string
    :param master_alias: master alias string
    :type master_alias: string
    :return: dict of condition type, alias clause and alias pairs
    :rtype: dict
    :raises: # TODO error type?
    """
    return None
    # TODO write make_aliases()

class Condition:
    """
    Single condition, its aliases, query handling and results.
    
    :Example:
    # TODO example
    
    # TODO Condition init parameters and results
    """
    def __init__(self, raw_condition_string):
        pass
    # TODO write Condition
        
class CondCollection:
    """
    A set of conditions. Main task to prevent duplicates.
    
    # TODO CondCollection init parameters and results
    """
    
    # TODO write CondCollection
    pass