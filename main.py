import asyncio
import keyboard
import openai
import os
import pyttsx3
import queue
import speech_recognition as sr
import tempfile
import threading
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

from prompts import prompts

should_go_to_tts_engine = False
should_go_back = False

openai.api_key = "YOUR_API_KEY_HERE"
recognizer = sr.Recognizer()

recognizer.non_speech_duration = 3
recognizer.energy_threshold = 300
recognizer.phrase_threshold = 0.3

def speak_with_pyttsx3(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def synthesize_and_play_speech(text, tts_engine):
    if tts_engine == "gtts":
        tts = gTTS(text, lang="en", slow=False)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)

        audio_segment = AudioSegment.from_file(temp_file.name, format="mp3")
        play(audio_segment)

        temp_file.close()
        os.unlink(temp_file.name)
    elif tts_engine == "pyttsx3":
        speak_with_pyttsx3(text)

async def process_input(input_text: str, prompt_key: str, input_mode: str) -> str:
    messages = [
        {"role": "system", "content": prompts[prompt_key]},
        {"role": "user", "content": input_text},
    ]

    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=f"{prompts[prompt_key]}\nUser: {input_text}\nAI:",
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0,
    )

    bot_response = response.choices[0].text.strip()
    messages.append({"role": "assistant", "content": bot_response})

    print(f"Bot's response: {bot_response}")

    if input_mode == 'V':
        synthesize_and_play_speech(bot_response)
    elif input_mode == 'T':
        print(f"Bot's response: {bot_response}")
    elif input_mode == 'TO':
        pass

    return bot_response

async def main():
    def on_key(event):
        global should_go_back
        global should_go_to_tts_engine

        if event.name == 'b' and keyboard.is_pressed('ctrl'):
            print("\nCtrl+B pressed. Going back to input type selection. Press ENTER to continue.")
            should_go_back = True
        elif event.name == 'd' and keyboard.is_pressed('ctrl'):
            print("\nCtrl+D pressed. Going back to text-to-speech engine selection.")
            should_go_to_tts_engine = True

    def start_key_listener():
        keyboard.on_press(on_key)

    key_listener = threading.Thread(target=start_key_listener)
    key_listener.start()

    prompt_key = ""
    while prompt_key not in prompts.keys():
        prompt_key = input(f"Choose a set of prompts ({', '.join(prompts.keys())}): ")

    messages = [
        {"role": "system",
         "content": prompts[prompt_key]},
    ]

    tts_engine = ""
    while tts_engine not in ('gtts', 'pyttsx3'):
        tts_engine = input("Choose a text-to-speech engine (gtts or pyttsx3): ").lower()

    input_type = ""
    while input_type not in ('v', 't', 'to'):
        input_type = input("Choose input type- [v] for Voice, [t] for Text, [to] for text-ONLY): ").lower()

    while True:
        global should_go_back
        global should_go_to_tts_engine
        user_input = ""

        if input_type == 'v':
            with sr.Microphone() as source:  # Add this line
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening... Press Ctrl+B to stop listening.")

                audio_queue = queue.Queue()

            def callback(recognizer, audio):
                audio_queue.put(audio)

            stop_listening = recognizer.listen_in_background(source, callback)

            while not should_go_back:
                try:
                    audio = audio_queue.get(timeout=10)
                    print("Processing...")
                    user_input = recognizer.recognize_google(audio)
                    break
                except queue.Empty:
                    print("Timeout. Try again.")
                except sr.UnknownValueError:
                    print("Not sure what's going on here. Ignore this.")
                except sr.RequestError as e:
                    print(f"Could not request results from Speech Recognition service; {e}")
                    user_input = "I'm having trouble connecting to the speech recognition service."
                    break
                except Exception as e:
                    print("Error:", e)
                    user_input = "Continuing"
                    break

            stop_listening(wait_for_stop=True)


        elif input_type in ('t', 'to'):
            user_input = input("Enter your text: ")

            if should_go_back:
                should_go_back = False
                input_type = ""
                while input_type not in ('v', 't', 'to'):
                    input_type = input("Choose input type (V for voice, T for text, TO for text only): ").lower()
                continue

                # Add the conditional block to handle the should_go_to_tts_engine variable
            if should_go_to_tts_engine:
                should_go_to_tts_engine = False
                tts_engine = ""
                while tts_engine not in ('gtts', 'pyttsx3'):
                    tts_engine = input("Choose a text-to-speech engine (gtts or pyttsx3): ").lower()
                continue

        messages.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.6,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=0,
        )

        bot_response = response["choices"][0]["message"]["content"]
        bot_response = bot_response.replace("[Response]: ", "")
        messages.append({"role": "assistant", "content": bot_response})

        print("Bot's response:", bot_response)

        if input_type != 'to':
            synthesize_and_play_speech(bot_response, tts_engine)

if __name__ == "__main__":
    asyncio.run(main())