from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import google.generativeai as genai
import os

# Configuração da API
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        prompt = query.get('prompt', [None])[0]

        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()

        if not api_key:
            self.wfile.write("Erro: GEMINI_API_KEY não configurada na Vercel.".encode('utf-8'))
            return

        if not prompt:
            self.wfile.write("Erro: Envie um prompt na URL.".encode('utf-8'))
            return

        try:
            # Trocamos para o gemini-pro (mais estável) e garantimos o nome correto
            # O modelo 'gemini-pro' tem compatibilidade universal
            model = genai.GenerativeModel('gemini-pro')
            
            response = model.generate_content(prompt)
            
            if response.text:
                self.wfile.write(response.text.encode('utf-8'))
            else:
                self.wfile.write("Erro: Resposta vazia da IA.".encode('utf-8'))

        except Exception as e:
            # Se o gemini-pro falhar, tentamos o 1.0-pro como última alternativa
            try:
                model_alt = genai.GenerativeModel('gemini-1.0-pro')
                response = model_alt.generate_content(prompt)
                self.wfile.write(response.text.encode('utf-8'))
            except:
                self.wfile.write(f"Erro crítico: {str(e)}".encode('utf-8'))
                
