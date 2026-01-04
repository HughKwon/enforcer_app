import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import api from '@/lib/api';
import { Buddy, BuddyRequest } from '@/types';

// Fetch buddies list
export function useBuddies() {
  return useQuery({
    queryKey: ['buddies'],
    queryFn: async () => {
      const response = await api.get<{ buddies: Buddy[] }>('/buddy/list');
      console.log('Buddies response:', response.data);
      return response.data.buddies;
    },
  });
}

// Fetch received buddy requests
export function useReceivedBuddyRequests() {
  return useQuery({
    queryKey: ['buddy-requests', 'received'],
    queryFn: async () => {
      const response = await api.get<BuddyRequest[]>('/buddy/requests/received');
      return response.data;
    },
  });
}

// Fetch sent buddy requests
export function useSentBuddyRequests() {
  return useQuery({
    queryKey: ['buddy-requests', 'sent'],
    queryFn: async () => {
      const response = await api.get<BuddyRequest[]>('/buddy/requests/sent');
      return response.data;
    },
  });
}

// Send buddy request mutation
export function useSendBuddyRequest() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ userId, message }: { userId: number; message?: string }) => {
      await api.post(`/buddy/request/${userId}`, { message });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['buddy-requests', 'sent'] });
      toast.success('Buddy request sent!');
    },
  });
}

// Accept buddy request mutation
export function useAcceptBuddyRequest() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (requestId: number) => {
      await api.post(`/buddy/request/${requestId}/accept`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['buddy-requests', 'received'] });
      queryClient.invalidateQueries({ queryKey: ['buddies'] });
      toast.success('Buddy request accepted!');
    },
  });
}

// Decline buddy request mutation
export function useDeclineBuddyRequest() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (requestId: number) => {
      await api.post(`/buddy/request/${requestId}/decline`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['buddy-requests', 'received'] });
      toast.success('Buddy request declined!');
    },
  });
}

// Remove buddy mutation
export function useRemoveBuddy() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (userId: number) => {
      await api.delete(`/buddy/${userId}/remove`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['buddies'] });
      toast.success('Buddy removed!');
    },
  });
}
