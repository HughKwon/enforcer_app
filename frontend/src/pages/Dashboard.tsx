import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Skeleton } from '@/components/ui/skeleton';
import { CheckInCard } from '@/components/CheckInCard';
import { useFeed, useFollowingFeed, useCirclesFeed } from '@/hooks/useFeed';

function FeedSkeleton() {
  return (
    <div className="space-y-4">
      {Array.from({ length: 3 }).map((_, i) => (
        <div key={i} className="space-y-3 p-4 border rounded-lg">
          <div className="flex items-center space-x-4">
            <Skeleton className="h-12 w-12 rounded-full" />
            <div className="space-y-2 flex-1">
              <Skeleton className="h-4 w-[250px]" />
              <Skeleton className="h-4 w-[200px]" />
            </div>
          </div>
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-[300px]" />
        </div>
      ))}
    </div>
  );
}

export function Dashboard() {
  console.log('Dashboard component rendering');
  const { data: allFeed, isLoading: allFeedLoading } = useFeed();
  const { data: followingFeed, isLoading: followingFeedLoading } = useFollowingFeed();
  const { data: circlesFeed, isLoading: circlesFeedLoading } = useCirclesFeed();

  console.log('Dashboard data:', { allFeed, followingFeed, circlesFeed });

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Feed</h1>
        <p className="text-muted-foreground">
          See what your accountability buddies and circles are up to
        </p>
      </div>

      <Tabs defaultValue="all" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="all">All Feed</TabsTrigger>
          <TabsTrigger value="following">Following</TabsTrigger>
          <TabsTrigger value="circles">Circles</TabsTrigger>
        </TabsList>

        <TabsContent value="all" className="space-y-4 mt-6">
          {allFeedLoading ? (
            <FeedSkeleton />
          ) : allFeed && allFeed.length > 0 ? (
            allFeed.map((checkIn) => (
              <CheckInCard key={checkIn.id} checkIn={checkIn} />
            ))
          ) : (
            <div className="text-center py-12">
              <p className="text-muted-foreground">No check-ins yet. Start by creating a goal!</p>
            </div>
          )}
        </TabsContent>

        <TabsContent value="following" className="space-y-4 mt-6">
          {followingFeedLoading ? (
            <FeedSkeleton />
          ) : followingFeed && followingFeed.length > 0 ? (
            followingFeed.map((checkIn) => (
              <CheckInCard key={checkIn.id} checkIn={checkIn} />
            ))
          ) : (
            <div className="text-center py-12">
              <p className="text-muted-foreground">
                No check-ins from people you follow. Start following buddies to see their progress!
              </p>
            </div>
          )}
        </TabsContent>

        <TabsContent value="circles" className="space-y-4 mt-6">
          {circlesFeedLoading ? (
            <FeedSkeleton />
          ) : circlesFeed && circlesFeed.length > 0 ? (
            circlesFeed.map((checkIn) => (
              <CheckInCard key={checkIn.id} checkIn={checkIn} />
            ))
          ) : (
            <div className="text-center py-12">
              <p className="text-muted-foreground">
                No circle activity yet. Join or create a circle to see group check-ins!
              </p>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
