import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from 'recharts'
import dashboardData from '../../../data/dashboardData.json'
import KpiCard from '../KpiCard.jsx'
import ChartCard from '../ChartCard.jsx'
import ChartGradientDefs from '../ChartGradientDefs.jsx'
import { gradientIds } from '../../../utils/chartColors.js'

const { overview } = dashboardData

export default function OverviewPage() {
  return (
    <div className="flex flex-col gap-6">
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-5">
        <KpiCard label="Total Bookings" value={overview.totalBookings.toLocaleString()} accent="#B4A5F5" />
        <KpiCard label="Completed" value={overview.completedBookings.toLocaleString()} accent="#5FCB9B" />
        <KpiCard label="Completion Rate" value={`${overview.completionRate}%`} accent="#8FB1E8" />
        <KpiCard
          label="Total Revenue"
          value={`₹${(overview.totalRevenue / 100000).toFixed(1)}L`}
          accent="#F5C26B"
        />
        <KpiCard label="Avg Ride Distance" value={`${overview.avgRideDistance} km`} accent="#7DD3FC" />
      </div>

      <div className="grid gap-6 lg:grid-cols-[1.5fr_1fr]">
        <ChartCard title="Bookings Over Time">
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={overview.bookingsOverTime}>
                <ChartGradientDefs />
                <CartesianGrid stroke="rgba(255,255,255,0.06)" vertical={false} />
                <XAxis dataKey="month" stroke="#8D8D93" fontSize={11} tickLine={false} />
                <YAxis stroke="#8D8D93" fontSize={11} tickLine={false} axisLine={false} />
                <Tooltip
                  contentStyle={{ background: '#141415', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 12 }}
                  labelStyle={{ color: '#F3F2EF' }}
                />
                <Area
                  type="monotone"
                  dataKey="count"
                  name="Bookings"
                  stroke="#B4A5F5"
                  strokeWidth={2.5}
                  fill={`url(#${gradientIds.area(0)})`}
                  dot={false}
                  activeDot={{ r: 5, fill: '#B4A5F5', stroke: '#0A0A0A', strokeWidth: 2 }}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        <ChartCard title="Booking Status Breakdown">
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <ChartGradientDefs />
                <Pie
                  data={overview.statusBreakdown}
                  dataKey="count"
                  nameKey="status"
                  innerRadius={55}
                  outerRadius={90}
                  paddingAngle={3}
                >
                  {overview.statusBreakdown.map((entry, i) => (
                    <Cell key={entry.status} fill={`url(#${gradientIds.pie(i)})`} stroke="#111" strokeWidth={2} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ background: '#141415', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 12 }}
                  labelStyle={{ color: '#F3F2EF' }}
                />
                <Legend
                  layout="vertical"
                  position="right"
                  formatter={(value) => <span className="text-xs text-text-secondary">{value}</span>}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
      </div>
    </div>
  )
}
