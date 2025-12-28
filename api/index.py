from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import google.generativeai as genai
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        prompt = query.get('prompt', [None])[0]

        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            self.wfile.write("Erro: Chave ausente na Vercel.".encode('utf-8'))
            return

        genai.configure(api_key=api_key)

        # Tentativa em lista (ele vai tentar um por um até dar certo)
        modelos_para_testar = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-1.0-pro']
        
        sucesso = False
        for nome_modelo in modelos_para_testar:
            if sucesso: break
            try:
                model = genai.GenerativeModel(nome_modelo)
                response = model.generate_content(prompt if prompt else "Oi")
                self.wfile.write(response.text.encode('utf-8'))
                sucesso = True
            except Exception:
                continue # Se der erro, tenta o próximo modelo da lista

        if not sucesso:
            self.wfile.write("Erro: Nenhum modelo do Gemini respondeu. Verifique sua API Key.".encode('utf-8'))
            
