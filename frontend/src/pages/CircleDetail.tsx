import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Textarea } from '@/components/ui/textarea';
import { ArrowLeft, Trophy, MessageSquare } from 'lucide-react';
import {
  useCircle,
  useCircleMembers,
  useCircleLeaderboard,
  useCircleMessages,
  useSendCircleMessage,
} from '@/hooks/useCircles';
import { circleMessageSchema, CircleMessageFormData } from '@/lib/validations';
import { format } from 'date-fns';

export function CircleDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('leaderboard');

  const { data: circle, isLoading: circleLoading } = useCircle(id!);
  const { data: members, isLoading: membersLoading } = useCircleMembers(id!);
  const { data: leaderboard, isLoading: leaderboardLoading } = useCircleLeaderboard(id!);
  const { data: messages, isLoading: messagesLoading } = useCircleMessages(id!);
  const sendMessage = useSendCircleMessage();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<CircleMessageFormData>({
    resolver: zodResolver(circleMessageSchema),
  });

  const onSubmitMessage = async (data: CircleMessageFormData) => {
    try {
      await sendMessage.mutateAsync({
        circleId: Number(id),
        content: data.content,
      });
      reset();
    } catch (error) {
      // Error handled by mutation
    }
  };

  if (circleLoading) {
    return (
      <div className="max-w-4xl mx-auto space-y-6">
        <Skeleton className="h-8 w-64" />
        <Card>
          <CardHeader>
            <Skeleton className="h-6 w-full" />
            <Skeleton className="h-4 w-full" />
          </CardHeader>
        </Card>
      </div>
    );
  }

  if (!circle) {
    return (
      <div className="max-w-4xl mx-auto">
        <Card>
          <CardHeader>
            <CardTitle>Circle Not Found</CardTitle>
            <CardDescription>The circle you're looking for doesn't exist.</CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={() => navigate('/circles')}>Back to Circles</Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => navigate('/circles')}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <div>
          <h1 className="text-3xl font-bold">{circle.name}</h1>
          {circle.description && (
            <p className="text-muted-foreground">{circle.description}</p>
          )}
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="leaderboard">
            <Trophy className="mr-2 h-4 w-4" />
            Leaderboard
          </TabsTrigger>
          <TabsTrigger value="members">
            Members ({members?.user?.length || 0})
          </TabsTrigger>
          <TabsTrigger value="chat">
            <MessageSquare className="mr-2 h-4 w-4" />
            Chat
          </TabsTrigger>
        </TabsList>

        <TabsContent value="leaderboard" className="space-y-4 mt-6">
          {leaderboardLoading ? (
            <Card>
              <CardContent className="p-6">
                <Skeleton className="h-20 w-full" />
              </CardContent>
            </Card>
          ) : leaderboard?.leaderboard && leaderboard.leaderboard.length > 0 ? (
            <div className="space-y-4">
              {leaderboard.leaderboard.map((entry, index) => (
                <Card key={entry.user_id}>
                  <CardContent className="pt-6">
                    <div className="flex items-center gap-4">
                      <div className="text-2xl font-bold text-muted-foreground w-8">
                        #{index + 1}
                      </div>
                      <Avatar>
                        <AvatarFallback>{entry.username.charAt(0).toUpperCase()}</AvatarFallback>
                      </Avatar>
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <h3 className="font-semibold">{entry.username}</h3>
                          {entry.role === 'creator' && (
                            <Badge variant="default">Creator</Badge>
                          )}
                          {entry.role === 'admin' && (
                            <Badge variant="secondary">Admin</Badge>
                          )}
                        </div>
                        <div className="flex gap-4 text-sm text-muted-foreground mt-1">
                          <span>{entry.total_checkins} check-ins</span>
                          <span>{entry.active_goals} active goals</span>
                          {entry.last_checkin && (
                            <span>Last: {format(new Date(entry.last_checkin), 'PP')}</span>
                          )}
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Card>
              <CardContent className="py-12 text-center">
                <Trophy className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
                <p className="text-muted-foreground">No activity yet. Start checking in!</p>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="members" className="space-y-4 mt-6">
          {membersLoading ? (
            <Card>
              <CardContent className="p-6">
                <Skeleton className="h-20 w-full" />
              </CardContent>
            </Card>
          ) : members?.user && members.user.length > 0 ? (
            <div className="grid gap-4 md:grid-cols-2">
              {members.user.map((member) => (
                <Card key={member.id}>
                  <CardHeader>
                    <div className="flex items-center gap-3">
                      <Avatar>
                        <AvatarFallback>{member.username.charAt(0).toUpperCase()}</AvatarFallback>
                      </Avatar>
                      <div className="flex-1">
                        <CardTitle className="text-base">{member.username}</CardTitle>
                        <CardDescription className="text-xs">{member.email}</CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                </Card>
              ))}
            </div>
          ) : (
            <Card>
              <CardContent className="py-12 text-center">
                <p className="text-muted-foreground">No members yet.</p>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="chat" className="space-y-4 mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Circle Chat</CardTitle>
              <CardDescription>Communicate with your circle members</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit(onSubmitMessage)} className="space-y-4">
                <div className="space-y-2">
                  <Textarea
                    placeholder="Type your message..."
                    rows={3}
                    {...register('content')}
                    aria-invalid={!!errors.content}
                  />
                  {errors.content && (
                    <p className="text-sm text-destructive">{errors.content.message}</p>
                  )}
                </div>
                <Button type="submit" disabled={sendMessage.isPending}>
                  {sendMessage.isPending ? 'Sending...' : 'Send Message'}
                </Button>
              </form>
            </CardContent>
          </Card>

          <div className="space-y-4">
            {messagesLoading ? (
              <Card>
                <CardContent className="p-6">
                  <Skeleton className="h-20 w-full" />
                </CardContent>
              </Card>
            ) : messages && messages.length > 0 ? (
              messages.map((message) => (
                <Card key={message.id}>
                  <CardContent className="pt-6">
                    <div className="flex items-start gap-3">
                      <Avatar>
                        <AvatarFallback>{message.username.charAt(0).toUpperCase()}</AvatarFallback>
                      </Avatar>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="font-semibold text-sm">{message.username}</span>
                          <span className="text-xs text-muted-foreground">
                            {format(new Date(message.created_at), 'PPp')}
                          </span>
                        </div>
                        <p className="text-sm">{message.content}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))
            ) : (
              <Card>
                <CardContent className="py-12 text-center">
                  <MessageSquare className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
                  <p className="text-muted-foreground">No messages yet. Start the conversation!</p>
                </CardContent>
              </Card>
            )}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
