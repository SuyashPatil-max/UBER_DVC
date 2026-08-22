import { useCallback, useState } from 'react'
import { predictRideOutcome, PredictionApiError } from '../services/predictionApi.js'

export const STATUS = {
  IDLE: 'idle',
  LOADING: 'loading',
  SUCCESS: 'success',
  ERROR: 'error',
}

export function useRidePrediction() {
  const [status, setStatus] = useState(STATUS.IDLE)
  const [result, setResult] = useState(null)
  const [errorMessage, setErrorMessage] = useState('')

  const predict = useCallback(async (ridePayload) => {
    setStatus(STATUS.LOADING)
    setErrorMessage('')

    try {
      const outcome = await predictRideOutcome(ridePayload)
      setResult(outcome)
      setStatus(STATUS.SUCCESS)
    } catch (error) {
      const message =
        error instanceof PredictionApiError
          ? error.message
          : 'Unable to get a prediction. Please try again.'
      setErrorMessage(message)
      setResult(null)
      setStatus(STATUS.ERROR)
    }
  }, [])

  const reset = useCallback(() => {
    setStatus(STATUS.IDLE)
    setResult(null)
    setErrorMessage('')
  }, [])

  return { status, result, errorMessage, predict, reset }
}
