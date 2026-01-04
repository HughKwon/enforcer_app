# Accountability App - shadcn/ui Component Research

## Overview
This document provides comprehensive research on all shadcn/ui components required for the Accountability App frontend implementation. Each component includes installation commands, API documentation, usage examples, and integration notes.

---

## Table of Contents
1. [Installation Commands](#installation-commands)
2. [Forms & Inputs](#forms--inputs)
3. [Layout & Navigation](#layout--navigation)
4. [Data Display](#data-display)
5. [Overlays & Dialogs](#overlays--dialogs)
6. [Feedback Components](#feedback-components)
7. [Pre-built Blocks](#pre-built-blocks)
8. [Best Practices](#best-practices)
9. [Component Dependencies](#component-dependencies)

---

## Installation Commands

### Install All Core Components (Single Command)
```bash
npx shadcn@latest add @shadcn/form @shadcn/input @shadcn/textarea @shadcn/select @shadcn/button @shadcn/calendar @shadcn/input-otp @shadcn/card @shadcn/tabs @shadcn/separator @shadcn/sidebar @shadcn/dropdown-menu @shadcn/table @shadcn/badge @shadcn/avatar @shadcn/skeleton @shadcn/dialog @shadcn/alert-dialog @shadcn/sheet @shadcn/popover @shadcn/hover-card @shadcn/sonner @shadcn/progress @shadcn/spinner
```

### Install Pre-built Blocks (Recommended for Faster Development)
```bash
npx shadcn@latest add @shadcn/login-01 @shadcn/login-04 @shadcn/signup-01 @shadcn/signup-04 @shadcn/dashboard-01 @shadcn/sidebar-01
```

### Category-Based Installation

#### 1. Forms & Inputs
```bash
npx shadcn@latest add @shadcn/form @shadcn/input @shadcn/textarea @shadcn/select @shadcn/button @shadcn/calendar @shadcn/input-otp
```

#### 2. Layout & Navigation
```bash
npx shadcn@latest add @shadcn/card @shadcn/tabs @shadcn/separator @shadcn/sidebar @shadcn/dropdown-menu
```

#### 3. Data Display
```bash
npx shadcn@latest add @shadcn/table @shadcn/badge @shadcn/avatar @shadcn/skeleton
```

#### 4. Overlays & Dialogs
```bash
npx shadcn@latest add @shadcn/dialog @shadcn/alert-dialog @shadcn/sheet @shadcn/popover @shadcn/hover-card
```

#### 5. Feedback
```bash
npx shadcn@latest add @shadcn/sonner @shadcn/progress @shadcn/spinner
```

---

## Forms & Inputs

### 1. Form Component

**Type:** registry:ui
**Dependencies:**
- `@radix-ui/react-label`
- `@radix-ui/react-slot`
- `@hookform/resolvers`
- `zod`
- `react-hook-form`

**Description:**
A comprehensive form wrapper with built-in validation support using React Hook Form and Zod. Essential for all form-based interactions in the accountability app.

**Key Features:**
- Integrated validation with Zod schemas
- Support for React Hook Form and TanStack Form
- Accessible form controls with ARIA labels
- Error handling and display
- Field grouping and layouts

**Usage Example (React Hook Form):**
```tsx
"use client"

import * as React from "react"
import { zodResolver } from "@hookform/resolvers/zod"
import { Controller, useForm } from "react-hook-form"
import { toast } from "sonner"
import * as z from "zod"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Field, FieldError, FieldGroup, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"

const formSchema = z.object({
  title: z.string().min(5, "Title must be at least 5 characters.").max(50),
  description: z.string().min(20).max(256),
})

export default function GoalForm() {
  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: { title: "", description: "" },
  })

  function onSubmit(data: z.infer<typeof formSchema>) {
    toast.success("Goal created successfully!")
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Create Goal</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={form.handleSubmit(onSubmit)}>
          <FieldGroup>
            <Controller
              name="title"
              control={form.control}
              render={({ field, fieldState }) => (
                <Field data-invalid={fieldState.invalid}>
                  <FieldLabel>Goal Title</FieldLabel>
                  <Input {...field} placeholder="Run 5k every morning" />
                  {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
                </Field>
              )}
            />
          </FieldGroup>
        </form>
      </CardContent>
      <CardFooter>
        <Button type="submit">Create Goal</Button>
      </CardFooter>
    </Card>
  )
}
```

**Use Cases in Accountability App:**
- Login/Register forms
- Goal creation and editing
- Check-in submission forms
- Circle creation forms
- Buddy request forms
- User profile settings

**Validation Patterns:**
```tsx
// Goal validation schema
const goalSchema = z.object({
  title: z.string().min(1, "Required").max(50),
  description: z.string().max(256).optional(),
  goalType: z.enum(["daily", "weekly", "monthly", "project", "habit", "custom"]),
  startDate: z.date().optional(),
  endDate: z.date().optional(),
  circleId: z.string().optional(),
})

// Check-in validation (project/habit require content)
const checkInSchema = z.object({
  content: z.string().min(1, "Content required for project/habit goals"),
  goalId: z.string(),
})
```

---

### 2. Input Component

**Type:** registry:ui
**Dependencies:** None (pure component)

**Description:**
A styled text input component that extends native HTML input with consistent theming.

**Key Props:**
- `type`: text, email, password, number, etc.
- `placeholder`: Placeholder text
- `disabled`: Disable input
- `aria-invalid`: Accessibility for validation states

**Usage Example:**
```tsx
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

<div className="grid gap-2">
  <Label htmlFor="email">Email</Label>
  <Input
    id="email"
    type="email"
    placeholder="user@example.com"
    required
  />
</div>
```

**Use Cases:**
- Username/email input (login/register)
- Goal title input
- Search functionality
- Circle name input
- Comment input fields

---

### 3. Textarea Component

**Type:** registry:ui
**Dependencies:** None

**Description:**
Multi-line text input for longer content.

**Usage Example:**
```tsx
import { Textarea } from "@/components/ui/textarea"

<Textarea
  placeholder="Describe your goal..."
  rows={4}
  maxLength={256}
/>
```

**Use Cases:**
- Goal descriptions
- Check-in content (required for project/habit goals)
- Circle descriptions
- Comments on check-ins
- Buddy request messages

---

### 4. Select Component

**Type:** registry:ui
**Dependencies:** `@radix-ui/react-select`

**Description:**
Dropdown selection component with keyboard navigation and accessibility features.

**Usage Example:**
```tsx
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

export default function GoalTypeSelect() {
  return (
    <Select>
      <SelectTrigger className="w-[180px]">
        <SelectValue placeholder="Select goal type" />
      </SelectTrigger>
      <SelectContent>
        <SelectGroup>
          <SelectLabel>Goal Types</SelectLabel>
          <SelectItem value="daily">Daily</SelectItem>
          <SelectItem value="weekly">Weekly</SelectItem>
          <SelectItem value="monthly">Monthly</SelectItem>
          <SelectItem value="project">Project</SelectItem>
          <SelectItem value="habit">Habit</SelectItem>
          <SelectItem value="custom">Custom</SelectItem>
        </SelectGroup>
      </SelectContent>
    </Select>
  )
}
```

**Use Cases:**
- Goal type selection (daily, weekly, monthly, project, habit, custom)
- Circle selection when creating goals
- Filter selections in feeds
- Role assignment in circles

---

### 5. Button Component

**Type:** registry:ui
**Dependencies:** `@radix-ui/react-slot`

**Description:**
Versatile button component with multiple variants and sizes.

**Variants:**
- `default`: Primary action button
- `destructive`: Delete/remove actions
- `outline`: Secondary actions
- `secondary`: Alternative styling
- `ghost`: Minimal styling
- `link`: Link-styled button

**Sizes:**
- `default`: Standard size
- `sm`: Small button
- `lg`: Large button
- `icon`: Icon-only button

**Usage Example:**
```tsx
import { Button } from "@/components/ui/button"

<div className="flex gap-2">
  <Button>Create Goal</Button>
  <Button variant="outline">Cancel</Button>
  <Button variant="destructive">Delete</Button>
  <Button variant="ghost" size="icon">
    <MoreHorizontal />
  </Button>
</div>
```

**Use Cases:**
- Form submissions
- Action triggers (Create Goal, Check In, Send Request)
- Navigation actions
- Delete confirmations
- Icon buttons for menus and actions

---

### 6. Calendar Component

**Type:** registry:ui
**Dependencies:**
- `react-day-picker@latest`
- `date-fns`

**Description:**
Date picker component for selecting dates with range support.

**Usage Example:**
```tsx
"use client"

import * as React from "react"
import { Calendar } from "@/components/ui/calendar"

export default function DatePicker() {
  const [date, setDate] = React.useState<Date | undefined>(new Date())

  return (
    <Calendar
      mode="single"
      selected={date}
      onSelect={setDate}
      className="rounded-md border shadow-sm"
      captionLayout="dropdown"
    />
  )
}
```

**Use Cases:**
- Goal start/end date selection
- Date range filtering in feeds
- Check-in date selection
- Statistics date range picker

**Date Range Example:**
```tsx
const [dateRange, setDateRange] = React.useState<DateRange | undefined>({
  from: new Date(),
  to: addDays(new Date(), 30),
})

<Calendar
  mode="range"
  selected={dateRange}
  onSelect={setDateRange}
/>
```

---

### 7. Input OTP Component

**Type:** registry:ui
**Dependencies:** `input-otp`

**Description:**
One-time password input for 2FA verification (future enhancement).

**Usage Example:**
```tsx
import { InputOTP, InputOTPGroup, InputOTPSlot } from "@/components/ui/input-otp"

<InputOTP maxLength={6}>
  <InputOTPGroup>
    <InputOTPSlot index={0} />
    <InputOTPSlot index={1} />
    <InputOTPSlot index={2} />
    <InputOTPSlot index={3} />
    <InputOTPSlot index={4} />
    <InputOTPSlot index={5} />
  </InputOTPGroup>
</InputOTP>
```

**Use Cases:**
- Two-factor authentication (future feature)
- Email verification codes
- Security confirmations

---

## Layout & Navigation

### 1. Card Component

**Type:** registry:ui
**Dependencies:** None

**Description:**
Versatile container component for grouping related content.

**Components:**
- `Card`: Main container
- `CardHeader`: Top section for titles/descriptions
- `CardTitle`: Card heading
- `CardDescription`: Subtitle/description
- `CardContent`: Main content area
- `CardFooter`: Bottom section for actions
- `CardAction`: Action buttons in header

**Usage Example:**
```tsx
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Button } from "@/components/ui/button"

export default function GoalCard() {
  return (
    <Card className="w-full max-w-sm">
      <CardHeader>
        <CardTitle>Morning Run Goal</CardTitle>
        <CardDescription>Daily goal - 30 days streak</CardDescription>
        <CardAction>
          <Button variant="link">Edit</Button>
        </CardAction>
      </CardHeader>
      <CardContent>
        <p>Run 5k every morning before 8 AM</p>
      </CardContent>
      <CardFooter className="flex gap-2">
        <Button>Check In</Button>
        <Button variant="outline">View Details</Button>
      </CardFooter>
    </Card>
  )
}
```

**Use Cases:**
- Goal cards in goal list
- Check-in cards in feed
- Circle cards
- Buddy cards
- Statistics cards on dashboard
- User profile cards

---

### 2. Tabs Component

**Type:** registry:ui
**Dependencies:** `@radix-ui/react-tabs`

**Description:**
Tabbed navigation for organizing related content sections.

**Components:**
- `Tabs`: Container with state management
- `TabsList`: Tab header container
- `TabsTrigger`: Individual tab button
- `TabsContent`: Content panel for each tab

**Usage Example:**
```tsx
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function FeedTabs() {
  return (
    <Tabs defaultValue="all">
      <TabsList>
        <TabsTrigger value="all">All Feed</TabsTrigger>
        <TabsTrigger value="following">Following</TabsTrigger>
        <TabsTrigger value="circles">Circles</TabsTrigger>
      </TabsList>
      <TabsContent value="all">
        <Card>
          <CardHeader>
            <CardTitle>All Activity</CardTitle>
          </CardHeader>
          <CardContent>
            {/* Feed items */}
          </CardContent>
        </Card>
      </TabsContent>
      <TabsContent value="following">
        {/* Following feed */}
      </TabsContent>
      <TabsContent value="circles">
        {/* Circles feed */}
      </TabsContent>
    </Tabs>
  )
}
```

**Use Cases:**
- Feed filtering (All/Following/Circles)
- Goal views (Active/Completed/All)
- Circle detail sections (Overview/Leaderboard/Members/Chat)
- Buddy requests (My Buddies/Received/Sent)
- Profile sections (Goals/Activity/Circles)
- Settings navigation

---

### 3. Separator Component

**Type:** registry:ui
**Dependencies:** `@radix-ui/react-separator`

**Description:**
Visual divider for separating content sections.

**Usage Example:**
```tsx
import { Separator } from "@/components/ui/separator"

<div>
  <h3>Active Goals</h3>
  <Separator className="my-4" />
  <div>{/* Goal list */}</div>
</div>
```

**Use Cases:**
- Separating sections in sidebar
- Dividing content in cards
- Between items in dropdown menus
- Between feed items

---

### 4. Sidebar Component

**Type:** registry:ui
**Dependencies:**
- `@radix-ui/react-slot`
- `class-variance-authority`
- `lucide-react`

**Description:**
Full-featured sidebar navigation with collapsible sections and responsive behavior.

**Key Features:**
- Collapsible navigation
- Grouped sections
- Icon support
- Active state indicators
- Responsive design

**Usage Example:**
```tsx
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"
import { Home, Target, Users, UserCircle, Settings } from "lucide-react"

export default function AppSidebar() {
  return (
    <Sidebar>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Main</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <a href="/dashboard">
                    <Home />
                    <span>Feed</span>
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <a href="/goals">
                    <Target />
                    <span>My Goals</span>
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <a href="/circles">
                    <Users />
                    <span>Circles</span>
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
        <SidebarGroup>
          <SidebarGroupLabel>Account</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <a href="/profile">
                    <UserCircle />
                    <span>Profile</span>
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <a href="/settings">
                    <Settings />
                    <span>Settings</span>
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  )
}
```

**Use Cases:**
- Main app navigation
- Settings navigation
- Dashboard layout

---

### 5. Dropdown Menu Component

**Type:** registry:ui
**Dependencies:** `@radix-ui/react-dropdown-menu`

**Description:**
Context menu for actions and options.

**Components:**
- `DropdownMenu`: Container
- `DropdownMenuTrigger`: Trigger button
- `DropdownMenuContent`: Menu panel
- `DropdownMenuItem`: Menu item
- `DropdownMenuSeparator`: Divider
- `DropdownMenuLabel`: Section label
- `DropdownMenuCheckboxItem`: Checkbox item
- `DropdownMenuRadioGroup`: Radio group

**Usage Example:**
```tsx
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Button } from "@/components/ui/button"
import { MoreHorizontal } from "lucide-react"

export default function GoalActions() {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon">
          <MoreHorizontal />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuLabel>Actions</DropdownMenuLabel>
        <DropdownMenuItem>View Details</DropdownMenuItem>
        <DropdownMenuItem>Check In</DropdownMenuItem>
        <DropdownMenuItem>Edit Goal</DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem className="text-destructive">
          Delete Goal
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
```

**Use Cases:**
- Goal action menus
- User menus
- Circle member actions
- Check-in actions
- Table row actions

---

## Data Display

### 1. Table Component

**Type:** registry:ui
**Dependencies:** None (can be enhanced with `@tanstack/react-table`)

**Description:**
Semantic HTML table with consistent styling. Can be integrated with TanStack Table for advanced features.

**Components:**
- `Table`: Main container
- `TableHeader`: Header section
- `TableBody`: Body section
- `TableFooter`: Footer section
- `TableRow`: Table row
- `TableHead`: Header cell
- `TableCell`: Data cell
- `TableCaption`: Table caption

**Basic Usage:**
```tsx
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

const leaderboard = [
  { rank: 1, username: "alice", checkIns: 45, activeGoals: 5 },
  { rank: 2, username: "bob", checkIns: 38, activeGoals: 4 },
  { rank: 3, username: "charlie", checkIns: 32, activeGoals: 6 },
]

export default function CircleLeaderboard() {
  return (
    <Table>
      <TableCaption>Circle Leaderboard - Last 30 Days</TableCaption>
      <TableHeader>
        <TableRow>
          <TableHead className="w-[100px]">Rank</TableHead>
          <TableHead>Username</TableHead>
          <TableHead>Check-ins</TableHead>
          <TableHead>Active Goals</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {leaderboard.map((member) => (
          <TableRow key={member.rank}>
            <TableCell className="font-medium">{member.rank}</TableCell>
            <TableCell>{member.username}</TableCell>
            <TableCell>{member.checkIns}</TableCell>
            <TableCell>{member.activeGoals}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

**Advanced Usage with TanStack Table:**
```tsx
"use client"

import * as React from "react"
import {
  flexRender,
  getCoreRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
  type ColumnDef,
} from "@tanstack/react-table"
import { ArrowUpDown } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

type LeaderboardEntry = {
  rank: number
  username: string
  checkIns: number
  activeGoals: number
}

const columns: ColumnDef<LeaderboardEntry>[] = [
  {
    accessorKey: "rank",
    header: "Rank",
  },
  {
    accessorKey: "username",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Username
          <ArrowUpDown />
        </Button>
      )
    },
  },
  {
    accessorKey: "checkIns",
    header: "Check-ins",
  },
  {
    accessorKey: "activeGoals",
    header: "Active Goals",
  },
]

export default function LeaderboardTable({ data }: { data: LeaderboardEntry[] }) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
  })

  return (
    <div className="w-full">
      <div className="overflow-hidden rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <TableHead key={header.id}>
                    {flexRender(header.column.columnDef.header, header.getContext())}
                  </TableHead>
                ))}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow key={row.id}>
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={columns.length} className="h-24 text-center">
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      <div className="flex items-center justify-end space-x-2 py-4">
        <Button
          variant="outline"
          size="sm"
          onClick={() => table.previousPage()}
          disabled={!table.getCanPreviousPage()}
        >
          Previous
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => table.nextPage()}
          disabled={!table.getCanNextPage()}
        >
          Next
        </Button>
      </div>
    </div>
  )
}
```

**Use Cases:**
- Circle leaderboards
- Member lists
- Goal lists (alternative to cards)
- Check-in history tables

---

### 2. Badge Component

**Type:** registry:ui
**Dependencies:** `@radix-ui/react-slot`

**Description:**
Small status indicators and labels.

**Variants:**
- `default`: Primary badge
- `secondary`: Secondary styling
- `destructive`: Error/warning state
- `outline`: Outlined badge

**Usage Example:**
```tsx
import { Badge } from "@/components/ui/badge"
import { BadgeCheckIcon } from "lucide-react"

export default function GoalBadges() {
  return (
    <div className="flex gap-2">
      <Badge>Daily</Badge>
      <Badge variant="secondary">Active</Badge>
      <Badge variant="outline">Circle</Badge>
      <Badge variant="destructive">Overdue</Badge>

      {/* Icon badges */}
      <Badge variant="secondary" className="bg-blue-500 text-white">
        <BadgeCheckIcon />
        Verified
      </Badge>

      {/* Count badges */}
      <Badge className="h-5 min-w-5 rounded-full px-1 font-mono tabular-nums">
        8
      </Badge>
    </div>
  )
}
```

**Use Cases:**
- Goal type indicators (daily, weekly, monthly, project, habit, custom)
- Status indicators (active, completed, paused)
- Role badges (creator, admin, member)
- Notification counts
- Circle membership indicators
- Check-in counts

**Styling for Goal Types:**
```tsx
function GoalTypeBadge({ type }: { type: string }) {
  const variants = {
    daily: "bg-blue-500 text-white",
    weekly: "bg-green-500 text-white",
    monthly: "bg-purple-500 text-white",
    project: "bg-orange-500 text-white",
    habit: "bg-pink-500 text-white",
    custom: "bg-gray-500 text-white",
  }

  return (
    <Badge className={variants[type as keyof typeof variants]}>
      {type}
    </Badge>
  )
}
```

---

### 3. Avatar Component

**Type:** registry:ui
**Dependencies:** `@radix-ui/react-avatar`

**Description:**
User profile image with fallback support.

**Components:**
- `Avatar`: Container
- `AvatarImage`: Image element
- `AvatarFallback`: Fallback content (initials)

**Usage Example:**
```tsx
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

export default function UserAvatar({ user }: { user: { name: string; image?: string } }) {
  return (
    <Avatar>
      <AvatarImage src={user.image} alt={user.name} />
      <AvatarFallback>
        {user.name.split(' ').map(n => n[0]).join('').toUpperCase()}
      </AvatarFallback>
    </Avatar>
  )
}

// Rounded square variant
export default function RoundedAvatar() {
  return (
    <Avatar className="rounded-lg">
      <AvatarImage src="/avatar.png" alt="User" />
      <AvatarFallback>UN</AvatarFallback>
    </Avatar>
  )
}

// Avatar group (overlapping avatars)
export default function AvatarGroup({ users }: { users: User[] }) {
  return (
    <div className="flex -space-x-2">
      {users.map((user, i) => (
        <Avatar key={i} className="ring-2 ring-background">
          <AvatarImage src={user.image} alt={user.name} />
          <AvatarFallback>{user.name[0]}</AvatarFallback>
        </Avatar>
      ))}
    </div>
  )
}
```

**Use Cases:**
- User profile displays
- Check-in author display
- Circle member lists
- Buddy lists
- Comment authors
- Leaderboard entries
- Avatar groups showing multiple members

---

### 4. Skeleton Component

**Type:** registry:ui
**Dependencies:** None

**Description:**
Loading placeholder for content that's being fetched.

**Usage Example:**
```tsx
import { Skeleton } from "@/components/ui/skeleton"

export default function GoalCardSkeleton() {
  return (
    <div className="flex flex-col space-y-3">
      <Skeleton className="h-[125px] w-[250px] rounded-xl" />
      <div className="space-y-2">
        <Skeleton className="h-4 w-[250px]" />
        <Skeleton className="h-4 w-[200px]" />
      </div>
    </div>
  )
}

// Feed skeleton
export default function FeedSkeleton() {
  return (
    <div className="space-y-4">
      {Array.from({ length: 3 }).map((_, i) => (
        <div key={i} className="flex items-start space-x-4">
          <Skeleton className="h-12 w-12 rounded-full" />
          <div className="space-y-2 flex-1">
            <Skeleton className="h-4 w-[250px]" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-[200px]" />
          </div>
        </div>
      ))}
    </div>
  )
}
```

**Use Cases:**
- Loading states for:
  - Goal lists
  - Feed items
  - Circle members
  - Leaderboards
  - User profiles
  - Comments

---

## Overlays & Dialogs

### 1. Dialog Component

**Type:** registry:ui
**Dependencies:** `@radix-ui/react-dialog`

**Description:**
Modal dialog for focused interactions.

**Components:**
- `Dialog`: Container with state
- `DialogTrigger`: Trigger button
- `DialogContent`: Modal content
- `DialogHeader`: Header section
- `DialogTitle`: Dialog title
- `DialogDescription`: Dialog description
- `DialogFooter`: Footer with actions
- `DialogClose`: Close button

**Usage Example:**
```tsx
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export default function CreateGoalDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button>Create Goal</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Create New Goal</DialogTitle>
          <DialogDescription>
            Set up a new goal to track. Click create when you're done.
          </DialogDescription>
        </DialogHeader>
        <form>
          <div className="grid gap-4">
            <div className="grid gap-3">
              <Label htmlFor="title">Goal Title</Label>
              <Input id="title" placeholder="Run 5k every morning" />
            </div>
            <div className="grid gap-3">
              <Label htmlFor="description">Description</Label>
              <Input id="description" placeholder="Morning exercise routine" />
            </div>
          </div>
        </form>
        <DialogFooter>
          <DialogClose asChild>
            <Button variant="outline">Cancel</Button>
          </DialogClose>
          <Button type="submit">Create Goal</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
```

**Use Cases:**
- Create/edit goal forms
- Check-in submission
- Circle creation
- Send buddy request
- Add circle members
- Add reactions to check-ins
- Comment submission

---

### 2. Alert Dialog Component

**Type:** registry:ui
**Dependencies:** `@radix-ui/react-alert-dialog`

**Description:**
Modal dialog for confirmations and important alerts.

**Components:**
- `AlertDialog`: Container
- `AlertDialogTrigger`: Trigger button
- `AlertDialogContent`: Modal content
- `AlertDialogHeader`: Header section
- `AlertDialogTitle`: Title
- `AlertDialogDescription`: Description
- `AlertDialogFooter`: Action buttons
- `AlertDialogAction`: Confirm button
- `AlertDialogCancel`: Cancel button

**Usage Example:**
```tsx
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import { Button } from "@/components/ui/button"

export default function DeleteGoalDialog() {
  return (
    <AlertDialog>
      <AlertDialogTrigger asChild>
        <Button variant="destructive">Delete Goal</Button>
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
          <AlertDialogDescription>
            This action cannot be undone. This will permanently delete your
            goal and all associated check-ins.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction onClick={handleDelete}>
            Delete Goal
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}
```

**Use Cases:**
- Delete confirmations (goals, circles, comments)
- Remove buddy confirmations
- Leave circle confirmations
- Logout confirmations
- Account deletion warnings

---

### 3. Sheet Component

**Type:** registry:ui
**Dependencies:** `@radix-ui/react-dialog`

**Description:**
Slide-out panel from screen edges.

**Usage Example:**
```tsx
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet"
import { Button } from "@/components/ui/button"

export default function GoalDetailsSheet() {
  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button variant="outline">View Details</Button>
      </SheetTrigger>
      <SheetContent>
        <SheetHeader>
          <SheetTitle>Goal Details</SheetTitle>
          <SheetDescription>
            View all information about this goal.
          </SheetDescription>
        </SheetHeader>
        <div className="mt-4 space-y-4">
          {/* Goal details content */}
        </div>
      </SheetContent>
    </Sheet>
  )
}
```

**Use Cases:**
- Mobile navigation menu
- Goal detail panels
- User profile quick view
- Filter panels
- Notification panels

---

### 4. Popover Component

**Type:** registry:ui
**Dependencies:** `@radix-ui/react-popover`

**Description:**
Floating panel for contextual content.

**Usage Example:**
```tsx
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"

export default function DatePickerPopover() {
  const [date, setDate] = React.useState<Date>()

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="outline">
          {date ? format(date, "PPP") : "Pick a date"}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-auto p-0">
        <Calendar
          mode="single"
          selected={date}
          onSelect={setDate}
          initialFocus
        />
      </PopoverContent>
    </Popover>
  )
}
```

**Use Cases:**
- Date pickers
- Color pickers
- Quick action menus
- Filter controls
- Reaction pickers

---

### 5. Hover Card Component

**Type:** registry:ui
**Dependencies:** `@radix-ui/react-hover-card`

**Description:**
Preview card on hover for additional information.

**Usage Example:**
```tsx
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"

export default function UserHoverCard() {
  return (
    <HoverCard>
      <HoverCardTrigger asChild>
        <Button variant="link">@username</Button>
      </HoverCardTrigger>
      <HoverCardContent className="w-80">
        <div className="flex gap-4">
          <Avatar>
            <AvatarImage src="/avatar.png" />
            <AvatarFallback>UN</AvatarFallback>
          </Avatar>
          <div className="space-y-1">
            <h4 className="text-sm font-semibold">@username</h4>
            <p className="text-sm">
              Fitness enthusiast tracking daily workout goals.
            </p>
            <div className="text-xs text-muted-foreground">
              Member since January 2024
            </div>
          </div>
        </div>
      </HoverCardContent>
    </HoverCard>
  )
}
```

**Use Cases:**
- User profile previews on username hover
- Goal previews in feed
- Circle previews
- Quick info tooltips

---

## Feedback Components

### 1. Sonner (Toast Notifications)

**Type:** registry:ui
**Dependencies:**
- `sonner`
- `next-themes`

**Description:**
Toast notification system for user feedback. Note: shadcn/ui uses "sonner" instead of "toast" for toast notifications.

**Usage Example:**
```tsx
import { toast } from "sonner"
import { Button } from "@/components/ui/button"

export default function ToastDemo() {
  return (
    <div className="space-x-2">
      <Button onClick={() => toast.success("Goal created successfully!")}>
        Success Toast
      </Button>

      <Button onClick={() => toast.error("Failed to create goal")}>
        Error Toast
      </Button>

      <Button onClick={() => toast.info("Check-in reminder")}>
        Info Toast
      </Button>

      <Button onClick={() => toast.warning("Goal deadline approaching")}>
        Warning Toast
      </Button>

      <Button onClick={() => {
        toast("You submitted the following values:", {
          description: (
            <pre className="mt-2 w-[320px] rounded-md bg-slate-950 p-4">
              <code>{JSON.stringify({ title: "Daily Run" }, null, 2)}</code>
            </pre>
          ),
        })
      }}>
        Custom Content
      </Button>

      <Button onClick={() => {
        toast.promise(
          fetch('/api/goals'),
          {
            loading: 'Creating goal...',
            success: (data) => 'Goal created!',
            error: 'Error creating goal',
          }
        )
      }}>
        Promise Toast
      </Button>
    </div>
  )
}

// Add Toaster to root layout
import { Toaster } from "@/components/ui/sonner"

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Toaster />
      </body>
    </html>
  )
}
```

**Toast Options:**
```tsx
toast("Event created", {
  description: "Monday, January 3rd at 6:00pm",
  action: {
    label: "Undo",
    onClick: () => console.log("Undo"),
  },
  position: "top-center", // top-left, top-right, bottom-left, bottom-right, top-center, bottom-center
  duration: 4000, // milliseconds
})
```

**Use Cases:**
- Success confirmations (goal created, check-in submitted, buddy request sent)
- Error messages (API failures, validation errors)
- Info notifications (reminders, updates)
- Warning alerts (deadline approaching, missing data)
- Loading states during async operations

---

### 2. Progress Component

**Type:** registry:ui
**Dependencies:** `@radix-ui/react-progress`

**Description:**
Progress indicator for tracking completion.

**Usage Example:**
```tsx
"use client"

import * as React from "react"
import { Progress } from "@/components/ui/progress"

export default function GoalProgress() {
  const [progress, setProgress] = React.useState(13)

  React.useEffect(() => {
    const timer = setTimeout(() => setProgress(66), 500)
    return () => clearTimeout(timer)
  }, [])

  return (
    <div className="space-y-2">
      <div className="flex justify-between text-sm">
        <span>Goal Progress</span>
        <span>{progress}%</span>
      </div>
      <Progress value={progress} className="w-full" />
    </div>
  )
}

// Goal completion progress
export default function GoalCompletionProgress({
  checkInsCompleted,
  checkInsTotal
}: {
  checkInsCompleted: number
  checkInsTotal: number
}) {
  const percentage = (checkInsCompleted / checkInsTotal) * 100

  return (
    <div className="space-y-2">
      <div className="flex justify-between text-sm">
        <span>Check-ins</span>
        <span>{checkInsCompleted}/{checkInsTotal}</span>
      </div>
      <Progress value={percentage} />
    </div>
  )
}
```

**Use Cases:**
- Goal completion percentage
- Check-in progress tracking
- Loading states for file uploads
- Streak visualization
- Monthly goal progress

---

### 3. Spinner Component

**Type:** registry:ui
**Dependencies:** `class-variance-authority`

**Description:**
Loading spinner for async operations.

**Usage Example:**
```tsx
import { Spinner } from "@/components/ui/spinner"
import { Button } from "@/components/ui/button"

// Basic spinner
export default function LoadingSpinner() {
  return <Spinner />
}

// Button with spinner
export default function LoadingButton() {
  const [loading, setLoading] = React.useState(false)

  return (
    <Button disabled={loading}>
      {loading && <Spinner className="mr-2 h-4 w-4" />}
      {loading ? "Creating..." : "Create Goal"}
    </Button>
  )
}

// Different sizes
export default function SpinnerSizes() {
  return (
    <div className="flex gap-4 items-center">
      <Spinner size="sm" />
      <Spinner size="default" />
      <Spinner size="lg" />
    </div>
  )
}
```

**Use Cases:**
- Loading buttons during form submission
- Page loading states
- Lazy loaded content
- API request indicators
- Infinite scroll loading

---

## Pre-built Blocks

### Authentication Blocks

#### 1. login-01
**Description:** A simple login form
**Files:** 2 files
**Type:** registry:block

**Use Case:** Basic login page with username/email and password fields.

**Installation:**
```bash
npx shadcn@latest add @shadcn/login-01
```

**Features:**
- Email/username input
- Password input
- Remember me checkbox
- Forgot password link
- Sign up link
- Submit button

---

#### 2. login-04
**Description:** A login page with form and image
**Files:** 2 files
**Type:** registry:block

**Use Case:** More visually appealing login page with split layout (form + image).

**Installation:**
```bash
npx shadcn@latest add @shadcn/login-04
```

**Features:**
- Two-column layout
- Image/illustration panel
- Login form panel
- Modern design
- Responsive layout

---

#### 3. signup-01
**Description:** A simple signup form
**Files:** 2 files
**Type:** registry:block

**Use Case:** Basic registration page.

**Installation:**
```bash
npx shadcn@latest add @shadcn/signup-01
```

**Features:**
- Username input
- Email input
- Password input
- Confirm password input
- Terms acceptance checkbox
- Submit button
- Login link

---

#### 4. signup-04
**Description:** A signup page with form and image
**Files:** 2 files
**Type:** registry:block

**Use Case:** Visually enhanced registration page with split layout.

**Installation:**
```bash
npx shadcn@latest add @shadcn/signup-04
```

**Features:**
- Two-column layout
- Image/illustration panel
- Registration form panel
- Modern design
- Responsive layout

---

### Dashboard Blocks

#### 1. dashboard-01
**Description:** A dashboard with sidebar, charts and data table
**Files:** 11 files
**Type:** registry:block
**Dependencies:**
- `@dnd-kit/core`
- `@dnd-kit/modifiers`
- `@dnd-kit/sortable`
- `@dnd-kit/utilities`
- `@tabler/icons-react`
- `@tanstack/react-table`
- `zod`

**Use Case:** Complete dashboard layout with sidebar navigation, statistics cards, charts, and data tables.

**Installation:**
```bash
npx shadcn@latest add @shadcn/dashboard-01
```

**Features:**
- Sidebar navigation
- Statistics cards
- Chart components
- Data tables
- Drag and drop support
- Responsive layout
- Dark mode support

**Customization Notes:**
- Can be adapted for the main dashboard showing feed, goals summary, and activity
- Statistics cards can display total goals, check-ins, circles, buddies
- Charts can visualize check-in frequency, goal completion trends
- Tables can show recent activity, leaderboards

---

#### 2. sidebar-01
**Description:** A simple sidebar with navigation grouped by section
**Files:** 4 files
**Type:** registry:block

**Use Case:** Main app sidebar navigation with grouped sections.

**Installation:**
```bash
npx shadcn@latest add @shadcn/sidebar-01
```

**Features:**
- Grouped navigation sections
- Icon support
- Active state indicators
- Collapsible sections
- User menu
- Responsive behavior

**Recommended Structure:**
```
Main
├── Feed (Home icon)
├── My Goals (Target icon)
├── Circles (Users icon)
└── Buddies (UserCircle icon)

Account
├── Profile (User icon)
└── Settings (Settings icon)
```

---

## Best Practices

### Accessibility

1. **Form Components**
   - Always use `Label` with form inputs
   - Include `aria-invalid` for validation states
   - Provide `aria-describedby` for help text
   - Use semantic HTML elements

2. **Interactive Elements**
   - Ensure keyboard navigation works
   - Include focus visible states
   - Use proper ARIA labels
   - Test with screen readers

3. **Dialogs and Modals**
   - Trap focus within dialogs
   - Allow ESC key to close
   - Restore focus on close
   - Use proper heading hierarchy

4. **Tables**
   - Use semantic table elements
   - Include table captions
   - Support keyboard navigation
   - Ensure proper header associations

### Performance

1. **Loading States**
   - Use Skeleton components for initial loads
   - Implement progressive loading
   - Show Spinner for async operations
   - Provide feedback with Toast notifications

2. **Data Tables**
   - Implement pagination for large datasets
   - Use virtualization for very long lists
   - Consider server-side sorting/filtering
   - Cache data appropriately

3. **Forms**
   - Debounce validation
   - Use controlled components wisely
   - Validate on blur for better UX
   - Consider using React Hook Form for performance

### Validation Patterns

#### Goal Creation Form
```tsx
const goalSchema = z.object({
  title: z.string()
    .min(1, "Title is required")
    .max(50, "Title must be 50 characters or less"),
  description: z.string()
    .max(256, "Description must be 256 characters or less")
    .optional(),
  goalType: z.enum(["daily", "weekly", "monthly", "project", "habit", "custom"], {
    required_error: "Please select a goal type",
  }),
  circleId: z.string().optional(),
  startDate: z.date().optional(),
  endDate: z.date().optional(),
  isActive: z.boolean().default(true),
}).refine((data) => {
  if (data.startDate && data.endDate) {
    return data.endDate > data.startDate
  }
  return true
}, {
  message: "End date must be after start date",
  path: ["endDate"],
})
```

#### Check-in Form (Project/Habit Validation)
```tsx
const checkInSchema = z.object({
  content: z.string(),
  goalId: z.string(),
  goalType: z.string(),
}).refine((data) => {
  if (data.goalType === "project" || data.goalType === "habit") {
    return data.content.length > 0
  }
  return true
}, {
  message: "Content is required for project and habit goals",
  path: ["content"],
})
```

#### Buddy Request Form
```tsx
const buddyRequestSchema = z.object({
  userId: z.string(),
  message: z.string().max(256).optional(),
})
```

### State Management Recommendations

1. **Server State (React Query/TanStack Query)**
   - Goals list
   - Feed data
   - Circle members
   - Leaderboards
   - User profiles

2. **Client State (Zustand/Context)**
   - Current user
   - UI state (sidebar collapsed, theme)
   - Modal states
   - Form drafts

3. **Form State (React Hook Form)**
   - Form values
   - Validation states
   - Submit status

### Error Handling

```tsx
// API error handling with toast
async function createGoal(data: GoalData) {
  try {
    const response = await api.post('/goals', data)
    toast.success("Goal created successfully!")
    return response.data
  } catch (error) {
    if (error.response?.status === 400) {
      toast.error("Invalid goal data. Please check your inputs.")
    } else if (error.response?.status === 401) {
      toast.error("Session expired. Please log in again.")
      // Redirect to login
    } else {
      toast.error("Failed to create goal. Please try again.")
    }
    throw error
  }
}
```

### Responsive Design

1. **Mobile-First Approach**
   - Use responsive classes (`sm:`, `md:`, `lg:`)
   - Consider Sheet instead of Dialog for mobile
   - Ensure touch targets are at least 44x44px
   - Test on various screen sizes

2. **Component Adaptations**
   - Use Sheet for mobile navigation
   - Convert tables to cards on mobile
   - Stack columns vertically on small screens
   - Adjust sidebar behavior for mobile

---

## Component Dependencies

### Critical Dependencies

These packages are required by multiple components and should be installed first:

```bash
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-select @radix-ui/react-tabs @radix-ui/react-slot
```

### Form Dependencies

```bash
npm install react-hook-form @hookform/resolvers zod
```

### Table Dependencies (Optional but Recommended)

```bash
npm install @tanstack/react-table
```

### Date Dependencies

```bash
npm install react-day-picker date-fns
```

### Toast Dependencies

```bash
npm install sonner next-themes
```

### Additional UI Dependencies

```bash
npm install class-variance-authority lucide-react
```

---

## Component Dependency Tree

```
Authentication Pages
├── login-01 / login-04
│   ├── form
│   ├── input
│   ├── button
│   └── card
└── signup-01 / signup-04
    ├── form
    ├── input
    ├── button
    └── card

Dashboard
├── sidebar-01 / dashboard-01
│   ├── sidebar
│   ├── card
│   ├── badge
│   └── button
├── tabs
├── card
└── skeleton (loading states)

Goals Page
├── card
├── badge
├── button
├── dropdown-menu
├── dialog (create/edit)
├── alert-dialog (delete)
├── form
├── input
├── textarea
├── select
├── calendar
└── progress

Feed Page
├── card
├── avatar
├── badge
├── button
├── dialog (reactions, comments)
├── textarea
└── skeleton

Circles Page
├── card
├── badge
├── tabs
├── table
├── avatar
├── dialog
├── alert-dialog
└── textarea (messaging)

Buddies Page
├── card
├── avatar
├── badge
├── tabs
├── button
├── dialog
└── alert-dialog
```

---

## Integration Notes

### API Integration Pattern

```tsx
// hooks/useGoals.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'

export function useGoals() {
  const queryClient = useQueryClient()

  const { data: goals, isLoading } = useQuery({
    queryKey: ['goals'],
    queryFn: () => api.get('/goals').then(res => res.data),
  })

  const createGoal = useMutation({
    mutationFn: (data: GoalData) => api.post('/goals', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['goals'] })
      toast.success("Goal created successfully!")
    },
    onError: () => {
      toast.error("Failed to create goal")
    },
  })

  return { goals, isLoading, createGoal }
}

// components/GoalsList.tsx
export function GoalsList() {
  const { goals, isLoading } = useGoals()

  if (isLoading) {
    return <GoalsSkeleton />
  }

  return (
    <div className="grid gap-4">
      {goals.map(goal => (
        <GoalCard key={goal.id} goal={goal} />
      ))}
    </div>
  )
}
```

### Authentication Flow

```tsx
// lib/auth.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AuthState {
  user: User | null
  token: string | null
  login: (username: string, password: string) => Promise<void>
  logout: () => void
}

export const useAuth = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      login: async (username, password) => {
        const response = await api.post('/login', { username, password })
        set({ user: response.data.user, token: response.data.access_token })
        toast.success("Logged in successfully!")
      },
      logout: () => {
        set({ user: null, token: null })
        toast.info("Logged out")
      },
    }),
    { name: 'auth-storage' }
  )
)
```

### Protected Routes

```tsx
// components/ProtectedRoute.tsx
import { useAuth } from '@/lib/auth'
import { Navigate } from 'react-router-dom'

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { token } = useAuth()

  if (!token) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}
```

---

## Summary

This component research document provides:

1. **Complete Installation Commands** - Ready-to-use commands for all components
2. **Component Details** - API, props, dependencies for each component
3. **Usage Examples** - Real-world code examples for the accountability app
4. **Best Practices** - Accessibility, performance, and validation patterns
5. **Integration Patterns** - API integration, auth flow, and routing examples
6. **Pre-built Blocks** - Authentication and dashboard blocks for rapid development

### Next Steps

1. **Install shadcn/ui components** using the provided commands
2. **Set up authentication** using login/signup blocks
3. **Implement dashboard** using dashboard-01 and sidebar-01 blocks
4. **Build feature pages** using component examples as reference
5. **Integrate with backend API** using React Query patterns
6. **Add validation** using Zod schemas provided
7. **Implement accessibility** following WCAG guidelines
8. **Test responsiveness** across different screen sizes

### Recommended Development Order

**Phase 1: Foundation**
1. Install all components
2. Set up authentication pages (login-01, signup-01)
3. Implement auth state management
4. Create protected route wrapper

**Phase 2: Core Layout**
1. Set up dashboard layout (dashboard-01, sidebar-01)
2. Implement main navigation
3. Create feed page structure
4. Add skeleton loading states

**Phase 3: Goals Feature**
1. Goals list page with cards
2. Create goal dialog with form validation
3. Goal detail page with check-ins
4. Edit/delete functionality with alert dialogs

**Phase 4: Social Features**
1. Circle pages with tabs (overview, leaderboard, members, chat)
2. Buddies page with request management
3. Feed with check-in cards, reactions, comments
4. User profile pages

**Phase 5: Polish**
1. Add toast notifications throughout
2. Implement error boundaries
3. Optimize performance
4. Ensure accessibility compliance
5. Test on various devices

---

**Document Generated:** 2026-01-03
**shadcn/ui Registry:** @shadcn (new-york-v4)
**Total Components Researched:** 24 core components + 6 blocks
