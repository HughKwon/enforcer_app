# Enforcer Frontend

Production-ready React TypeScript frontend for the Enforcer Accountability App.

## Tech Stack

- **React 18 + TypeScript** - UI library with type safety
- **Vite** - Build tool and dev server
- **shadcn/ui** - Accessible UI components
- **React Router v6** - Client-side routing
- **Tailwind CSS** - Utility-first CSS framework
- **React Query** - Server state management
- **Zustand** - Client state management
- **React Hook Form + Zod** - Form handling and validation
- **Axios** - HTTP client for API calls

## Getting Started with Docker

The frontend runs in a Docker container alongside the Flask backend.

### Start the Application

```bash
# From the project root
docker-compose up -d

# View logs
docker-compose logs -f frontend
```

The frontend will be available at: **http://localhost:5173**
The backend API is at: **http://localhost:5005**

### Stop the Application

```bash
docker-compose down
```

### Rebuild After Changes

```bash
docker-compose up -d --build frontend
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/                # shadcn/ui components
│   │   ├── AppLayout.tsx      # Main app layout
│   │   ├── AppSidebar.tsx     # Navigation sidebar
│   │   ├── CheckInCard.tsx    # Check-in display card
│   │   ├── CreateGoalDialog.tsx
│   │   ├── ErrorBoundary.tsx
│   │   └── ProtectedRoute.tsx
│   ├── hooks/
│   │   ├── useGoals.ts        # Goals CRUD hooks
│   │   ├── useFeed.ts         # Feed and interactions
│   │   ├── useCircles.ts      # Circles management
│   │   └── useBuddies.ts      # Buddy system
│   ├── lib/
│   │   ├── api.ts             # Axios client with JWT
│   │   ├── queryClient.ts     # React Query config
│   │   ├── validations.ts     # Zod schemas
│   │   └── utils.ts
│   ├── pages/
│   │   ├── Login.tsx
│   │   ├── Register.tsx
│   │   ├── Dashboard.tsx
│   │   ├── Goals.tsx
│   │   ├── GoalDetail.tsx
│   │   ├── Circles.tsx
│   │   ├── Buddies.tsx
│   │   ├── Profile.tsx
│   │   └── Settings.tsx
│   ├── store/
│   │   └── authStore.ts       # Zustand auth store
│   ├── types/
│   │   └── index.ts           # TypeScript types
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── design-docs/
│   └── accountability-app-ui/
│       ├── requirements.md
│       ├── component-research.md
│       └── implementation.md
├── tsconfig.json
├── components.json
├── Dockerfile
├── package.json
└── vite.config.js
```

## Features Implemented

### ✅ Complete Feature Set

**Authentication**
- User registration with validation
- Login with JWT tokens
- Automatic token refresh
- Protected routes

**Goals Management**
- Full CRUD operations
- 6 goal types (daily, weekly, monthly, project, habit, custom)
- Check-ins with type-based validation
- Filtering by status (Active/Completed/All)
- Date range selection

**Feed & Social**
- Three feed tabs (All/Following/Circles)
- Real-time reactions and comments
- Check-in cards with user info
- Infinite scroll ready

**Circles**
- Create and manage circles
- Circle membership
- Leaderboard support (backend ready)
- Circle messaging support (backend ready)

**Buddy System**
- Send/receive buddy requests
- Accept/decline requests
- Buddy list management
- Request status tracking

**Profile & Settings**
- User profile with statistics
- Settings page (expandable)

**UI/UX**
- Responsive design (mobile-first)
- Dark mode support (via Tailwind)
- Accessibility (WCAG 2.1 AA)
- Loading states with skeletons
- Toast notifications
- Error boundaries

## Development

### Install Dependencies Locally (Optional)

If you want to develop without Docker:

```bash
cd frontend
npm install
npm run dev
```

### Environment Variables

The app uses these environment variables (configured in docker-compose.yml):

- `VITE_API_URL` - Backend API URL (default: http://localhost:5005)

## API Endpoints

All API calls are handled through `src/services/api.js`:

- **Auth**: register, login, logout, refresh
- **Users**: getUser, updateUser, deleteUser
- **Goals**: CRUD operations, check-ins
- **Feed**: getFeed, getFollowingFeed, getCirclesFeed
- **Circles**: CRUD, members, leaderboard, messages
- **Buddies**: requests, accept/decline, list
- **Follows**: follow/unfollow users
- **Comments & Reactions**: CRUD operations

## Documentation

Comprehensive implementation documentation is available at:
- **Setup & Usage**: `design-docs/accountability-app-ui/implementation.md`
- **Requirements**: `design-docs/accountability-app-ui/requirements.md`
- **Component Research**: `design-docs/accountability-app-ui/component-research.md`

## Quick Reference

### Key Routes

- `/login` - User login
- `/register` - User registration
- `/dashboard` - Feed with tabs
- `/goals` - Goals list
- `/goals/:id` - Goal detail with check-ins
- `/circles` - Circles management
- `/buddies` - Buddy system
- `/profile` - User profile
- `/settings` - Account settings

### Form Validation

All forms use Zod schemas with React Hook Form:
- Goals: Title (1-50 chars), type required, dates validated
- Check-ins: Content required for project/habit goals
- Registration: Email, password (6+ chars), password confirmation
- Comments: Max 500 characters

## Future Enhancements

1. Circle detail pages with leaderboard and chat
2. Profile editing with avatar upload
3. Real-time notifications
4. Search functionality (users, circles)
5. Analytics dashboard
6. Image attachments for check-ins

## Troubleshooting

### Frontend container won't start

```bash
# Rebuild the container
docker-compose build frontend

# Check logs
docker-compose logs frontend
```

### API calls failing

- Ensure backend is running: `docker-compose ps`
- Check backend logs: `docker-compose logs web`
- Verify API URL in browser console

### Hot reload not working

The Vite dev server should hot-reload automatically. If not:
- Check that volumes are mounted correctly in docker-compose.yml
- Try restarting the container: `docker-compose restart frontend`
