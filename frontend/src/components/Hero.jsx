export default function Hero() {
  return (
    <section className="relative overflow-hidden px-6 pt-4 pb-2 sm:pt-6 sm:pb-4">
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-x-0 top-0 flex justify-center opacity-[0.25]"
      >
        <svg
          width="900"
          height="120"
          viewBox="0 0 900 120"
          fill="none"
          className="w-[140%] max-w-none sm:w-[900px]"
        >
          <path
            d="M0 60 C 60 20, 120 100, 180 60 S 300 20, 360 60 S 480 100, 540 60 S 660 20, 720 60 S 840 100, 900 60"
            stroke="url(#waveGradA)"
            strokeWidth="1"
            className="animate-drift"
          />

          <path
            d="M0 70 C 70 110,130 30,200 70 S320 110,390 70 S510 30,580 70 S700 110,770 70 S890 30,900 70"
            stroke="url(#waveGradB)"
            strokeWidth="1"
            className="animate-drift"
            style={{
              animationDelay: "-4s",
              animationDuration: "16s",
            }}
          />

          <defs>
            <linearGradient id="waveGradA" x1="0" y1="0" x2="900" y2="0">
              <stop offset="0%" stopColor="#5FCB9B" stopOpacity="0" />
              <stop offset="50%" stopColor="#B4A5F5" stopOpacity="0.6" />
              <stop offset="100%" stopColor="#5FCB9B" stopOpacity="0" />
            </linearGradient>

            <linearGradient id="waveGradB" x1="0" y1="0" x2="900" y2="0">
              <stop offset="0%" stopColor="#E38A93" stopOpacity="0" />
              <stop offset="50%" stopColor="#8FB1E8" stopOpacity="0.5" />
              <stop offset="100%" stopColor="#E38A93" stopOpacity="0" />
            </linearGradient>
          </defs>
        </svg>
      </div>

      <div className="relative mx-auto flex max-w-5xl flex-col items-center text-center">

        <span
          className="animate-fadeUp mb-4 inline-flex items-center rounded-full border border-ink-borderStrong bg-ink-900 px-5 py-2 text-xs tracking-[0.22em] uppercase text-text-secondary"
        >
          AI-Powered Ride Prediction
        </span>

        <h1
          className="animate-fadeUp font-display text-4xl font-light leading-[1.02] tracking-tight text-text-primary sm:text-5xl lg:text-6xl"
        >
          Will this{" "}
          <span className="bg-gradient-to-r from-accent-violet via-text-primary to-accent-blue bg-clip-text text-transparent">
            ride
          </span>

          <br />
          complete, or fall through?
        </h1>

        <p
          className="mt-5 max-w-3xl text-base leading-7 text-text-secondary sm:text-lg"
        >
          Enter the trip details below and a machine learning model will
          predict whether the booking completes, along with its confidence.
        </p>

      </div>
    </section>
  );
}
