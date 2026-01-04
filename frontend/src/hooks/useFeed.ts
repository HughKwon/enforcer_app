import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import api from '@/lib/api';
import { FeedItem, Comment, Reaction, CreateCommentInput, CreateReactionInput } from '@/types';

// Fetch all feed
export function useFeed() {
  return useQuery({
    queryKey: ['feed'],
    queryFn: async () => {
      const response = await api.get<FeedItem[]>('/feed');
      return response.data;
    },
  });
}

// Fetch following feed
export function useFollowingFeed() {
  return useQuery({
    queryKey: ['feed', 'following'],
    queryFn: async () => {
      const response = await api.get<FeedItem[]>('/feed/following');
      return response.data;
    },
  });
}

// Fetch circles feed
export function useCirclesFeed() {
  return useQuery({
    queryKey: ['feed', 'circles'],
    queryFn: async () => {
      const response = await api.get<FeedItem[]>('/feed/circles');
      return response.data;
    },
  });
}

// Fetch check-in comments
export function useCheckInComments(checkInId: number) {
  return useQuery({
    queryKey: ['check-in-comments', checkInId],
    queryFn: async () => {
      const response = await api.get<Comment[]>(`/check-ins/${checkInId}/comments`);
      return response.data;
    },
    enabled: !!checkInId,
  });
}

// Fetch check-in reactions
export function useCheckInReactions(checkInId: number) {
  return useQuery({
    queryKey: ['check-in-reactions', checkInId],
    queryFn: async () => {
      const response = await api.get<Reaction[]>(`/check-ins/${checkInId}/reactions`);
      return response.data;
    },
    enabled: !!checkInId,
  });
}

// Add comment mutation
export function useAddComment() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ checkInId, data }: { checkInId: number; data: CreateCommentInput }) => {
      const response = await api.post<Comment>(`/check-ins/${checkInId}/comments`, data);
      return response.data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['check-in-comments', variables.checkInId] });
      queryClient.invalidateQueries({ queryKey: ['feed'] });
      toast.success('Comment added!');
    },
  });
}

// Add reaction mutation
export function useAddReaction() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ checkInId, data }: { checkInId: number; data: CreateReactionInput }) => {
      const response = await api.post<Reaction>(`/check-ins/${checkInId}/reactions`, data);
      return response.data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['check-in-reactions', variables.checkInId] });
      queryClient.invalidateQueries({ queryKey: ['feed'] });
    },
  });
}

// Delete comment mutation
export function useDeleteComment() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (commentId: number) => {
      await api.delete(`/comments/${commentId}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['check-in-comments'] });
      queryClient.invalidateQueries({ queryKey: ['feed'] });
      toast.success('Comment deleted!');
    },
  });
}
