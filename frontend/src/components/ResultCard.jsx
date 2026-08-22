import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import { getResultMeta } from "../utils/resultMeta.js";

export default function ResultCard({ result }) {
  if (!result) return null;

  const probability = Number(result.probability ?? 0);
  const meta = getResultMeta(result.prediction);

  // Binary donut: the predicted class's own probability, and the
  // remainder, so the ring always reads as "how sure are we" rather
  // than a full class breakdown.
  const data = [
    { name: meta.label, value: probability * 100, color: meta.color },
    { name: "Remainder", value: (1 - probability) * 100, color: "#2A2A2C" },
  ];

  return (
    <div className="result-card animate-resultReveal">

      <div className="grid md:grid-cols-2 gap-6 items-center">

        {/* LEFT */}

        <div className="text-center">

          <div className="emoji-pop text-5xl mb-2">
            {meta.emoji}
          </div>

          <h2
            className="text-2xl font-bold tracking-tight"
            style={{ color: meta.color }}
          >
            {meta.label}
          </h2>

          <p className="mt-1 text-sm text-zinc-500">
            Predicted ride outcome
          </p>

          <div className="mt-5">

            <p className="text-xs tracking-[0.3em] uppercase text-zinc-500">
              Probability
            </p>

            <h3 className="mt-1 text-3xl font-bold">
              {(probability * 100).toFixed(1)}%
            </h3>

          </div>

        </div>

        {/* RIGHT */}

        <div>

          <div className="h-52">

            <ResponsiveContainer width="100%" height="100%">

              <PieChart>

                <defs>
                  <filter
                    id="resultGlow"
                    x="-50%"
                    y="-50%"
                    width="200%"
                    height="200%"
                  >
                    <feDropShadow
                      dx="0"
                      dy="0"
                      stdDeviation="8"
                      floodColor={meta.color}
                      floodOpacity="0.7"
                    />
                  </filter>
                </defs>

                <Pie
                  data={data}
                  dataKey="value"
                  innerRadius={48}
                  outerRadius={76}
                  paddingAngle={2}
                  cornerRadius={8}
                  startAngle={90}
                  endAngle={-270}
                  isAnimationActive={true}
                  animationDuration={1400}
                  animationEasing="ease-out"
                >

                  {data.map((entry, index) => (
                    <Cell
                      key={`cell-${entry.name}`}
                      fill={entry.color}
                      filter={index === 0 ? "url(#resultGlow)" : undefined}
                      stroke="#111"
                      strokeWidth={2}
                    />
                  ))}

                </Pie>

                {/* CENTER PERCENTAGE */}

                <text
                  x="50%"
                  y="48%"
                  textAnchor="middle"
                  fill="#FFFFFF"
                  fontSize="20"
                  fontWeight="700"
                >
                  {(probability * 100).toFixed(0)}%
                </text>

                <text
                  x="50%"
                  y="60%"
                  textAnchor="middle"
                  fill="#9CA3AF"
                  fontSize="11"
                >
                  AI
                </text>

                <Tooltip formatter={(value) => `${value.toFixed(1)}%`} />

              </PieChart>

            </ResponsiveContainer>

          </div>

          <div className="mt-3 flex flex-wrap justify-center gap-x-6 gap-y-2 text-sm">

            <div className="flex items-center gap-2">
              <div
                className="h-3 w-3 rounded-full"
                style={{
                  backgroundColor: meta.color,
                  boxShadow: `0 0 10px ${meta.color}`,
                }}
              />
              <span>{meta.label}</span>
              <strong>{(probability * 100).toFixed(1)}%</strong>
            </div>

            <div className="flex items-center gap-2">
              <div
                className="h-3 w-3 rounded-full"
                style={{ backgroundColor: "#2A2A2C" }}
              />
              <span>Remaining uncertainty</span>
              <strong>{((1 - probability) * 100).toFixed(1)}%</strong>
            </div>

          </div>

        </div>

      </div>

    </div>
  );
}
