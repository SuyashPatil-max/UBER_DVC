import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import dashboardData from '../../../data/dashboardData.json'
import KpiCard from '../KpiCard.jsx'
import ChartCard from '../ChartCard.jsx'
import ChartGradientDefs from '../ChartGradientDefs.jsx'
import { gradientIds } from '../../../utils/chartColors.js'

const { cancellation } = dashboardData

const tooltipStyle = {
  contentStyle: { background: '#141415', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 12 },
  labelStyle: { color: '#F3F2EF' },
}

function ReasonPie({ data, dataKey = 'count', nameKey = 'reason' }) {
  return (
    <div className="h-72">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <ChartGradientDefs />
          <Pie data={data} dataKey={dataKey} nameKey={nameKey} innerRadius={50} outerRadius={85} paddingAngle={3}>
            {data.map((entry, i) => (
              <Cell key={entry[nameKey]} fill={`url(#${gradientIds.pie(i)})`} stroke="#111" strokeWidth={2} />
            ))}
          </Pie>
          <Tooltip {...tooltipStyle} />
          <Legend
            layout="vertical"
            position="right"
            formatter={(value) => <span className="text-xs text-text-secondary">{value}</span>}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}

export default function CancellationPage() {
  return (
    <div className="flex flex-col gap-6">
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <KpiCard
          label="Cancelled by Customer"
          value={cancellation.totalCancelledByCustomer.toLocaleString()}
          accent="#E38A93"
        />
        <KpiCard
          label="Cancelled by Driver"
          value={cancellation.totalCancelledByDriver.toLocaleString()}
          accent="#E38A93"
        />
        <KpiCard label="Incomplete Rides" value={cancellation.totalIncomplete.toLocaleString()} accent="#F5C26B" />
        <KpiCard label="Cancellation Rate" value={`${cancellation.cancelledPercentage}%`} accent="#B4A5F5" />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <ChartCard title="Customer Cancellation Reasons">
          <ReasonPie data={cancellation.customerCancelReasons} />
        </ChartCard>
        <ChartCard title="Driver Cancellation Reasons">
          <ReasonPie data={cancellation.driverCancelReasons} />
        </ChartCard>
      </div>
    </div>
  )
}
