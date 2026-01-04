import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import api from '@/lib/api';
import { Circle, CreateCircleInput, CircleMember, LeaderboardEntry, CircleMessage } from '@/types';

// Fetch user's circles
export function useCircles() {
  return useQuery({
    queryKey: ['circles'],
    queryFn: async () => {
      const response = await api.get<Circle[]>('/circles');
      return response.data;
    },
  });
}

// Fetch single circle
export function useCircle(circleId: number | string) {
  return useQuery({
    queryKey: ['circle', circleId],
    queryFn: async () => {
      const response = await api.get<Circle>(`/circle/${circleId}`);
      return response.data;
    },
    enabled: !!circleId,
  });
}

// Fetch circle members
export function useCircleMembers(circleId: number | string) {
  return useQuery({
    queryKey: ['circle-members', circleId],
    queryFn: async () => {
      const response = await api.get<CircleMember[]>(`/circle/${circleId}/users`);
      return response.data;
    },
    enabled: !!circleId,
  });
}

// Fetch circle leaderboard
export function useCircleLeaderboard(circleId: number | string) {
  return useQuery({
    queryKey: ['circle-leaderboard', circleId],
    queryFn: async () => {
      const response = await api.get<LeaderboardEntry[]>(`/circle/${circleId}/leaderboard`);
      return response.data;
    },
    enabled: !!circleId,
  });
}

// Fetch circle messages
export function useCircleMessages(circleId: number | string) {
  return useQuery({
    queryKey: ['circle-messages', circleId],
    queryFn: async () => {
      const response = await api.get<CircleMessage[]>(`/circle/${circleId}/message`);
      return response.data;
    },
    enabled: !!circleId,
  });
}

// Create circle mutation
export function useCreateCircle() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CreateCircleInput) => {
      const response = await api.post<Circle>('/circle', data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['circles'] });
      toast.success('Circle created successfully!');
    },
  });
}

// Update circle mutation
export function useUpdateCircle() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, data }: { id: number; data: Partial<CreateCircleInput> }) => {
      const response = await api.put<Circle>(`/circle/${id}`, data);
      return response.data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['circles'] });
      queryClient.invalidateQueries({ queryKey: ['circle', variables.id] });
      toast.success('Circle updated successfully!');
    },
  });
}

// Delete circle mutation
export function useDeleteCircle() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: number) => {
      await api.delete(`/circle/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['circles'] });
      toast.success('Circle deleted successfully!');
    },
  });
}

// Add member mutation
export function useAddCircleMember() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ circleId, userId }: { circleId: number; userId: number }) => {
      await api.post(`/circle/${circleId}/users`, { user_id: userId });
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['circle-members', variables.circleId] });
      toast.success('Member added to circle!');
    },
  });
}

// Remove member mutation
export function useRemoveCircleMember() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ circleId, userId }: { circleId: number; userId: number }) => {
      await api.delete(`/circle/${circleId}/users`, { data: { user_id: userId } });
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['circle-members', variables.circleId] });
      toast.success('Member removed from circle!');
    },
  });
}

// Send message mutation
export function useSendCircleMessage() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ circleId, content }: { circleId: number; content: string }) => {
      const response = await api.post<CircleMessage>(`/circle/${circleId}/message`, { content });
      return response.data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['circle-messages', variables.circleId] });
    },
  });
}
