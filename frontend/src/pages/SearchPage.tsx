import { useEffect, useRef, useCallback } from 'react'
import { useFeatureSearch } from '../hooks/useFeatureSearch'
import SearchBar from '../components/SearchBar'
import FilterRow from '../components/FilterRow'
import FeatureCard from '../components/FeatureCard'
import SkeletonCard from '../components/SkeletonCard'

export default function SearchPage() {
  const {
    items, totalCount, loading, loadingMore, error, hasMore,
    q, service, type, from_date, to_date, sort,
    setFilter, loadMore,
  } = useFeatureSearch()

  const sentinelRef = useRef<HTMLDivElement>(null)

  const handleIntersect = useCallback((entries: IntersectionObserverEntry[]) => {
    if (entries[0].isIntersecting && hasMore && !loadingMore) {
      loadMore()
    }
  }, [hasMore, loadingMore, loadMore])

  useEffect(() => {
    const el = sentinelRef.current
    if (!el) return
    const observer = new IntersectionObserver(handleIntersect, { threshold: 0.1 })
    observer.observe(el)
    return () => observer.disconnect()
  }, [handleIntersect])

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center gap-4 mb-3">
            <div>
              <h1 className="text-xl font-bold text-gray-900">AWS Features Tracker</h1>
              <p className="text-xs text-gray-500">AI-summarized AWS announcements</p>
            </div>
          </div>
          <SearchBar value={q} onChange={v => setFilter('q', v)} />
          <div className="mt-3">
            <FilterRow
              service={service}
              type={type}
              from_date={from_date}
              to_date={to_date}
              sort={sort}
              onFilter={setFilter}
            />
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6">
        {!loading && !error && (
          <p className="text-sm text-gray-500 mb-4">
            Showing {items.length} of {totalCount} features
          </p>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 rounded-xl p-4 mb-4 text-sm">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {loading
            ? Array.from({ length: 6 }).map((_, i) => <SkeletonCard key={i} />)
            : items.map(f => <FeatureCard key={f.guid} feature={f} />)
          }
          {loadingMore && Array.from({ length: 3 }).map((_, i) => <SkeletonCard key={`more-${i}`} />)}
        </div>

        {!loading && items.length === 0 && !error && (
          <div className="text-center py-20 text-gray-400">
            <p className="text-lg font-medium">No features found</p>
            <p className="text-sm mt-1">Try adjusting your search or filters</p>
          </div>
        )}

        <div ref={sentinelRef} className="h-4" />
      </main>
    </div>
  )
}
