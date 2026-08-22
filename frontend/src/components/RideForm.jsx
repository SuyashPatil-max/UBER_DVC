import { LOCATIONS } from '../data/locations.js'
import { VEHICLES } from '../data/vehicles.js'
import { PAYMENT_METHODS } from '../data/paymentMethods.js'

const inputClasses =
  'w-full rounded-xl border border-ink-border bg-ink-950 px-4 py-2.5 text-[0.92rem] text-text-primary outline-none transition-colors duration-200 focus:border-accent-violet/50 appearance-none'

const labelClasses =
  'mb-1.5 block text-xs font-medium uppercase tracking-wider text-text-secondary'

function Field({ label, children }) {
  return (
    <div>
      <label className={labelClasses}>{label}</label>
      {children}
    </div>
  )
}

export default function RideForm({ values, onChange, onSubmit, isLoading, isDisabled, errorMessage, locationError }) {
  const set = (key) => (event) => onChange(key, event.target.value)

  return (
    <form
      onSubmit={onSubmit}
      className="rounded-2xl border border-ink-border bg-gradient-to-b from-ink-900 to-ink-850 p-6 shadow-[0_30px_80px_-40px_rgba(0,0,0,0.9)]"
    >
      <h2 className="font-display text-2xl font-normal text-text-primary">
        Ride Details
      </h2>

      <p className="mt-2 text-sm text-text-secondary">
        Fill in the trip details to predict whether it will complete.
      </p>

      <div className="mt-5 grid grid-cols-1 gap-4 sm:grid-cols-2">

        <Field label="Pickup Location">
          <select
            className={inputClasses}
            value={values.pickup_location}
            onChange={set('pickup_location')}
          >
            {LOCATIONS.map((loc) => (
              <option key={loc} value={loc}>{loc}</option>
            ))}
          </select>
        </Field>

        <Field label="Drop Location">
          <select
            className={inputClasses}
            value={values.drop_location}
            onChange={set('drop_location')}
          >
            {LOCATIONS.map((loc) => (
              <option key={loc} value={loc}>{loc}</option>
            ))}
          </select>
        </Field>

        <Field label="Vehicle Type">
          <select
            className={inputClasses}
            value={values.vehicle_type}
            onChange={set('vehicle_type')}
          >
            {VEHICLES.map((v) => (
              <option key={v} value={v}>{v}</option>
            ))}
          </select>
        </Field>

        <Field label="Payment Method">
          <select
            className={inputClasses}
            value={values.payment_method}
            onChange={set('payment_method')}
          >
            {PAYMENT_METHODS.map((p) => (
              <option key={p.value} value={p.value}>{p.label}</option>
            ))}
          </select>
        </Field>

        <Field label="Date">
          <input
            type="date"
            className={inputClasses}
            value={values.date}
            onChange={set('date')}
          />
        </Field>

        <Field label="Time">
          <input
            type="time"
            step="1"
            className={inputClasses}
            value={values.time}
            onChange={set('time')}
          />
        </Field>

        <Field label="Booking Value (₹)">
          <input
            type="number"
            min="0"
            step="0.01"
            className={inputClasses}
            value={values.Booking_value}
            onChange={set('Booking_value')}
          />
        </Field>

        <Field label="Ride Distance (km)">
          <input
            type="number"
            min="0"
            step="0.01"
            className={inputClasses}
            value={values.Ride_Distance}
            onChange={set('Ride_Distance')}
          />
        </Field>

        <Field label="VTAT (min)">
          <input
            type="number"
            min="0"
            step="0.1"
            className={inputClasses}
            value={values.vtat}
            onChange={set('vtat')}
          />
        </Field>

        <Field label="CTAT (min)">
          <input
            type="number"
            min="0"
            step="0.1"
            className={inputClasses}
            value={values.ctat}
            onChange={set('ctat')}
          />
        </Field>

      </div>

      {locationError && (
        <p className="mt-4 text-center text-sm text-negative-text">
          {locationError}
        </p>
      )}

      <button
        type="submit"
        disabled={isDisabled}
        className="mt-6 flex w-full items-center justify-center rounded-xl bg-text-primary px-6 py-3 text-sm font-medium text-ink-950 transition-all duration-200 enabled:hover:scale-[1.01] enabled:hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-40"
      >
        {isLoading ? (
          <>
            <span className="mr-2 h-3.5 w-3.5 animate-spin rounded-full border-2 border-ink-950/20 border-t-ink-950" />
            Predicting...
          </>
        ) : (
          'Predict Ride Outcome'
        )}
      </button>

      {errorMessage && (
        <p className="mt-4 text-center text-sm text-negative-text">
          {errorMessage}
        </p>
      )}
    </form>
  )
}
