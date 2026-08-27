import {
  BarChart,
  Bar,
  AreaChart,
  Area,
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

const { revenue } = dashboardData
const totalRevenue = revenue.revenueByPaymentMethod.reduce((s, p) => s + p.value, 0)
const topMethod = revenue.revenueByPaymentMethod[0]

const tooltipStyle = {
  contentStyle: { background: '#141415', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 12 },
  labelStyle: { color: '#F3F2EF' },
}

export default function RevenuePage() {
  return (
    <div className="flex flex-col gap-6">
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3">
        <KpiCard label="Total Revenue" value={`₹${(totalRevenue / 100000).toFixed(1)}L`} accent="#F5C26B" />
        <KpiCard
          label="Top Payment Method"
          value={topMethod.method}
          sublabel={`₹${(topMethod.value / 100000).toFixed(1)}L`}
          accent="#B4A5F5"
        />
        <KpiCard label="Top Customers Tracked" value={revenue.topCustomers.length} accent="#8FB1E8" />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <ChartCard title="Revenue by Payment Method">
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={revenue.revenueByPaymentMethod}>
                <ChartGradientDefs />
                <CartesianGrid stroke="rgba(255,255,255,0.06)" vertical={false} />
                <XAxis dataKey="method" stroke="#8D8D93" fontSize={11} tickLine={false} />
                <YAxis stroke="#8D8D93" fontSize={11} tickLine={false} axisLine={false} />
                <Tooltip {...tooltipStyle} formatter={(v) => `₹${v.toLocaleString()}`} cursor={{ fill: 'rgba(255,255,255,0.04)' }} />
                <Bar dataKey="value" name="Revenue" radius={[6, 6, 0, 0]}>
                  {revenue.revenueByPaymentMethod.map((entry, i) => (
                    <Cell key={entry.method} fill={`url(#${gradientIds.bar(i)})`} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        <ChartCard title="Revenue Trend">
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={revenue.revenueOverTime}>
                <ChartGradientDefs />
                <CartesianGrid stroke="rgba(255,255,255,0.06)" vertical={false} />
                <XAxis dataKey="month" stroke="#8D8D93" fontSize={11} tickLine={false} />
                <YAxis stroke="#8D8D93" fontSize={11} tickLine={false} axisLine={false} />
                <Tooltip {...tooltipStyle} formatter={(v) => `₹${v.toLocaleString()}`} />
                <Area
                  type="monotone"
                  dataKey="value"
                  name="Revenue"
                  stroke="#8FB1E8"
                  strokeWidth={2.5}
                  fill={`url(#${gradientIds.area(1)})`}
                  dot={false}
                  activeDot={{ r: 5, fill: '#8FB1E8', stroke: '#0A0A0A', strokeWidth: 2 }}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
      </div>

      <ChartCard title="Top Customers by Spend">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-ink-border text-xs uppercase tracking-wider text-text-tertiary">
                <th className="py-2 pr-4">Rank</th>
                <th className="py-2 pr-4">Customer ID</th>
                <th className="py-2 pr-4 text-right">Total Spend</th>
              </tr>
            </thead>
            <tbody>
              {revenue.topCustomers.map((c, i) => (
                <tr key={c.customerId} className="border-b border-ink-border/50 text-text-secondary">
                  <td className="py-2 pr-4 text-text-tertiary">{i + 1}</td>
                  <td className="py-2 pr-4 text-text-primary">{c.customerId}</td>
                  <td className="py-2 pr-4 text-right">₹{c.value.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </ChartCard>
    </div>
  )
}
