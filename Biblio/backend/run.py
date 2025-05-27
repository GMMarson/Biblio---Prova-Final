from app import create_app
from flask import send_from_directory
import os

app = create_app()

# Caminho absoluto até a pasta frontend_dist
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend_dist')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_vue_app(path):
    file_path = os.path.join(FRONTEND_DIR, path)
    if path != "" and os.path.exists(file_path):
        return send_from_directory(FRONTEND_DIR, path)
    else:
        return send_from_directory(FRONTEND_DIR, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
