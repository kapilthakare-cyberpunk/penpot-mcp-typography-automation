# Penpot MCP Typography Automation

## Overview
Automated system that watches the `input-images` folder for new images and triggers the MCP server with notifications for typography processing.

## Setup
1. Folders created: `input-images/` and `output-exports/`
2. Dependencies installed: `fswatch` for file watching
3. Script created: `watch-images.sh` for automation

## How to Use
1. Copy images (JPG, PNG, GIF, WEBP) to the `input-images` folder
2. The script will automatically:
   - Start the MCP server (if not running)
   - Show terminal notification with instructions
   - Display macOS system notification
3. Use your MCP client to provide typography instructions
4. The MCP client can export results to `output-exports/`

## Running the Automation
```bash
./watch-images.sh
```

## Example Workflow
1. Paste `photo.jpg` into `input-images/`
2. Script detects it and starts MCP server
3. Notifications appear: "New image: photo.jpg - Use MCP client for typography"
4. In MCP client: "Upload the image from input-images/photo.jpg and add typography 'Hello World' at position 100,100"
5. Export: "Export the frame as PNG to output-exports/photo-with-text.png"

## Files
- `input-images/`: Drop images here to trigger processing
- `output-exports/`: Exported results with typography
- `watch-images.sh`: Automation script
- `mcp-server.log`: MCP server logs

## Stopping
- Press Ctrl+C to stop watching
- MCP server will continue running until manually stopped