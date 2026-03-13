from flask import Flask, render_template, request, jsonify
import re
 
app = Flask(__name__)
 

def calculate_expression(expression):
 
    # 1. 数字と演算子(+ - * /)をバラバラのリストにする
    # 例: "3+5*2-1" → ['3', '+', '5', '*', '2', '-', '1']
    tokens = re.findall(r'\d+\.?\d*|[+\-*/]', expression)
 
    # 2. 優先順位が高い * と / を先にすべて計算する
    i = 0
    while i < len(tokens):
        if tokens[i] in ('*', '/'):
            left  = float(tokens[i-1])
            right = float(tokens[i+1])
 
            if tokens[i] == '*':
                result = left * right  # 掛け算を実行
            else:
                if right == 0:
                    raise ZeroDivisionError
                result = left / right  # 割り算を実行
 
            # 計算し終わった部分(例: '3','*','4')を結果('12.0')に置き換える
            tokens[i-1:i+2] = [str(result)]
            i -= 1  # リストが縮んだ分、位置を戻す
        i += 1
 
    # 3. 残った + と - を前から順番に計算する
    total = float(tokens[0])
    i = 1
    while i < len(tokens):
        op  = tokens[i]
        num = float(tokens[i+1])
 
        if op == '+':
            total += num  # 足し算を実行
        elif op == '-':
            total -= num  # 引き算を実行
        i += 2
 
    return total


@app.route('/')
def index():
    return render_template('index.html')
 
 
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    expression = data['expression']
 
    try:
        result = calculate_expression(expression)
 
        # 小数点以下が不要なら整数で返す（例: 13.0 → 13）
        if result == int(result):
            return jsonify({'result': int(result)})
        return jsonify({'result': round(result, 10)})
 
    except ZeroDivisionError:
        return jsonify({'result': 'Error: ÷0'})
    except Exception:
        return jsonify({'result': 'Error'})
 
 
if __name__ == '__main__':
    app.run(debug=True, port=5003)