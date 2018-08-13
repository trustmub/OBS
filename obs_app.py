from src import APP

if __name__ == '__main__':
    print("Server started press Crtl-C to terminate server")
    APP.run(debug=True, port=5001)
