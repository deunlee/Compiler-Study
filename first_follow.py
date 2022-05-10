# Compute the FIRST and FOLLOW of production rule
# Code by Deun Lee (https://github.com/deunlee)

def print_matrix(matrix, use_col=False):
    s = [[str(e) for e in row] for row in matrix]
    lengths = [max(map(len, col)) for col in zip(*s)]
    fmt     = ' | '.join('{{:{}}}'.format(x) for x in lengths)
    table   = [fmt.format(*row) for row in s]
    div     = '+' + '+'.join(['-'*(x+2) for x in lengths]) + '+'
    if use_col:
        print(div + '\n| ' + table[0] + ' |')
        print(div + '\n| ' + ' |\n| '.join(table[1:]) + ' |\n' + div)
    else:
        print(div + '\n| ' + ' |\n| '.join(table) + ' |\n' + div)



def is_non_terminal(x):
    return x[0].isupper() # 논터미널 기호는 대문자로 시작한다.

def is_terminal(x):
    return not x[0].isupper() # 터미널 기호는 대문자로 시작하지 않는다. (소문자 및 특수문자 등)

def is_epsilon(x):
    return x == 'ε'



def prod_rules_to_list(rules):
    """문자열로 이루어진 생성 규칙(production rule)을 리스트로 변환하는 함수
    
    Args:
        rules: 문자열로 이루어진 생성 규칙
         - 각 규칙을 한 줄에 하나 씩 표기하며, 축약(|) 표현을 사용할 수 있다.
         - 축약 표현은 여러 줄에 걸처서 사용할 수 있다.
         - 논터미널 기호는 알파벳 대문자로 시작하며, 터미널은 대문자로 시작하지 않는다.
         - 각 기호 사이에는 띄어쓰기를 사용한다. 붙여 쓸 경우 하나의 기호로 인식한다.
         - 엡실론 기호는 ε을 사용한다.

    Example:
        prod_rules_to_dict('''
            S -> C   | D
            C -> a C | b
            D -> c D | d
        ''')
        [['S', 'C'], ['S', 'D'], ['C', 'a', 'C'], ['C', 'b'], ['D', 'c', 'D'], ['D', 'd']]
    """
    merged = []
    for rule in filter(len, map(lambda x: x.strip(), rules.split('\n'))): # 빈 줄 및 앞뒤 공백 제거
        if '->' in rule:
            merged.append(rule)
        else:
            merged[len(merged)-1] += rule # 여러 줄에 걸친 축약 표현은 한 줄로 합친다.
    result = []
    for rule in merged:
        lhs, rhs = rule.split('->')     # 생성 규칙의 왼쪽/오른쪽 분리
        for r in rhs.split('|'):        # 축약된 생성 규칙 분리
            result.append([lhs.strip()] + list(filter(lambda x: x, r.split(' '))))
    return result



def compute_first(rules, verbose=False):
    """모든 생성 규칙에 대해 FIRST를 계산하는 함수

    Args:
        rules: 생성 규칙의 리스트
        verbose: True일 경우 Pass Table을 출력한다.

    Note:
        FIRST란? 논터미널 기호로부터 유도되어 첫 번째로 나타날 수 있는 터미널 기호의 집합

    Example:
        {'S': {'a', 'c', 'd', 'b'}, 'C': {'a', 'b'}, 'D': {'d', 'c'}}
    """

    FIRSTs = {} # 각 논터미널에 대한 FIRST를 저장하는 딕셔너리
    PASSs  = [] # verbose가 True인 경우 Pass Table을 출력하기 위한 리스트
    
    # 각 논터미널의 FIRST를 빈 set으로 초기화
    for rule in rules:
        for r in filter(is_non_terminal, rule): # LHS 및 RHS에 있는 모든 논터미널을 빈 set으로 초기화한다.
            FIRSTs[r] = set()
        if verbose:
            PASSs.append([f'{rule[0]} -> {" ".join(rule[1:])}'])

    # INIT_FIRST 계산 (처음 한 번만 계산한다.) ????
    # INIT_FIRST(A) = {a ∈ V_T | A -> aα ∈ P, α ∈ V*}
    for idx, rule in enumerate(rules):
        lhs = rule[0] # LHS (LHS는 논터미널로 가정)
        rhs = rule[1] # RHS의 첫 번째 기호

        if is_terminal(rhs): # 생성 규칙에 처음 나오는 기호가 터미널일 경우
            FIRSTs[lhs].add(rhs)
        
        if verbose:
            t = ", ".join(sorted(FIRSTs[lhs]))
            PASSs[idx].append(f'FIRST({lhs}) = {{{t}}}' if t else ' ')

    # FIRST 계산
    # A -> Bα인 생성 규칙이 존재하면, FIRST(A)에 FIRST(B)를 추가한다. (B => a𝛿 이면, A => Bα => a𝛿α)
    # FIRST(A) = INIT_FIRST(A) U {FIRST(B) | A -> Bα ∈ P, A ≠ B}
    while True:
        updated_count = 0

        for idx, rule in enumerate(rules):
            lhs = rule[0] # LHS (LHS는 논터미널로 가정)
            rhs = rule[1] # RHS의 첫 번째 기호
            cnt = len(FIRSTs[lhs]) # 기존 개수 카운팅

            if is_non_terminal(rhs) and lhs != rhs:
                FIRSTs[lhs].update(FIRSTs[rhs])

            cnt = len(FIRSTs[lhs]) - cnt
            updated_count += cnt

            if verbose:
                t = ", ".join(sorted(FIRSTs[lhs]))
                PASSs[idx].append(f'FIRST({lhs}) = {{{t}}}' if t and cnt else ' ')

        if updated_count == 0: # 추가된 FIRST가 더 이상 없으면 while문 종료
            break

    if verbose:
        PASSs.insert(0, ['Production Rule'] + [f'Pass {i+1}' for i in range(len(PASSs[0]))])
        PASSs = [p[:-1] for p in PASSs]
        print_matrix(PASSs, use_col=True)

    return FIRSTs



def compute_follow(rules, verbose=False):
    """모든 생성 규칙에 대해 FOLLOW를 계산하는 함수

    Args:
        rules: 생성 규칙의 리스트
        - 첫 번째 생성 규칙의 LHS(논터미널)을 시작 기호(start symbol)로 간주한다.

        verbose: True일 경우 Pass Table을 출력한다.

    Note:
        FOLLOW란? 논터미널 기호 바로 다음에 나오는 터미널 기호들의 집합
        시작 기호에는 end marker($)를 추가한다.

    Example:
        {'S': {'a', 'c', 'd', 'b'}, 'C': {'a', 'b'}, 'D': {'d', 'c'}}
    """

    FOLLOWs = {} # 각 논터미널에 대한 FOLLOW를 저장하는 딕셔너리
    PASSs   = []  # verbose가 True인 경우 Pass Table을 출력하기 위한 리스트
    
    FIRSTs = compute_first(rules)
    def first_without_epsilon(x): # 입실론을 제외한 FIRST를 반환한다. (x가 터미널일 경우 x 그대로 반환)
        if is_epsilon(x):  return {}
        if is_terminal(x): return {x}
        return FIRSTs[x] - {'ε'}

    # 각 논터미널의 FOLLOW를 빈 set으로 초기화
    for rule in rules:
        for r in filter(is_non_terminal, rule): # LHS 및 RHS에 있는 모든 논터미널을 빈 set으로 초기화한다.
            FOLLOWs[r] = set()
        if verbose:
            PASSs.append([f'{rule[0]} -> {" ".join(rule[1:])}'])
    
    while True:
        updated_count = 0

        for idx, rule in enumerate(rules):
            lhs  = rule[0]  # LHS (LHS는 논터미널로 가정)
            rhs  = rule[-1] # RHS의 마지막 기호
            desc = []

            # 시작 기호에 end marker($) 추가
            if idx == 0 and '$' not in FOLLOWs[lhs]:
                FOLLOWs[lhs].add('$')
                desc.append(f'FOLLOW({lhs}) = {{$}} (start)')

            # INIT_FOLLOW 계산 (한번만 해도되는지??)
            # INIT_FOLLOW(A) = {a ∈ V_T | B -> αACβ, a ∈ FIRST(C), α, β ∈ V*}
            for i in range(1, len(rule)-1):
                curr = rule[i]
                next = rule[i+1]
                if is_non_terminal(curr):
                    cnt = len(FOLLOWs[curr])              # 기존 개수 카운팅
                    FOLLOWs[curr].update(first_without_epsilon(next)) # 입실론을 제외한 FIRST를 추가한다.
                    cnt = len(FOLLOWs[curr]) - cnt        # 추가된 개수 카운팅
                    updated_count += cnt

                    if verbose and cnt:
                        desc.append(f'FOLLOW({curr}) = {{{", ".join(sorted(FOLLOWs[curr]))}}} (init)')

            # FOLLOW 계산
            # B -> αA인 생성 규칙이 존재하면, FOLLOW(A)에 FOLLOW(B)를 추가한다. (S => λBaρ => λαAaρ)
            # FOLLOW(A) = INIT_FOLLOW(A) U {FOLLOW(B) | B -> αA ∈ P, α ∈ V*}
            if is_non_terminal(rhs):
                cnt = len(FOLLOWs[rhs])           # 기존 개수 카운팅
                FOLLOWs[rhs].update(FOLLOWs[lhs]) # B -> αA 일 경우, FOLLOW(A)에 FOLLOW(B)를 추가
                cnt = len(FOLLOWs[rhs]) - cnt     # 추가된 개수 카운팅
                updated_count += cnt

                if verbose and cnt:
                    desc.append(f'FOLLOW({rhs}) = {{{", ".join(sorted(FOLLOWs[rhs]))}}}')

                if 'ε' in FIRSTs[rhs] and len(rule) >= 3: # B -> CA 이고, FIRST(A)에 ε이 포함되어 있을 경우
                    priv = rule[-2]
                    cnt = len(FOLLOWs[priv])           # 기존 개수 카운팅
                    FOLLOWs[priv].update(FOLLOWs[lhs]) # FOLLOW(C)에 FOLLOW(B)를 추가
                    cnt = len(FOLLOWs[priv]) - cnt     # 추가된 개수 카운팅
                    updated_count += cnt

                    if verbose and len(FOLLOWs[lhs]): # and cnt:
                        desc.append(f'FOLLOW({priv}) = {{{", ".join(sorted(FOLLOWs[priv]))}}} (fce)') # FIRST contains epsilon
            
            if verbose:
                PASSs[idx].append('/'.join(desc))
            
        if updated_count == 0: # 추가된 FOLLOW가 더 이상 없으면 while문 종료
            break

    if verbose:
        temp = [] # 하나의 생성 규칙에 의해 여러 개의 FOLLOW가 나온 경우, Pass Table의 한 row에는 하나의 FOLLOW만 표시되도록 한다.
        for row in PASSs:
            m = max(map(lambda x: len(x.split('/')), row))
            row = [x.split('/') + [''] * (m-len(x.split('/'))) for x in row]
            for i in range(m):
                temp.append([r[i] for r in row])
        PASSs = temp
        PASSs.insert(0, ['Production Rule'] + [f'Pass {i+1}' for i in range(len(PASSs[0]))])
        PASSs = [p[:-1] for p in PASSs]
        print_matrix(PASSs, use_col=True)

    return FOLLOWs



def print_first_and_follow(rules):
    rules = prod_rules_to_list(rules)

    FIRSTs = compute_first(rules, verbose=True)
    for symbol in FIRSTs:
        print(f'FIRST({symbol}) = {{{", ".join(sorted(FIRSTs[symbol]))}}}')
    print()

    FOLLOWs = compute_follow(rules, verbose=True)
    for symbol in FOLLOWs:
        print(f'FOLLOW({symbol}) = {{{", ".join(sorted(FOLLOWs[symbol]))}}}')
    print()



if __name__ == '__main__':

    # 논터미널 기호는 대문자로 시작한다.
    # 논터미널 및 터미널 기호는 여러 글자를 사용할 수 있다. (ex: If, Then, num)
    # 각 기호 사이에는 띄어쓰기를 사용한다.
    # 엡실론 기호는 ε을 사용한다.

    print_first_and_follow('''
        S -> C   | D
        C -> a C | b
        D -> c D | d
    ''')

    print_first_and_follow('''
        E  -> T E'
        E' -> + T E' | ε
        T  -> F T'
        T' -> * F T' | ε
        F  -> ( E ) | id
    ''')

    # print_first_and_follow('''
    #     Stmt -> If Expr Then Stmt | If Expr Then Stmt Else Stmt | other
    #     Expr -> true | false
    # ''')

    # Tiny-C language (Id와 Int는 일부 생략함)
    # print_first_and_follow('''
    #     Prog -> Stmt
    #     Stmt -> if ParenExpr Stmt
    #           | if ParenExpr Stmt else Stmt
    #           | while ParenExpr Stmt
    #           | do Stmt while ParenExpr ;
    #           | { Stmt }
    #           | Expr ;
    #           | ;
    #     ParenExpr -> ( Expr )
    #     Expr -> Test | Id = Expr
    #     Test -> Sum  | Sum < Sum
    #     Sum  -> Term | Sum + Term | Sum - Term
    #     Term -> Id   | Int | ParenExpr
    #     Id   -> a | b | c | d
    #     Int  -> 0 | 1 | 2 | 3
    # ''')

    # 출력이 길 경우 리다이렉션을 사용하세요.
    # python ./first_follow.py > out.txt
