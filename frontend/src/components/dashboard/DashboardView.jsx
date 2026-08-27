import { useState } from 'react'
import OverviewPage from './pages/OverviewPage.jsx'
import VehicleTypePage from './pages/VehicleTypePage.jsx'
import RevenuePage from './pages/RevenuePage.jsx'
import CancellationPage from './pages/CancellationPage.jsx'
import RatingsPage from './pages/RatingsPage.jsx'

const PAGES = [
  { id: 'overview', label: 'Overall', component: OverviewPage },
  { id: 'vehicleType', label: 'Vehicle Type', component: VehicleTypePage },
  { id: 'revenue', label: 'Revenue', component: RevenuePage },
  { id: 'cancellation', label: 'Cancellation', component: CancellationPage },
  { id: 'ratings', label: 'Ratings', component: RatingsPage },
]

export default function DashboardView() {
  const [activePageId, setActivePageId] = useState(PAGES[0].id)
  const activePage = PAGES.find((p) => p.id === activePageId) ?? PAGES[0]
  const ActiveComponent = activePage.component

  return (
    <div className="flex min-h-[calc(100vh-4rem)] flex-col">
      <div className="flex-1 px-6 pb-8 pt-8">
        <div className="mx-auto max-w-6xl">
          <div className="mb-6">
            <span className="text-xs uppercase tracking-[0.22em] text-text-tertiary">Analytics Dashboard</span>
            <h1 className="mt-2 font-display text-2xl font-light text-text-primary sm:text-3xl">
              {activePage.label}
            </h1>
          </div>
          <ActiveComponent />
        </div>
      </div>

      <nav
        aria-label="Dashboard pages"
        className="sticky bottom-0 border-t border-ink-border bg-ink-950/90 px-6 py-3 backdrop-blur-md"
      >
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-center gap-2 sm:justify-start">
          {PAGES.map((page) => {
            const isActive = page.id === activePageId
            return (
              <button
                key={page.id}
                type="button"
                onClick={() => setActivePageId(page.id)}
                className={`rounded-full px-4 py-2 text-sm transition-colors duration-200 ${
                  isActive
                    ? 'bg-ink-700 text-text-primary'
                    : 'text-text-secondary hover:bg-ink-800 hover:text-text-primary'
                }`}
                aria-current={isActive ? 'page' : undefined}
              >
                {page.label}
              </button>
            )
          })}
        </div>
      </nav>
    </div>
  )
}
