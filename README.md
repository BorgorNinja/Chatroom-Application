# WiFi Chatting Application

This is a simple chat application that allows users to set up a chat server or connect to an existing server using a graphical user interface (GUI) built with `tkinter`. This application supports multiple clients connecting to a server and exchanging messages.

## Features

- **Server Mode**: Start a chat server and accept connections from multiple clients.
- **Client Mode**: Connect to a server using a specified IP address and port.
- **Chat Interface**: Send and receive messages in a graphical chat window.
- **Settings**: Configure the server IP address and port from the GUI.
- **Custom Icon**: The application window can be customized with an icon.

## Prerequisites

- Python 3.x installed on your system.
- `tkinter` is included with standard Python installations, but if it's missing, ensure a complete Python installation.

## Installation

1. **Clone the Repository**

    ```bash
    git clone <repository_url>
    cd WiFi-Chatting-Application
    ```

2. **Install Dependencies**

    Ensure you have Python and `pip` installed. Install any missing modules using:

    ```bash
    pip install -r requirements.txt
    ```

    **Note:** As `tkinter` is a standard library module, it should be installed with Python. If it's not, ensure you have a complete Python installation.

3. **Requirements File**

    Create a `requirements.txt` file to list necessary modules:

    ```txt
    # requirements.txt
    ```

## Running the Application

1. **Run the Python Script**

    To start the application, run the `main.py` script:

    ```bash
    python main.py
    ```

    This will open the main application window where you can start the server or connect as a client.

2. **Starting the Server**

    - Click the "Start Server" button to start the chat server.
    - The server will be ready to accept client connections on the default IP address (`127.0.0.1`) and port (`21`).

3. **Connecting as a Client**

    - Enter a nickname in the "Nickname" field.
    - Click "Connect to Server" to connect to a server using the default IP address and port. 
    - You can also configure these settings through the "Settings" button.

## Customizing the Icon

1. **Prepare the Icon File**

    Ensure you have an icon file in `.ico` format. Convert your image to `.ico` if necessary.

2. **Update the Tkinter Window Icon**

    Place your `.ico` file in the project directory and update the `create_main_window` function in `main.py`:

    ```python
    main_window.iconbitmap('path_to_your_icon.ico')
    ```

    Replace `'path_to_your_icon.ico'` with the path to your icon file.

## Compiling into a Windows Executable

1. **Install PyInstaller**

    Install `PyInstaller` using `pip`:

    ```bash
    pip install pyinstaller
    ```

2. **Compile the Script**

    Use `PyInstaller` to create a standalone executable with the embedded icon:

    ```bash
    pyinstaller --onefile --windowed --icon=path_to_your_icon.ico main.py
    ```

    Replace `path_to_your_icon.ico` with the path to your `.ico` file.

3. **Locate the Executable**

    After compiling, the executable will be located in the `dist` directory:

    ```bash
    dist/main.exe
    ```

## Troubleshooting

- **Missing Tkinter**: If `tkinter` is not available, ensure you have a complete Python installation. `tkinter` is included with standard Python distributions.
- **Icon Issues**: Ensure your icon file is in `.ico` format. PyInstaller requires this format for embedding icons.
- **Connection Issues**: Verify that the IP address and port are correctly set and not blocked by firewalls.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- `tkinter` for providing the GUI framework.
- `PyInstaller` for creating standalone executables.

