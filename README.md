# Project 4
For this Project, I researched and played around with the following topics: threading, speech2text and text2speech.

---

## Table of Contents

- [Functions](#functions)
- [Setup](#setup)

---

## Functions
In this directory there are currently three .py files: app.py, speech_to_text.py and text_to_speech.py. 

* app.py 
  * Shows how threading can be implemented using python. For the purpose of this project, app.py creates three task to open three seperate .wav files and do text2speech. 
* speech_to_text.py 
  * Converts a valid .wav file into text that is printed in the terminal. 
* text_to_speech.py 
  * Converts a string into a .wav file whihc is then played through the speakers of your device. 

---

## Setup

This repo uses python 3.9+.

After cloning the repository, it is recommended to use a virtual environment when working with the repo to avoid any conflict that may occur between different environments. With virtualenv installed you can create a new environment by running:

```
python3 -m virtualenv .venv
```

Then activate the environment:

```
source .venv/bin/activate (macOS/*nix)
.venv/bin/activate.cmd (Windows)
```

Then install the requirements:

```
python3 -m pip install requirements
```

Then run the function you want:

```
python3 [filename.py]
```

---
