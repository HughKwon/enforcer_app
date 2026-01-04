import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';
import { User } from '@/types';

// Search users
export function useSearchUsers(searchQuery: string) {
  return useQuery({
    queryKey: ['users', 'search', searchQuery],
    queryFn: async () => {
      const response = await api.get<User[]>('/users', {
        params: { search: searchQuery },
      });
      console.log('User search response:', response.data);
      return response.data;
    },
    enabled: searchQuery.length > 0,
  });
}
