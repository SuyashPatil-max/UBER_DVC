export default function KpiCard({ label, value, sublabel, accent = '#B4A5F5' }) {
  return (
    <div
      className="chart-card relative overflow-hidden"
      style={{
        background: `radial-gradient(circle at 15% -20%, color-mix(in srgb, ${accent} 20%, transparent), transparent 60%), rgba(255,255,255,.02)`,
      }}
    >
      <span
        aria-hidden="true"
        className="absolute inset-x-0 top-0 h-[2px]"
        style={{ background: `linear-gradient(90deg, transparent, ${accent}, transparent)` }}
      />
      <p className="text-xs uppercase tracking-[0.16em] text-text-tertiary">{label}</p>
      <p
        className="mt-2 bg-clip-text font-display text-3xl font-light text-transparent"
        style={{ backgroundImage: `linear-gradient(135deg, color-mix(in srgb, ${accent} 60%, white 40%), ${accent})` }}
      >
        {value}
      </p>
      {sublabel && <p className="mt-1 text-xs text-text-secondary">{sublabel}</p>}
    </div>
  )
}
