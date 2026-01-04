# Accountability App - Frontend UI Requirements

## Overview
The Enforcer App is a comprehensive accountability and goal-tracking platform with social features. Based on the backend API analysis, this document outlines all required UI components, pages, and features needed for the frontend implementation.

---

## Core Features Analysis

### 1. Authentication System
**API Endpoints:**
- `POST /register` - User registration
- `POST /login` - User login with JWT tokens
- `POST /logout` - User logout
- `POST /refresh` - Token refresh

### 2. User Management
**API Endpoints:**
- `GET /user/{user_id}` - Get user profile
- `PUT /user/{user_id}` - Update user profile
- `DELETE /user/{user_id}` - Delete user (admin only)

### 3. Goal Management
**API Endpoints:**
- `POST /goals` - Create goal
- `GET /goals` - List user's goals
- `GET /goal/{goal_id}` - Get specific goal
- `PUT /goal/{goal_id}` - Update goal
- `DELETE /goal/{goal_id}` - Delete goal
- `POST /goal/{goal_id}/check-ins` - Create check-in for goal
- `GET /goal/{goal_id}/check-ins` - List goal check-ins

**Goal Types:** daily, weekly, monthly, project, habit, custom

### 4. Target Management
**API Endpoints:**
- `POST /targets` - Create target
- `GET /target/{target_id}` - Get target
- `DELETE /target/{target_id}` - Delete target
- `POST /target/{target_id}/check-ins` - Create check-in for target
- `GET /target/{target_id}/check-ins` - List target check-ins

### 5. Check-In System
**API Endpoints:**
- `GET /check-ins/{check_in_id}` - Get check-in details
- `POST /check-ins/{check_in_id}/comments` - Add comment
- `GET /check-ins/{check_in_id}/comments` - List comments
- `POST /check-ins/{check_in_id}/reactions` - Add reaction
- `GET /check-ins/{check_in_id}/reactions` - List reactions

**Validation:** Project and habit check-ins require content

### 6. Social Features - Follow System
**API Endpoints:**
- `POST /follow/{user_id}` - Follow user
- `DELETE /follow/{user_id}` - Unfollow user
- `GET /followings` - Get users you follow
- `GET /followers` - Get your followers

### 7. Accountability Buddy System
**API Endpoints:**
- `POST /buddy/request/{user_id}` - Send buddy request
- `GET /buddy/requests/received` - Get received requests
- `GET /buddy/requests/sent` - Get sent requests
- `POST /buddy/request/{request_id}/accept` - Accept buddy request
- `POST /buddy/request/{request_id}/decline` - Decline buddy request
- `GET /buddy/list` - List all buddies
- `DELETE /buddy/{user_id}/remove` - Remove buddy

**Relationship Types:** follow, buddy (mutual)

### 8. Circle System (Groups)
**API Endpoints:**
- `POST /circle` - Create circle
- `GET /circle/{circle_id}` - Get circle details
- `PUT /circle/{circle_id}` - Update circle
- `DELETE /circle/{circle_id}` - Delete circle
- `GET /circle/{circle_id}/users` - List circle members
- `POST /circle/{circle_id}/users` - Add member to circle
- `DELETE /circle/{circle_id}/users` - Remove member from circle
- `GET /circle/{circle_id}/leaderboard` - Get circle leaderboard

**Leaderboard Data:** Total check-ins, active goals, last check-in, member since, role

### 9. Circle Messaging
**API Endpoints:**
- `GET /circle/{circle_id}/message` - Get circle messages
- `POST /circle/{circle_id}/message` - Send message to circle

### 10. Feed System
**API Endpoints:**
- `GET /feed` - Personalized feed (following + circles + self)
- `GET /feed/following` - Feed from followed users only
- `GET /feed/circles` - Feed from circle members only

### 11. Comments & Reactions
**API Endpoints:**
- `DELETE /comments/{comment_id}` - Delete comment
- `POST /comments/{comment_id}/reactions` - React to comment
- `PUT /reactions/{reaction_id}` - Update reaction
- `DELETE /reactions/{reaction_id}` - Delete reaction

---

## Component Requirements

### Core UI Components (shadcn/ui)

#### 1. Forms & Inputs
- **@shadcn/form** - Form wrapper with validation
- **@shadcn/input** - Text input fields
- **@shadcn/textarea** - Multi-line text input
- **@shadcn/select** - Dropdown selection
- **@shadcn/button** - Action buttons
- **@shadcn/calendar** - Date selection for goals
- **@shadcn/input-otp** - OTP verification (if 2FA added)

#### 2. Layout & Navigation
- **@shadcn/card** - Content containers
- **@shadcn/tabs** - Tab navigation
- **@shadcn/separator** - Visual dividers
- **@shadcn/sidebar** - Main navigation sidebar
- **@shadcn/dropdown-menu** - Contextual menus

#### 3. Data Display
- **@shadcn/table** - Data tables (leaderboard, lists)
- **@shadcn/badge** - Status indicators (goal types, roles)
- **@shadcn/avatar** - User avatars
- **@shadcn/skeleton** - Loading states

#### 4. Overlays & Dialogs
- **@shadcn/dialog** - Modal dialogs
- **@shadcn/alert-dialog** - Confirmation dialogs
- **@shadcn/sheet** - Slide-out panels
- **@shadcn/popover** - Contextual popovers
- **@shadcn/hover-card** - Hover information

#### 5. Feedback
- **@shadcn/toast** - Notifications
- **@shadcn/progress** - Progress indicators
- **@shadcn/spinner** - Loading spinners

---

## Page Requirements & Component Hierarchy

### 1. Authentication Pages

#### Login Page (`/login`)
```
LoginPage
├── Card
│   ├── Form
│   │   ├── Input (username)
│   │   ├── Input (password)
│   │   └── Button (submit)
│   └── Link (to register)
└── Toast (error/success notifications)
```

**Reference Block:** `@shadcn/login-01` or `@shadcn/login-04`

#### Register Page (`/register`)
```
RegisterPage
├── Card
│   ├── Form
│   │   ├── Input (username)
│   │   ├── Input (email)
│   │   ├── Input (password)
│   │   ├── Input (confirm password)
│   │   └── Button (submit)
│   └── Link (to login)
└── Toast (error/success notifications)
```

**Reference Block:** `@shadcn/signup-01` or `@shadcn/signup-04`

---

### 2. Dashboard / Home Page (`/dashboard`)

```
DashboardPage
├── Sidebar
│   ├── Navigation Links
│   │   ├── Feed
│   │   ├── My Goals
│   │   ├── Circles
│   │   ├── Buddies
│   │   └── Profile
│   └── User Menu (Dropdown)
├── MainContent
│   ├── Tabs
│   │   ├── All Feed
│   │   ├── Following
│   │   └── Circles
│   └── FeedList
│       └── CheckInCard[] (multiple cards)
│           ├── Avatar
│           ├── User Info
│           ├── Goal/Target Info
│           ├── Check-in Content
│           ├── Timestamp
│           ├── Reactions Display
│           ├── Comments Section
│           │   └── CommentList[]
│           └── Actions
│               ├── Button (React)
│               └── Button (Comment)
└── Toast (notifications)
```

**Components:**
- Sidebar navigation with collapsible sections
- Tabs for feed filtering
- Card components for check-ins
- Avatar for user display
- Badge for goal types
- Button for interactions
- Dialog for adding reactions/comments

---

### 3. Goals Page (`/goals`)

```
GoalsPage
├── Header
│   ├── Title
│   └── Button (Create Goal)
├── Tabs
│   ├── Active Goals
│   ├── Completed Goals
│   └── All Goals
├── GoalsList
│   └── GoalCard[]
│       ├── Badge (goal type)
│       ├── Title & Description
│       ├── Progress Indicator
│       ├── Circle Badge (if in circle)
│       ├── Date Range
│       ├── Check-in Count
│       └── Actions Dropdown
│           ├── View Details
│           ├── Check In
│           ├── Edit
│           └── Delete (Alert Dialog)
└── CreateGoalDialog
    ├── Form
    │   ├── Input (title)
    │   ├── Textarea (description)
    │   ├── Select (goal type)
    │   ├── Select (circle - optional)
    │   ├── Calendar (start date)
    │   ├── Calendar (end date)
    │   └── Switch (is active)
    └── Button (Submit)
```

**Components:**
- Card for each goal
- Badge for goal type indicators
- Select for goal type (daily, weekly, monthly, project, habit, custom)
- Dialog for goal creation/editing
- Calendar for date selection
- Alert Dialog for delete confirmation
- Progress component for goal progress

---

### 4. Goal Detail Page (`/goals/{id}`)

```
GoalDetailPage
├── Header
│   ├── Back Button
│   ├── Goal Title
│   └── Actions Dropdown
│       ├── Edit
│       └── Delete
├── GoalInfo Card
│   ├── Badge (type)
│   ├── Description
│   ├── Circle Info (if applicable)
│   ├── Date Range
│   └── Status Badge
├── CheckInSection
│   ├── Button (Create Check-in)
│   └── CheckInList
│       └── CheckInCard[]
│           ├── Timestamp
│           ├── Content
│           ├── Reactions
│           ├── Comments
│           └── Dropdown Actions
├── CreateCheckInDialog
│   ├── Form
│   │   ├── Textarea (content - required for project/habit)
│   │   └── Button (Submit)
│   └── Toast (validation errors)
└── Statistics Card
    ├── Total Check-ins
    ├── Current Streak
    └── Last Check-in
```

**Components:**
- Card for goal info and statistics
- Badge for status/type
- Dialog for check-in creation
- Textarea for check-in content
- Alert for validation (project/habit require content)

---

### 5. Circles Page (`/circles`)

```
CirclesPage
├── Header
│   ├── Title
│   └── Button (Create Circle)
├── MyCircles Section
│   └── CircleCard[]
│       ├── Circle Name
│       ├── Description
│       ├── Member Count Badge
│       ├── Role Badge
│       └── Button (View Circle)
└── CreateCircleDialog
    ├── Form
    │   ├── Input (name)
    │   └── Textarea (description)
    └── Button (Submit)
```

**Components:**
- Card for each circle
- Badge for member count and role
- Dialog for circle creation

---

### 6. Circle Detail Page (`/circles/{id}`)

```
CircleDetailPage
├── Header
│   ├── Back Button
│   ├── Circle Name
│   └── Actions Dropdown (if creator)
│       ├── Edit
│       ├── Add Members
│       └── Delete Circle
├── Tabs
│   ├── Overview
│   ├── Leaderboard
│   ├── Members
│   └── Chat
├── OverviewTab
│   ├── Card (Circle Info)
│   ├── Card (Recent Activity)
│   └── Card (Quick Stats)
├── LeaderboardTab
│   └── Table
│       ├── Rank Column
│       ├── Avatar + Username
│       ├── Total Check-ins
│       ├── Active Goals
│       ├── Last Check-in
│       └── Role Badge
├── MembersTab
│   ├── Button (Add Member)
│   └── Table/List
│       └── MemberRow[]
│           ├── Avatar
│           ├── Username
│           ├── Role Badge
│           ├── Joined Date
│           └── Actions (if admin)
│               └── Remove (Alert Dialog)
└── ChatTab
    ├── MessageList
    │   └── MessageCard[]
    │       ├── Avatar
    │       ├── Username
    │       ├── Message
    │       └── Timestamp
    └── MessageInput
        ├── Textarea
        └── Button (Send)
```

**Components:**
- Tabs for different views
- Table for leaderboard
- Avatar for member display
- Badge for roles and stats
- Dialog for adding members
- Alert Dialog for removing members
- Card for messages

---

### 7. Buddies Page (`/buddies`)

```
BuddiesPage
├── Header
│   ├── Title
│   └── Button (Send Request)
├── Tabs
│   ├── My Buddies
│   ├── Requests Received
│   └── Requests Sent
├── MyBuddiesTab
│   └── BuddyCard[]
│       ├── Avatar
│       ├── Username
│       ├── Buddies Since
│       ├── Recent Activity Badge
│       └── Actions Dropdown
│           ├── View Profile
│           └── Remove Buddy (Alert Dialog)
├── RequestsReceivedTab
│   └── RequestCard[]
│       ├── Avatar
│       ├── Username
│       ├── Message
│       ├── Timestamp
│       └── Actions
│           ├── Button (Accept)
│           └── Button (Decline)
└── RequestsSentTab
    └── RequestCard[]
        ├── Avatar
        ├── Username
        ├── Message
        ├── Status Badge (pending)
        └── Timestamp
```

**Components:**
- Tabs for different request views
- Card for buddy display
- Badge for status
- Avatar for user display
- Alert Dialog for buddy removal
- Dialog for sending requests

---

### 8. User Profile Page (`/profile/{id}`)

```
ProfilePage
├── Header
│   ├── Avatar (large)
│   ├── Username
│   ├── Email
│   └── Actions (if own profile)
│       └── Button (Edit Profile)
├── Stats Cards
│   ├── Card (Total Goals)
│   ├── Card (Total Check-ins)
│   ├── Card (Circles)
│   └── Card (Buddies)
├── Tabs
│   ├── Goals
│   ├── Recent Activity
│   └── Circles
├── GoalsTab
│   └── GoalCard[] (view-only)
├── RecentActivityTab
│   └── CheckInCard[] (recent check-ins)
└── CirclesTab
    └── CircleCard[] (shared circles)
```

**Components:**
- Avatar (large version)
- Card for stats display
- Tabs for profile sections
- Badge for metrics

---

### 9. Settings Page (`/settings`)

```
SettingsPage
├── Sidebar (Settings Navigation)
│   ├── Profile
│   ├── Security
│   ├── Notifications
│   └── Privacy
├── ProfileTab
│   └── Form
│       ├── Input (username)
│       ├── Input (email)
│       └── Button (Save)
├── SecurityTab
│   └── Form
│       ├── Input (current password)
│       ├── Input (new password)
│       ├── Input (confirm password)
│       └── Button (Update Password)
└── NotificationsTab
    └── Form (switches for preferences)
```

**Components:**
- Sidebar for settings navigation
- Form components with validation
- Switch for toggles
- Button for actions

---

## Data Flow Patterns

### State Management
- **User Authentication State:** JWT tokens, user info
- **Global State:** Current user, navigation
- **Feature State:** Goals, circles, buddies, feed data
- **UI State:** Modals, toasts, loading states

### API Integration Patterns
```
Component
  ├── React Query / SWR (data fetching)
  ├── Axios / Fetch (API calls)
  ├── JWT Token Management
  └── Error Handling
```

### Real-time Features (Future Enhancement)
- Circle chat messages (WebSocket/Socket.io)
- Live feed updates
- Real-time notifications

---

## Validation Rules

### Goal Creation
- Title: Required, max 50 characters
- Description: Optional, max 256 characters
- Goal Type: Required, must be one of: daily, weekly, monthly, project, habit, custom
- Start/End Date: Optional, end must be after start
- Circle: Optional

### Check-in Creation
- **Project Goals:** Content required (progress description)
- **Habit Goals:** Content required (progress description)
- **Daily/Weekly Goals:** Content optional (simple check-in allowed)

### Circle Management
- Name: Required, max length
- Description: Optional
- Member must not already exist in circle
- User must be member to view chat/leaderboard

### Buddy Requests
- Cannot send to self
- Cannot send duplicate pending requests
- Cannot be already buddies
- Message: Optional

---

## Accessibility Requirements

### WCAG 2.1 Level AA Compliance
- Semantic HTML structure
- Keyboard navigation support
- ARIA labels for interactive elements
- Focus visible indicators
- Color contrast ratios (4.5:1 for normal text)
- Screen reader compatibility

### Specific Considerations
- Form validation with clear error messages
- Loading states with appropriate announcements
- Modal dialogs with proper focus management
- Table navigation for leaderboards
- Alternative text for avatars
- Accessible date pickers

---

## Component Dependencies

### Installation Order
1. **Core Components:**
   ```bash
   npx shadcn@latest add button input textarea form select
   ```

2. **Layout Components:**
   ```bash
   npx shadcn@latest add card tabs separator sidebar dropdown-menu
   ```

3. **Data Display:**
   ```bash
   npx shadcn@latest add table badge avatar skeleton
   ```

4. **Overlays:**
   ```bash
   npx shadcn@latest add dialog alert-dialog sheet popover hover-card
   ```

5. **Feedback:**
   ```bash
   npx shadcn@latest add toast progress
   ```

6. **Date Selection:**
   ```bash
   npx shadcn@latest add calendar
   ```

### Suggested Blocks
- **Login/Register:** `npx shadcn@latest add @shadcn/login-01 @shadcn/signup-01`
- **Dashboard:** `npx shadcn@latest add @shadcn/dashboard-01`
- **Sidebar Navigation:** `npx shadcn@latest add @shadcn/sidebar-01`

---

## Routing Structure

```
/
├── /login
├── /register
├── /dashboard (protected)
├── /goals (protected)
│   └── /goals/:id
├── /circles (protected)
│   └── /circles/:id
├── /buddies (protected)
├── /profile/:id (protected)
├── /settings (protected)
└── /404
```

### Protected Route Requirements
- JWT token verification
- Redirect to /login if unauthenticated
- Token refresh on expiry
- Logout on 401 responses

---

## Performance Considerations

### Optimization Strategies
- Lazy loading for routes
- Pagination for feeds (50 items limit)
- Infinite scroll for feed
- Debounced search inputs
- Optimistic UI updates
- Image optimization for avatars
- Skeleton loading states

### Caching Strategy
- React Query for server state
- localStorage for JWT tokens
- Session storage for form drafts
- Cache invalidation on mutations

---

## Error Handling

### API Error Responses
- 400: Bad Request → Form validation errors
- 401: Unauthorized → Redirect to login
- 403: Forbidden → Show permission error
- 404: Not Found → Show not found message
- 409: Conflict → Show conflict message (duplicate username)
- 500: Server Error → Show generic error message

### User Feedback
- Toast notifications for success/errors
- Inline form validation
- Loading spinners during API calls
- Error boundaries for component crashes
- Retry mechanisms for failed requests

---

## Testing Requirements

### Component Testing
- Form validation
- Button interactions
- Modal open/close
- Data rendering
- Error states

### Integration Testing
- API integration
- Authentication flow
- CRUD operations
- Navigation

### E2E Testing
- User registration/login
- Goal creation and check-in
- Circle creation and management
- Buddy request flow
- Feed interaction

---

## Future Enhancements

### Potential Features
- Push notifications
- Mobile responsive design refinements
- Progressive Web App (PWA)
- Offline support
- File attachments for check-ins
- Photo uploads for check-ins
- Advanced goal analytics
- Streak tracking
- Reminder system
- Email notifications
- Social sharing
- Gamification (achievements, levels)

---

## Development Priorities

### Phase 1: Core Features (MVP)
1. Authentication (login, register, logout)
2. Goal creation and management
3. Check-in system
4. Basic feed display
5. User profiles

### Phase 2: Social Features
1. Follow system
2. Circle creation and management
3. Circle leaderboard
4. Buddy request system
5. Circle messaging

### Phase 3: Enhanced UX
1. Advanced filtering and search
2. Notifications system
3. User settings
4. Profile customization
5. Statistics and analytics

### Phase 4: Polish
1. Accessibility improvements
2. Performance optimization
3. Mobile responsiveness
4. Error handling refinement
5. User onboarding

---

## Technical Stack Recommendations

### Frontend Framework
- **React 18+** with TypeScript
- **Vite** for build tooling
- **React Router v6** for routing

### State Management
- **React Query / TanStack Query** for server state
- **Zustand** or **Context API** for client state

### Form Management
- **React Hook Form** with Zod validation
- Integration with shadcn/ui form components

### HTTP Client
- **Axios** with interceptors for JWT
- Base URL configuration

### Styling
- **Tailwind CSS** (required for shadcn/ui)
- **CSS Modules** for component-specific styles

---

## File Structure Recommendation

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/              # shadcn/ui components
│   │   ├── auth/            # Auth-related components
│   │   ├── goals/           # Goal components
│   │   ├── circles/         # Circle components
│   │   ├── feed/            # Feed components
│   │   ├── buddies/         # Buddy components
│   │   └── common/          # Shared components
│   ├── pages/
│   │   ├── Login.tsx
│   │   ├── Register.tsx
│   │   ├── Dashboard.tsx
│   │   ├── Goals.tsx
│   │   ├── GoalDetail.tsx
│   │   ├── Circles.tsx
│   │   ├── CircleDetail.tsx
│   │   ├── Buddies.tsx
│   │   ├── Profile.tsx
│   │   └── Settings.tsx
│   ├── hooks/               # Custom hooks
│   ├── lib/
│   │   ├── api.ts           # API client setup
│   │   └── utils.ts         # Utility functions
│   ├── types/               # TypeScript types
│   ├── store/               # State management
│   └── App.tsx
├── public/
└── package.json
```

---

## Summary

This Accountability App requires a comprehensive UI implementation with:

- **10+ Pages:** Authentication, dashboard, goals, circles, buddies, profiles, settings
- **20+ shadcn/ui Components:** Forms, cards, tables, dialogs, navigation
- **11 Major Feature Areas:** Auth, goals, targets, check-ins, follow, buddy, circles, messaging, feed, comments, reactions
- **Robust Validation:** Type-specific rules for goals and check-ins
- **Social Features:** Follow system, accountability buddies, group circles
- **Real-time Capabilities:** Feed updates, circle chat
- **Accessibility:** WCAG 2.1 Level AA compliance throughout

The implementation should prioritize user experience, performance, and maintainability while building a cohesive accountability platform that motivates users to achieve their goals through social support and tracking.
