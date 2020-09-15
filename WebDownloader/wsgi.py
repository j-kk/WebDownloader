from WebDownloader.api import create_app
import gunicorn_config as config

app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE)