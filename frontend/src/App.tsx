import { useEffect, useState } from 'react'
import { apiFetch } from './api'

type Task = { id: number; title: string; status: string }
type Project = { id: number; name: string; tasks: Task[] }

export default function App() {
  const [user, setUser] = useState<string | null>(null)
  const [projects, setProjects] = useState<Project[]>([])
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    apiFetch('/api/auth/me/')
      .then((data) => setUser(data.username))
      .catch(() => setUser(null))
  }, [])

  useEffect(() => {
    if (!user) return
    apiFetch('/api/projects/')
      .then((data) => setProjects(data.results))
      .catch((e) => setError(e.message))
  }, [user])

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    try {
      const data = await apiFetch('/api/auth/login/', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
      })
      setUser(data.username)
    } catch {
      setError('Invalid credentials')
    }
  }

  async function handleLogout() {
    await apiFetch('/api/auth/logout/', { method: 'POST' })
    setUser(null)
    setProjects([])
  }

  if (!user) {
    return (
      <form onSubmit={handleLogin}>
        <h1>Log in</h1>
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
        />
        <button type="submit">Log in</button>
        {error && <p>{error}</p>}
      </form>
    )
  }

  return (
    <main>
      <p>
        {user} <button onClick={handleLogout}>Log out</button>
      </p>
      <h1>Projects</h1>
      {projects.map((project) => (
        <section key={project.id}>
          <h2>{project.name}</h2>
          <ul>
            {project.tasks.map((task) => (
              <li key={task.id}>
                {task.title} — {task.status}
              </li>
            ))}
          </ul>
        </section>
      ))}
    </main>
  )
}