# MCP Server Configuration Update

## Overview
This document describes the changes made to configure the Penpot MCP Server for use with various AI coding assistants.

## Changes Made

### Previous Configuration (Claude Desktop)
- Connected to the hosted Penpot MCP server at `https://design.penpot.app/mcp/stream`
- Used HTTP/SSE transport with token embedded in the URL

### Updated Configuration (Claude Desktop)
- Switched to using the **local** Penpot MCP server via stdio transport
- Claude Desktop now spawns and manages the local MCP server as a subprocess
- Configuration moved to environment variables for better security and flexibility

## New Claude Desktop Configuration
The following configuration has been applied to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "penpot": {
      "command": "node",
      "args": ["/Users/kapilthakare/Projects/penpot-arena/mcp-server/dist/index.js"],
      "env": {
        "PENPOT_ACCESS_TOKEN": "eyJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2R0NNIn0.YirDdlG558ODcBdPxYWjqMgVrB6cY5ZQxnMmcnPIgPUwCYrfJbGC_Q.qe9SNTa3_jq5KWcm.jJkvgTuevWkK167wRWHenStRl8V018SGISnVzDP3YTliXsggms8CGoDbogGUK-gaR73NwV01bvOOjMK2skRQNseLI-aisz_gk_rVIFPYS5tV_hewhBT0Xc5txojatfscUZA1Q2XiZTm4OFHjnjkmSEeqL0aA_kKrUs62h9bWmXP0TQU09-8pF8on2UwHYZ2YTfzxDdBLAC1A.sIPGDFSPALpCTOukTFXZAQ",
        "PENPOT_API_URL": "https://design.penpot.app",
        "TRANSPORT": "stdio"
      }
    }
  },
  "preferences": {
    "coworkScheduledTasksEnabled": false,
    "ccdScheduledTasksEnabled": false,
    "coworkWebSearchEnabled": true,
    "epitaxyPrefs": {
      "starred-local-code-sessions": [],
      "starred-cowork-spaces": [],
      "starred-session-groups": [],
      "dframe-local-slice": {
        "pinnedOrder": [],
        "customGroupAssignments": {},
        "customGroupOrder": {}
      }
    }
  }
}
```

## Benefits of This Change
1. **Performance**: Direct stdio communication is faster than HTTP/SSE
2. **Reliability**: No network dependency for MCP server communication
3. **Security**: Token is stored in environment variables rather than URLs
4. **Self-contained**: The MCP server lifecycle is managed by the client

## Configuring for Other Tools

### Gemini CLI
Gemini CLI likely uses a similar MCP configuration format. To configure:

1. Locate Gemini's MCP configuration file (typically `~/.gemini/mcp_config.json` or similar)
2. Add the following configuration:

```json
{
  "mcpServers": {
    "penpot": {
      "command": "node",
      "args": ["/Users/kapilthakare/Projects/penpot-arena/mcp-server/dist/index.js"],
      "env": {
        "PENPOT_ACCESS_TOKEN": "your-token-here",
        "PENPOT_API_URL": "https://design.penpot.app",
        "TRANSPORT": "stdio"
      }
    }
  }
}
```

Replace `your-token-here` with your actual Penpot access token.

### Opencode
OpenCode CLI may use a configuration file at `~/.opencode/mcp.json` or project-specific `.opencode/mcp.json`:

```json
{
  "servers": {
    "penpot": {
      "command": "node",
      "args": ["/path/to/penpot-arena/mcp-server/dist/index.js"],
      "env": {
        "PENPOT_ACCESS_TOKEN": "your-token-here",
        "PENPOT_API_URL": "https://design.penpot.app",
        "TRANSPORT": "stdio"
      }
    }
  }
}
```

### Kilocode
Kilocode configuration may be located at `~/.kilocode/mcp_config.json` or similar:

```json
{
  "mcpServers": {
    "penpot": {
      "command": "node",
      "args": ["/Users/kapilthakare/Projects/penpot-arena/mcp-server/dist/index.js"],
      "env": {
        "PENPOT_ACCESS_TOKEN": "your-token-here",
        "PENPOT_API_URL": "https://design.penpot.app",
        "TRANSPORT": "stdio"
      }
    }
  }
}
```

## Verification
After updating the configuration for each tool:
1. Restart the respective application
2. Verify the MCP server connects successfully
3. Test with a simple Penpot operation (e.g., listing files)

## Troubleshooting
- Ensure Node.js is installed and accessible in PATH
- Verify the path to `dist/index.js` is correct
- Check that the access token is valid and has sufficient permissions
- Review server logs if connection issues occur

## Notes
- The token used in this example should be replaced with your actual token in production
- Keep your access token secure and do not share it publicly
- The local MCP server will be started/stopped automatically by each client as needed
