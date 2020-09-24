from app.views import app
from app import db

if __name__ == "__main__":
    try:
        db.create_all()
        app.run(host='localhost', threaded=True, debug=True)
    except Exception as e:
        print(e)
