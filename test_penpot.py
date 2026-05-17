import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("PENPOT_API_URL", "https://design.penpot.app")
TOKEN = os.getenv("PENPOT_ACCESS_TOKEN")

headers = {
    "Authorization": f"Token {TOKEN}"
}

def run_test():
    # 1. Create a dummy PNG file
    with open("dummy.png", "wb") as f:
        f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDAT\x08\x99c\xf8\x0f\x04\x00\x09\xfb\x03\xfd\xe3U\xf2\x9c\x00\x00\x00\x00IEND\xaeB`\x82')
        
    # We need a valid file ID. Let's start the MCP server locally and ask it to create a file?
    # Or just parse Transit JSON.
    res = requests.post(f"{API_URL}/api/rpc/command/get-teams", headers={"Authorization": f"Token {TOKEN}", "Content-Type": "application/json"}, json={})
    # Response is transit JSON like: [["^ ", "~:id", "~u8c927302-d076-8020-8007-fdfc63077dc0", ...]]
    text = res.text
    # Extract team ID
    team_id = re.search(r'~:id.*?~u([0-9a-f-]+)', text).group(1)
    
    # Get project
    res = requests.post(f"{API_URL}/api/rpc/command/get-projects", headers={"Authorization": f"Token {TOKEN}", "Content-Type": "application/json"}, json={"team-id": team_id})
    text = res.text
    project_match = re.search(r'~:id.*?~u([0-9a-f-]+)', text)
    if not project_match:
        res = requests.post(f"{API_URL}/api/rpc/command/create-project", headers={"Authorization": f"Token {TOKEN}", "Content-Type": "application/json"}, json={"team-id": team_id, "name": "API Test"})
        text = res.text
        project_id = re.search(r'~:id.*?~u([0-9a-f-]+)', text).group(1)
    else:
        project_id = project_match.group(1)
        
    # Create file
    res = requests.post(f"{API_URL}/api/rpc/command/create-file", headers={"Authorization": f"Token {TOKEN}", "Content-Type": "application/json"}, json={"project-id": project_id, "name": "Auto-Generated File"})
    text = res.text
    file_id = re.search(r'~:id.*?~u([0-9a-f-]+)', text).group(1)
    print("File ID:", file_id)

    # 4. Upload Image (Multipart)
    with open("dummy.png", "rb") as f:
        files = {
            "content": ("dummy.png", f, "image/png")
        }
        data = {
            "file-id": file_id,
            "is-local": "true",
            "name": "dummy.png"
        }
        res = requests.post(f"{API_URL}/api/rpc/command/upload-file-media-object", headers=headers, files=files, data=data)
        print("Upload Status:", res.status_code)
        print("Upload Response:", res.text)
        
        # Check if media ID is returned
        media_match = re.search(r'~:id.*?~u([0-9a-f-]+)', res.text)
        if media_match:
            print("Media ID:", media_match.group(1))

if __name__ == "__main__":
    run_test()
