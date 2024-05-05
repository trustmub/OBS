from src import APP as app

if __name__ == '__main__':
    print("Server started press Crtl-C to terminate server - (DEBUG MODE)")
    app.run(host="0.0.0.0", port=8080, debug=True, )
