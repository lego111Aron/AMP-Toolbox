import os
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from utils.pdf_manager import merge_pdfs, split_pdf, crop_pdf
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, send_file, flash, redirect, url_for, send_from_directory

app = Flask(__name__)
# ...
@app.route('/upload/pdf-split', methods=['POST'])
def upload_pdf_split():
    # Implementation for split
    # ...
    pass

@app.route('/upload/pdf-crop', methods=['POST'])
def upload_pdf_crop():
    # Implementation for crop
    pass

@app.route('/pdf-reader')
def pdf_reader():
    return render_template('pdf_reader.html')

@app.route('/upload/pdf-viewer', methods=['POST'])
def upload_pdf_viewer():
    # ...
    pass

app.secret_key = 'super_secret_key_amp' # Change this in production

# Configuration
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pdf-tools')
def pdf_tools():
    return render_template('pdf_tools.html')

@app.route('/converter')
def converter():
    return render_template('converter.html')

@app.route('/upload/pdf-merge', methods=['POST'])
def upload_pdf_merge():
    if 'files' not in request.files:
        flash('Nincs kiválasztott fájl!')
        return redirect(request.url)
    
    files = request.files.getlist('files')
    file_paths = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            file_paths.append(path)
    
    if not file_paths:
        flash('Nincsenek érvényes fájlok!')
        return redirect(url_for('pdf_tools'))
        
    output_filename = 'merged_document.pdf'
    output_path = os.path.join(app.config['DOWNLOAD_FOLDER'], output_filename)
    
    success = merge_pdfs(file_paths, output_path)
    
    if success:
        return send_file(output_path, as_attachment=True)
    else:
        flash('Hiba történt az egyesítés közben.')
        return redirect(url_for('pdf_tools'))

@app.route('/upload/convert', methods=['POST'])
def upload_convert():
    if 'file' not in request.files:
        flash('Nincs fájl kiválasztva')
        return redirect(request.url)
        
    file = request.files['file']
    target_format = request.form.get('format')
    
    if file.filename == '':
        flash('Nincs kiválasztott fájl')
        return redirect(request.url)
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        output_filename = f"converted.{target_format}"
        output_path = os.path.join(app.config['DOWNLOAD_FOLDER'], output_filename)
        
        success = False
        if target_format in ['jpg', 'png']:
            success = convert_image(input_path, output_path, target_format)
        elif target_format == 'pdf':
            success = convert_to_pdf(input_path, output_path)
        else:
            flash('Ez a formátum még nem támogatott.')
            return redirect(url_for('converter'))
            
        if success:
             return send_file(output_path, as_attachment=True)
        else:
            flash('Hiba a konvertálás során.')
            return redirect(url_for('converter'))

    return redirect(url_for('converter'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8443, debug=True)