from flask_blog import app

if __name__ == '__main__':
    app.server(host='0.0.0.0', port=8080, debug=True)
