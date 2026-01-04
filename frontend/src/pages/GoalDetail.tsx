import { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { ArrowLeft, Plus } from 'lucide-react';
import { useGoal, useGoalCheckIns, useCreateCheckIn } from '@/hooks/useGoals';
import { checkInSchema, CheckInFormData } from '@/lib/validations';
import { format } from 'date-fns';

export function GoalDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [checkInDialogOpen, setCheckInDialogOpen] = useState(false);

  const { data: goal, isLoading: goalLoading } = useGoal(id!);
  const { data: checkIns, isLoading: checkInsLoading } = useGoalCheckIns(id!);
  const createCheckIn = useCreateCheckIn();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<CheckInFormData>({
    resolver: zodResolver(checkInSchema),
    defaultValues: {
      goal_type: goal?.goal_type,
    },
  });

  const onSubmit = async (data: CheckInFormData) => {
    try {
      await createCheckIn.mutateAsync({
        goalId: Number(id),
        data: {
          content: data.content,
        },
      });
      setCheckInDialogOpen(false);
      reset();
    } catch (error) {
      // Error handled by mutation
    }
  };

  if (goalLoading) {
    return (
      <div className="max-w-4xl mx-auto space-y-6">
        <Skeleton className="h-8 w-64" />
        <Card>
          <CardHeader>
            <Skeleton className="h-6 w-full" />
            <Skeleton className="h-4 w-full" />
          </CardHeader>
          <CardContent>
            <Skeleton className="h-20 w-full" />
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!goal) {
    return (
      <div className="max-w-4xl mx-auto">
        <Card>
          <CardHeader>
            <CardTitle>Goal Not Found</CardTitle>
            <CardDescription>The goal you're looking for doesn't exist.</CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={() => navigate('/goals')}>Back to Goals</Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const requiresContent = goal.goal_type === 'project' || goal.goal_type === 'habit';

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => navigate('/goals')}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <h1 className="text-3xl font-bold">{goal.title}</h1>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-start justify-between">
            <div>
              <CardTitle>Goal Details</CardTitle>
              <CardDescription className="mt-2">{goal.description}</CardDescription>
            </div>
            <Badge className={goal.is_active ? 'bg-green-500' : 'bg-gray-500'}>
              {goal.is_active ? 'Active' : 'Completed'}
            </Badge>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p className="font-semibold">Type</p>
              <Badge>{goal.goal_type}</Badge>
            </div>
            {goal.start_date && (
              <div>
                <p className="font-semibold">Start Date</p>
                <p>{format(new Date(goal.start_date), 'PP')}</p>
              </div>
            )}
            {goal.end_date && (
              <div>
                <p className="font-semibold">End Date</p>
                <p>{format(new Date(goal.end_date), 'PP')}</p>
              </div>
            )}
            <div>
              <p className="font-semibold">Total Check-ins</p>
              <p>{checkIns?.length || 0}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Check-ins</h2>
        <Dialog open={checkInDialogOpen} onOpenChange={setCheckInDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              Add Check-in
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Create Check-in</DialogTitle>
              <DialogDescription>
                {requiresContent
                  ? 'Describe your progress on this goal.'
                  : 'Add a check-in to track your progress.'}
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={handleSubmit(onSubmit)}>
              <div className="space-y-4 py-4">
                <div className="space-y-2">
                  <Label htmlFor="content">
                    Content {requiresContent && '*'}
                  </Label>
                  <Textarea
                    id="content"
                    placeholder={
                      requiresContent
                        ? 'Describe what you accomplished...'
                        : 'Add notes (optional)...'
                    }
                    rows={4}
                    {...register('content')}
                    aria-invalid={!!errors.content}
                  />
                  {errors.content && (
                    <p className="text-sm text-destructive">{errors.content.message}</p>
                  )}
                </div>
              </div>
              <DialogFooter>
                <Button type="button" variant="outline" onClick={() => setCheckInDialogOpen(false)}>
                  Cancel
                </Button>
                <Button type="submit" disabled={createCheckIn.isPending}>
                  {createCheckIn.isPending ? 'Submitting...' : 'Submit Check-in'}
                </Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <div className="space-y-4">
        {checkInsLoading ? (
          <Card>
            <CardContent className="p-6">
              <Skeleton className="h-20 w-full" />
            </CardContent>
          </Card>
        ) : checkIns && checkIns.length > 0 ? (
          checkIns.map((checkIn) => (
            <Card key={checkIn.id}>
              <CardContent className="pt-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    {checkIn.content && <p className="text-sm">{checkIn.content}</p>}
                  </div>
                  <p className="text-sm text-muted-foreground">
                    {format(new Date(checkIn.created_at), 'PPp')}
                  </p>
                </div>
              </CardContent>
            </Card>
          ))
        ) : (
          <Card>
            <CardContent className="py-12 text-center">
              <p className="text-muted-foreground">
                No check-ins yet. Add your first check-in to start tracking progress!
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
