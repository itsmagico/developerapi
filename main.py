from flask import Flask, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

# Função para executar código com segurança
def run_code(language, code):
    if language not in ["python", "javascript"]:
        return {"error": "Linguagem não suportada!"}

    try:
        # Criando um arquivo temporário para execução
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py" if language == "python" else ".js") as temp_file:
            temp_file.write(code.encode())  # Escreve o código no arquivo
            temp_file_path = temp_file.name

        # Comandos para Python e Node.js
        command = ["python3", temp_file_path] if language == "python" else ["node", temp_file_path]
        
        # Executa o código com timeout de 5 segundos
        result = subprocess.run(command, capture_output=True, text=True, timeout=5)
        
        # Obtém a saída
        output = result.stdout if result.stdout else result.stderr

    except subprocess.TimeoutExpired:
        output = "Erro: Tempo limite excedido (5s)"
    except Exception as e:
        output = str(e)
    
    finally:
        # Removendo o arquivo temporário
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    return {"language": language, "output": output}

# Rota para executar código via GET
@app.route('/code', methods=['GET'])
def run_code_get():
    code = request.args.get("code", "")
    language = request.args.get("language", "python").lower()

    if not code:
        return jsonify({"error": "Nenhum código fornecido!"}), 400

    result = run_code(language, code)
    return jsonify(result)

# Rota para executar código via POST
@app.route('/code', methods=['POST'])
def run_code_post():
    data = request.get_json()
    code = data.get("code", "")
    language = data.get("language", "python").lower()

    if not code:
        return jsonify({"error": "Nenhum código fornecido!"}), 400

    result = run_code(language, code)
    return jsonify(result)

# Inicializa o servidor
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
