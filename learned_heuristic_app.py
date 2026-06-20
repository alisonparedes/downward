#from http.server import BaseHTTPRequestHandler, HTTPServer

#class Handler(BaseHTTPRequestHandler):
#    def do_GET(self):
#        self.send_response(200)
#        self.end_headers()
#        self.wfile.write(b"hello")
        

#server = HTTPServer(("0.0.0.0", 8080), Handler)
#server.serve_forever()

# A FastAPI application
from fastapi import FastAPI, Request
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
async def root():
    #return {"message": "Hello World"}
    return {"heuristic": 0}

@app.post("/heuristic")
async def heuristic(payload: dict):
    
    logger.info("Received request payload: %s", payload)
    
    state = payload["state"]  # Input to learned model
  
    h = 0

    return {"heuristic": h}