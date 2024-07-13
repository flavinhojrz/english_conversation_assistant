import os
from dotenv import load_dotenv
import google.generativeai as genai
from gtts import gTTS
from playsound3 import playsound 

# Carregando variavel ambiente e inicializando IA
load_dotenv()
genai.configure(api_key=os.environ.get('API_KEY'))

# Definindo o contexto inicial
initial_context = (
	"Você é um professor de inglês dando uma aula. "
	"Por favor, responda às perguntas e forneça explicações como faria em uma aula de inglês. "
	"Todas as suas respostas devem ser em inglês. "
	"Dê respostas curtas e diretas, incentivando a conversação do usuário. "
	"Não insira emojis nas conversas."
)

model = genai.GenerativeModel(
	model_name="gemini-1.5-flash",
	system_instruction=initial_context
)

chat = model.start_chat(history=[])

def text_to_speech(text, lang='en'):
	tts = gTTS(text=text, lang=lang)
	tts.save("output.mp3")
	playsound("output.mp3")

def interactive_chat():
	while True:
		user_input = input(">> ")
		if user_input.lower() == 'sair':
			print("Encerrando a conversa.")
			break
		response = chat.send_message(user_input)
		print(f"Chatbot (Professor de Inglês): {response.text}")
		text_to_speech(response.text)

# Iniciando a conversa interativa
interactive_chat()
