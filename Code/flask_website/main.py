from website import create_app
import socket
app = create_app()
if __name__ == '__main__':
    app.run(host='192.168.2.7', port=5000,debug=True)