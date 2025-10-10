
"use client";

import { useContext } from 'react';
import { AuthContext } from '@/contexts/auth-provider';
import type { LoginFormData } from '@/lib/schemas/auth'; // Ensure this is imported if needed by context type

// Infer the context type from AuthContext if possible, or define explicitly
type AuthContextType = ReturnType<typeof useContext<typeof AuthContext>>;


export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
