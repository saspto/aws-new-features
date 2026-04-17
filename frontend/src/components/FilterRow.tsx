import { useEffect, useState } from 'react'
import { getServices, getTypes } from '../api/client'

interface Props {
  service: string
  type: string
  from_date: string
  to_date: string
  sort: 'date_desc' | 'date_asc'
  onFilter: (key: string, value: string) => void
}

export default function FilterRow({ service, type, from_date, to_date, sort, onFilter }: Props) {
  const [services, setServices] = useState<{ service_slug: string; count: number }[]>([])
  const [types, setTypes] = useState<{ feature_type: string; count: number }[]>([])

  useEffect(() => {
    getServices().then(setServices).catch(() => {})
    getTypes().then(setTypes).catch(() => {})
  }, [])

  return (
    <div className="flex flex-wrap gap-2 items-center">
      <select
        value={service}
        onChange={e => onFilter('service', e.target.value)}
        className="text-sm border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">All services</option>
        {services.map(s => (
          <option key={s.service_slug} value={s.service_slug}>
            {s.service_slug} ({s.count})
          </option>
        ))}
      </select>

      <select
        value={type}
        onChange={e => onFilter('type', e.target.value)}
        className="text-sm border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">All types</option>
        {types.map(t => (
          <option key={t.feature_type} value={t.feature_type}>
            {t.feature_type.replace(/-/g, ' ')} ({t.count})
          </option>
        ))}
      </select>

      <input
        type="date"
        value={from_date}
        onChange={e => onFilter('from_date', e.target.value)}
        className="text-sm border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="From date"
      />
      <input
        type="date"
        value={to_date}
        onChange={e => onFilter('to_date', e.target.value)}
        className="text-sm border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="To date"
      />

      <button
        onClick={() => onFilter('sort', sort === 'date_desc' ? 'date_asc' : 'date_desc')}
        className="text-sm font-medium text-gray-700 border border-gray-300 rounded-lg px-3 py-2 hover:bg-gray-50 transition-colors"
      >
        {sort === 'date_desc' ? 'Newest First ↓' : 'Oldest First ↑'}
      </button>
    </div>
  )
}
