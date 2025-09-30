from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_file
import sqlite3
import pandas as pd
import io

app = Flask(__name__)

# Inicializa banco


def init_db():
    conn = sqlite3.connect('temperaturas.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS leituras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        temperatura TEXT,
        data_hora TEXT
    )
''')
    conn.commit()
    conn.close()

# Rota para receber dados via POST


@app.route('/temperatura', methods=['POST'])
def receber_temperatura():
    dados = request.get_json()
    temp = dados.get('temperatura')

    if temp:
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = sqlite3.connect('temperaturas.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO leituras (temperatura, data_hora) VALUES (?, ?)", (temp, data_hora))
        conn.commit()
        conn.close()
        return jsonify({"status": "sucesso", "temperatura": temp, "horario": data_hora}), 200
    else:
        return jsonify({"erro": "Temperatura não recebida"}), 400

# Rota JSON (bruta)


@app.route('/temperaturas', methods=['GET'])
def listar_temperaturas():
    conn = sqlite3.connect('temperaturas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leituras ORDER BY id DESC LIMIT 10")
    dados = cursor.fetchall()
    conn.close()
    return jsonify(dados)

# ✅ Rota HTML visual


@app.route('/visualizar', methods=['GET'])
def visualizar_temperaturas():
    conn = sqlite3.connect('temperaturas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leituras ORDER BY id DESC LIMIT 20")
    dados = cursor.fetchall()
    conn.close()
    return render_template('temperaturas.html', dados=dados)

# ✅ Rota para exportar Excel


@app.route('/exportar_excel', methods=['GET'])
def exportar_excel():
    conn = sqlite3.connect('temperaturas.db')
    df = pd.read_sql_query("SELECT * FROM leituras ORDER BY id DESC", conn)
    conn.close()

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Temperaturas')

    output.seek(0)
    return send_file(
        output,
        as_attachment=True,
        download_name="relatorio_temperaturas.xlsx",
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# ✅ Rota para resetar os dados do banco (deleta todos os registros)


@app.route('/resetar', methods=['GET'])
def resetar_banco():
    conn = sqlite3.connect('temperaturas.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM leituras")
    conn.commit()
    conn.close()
    return "✅ Todos os dados foram apagados com sucesso!"


# Executa o app
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
