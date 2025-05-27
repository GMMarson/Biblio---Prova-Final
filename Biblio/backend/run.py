from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

from flask import send_from_directory

@app.route('/')
def serve_index():
    return send_from_directory('frontend_dist', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('frontend_dist', path)