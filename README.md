# README

## WebRTC Signaling Client with Media Recording

This Python script establishes a WebRTC connection via a PeerJS-compatible signaling server, handles audio/video streams, and records incoming media streams to a timestamped MP4 file. It uses `aiortc` for WebRTC and `websockets` for signaling.

---

## Features

- Connects to the official PeerJS signaling server (`wss://0.peerjs.com`).
- Handles WebRTC signaling (SDP offers/answers and ICE candidates).
- Receives and records audio/video streams to a timestamped MP4 file.
- Supports dynamic peer IDs and secure WebSocket communication.

---

## Prerequisites

1. **Python Version**: Ensure you are using Python 3.7 or later.
2. **Dependencies**: Install the required Python packages:
   ```bash
   pip install aiortc websockets
   ```

3. **Signaling Server**: This script uses the official PeerJS signaling server (`wss://0.peerjs.com`). Ensure the server is accessible from your network.

---

## Installation

1. Clone this repository or copy the script to a local file (e.g., `webrtc_client.py`).
2. Install the required dependencies:
   ```bash
   pip install aiortc websockets
   ```

---

## Usage

### 1. Update the Peer ID
Replace the `peer_id` with a unique identifier for your client:

```python
peer_id = "mastapi"  # Replace with a unique identifier
```

### 2. Run the Script
Execute the script to start the client:

```bash
python webrtc_client.py
```

### 3. Connect a Remote Peer
Use another PeerJS-compatible client to establish a WebRTC connection with this client. For example:
- A JavaScript client in a web browser using the PeerJS library.
- Another instance of this script with a different peer ID.

---

## Output

- **Media Recording**: The script saves incoming audio and video streams to a file named with a timestamp, e.g., `20241117_143550.mp4`.
- **Logs**: The script logs all signaling events and connection status to the console.

---

## How It Works

### 1. Signaling
- The client connects to the PeerJS signaling server using the WebSocket protocol.
- It sends a handshake message to register with the server.

### 2. WebRTC Connection
- When an SDP offer is received, the script:
  - Sets the offer as the remote description.
  - Creates an SDP answer and sends it back to the signaling server.
- ICE candidates are exchanged to establish a peer-to-peer connection.

### 3. Media Handling
- Incoming audio and video tracks are added to an `aiortc` MediaRecorder, which saves the streams to an MP4 file.

---

## Example Log Output

```plaintext
Connecting to PeerJS server at wss://0.peerjs.com/peerjs?id=mastapi&token=12345678-abcd-ef01-2345-6789abcdef01&key=peerjs
Connected to PeerJS server.
Sent handshake: {'type': 'open', 'id': 'mastapi', 'key': 'peerjs', 'token': '12345678-abcd-ef01-2345-6789abcdef01'}
Received message: {'type': 'offer', 'src': 'remote-peer-id', 'payload': {'sdp': {'sdp': '...', 'type': 'offer'}}}
Processing offer...
Track received: video
Track received: audio
Recording saved to 20241117_143550.mp4
```

---

## Customization

- **Media File Format**:
  Change the output format by modifying the `MediaRecorder` initialization:
  ```python
  self.recorder = MediaRecorder("output.webm")
  ```

- **PeerJS Server**:
  If you want to use a custom PeerJS server, update the `server_url` parameter:
  ```python
  server_url="wss://your-custom-peerjs-server.com"
  ```

---

## Dependencies

- [`aiortc`](https://github.com/aiortc/aiortc): Python library for WebRTC and real-time media processing.
- [`websockets`](https://websockets.readthedocs.io/): Library for WebSocket communication.

---

## License

This script is provided under the MIT License. Feel free to modify and distribute it.

---

## Contact

For questions or support, please reach out via the repository issue tracker or email jyrone.parker@gmail.com.