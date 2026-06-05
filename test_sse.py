#!/usr/bin/env python3
import urllib.request
import json

print("Testing SSE connection...")

try:
    req = urllib.request.Request("http://localhost:4401/mcp")
    req.add_header("Accept", "application/json, text/event-stream")
    
    response = urllib.request.urlopen(req)
    
    print(f"Response status: {response.status}")
    print(f"Response headers: {dict(response.headers)}")
    
    # Read a few lines
    for i in range(5):
        line = response.readline()
        if not line:
            break
        print(f"Line {i}: {line}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
