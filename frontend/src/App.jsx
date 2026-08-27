import { useState } from 'react'
import Sidebar from './components/Sidebar.jsx'
import Navbar from './components/Navbar.jsx'
import Hero from './components/Hero.jsx'
import PredictionPanel from './components/PredictionPanel.jsx'
import DashboardView from './components/dashboard/DashboardView.jsx'
import Footer from './components/Footer.jsx'

export default function App() {
  const [view, setView] = useState('predictor')

  return (
    <div className="min-h-screen bg-ink-950 font-body">
      <Sidebar activeView={view} onNavigate={setView} />

      <div className="pl-20">
        <Navbar onNavigateHome={() => setView('predictor')} />

        <main>
          {view === 'predictor' ? (
            <>
              <Hero />
              <PredictionPanel />
            </>
          ) : (
            <DashboardView />
          )}
        </main>

        {view === 'predictor' && <Footer />}
      </div>
    </div>
  )
}
