import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Feature } from '../api/client'

const FEATURE_TYPE_COLORS: Record<string, string> = {
  'new-feature': 'bg-blue-100 text-blue-800',
  'enhancement': 'bg-green-100 text-green-800',
  'preview': 'bg-yellow-100 text-yellow-800',
  'general-availability': 'bg-emerald-100 text-emerald-800',
  'deprecation': 'bg-red-100 text-red-800',
  'price-change': 'bg-purple-100 text-purple-800',
  'region-expansion': 'bg-indigo-100 text-indigo-800',
  'integration': 'bg-cyan-100 text-cyan-800',
}

function formatDate(iso: string): string {
  if (!iso) return ''
  try {
    return new Date(iso).toLocaleDateString('en-US', {
      year: 'numeric', month: 'short', day: 'numeric',
    })
  } catch {
    return iso
  }
}

interface Props {
  feature: Feature
}

export default function FeatureCard({ feature }: Props) {
  const navigate = useNavigate()
  const [expanded, setExpanded] = useState(false)
  const typeColor = FEATURE_TYPE_COLORS[feature.feature_type] ?? 'bg-gray-100 text-gray-800'

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 flex flex-col gap-3 hover:shadow-md transition-shadow">
      <div className="flex flex-wrap gap-2 items-center">
        <span className="text-xs font-medium text-gray-500">{formatDate(feature.pub_date)}</span>
        {feature.service_name && (
          <span className="px-2 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
            {feature.service_name}
          </span>
        )}
        {feature.type && (
          <span className="px-2 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-700">
            {feature.type}
          </span>
        )}
        {feature.feature_type && (
          <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${typeColor}`}>
            {feature.feature_type.replace(/-/g, ' ')}
          </span>
        )}
      </div>

      <h3 className="font-semibold text-gray-900 leading-snug line-clamp-2">{feature.title}</h3>

      {feature.summary && (
        <p className="text-sm text-gray-600 line-clamp-2">{feature.summary}</p>
      )}

      {feature.key_points && feature.key_points.length > 0 && (
        <div>
          <button
            className="text-xs text-blue-600 hover:underline mb-1"
            onClick={() => setExpanded(e => !e)}
          >
            {expanded ? 'Hide' : 'Show'} key points
          </button>
          {expanded && (
            <ul className="list-disc list-inside space-y-0.5">
              {feature.key_points.map((pt, i) => (
                <li key={i} className="text-sm text-gray-700">{pt}</li>
              ))}
            </ul>
          )}
        </div>
      )}

      <div className="flex gap-2 mt-auto pt-2">
        <button
          onClick={() => navigate(`/feature/${encodeURIComponent(feature.guid)}`)}
          className="flex-1 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg px-3 py-1.5 transition-colors text-center"
        >
          View Details
        </button>
        <a
          href={feature.link}
          target="_blank"
          rel="noopener noreferrer"
          className="text-sm font-medium text-blue-600 hover:text-blue-800 border border-blue-200 hover:border-blue-400 rounded-lg px-3 py-1.5 transition-colors"
        >
          AWS Announcement →
        </a>
      </div>
    </div>
  )
}
