from web.web_server import create_app


def main():
    app = create_app()
    with app.app_context():
        app.run()


if __name__ == "__main__":
    main()
