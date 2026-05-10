# Penpot MCP Typography Workflow

## Overview
Use the hosted Penpot MCP server to add typography (text) to your images. Since the hosted server doesn't support direct local file access, you'll upload images manually to Penpot first, then use MCP commands to add text overlays.

## Setup
1. Save the `mcp-config.json` file to your MCP client's configuration directory
2. Ensure your MCP client (like Claude Desktop) is configured to use this config

## Workflow
1. **Copy your desired image** to the `penpot-arena` folder (e.g., `image.jpg`)

2. **Upload the image to Penpot:**
   - Go to https://design.penpot.app
   - Create a new file or open existing
   - Upload your image file manually via the Penpot UI (drag & drop or upload button)

3. **Use MCP client commands** to add typography:
   - "Create a text element with content 'Your Text Here' at position x=100, y=100"
   - "Set the font to Arial, size 24, color black"
   - "Position the text over the uploaded image"

4. **Export the result:**
   - "Export the current frame as PNG"

## Example Commands
- "Add typography 'Hello World' in bold Arial font, size 36, centered on the image"
- "Create text overlay with 'Sample Text' in white color with shadow effect"
- "Add multiple text elements for title and subtitle on the background image"

## Notes
- The hosted MCP server provides access to Penpot's design tools for creating and styling text
- For fully automated local file processing, a local MCP server setup would be needed
- Keep your user token secure and don't share the config file