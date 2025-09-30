# -*- coding: utf-8 -*-
import argparse
from .grammar import load_grammar, EPS, END
from .predict import compute_predict, build_ll1_table

def fmt_set(S):
    return "{" + ", ".join(sorted(S)) + "}"

def main():
    ap = argparse.ArgumentParser(description="FIRST, FOLLOW y PREDICT (LL(1))")
    ap.add_argument("--grammar", required=True, help="Ruta a archivo de gramática (.txt)")
    ap.add_argument("--table", action="store_true", help="Construir tabla LL(1) y validar conflictos")
    args = ap.parse_args()

    G = load_grammar(args.grammar)
    FIRST, FOLLOW, PRED = compute_predict(G)

    print("== Resumen de la Gramática ==")
    print(f"Inicial: {G.start}")
    print(f"No terminales: {sorted(G.nonterminals)}")
    print(f"Terminales: {sorted(G.terminals)}\n")

    print("== FIRST ==")
    for A in sorted(G.nonterminals):
        print(f"FIRST({A}) = {fmt_set(FIRST[A])}")

    print("\n== FOLLOW ==")
    for A in sorted(G.nonterminals):
        print(f"FOLLOW({A}) = {fmt_set(FOLLOW[A])}")

    print("\n== PREDICT por producción ==")
    for (A, rhs), look in PRED.items():
        rhs_str = " ".join(rhs)
        print(f"PREDICT({A} -> {rhs_str if rhs else EPS}) = {fmt_set(look)}")

    if args.table:
        print("\n== Tabla LL(1) ==")
        try:
            table = build_ll1_table(G, PRED)
            # Mostrar compacta por NT
            by_nt = {}
            for (A, a), prod in table.items():
                by_nt.setdefault(A, []).append((a, prod))
            for A in sorted(by_nt):
                entries = ", ".join([f"{t}→{' '.join(rhs) if rhs else EPS}" for t, (_, rhs) in sorted(by_nt[A])])
                print(f"{A}: {entries}")
            print("\n✓ Sin conflictos LL(1).")
        except ValueError as e:
            print(f"\n✗ Conflicto: {e}")

if __name__ == "__main__":
    main()
