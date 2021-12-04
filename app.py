import os
from flask import Flask, request, jsonify, send_file, redirect
from translate import Translator
from config import *
import pyttsx3
import time

app = Flask(__name__)
translator = Translator(MODEL_PATH)

app.config["DEBUG"] = False  # turn off in prod


@app.route('/', methods=["GET"])
def health_check():
    """Confirms service is running"""
    return "Machine translation service is up and running."


@app.route('/lang_routes', methods=["GET"])
def get_lang_route():
    lang = request.args['lang']
    all_langs = translator.get_supported_langs()
    lang_routes = [l for l in all_langs if l[0] == lang]
    return jsonify({"output": lang_routes})


@app.route('/supported_languages', methods=["GET"])
def get_supported_languages():
    langs = translator.get_supported_langs()
    return jsonify({"output": langs})


@app.route('/mlservice/translate', methods=["POST"])
def get_prediction():
    source = request.json['source']
    target = request.json['target']
    text = request.json['text']
    translation = translator.translate(source, target, text)
    return jsonify({"output": translation})


@app.route('/mlservice/voice', methods=["POST"])
def Text_To_Speek():
    lang = request.json['lang']
    text = request.json['text']
    voice_id = ""

    # Voice IDs pulled from engine.getProperty('voices')
    en_voice_id = "english"
    fr_voice_id = "french"
    jap_voice_id = ""
    # spanish
    es_voice_id = "spanish"
    # Mandarin
    zh_voice_id = "Mandarin"
    # Russian
    ru_voice_id = "russian"
    
    # implement switch case for the variable lang
    if lang == "fr":
        voice_id = fr_voice_id
    elif lang == "jap":
        voice_id = jap_voice_id
    elif lang == "es":
        voice_id = es_voice_id
    elif lang == "zh":
        voice_id == zh_voice_id
    elif lang == "ru":
        voice_id = ru_voice_id
    else :
        voice_id = en_voice_id

    t = time.time()

    engine = pyttsx3.init()

    # Set a new voice rate
    engine.setProperty('rate', 200)

    # Set the new voice volume. The minimum volume is 0 and the maximum volume is 1
    engine.setProperty('volume', 1.0)

   
    # Gets the details of the current voice
    voices = engine.getProperty('voices')

    for voice in voices:
        print("Voice:")
        print(" - ID: %s" % voice.id)
        print(" - Name: %s" % voice.name)
        print(" - Languages: %s" % voice.languages)
        print(" - Gender: %s" % voice.gender)
        print(" - Age: %s" % voice.age)

    # print(f'Voice voice details:{voices}')
    # # Set the current voice to female. The current voice cannot read Chinese
    # engine.setProperty('voice', voices[1].id)
    # Set the current voice to male, and the current voice can read Chinese
    engine.setProperty('voice', voice_id)

    # Voice broadcast content
    content = text
    # Output file format
    outFile = f'./audio/{t}.mp3'
    print(outFile)

    engine.save_to_file(content, outFile)
    engine.runAndWait()
    engine.stop()

    return jsonify({"output": f'/mlservice/audio/{t}.mp3'})
    # return send_file(f"./audio/{t}.mp3")

# app route for serving files with mp3 mime type


@app.route('/mlservice/audio/<path:path>')
def send_audio(path):
    return send_file(os.path.join(AUDIO_PATH, path), mimetype='audio/mp3')


app.run(host="0.0.0.0")
