"""
This module contains functionality for translating various tagsets to the
Typecraft tagset.
"""

import six

# noinspection SpellCheckingInspection
POS_CONVERSIONS = {
    "$": "PUN",
    "$(": "PUN",
    "$.": "PUN",
    "adj": "ADJ",
    "adja": "ADJ",
    "adjd": "ADJ",
    "adv": "ADV",
    "advprt": "PRT",
    "advs": "ADV",
    "appo": "PPOST",
    "appr": "PREP",
    "apprart": "PREP",
    "apzr": "",
    "art": "ART",
    "c": "COMP",
    "card": "CARD",
    "conj": "CONJ",
    "deg": "PRT",
    "expl": "EXPL",
    "fm": "",
    "inf": "PRTinf",
    "interjct": "INTRJCT",
    "itj": "INTRJCT",
    "kokom": "PRT",
    "kon": "CONJC",
    "koui": "CONJS",
    "koui": "CONJSINF",
    "kous": "CONJS",
    "ne": "Np",
    "net": "",
    "nn": "N",
    "nprop": "Np",
    "ord": "ORD",
    "p": "PREP",
    "pav": "ADV",
    "pav": "PN",
    "pdat": "PN",
    "pdat": "PNdem",
    "pds": "PN",
    "pds": "PNdem",
    "piat": "PN",
    "pidat": "",
    "pis": "PN",
    "pninterr": "Wh",
    "pnrefl": "PNrefl",
    "pnresmptv": "PNrel",
    "poss": "PRTposs",
    "pper": "",
    "pper": "PN",
    "pposat": "Pnposs",
    "pposs": "Pnposs",
    "prelat": "PNrel",
    "prels": "Pnrel",
    "prf": "Pnrefl",
    "prtcmpr": "PRT",
    "ptka": "PRT",
    "ptkant": "PRT",
    "ptkant": "PRTresp",
    "ptkneg": "PRT",
    "ptkneg": "PRTneg",
    "ptkvz": "PRTv",
    "ptkzu": "PRTinf",
    "pun": "PUN",
    "punct": "PUN",
    "pwat": "PN",
    "pwat": "PROint",
    "pwav": "PN",
    "pwav": "PROint",
    "pws": "PROint",
    "pws": "Wh",
    "quantinterr": "QUANT",
    "sgml": "",
    "spell": "",
    "trunc": "",
    "trunc": "TRUNC",
    "v-ditr": "Vdtr",
    "v-ditrobl": "V",
    "v-extrapos": "V",
    "v-extraposobl": "V",
    "v-intr": "Vitr",
    "v-introbl": "VitrOBL",
    "v-intrscpr": "V",
    "v-obextrapos": "V",
    "v-presntn": "V",
    "v-presntnobl": "V",
    "v-tr": "Vtr",
    "v-trobl": "VtrOBL",
    "v-trscpr": "V",
    "vafin": "AUX",
    "vaimp": "AUX",
    "vainf": "AUX",
    "vapp": "AUX",
    "vapp": "PTCP",
    "vaux": "AUX",
    "vcopa": "COP",
    "vcopn": "COP",
    "vmfin": "Vmod",
    "vminf": "Vmod",
    "vmpp": "PTCP",
    "vmpp": "Vmod",
    "vrefl": "V",
    "vrefl-ob": "V",
    "vrefl-obl": "V",
    "vrefl-presobl": "V",
    "vrefl-scpr": "V",
    "vrefl-trobl": "V",
    "vvfin": "V",
    "vvimp": "V",
    "vvinf": "V",
    "vvizu": "V",
    "vvpp": "V",
    "xy": "XY"
}


def get_pos_conversions(pos, tagset='tc'):
    """
    Gets a pos conversion.

    :param pos:
    :param tagset: Currently not used, as the only mapping supported is 'tc'
    :return:
    """
    assert isinstance(pos, six.string_types)
    potential_tag = POS_CONVERSIONS.get(pos.lower())
    if potential_tag:
        return potential_tag
    else:
        return pos


def get_gloss_conversions(gloss, tagset='tc'):
    """
    Gets a gloss conversion into the given tagset.
    Currently acts as the identity, as we don't have any conversions registered yet.

    :param gloss:
    :param tagset: Currently not used, as the only mapping supported is 'tc'
    :return:
    """
    return gloss
