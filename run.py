import time

from app.main import create_app

app = create_app()

if __name__ == "__main__":
    time.sleep(5)
    app.run(debug=True, host="0.0.0.0")
