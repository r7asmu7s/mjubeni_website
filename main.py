from flask_blog import app

server = app.server

if __name__ == '__main__':
    app.server(host='0.0.0.0', port=8080, debug=True)
