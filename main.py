from app.views import app
from app import db
import os

if __name__ == "__main__":
    try:
        db.create_all()
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, threaded=True, debug=True)
    except Exception as e:
        print(e)
