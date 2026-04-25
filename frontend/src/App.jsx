import { useCallback, useEffect, useState } from 'react'

function App() {
  const [tasks, setTasks] = useState([])
  const [status, setStatus] = useState('loading')
  const [newTitle, setNewTitle] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [createError, setCreateError] = useState(null)

  const loadTasks = useCallback(async (signal) => {
    try {
      const response = await fetch('/api/tasks/', { signal })
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }
      const data = await response.json()
      setTasks(data)
      setStatus('ready')
    } catch (err) {
      if (err.name !== 'AbortError') setStatus('error')
    }
  }, [])

  useEffect(() => {
    const controller = new AbortController()
    loadTasks(controller.signal)
    return () => controller.abort()
  }, [loadTasks])

  async function handleSubmit(event) {
    event.preventDefault()
    const title = newTitle.trim()
    if (!title || submitting) return

    setSubmitting(true)
    setCreateError(null)

    try {
      const response = await fetch('/api/tasks/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title }),
      })
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }
      setNewTitle('')
      await loadTasks()
    } catch {
      setCreateError('Failed to add task')
    } finally {
      setSubmitting(false)
    }
  }

  const canSubmit = newTitle.trim().length > 0 && !submitting

  return (
    <main>
      <h1>Tasks</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="New task"
          value={newTitle}
          onChange={(event) => setNewTitle(event.target.value)}
          disabled={submitting}
          aria-label="New task title"
        />
        <button type="submit" disabled={!canSubmit}>
          {submitting ? 'Adding…' : 'Add'}
        </button>
      </form>
      {createError && <p role="alert">{createError}</p>}

      {status === 'loading' && <p>Loading…</p>}
      {status === 'error' && <p>Failed to load tasks</p>}
      {status === 'ready' && tasks.length === 0 && <p>No tasks yet</p>}
      {status === 'ready' && tasks.length > 0 && (
        <ul>
          {tasks.map((task) => (
            <li key={task.id}>
              [{task.done ? 'x' : ' '}] {task.title}
            </li>
          ))}
        </ul>
      )}
    </main>
  )
}

export default App
