import os
import pathlib
import uvicorn
import webbrowser
from threading import Timer

# Serves as relative root path. Used in other modules
root_folder = pathlib.Path(__file__).resolve().parent.parent


def open_browser():
    webbrowser.open_new_tab("http://localhost:8020")


def main():
    """Main Entry Point of Silzila App.
    This function will start app, the backend which serves API.
    """
    print("Silzila app will open in browser.\nPlease keep the Terminal Open until working in the App.\nTo close the app, please log out in browser app and press Ctrl+C in Terminal")
    Timer(3, open_browser).start()
    uvicorn.run("silzila.app.app:app", host="0.0.0.0", port=8020, reload=False)


if __name__ == '__main__':
    main()
