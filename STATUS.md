# Penpot Arena: Project Status & Technical Audit (May 18, 2026)

## 🎯 Current Status: **Partial Success / Blocked**

The project has been significantly upgraded to handle native Penpot asset management, but the automated typography overlay is currently blocked by a low-level protocol mismatch between the Python client and the MCP (Model Context Protocol) server.

---

## ✅ Completed Upgrades

### 1. Zero-Touch Native Image Upload
- **Old Way:** Script relied on an unimplemented MCP tool (`upload_file_media`) and required manual uploads to the Penpot UI.
- **New Way:** I implemented a native `requests`-based multipart upload that hits the Penpot RPC endpoint (`/api/rpc/command/upload-file-media-object`) directly.
- **Result:** Images are now automatically uploaded to a dedicated Penpot project ("API Test") and a new design file is created for every run.

### 2. Automation Pipeline Refinement
- The `process-image.py` script now handles the full lifecycle:
    1. Authentication via `.env` token.
    2. Dynamic Project/Team/File creation.
    3. Asset upload and Media ID retrieval.
    4. Page ID discovery (with REST fallback for SSE lag).

---

## ❌ Current Blockers

### 1. HTTP 406: Not Acceptable (MCP Protocol Mismatch)
Despite fixing the `Accept` header to include `text/event-stream`, the MCP server (built on the official SDK) is rejecting typography and shape commands with `HTTP 406`.
- **Diagnosis:** The MCP SDK's HTTP transport is designed strictly for Server-Sent Events (SSE). It expects a persistent connection for notifications and a specific handshake for commands. Sending isolated `POST` requests to the `/mcp` endpoint is causing the SDK to throw "Not Acceptable" or "Method not found" because it doesn't recognize the "stateless" command style.

### 2. Typography Logic Failure
- Because of the 406 errors, the commands to `create_rectangle` (for the background) and `create_text` (for the headers) are failing.
- **Result:** You see the file in Penpot, and the image is in the assets library, but the canvas remains empty.

---

## 🛠 Proposed Fixes

1. **Client-Side Upgrade:** Replace the manual `urllib`/`requests` JSON-RPC logic in `process-image.py` with a proper MCP Client implementation (using the `mcp` Python package). This will handle the SSE stream and session management correctly.
2. **Server-Side Bridge:** Modify `http-server.ts` to support a "Simple JSON" mode that bypasses SSE for automated scripts that don't need real-time notifications.
3. **Template Logic:** Once communication is restored, refine the `create_text_overlay` coordinates to handle center-alignment properly (currently hardcoded to 540x).

---

## 📝 How to View Current Progress
You can see the successfully uploaded images and generated files by visiting:
**[design.penpot.app](https://design.penpot.app)** -> **API Test Project** -> **Automation: [Filename]**
