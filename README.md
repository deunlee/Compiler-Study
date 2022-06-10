# Compiler-Study

컴파일러 강의 들으면서 개인적으로 정리한 내용과 구현해본 알고리즘


## NFA to DFA
- `RegExpr -> ε-NFA -> DFA -> minimized-DFA`
- TODO


---
## FIRST and FOLLOW [(first_follow.py)](./first_follow.py)
- FIRST: 논터미널 기호로부터 **유도되어** 첫 번째로 나타날 수 있는 터미널 기호(심볼)의 집합
  - $A \to a \alpha$ 이면, $FIRST(A)$에 $a$ 추가 (INIT-FIRST)
  - $A \to Ba$ 이면, $FIRST(A)$에 $FIRST(B)$ 추가
  - 참고) 논터미널의 FIRST는 해당 논터미널임 ($FIRST(a) = \{a\}$)
- FOLLOW: 논터미널 기호 **바로 다음에** 나오는 터미널 기호의 집합
  - $B \to A \alpha$ 이면, $FOLLOW(A)$에 $FIRST(\alpha) - \epsilon$ 을 추가 (INIT-FOLLOW)
  - $B \to \alpha A$ 이면, $FOLLOW(A)$에 $FOLLOW(B)$ 추가
    - $B \to CA$ 이고, $\epsilon \in FIRST(A)$ 이면, $FOLLOW(C)$에도 $FOLLOW(B)$ 추가

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
## Top-Down Parsing
- Recursive Descent Parser: Backtracking Parser
  - 가장 상위 논터미널(start symbol) 부터 시작해서 아래로 내려감
  - 각 단계에서 사용할 production rule을 결정
  - 잘못된 rule을 선택할 경우 이전 단계로 돌아감(undo) => backtracking
  - 백트래킹이 너무 비효율적(too inefficient)이므로 사용되지 않음
- Predictive Parser: LL(k)
  - 하나 이상의 토큰을 미리 보고(look ahead) 다음 action을 결정
  - LL(k)의 의미:
    - L: left-to-right scan (왼쪽부터 오른쪽으로 문자열 읽기)
    - L: leftmost-derivation
    - k: look ahead할 token의 개수
  - LL(k) 파서는 파싱 스택을 사용함
- 조건:
  - $S \to Sa \; | \; b$ 와 같은 left-recursive(좌재귀)가 있을 경우 무한 루프에 빠지므로 right-recursive로 바꿔야 함
  - $A \to ab \; | \; ac$와 같이 common prefix가 있을 경우 left-refactoring(좌인수분해) 해야 함
    - $A \to a \; A' $ 및 $A' \to b \; | \; c$ 처럼 공통인수만 남기고 분리

### LL(1) Parsing
  - 용어: s-top = top of parsing stack, i-top = top of input string
  1. stack에 $\$$를 push, 시작 심볼도 push, input 끝에는 $\$$ 추가
  1. i-top이 터미널이고 i-top과 s-top이 같을 경우, 모두 지움 $\Rightarrow$ match
     - 같지 않을 경우, $\Rightarrow$ reject
  1. i-top이 논터미널일 경우, 파싱 테이블에서 production rule을 가져와서 RHS를 stack에 삽입
     - stack이 $\$ S$이고 rule이 $S \to ( S ) S$인 경우 stack은 $\$ S ) S ($이 됨
  1. input이 빌 때($\$$만 남을 때)까지 2~3번 반복
     - stack과 input이 모두 $\$$가 될 경우 $\Rightarrow$ accept
     - stack이 비어있지 않은데, input이 비어있을 경우 $\Rightarrow$ reject

### Construct LL(1) Parsing Table
  1. $A \to \alpha$ 이면, 모든 $a \in FIRST(\alpha)$ 에 대해서, $M[A, a]$에 $A \to \alpha$ 추가
  1. $A \to \alpha$ 이고, $\epsilon \in FIRST(\alpha)$ 이면, 모든 $b \in FOLLOW(A)$에 대해서 $M[A, b]$에 $A \to \alpha$ 추가
  - 파싱 테이블의 빈 칸은 파싱 오류 -> error message/recovery
  - 한 칸에 rule이 2개 이상 있으면 모호(ambiguous)함 -> LL(1) 문법이 아님


---
## LL(1) Parsing
code & result



---
## Bottom-Up Parsing



### LR(1) Parsing

### SLR(1) Parsing
- TODO


