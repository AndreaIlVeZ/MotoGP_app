// races api methods

import {apiClient} from './client'
import type { RaceCircuit, ResultRace } from './types'



export async function getRaceCircuits(): Promise<RaceCircuit[]> {
    const response = await apiClient.get<RaceCircuit[]>('/races/')
    return response.data
}

export async function getRaceCircuitById(raceCircuitId: number): Promise<RaceCircuit> {
    const response = await apiClient.get<RaceCircuit>(`/races/${raceCircuitId}`)
    return response.data
}   

export async function getResultRaces(): Promise<ResultRace[]> {
    const response = await apiClient.get<ResultRace[]>('/results/')
    return response.data
}   

