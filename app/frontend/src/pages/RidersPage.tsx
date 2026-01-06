import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { getRiders } from '@/api/riders'
import type { Rider } from '@/api/types'
import { Users, Database } from 'lucide-react'

export function RidersPage() {
  // ============================================================================
  // 📦 STATE MANAGEMENT (You'll implement these)
  // ============================================================================
  
  // TODO: Add useState for riders data
  const [riders, setRiders] = useState<Rider[]>([])
  
  // TODO: Add useState for loading state
  const [loading, setLoading] = useState(true)
  
  // TODO: Add useState for error state
  const [error, setError] = useState<string | null>(null)

  // useEffect runs AFTER the component renders
  // The empty dependency array [] means: "run once when component mounts"
  useEffect(() => {
    // Define an async function inside useEffect
    // (useEffect itself cannot be async, but functions inside it can be)
    async function fetchRiders() {
      try {
        // Step 1: Set loading to true (show loading UI)
        setLoading(true)
        
        // Step 2: Call the API (this is async, so we await)
        console.log('Fetching riders from API...')
        const data = await getRiders()
        console.log('Riders fetched:', data)
        
        // Step 3: Update state with the data
        // This triggers a re-render!
        setRiders(data)
        
        // Step 4: Clear any previous errors
        setError(null)
        
      } catch (err) {
        // If API call fails, set error message
        console.error('Failed to fetch riders:', err)
        setError('Failed to load riders. Please try again later.')
        
      } finally {
        // Always set loading to false (whether success or error)
        setLoading(false)
      }
    }
    
    // Call the function we just defined
    fetchRiders()
    
    // Cleanup function (optional) - runs when component unmounts
    return () => {
      console.log('RidersPage unmounting...')
      // You could cancel ongoing requests here
    }
  }, [])  // Empty array = run once on mount
  //      ↑
  //      If you put [someValue] here, effect re-runs when someValue changes

  // ============================================================================
  // 🎨 CONDITIONAL RENDERING
  // ============================================================================

  // If loading, show loading UI
  // This happens during the first render (before data arrives)
  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-lg text-muted-foreground">Loading riders...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="text-center">
          <div className="text-lg text-destructive mb-4">⚠️ {error}</div>
          <button 
            onClick={() => window.location.reload()} 
            className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-6">
      {/* Page Header */}
      <div className="flex flex-col gap-2">
        <div className="flex items-center gap-3">
          <Users className="h-8 w-8" />
          <h1 className="text-3xl font-bold tracking-tight">Riders</h1>
        </div>
        <p className="text-muted-foreground">
          Browse all MotoGP riders and their statistics
          {riders.length > 0 && ` (${riders.length} riders)`}
        </p>
      </div>

      {/* Empty State */}
      {riders.length === 0 && (
        <Card className="border-dashed">
          <CardContent className="flex flex-col items-center justify-center py-12">
            <Database className="h-16 w-16 text-muted-foreground mb-4" />
            <h3 className="text-xl font-semibold mb-2">No Riders Yet</h3>
            <p className="text-muted-foreground text-center max-w-md mb-4">
              The database is empty. Add riders through the ETL process to see them here.
            </p>
            <p className="text-sm text-muted-foreground">
              API endpoint is working correctly ✅
            </p>
          </CardContent>
        </Card>
      )}

      {/* Riders Grid - Shows when data exists */}
      {riders.length > 0 && (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {riders.map((rider) => (
            <Card key={rider.id} className="hover:shadow-md transition-shadow">
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="space-y-1">
                    <CardTitle className="text-lg">
                      {rider.name} {rider.surname}
                    </CardTitle>
                    <div className="flex items-center gap-2">
                      {rider.nationality && (
                        <Badge variant="secondary">{rider.nationality}</Badge>
                      )}
                    </div>
                  </div>
                  <span className="text-2xl font-bold text-muted-foreground">
                    #{rider.id}
                  </span>
                </div>
              </CardHeader>
              <CardContent className="pt-0">
                <div className="flex justify-between text-sm text-muted-foreground">
                  <span>Status</span>
                  <span className="font-medium">
                    {rider.career_status || 'Unknown'}
                  </span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}