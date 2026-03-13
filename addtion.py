import re 

def calculate_subtract_divide(expression):
    tokens = re.findall(r'\d+\.?\d*|[-/]', expression)

    i = 0
    while i < len(tokens):
        if tokens[i] == '/':
            left = float(tokens[i-1])
            right = float(tokens[i+1])

            if right == 0:
                return 'Error: ÷0'
            
            result = left / right

            tokens[i-1:i+2] = [str(result)]
            i -= 1

        i += 1

    
    total = float(tokens[0])
    i = 1
    while i < len(tokens):
        op = tokens[i]
        num = float(tokens[i+1])

        if op == '-':
            total -= num

        i += 2
    
    return total