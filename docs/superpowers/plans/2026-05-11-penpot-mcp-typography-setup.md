# Penpot MCP Typography Setup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Set up Penpot MCP server to enable adding typography to images via MCP client commands, allowing users to copy images to the penpot-arena folder and use MCP client to add text overlays.

**Architecture:** Run a self-hosted Penpot instance using Docker, deploy the Penpot MCP server to connect to it via API and database access, configure for local file system access to upload images from the penpot-arena folder.

**Tech Stack:** Docker, PostgreSQL, Penpot (Clojure), MCP server (Clojure), local file system access.

---

### Task 1: Set up self-hosted Penpot instance

**Files:**
- Create: docker-compose.yml (for Penpot)
- Create: .env (environment configuration)

- [ ] **Step 1: Clone Penpot repository**

```bash
git clone https://github.com/penpot/penpot.git penpot-repo
cd penpot-repo
```

- [ ] **Step 2: Create Docker environment file**

```bash
cat > .env << 'EOF'
PENPOT_PUBLIC_URI=http://localhost:9001
PENPOT_DATABASE_URI=postgresql://penpot:penpot@localhost/penpot
PENPOT_DATABASE_USERNAME=penpot
PENPOT_DATABASE_PASSWORD=penpot
PENPOT_REDIS_URI=redis://localhost:6379
PENPOT_ASSETS_STORAGE_BACKEND=assets-fs
PENPOT_STORAGE_ASSETS_FS_DIRECTORY=/opt/data/assets
EOF
```

- [ ] **Step 3: Start Penpot with Docker Compose**

```bash
docker-compose -f docker-compose.yaml up -d
```

Expected: Penpot starts on http://localhost:9001

- [ ] **Step 4: Verify Penpot is running**

```bash
curl -s http://localhost:9001 | head -20
```

Expected: HTML content from Penpot

- [ ] **Step 5: Commit Penpot setup**

```bash
git add docker-compose.yml .env
git commit -m "feat: set up self-hosted Penpot instance"
```

---

### Task 2: Clone and configure Penpot MCP server

**Files:**
- Create: mcp-server/ (cloned repo)
- Modify: mcp-server/.env (configuration)

- [ ] **Step 1: Clone MCP server repository**

```bash
git clone https://github.com/ancrz/penpot-mcp-server.git mcp-server
cd mcp-server
```

- [ ] **Step 2: Install dependencies**

```bash
# Assuming Clojure CLI is installed
clojure -P
```

- [ ] **Step 3: Create environment configuration**

```bash
cat > .env << 'EOF'
PENPOT_BASE_URL=http://localhost:9001
DATABASE_URL=postgresql://penpot:penpot@localhost/penpot
PENPOT_ACCESS_TOKEN=your_access_token_here
EOF
```

Note: Get access token from Penpot UI after login

- [ ] **Step 4: Test MCP server connection**

```bash
# Run a quick test to verify database connection
clojure -M -e "(require '[next.jdbc :as jdbc]) (jdbc/execute! (jdbc/get-datasource (System/getenv \"DATABASE_URL\")) [\"SELECT 1\"])"
```

Expected: No errors, returns result

- [ ] **Step 5: Commit MCP server setup**

```bash
git add .env
git commit -m "feat: clone and configure Penpot MCP server"
```

---

### Task 3: Configure MCP client and test typography workflow

**Files:**
- Create: test-image.jpg (sample image)
- Create: mcp-config.json (client configuration)

- [ ] **Step 1: Copy sample image to folder**

```bash
cp /path/to/sample/image.jpg ./test-image.jpg
```

- [ ] **Step 2: Create MCP client configuration**

```json
{
  "mcpServers": {
    "penpot": {
      "command": "clojure",
      "args": ["-M", "-m", "penpot-mcp-server.core"],
      "env": {
        "PENPOT_BASE_URL": "http://localhost:9001",
        "DATABASE_URL": "postgresql://penpot:penpot@localhost/penpot",
        "PENPOT_ACCESS_TOKEN": "your_token"
      }
    }
  }
}
```

- [ ] **Step 3: Test image upload via MCP**

Use MCP client to call upload_media tool with path to test-image.jpg

Expected: Image uploaded to Penpot file

- [ ] **Step 4: Test typography creation**

Use MCP client to call create_text tool to add text overlay on the image

Expected: Text element created on the design

- [ ] **Step 5: Test export**

Use MCP client to export the frame as PNG

Expected: Image with typography exported

- [ ] **Step 6: Commit test configuration**

```bash
git add test-image.jpg mcp-config.json
git commit -m "feat: configure MCP client and test typography workflow"
```

---

### Task 4: Document usage instructions

**Files:**
- Create: README.md (usage guide)

- [ ] **Step 1: Write usage instructions**

```markdown
# Penpot MCP Typography Setup

## Setup
1. Ensure Docker and Docker Compose are installed
2. Run Penpot: `cd penpot-repo && docker-compose up -d`
3. Run MCP server: `cd mcp-server && clojure -M -m penpot-mcp-server.core`

## Usage
1. Copy your images to the penpot-arena folder
2. Use MCP client (e.g., Claude Desktop) with the configuration
3. Command: "Upload the image from /path/to/penpot-arena/image.jpg to Penpot"
4. Command: "Add typography 'Hello World' in Arial font, size 24, position 100,100"
5. Command: "Export the frame as PNG to /path/to/output.png"
```

- [ ] **Step 2: Commit documentation**

```bash
git add README.md
git commit -m "docs: add usage instructions for Penpot MCP typography"
```
</content>
<parameter name="filePath">docs/superpowers/plans/2026-05-11-penpot-mcp-typography-setup.md