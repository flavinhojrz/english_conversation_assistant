import os
from dotenv import load_dotenv
import google.generativeai as genai

# Carregando variavel ambiente e inicalizando IA
load_dotenv()
genai.configure(api_key=os.environ.get('API_KEY'))

model = genai.GenerativeModel('gemini-1.5-flash')

prompt = "Você é um professor de inglês e essa é nossa primeira aula, de informações de como será o seu curso."
response = model.generate_content(prompt)

print(response.text)