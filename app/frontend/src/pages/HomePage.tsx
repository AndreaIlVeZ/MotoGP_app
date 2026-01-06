// filepath: [HomePage.tsx](http://_vscodecontentref_/0)
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Link } from 'react-router-dom'
import { Users, Flag, Trophy } from 'lucide-react'

export function HomePage() {
  return (
    <div className="flex flex-col gap-8">
      {/* Hero Section */}
      <div className="flex flex-col items-center gap-4 text-center">
        <div className="space-y-2">
          <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl">
            Welcome to MotoGP Stats
          </h1>
          <p className="mx-auto max-w-[700px] text-muted-foreground md:text-xl">
            Explore riders, races, and championship standings from the world of MotoGP racing
          </p>
        </div>
      </div>

      {/* Feature Cards */}
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <Users className="h-10 w-10 mb-2 text-primary" />
            <CardTitle>Riders</CardTitle>
            <CardDescription>
              Browse all MotoGP riders and their career statistics
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full">
              <Link to="/riders">View Riders</Link>
            </Button>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <Flag className="h-10 w-10 mb-2 text-primary" />
            <CardTitle>Races</CardTitle>
            <CardDescription>
              Check out race results and circuit information
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full">
              <Link to="/races">View Races</Link>
            </Button>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <Trophy className="h-10 w-10 mb-2 text-primary" />
            <CardTitle>Standings</CardTitle>
            <CardDescription>
              Current championship standings and rankings
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full">
              <Link to="/standings">View Standings</Link>
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Stats Preview */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Riders</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">--</div>
            <p className="text-xs text-muted-foreground">
              Active in current season
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Races</CardTitle>
            <Flag className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">--</div>
            <p className="text-xs text-muted-foreground">
              Circuits worldwide
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Championships</CardTitle>
            <Trophy className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">--</div>
            <p className="text-xs text-muted-foreground">
              Years of data
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}