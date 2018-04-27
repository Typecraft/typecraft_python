import nltk

LEGAL_NE_TAGS = [
    'ORGANIZATION',
    'PERSON',
    'LOCATION',
    'DATE',
    'TIME',
    'MONEY',
    'PERCENT',
    'FACILITY',
    'GPE',
    'NE'
]


def _parse_entity_tree_to_string(tree, use_tags=False):
    return_string = ""
    for child in tree:
        if isinstance(child, nltk.tree.Tree):
            return_string += _parse_entity_tree_to_string(child) + " "
        else:
            return_string += child[0] + " "
    return return_string


def _parse_entity_tree_for_named_entities(tree):
    parsed_entity_names = []

    if hasattr(tree, 'label') and tree.label() in LEGAL_NE_TAGS:
        parsed_entity_names.append((tree.label(), _parse_entity_tree_to_string(tree)))
    # We might recurse down to the string level, in which case we simply return
    # So we check if it is in fact a tree
    elif isinstance(tree, nltk.tree.Tree):
        for child in tree:
            parsed_entity_names.extend(_parse_entity_tree_for_named_entities(child))
    return parsed_entity_names
