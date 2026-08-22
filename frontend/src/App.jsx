import Navbar from './components/Navbar.jsx'
import Hero from './components/Hero.jsx'
import PredictionPanel from './components/PredictionPanel.jsx'
import Footer from './components/Footer.jsx'

export default function App() {
  return (
    <div className="min-h-screen bg-ink-950 font-body">
      <Navbar />
      <main>
        <Hero />
        <PredictionPanel />
      </main>
      <Footer />
    </div>
  )
}
