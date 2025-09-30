# -*- coding: utf-8 -*-
from typing import Dict, List, Set
from .grammar import Grammar, EPS, END

def compute_first(G: Grammar) -> Dict[str, Set[str]]:
    FIRST: Dict[str, Set[str]] = {A: set() for A in G.nonterminals}
    # los terminales tienen FIRST(t) = {t}; no almacenamos para terminales, pero lo usamos en cálculo
    changed = True
    while changed:
        changed = False
        for A, alts in G.prods.items():
            for rhs in alts:
                # rhs puede ser [ε] o secuencia de símbolos
                if rhs == [EPS]:
                    if EPS not in FIRST[A]:
                        FIRST[A].add(EPS); changed = True
                    continue
                # Avanza por los símbolos acumulando FIRST
                nullable_prefix = True
                for X in rhs:
                    if X in G.terminals:
                        if X not in FIRST[A]:
                            FIRST[A].add(X); changed = True
                        nullable_prefix = False
                        break
                    elif X in G.nonterminals:
                        before = len(FIRST[A])
                        FIRST[A].update(sym for sym in FIRST[X] if sym != EPS)
                        changed |= (len(FIRST[A]) != before)
                        if EPS in FIRST[X]:
                            nullable_prefix = True
                        else:
                            nullable_prefix = False
                            break
                    else:
                        # símbolo desconocido -> tratarlo como terminal literal
                        if X not in FIRST[A]:
                            FIRST[A].add(X); changed = True
                        nullable_prefix = False
                        break
                if nullable_prefix:
                    if EPS not in FIRST[A]:
                        FIRST[A].add(EPS); changed = True
    return FIRST

def compute_follow(G: Grammar, FIRST: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
    FOLLOW: Dict[str, Set[str]] = {A: set() for A in G.nonterminals}
    FOLLOW[G.start].add(END)
    changed = True
    while changed:
        changed = False
        for A, alts in G.prods.items():
            for rhs in alts:
                # recorremos Beta y aplicamos reglas de FOLLOW
                for i, B in enumerate(rhs):
                    if B not in G.nonterminals:
                        continue
                    # lo que sigue de B es beta = rhs[i+1:]
                    beta = rhs[i+1:]
                    if not beta:
                        # Regla 3: si beta vacío -> FOLLOW(A) ⊆ FOLLOW(B)
                        before = len(FOLLOW[B])
                        FOLLOW[B].update(FOLLOW[A])
                        changed |= (len(FOLLOW[B]) != before)
                    else:
                        # Añadir FIRST(beta) \ {ε} a FOLLOW(B)
                        first_beta = first_of_seq(beta, FIRST, G)
                        before = len(FOLLOW[B])
                        FOLLOW[B].update(x for x in first_beta if x != EPS)
                        changed |= (len(FOLLOW[B]) != before)
                        # si beta =>* ε, entonces FOLLOW(A) ⊆ FOLLOW(B)
                        if EPS in first_beta:
                            before = len(FOLLOW[B])
                            FOLLOW[B].update(FOLLOW[A])
                            changed |= (len(FOLLOW[B]) != before)
    return FOLLOW

def first_of_seq(seq: List[str], FIRST: Dict[str, Set[str]], G: Grammar) -> Set[str]:
    out: Set[str] = set()
    nullable = True
    for X in seq:
        if X in G.terminals:
            out.add(X); nullable = False; break
        elif X in G.nonterminals:
            out.update(sym for sym in FIRST[X] if sym != EPS)
            if EPS not in FIRST[X]:
                nullable = False; break
        else:
            # literal desconocido => terminal
            out.add(X); nullable = False; break
    if nullable: out.add(EPS)
    return out
