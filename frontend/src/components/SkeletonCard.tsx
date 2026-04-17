export default function SkeletonCard() {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 flex flex-col gap-3 animate-pulse">
      <div className="flex gap-2">
        <div className="h-4 w-20 bg-gray-200 rounded-full" />
        <div className="h-4 w-24 bg-gray-200 rounded-full" />
        <div className="h-4 w-16 bg-gray-200 rounded-full" />
      </div>
      <div className="h-5 w-3/4 bg-gray-200 rounded" />
      <div className="h-4 w-full bg-gray-200 rounded" />
      <div className="h-4 w-5/6 bg-gray-200 rounded" />
      <div className="flex gap-2 mt-2">
        <div className="h-8 flex-1 bg-gray-200 rounded-lg" />
        <div className="h-8 w-36 bg-gray-200 rounded-lg" />
      </div>
    </div>
  )
}
