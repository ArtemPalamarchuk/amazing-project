import { useEffect, useState } from 'react'

type Task = {
  id: number
  title: string
  status: string
}

type Project = {
  id: number
  name: string
  tasks: Task[]
}

export default function App() {
  const [projects, setProjects] = useState<Project[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch('/api/projects/')
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        return res.json()
      })
      .then((data) => setProjects(data.results))
      .catch((e) => setError(e.message))
  }, [])

  if (error) return <p>Error: {error}</p>

  return (
    <main>
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
