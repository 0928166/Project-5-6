from website import create_app

app = create_app()
if __name__ == '__main__':
    #host='192.168.2.7 or something, port=custom
    app.run(debug=True)