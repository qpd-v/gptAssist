# gptAssist 1.0 README.md

## Overview

gptAssist is a simple AI voice assistant that utilizes GPT-3.5 Turbo by OpenAI to generate responses to user inputs. The user can interact with the voice assistant using text or voice input. The assistant can also provide responses through text or text-to-speech.

The following packages are used:

- `asyncio`
- `keyboard`
- `openai`
- `os`
- `pyttsx3`
- `queue`
- `speech_recognition`
- `tempfile`
- `threading`
- `gtts`
- `pydub`
- `pydub.playback`

## Installation

	Install the required packages using pip:
	pip install asyncio keyboard openai pyttsx3 queue SpeechRecognition tempfile gtts pydub

    Or install all the required packages using the requirements.txt file:
    pip install -r requirements.txt

## Usage

    Ensure you have a valid OpenAI API key and replace the placeholder openai.api_key with your own.
    ex.: (Line 19)
        openai.api_key = "YOUR_API_KEY_HERE"  <-- Replace YOUR_API_KEY_HERE with your API key.

    Edit the prompts.py file to add your own prompts.

    Run the script using this command: python main.py

    Use the menu options to choose a set of prompts, text-to-speech engine, and input type.

    Interact with gptAssist using your chosen input method.

## Input Types

    Voice (V): Use your microphone to provide voice input and recieve a voice response back.
    Text (T): Type your input using the keyboard and recieve a voice response back.
    Text-only (TO): Type your input using the keyboard, and receive text responses without text-to-speech.

## Text-to-Speech Engines

    Google Text-to-Speech (gtts): Utilizes Google's TTS API.
    pyttsx3: A cross-platform, offline TTS library.

## Hotkeys

    Ctrl+B: Go back to input type selection.

    Ctrl+C: Stop voice response and go back to user input. 
            Effectively stops gptAssist from speaking in case of long replies. 
            ***Currently only works in TEXT mode.

    Ctrl+D: Go back to text-to-speech engine selection.

## License

	This project is released under the Apache 2.0 License.
