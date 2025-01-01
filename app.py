from flask import Flask, request, render_template, flash, send_from_directory
import os

app = Flask(__name__, template_folder=os.getcwd(), static_folder='assets')  # Set static folder to assets directory

# Set the folder where the uploaded files will be saved
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}

# Set the maximum file size to 500MB (in bytes)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']

    # Handle file upload
    file = request.files.get('file')
    if file:
        if allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
        else:
            flash('Invalid file type. Allowed types are: png, jpg, jpeg, gif, pdf, doc, docx.')
            return render_template('index.html')

    # Process or store the contact form data (e.g., save to database, send email, etc.)
    return f"Thank you for your message, {name}!"

# Error handling for file size exceeding the limit
@app.errorhandler(413)
def request_entity_too_large(error):
    return "File is too large. Please upload a file smaller than 500MB.", 413

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)

