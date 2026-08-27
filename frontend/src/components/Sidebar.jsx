const NAV_ITEMS = [
  {
    id: 'predictor',
    label: 'Predict',
    icon: (
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={1.6}
        d="M13 2 3 14h7l-1 8 10-12h-7l1-8z"
      />
    ),
  },
  {
    id: 'dashboard',
    label: 'Dashboard',
    icon: (
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={1.6}
        d="M4 19V10m6 9V5m6 14v-7m6 7V9"
      />
    ),
  },
]

export default function Sidebar({ activeView, onNavigate }) {
  return (
    <aside className="fixed inset-y-0 left-0 z-40 flex w-20 flex-col items-center border-r border-ink-border bg-ink-950/95 py-6 backdrop-blur-md">
      <span
        aria-hidden="true"
        className="mb-8 flex h-9 w-9 items-center justify-center rounded-full bg-gradient-to-br from-accent-violet to-accent-blue text-xs font-semibold text-ink-950"
      >
        RC
      </span>

      <nav aria-label="Sections" className="flex flex-col items-center gap-2">
        {NAV_ITEMS.map((item) => {
          const isActive = activeView === item.id
          return (
            <button
              key={item.id}
              type="button"
              onClick={() => onNavigate(item.id)}
              aria-current={isActive ? 'page' : undefined}
              className={`group flex w-16 flex-col items-center gap-1 rounded-2xl py-3 transition-colors duration-200 ${
                isActive ? 'bg-ink-800 text-text-primary' : 'text-text-secondary hover:bg-ink-900 hover:text-text-primary'
              }`}
            >
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                className="h-5 w-5"
                style={{ color: isActive ? '#B4A5F5' : 'currentColor' }}
              >
                {item.icon}
              </svg>
              <span className="text-[0.65rem] tracking-wide">{item.label}</span>
            </button>
          )
        })}
      </nav>
    </aside>
  )
}
