import { CHART_PALETTE, lighten, darken } from '../../utils/chartColors.js'

// Centralized <defs> block: every dashboard chart references these by id
// (barGrad0, pieGrad0, areaGrad0, ...) instead of flat fill colors, so
// bars/pies/areas render with a soft gradient instead of a solid color.
export default function ChartGradientDefs() {
  return (
    <defs>
      {CHART_PALETTE.map((color, i) => (
        <linearGradient key={`bar-${i}`} id={`barGrad${i}`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={lighten(color, 0.3)} />
          <stop offset="100%" stopColor={darken(color, 0.18)} />
        </linearGradient>
      ))}

      {CHART_PALETTE.map((color, i) => (
        <linearGradient key={`barh-${i}`} id={`barGradH${i}`} x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stopColor={darken(color, 0.12)} />
          <stop offset="100%" stopColor={lighten(color, 0.32)} />
        </linearGradient>
      ))}

      {CHART_PALETTE.map((color, i) => (
        <radialGradient key={`pie-${i}`} id={`pieGrad${i}`} cx="35%" cy="30%" r="75%">
          <stop offset="0%" stopColor={lighten(color, 0.5)} />
          <stop offset="100%" stopColor={darken(color, 0.08)} />
        </radialGradient>
      ))}

      {CHART_PALETTE.map((color, i) => (
        <linearGradient key={`area-${i}`} id={`areaGrad${i}`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={color} stopOpacity={0.55} />
          <stop offset="60%" stopColor={color} stopOpacity={0.12} />
          <stop offset="100%" stopColor={color} stopOpacity={0} />
        </linearGradient>
      ))}
    </defs>
  )
}
