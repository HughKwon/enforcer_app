import { useState } from 'react';
import { formatDistanceToNow } from 'date-fns';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Heart, MessageCircle, Send } from 'lucide-react';
import { FeedItem } from '@/types';
import { useAddComment, useAddReaction } from '@/hooks/useFeed';
import { toast } from 'sonner';

interface CheckInCardProps {
  checkIn: FeedItem;
}

export function CheckInCard({ checkIn }: CheckInCardProps) {
  const [showCommentInput, setShowCommentInput] = useState(false);
  const [commentText, setCommentText] = useState('');
  const addComment = useAddComment();
  const addReaction = useAddReaction();

  const getUserInitials = () => {
    return checkIn.username?.charAt(0).toUpperCase() || 'U';
  };

  const getGoalTypeBadgeColor = (type: string) => {
    const colors: Record<string, string> = {
      daily: 'bg-blue-500',
      weekly: 'bg-green-500',
      monthly: 'bg-purple-500',
      project: 'bg-orange-500',
      habit: 'bg-pink-500',
      custom: 'bg-gray-500',
    };
    return colors[type] || 'bg-gray-500';
  };

  const handleLike = async () => {
    try {
      await addReaction.mutateAsync({
        checkInId: checkIn.id,
        data: { type: 'like' },
      });
    } catch (error) {
      // Error already handled by mutation
    }
  };

  const handleSubmitComment = async () => {
    if (!commentText.trim()) {
      toast.error('Comment cannot be empty');
      return;
    }

    try {
      await addComment.mutateAsync({
        checkInId: checkIn.id,
        data: { content: commentText },
      });
      setCommentText('');
      setShowCommentInput(false);
    } catch (error) {
      // Error already handled by mutation
    }
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <Avatar>
              <AvatarFallback>{getUserInitials()}</AvatarFallback>
            </Avatar>
            <div>
              <p className="font-semibold">{checkIn.username}</p>
              <p className="text-sm text-muted-foreground">
                {formatDistanceToNow(new Date(checkIn.created_at), { addSuffix: true })}
              </p>
            </div>
          </div>
          {checkIn.goal && (
            <Badge className={`${getGoalTypeBadgeColor(checkIn.goal.goal_type)} text-white`}>
              {checkIn.goal.goal_type}
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {checkIn.goal && (
          <div>
            <h3 className="font-semibold">{checkIn.goal.title}</h3>
            {checkIn.goal.description && (
              <p className="text-sm text-muted-foreground">{checkIn.goal.description}</p>
            )}
          </div>
        )}
        {checkIn.content && (
          <p className="text-sm">{checkIn.content}</p>
        )}
        <div className="flex items-center gap-4 pt-2 border-t">
          <Button
            variant="ghost"
            size="sm"
            onClick={handleLike}
            disabled={addReaction.isPending}
            className="gap-2"
          >
            <Heart className="h-4 w-4" />
            <span>{checkIn.reaction_count || 0}</span>
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setShowCommentInput(!showCommentInput)}
            className="gap-2"
          >
            <MessageCircle className="h-4 w-4" />
            <span>{checkIn.comment_count || 0}</span>
          </Button>
        </div>
        {showCommentInput && (
          <div className="flex gap-2 pt-2">
            <Textarea
              placeholder="Write a comment..."
              value={commentText}
              onChange={(e) => setCommentText(e.target.value)}
              rows={2}
              className="flex-1"
            />
            <Button
              onClick={handleSubmitComment}
              disabled={addComment.isPending || !commentText.trim()}
              size="icon"
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
