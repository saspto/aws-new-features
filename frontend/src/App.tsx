import { BrowserRouter, Routes, Route } from 'react-router-dom'
import SearchPage from './pages/SearchPage'
import FeatureDetailPage from './pages/FeatureDetailPage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<SearchPage />} />
        <Route path="/feature/:guid" element={<FeatureDetailPage />} />
      </Routes>
    </BrowserRouter>
  )
}
