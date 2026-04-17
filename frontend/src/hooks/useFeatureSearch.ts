import { useState, useEffect, useCallback, useRef } from 'react'
import { useSearchParams } from 'react-router-dom'
import { searchFeatures, Feature, SearchParams } from '../api/client'

interface SearchState {
  items: Feature[]
  totalCount: number
  loading: boolean
  loadingMore: boolean
  error: string | null
  nextToken: string | null
  hasMore: boolean
}

export function useFeatureSearch() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [state, setState] = useState<SearchState>({
    items: [],
    totalCount: 0,
    loading: false,
    loadingMore: false,
    error: null,
    nextToken: null,
    hasMore: false,
  })

  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const abortRef = useRef<AbortController | null>(null)

  const q = searchParams.get('q') ?? ''
  const service = searchParams.get('service') ?? ''
  const type = searchParams.get('type') ?? ''
  const from_date = searchParams.get('from_date') ?? ''
  const to_date = searchParams.get('to_date') ?? ''
  const sort = (searchParams.get('sort') ?? 'date_desc') as 'date_desc' | 'date_asc'

  const buildParams = useCallback((): SearchParams => {
    const p: SearchParams = { sort, limit: 20 }
    if (q) p.q = q
    if (service) p.service = service
    if (type) p.type = type
    if (from_date) p.from_date = from_date
    if (to_date) p.to_date = to_date
    return p
  }, [q, service, type, from_date, to_date, sort])

  const doSearch = useCallback(async (params: SearchParams) => {
    if (abortRef.current) abortRef.current.abort()
    abortRef.current = new AbortController()

    setState(prev => ({ ...prev, loading: true, error: null }))
    try {
      const result = await searchFeatures(params)
      setState({
        items: result.items,
        totalCount: result.total_count,
        loading: false,
        loadingMore: false,
        error: null,
        nextToken: result.next_token,
        hasMore: result.next_token !== null,
      })
    } catch (err: unknown) {
      if (err instanceof Error && err.name === 'CanceledError') return
      setState(prev => ({
        ...prev,
        loading: false,
        error: 'Failed to load features. Please try again.',
      }))
    }
  }, [])

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => {
      doSearch(buildParams())
    }, 300)
    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current)
    }
  }, [buildParams, doSearch])

  const loadMore = useCallback(async () => {
    if (!state.nextToken || state.loadingMore) return
    setState(prev => ({ ...prev, loadingMore: true }))
    try {
      const params = { ...buildParams(), next_token: state.nextToken }
      const result = await searchFeatures(params)
      setState(prev => ({
        ...prev,
        items: [...prev.items, ...result.items],
        totalCount: result.total_count,
        loadingMore: false,
        nextToken: result.next_token,
        hasMore: result.next_token !== null,
      }))
    } catch {
      setState(prev => ({ ...prev, loadingMore: false }))
    }
  }, [state.nextToken, state.loadingMore, buildParams])

  const setFilter = useCallback((key: string, value: string) => {
    setSearchParams(prev => {
      const next = new URLSearchParams(prev)
      if (value) {
        next.set(key, value)
      } else {
        next.delete(key)
      }
      return next
    }, { replace: true })
  }, [setSearchParams])

  return {
    ...state,
    q, service, type, from_date, to_date, sort,
    setFilter,
    loadMore,
  }
}
