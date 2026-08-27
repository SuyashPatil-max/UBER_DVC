// One-off build script: aggregates data/external/ncr_ride_bookings.csv (the
// same source the Uber.pbix Power BI report reads) into a static JSON file
// consumed by the in-app dashboard. Re-run with `node scripts/buildDashboardData.mjs`
// whenever the source CSV changes — the frontend never parses the raw CSV itself.

import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const CSV_PATH = path.resolve(__dirname, '../../data/external/ncr_ride_bookings.csv')
const OUT_PATH = path.resolve(__dirname, '../src/data/dashboardData.json')

const raw = fs.readFileSync(CSV_PATH, 'utf8')
const lines = raw.split(/\r?\n/).filter(Boolean)
const header = lines[0].split(',').map((h) => h.trim())
const idx = Object.fromEntries(header.map((h, i) => [h, i]))

const num = (v) => {
  const n = Number(v)
  return v && v !== 'null' && !Number.isNaN(n) ? n : null
}
const str = (v) => (v && v !== 'null' ? v.replace(/^"+|"+$/g, '') : null)

const rows = []
for (let i = 1; i < lines.length; i++) {
  const parts = lines[i].split(',')
  rows.push({
    date: parts[idx['Date']],
    status: str(parts[idx['Booking Status']]),
    vehicleType: str(parts[idx['Vehicle Type']]),
    bookingValue: num(parts[idx['Booking Value']]),
    rideDistance: num(parts[idx['Ride Distance']]),
    driverRating: num(parts[idx['Driver Ratings']]),
    customerRating: num(parts[idx['Customer Rating']]),
    paymentMethod: str(parts[idx['Payment Method']]),
    customerId: str(parts[idx['Customer ID']]),
    custCancelReason: str(parts[idx['Reason for cancelling by Customer']]),
    driverCancelReason: str(parts[idx['Driver Cancellation Reason']]),
    incompleteReason: str(parts[idx['Incomplete Rides Reason']]),
  })
}

const totalBookings = rows.length

// ---- Overview page ----
const statusCounts = {}
const monthCounts = {}
for (const r of rows) {
  statusCounts[r.status] = (statusCounts[r.status] || 0) + 1
  const month = r.date.slice(0, 7) // YYYY-MM
  monthCounts[month] = (monthCounts[month] || 0) + 1
}
const statusBreakdown = Object.entries(statusCounts).map(([status, count]) => ({ status, count }))
const bookingsOverTime = Object.entries(monthCounts)
  .sort(([a], [b]) => a.localeCompare(b))
  .map(([month, count]) => ({ month, count }))

const completedRows = rows.filter((r) => r.status === 'Completed')
const totalRevenue = completedRows.reduce((s, r) => s + (r.bookingValue || 0), 0)
const totalDistance = completedRows.reduce((s, r) => s + (r.rideDistance || 0), 0)
const overview = {
  totalBookings,
  completedBookings: completedRows.length,
  completionRate: +((completedRows.length / totalBookings) * 100).toFixed(1),
  totalRevenue: Math.round(totalRevenue),
  avgRideDistance: +(totalDistance / completedRows.length).toFixed(2),
  statusBreakdown,
  bookingsOverTime,
}

// ---- Vehicle type page ----
const vehicleAgg = {}
for (const r of completedRows) {
  if (!r.vehicleType) continue
  const a = (vehicleAgg[r.vehicleType] ??= { vehicleType: r.vehicleType, bookings: 0, totalValue: 0, totalDistance: 0 })
  a.bookings += 1
  a.totalValue += r.bookingValue || 0
  a.totalDistance += r.rideDistance || 0
}
const vehicleType = Object.values(vehicleAgg)
  .map((v) => ({
    ...v,
    totalValue: Math.round(v.totalValue),
    totalDistance: Math.round(v.totalDistance),
    avgDistance: +(v.totalDistance / v.bookings).toFixed(2),
  }))
  .sort((a, b) => b.totalValue - a.totalValue)

// ---- Revenue page ----
const paymentAgg = {}
for (const r of completedRows) {
  if (!r.paymentMethod) continue
  paymentAgg[r.paymentMethod] = (paymentAgg[r.paymentMethod] || 0) + (r.bookingValue || 0)
}
const revenueByPaymentMethod = Object.entries(paymentAgg)
  .map(([method, value]) => ({ method, value: Math.round(value) }))
  .sort((a, b) => b.value - a.value)

const revenueMonthAgg = {}
for (const r of completedRows) {
  const month = r.date.slice(0, 7)
  revenueMonthAgg[month] = (revenueMonthAgg[month] || 0) + (r.bookingValue || 0)
}
const revenueOverTime = Object.entries(revenueMonthAgg)
  .sort(([a], [b]) => a.localeCompare(b))
  .map(([month, value]) => ({ month, value: Math.round(value) }))

const customerAgg = {}
for (const r of completedRows) {
  if (!r.customerId) continue
  customerAgg[r.customerId] = (customerAgg[r.customerId] || 0) + (r.bookingValue || 0)
}
const topCustomers = Object.entries(customerAgg)
  .map(([customerId, value]) => ({ customerId, value: Math.round(value) }))
  .sort((a, b) => b.value - a.value)
  .slice(0, 10)

const revenue = { revenueByPaymentMethod, revenueOverTime, topCustomers }

// ---- Cancellation page ----
const custCancelRows = rows.filter((r) => r.status === 'Cancelled by Customer')
const driverCancelRows = rows.filter((r) => r.status === 'Cancelled by Driver')
const incompleteRows = rows.filter((r) => r.status === 'Incomplete')

const tally = (arr, key) => {
  const agg = {}
  for (const r of arr) {
    const k = r[key] || 'Unspecified'
    agg[k] = (agg[k] || 0) + 1
  }
  return Object.entries(agg)
    .map(([reason, count]) => ({ reason, count }))
    .sort((a, b) => b.count - a.count)
}

const cancellation = {
  totalCancelledByCustomer: custCancelRows.length,
  totalCancelledByDriver: driverCancelRows.length,
  totalIncomplete: incompleteRows.length,
  cancelledPercentage: +(((custCancelRows.length + driverCancelRows.length) / totalBookings) * 100).toFixed(1),
  customerCancelReasons: tally(custCancelRows, 'custCancelReason'),
  driverCancelReasons: tally(driverCancelRows, 'driverCancelReason'),
}

// ---- Ratings page ----
const ratingAgg = {}
for (const r of completedRows) {
  if (!r.vehicleType) continue
  const a = (ratingAgg[r.vehicleType] ??= {
    vehicleType: r.vehicleType,
    custSum: 0,
    custCount: 0,
    drvSum: 0,
    drvCount: 0,
  })
  if (r.customerRating != null) {
    a.custSum += r.customerRating
    a.custCount += 1
  }
  if (r.driverRating != null) {
    a.drvSum += r.driverRating
    a.drvCount += 1
  }
}
const ratings = Object.values(ratingAgg)
  .map((a) => ({
    vehicleType: a.vehicleType,
    avgCustomerRating: +(a.custSum / a.custCount).toFixed(2),
    avgDriverRating: +(a.drvSum / a.drvCount).toFixed(2),
  }))
  .sort((a, b) => a.vehicleType.localeCompare(b.vehicleType))

const output = { overview, vehicleType, revenue, cancellation, ratings }

fs.mkdirSync(path.dirname(OUT_PATH), { recursive: true })
fs.writeFileSync(OUT_PATH, JSON.stringify(output, null, 2))
console.log(`Wrote ${OUT_PATH}`)
console.log(`Rows processed: ${totalBookings}`)
