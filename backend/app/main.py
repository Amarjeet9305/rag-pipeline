# from flask import Flask
# from app.routes.upload import upload_bp
# from app.routes.query import query_bp
# from app.routes.metadata import metadata_bp

# def create_app():
#     app = Flask(__name__)

#     # Register blueprints
#     app.register_blueprint(upload_bp, url_prefix='/upload')
#     app.register_blueprint(query_bp, url_prefix='/query')
#     app.register_blueprint(metadata_bp, url_prefix='/metadata')

#     @app.route('/')
#     def index():
#         return "<h2>RAG Flask System Running 🚀</h2>"

#     return app

# if __name__ == "__main__":
#     app = create_app()
#     app.run(debug=True)
# from flask import Flask, render_template
# from app.routes.upload import upload_bp
# from app.routes.query import query_bp
# from app.routes.metadata import metadata_bp

# app = Flask(__name__)

# # Register blueprints
# app.register_blueprint(upload_bp)
# app.register_blueprint(query_bp)
# app.register_blueprint(metadata_bp)

# # Serve frontend
# @app.route("/")
# def index():
#     return render_template("index.html")

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000, debug=True)

# from flask import Flask, render_template
# from flask_cors import CORS  # ✅ Allow frontend requests (important!)
# from app.routes.upload import upload_bp
# from app.routes.query import query_bp
# from app.routes.metadata import metadata_bp

# # ✅ Create Flask app
# app = Flask(
#     __name__,
#     static_folder="../frontend/static",   # where styles.css and app.js are stored
#     template_folder="../frontend/templates"  # where index.html is stored
# )

# # ✅ Enable CORS so frontend (e.g. http://127.0.0.1:5500) can talk to Flask
# CORS(app)

# # ✅ Register blueprints
# app.register_blueprint(upload_bp)
# app.register_blueprint(query_bp)
# app.register_blueprint(metadata_bp)

# # ✅ Serve index.html (main UI)
# @app.route("/")
# def index():
#     return render_template("index.html")

# # ✅ Run Flask app
# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=8000, debug=True)
import os
from flask import Flask, render_template
from flask_cors import CORS
from app.routes.upload import upload_bp
from app.routes.query import query_bp
from app.routes.metadata import metadata_bp

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "frontend", "static"),
    template_folder=os.path.join(BASE_DIR, "frontend", "templates")
)

# ✅ Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})

# ✅ Register blueprints with prefixes
app.register_blueprint(upload_bp, url_prefix="/api")
app.register_blueprint(query_bp, url_prefix="/api")
app.register_blueprint(metadata_bp, url_prefix="/api")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
    app.run(debug=True, use_reloader=False)
