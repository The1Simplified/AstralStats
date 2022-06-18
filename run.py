import pathlib
import logging

from waitress import serve
from __init__ import create_app

app = create_app()
logging.basicConfig(
    format='%(asctime)s | [%(levelname)s] %(message)s',
    datefmt='%m/%d/%Y at %I:%M:%S %p',
    filename=f'{str(pathlib.Path(__file__).parent.resolve())}\\WebLogs.log',
    encoding='utf-8',
    level=logging.WARNING)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    #serve(app, host="0.0.0.0", port=5000)
