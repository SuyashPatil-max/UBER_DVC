import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts'
import dashboardData from '../../../data/dashboardData.json'
import KpiCard from '../KpiCard.jsx'
import ChartCard from '../ChartCard.jsx'
import ChartGradientDefs from '../ChartGradientDefs.jsx'
import { gradientIds } from '../../../utils/chartColors.js'

const { vehicleType } = dashboardData
const totalValue = vehicleType.reduce((s, v) => s + v.totalValue, 0)
const totalBookings = vehicleType.reduce((s, v) => s + v.bookings, 0)
const topVehicle = vehicleType[0]

const tooltipStyle = {
  contentStyle: { background: '#141415', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 12 },
  labelStyle: { color: '#F3F2EF' },
  cursor: { fill: 'rgba(255,255,255,0.04)' },
}

export default function VehicleTypePage() {
  return (
    <div className="flex flex-col gap-6">
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3">
        <KpiCard label="Vehicle Types" value={vehicleType.length} accent="#B4A5F5" />
        <KpiCard label="Total Completed Bookings" value={totalBookings.toLocaleString()} accent="#8FB1E8" />
        <KpiCard
          label="Top Earner"
          value={topVehicle.vehicleType}
          sublabel={`₹${(topVehicle.totalValue / 100000).toFixed(1)}L revenue`}
          accent="#5FCB9B"
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <ChartCard title="Booking Value by Vehicle Type">
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={vehicleType} layout="vertical" margin={{ left: 24 }}>
                <ChartGradientDefs />
                <CartesianGrid stroke="rgba(255,255,255,0.06)" horizontal={false} />
                <XAxis type="number" stroke="#8D8D93" fontSize={11} tickLine={false} />
                <YAxis
                  type="category"
                  dataKey="vehicleType"
                  stroke="#8D8D93"
                  fontSize={11}
                  tickLine={false}
                  axisLine={false}
                  width={90}
                />
                <Tooltip {...tooltipStyle} formatter={(v) => `₹${v.toLocaleString()}`} />
                <Bar dataKey="totalValue" name="Booking Value" radius={[0, 6, 6, 0]}>
                  {vehicleType.map((entry, i) => (
                    <Cell key={entry.vehicleType} fill={`url(#${gradientIds.barHorizontal(i)})`} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        <ChartCard title="Ride Distance by Vehicle Type (km)">
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={vehicleType} layout="vertical" margin={{ left: 24 }}>
                <ChartGradientDefs />
                <CartesianGrid stroke="rgba(255,255,255,0.06)" horizontal={false} />
                <XAxis type="number" stroke="#8D8D93" fontSize={11} tickLine={false} />
                <YAxis
                  type="category"
                  dataKey="vehicleType"
                  stroke="#8D8D93"
                  fontSize={11}
                  tickLine={false}
                  axisLine={false}
                  width={90}
                />
                <Tooltip {...tooltipStyle} formatter={(v) => `${v.toLocaleString()} km`} />
                <Bar dataKey="totalDistance" name="Ride Distance" radius={[0, 6, 6, 0]}>
                  {vehicleType.map((entry, i) => (
                    <Cell key={entry.vehicleType} fill={`url(#${gradientIds.barHorizontal(i + 2)})`} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
      </div>
    </div>
  )
}
