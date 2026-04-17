import axios from 'axios'

const BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? '') + '/api'

const api = axios.create({ baseURL: BASE_URL })

export interface Feature {
  guid: string
  title: string
  service_slug: string
  service_name: string
  type: string
  feature_type: string
  pub_date: string
  link: string
  summary: string
  key_points: string[]
  summarized_at: string
}

export interface FeaturesResponse {
  items: Feature[]
  next_token: string | null
  total_count: number
}

export interface SearchParams {
  q?: string
  service?: string
  type?: string
  from_date?: string
  to_date?: string
  sort?: 'date_desc' | 'date_asc'
  limit?: number
  next_token?: string
}

export async function searchFeatures(params: SearchParams): Promise<FeaturesResponse> {
  const filtered = Object.fromEntries(
    Object.entries(params).filter(([, v]) => v !== '' && v !== undefined && v !== null)
  )
  const resp = await api.get<FeaturesResponse>('/features', { params: filtered })
  return resp.data
}

export async function getFeature(guid: string): Promise<Feature> {
  const resp = await api.get<Feature>(`/features/${encodeURIComponent(guid)}`)
  return resp.data
}

export async function getServices(): Promise<{ service_slug: string; count: number }[]> {
  const resp = await api.get('/services')
  return resp.data
}

export async function getTypes(): Promise<{ feature_type: string; count: number }[]> {
  const resp = await api.get('/types')
  return resp.data
}
