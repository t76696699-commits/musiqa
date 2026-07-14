import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Musiqalar saqlanadigan papka
MUSIC_DIR = os.path.join(app.root_path, 'music')


def get_music_list():
    if not os.path.exists(MUSIC_DIR):
        os.makedirs(MUSIC_DIR)

    allowed_extensions = ('.mp3', '.m4a', '.wav')
    files = os.listdir(MUSIC_DIR)

    songs = []
    for file in files:
        if file.lower().endswith(allowed_extensions):
            name_without_ext = os.path.splitext(file)[0]

            # Har xil formatdagi rasmlarni tekshirish
            img_url = None
            for ext in ['.jpg', '.jpeg', '.png', '.webp']:
                img_name = f"{name_without_ext}{ext}"
                img_path = os.path.join(app.root_path, 'static', 'music_images', img_name)
                if os.path.exists(img_path):
                    img_url = f"/static/music_images/{img_name}"
                    break

            # Rasm topilmasa universal chiroyli muqova
            if not img_url:
                img_url = "https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?q=80&w=300&auto=format&fit=crop"

            songs.append({
                "title": name_without_ext.replace('_', ' '),
                "music_url": f"/music_file/{file}",
                "img_url": img_url
            })
    return songs


@app.route('/')
def index():
    songs = get_music_list()
    return render_template('index.html', songs=songs)


@app.route('/music_file/<path:filename>')
def serve_music(filename):
    # path xavfsizligi barcha belgilarni (jumladan tutuq belgilarini) to'g'ri o'qish imkonini beradi
    return send_from_directory(MUSIC_DIR, filename)


if __name__ == '__main__':
    # Tarmoqdagi boshqa qurilmalar (telefonlar) ulanishi uchun host='0.0.0.0'
    app.run(host='0.0.0.0', port=5000, debug=True)
