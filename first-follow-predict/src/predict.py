# -*- coding: utf-8 -*-
from typing import Dict, List, Set, Tuple
from .grammar import Grammar, EPS
from .first_follow import compute_first, compute_follow, first_of_seq

def compute_predict(G: Grammar) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]], Dict[Tuple[str, Tuple[str, ...]], Set[str]]]:
    FIRST = compute_first(G)
    FOLLOW = compute_follow(G, FIRST)
    PRED: Dict[Tuple[str, Tuple[str, ...]], Set[str]] = {}

    for A, rhs in G.productions():
        key = (A, tuple(rhs))
        first_alpha = set()
        if rhs == [EPS]:
            first_alpha = {EPS}
        else:
            first_alpha = first_of_seq(rhs, FIRST, G)
        pred = set(x for x in first_alpha if x != EPS)
        if EPS in first_alpha:
            pred.update(FOLLOW[A])
        PRED[key] = pred
    return FIRST, FOLLOW, PRED

def build_ll1_table(G: Grammar, PRED) -> Dict[Tuple[str, str], Tuple[str, List[str]]]:
    """ Devuelve tabla LL(1): (A, a) -> (A -> α). Reporta conflictos con claves repetidas. """
    table: Dict[Tuple[str, str], Tuple[str, List[str]]] = {}
    for (A, rhs), lookaheads in PRED.items():
        for a in lookaheads:
            key = (A, a)
            if key in table:
                # conflicto LL(1)
                prev = table[key]
                raise ValueError(f"Conflicto LL(1) en celda {key}: {prev} / {(A, list(rhs))}")
            table[key] = (A, list(rhs))
    return table
