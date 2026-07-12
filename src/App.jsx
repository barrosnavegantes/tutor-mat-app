import { useState, useRef, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import remarkMath from 'remark-math'
import rehypeKatex from 'rehype-katex'
import 'katex/dist/katex.min.css'
import './App.css'

function MathRenderer({ text, isUser }) {
  if (isUser) {
    return <div className="message-text">{text}</div>
  }

  return (
    <div className="message-text">
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[rehypeKatex]}
      >
        {text}
      </ReactMarkdown>
    </div>
  )
}

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [context, setContext] = useState('')
  const messagesEndRef = useRef(null)

  useEffect(() => {
    fetch('/pdf_content.txt')
      .then(r => r.text())
      .then(t => {
        setContext(t)
        setMessages([{
          role: 'assistant',
          content: `## Bem-vindo(a) ao Tutor de Matemática! 👋

Sou seu professor particular de matemática para o **Concurso Público da Câmara Municipal de São Domingos do Capim - Edital 001/2026**.

Vou te ensinar matemática de forma **didática, paciente e prática**, sempre usando exemplos do dia a dia administrativo. 

### Conteúdos que posso te ajudar:
- 📊 Operações básicas (adição, subtração, multiplicação, divisão)
- 💰 Sistema Monetário Nacional
- 📈 Porcentagem, juros simples e compostos
- 🔢 Regra de três e proporcionalidade
- 📐 Raciocínio lógico
- E muito mais!

**Como funciona:** Me pergunte qualquer coisa sobre os tópicos de matemática do edital. Vou explicar passo a passo, com exemplos práticos de escritório. Ao final, sempre darei um exercício para você praticar! 😊`
        }])
      })
      .catch(() => {
        setMessages([{
          role: 'assistant',
          content: 'Bem-vindo ao Tutor de Matemática! Me pergunte qualquer coisa sobre os tópicos do edital.'
        }])
      })
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function handleSend(e) {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMsg = { role: 'user', content: input.trim() }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)

        const systemPrompt = `Você é um professor de matemática especializado em concursos públicos, com foco no edital da Câmara Municipal de São Domingos do Capim.

## SEU PERFIL
- Nome: Prof. Tutor
- Estilo: Paciente, didático, motivador
- Público: Candidatos com ensino fundamental/médio, muitos com dificuldade em matemática

## GLOSSÁRIO DE TERMOS (o aluno vai usar estes nomes)
- "Regra de três" = proporção com multiplicação cruzada (cross-multiplication)
- "Juros simples" = simple interest (J = C × i × t)
- "Juros compostos" = compound interest (M = C × (1 + i)^t)
- "Porcentagem" = percentage
- "Razão e proporção" = ratio and proportion
- "Regra de sociedade" = partnership profit sharing by ratio

## INSTRUÇÕES RÍGIDAS
1. Responda SEMPRE em português claro e simples.
2. Explique cada conceito passo a passo, como se fosse a primeira vez do aluno.
3. Use exemplos do dia a dia administrativo (planilhas, recibos, contas, orçamentos, licitações).
4. Para fórmulas matemáticas, use SEMPRE LaTeX: $$...$$ para fórmulas em destaque e $...$ para fórmulas inline (ex: $$A = \pi r^2$$ ou $x = 5$).
5. Estruture respostas longas com títulos, listas e tabelas markdown.
6. SEMPRE finalize com um exercício prático (sem mostrar a resposta — diga "Tente resolver e me mostre sua resposta!").
7. Se o aluno errar, corrija com gentileza mostrando o passo a passo correto.
8. NUNCA invente informações que não estejam no edital.

## CONTEÚDO DO EDITAL (referência)
${context.slice(0, 8000)}\`\`\``

    const history = messages.concat(userMsg).map(m => ({
      role: m.role,
      content: m.content
    }))

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: 'tutor-matematica:latest',
          messages: [
            { role: 'system', content: systemPrompt },
            ...history.slice(-10)
          ],
          stream: true,
          options: {
            temperature: 0.5,
            top_p: 0.9,
            num_predict: 4096
          }
        })
      })

      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let assistantMsg = ''
      let thinkingMsg = ''

      setMessages(prev => [...prev, { role: 'assistant', content: '' }])

      let buffer = ''
      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop()

        for (const line of lines) {
          const trimmed = line.trim()
          if (!trimmed) continue
          try {
            const parsed = JSON.parse(trimmed)
            const thinking = parsed.message?.thinking || ''
            const content = parsed.message?.content || ''
            if (thinking) thinkingMsg += thinking
            if (content) assistantMsg += content
            const displayed = assistantMsg || thinkingMsg
            if (thinking || content) {
              setMessages(prev => {
                const updated = [...prev]
                updated[updated.length - 1] = { role: 'assistant', content: displayed }
                return updated
              })
            }
          } catch (e) {
            console.warn('JSON parse error (line may be incomplete):', e.message)
          }
        }
      }

      if (buffer.trim()) {
        try {
          const parsed = JSON.parse(buffer.trim())
          const content = parsed.message?.content || ''
          if (content) {
            assistantMsg += content
            setMessages(prev => {
              const updated = [...prev]
              updated[updated.length - 1] = { role: 'assistant', content: assistantMsg }
              return updated
            })
          }
        } catch {}
      }
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `[!] Erro de conexao com o modelo. Verifique se o Ollama esta rodando.`
      }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>📐 Tutor de Matemática</h1>
        <p className="subtitle">Concurso Público CMSDC 2026 • Edital 001/2026</p>
      </header>

      <main className="chat-area">
        <div className="messages">
          {messages.map((msg, i) => (
            <div key={i} className={`message ${msg.role}`}>
              <div className="avatar">
                {msg.role === 'assistant' ? '🎓' : '👤'}
              </div>
              <div className="bubble">
                <MathRenderer text={msg.content} isUser={msg.role === 'user'} />
              </div>
            </div>
          ))}
          {loading && messages[messages.length - 1]?.role === 'user' && (
            <div className="message assistant">
              <div className="avatar">🎓</div>
              <div className="bubble">
                <div className="typing">▊</div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </main>

      <form className="input-area" onSubmit={handleSend}>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Pergunte sobre qualquer tópico de matemática do edital..."
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          {loading ? '⏳' : '➤'}
        </button>
      </form>
    </div>
  )
}

export default App
