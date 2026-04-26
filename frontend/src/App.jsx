import { useCallback, useEffect, useState } from 'react'

function App() {
  const [tasks, setTasks] = useState([])
  const [status, setStatus] = useState('loading')
  const [newTitle, setNewTitle] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [createError, setCreateError] = useState(null)
  const [togglingIds, setTogglingIds] = useState(() => new Set())
  const [toggleErrors, setToggleErrors] = useState(() => new Map())

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
        const data = await response.json().catch(() => null)
        const fieldErrors =
          data && typeof data === 'object' ? Object.values(data).flat() : []
        const message = fieldErrors.find((m) => typeof m === 'string')
        setCreateError(message || 'Failed to add task')
        return
      }
      setNewTitle('')
      await loadTasks()
    } catch {
      setCreateError('Failed to add task')
    } finally {
      setSubmitting(false)
    }
  }

  function toggleDone(task) {
    setTogglingIds((prev) => {
      const next = new Set(prev)
      next.add(task.id)
      return next
    })
    setToggleErrors((prev) => {
      if (!prev.has(task.id)) return prev
      const next = new Map(prev)
      next.delete(task.id)
      return next
    })

    fetch(`/api/tasks/${task.id}/`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ done: !task.done }),
    })
      .then((response) => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        return response.json()
      })
      .then((updated) => {
        setTasks((prev) =>
          prev.map((t) => (t.id === updated.id ? updated : t))
        )
      })
      .catch(() => {
        setToggleErrors((prev) =>
          new Map(prev).set(task.id, 'Failed to update')
        )
      })
      .finally(() => {
        setTogglingIds((prev) => {
          const next = new Set(prev)
          next.delete(task.id)
          return next
        })
      })
  }

  const canSubmit = newTitle.trim().length > 0 && !submitting

  return (
    <main>
      <h1>Tasks</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="New task"
          maxLength={201}
          value={newTitle}
          onChange={(event) => setNewTitle(event.target.value)}
          disabled={submitting}
          aria-label="New task title"
        />
        <button type="submit" disabled={!canSubmit}>
          {submitting ? 'Adding…' : 'Add'}
        </button>
      </form>
      {newTitle.length > 200 && <p role="status">Max 200 characters</p>}
      {createError && <p role="alert">{createError}</p>}

      {status === 'loading' && <p>Loading…</p>}
      {status === 'error' && <p>Failed to load tasks</p>}
      {status === 'ready' && tasks.length === 0 && <p>No tasks yet</p>}
      {status === 'ready' && tasks.length > 0 && (
        <ul>
          {tasks.map((task) => {
            const isToggling = togglingIds.has(task.id)
            const toggleError = toggleErrors.get(task.id)
            return (
              <li key={task.id}>
                <label>
                  <input
                    type="checkbox"
                    checked={task.done}
                    onChange={() => toggleDone(task)}
                    disabled={isToggling}
                  />
                  {' '}
                  {task.title}
                </label>
                {isToggling && <span> Saving…</span>}
                {toggleError && <span role="alert"> {toggleError}</span>}
              </li>
            )
          })}
        </ul>
      )}
    </main>
  )
}

export default App
