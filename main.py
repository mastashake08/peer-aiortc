import asyncio
import websockets
import json
import uuid
from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack
from aiortc.contrib.media import MediaRecorder
from datetime import datetime

class SignalingClient:
    def __init__(self, peer_id, server_url="wss://0.peerjs.com", key="peerjs"):
        self.peer_id = peer_id
        self.server_url = server_url
        self.key = key
        self.token = str(uuid.uuid4())
        self.ws_url = f"{server_url}/peerjs?id={peer_id}&token={self.token}&key={key}"
        self.pc = RTCPeerConnection()

        # Create a timestamped output file name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_file = f"./{timestamp}.mp4"

        # Initialize MediaRecorder with the timestamped filename
        self.recorder = MediaRecorder(self.output_file)

    async def handle_signaling(self, websocket):
        """
        Handle incoming signaling messages and process SDP/ICE candidates.
        """
        async for message in websocket:
            data = json.loads(message)
            print(f"Received message: {data}")
            if data["type"] == "OFFER":
                print("Processing offer...")
                # Set remote description
                offer = RTCSessionDescription(sdp=data["payload"]["sdp"]["sdp"], type="offer")
                await self.pc.setRemoteDescription(offer)
                # Add a recorder for incoming tracks
                @self.pc.on("track")
                async def on_track(track: MediaStreamTrack):
                    print(f"Track received: {track.kind}")
                    self.recorder.addTrack(track)

                # Start recording
                await self.recorder.start()

                # Create and send an answer
                answer = await self.pc.createAnswer()

                self.pc.createDataChannel(label="mastapi")
                await self.pc.setLocalDescription(answer)
                
                answer_message = {
                    "type": "ANSWER",
                    "src": data["dst"],
                    "dst": data["src"],
                    "payload": {
                        "sdp": {
                            "sdp:": self.pc.localDescription.sdp,
                            "type": "answer"
                        },
                        'type': 'media', 
                        'connectionId': data["payload"]['connectionId']
                    }
                }
                await websocket.send(json.dumps(answer_message))
                print("Sent answer message.")

            elif data["type"] == "CANDIDATE":
                print("Processing ICE candidate...")

                candidate = data["payload"]["candidate"]
                print(candidate)
                if candidate:
                    await self.pc.addIceCandidate(candidate)

    async def connect(self):
        """
        Connect to the PeerJS server and handle signaling.
        """
        print(f"Connecting to PeerJS server at {self.ws_url}")
        try:
            async with websockets.connect(self.ws_url) as websocket:
                print("Connected to PeerJS server.")

                # Send handshake message
                handshake_message = {
                    "type": "open",
                    "id": self.peer_id,
                    "key": self.key,
                    "token": self.token,
                }
                await websocket.send(json.dumps(handshake_message))
                print(f"Sent handshake: {handshake_message}")

                # Handle signaling
                await self.handle_signaling(websocket)

        except Exception as e:
            print(f"Connection failed: {e}")
        finally:
            # Stop recording and close WebRTC connection
            await self.recorder.stop()
            print(f"Recording saved to {self.output_file}")
            await self.pc.close()


# Example usage
if __name__ == "__main__":
    peer_id = "mastapi"  # Replace with a unique identifier
    client = SignalingClient(peer_id)
    asyncio.run(client.connect())
