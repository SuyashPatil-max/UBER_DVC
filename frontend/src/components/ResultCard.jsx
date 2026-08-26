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
  const confidencePct = probability * 100;
  const meta = getResultMeta(result.prediction);

  // Binary donut: the predicted class's own probability, and the
  // remainder, so the ring always reads as "how sure are we" rather
  // than a full class breakdown.
  const data = [
    { name: meta.label, value: confidencePct, color: meta.color },
    { name: "Remainder", value: 100 - confidencePct, color: "#2A2A2C" },
  ];

  return (
    <div
      className="result-card animate-resultReveal"
      style={{ "--result-color": meta.color }}
    >

      {/* HEADER */}

      <div className="result-topbar">

        <span className="result-pill">
          <span className="result-pill-dot" />
          Prediction Result
        </span>

        <span className="result-model-tag">
          Ride Completion Model
        </span>

      </div>

      <div className="grid md:grid-cols-[1fr_auto_1fr] gap-6 md:gap-8 items-center">

        {/* LEFT */}

        <div className="text-center">

          <div className="result-emoji-badge emoji-pop">
            <span className="text-4xl">{meta.emoji}</span>
          </div>

          <h2
            className="mt-4 text-2xl font-bold tracking-tight"
            style={{ color: meta.color }}
          >
            {meta.label}
          </h2>

          <p className="mt-1 text-sm text-zinc-500">
            Predicted ride outcome
          </p>

          <div className="mt-6">

            <p className="text-xs tracking-[0.3em] uppercase text-zinc-500">
              Probability
            </p>

            <h3 className="mt-1 text-3xl font-bold">
              {confidencePct.toFixed(1)}%
            </h3>

            <div className="confidence-track mt-3 max-w-[220px] mx-auto">
              <div
                className="confidence-fill"
                style={{ width: `${confidencePct}%` }}
              />
            </div>

          </div>

        </div>

        {/* DIVIDER */}

        <div className="result-divider hidden md:block" aria-hidden="true" />

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
                  {confidencePct.toFixed(0)}%
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

          <div className="mt-3 flex flex-wrap justify-center gap-2 text-sm">

            <div className="result-chip">
              <div
                className="h-2.5 w-2.5 rounded-full"
                style={{
                  backgroundColor: meta.color,
                  boxShadow: `0 0 10px ${meta.color}`,
                }}
              />
              <span className="text-zinc-300">{meta.label}</span>
              <strong>{confidencePct.toFixed(1)}%</strong>
            </div>

            <div className="result-chip">
              <div
                className="h-2.5 w-2.5 rounded-full"
                style={{ backgroundColor: "#2A2A2C" }}
              />
              <span className="text-zinc-300">Remaining uncertainty</span>
              <strong>{(100 - confidencePct).toFixed(1)}%</strong>
            </div>

          </div>

        </div>

      </div>

    </div>
  );
}
