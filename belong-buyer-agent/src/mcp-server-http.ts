/**
 * Servidor MCP del belong-buyer-agent — transporte HTTP (Streamable HTTP).
 *
 * Es el que usa el "Add custom connector" de la app de Claude (URL remota).
 * Sirve el endpoint MCP en `/mcp` (y también en `/` para ser tolerante con la
 * URL que se pegue). Loggea cada request para diagnosticar el handshake.
 *
 * Arranque: `npm run mcp:http`  (escucha en PORT, por defecto 8080).
 * Para exponerlo a Claude necesitas una URL pública SIN intersticial, p.ej.:
 *   cloudflared tunnel --url http://localhost:8080
 */

import "dotenv/config";
import http from "node:http";
import { randomUUID } from "node:crypto";
import { buildMcpServer } from "./mcp-app";

const PORT = Number(process.env.PORT ?? 8080);
const MCP_PATHS = new Set(["/mcp", "/"]);

const server = buildMcpServer();

function log(...parts: unknown[]) {
  console.log(`[mcp-http]`, ...parts);
}

const httpServer = http.createServer(async (req, res) => {
  const url = new URL(req.url ?? "", `http://localhost:${PORT}`);
  const { method = "GET" } = req;
  log(
    method,
    url.pathname,
    `accept=${req.headers["accept"] ?? "-"}`,
    `auth=${req.headers["authorization"] ? "yes" : "no"}`,
    `ua=${req.headers["user-agent"] ?? "-"}`,
  );

  // Healthcheck explícito (solo GET en /health, para no pisar el MCP en "/").
  if (url.pathname === "/health") {
    res.writeHead(200, { "content-type": "application/json" });
    res.end(JSON.stringify({ status: "ok", mcp_endpoint: "/mcp" }));
    return;
  }

  // Endpoint MCP (Streamable HTTP) en "/mcp" y "/".
  if (MCP_PATHS.has(url.pathname)) {
    res.on("finish", () => log("  ->", method, url.pathname, "status", res.statusCode));
    await server.startHTTP({
      url,
      httpPath: url.pathname,
      req,
      res,
      options: { sessionIdGenerator: () => randomUUID() },
    });
    return;
  }

  // Cualquier otra ruta (p.ej. sondeos OAuth /.well-known/...) -> 404 JSON.
  log("  -> 404", url.pathname);
  res.writeHead(404, { "content-type": "application/json" });
  res.end(JSON.stringify({ error: "Not found", try: "/mcp" }));
});

httpServer.listen(PORT, () => {
  log(`escuchando en http://localhost:${PORT}  (MCP en / y /mcp)`);
});
