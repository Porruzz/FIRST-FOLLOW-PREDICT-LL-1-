FIRST – FOLLOW – PREDICT (LL(1))

Este proyecto en Python calcula los conjuntos FIRST, FOLLOW y PREDICT de una gramática libre de contexto, y además construye la tabla LL(1) para verificar si la gramática es apta para análisis predictivo.

Estructura
first-follow-predict/
├─ grammars/
│  ├─ aritmetica.txt      # Gramática de expresiones
│  └─ ejemplo_p6.txt      # Gramática de la presentación 6
└─ src/
   ├─ main.py
   ├─ grammar.py
   ├─ first_follow.py
   └─ predict.py

Formato de gramática

Cada producción: A -> α | β

ε representa epsilon.

Separar símbolos con espacios.

Ejemplo (ejemplo_p6.txt):

A -> a B C
B -> b bas | big C boss
C -> ε | c

Uso en Kali

Ejecutar desde la raíz del proyecto:

# Calcular FIRST, FOLLOW y PREDICT
python -m src.main --grammar grammars/ejemplo_p6.txt

# Con tabla LL(1)
python -m src.main --grammar grammars/ejemplo_p6.txt --table

Ejemplo de salida
== FIRST ==
FIRST(A) = {a}
FIRST(B) = {b, big}
FIRST(C) = {c, ε}

== FOLLOW ==
FOLLOW(A) = {$}
FOLLOW(B) = {c, ε}
FOLLOW(C) = {$}
