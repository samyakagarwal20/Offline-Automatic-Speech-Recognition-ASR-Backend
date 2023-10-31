from vosk import Model, KaldiRecognizer
import pyaudio
import json
import websockets
import asyncio
from threading import Event

model = Model(r"E:\Hands-on\Models\Pre-Trained\Speech_to_Text\vosk-model-en-us-0.22-lgraph")
mic = None
stream = None
is_recording = False
capture_thread = None
stop_event = Event()
rec = KaldiRecognizer(model, 16000)
queue = asyncio.Queue()
print('Recognition Module Initialized')

async def start_audio_capture():
    global is_recording, mic, stream, stop_event, queue
    
    print('Capturing audio...')
    stream.start_stream()
    while not stop_event.is_set():
        data = stream.read(4096, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            text = rec.Result()
            formatted_text = text[14:-3]
            print(formatted_text)
            await queue.put(formatted_text)
            await asyncio.sleep(0.1)

def stop_audio_capture():
    global mic, stream

    print('Stopping audio capture...')
    if stream is None and mic is None:
        print('Audio capture is already stopped')
    else:
        if stream is not None:
            stream.stop_stream()
            stream.close()
    
        if mic is not None:
            mic.terminate()
        
        print('Audio capturing stopped!')

    stream = None
    mic = None

async def send_transcriptions(websocket):
    global queue, is_recording

    print('preparing to send transcribed text in parallel...')
    while not stop_event.is_set():
        transcribed_text = await queue.get()
        if transcribed_text:
            await websocket.send(json.dumps({'data': transcribed_text}))
            await asyncio.sleep(0.1)

async def websocket_server(websocket, uri):
    print(f"New WebSocket connection from {uri}")
    global is_recording, mic, stream, capture_thread, stop_event

    async for message in websocket:
        print('Message received : ', message)
        message_data = json.loads(message)
        if 'message' in message_data:
            command = message_data['message']
            if command == 'start':
                stop_event.clear()
                mic = pyaudio.PyAudio()
                stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
                audio_capture_task = asyncio.create_task(start_audio_capture())
                transcription_task = asyncio.create_task(send_transcriptions(websocket))
            elif command == 'stop':
                stop_event.set()
                await audio_capture_task
                await transcription_task
                stop_audio_capture()

start_server = websockets.serve(websocket_server, "localhost", 8765)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()
