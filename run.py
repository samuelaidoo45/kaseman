# run.py
from app import create_app
from models import loan_classification, loan_classification_files, loan_classification_items

app = create_app()

def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 0))
    _, port = s.getsockname()
    s.close()
    return port

if __name__ == '__main__':
    port = find_free_port()
    app.run(port=port)



