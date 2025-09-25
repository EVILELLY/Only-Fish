
from app import create_app

app = create_app()

if __name__ == '__main__':
    import sys
    port = 5000
    for i, arg in enumerate(sys.argv):
        if arg in ('--port', '-p') and i+1 < len(sys.argv):
            try:
                port = int(sys.argv[i+1])
            except Exception:
                pass
    app.run(host='0.0.0.0', port=port, debug=False)
