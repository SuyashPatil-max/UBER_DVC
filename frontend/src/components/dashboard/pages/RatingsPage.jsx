import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import dashboardData from '../../../data/dashboardData.json'
import KpiCard from '../KpiCard.jsx'
import ChartCard from '../ChartCard.jsx'
import ChartGradientDefs from '../ChartGradientDefs.jsx'
import { gradientIds } from '../../../utils/chartColors.js'

const { ratings } = dashboardData
const avgCustomer = (ratings.reduce((s, r) => s + r.avgCustomerRating, 0) / ratings.length).toFixed(2)
const avgDriver = (ratings.reduce((s, r) => s + r.avgDriverRating, 0) / ratings.length).toFixed(2)

const tooltipStyle = {
  contentStyle: { background: '#141415', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 12 },
  labelStyle: { color: '#F3F2EF' },
  cursor: { fill: 'rgba(255,255,255,0.04)' },
}

export default function RatingsPage() {
  return (
    <div className="flex flex-col gap-6">
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3">
        <KpiCard label="Avg Customer Rating" value={`${avgCustomer} ★`} accent="#5FCB9B" />
        <KpiCard label="Avg Driver Rating" value={`${avgDriver} ★`} accent="#8FB1E8" />
        <KpiCard label="Vehicle Types Rated" value={ratings.length} accent="#B4A5F5" />
      </div>

      <ChartCard title="Average Ratings by Vehicle Type">
        <div className="h-96">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={ratings} margin={{ bottom: 8 }}>
              <ChartGradientDefs />
              <CartesianGrid stroke="rgba(255,255,255,0.06)" vertical={false} />
              <XAxis dataKey="vehicleType" stroke="#8D8D93" fontSize={11} tickLine={false} />
              <YAxis domain={[0, 5]} stroke="#8D8D93" fontSize={11} tickLine={false} axisLine={false} />
              <Tooltip {...tooltipStyle} />
              <Legend formatter={(value) => <span className="text-xs text-text-secondary">{value}</span>} />
              <Bar
                dataKey="avgCustomerRating"
                name="Customer Rating"
                fill={`url(#${gradientIds.bar(2)})`}
                radius={[6, 6, 0, 0]}
              />
              <Bar
                dataKey="avgDriverRating"
                name="Driver Rating"
                fill={`url(#${gradientIds.bar(1)})`}
                radius={[6, 6, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </ChartCard>
    </div>
  )
}
