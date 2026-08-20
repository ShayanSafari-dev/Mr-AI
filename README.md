**Mr. AI** 
<img width="100" height="100" alt="image" src="https://github.com/user-attachments/assets/2942975d-a16a-4617-bdba-203e6f8d3da5" />
----------

**Mr. AI** is a Python desktop AI assistant designed as a school project. It combines a modern CustomTkinter interface with AI-powered conversations, voice interaction, speech recognition, and simple student memory.

> **Version:** v1.1 
>**Platform:** Windows 
>**Language:** Python

✨ Features
----------

*   🤖 AI-powered conversations using OpenAI
    
*   💬 Chat-style interface
    
*   🎙️ Voice conversation mode
    
*   🔊 AI text-to-speech
    
*   🎤 Speech recognition
    
*   🧠 Basic student personality memory
    
*   👤 Login screen
    
*   📋 Copy AI responses
    
*   🔙 Back button for navigation
    
*   🌎 English and French voice support
    
*   🎨 Custom-designed interface
    
*   ⚡ Animated AI responses and "thinking" indicator
    

🚀 How to Run (IMPORTANT)
-------------------------

👉 **You must run App.py (NOT LoginScreen.py)**

### ✅ Correct command:

`   python App.py   `

The login system is already built into the app, so you do **NOT** need to start the login screen manually.

🔐 Login Credentials
--------------------

Use the following credentials inside the app:

*   **Username:** shayan-safari-dev
    
*   **Password:** 1234
    

📸 How It Works
---------------

Mr. AI has two main parts:

*   LoginScreen.py — handles the login UI
*   <img width="830" height="725" alt="image" src="https://github.com/user-attachments/assets/adc93672-b534-4ea0-a5ff-481cac824089" />

    
*   App.py — runs the full Mr. AI application (**MAIN FILE**)
*   <img width="1331" height="985" alt="image" src="https://github.com/user-attachments/assets/07aaecf0-58c8-464b-8f8f-278e13d0575b" />


⚠️ You should always start from App.py.

📁 Project Structure
--------------------
The design folder is required because the application loads images and icons from it.

The application also creates a voice/ folder while running to temporarily store generated voice files.

🚀 Installation
---------------

### 1\. Install Python

Install **Python 3.10+** on Windows.

Check installation:

`   python --version   `

### 2\. Clone the Repository

`   git clone https://github.com/ShayanSafari-dev/Mr-AI.git  cd Mr-AI   `

### 3\. Install Dependencies

`   pip install -r requirements.txt   `

> ⚠️ SpeechRecognition may require PyAudio on some systems.

### 4\. OpenAI API Key

Mr. AI uses **OpenAI** for AI responses.

Create an API key from your OpenAI account.

⚠️ **Never upload your API key to GitHub.**

### 5\. Add Your API Key

Open:

`   App.py   `

Find: (line 173 in App.py)

`   API_KEY = "Replace with your OpenAI API key"   `

Replace it with:

`   API_KEY = "YOUR_OPENAI_API_KEY"   `

> 🔒 **Keep your real API key private.**

### 6\. Run the App

`   python App.py   `

🎙️ Voice Mode
--------------

Mr. AI supports voice interaction using:

*   **SpeechRecognition** — speech input
    
*   **Edge TTS** — voice output
    
*   **Pygame** — audio playback
    

Supports **English and French** voices.

🧠 Memory System
----------------

Mr. AI stores temporary session memory to adapt responses based on user interaction and learning style.

**Memory resets when the app closes.**

🧮 Math Support
---------------

For math questions, Mr. AI:

*   Solves step-by-step
    
*   Avoids guessing
    
*   Explains clearly
    
*   Uses normal text (**no LaTeX**)
    

⚠️ Important Notes
------------------

*   Works on **Windows only**
    
*   Requires an **internet connection**
    
*   Requires an **OpenAI API key**
    
*   **Do NOT upload API keys to GitHub**
    
*   The design/ folder is required
    
*   Voice files are temporary
    
*   A working microphone is required for voice mode
    

🛠️ Built With
--------------

*   **Python**
    
*   **CustomTkinter**
    
*   **OpenAI API**
    
*   **Edge TTS**
    
*   **SpeechRecognition**
    
*   **Pygame**
    
*   **Pillow**
    

👨‍💻 About the Project
-----------------------

Mr. AI was created as a school project by **Shayan Safari**, with contributions to the presentation from **Ruan and Henry**.

It evolved from a simple chatbot into a full desktop AI assistant with **voice, memory, login, speech recognition, and a modern UI**.

📌 Future Plans
---------------

*   Custom AI themes
    
*   Better memory system
    
*   Multi-model support
    
*   Improved security
    
*   Cross-platform support
    
*   UI improvements
    

📄 License
----------

This project is licensed under the **MIT License**.
