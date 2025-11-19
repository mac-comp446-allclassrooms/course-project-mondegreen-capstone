from application import create_app

if __name__ == '__main__':
    create_app = create_app("application/songs.txt")
    create_app.run()
else:
    app = create_app("server/application/songs.txt")