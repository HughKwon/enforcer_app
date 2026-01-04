import { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Input } from '@/components/ui/input';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { UserCircle, Check, X, UserPlus, Search } from 'lucide-react';
import { useBuddies, useReceivedBuddyRequests, useSentBuddyRequests, useAcceptBuddyRequest, useDeclineBuddyRequest, useSendBuddyRequest } from '@/hooks/useBuddies';
import { useSearchUsers } from '@/hooks/useUsers';
import { format } from 'date-fns';

function BuddiesSkeleton() {
  return (
    <div className="space-y-4">
      {Array.from({ length: 3 }).map((_, i) => (
        <Card key={i}>
          <CardHeader>
            <Skeleton className="h-6 w-full" />
          </CardHeader>
        </Card>
      ))}
    </div>
  );
}

export function Buddies() {
  const [searchDialogOpen, setSearchDialogOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const { data: buddies, isLoading: buddiesLoading } = useBuddies();
  const { data: receivedRequests, isLoading: receivedLoading } = useReceivedBuddyRequests();
  const { data: sentRequests, isLoading: sentLoading } = useSentBuddyRequests();
  const { data: searchResults, isLoading: searchLoading } = useSearchUsers(searchQuery);

  const acceptRequest = useAcceptBuddyRequest();
  const declineRequest = useDeclineBuddyRequest();
  const sendRequest = useSendBuddyRequest();

  const handleSendRequest = async (userId: number) => {
    try {
      await sendRequest.mutateAsync({ userId });
      setSearchQuery('');
      setSearchDialogOpen(false);
    } catch (error) {
      // Error handled by mutation
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Buddies</h1>
          <p className="text-muted-foreground">Manage your accountability buddies</p>
        </div>
        <Dialog open={searchDialogOpen} onOpenChange={setSearchDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <UserPlus className="mr-2 h-4 w-4" />
              Add Buddy
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle>Find Buddies</DialogTitle>
              <DialogDescription>
                Search for users by username or email to send buddy requests
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div className="relative">
                <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search by username or email..."
                  value={searchQuery}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSearchQuery(e.target.value)}
                  className="pl-9"
                />
              </div>

              {searchLoading && searchQuery && (
                <div className="space-y-2">
                  <Skeleton className="h-16 w-full" />
                  <Skeleton className="h-16 w-full" />
                </div>
              )}

              {searchResults && searchResults.length > 0 && (
                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {searchResults.map((user) => (
                    <Card key={user.id}>
                      <CardContent className="p-4">
                        <div className="flex items-center gap-3">
                          <Avatar>
                            <AvatarFallback>
                              {user.username ? user.username.charAt(0).toUpperCase() : '?'}
                            </AvatarFallback>
                          </Avatar>
                          <div className="flex-1">
                            <p className="font-semibold">{user.username || 'Unknown'}</p>
                            <p className="text-sm text-muted-foreground">{user.email || 'No email'}</p>
                          </div>
                          <Button
                            size="sm"
                            onClick={() => handleSendRequest(user.id)}
                            disabled={sendRequest.isPending}
                          >
                            <UserPlus className="h-4 w-4 mr-1" />
                            Send Request
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}

              {searchQuery && !searchLoading && searchResults?.length === 0 && (
                <div className="text-center py-8 text-muted-foreground">
                  No users found matching "{searchQuery}"
                </div>
              )}

              {!searchQuery && (
                <div className="text-center py-8 text-muted-foreground">
                  Start typing to search for users
                </div>
              )}
            </div>
          </DialogContent>
        </Dialog>
      </div>

      <Tabs defaultValue="buddies">
        <TabsList>
          <TabsTrigger value="buddies">
            My Buddies ({buddies?.length || 0})
          </TabsTrigger>
          <TabsTrigger value="received">
            Requests Received ({receivedRequests?.length || 0})
          </TabsTrigger>
          <TabsTrigger value="sent">
            Sent ({sentRequests?.length || 0})
          </TabsTrigger>
        </TabsList>

        <TabsContent value="buddies" className="space-y-4 mt-6">
          {buddiesLoading ? (
            <BuddiesSkeleton />
          ) : buddies && buddies.length > 0 ? (
            buddies.map((buddy) => (
              <Card key={buddy.user_id}>
                <CardHeader>
                  <div className="flex items-center gap-4">
                    <Avatar>
                      <AvatarFallback>
                        {buddy.username ? buddy.username.charAt(0).toUpperCase() : '?'}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                      <CardTitle className="text-lg">{buddy.username || 'Unknown'}</CardTitle>
                      <CardDescription>{buddy.email || 'No email'}</CardDescription>
                      <p className="text-xs text-muted-foreground mt-1">
                        Buddies since {format(new Date(buddy.buddies_since), 'PP')}
                      </p>
                    </div>
                  </div>
                </CardHeader>
              </Card>
            ))
          ) : (
            <Card>
              <CardContent className="py-12 text-center">
                <UserCircle className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
                <p className="text-muted-foreground">No buddies yet. Send some requests!</p>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="received" className="space-y-4 mt-6">
          {receivedLoading ? (
            <BuddiesSkeleton />
          ) : receivedRequests && receivedRequests.length > 0 ? (
            receivedRequests.map((request) => (
              <Card key={request.id}>
                <CardHeader>
                  <div className="flex items-center gap-4">
                    <Avatar>
                      <AvatarFallback>
                        {request.requester_username ? request.requester_username.charAt(0).toUpperCase() : '?'}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                      <CardTitle className="text-lg">{request.requester_username || 'Unknown'}</CardTitle>
                      {request.message && (
                        <CardDescription className="mt-1">{request.message}</CardDescription>
                      )}
                      <p className="text-xs text-muted-foreground mt-1">
                        {format(new Date(request.created_at), 'PPp')}
                      </p>
                    </div>
                    <div className="flex gap-2">
                      <Button
                        size="sm"
                        variant="default"
                        onClick={() => acceptRequest.mutate(request.id)}
                        disabled={acceptRequest.isPending}
                      >
                        <Check className="h-4 w-4 mr-1" />
                        Accept
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => declineRequest.mutate(request.id)}
                        disabled={declineRequest.isPending}
                      >
                        <X className="h-4 w-4 mr-1" />
                        Decline
                      </Button>
                    </div>
                  </div>
                </CardHeader>
              </Card>
            ))
          ) : (
            <Card>
              <CardContent className="py-12 text-center">
                <p className="text-muted-foreground">No pending requests.</p>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="sent" className="space-y-4 mt-6">
          {sentLoading ? (
            <BuddiesSkeleton />
          ) : sentRequests && sentRequests.length > 0 ? (
            sentRequests.map((request) => (
              <Card key={request.id}>
                <CardHeader>
                  <div className="flex items-center gap-4">
                    <Avatar>
                      <AvatarFallback>
                        {request.receiver_username ? request.receiver_username.charAt(0).toUpperCase() : '?'}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                      <CardTitle className="text-lg">{request.receiver_username || 'Unknown'}</CardTitle>
                      {request.message && (
                        <CardDescription className="mt-1">{request.message}</CardDescription>
                      )}
                      <p className="text-xs text-muted-foreground mt-1">
                        {format(new Date(request.created_at), 'PPp')}
                      </p>
                    </div>
                    <Badge variant="secondary">{request.status}</Badge>
                  </div>
                </CardHeader>
              </Card>
            ))
          ) : (
            <Card>
              <CardContent className="py-12 text-center">
                <p className="text-muted-foreground">No sent requests.</p>
              </CardContent>
            </Card>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
