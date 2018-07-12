from __future__ import unicode_literals
from flask import Flask
from flask import render_template, request, send_file
import os
import json
import youtube_dl


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/download", methods=['POST'])
def authenticate():
    video = request.form['url']

    if 'youtube' not in video and 'youtu' not in video:
        print "You need to specify one or more youtube videos"
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'keepvideo': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    #Delete mp3 files in current dir / not threadsafe but no problem :)
    files = [f for f in os.listdir('.') if os.path.isfile(f) and (".mp3" in f or ".webm" in f or ".m4a" in f)]
    for f in files:
        os.unlink(f)

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video, download=False)
        ydl.download([video])

        suffix=""
        if "?v=" in video:
            suffix = video.split("?v=")[1].split("/")[0] + ".mp3"
        else:
            suffix = video.split("/")[-1] + ".mp3"
        fileName = info_dict.get('title', None).replace("/", "_") + "-" + suffix
        print fileName
        if os.path.isfile(fileName):
            print('found')
        return send_file(fileName, as_attachment=True, attachment_filename=fileName.encode('utf-8').strip())


if __name__ == "__main__":
    #create secret key
    app.secret_key = os.urandom(24)
    app.run(host='0.0.0.0')