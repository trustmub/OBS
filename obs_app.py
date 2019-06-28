from run import APP as app
from .create_entries import create_application_defaults

if __name__ == '__main__':
    print("Server started press Crtl-C to terminate server - (DEBUG MODE)")
    app.run(debug=True, port=5000, host='0.0.0.0')
