# Compiler-Study

컴파일러 강의 들으면서 구현한 알고리즘


## NFA to DFA
- `RegExpr -> ε-NFA -> DFA -> minimized-DFA`
- TODO

---
## FIRST and FOLLOW [(first_follow.py)](./first_follow.py)
- FIRST란? 논터미널 기호로부터 유도되어 첫 번째로 나타날 수 있는 터미널 기호의 집합
- FOLLOW란? 논터미널 기호 바로 다음에 나오는 터미널 기호들의 집합
- 출력이 길 경우 리다이렉션을 사용하세요. 
- `python ./first_follow.py > out.txt`
```
$ python ./first_follow.py
+-----------------+--------------------+--------------------+--------------------+
| Production Rule | Pass 1             | Pass 2             | Pass 3             |
+-----------------+--------------------+--------------------+--------------------+
| E -> T E'       |                    |                    | FIRST(E) = {(, id} |
| E' -> + T E'    | FIRST(E') = {+}    |                    |                    |
| E' -> ε         | FIRST(E') = {+, ε} |                    |                    |
| T -> F T'       |                    | FIRST(T) = {(, id} |                    |
| T' -> * F T'    | FIRST(T') = {*}    |                    |                    |
| T' -> ε         | FIRST(T') = {*, ε} |                    |                    |
| F -> ( E )      | FIRST(F) = {(}     |                    |                    |
| F -> id         | FIRST(F) = {(, id} |                    |                    |
+-----------------+--------------------+--------------------+--------------------+
FIRST(E) = {(, id}
FIRST(E') = {+, ε}
FIRST(T) = {(, id}
FIRST(T') = {*, ε}
FIRST(F) = {(, id}

+-----------------+-----------------------------+--------------------------------+
| Production Rule | Pass 1                      | Pass 2                         |
+-----------------+-----------------------------+--------------------------------+
| E -> T E'       | FOLLOW(E) = {$} (start)     | FOLLOW(E') = {$, )}            |
|                 | FOLLOW(T) = {+} (init)      | FOLLOW(T) = {$, ), +} (fce)    |
|                 | FOLLOW(E') = {$}            |                                |
|                 | FOLLOW(T) = {$, +} (fce)    |                                |
| E' -> + T E'    | FOLLOW(T) = {$, +} (fce)    | FOLLOW(T) = {$, ), +} (fce)    |
| E' -> ε         |                             |                                |
| T -> F T'       | FOLLOW(F) = {*} (init)      | FOLLOW(T') = {$, ), +}         |
|                 | FOLLOW(T') = {$, +}         | FOLLOW(F) = {$, ), *, +} (fce) |
|                 | FOLLOW(F) = {$, *, +} (fce) |                                |
| T' -> * F T'    | FOLLOW(F) = {$, *, +} (fce) | FOLLOW(F) = {$, ), *, +} (fce) |
| T' -> ε         |                             |                                |
| F -> ( E )      | FOLLOW(E) = {$, )} (init)   |                                |
| F -> id         |                             |                                |
+-----------------+-----------------------------+--------------------------------+
FOLLOW(E) = {$, )}
FOLLOW(E') = {$, )}
FOLLOW(T) = {$, ), +}
FOLLOW(T') = {$, ), +}
FOLLOW(F) = {$, ), *, +}
```

---
## LL(1) Parsing Table
- TODO

---
## SLR(1) Parsing Table
- TODO (할 수 있을까..?)