import argparse
from mentalHealth import detect_mental_health

parser = argparse.ArgumentParser()
parser.add_argument('--type', type=str, required=True)
parser.add_argument('--port', type=int, required=True)
args = parser.parse_args()

arg1 = args.type

if arg1=="runserver":
    pass
elif arg1=="websocket":
    import asyncio
    import websockets
    
    port = args.port

    print("Starting Server....")
    async def server(websocket, path):
        try:
            async for message in websocket:
                # print(message)
                res = detect_mental_health(message)
                # print (res)
                await websocket.send(f'Mental Health: {res}')
        except:
            pass

    print("Server Started")

    start_server = websockets.serve(server, "0.0.0.0", port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

    print("Server Stopped")