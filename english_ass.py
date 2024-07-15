import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from google.cloud import texttospeech

# Carregando variáveis de ambiente e inicializando IA
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

def synthesize_text(text):
	client = texttospeech.TextToSpeechClient()

	input_text = texttospeech.SynthesisInput(text=text)

	voice = texttospeech.VoiceSelectionParams(
		language_code="en-US",
		name="en-US-Standard-C",
		ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
	)

	audio_config = texttospeech.AudioConfig(
		audio_encoding=texttospeech.AudioEncoding.MP3
	)

	response = client.synthesize_speech(
		request={"input": input_text, "voice": voice, "audio_config": audio_config}
	)

	output_file = "output.mp3"
	with open(output_file, "wb") as out:
		out.write(response.audio_content)
		print(f'Audio content written to file "{output_file}"')

	return output_file

def interactive_chat():
	while True:
		user_input = input(">> ")
		if user_input.lower() == 'sair':
				print("Encerrando a conversa.")
				break
		response = chat.send_message(user_input)
		print(f"Chatbot (Professor de Inglês): {response.text}")
		
		try:
			audio_file = synthesize_text(response.text)
			result = {
				"status": "success",
				"text": response.text,
				"audio_file": audio_file
			}
		except Exception as e:
			result = {
				"status": "error",
				"message": str(e)
			}

		print(json.dumps(result, indent=4))

# Iniciando a conversa interativa
interactive_chat()
