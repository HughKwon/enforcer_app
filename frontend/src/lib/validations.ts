import { z } from 'zod';

// Auth validation schemas
export const loginSchema = z.object({
  username: z.string().min(1, 'Username is required'),
  password: z.string().min(1, 'Password is required'),
});

export const registerSchema = z.object({
  username: z.string().min(3, 'Username must be at least 3 characters').max(50),
  email: z.string().email('Invalid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
  confirmPassword: z.string().min(1, 'Please confirm your password'),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});

// Goal validation schemas
export const goalSchema = z.object({
  title: z.string().min(1, 'Title is required').max(50, 'Title must be 50 characters or less'),
  description: z.string().max(256, 'Description must be 256 characters or less').optional(),
  goal_type: z.enum(['daily', 'weekly', 'monthly', 'project', 'habit', 'custom'], {
    required_error: 'Please select a goal type',
  }),
  circle_id: z.number().optional(),
  start_date: z.string().optional(),
  end_date: z.string().optional(),
  is_active: z.boolean().default(true),
}).refine((data) => {
  if (data.start_date && data.end_date) {
    return new Date(data.end_date) > new Date(data.start_date);
  }
  return true;
}, {
  message: 'End date must be after start date',
  path: ['end_date'],
});

// Check-in validation schema
export const checkInSchema = z.object({
  content: z.string(),
  goal_type: z.string().optional(),
}).refine((data) => {
  // Project and habit goals require content
  if (data.goal_type === 'project' || data.goal_type === 'habit') {
    return data.content && data.content.length > 0;
  }
  return true;
}, {
  message: 'Content is required for project and habit goals',
  path: ['content'],
});

// Circle validation schemas
export const circleSchema = z.object({
  name: z.string().min(1, 'Name is required').max(100, 'Name must be 100 characters or less'),
  description: z.string().max(500, 'Description must be 500 characters or less').optional(),
});

// Comment validation schema
export const commentSchema = z.object({
  content: z.string().min(1, 'Comment cannot be empty').max(500, 'Comment must be 500 characters or less'),
});

// Buddy request validation schema
export const buddyRequestSchema = z.object({
  message: z.string().max(256, 'Message must be 256 characters or less').optional(),
});

// Circle message validation schema
export const circleMessageSchema = z.object({
  content: z.string().min(1, 'Message cannot be empty').max(1000, 'Message must be 1000 characters or less'),
});

// Password change validation schema
export const changePasswordSchema = z.object({
  currentPassword: z.string().min(1, 'Current password is required'),
  newPassword: z.string().min(6, 'New password must be at least 6 characters'),
  confirmPassword: z.string().min(1, 'Please confirm your new password'),
}).refine((data) => data.newPassword === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});

export type LoginFormData = z.infer<typeof loginSchema>;
export type RegisterFormData = z.infer<typeof registerSchema>;
export type GoalFormData = z.infer<typeof goalSchema>;
export type CheckInFormData = z.infer<typeof checkInSchema>;
export type CircleFormData = z.infer<typeof circleSchema>;
export type CommentFormData = z.infer<typeof commentSchema>;
export type BuddyRequestFormData = z.infer<typeof buddyRequestSchema>;
export type CircleMessageFormData = z.infer<typeof circleMessageSchema>;
export type ChangePasswordFormData = z.infer<typeof changePasswordSchema>;
