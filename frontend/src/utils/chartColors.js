// Shared categorical palette for the analytics dashboard charts, drawn
// from the same accent/positive/negative tokens used across the app.
export const CHART_PALETTE = [
  '#B4A5F5', // accent-violet
  '#8FB1E8', // accent-blue
  '#5FCB9B', // positive
  '#E38A93', // negative
  '#F5C26B',
  '#7DD3FC',
  '#D98FE8',
]

export function colorAt(index) {
  return CHART_PALETTE[index % CHART_PALETTE.length]
}

function hexToRgb(hex) {
  const clean = hex.replace('#', '')
  const value = parseInt(clean, 16)
  return [(value >> 16) & 255, (value >> 8) & 255, value & 255]
}

function rgbToHex([r, g, b]) {
  return `#${[r, g, b]
    .map((c) => Math.round(Math.min(255, Math.max(0, c))).toString(16).padStart(2, '0'))
    .join('')}`
}

// Linear-interpolates between two hex colors. t=0 -> a, t=1 -> b.
export function mixColor(hexA, hexB, t) {
  const a = hexToRgb(hexA)
  const b = hexToRgb(hexB)
  return rgbToHex(a.map((channel, i) => channel + (b[i] - channel) * t))
}

export function lighten(hex, amount = 0.35) {
  return mixColor(hex, '#ffffff', amount)
}

export function darken(hex, amount = 0.35) {
  return mixColor(hex, '#000000', amount)
}

// Stable ids so gradients defined once via <ChartGradientDefs /> can be
// referenced from any chart via `fill="url(#barGrad0)"` etc.
export const gradientIds = {
  bar: (i) => `barGrad${i % CHART_PALETTE.length}`,
  barHorizontal: (i) => `barGradH${i % CHART_PALETTE.length}`,
  pie: (i) => `pieGrad${i % CHART_PALETTE.length}`,
  area: (i) => `areaGrad${i % CHART_PALETTE.length}`,
}
