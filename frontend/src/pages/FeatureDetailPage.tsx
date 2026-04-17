import { useEffect, useState } from 'react'
import { useParams, useNavigate, useLocation } from 'react-router-dom'
import { getFeature, Feature } from '../api/client'

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
      year: 'numeric', month: 'long', day: 'numeric',
    })
  } catch {
    return iso
  }
}

export default function FeatureDetailPage() {
  const { guid } = useParams<{ guid: string }>()
  const navigate = useNavigate()
  const location = useLocation()
  const [feature, setFeature] = useState<Feature | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!guid) return
    setLoading(true)
    getFeature(decodeURIComponent(guid))
      .then(setFeature)
      .catch(() => setError('Feature not found'))
      .finally(() => setLoading(false))
  }, [guid])

  const backUrl = location.state?.from ?? '/'

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
      </div>
    )
  }

  if (error || !feature) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 font-medium">{error ?? 'Feature not found'}</p>
          <button onClick={() => navigate(backUrl)} className="mt-4 text-blue-600 hover:underline text-sm">
            ← Back to search
          </button>
        </div>
      </div>
    )
  }

  const typeColor = FEATURE_TYPE_COLORS[feature.feature_type] ?? 'bg-gray-100 text-gray-800'

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-3xl mx-auto px-4 py-8">
        <button
          onClick={() => navigate(backUrl)}
          className="flex items-center gap-1 text-sm text-blue-600 hover:underline mb-6"
        >
          ← Back to search
        </button>

        <article className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
          <div className="flex flex-wrap gap-2 items-center mb-4">
            <span className="text-sm text-gray-500">{formatDate(feature.pub_date)}</span>
            {feature.service_name && (
              <span className="px-2.5 py-0.5 rounded-full text-sm font-medium bg-orange-100 text-orange-800">
                {feature.service_name}
              </span>
            )}
            {feature.type && (
              <span className="px-2.5 py-0.5 rounded-full text-sm font-medium bg-slate-100 text-slate-700">
                {feature.type}
              </span>
            )}
            {feature.feature_type && (
              <span className={`px-2.5 py-0.5 rounded-full text-sm font-semibold ${typeColor}`}>
                {feature.feature_type.replace(/-/g, ' ')}
              </span>
            )}
          </div>

          <h1 className="text-2xl font-bold text-gray-900 mb-6 leading-snug">{feature.title}</h1>

          {feature.summary && (
            <section className="mb-6">
              <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">Summary</h2>
              <p className="text-gray-800 leading-relaxed">{feature.summary}</p>
            </section>
          )}

          {feature.key_points && feature.key_points.length > 0 && (
            <section className="mb-6">
              <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">Key Points</h2>
              <ul className="space-y-2">
                {feature.key_points.map((pt, i) => (
                  <li key={i} className="flex items-start gap-2 text-gray-800">
                    <span className="mt-1 h-1.5 w-1.5 rounded-full bg-blue-500 shrink-0" />
                    {pt}
                  </li>
                ))}
              </ul>
            </section>
          )}

          <div className="border-t border-gray-100 pt-6 flex flex-wrap gap-3 items-center justify-between">
            <div className="text-xs text-gray-400">
              {feature.summarized_at && `Summarized: ${formatDate(feature.summarized_at)}`}
            </div>
            <a
              href={feature.link}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 text-sm font-medium text-white bg-orange-500 hover:bg-orange-600 rounded-lg px-4 py-2 transition-colors"
            >
              View AWS Announcement →
            </a>
          </div>
        </article>
      </div>
    </div>
  )
}
