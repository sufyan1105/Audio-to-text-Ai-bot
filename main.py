from flask import Flask, request, render_template
import os
import openai
audio = "static/[SPOTIFY-DOWNLOADER.COM] A Man Without Love.mp3"
audio1 = "static/pyari maa.mp3"
openai.api_key = "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"

app = Flask(__name__, template_folder="templates")
app.config["UPLOAD_FOLDER"] = "static"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        language = request.form['language']
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            audio_file = open(audio1, "rb")
            transcript = openai.Audio.translate("whisper-1", audio_file)
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{
                    "role": "system",
                    "content": f"You will be provided with a sentence in English, and your task is to translate it into {language}"
                }, {
                    "role": "user",
                    "content": transcript.text
                }],
                temperature=0,
                max_tokens=256
            )
            response_content = response['choices'][0]['message']['content']
            return render_template('output.html', output_content=response_content)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
