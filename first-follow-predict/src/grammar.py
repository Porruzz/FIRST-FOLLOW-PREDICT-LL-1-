# -*- coding: utf-8 -*-
from typing import Dict, List, Set, Tuple

EPS = "ε"
END = "$"

class Grammar:
    def __init__(self, start: str, prods: Dict[str, List[List[str]]]):
        self.start: str = start
        self.prods: Dict[str, List[List[str]]] = prods
        self.nonterminals: Set[str] = set(prods.keys())
        # Terminals = todo símbolo que NO es NT (y no es ε)
        syms = set()
        for A, alts in prods.items():
            for rhs in alts:
                syms.update(rhs)
        self.terminals: Set[str] = {t for t in syms if t not in self.nonterminals and t != EPS}

    def productions(self) -> List[Tuple[str, List[str]]]:
        out = []
        for A, alts in self.prods.items():
            for rhs in alts:
                out.append((A, rhs))
        return out

def _parse_rhs(rhs: str) -> List[List[str]]:
    alts = []
    for alt in rhs.split("|"):
        alt = alt.strip()
        if alt == "" or alt == EPS:
            alts.append([EPS])
        else:
            alts.append(alt.split())
    return alts

def load_grammar(path: str) -> Grammar:
    prods: Dict[str, List[List[str]]] = {}
    start = None
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"): 
                continue
            if "->" not in line:
                raise ValueError(f"Línea inválida: {line}")
            left, right = line.split("->", 1)
            A = left.strip()
            alts = _parse_rhs(right.strip())
            prods.setdefault(A, []).extend(alts)
            if start is None:
                start = A
    if not start:
        raise ValueError("Gramática vacía.")
    return Grammar(start, prods)
