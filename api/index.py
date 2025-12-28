from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import google.generativeai as genai
import os

# Configuração da API Key
# Certifique-se de que o nome na Vercel seja exatamente GEMINI_API_KEY
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Usando o caminho completo do modelo para evitar o erro 404
model = genai.GenerativeModel('models/gemini-1.5-flash')

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Extrai os parâmetros da URL
        query = parse_qs(urlparse(self.path).query)
        prompt = query.get('prompt', [None])[0]

        # Configura o cabeçalho de resposta
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()

        # Verifica se o prompt foi enviado
        if not prompt:
            self.wfile.write("Erro: Você não enviou uma pergunta. Use ?prompt=sua+pergunta".encode('utf-8'))
            return

        # Verifica se a chave da API está configurada
        if not api_key:
            self.wfile.write("Erro: A GEMINI_API_KEY não foi configurada na Vercel.".encode('utf-8'))
            return

        try:
            # Tenta gerar o conteúdo com o Gemini
            response = model.generate_content(prompt)
            
            # Se a resposta for bem-sucedida, envia o texto
            if response and response.text:
                self.wfile.write(response.text.encode('utf-8'))
            else:
                self.wfile.write("Erro: A IA retornou uma resposta vazia.".encode('utf-8'))

        except Exception as e:
            # Caso ocorra erro de cota, modelo ou chave, ele mostra aqui
            erro_msg = f"Erro na API Gemini: {str(e)}"
            self.wfile.write(erro_msg.encode('utf-8'))
            
