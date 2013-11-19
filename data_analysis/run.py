import os
import sys

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from data_analysis.views import posts
from data_analysis import app
app.register_blueprint(posts)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
