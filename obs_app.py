from src import APP

if __name__ == '__main__':
    print("Server started press Crtl-C to terminate server - (DEBUG MODE)")
    APP.run(host="0.0.0.0", port=8080, debug=True, )
