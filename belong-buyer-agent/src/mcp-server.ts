/**
 * Servidor MCP del belong-buyer-agent — transporte stdio.
 *
 * Para Claude Desktop con servidor local (claude_desktop_config.json).
 * La configuración del servidor vive en mcp-app.ts.
 *
 * Arranque: `npm run mcp`.
 */

import "dotenv/config";
import { buildMcpServer } from "./mcp-app";

const server = buildMcpServer();

// stdio: el transporte que usa Claude Desktop para servidores MCP locales.
await server.startStdio();
