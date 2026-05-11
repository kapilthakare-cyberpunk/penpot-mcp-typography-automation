#!/bin/bash

# Penpot MCP Typography Automation Script
# Watches input-images folder and triggers MCP server + notifications

INPUT_DIR="./input-images"
OUTPUT_DIR="./output-exports"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Penpot MCP Typography Automation${NC}"
echo -e "${GREEN}========================================${NC}"
echo "Watching folder: $INPUT_DIR"
echo "Output folder: $OUTPUT_DIR"
echo "Press Ctrl+C to stop"
echo

MCP_PID=""

cleanup() {
    echo -e "\n${YELLOW}Stopping...${NC}"
    if [ -n "$MCP_PID" ]; then
        kill "$MCP_PID" 2>/dev/null || true
        wait "$MCP_PID" 2>/dev/null || true
        echo -e "${GREEN}MCP server stopped${NC}"
    fi
    echo -e "${GREEN}Goodbye!${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

start_mcp_server() {
    if pgrep -f "node.*dist/index.js" > /dev/null 2>&1; then
        echo -e "${BLUE}MCP server already running${NC}"
        return 0
    fi

    echo -e "${YELLOW}Starting MCP server...${NC}"
    
    # Source .env and start server with HTTP transport
    export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
    cd "$SCRIPT_DIR/mcp-server" || { echo -e "${RED}Failed to cd to mcp-server${NC}"; exit 1; }
    
    TRANSPORT=http HTTP_PORT=4401 node dist/index.js > "$SCRIPT_DIR/mcp-server.log" 2>&1 &
    MCP_PID=$!

    local retries=0
    while [ $retries -lt 15 ]; do
        if curl -s http://localhost:4401/health > /dev/null 2>&1; then
            echo -e "${GREEN}MCP server started (PID: $MCP_PID)${NC}"
            echo -e "${GREEN}Endpoint: http://localhost:4401/mcp${NC}"
            return 0
        fi
        sleep 1
        retries=$((retries + 1))
    done

    echo -e "${RED}Warning: MCP server started but health check timed out${NC}"
    echo -e "${RED}Check: tail -f $SCRIPT_DIR/mcp-server.log${NC}"
    return 1
}

process_image() {
    local image_path="$1"
    local filename
    filename=$(basename "$image_path")

    echo -e "${YELLOW}────────────────────────────────────────${NC}"
    echo -e "${YELLOW}📸  New image detected: $filename${NC}"
    echo -e "${YELLOW}────────────────────────────────────────${NC}"

    start_mcp_server

    echo
    echo -e "${GREEN}  ✅ MCP server is running at http://localhost:4401${NC}"
    echo -e "${GREEN}  📋 Send commands to your MCP client:${NC}"
    echo
    echo -e "${BLUE}  \"Upload the image from penpot-arena/input-images/$filename\"${NC}"
    echo -e "${BLUE}  \"Add typography 'THE MARKETPLACE' Barlow Semi Condensed Bold 700\"${NC}"
    echo -e "${BLUE}  \"Export frame as PNG to output-exports/$filename\"${NC}"
    echo
    echo -e "${GREEN}  📁 Output: $OUTPUT_DIR/${NC}"
    echo -e "${YELLOW}────────────────────────────────────────${NC}"
    echo

    osascript -e "display notification \"New image: $filename\" with title \"Penpot MCP Ready\" subtitle \"Send typography commands to MCP client\"" 2>/dev/null || true
}

if ! command -v fswatch &> /dev/null; then
    echo -e "${RED}Error: fswatch not installed. Run: brew install fswatch${NC}"
    exit 1
fi

if [ ! -d "$INPUT_DIR" ]; then
    echo -e "${RED}Error: Directory $INPUT_DIR not found${NC}"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"
start_mcp_server

echo -e "${GREEN}Watching for images... (JPG, PNG, GIF, WEBP)${NC}"
echo

fswatch -0 -l 3 -e ".*" -i "\\.(jpg|jpeg|png|gif|webp)$" "$INPUT_DIR" | while read -d "" event; do
    if [[ "$event" == *.jpg ]] || [[ "$event" == *.jpeg ]] || \
       [[ "$event" == *.png ]] || [[ "$event" == *.gif ]] || \
       [[ "$event" == *.webp ]]; then
        process_image "$event"
    fi
done
