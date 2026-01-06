import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Layout } from './components/Layout'
import { HomePage } from './pages/HomePage'
import { RidersPage } from './pages/RidersPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Main Layout wraps all pages */}
        <Route path="/" element={<Layout />}>
          {/* index = default route when path is "/" */}
          <Route index element={<HomePage />} />
          
          {/* /riders route */}
          <Route path="riders" element={<RidersPage />} />
          
          {/* TODO: Add more routes as you build them */}
          {/* <Route path="races" element={<RacesPage />} /> */}
          {/* <Route path="standings" element={<StandingsPage />} /> */}
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App