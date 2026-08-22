// Central place that maps the model's predicted class to a display
// emoji and color. The backend's binary label is "Completed" /
// "Incomplete", but this stays label-driven (case-insensitive match)
// rather than hardcoding a boolean, so it keeps working if the backend
// ever adds a third class (e.g. "Cancelled").

const KNOWN_RESULTS = {
  completed: { emoji: '✅', color: '#5FCB9B' },
  complete: { emoji: '✅', color: '#5FCB9B' },
  success: { emoji: '✅', color: '#5FCB9B' },

  incomplete: { emoji: '⚠️', color: '#E38A93' },
  cancelled: { emoji: '⚠️', color: '#E38A93' },
  canceled: { emoji: '⚠️', color: '#E38A93' },
  failed: { emoji: '⚠️', color: '#E38A93' },
}

const FALLBACK_PALETTE = ['#B4A5F5', '#8FB1E8', '#F5C26B', '#7DD3FC']

function hashString(value) {
  let hash = 0
  for (let i = 0; i < value.length; i += 1) {
    hash = (hash * 31 + value.charCodeAt(i)) >>> 0
  }
  return hash
}

/**
 * Returns { emoji, color, label } for any predicted class label string.
 */
export function getResultMeta(rawLabel) {
  const original = typeof rawLabel === 'string' ? rawLabel.trim() : ''
  const key = original.toLowerCase()
  const known = KNOWN_RESULTS[key]

  const label = original || 'Unknown'

  if (known) {
    return { ...known, label }
  }

  const fallbackColor = FALLBACK_PALETTE[hashString(key) % FALLBACK_PALETTE.length]
  return { emoji: '🔮', color: fallbackColor, label }
}
