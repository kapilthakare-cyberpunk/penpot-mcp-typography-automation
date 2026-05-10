#!/bin/bash

# Penpot MCP Typography Automation Script
# Watches input-images folder and triggers MCP server + notifications

INPUT_DIR="./input-images"
OUTPUT_DIR="./output-exports"

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Penpot MCP Typography Automation...${NC}"
echo "Watching folder: $INPUT_DIR"
echo "Output folder: $OUTPUT_DIR"
echo "Press Ctrl+C to stop"
echo

# Function to show notification and start MCP server
process_image() {
    local image_path="$1"
    local filename=$(basename "$image_path")

    echo -e "${YELLOW}New image detected: $filename${NC}"

    # Start MCP server in background if not already running
    if ! pgrep -f "clojure.*penpot-mcp-server" > /dev/null; then
        echo "Starting MCP server..."
        cd mcp-server && export PATH="/opt/homebrew/bin:$PATH" && nohup clojure -M -m penpot-mcp-server.core > ../mcp-server.log 2>&1 &
        sleep 3  # Wait for server to start
        echo -e "${GREEN}MCP server started${NC}"
    fi

    # Show terminal notification
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}📸 New image ready for typography: $filename${NC}"
    echo -e "${GREEN}Use your MCP client to add typography instructions${NC}"
    echo -e "${GREEN}Example: 'Upload the image from input-images/$filename and add typography \"Hello World\" at position 100,100'${NC}"
    echo -e "${GREEN}========================================${NC}"

    # macOS system notification
    osascript -e "display notification \"New image: $filename\" with title \"Penpot Typography Ready\" subtitle \"Use MCP client for typography instructions\""
}

# Check if fswatch is available
if ! command -v fswatch &> /dev/null; then
    echo -e "${RED}Error: fswatch is not installed. Install with: brew install fswatch${NC}"
    exit 1
fi

# Check if input directory exists
if [ ! -d "$INPUT_DIR" ]; then
    echo -e "${RED}Error: Input directory $INPUT_DIR does not exist${NC}"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Watch for new image files
fswatch -0 -l 5 -e ".*" -i "\\.(jpg|jpeg|png|gif|webp)$" "$INPUT_DIR" | while read -d "" event; do
    # Only process created files
    if [[ "$event" == *.jpg ]] || [[ "$event" == *.jpeg ]] || [[ "$event" == *.png ]] || [[ "$event" == *.gif ]] || [[ "$event" == *.webp ]]; then
        process_image "$event"
    fi
done