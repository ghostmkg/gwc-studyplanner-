
"use client";
import type { FC } from 'react';
import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { BookMarked, LogOut, UserCircle, Puzzle, LogIn } from 'lucide-react';
import { useAuth } from '@/hooks/use-auth';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { ThemeToggleButton } from '@/components/theme-toggle-button'; // Added
import { cn } from '@/lib/utils';

export const AppHeader: FC = () => {
  const { user, signOutUser, loading } = useAuth();
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 10);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header 
      className={cn(
        "sticky top-0 z-50 py-3 transition-all duration-300 ease-in-out",
        scrolled ? "bg-background/90 shadow-md backdrop-blur-lg" : "bg-transparent shadow-sm backdrop-blur-sm"
      )}
    >
      <div className="container mx-auto flex h-16 items-center justify-between">
        <Link href="/" className="flex items-center gap-3 group">
          <BookMarked className="h-8 w-8 text-primary transition-transform group-hover:scale-110" />
          <div>
            <h1 className="text-2xl font-bold text-primary">Class Companion</h1>
            <p className="text-xs text-muted-foreground hidden md:block">
              Your friendly timetable planner & study assistant
            </p>
          </div>
        </Link>
        
        <nav className="flex items-center gap-2 sm:gap-3">
          <Button variant="ghost" asChild className="text-sm sm:text-base">
            <Link href="/quiz" className="flex items-center gap-1.5">
              <Puzzle className="h-5 w-5" />
              <span className="hidden sm:inline">Quiz Zone</span>
            </Link>
          </Button>

          <ThemeToggleButton />

          {loading ? (
            <Skeleton className="h-10 w-10 rounded-full" />
          ) : user ? (
             <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="relative h-10 w-10 rounded-full p-0">
                  <Avatar className="h-10 w-10 border-2 border-primary/50 hover:border-primary transition-colors">
                    <AvatarImage src={user.photoURL || undefined} alt={user.displayName || user.email || 'User'} />
                    <AvatarFallback className="bg-primary text-primary-foreground">
                       <UserCircle size={24}/>
                    </AvatarFallback>
                  </Avatar>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56" align="end" forceMount>
                <DropdownMenuLabel className="font-normal">
                  <div className="flex flex-col space-y-1">
                    <p className="text-sm font-medium leading-none">My Account</p>
                    <p className="text-xs leading-none text-muted-foreground">
                      {user.email}
                    </p>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={signOutUser} className="cursor-pointer text-destructive focus:bg-destructive/10 focus:text-destructive">
                  <LogOut className="mr-2 h-4 w-4" />
                  <span>Log out</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          ) : (
            <Button asChild variant="outline">
              <Link href="/login">
                <LogIn className="mr-2 h-4 w-4" /> Login
              </Link>
            </Button>
          )}
        </nav>
      </div>
    </header>
  );
};
