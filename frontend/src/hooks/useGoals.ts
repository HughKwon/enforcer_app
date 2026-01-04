import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import api from '@/lib/api';
import { Goal, CreateGoalInput, CheckIn, CreateCheckInInput } from '@/types';

// Fetch all goals
export function useGoals() {
  return useQuery({
    queryKey: ['goals'],
    queryFn: async () => {
      const response = await api.get<Goal[]>('/goals');
      return response.data;
    },
  });
}

// Fetch single goal
export function useGoal(goalId: number | string) {
  return useQuery({
    queryKey: ['goal', goalId],
    queryFn: async () => {
      const response = await api.get<Goal>(`/goal/${goalId}`);
      return response.data;
    },
    enabled: !!goalId,
  });
}

// Fetch goal check-ins
export function useGoalCheckIns(goalId: number | string) {
  return useQuery({
    queryKey: ['goal-checkins', goalId],
    queryFn: async () => {
      const response = await api.get<CheckIn[]>(`/goal/${goalId}/check-ins`);
      return response.data;
    },
    enabled: !!goalId,
  });
}

// Create goal mutation
export function useCreateGoal() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CreateGoalInput) => {
      const response = await api.post<Goal>('/goals', data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['goals'] });
      toast.success('Goal created successfully!');
    },
  });
}

// Update goal mutation
export function useUpdateGoal() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, data }: { id: number; data: Partial<CreateGoalInput> }) => {
      const response = await api.put<Goal>(`/goal/${id}`, data);
      return response.data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['goals'] });
      queryClient.invalidateQueries({ queryKey: ['goal', variables.id] });
      toast.success('Goal updated successfully!');
    },
  });
}

// Delete goal mutation
export function useDeleteGoal() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: number) => {
      await api.delete(`/goal/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['goals'] });
      toast.success('Goal deleted successfully!');
    },
  });
}

// Create check-in mutation
export function useCreateCheckIn() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ goalId, data }: { goalId: number; data: CreateCheckInInput }) => {
      const response = await api.post<CheckIn>(`/goal/${goalId}/check-ins`, data);
      return response.data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['goal-checkins', variables.goalId] });
      queryClient.invalidateQueries({ queryKey: ['feed'] });
      toast.success('Check-in submitted successfully!');
    },
  });
}
