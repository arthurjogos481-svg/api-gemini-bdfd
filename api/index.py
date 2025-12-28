from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import google.generativeai as genai
import os

# Configura a chave
api_key = os.environ.get("GEMINI_API_KEY")

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        prompt = query.get('prompt', [None])[0]

        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()

        if not api_key:
            self.wfile.write("Erro: Chave não configurada.".encode('utf-8'))
            return

        try:
            # Forçamos a configuração da API estável
            genai.configure(api_key=api_key)
            
            # Usamos o modelo Flash que é o mais rápido
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            response = model.generate_content(prompt)
            
            if response.text:
                self.wfile.write(response.text.encode('utf-8'))
            else:
                self.wfile.write("Erro: Resposta vazia.".encode('utf-8'))

        except Exception as e:
            # Se der erro, ele vai imprimir o erro detalhado
            self.wfile.write(f"Erro na conexao: {str(e)}".encode('utf-8'))
            
