#引き算
def subtract(a, b):
    return a - b

#割り算
def divide(a, b):
    if b != 0:
        return a / b
    else:
        return 'Error: Division by Zero'