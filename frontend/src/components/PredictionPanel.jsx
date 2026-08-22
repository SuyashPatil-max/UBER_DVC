import { useState } from 'react'
import { STATUS, useRidePrediction } from '../hooks/useRidePrediction.js'
import RideForm from './RideForm.jsx'
import ResultCard from './ResultCard.jsx'

const DEFAULT_VALUES = {
  payment_method: 'upi',
  vtat: '4.9',
  ctat: '14',
  Booking_value: '237',
  Ride_Distance: '5.73',
  pickup_location: 'Shastri Nagar',
  drop_location: 'Gurgaon Sector 56',
  date: '2024-11-29',
  time: '18:01:39',
  vehicle_type: 'Go Sedan',
}

export default function PredictionPanel() {
  const [values, setValues] = useState(DEFAULT_VALUES)
  const [locationError, setLocationError] = useState('')

  const { status, result, errorMessage, predict } = useRidePrediction()

  const isLoading = status === STATUS.LOADING

  const handleChange = (key, value) => {
    setValues((prev) => ({ ...prev, [key]: value }))
    if (locationError) setLocationError('')
  }

  const handleSubmit = (event) => {
    event.preventDefault()

    if (isLoading) return

    if (values.pickup_location === values.drop_location) {
      setLocationError('Pickup and drop location cannot be the same.')
      return
    }
    setLocationError('')

    const payload = {
      payment_method: values.payment_method,
      vtat: Number(values.vtat),
      ctat: Number(values.ctat),
      Booking_value: Number(values.Booking_value),
      Ride_Distance: Number(values.Ride_Distance),
      pickup_location: values.pickup_location,
      drop_location: values.drop_location,
      date: values.date,
      time: values.time,
      vehicle_type: values.vehicle_type,
    }

    predict(payload)
  }

  return (
    <section id="predictor" className="-mt-10 px-6 pb-16">

      <div className="mx-auto max-w-7xl">

        <div className="grid gap-8 lg:grid-cols-2 items-start">

          {/* LEFT SIDE — form */}

          <RideForm
            values={values}
            onChange={handleChange}
            onSubmit={handleSubmit}
            isLoading={isLoading}
            isDisabled={isLoading}
            errorMessage={status === STATUS.ERROR ? errorMessage : ''}
            locationError={locationError}
          />

          {/* RIGHT SIDE — result */}

          <div>

            {status === STATUS.SUCCESS && result ? (

              <ResultCard result={result} />

            ) : (

              <div className="flex min-h-[420px] items-center justify-center rounded-2xl border border-dashed border-zinc-700 bg-zinc-950/40">

                <div className="text-center">

                  <div className="text-6xl">
                    🚕
                  </div>

                  <h3 className="mt-5 text-2xl font-semibold text-white">
                    Waiting for Prediction
                  </h3>

                  <p className="mt-3 text-zinc-400">
                    Fill in the ride details and click
                    <br />
                    Predict Ride Outcome
                  </p>

                </div>

              </div>

            )}

          </div>

        </div>

      </div>

    </section>
  )
}
