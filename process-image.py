#!/usr/bin/env python3
"""
Penpot MCP Typography Automation
A Python script that automates adding typography to images via Penpot MCP server.

Usage:
  python3 process-image.py <image_path> [--text "Headline" "Subhead"]
"""

import subprocess
import sys
import os
import time
import json
import signal

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MCP_SERVER_DIR = os.path.join(SCRIPT_DIR, "mcp-server")
INPUT_DIR = os.path.join(SCRIPT_DIR, "input-images")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output-exports")
ENV_FILE = os.path.join(SCRIPT_DIR, ".env")

# Colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"

mcp_process = None


def banner():
    print(f"""
{BOLD}{GREEN}╔══════════════════════════════════════════════════════════╗
║  🎨 Penpot MCP Typography Automation                    ║
║  Automated typography overlay on images                  ║
╚══════════════════════════════════════════════════════════╝{RESET}
""")


def load_env():
    """Load environment variables from .env file"""
    env_vars = {}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip()
                    os.environ[key.strip()] = value.strip()
    return env_vars


def start_mcp_server():
    """Start the MCP server if not already running"""
    global mcp_process

    # Check if server is already running
    result = subprocess.run(
        ["pgrep", "-f", "node.*dist/index.js"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"{BLUE}ℹ MCP server already running{RESET}")
        return True

    print(f"{YELLOW}⏳ Starting MCP server...{RESET}")

    env = os.environ.copy()
    env.update(load_env())
    env["TRANSPORT"] = "http"
    env["HTTP_PORT"] = "4401"

    mcp_process = subprocess.Popen(
        ["node", "dist/index.js"],
        cwd=MCP_SERVER_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        env=env
    )

    # Wait for server to start
    for i in range(15):
        try:
            import urllib.request
            req = urllib.request.urlopen("http://localhost:4401/health", timeout=2)
            if req.status == 200:
                print(f"{GREEN}✅ MCP server started successfully{RESET}")
                print(f"{GREEN}   Endpoint: http://localhost:4401/mcp{RESET}")
                return True
        except:
            time.sleep(1)

    print(f"{RED}❌ MCP server failed to respond{RESET}")
    print(f"{RED}   Check: tail -f {MCP_SERVER_DIR}/mcp-server.log{RESET}")
    return False


def stop_mcp_server():
    """Stop the MCP server"""
    global mcp_process
    if mcp_process:
        mcp_process.terminate()
        try:
            mcp_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            mcp_process.kill()
        print(f"{YELLOW}⏹ MCP server stopped{RESET}")


def create_mcp_request(request_id, method, params=None):
    """Create an MCP JSON-RPC request"""
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
        "params": params or {}
    }


def send_mcp_request(payload):
    """Send an MCP request via HTTP POST"""
    import urllib.request
    import urllib.error

    url = "http://localhost:4401/mcp"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}


def upload_image(image_path):
    """Upload an image to Penpot"""
    print(f"{YELLOW}📤 Uploading image...{RESET}")

    with open(image_path, "rb") as f:
        image_data = f.read()

    import base64
    encoded = base64.b64encode(image_data).decode("utf-8")

    payload = create_mcp_request("upload", "upload_file_media", {
        "fileData": encoded,
        "fileName": os.path.basename(image_path),
        "mimeType": "image/jpeg"
    })

    result = send_mcp_request(payload)
    if "error" in result:
        print(f"{RED}❌ Upload failed: {result['error']}{RESET}")
        return None

    media_id = result.get("result", {}).get("id")
    print(f"{GREEN}✅ Image uploaded successfully{RESET}")
    return media_id


def create_text_overlay(media_id, text, x=100, y=100, font_size=48, color="#FFFFFF"):
    """Create a text overlay on the image"""
    print(f"{YELLOW}🔤 Creating typography overlay...{RESET}")

    payload = create_mcp_request("text", "create_text", {
        "x": x,
        "y": y,
        "content": text,
        "fontSize": font_size,
        "fontFamily": "Inter",
        "fontWeight": "bold",
        "fill": color,
        "textAlign": "center"
    })

    result = send_mcp_request(payload)
    if "error" in result:
        print(f"{RED}❌ Text creation failed: {result['error']}{RESET}")
        return None

    shape_id = result.get("result", {}).get("id")
    print(f"{GREEN}✅ Typography added successfully{RESET}")
    return shape_id


def export_design(output_path):
    """Export the design"""
    print(f"{YELLOW}📦 Exporting design...{RESET}")

    payload = create_mcp_request("export", "export_shape", {
        "format": "png",
        "scale": 2
    })

    result = send_mcp_request(payload)
    if "error" in result:
        print(f"{RED}❌ Export failed: {result['error']}{RESET}")
        return False

    # Save to output path
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_file = os.path.join(OUTPUT_DIR, output_path)
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2)

    print(f"{GREEN}✅ Exported to: {out_file}{RESET}")
    return True


def print_usage():
    """Print usage instructions"""
    print(f"""
{BOLD}Usage:{RESET}
  python3 process-image.py <image_path> [options]

{BOLD}Options:{RESET}
  --text "Headline" "Subhead"   Custom text overlay
  --title "Text"                Headline text
  --subtitle "Text"             Subtitle text
  --url "Text"                  URL text
  --position x,y                Text position (default: 100,100)
  --size N                      Font size (default: 48)
  --color #RRGGBB               Text color (default: #FFFFFF)
  --export                      Export result
  --help                        Show this help

{BOLD}Example:{RESET}
  python3 process-image.py input-images/photo.jpg \\
    --title "THE MARKETPLACE" \\
    --subtitle "IS LIVE." \\
    --url "buysell.primesandzooms.com" \\
    --export
""")


def main():
    banner()

    if len(sys.argv) < 2 or "--help" in sys.argv:
        print_usage()
        sys.exit(0)

    image_path = sys.argv[1]

    if not os.path.exists(image_path):
        print(f"{RED}❌ Image not found: {image_path}{RESET}")
        sys.exit(1)

    # Parse arguments
    args = sys.argv[2:]
    title = None
    subtitle = None
    url_text = None
    position = (100, 100)
    font_size = 48
    color = "#FFFFFF"
    do_export = False

    i = 0
    while i < len(args):
        if args[i] == "--title" and i + 1 < len(args):
            title = args[i + 1]
            i += 2
        elif args[i] == "--subtitle" and i + 1 < len(args):
            subtitle = args[i + 1]
            i += 2
        elif args[i] == "--url" and i + 1 < len(args):
            url_text = args[i + 1]
            i += 2
        elif args[i] == "--position" and i + 1 < len(args):
            try:
                x, y = args[i + 1].split(",")
                position = (int(x), int(y))
                i += 2
            except:
                print(f"{RED}Invalid position format. Use x,y{RESET}")
                sys.exit(1)
        elif args[i] == "--size" and i + 1 < len(args):
            font_size = int(args[i + 1])
            i += 2
        elif args[i] == "--color" and i + 1 < len(args):
            color = args[i + 1]
            i += 2
        elif args[i] == "--export":
            do_export = True
            i += 1
        else:
            i += 1

    try:
        if not start_mcp_server():
            sys.exit(1)

        # Upload image
        media_id = upload_image(image_path)
        if not media_id:
            print(f"{RED}❌ Failed to upload image{RESET}")
            sys.exit(1)

        # Create typography overlays
        y_offset = position[1]
        line_height = 60

        if title:
            print(f"\n{BOLD}Adding headline:{RESET} {title}")
            create_text_overlay(media_id, title, position[0], y_offset, font_size + 12, color)
            y_offset += line_height * 2

        if subtitle:
            print(f"\n{BOLD}Adding subtitle:{RESET} {subtitle}")
            create_text_overlay(media_id, subtitle, position[0], y_offset, font_size, "#8F98A1")
            y_offset += line_height

        if url_text:
            print(f"\n{BOLD}Adding URL:{RESET} {url_text}")
            create_text_overlay(media_id, url_text, position[0], y_offset, font_size - 4, "#E63946")

        if do_export:
            output_name = os.path.basename(image_path).rsplit(".", 1)[0] + "-typed.png"
            export_design(output_name)

        print(f"\n{GREEN}{BOLD}✨ Typography overlay complete!{RESET}")
        print(f"{BLUE}Open Penpot to view and refine your design{RESET}")

    except KeyboardInterrupt:
        print(f"\n{YELLOW}Interrupted{RESET}")
    finally:
        if mcp_process:
            stop_mcp_server()


if __name__ == "__main__":
    main()