# AudioChat

AudioChat is a project that facilitates real-time audio communication between users. It comprises a client application and a server, enabling seamless voice interactions over a network.

## Startup

### Clone the Repository

```bash
git clone https://github.com/shinypantzzz/audiochat
cd audiochat
```

### Server Setup with Docker

1. Navigate to the server directory:

   ```bash
   cd server
   ```

2. Build docker image:

   ```bash
   docker build -t audiochat-server .
   ```

2. Run docker container:

   ```bash
   docker run -d -p 80:80 audiochat-server
   ```

### Server Setup without Docker

1. Navigate to the server directory:

   ```bash
   cd server
   ```

2. Install the required Go packages:

   ```bash
   go mod tidy
   ```

3. Build the server application:

   ```bash
   go build -o ./build/audiochat-server ./cmd
   ```

4. Run the server:

   ```bash
   ./build/audiochat-server
   ```

### Client Setup

1. Navigate to the client directory:

   ```bash
   cd client
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the client application, use address of the server you want to connect to instead of SERVER_ADDRESS:

   ```bash
   python achat.py http://SERVER_ADDRESS
   ```

## Usage

After starting the client application you will fall into its environment where you can use the following commands:
1. `create ROOM_NAME` - creates a room
2. `connect ROOM_NAME` - connects to the specified room
3. `vol VALUE` - changes the volume, defaults to 1
4. `disconnect` - disconnects from the room
5. `exit` - exits the application