from waitress import serve
from __init__ import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    #serve(app, host="0.0.0.0", port=5000)
