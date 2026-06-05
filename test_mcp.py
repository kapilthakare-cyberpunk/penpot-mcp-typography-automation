#!/usr/bin/env python3
import urllib.request
import json
import base64

print("Testing MCP connection...")

# Test 1: Initialize
print("\n1. Testing initialization...")
try:
    req = urllib.request.Request("http://localhost:4401/mcp")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    
    init_data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0",
            },
        },
    }
    
    data = json.dumps(init_data).encode("utf-8")
    req.data = data
    
    response = urllib.request.urlopen(req)
    print(f"Response status: {response.status}")
    print(f"Response headers: {dict(response.headers)}")
    
    # Check for session ID in headers
    session_id = response.headers.get('mcp-session-id')
    print(f"Session ID from headers: {session_id}")
    
    # Read the response body
    response_body = response.read().decode('utf-8')
    print(f"Response body: {response_body}")
    
except Exception as e:
    print(f"Error during initialization: {e}")
    import traceback
    traceback.print_exc()

print("\nTest complete.")
