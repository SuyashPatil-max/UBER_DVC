// Centralized service for talking to the ride-completion prediction
// backend. Keeping this isolated means the base URL, request shape, or
// response contract can change without touching any UI code.

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

/**
 * Normalizes whatever the backend calls the predicted label into a
 * trimmed string ("Completed" | "Incomplete", but not hardcoded to
 * just those two).
 */
function normalizePrediction(raw) {
  if (typeof raw !== 'string') return null
  const value = raw.trim()
  return value.length > 0 ? value : null
}

/**
 * Pulls a 0-1 probability value out of the response. Guards against a
 * backend that returns 0-100 instead of 0-1.
 */
function extractProbability(payload) {
  const candidate = payload?.probability ?? payload?.confidence ?? payload?.score
  if (typeof candidate !== 'number' || Number.isNaN(candidate)) return null
  const normalized = candidate > 1 ? candidate / 100 : candidate
  return Math.min(Math.max(normalized, 0), 1)
}

/**
 * Sends the ride payload to the backend and returns a normalized
 * result: { prediction: string, probability: number | null }
 *
 * Throws a PredictionApiError with a user-safe message on any failure —
 * network issues, non-2xx responses, or a response shape we can't parse.
 */
export async function predictRideOutcome(ridePayload) {
  let response
  try {
    response = await fetch(`${API_BASE_URL}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(ridePayload),
    })
  } catch (networkError) {
    throw new PredictionApiError('Unable to reach the prediction service. Please try again.')
  }

  if (!response.ok) {
    let detail = null
    try {
      const errorBody = await response.json()
      detail = errorBody?.detail
    } catch (_) {
      // ignore parse failure, fall through to generic message
    }
    const message =
      typeof detail === 'string'
        ? detail
        : 'The prediction service rejected this request. Please check the ride details.'
    throw new PredictionApiError(message)
  }

  let payload
  try {
    payload = await response.json()
  } catch (parseError) {
    throw new PredictionApiError('Unable to parse the prediction response.')
  }

  const prediction = normalizePrediction(payload?.prediction ?? payload?.label)
  if (!prediction) {
    throw new PredictionApiError('The prediction service returned an unexpected response.')
  }

  return {
    prediction,
    probability: extractProbability(payload),
  }
}

export class PredictionApiError extends Error {
  constructor(message) {
    super(message)
    this.name = 'PredictionApiError'
  }
}
