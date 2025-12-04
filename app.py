import os
from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Dovoljeni tipi datotek
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_meme(image_path, top_text, bottom_text):
    """
    Ustvari meme z danim tekstom na sliki
    """
    # Odpri sliko
    img = Image.open(image_path)
    
    # Pripravi za risanje
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # Nastavi font - poskusi razlicne moznosti
    font_size = int(height / 10)
    font_paths = [
        "fonts/impact.ttf",  # Lokalni font v projektu
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux Docker font
        "C:/Windows/Fonts/impact.ttf",  # Windows Impact
        "C:/Windows/Fonts/arial.ttf",  # Windows Arial
    ]
    
    font = None
    for font_path in font_paths:
        try:
            font = ImageFont.truetype(font_path, font_size)
            break
        except:
            continue
    
    # Če noben font ne deluje, uporabi privzeti
    if font is None:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    # Funkcija za risanje teksta z outline efektom
    def draw_text_with_outline(text, position):
        x, y = position
        # crn outline (obroba)
        outline_width = 2
        for adj_x in range(-outline_width, outline_width + 1):
            for adj_y in range(-outline_width, outline_width + 1):
                draw.text((x + adj_x, y + adj_y), text, font=font, fill='black')
        # Bel tekst
        draw.text((x, y), text, font=font, fill='white')
    
    # Izracunaj pozicijo za zgornji tekst
    if top_text:
        bbox = draw.textbbox((0, 0), top_text.upper(), font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) / 2
        y = height * 0.05
        draw_text_with_outline(top_text.upper(), (x, y))
    
    # Izracunaj pozicijo za spodnji tekst
    if bottom_text:
        bbox = draw.textbbox((0, 0), bottom_text.upper(), font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) / 2
        y = height * 0.85 - text_height
        draw_text_with_outline(bottom_text.upper(), (x, y))
    
    return img

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_meme():
    # Preveri, ali je bila datoteka nalozena
    if 'image' not in request.files:
        return 'Ni bila naložena nobena slika!', 400
    
    file = request.files['image']
    
    if file.filename == '':
        return 'Ni bila izbrana nobena slika!', 400
    
    if file and allowed_file(file.filename):
        # Shrani nalozeno sliko
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Pridobi tekst iz obrazca
        top_text = request.form.get('top_text', '')
        bottom_text = request.form.get('bottom_text', '')
        
        # Ustvari meme
        meme_image = create_meme(filepath, top_text, bottom_text)
        
        # Shrani v memory buffer
        img_io = io.BytesIO()
        meme_image.save(img_io, 'PNG')
        img_io.seek(0)
        
        # Počisti nalozeno datoteko
        os.remove(filepath)
        
        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='meme.png')
    
    return 'Napacen format datoteke! Dovoljeni so: png, jpg, jpeg, gif', 400

if __name__ == '__main__':
    # Ustvari mapo za uploade, ce ne obstaja
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('fonts', exist_ok=True)
    
    # Preberi port iz okoljske spremenljivke ali uporabi 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)