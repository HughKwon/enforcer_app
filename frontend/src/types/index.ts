// User types
export interface User {
  id: number;
  username: string;
  email: string;
  created_at: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  user: User;
}

// Goal types
export type GoalType = 'daily' | 'weekly' | 'monthly' | 'project' | 'habit' | 'custom';

export interface Goal {
  id: number;
  title: string;
  description?: string;
  goal_type: GoalType;
  is_active: boolean;
  start_date?: string;
  end_date?: string;
  user_id: number;
  circle_id?: number;
  created_at: string;
  updated_at: string;
}

export interface CreateGoalInput {
  title: string;
  description?: string;
  goal_type: GoalType;
  is_active?: boolean;
  start_date?: string;
  end_date?: string;
  circle_id?: number;
}

// Check-in types
export interface CheckIn {
  id: number;
  content?: string;
  created_at: string;
  user_id: number;
  goal_id?: number;
  target_id?: number;
  username?: string;
  goal?: Goal;
}

export interface CreateCheckInInput {
  content?: string;
  goal_id?: number;
  target_id?: number;
}

// Circle types
export interface Circle {
  id: number;
  name: string;
  description?: string;
  created_by: number;
  created_at: string;
  updated_at: string;
}

export interface CreateCircleInput {
  name: string;
  description?: string;
}

export interface CircleMember {
  user_id: number;
  username: string;
  email: string;
  role: 'creator' | 'admin' | 'member';
  joined_at: string;
}

export interface LeaderboardEntry {
  user_id: number;
  username: string;
  total_checkins: number;
  active_goals: number;
  last_checkin?: string;
  member_since: string;
  role: 'creator' | 'admin' | 'member';
}

// Message types
export interface CircleMessage {
  id: number;
  content: string;
  user_id: number;
  username: string;
  circle_id: number;
  created_at: string;
}

// Buddy types
export interface BuddyRequest {
  id: number;
  requester_id: number;
  requester_username: string;
  receiver_id: number;
  receiver_username: string;
  message?: string;
  status: 'pending' | 'accepted' | 'declined';
  created_at: string;
}

export interface Buddy {
  user_id: number;
  username: string;
  email: string;
  buddies_since: string;
}

// Comment types
export interface Comment {
  id: number;
  content: string;
  user_id: number;
  username: string;
  check_in_id: number;
  created_at: string;
}

export interface CreateCommentInput {
  content: string;
}

// Reaction types
export interface Reaction {
  id: number;
  type: string;
  user_id: number;
  username: string;
  check_in_id?: number;
  comment_id?: number;
  created_at: string;
}

export interface CreateReactionInput {
  type: string;
}

// API error types
export interface ApiError {
  message: string;
  status?: number;
  errors?: Record<string, string[]>;
}

// Pagination types
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}

// Feed types
export interface FeedItem extends CheckIn {
  reactions?: Reaction[];
  comments?: Comment[];
  reaction_count?: number;
  comment_count?: number;
}
