def flatten_linked_list(linked_list):
    if not linked_list:
        return []

    head, tail = linked_list
    return [head] + flatten_linked_list(tail)

def map_linked_list(function, linked_list):
    if not linked_list:
        return None

    head, tail = linked_list
    return (function(head), map_linked_list(function, tail))

def len_linked_list(linked_list):
    if not linked_list:
        return 0

    head, tail = linked_list
    return 1 + len_linked_list(tail)