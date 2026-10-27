import { cleanup, render, screen } from '@testing-library/react'
import { afterEach, expect, test, vi } from 'vitest'
import App from './App'

afterEach(() => {
  cleanup()
  vi.restoreAllMocks()
})

function jsonResponse(data: unknown) {
  return new Response(JSON.stringify(data), { status: 200 })
}

test('shows projects of the logged-in user', async () => {
  vi.spyOn(globalThis, 'fetch').mockImplementation(async (input) => {
    const url = String(input)
    if (url === '/api/auth/me/') return jsonResponse({ username: 'alice' })
    if (url === '/api/projects/') {
      // The API is paginated: projects come inside `results`.
      return jsonResponse({
        results: [
          {
            id: 1,
            name: 'Alpha',
            tasks: [{ id: 10, title: 'Write tests', status: 'todo' }],
          },
        ],
      })
    }
    return new Response(null, { status: 404 })
  })

  render(<App />)

  expect(await screen.findByRole('heading', { name: 'Alpha' })).toBeTruthy()
  expect(screen.getByText(/alice/)).toBeTruthy()
  expect(screen.getByText('Write tests — todo')).toBeTruthy()
})
