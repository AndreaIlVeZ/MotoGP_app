//types defintinoi 
// based on the impedance mismatch is the equivalent of the schemas in the backend

export interface Rider {
    id: number
    name: string
    surname: string
    nationality: string | null
    career_status: string | null

}

export interface Season {
    id: number
    year: number
    category: string

}


export interface RaceCircuit {
    id: number
    season_id: number
    circuit: string
    date: string |null 
}

export interface ResultRace {

    id: number
    rider_id: number
    race_circuit_id: number
    position: number | null
    points: number | null
}

// others to be created


export interface RaceWithResults {
    
    id: number
    circuit: string | null
    date: string | null
    season_year: number
    category: string
}


// Error response type
export interface ApiError {
  detail: string
}