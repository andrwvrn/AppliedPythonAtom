#!/usr/bin/env python
# coding: utf-8


def revert_linked_list(head):
    """
    A -> B -> C should become: C -> B -> A
    :param head: LLNode
    :return: new_head: LLNode
    """
    # TODO: реализовать функцию
    next_node = None

    while head:
        remaining_nodes = head.next_node
        head.next_node = next_node
        next_node = head
        head = remaining_nodes

    return next_node
