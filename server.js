import express from 'express'
import http from 'http'
import https from 'https'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'

const __dirname = dirname(fileURLToPath(import.meta.url))
const app = express()
const PORT = 5173

// Keep model loaded in memory (ping every 4 min)
const OLLAMA_MODEL = 'tutor-matematica:latest'
function keepModelAlive() {
  const data = JSON.stringify({
    model: OLLAMA_MODEL,
    messages: [{ role: 'user', content: '' }],
    stream: false,
    options: { num_predict: 1 }
  })
  const req = http.request({
    hostname: 'localhost', port: 11434,
    path: '/api/chat', method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(data) }
  }, () => {})
  req.on('error', () => {})
  req.write(data)
  req.end()
}
keepModelAlive()
setInterval(keepModelAlive, 4 * 60 * 1000)

// Static files
app.use(express.static(join(__dirname, 'dist')))

// Proxy /api/chat → Ollama
app.use('/api/chat', (req, res) => {
  let body = ''
  req.on('data', chunk => body += chunk)
  req.on('end', () => {
    const options = {
      hostname: 'localhost',
      port: 11434,
      path: '/api/chat',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:11434',
        'Content-Length': Buffer.byteLength(body)
      },
      timeout: 60000
    }

    const proxyReq = http.request(options, (proxyRes) => {
      // Remove problematic keep-alive header from upstream
      const headers = { ...proxyRes.headers }
      delete headers['keep-alive']
      res.writeHead(proxyRes.statusCode, headers)
      proxyRes.pipe(res)
    })

    proxyReq.on('error', (err) => {
      console.error('Proxy error:', err.message)
      if (!res.headersSent) {
        res.status(502).json({ error: 'Ollama not reachable' })
      }
    })

    proxyReq.on('timeout', () => {
      proxyReq.destroy()
      if (!res.headersSent) {
        res.status(504).json({ error: 'Ollama timeout' })
      }
    })

    proxyReq.write(body)
    proxyReq.end()
  })
})

// SPA fallback
app.get('/{*path}', (req, res) => {
  res.sendFile(join(__dirname, 'dist', 'index.html'))
})

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on http://0.0.0.0:${PORT}`)
})
