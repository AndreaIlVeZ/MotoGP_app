//rider api mthods

import { apiClient } from './client'
import type { Rider } from './types'

/**
 * Fetch all riders from the API
 * GET /api/riders/
 */
export async function getRiders(): Promise<Rider[]> {
  const response = await apiClient.get<Rider[]>('/riders/')
  return response.data
}

/**
 * Fetch a single rider by ID
 * GET /api/riders/{rider_id}
 */
export async function getRiderById(riderId: number): Promise<Rider> {
  const response = await apiClient.get<Rider>(`/riders/${riderId}`)
  return response.data
}

// TODO: Add more rider-related API calls as needed
// export async function getRiderStats(riderId: number) { ... }
// export async function getRiderResults(riderId: number) { ... }