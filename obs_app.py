from run import APP as app

if __name__ == '__main__':
    print("Server started press Crtl-C to terminate server - (DEBUG MODE)")
    app.run(debug=True, port=5000)
