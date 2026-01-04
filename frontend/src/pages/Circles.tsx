import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Plus, Users as UsersIcon } from 'lucide-react';
import { useCircles, useCreateCircle } from '@/hooks/useCircles';
import { circleSchema, CircleFormData } from '@/lib/validations';
import { Circle } from '@/types';

function CirclesSkeleton() {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {Array.from({ length: 3 }).map((_, i) => (
        <Card key={i}>
          <CardHeader>
            <Skeleton className="h-6 w-full" />
            <Skeleton className="h-4 w-full" />
          </CardHeader>
        </Card>
      ))}
    </div>
  );
}

function CircleCard({ circle }: { circle: Circle }) {
  const navigate = useNavigate();

  return (
    <Card className="cursor-pointer hover:shadow-md transition-shadow" onClick={() => navigate(`/circles/${circle.id}`)}>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          {circle.name}
          <Badge variant="secondary">
            <UsersIcon className="h-3 w-3 mr-1" />
            Circle
          </Badge>
        </CardTitle>
        {circle.description && (
          <CardDescription className="line-clamp-2">{circle.description}</CardDescription>
        )}
      </CardHeader>
      <CardContent>
        <Button variant="outline" className="w-full" onClick={(e) => {
          e.stopPropagation();
          navigate(`/circles/${circle.id}`);
        }}>
          View Circle
        </Button>
      </CardContent>
    </Card>
  );
}

export function Circles() {
  const [dialogOpen, setDialogOpen] = useState(false);
  const { data: circles, isLoading } = useCircles();
  const createCircle = useCreateCircle();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<CircleFormData>({
    resolver: zodResolver(circleSchema),
  });

  const onSubmit = async (data: CircleFormData) => {
    try {
      await createCircle.mutateAsync(data);
      setDialogOpen(false);
      reset();
    } catch (error) {
      // Error handled by mutation
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Circles</h1>
          <p className="text-muted-foreground">Join accountability groups to stay motivated</p>
        </div>
        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              Create Circle
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Create Circle</DialogTitle>
              <DialogDescription>
                Create a new accountability circle for you and your buddies.
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={handleSubmit(onSubmit)}>
              <div className="space-y-4 py-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Name *</Label>
                  <Input
                    id="name"
                    placeholder="e.g., Morning Runners"
                    {...register('name')}
                    aria-invalid={!!errors.name}
                  />
                  {errors.name && (
                    <p className="text-sm text-destructive">{errors.name.message}</p>
                  )}
                </div>
                <div className="space-y-2">
                  <Label htmlFor="description">Description</Label>
                  <Textarea
                    id="description"
                    placeholder="Describe your circle..."
                    rows={3}
                    {...register('description')}
                  />
                </div>
              </div>
              <DialogFooter>
                <Button type="button" variant="outline" onClick={() => setDialogOpen(false)}>
                  Cancel
                </Button>
                <Button type="submit" disabled={createCircle.isPending}>
                  {createCircle.isPending ? 'Creating...' : 'Create Circle'}
                </Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {isLoading ? (
        <CirclesSkeleton />
      ) : circles && circles.length > 0 ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {circles.map((circle) => (
            <CircleCard key={circle.id} circle={circle} />
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="py-12 text-center">
            <UsersIcon className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
            <p className="text-muted-foreground">No circles yet. Create one to get started!</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
