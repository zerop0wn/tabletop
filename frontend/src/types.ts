export interface Token {
  access_token: string
  token_type: string
}

export interface Scenario {
  id: number
  name: string
  description?: string
  miro_board_url?: string
  created_at: string
  phases: ScenarioPhase[]
}

export interface ScenarioPhase {
  id: number
  scenario_id: number
  order_index: number
  name: string
  briefing_text?: string
  red_objective?: string
  blue_objective?: string
  default_duration_seconds?: number
  miro_frame_url?: string
  artifacts: Artifact[]
}

export interface Artifact {
  id: number
  name: string
  type: string
  description?: string
  file_url?: string
  embed_url?: string
}

export interface Game {
  id: number
  scenario_id: number
  status: 'lobby' | 'in_progress' | 'paused' | 'finished'
  current_phase_id?: number
  phase_state: 'not_started' | 'briefing' | 'open_for_decisions' | 'decision_lock' | 'resolution' | 'complete'
  created_at: string
  gm_id: number
  red_team_code: string
  blue_team_code: string
  audience_code?: string
  miro_session_url?: string
  settings: Record<string, any>
  scenario?: Scenario
  current_phase?: ScenarioPhase
}

export interface Team {
  id: number
  game_id: number
  name: string
  code: string
  role: string
}

export interface JoinResponse {
  player_id: number
  team_id: number
  game_id: number
  team_role: string
  game_basic_info: {
    scenario_name: string
    game_status: string
  }
}

export interface PlayerVote {
  id: number
  player_id: number
  player_name: string
  selected_action: string
  justification?: string
  voted_at: string
}

export interface VotingStatus {
  team_id: number
  team_name: string
  total_players: number
  votes_submitted: number
  votes: PlayerVote[]
  all_voted: boolean
}

export interface PlayerState {
  current_phase?: ScenarioPhase
  phase_state: string
  phase_briefing_text?: string
  team_objective?: string
  artifacts: Artifact[]
  decision?: Decision
  game_status: string
  team_role?: string
  team_name?: string
  has_voted?: boolean
  team_voting_status?: VotingStatus
}

export interface Decision {
  id: number
  game_id: number
  team_id: number
  phase_id: number
  submitted_at: string
  actions: Record<string, any>
  free_text_justification?: string
  status: string
  score_awarded?: number
  gm_notes?: string
  team?: Team
}

export interface DecisionSubmit {
  player_id: number
  actions: Record<string, any>
  free_text_justification: string
}

export interface ScoreHistoryEntry {
  phase_name: string
  phase_order: number
  score: number
}

export interface RecentEvent {
  delta: number
  reason: string
  created_at?: string
}

export interface GlobalEvent {
  team_id: number
  team_name: string
  team_role: string
  delta: number
  reason: string
  created_at?: string
}

export interface RecentDecision {
  action?: string
  score_awarded?: number
  submitted_at?: string
}

export interface VotingStatus {
  total_players: number
  votes_submitted: number
  all_voted: boolean
}

export interface TeamScore {
  team_id: number
  team_name: string
  team_role: string
  total_score: number
  recent_events: RecentEvent[]
  score_history: ScoreHistoryEntry[]
  recent_decision?: RecentDecision
  voting_status?: VotingStatus
}

export interface Scoreboard {
  game_id: number
  scenario_name: string
  current_phase_name?: string
  phase_state: string
  teams: TeamScore[]
  recent_events: GlobalEvent[]
}

