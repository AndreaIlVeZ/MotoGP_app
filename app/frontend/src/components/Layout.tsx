import { Link, Outlet } from 'react-router-dom'
import { Button } from './ui/button'
import { Flag } from 'lucide-react'

export function Layout() {
  return (
    <div className="min-h-screen bg-background">
      {/* Navigation Header */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-14 max-w-screen-2xl items-center">
          <div className="mr-4 flex">
            <Link to="/" className="mr-6 flex items-center space-x-2">
              <Flag className="h-6 w-6" />
              <span className="font-bold">MotoGP Stats</span>
            </Link>
          </div>
          <nav className="flex items-center gap-4 text-sm">
            <Button variant="ghost" size="sm" asChild>
              <Link to="/">Home</Link>
            </Button>
            <Button variant="ghost" size="sm" asChild>
              <Link to="/riders">Riders</Link>
            </Button>
            <Button variant="ghost" size="sm" asChild>
              <Link to="/races">Races</Link>
            </Button>
            <Button variant="ghost" size="sm" asChild>
              <Link to="/standings">Standings</Link>
            </Button>
          </nav>
        </div>
      </header>

      {/* Main Content Area - Child routes render here via <Outlet /> */}
      <main className="container py-6">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="border-t py-6 md:py-0">
        <div className="container flex flex-col items-center justify-between gap-4 md:h-24 md:flex-row">
          <p className="text-center text-sm leading-loose text-muted-foreground md:text-left">
            Built with FastAPI & React. MotoGP Stats © 2026
          </p>
        </div>
      </footer>
    </div>
  )
}