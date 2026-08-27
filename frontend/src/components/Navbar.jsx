export default function Navbar({ onNavigateHome }) {
  const handleAnchorClick = (event) => {
    // These anchors only exist on the predictor view — make sure we're
    // there first so the scroll actually has a target to land on.
    if (onNavigateHome) onNavigateHome()
  }

  return (
    <header className="sticky top-0 z-30 border-b border-ink-border bg-ink-950/80 backdrop-blur-md">
      <nav
        className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6"
        aria-label="Primary"
      >
        <span className="font-display text-[1.05rem] tracking-tight text-text-primary">
          Ride Completion AI
        </span>

        <ul className="flex items-center gap-8 text-sm text-text-secondary">
          <li>
            <a
              href="#predictor"
              onClick={handleAnchorClick}
              className="transition-colors duration-200 hover:text-text-primary"
            >
              Predictor
            </a>
          </li>
          <li>
            <a
              href="#about"
              onClick={handleAnchorClick}
              className="transition-colors duration-200 hover:text-text-primary"
            >
              About
            </a>
          </li>
        </ul>
      </nav>
    </header>
  )
}
