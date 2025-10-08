
"use client";

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { LoginForm } from '@/components/auth/login-form';
import { useAuth } from '@/hooks/use-auth';
import { Skeleton } from '@/components/ui/skeleton';
import { Loader2 } from 'lucide-react';

export default function LoginPage() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && user) {
      router.replace('/'); // Redirect to home if already logged in
    }
  }, [user, loading, router]);

  if (loading || (!loading && user)) { 
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-secondary p-4">
        <Loader2 className="h-12 w-12 animate-spin text-primary mb-4" />
        <p className="text-muted-foreground">Loading session...</p>
      </div>
    );
  }
  
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-secondary p-4">
      <LoginForm />
       <p className="mt-8 text-center text-sm text-muted-foreground">
        Login to manage your Class Companion.
      </p>
    </div>
  );
}
