export default function ChartCard({ title, children, className = '' }) {
  return (
    <div className={`chart-card ${className}`}>
      {title && (
        <p className="mb-4 text-xs uppercase tracking-[0.16em] text-text-tertiary">{title}</p>
      )}
      {children}
    </div>
  )
}
