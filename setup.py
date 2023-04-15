# This is for cx_Freeze. However, it currently does not produce a working executable.

import sys
from cx_Freeze import setup, Executable

# Replace 'my_script' with the name of your main Python script
script_name = "main.py"

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable(script_name, base=base)
]

setup(
    name="gptVoiceAssist",
    version="0.1",
    description="Voice assistant utilizing the GPT-3.5-TURBO and the ElevenLabs API",
    executables=executables
)
