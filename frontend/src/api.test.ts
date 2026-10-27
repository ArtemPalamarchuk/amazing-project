import { afterEach, expect, test, vi } from 'vitest'
import { apiFetch } from './api'

afterEach(() => {
  vi.restoreAllMocks()
  document.cookie = 'csrftoken=; expires=Thu, 01 Jan 1970 00:00:00 GMT'
})

test('sends the CSRF token from the cookie', async () => {
  document.cookie = 'csrftoken=abc123'
  const fetchMock = vi
    .spyOn(globalThis, 'fetch')
    .mockResolvedValue(new Response(JSON.stringify({}), { status: 200 }))

  await apiFetch('/api/projects/', { method: 'POST' })

  const [, init] = fetchMock.mock.calls[0]
  expect(new Headers(init?.headers).get('X-CSRFToken')).toBe('abc123')
})

test('throws on a non-ok response', async () => {
  vi.spyOn(globalThis, 'fetch').mockResolvedValue(
    new Response(null, { status: 403 }),
  )

  await expect(apiFetch('/api/projects/')).rejects.toThrow('HTTP 403')
})
