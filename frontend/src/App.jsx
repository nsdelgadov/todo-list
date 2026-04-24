import { useEffect, useState } from 'react'

function App() {
  const [tasks, setTasks] = useState([])
  const [status, setStatus] = useState('loading')

  useEffect(() => {
    const controller = new AbortController()

    fetch('/api/tasks/', { signal: controller.signal })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`)
        }
        return response.json()
      })
      .then((data) => {
        setTasks(data)
        setStatus('ready')
      })
      .catch((err) => {
        if (err.name !== 'AbortError') setStatus('error')
      })

    return () => controller.abort()
  }, [])

  return (
    <main>
      <h1>Tasks</h1>
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
