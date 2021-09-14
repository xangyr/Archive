def eval_infix_sum(expr, pos):
    ans, pos = eval_infix_product(expr, pos)
    oper = expr[pos]
    while oper == '+' or oper == '-':
        other, pos = eval_infix_product(expr, pos+1)
        if oper == '+':
            ans = ans + other
        else:
            ans = ans - other
        oper = expr[pos]
    return ans, pos

def eval_infix_product(expr, pos):
    ans, pos = eval_infix_factor(expr, pos)
    oper = expr[pos]
    while oper == '*' or oper == '/':
        other, pos = eval_infix_factor(expr, pos+1)
        if oper == '*':
            ans = ans * other
        elif oper == '/':
            ans = ans // other
        oper = expr[pos]
    return ans, pos

def eval_infix_factor(expr, pos):
    if expr[pos] == '(':
        ans, pos = eval_infix_sum(expr, pos+1)
        return ans, pos+1
    else:
        return int(expr[pos]), pos+1

def eval_infix_list(expr):
    ans, discard = eval_infix_sum(expr, 0)
    return ans

def eval_infix(expr):
    return eval_infix_list(expr.split() + [';'])

if __name__ == '__main__':
    print(eval_infix("15") )
    print(eval_infix("2 + 3"))
    print(eval_infix("2 * 3 + 1"))
    print(eval_infix("2 + 3 * 1"))
    print(eval_infix("1 + ( 2 + 10 * 3 ) * 10"))
    print(eval_infix("1 + 5 * ( 2 + 3 )"))
    print(eval_infix("8 * 5 * ( 8 - 3 )"))
    print(eval_infix("3 + ( 6 - 2 ) / 4"))
