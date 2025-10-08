
"use client";

import type { ReactNode, Dispatch, SetStateAction } from 'react';
import React, { createContext, useState, useEffect, useCallback } from 'react';
import { type User, onAuthStateChanged, signOut as firebaseSignOut, signInWithEmailAndPassword as firebaseSignInWithEmailAndPassword, GoogleAuthProvider, signInWithPopup } from 'firebase/auth';
import { auth } from '@/lib/firebase/clientApp';
import type { LoginFormData } from '@/lib/schemas/auth';
import { useToast } from "@/hooks/use-toast";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  signInWithEmail: (data: LoginFormData) => Promise<void>;
  signInWithBarcode: (barcodeValue: string) => Promise<void>;
  signInWithGoogle: () => Promise<void>; // New method
  signOutUser: () => Promise<void>;
  setError: Dispatch<SetStateAction<string | null>>;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

// IMPORTANT: For barcode demo to work, create a user in your Firebase project:
// Email: barcodeuser@example.com
// Password: password123
const DEMO_BARCODE_USER_EMAIL = "barcodeuser@example.com";
const DEMO_BARCODE_USER_PASSWORD = "password123";
const DEMO_BARCODE_VALUE_1 = "8918";
const DEMO_BARCODE_VALUE_2 = "8946";


export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      setLoading(false);
    }, (err) => {
      console.error("Auth state change error:", err);
      let friendlyMessage = "Failed to get authentication status.";
      if ((err as any).code === 'auth/invalid-api-key' || (err as any).code === 'auth/api-key-not-valid') {
        friendlyMessage = "Invalid Firebase API Key. Please check your .env or Firebase configuration.";
      } else if ((err as any).code === 'auth/network-request-failed') {
        friendlyMessage = "Network error. Please check your internet connection and Firebase configuration.";
      }
      setError(friendlyMessage);
      toast({ title: "Authentication Error", description: friendlyMessage, variant: "destructive"});
      setLoading(false);
    });
    return () => unsubscribe();
  }, [toast]);

  const signInWithEmail = useCallback(async (data: LoginFormData) => {
    setLoading(true);
    setError(null);
    try {
      await firebaseSignInWithEmailAndPassword(auth, data.email, data.password);
      toast({ title: "Login Successful", description: "Welcome back!"});
    } catch (err: any) {
      console.error("Sign in error:", err);
      let errorMessage = err.message || "Failed to sign in.";
      if (err.code === 'auth/invalid-credential') {
        errorMessage = "Invalid email or password. Please try again.";
      } else if (err.code === 'auth/invalid-api-key' || err.code === 'auth/api-key-not-valid') {
        errorMessage = "Firebase API Key is not valid. Please check your .env or Firebase configuration.";
      } else if (err.code === 'auth/network-request-failed') {
        errorMessage = "Network error. Please check your internet connection and try again.";
      }
      setError(errorMessage);
      toast({ title: "Login Failed", description: errorMessage, variant: "destructive"});
    } finally {
      // setLoading(false); // onAuthStateChanged handles final loading state
    }
  }, [toast]);

  const signInWithBarcode = useCallback(async (barcodeValue: string) => {
    setLoading(true);
    setError(null);
    if (barcodeValue === DEMO_BARCODE_VALUE_1 || barcodeValue === DEMO_BARCODE_VALUE_2) {
      try {
        await firebaseSignInWithEmailAndPassword(auth, DEMO_BARCODE_USER_EMAIL, DEMO_BARCODE_USER_PASSWORD);
        toast({ title: "Barcode Login Successful", description: `Welcome, ${DEMO_BARCODE_USER_EMAIL}!` });
      } catch (err: any) {
        console.error("Barcode Sign in error (demo user):", err);
        let errorMessage = err.message || "Failed to sign in with barcode.";
        if (err.code === 'auth/invalid-credential' || err.code === 'auth/user-not-found' || err.code === 'auth/wrong-password') {
             errorMessage = `Demo user ${DEMO_BARCODE_USER_EMAIL} not found or password incorrect. Please create it in your Firebase console with password '${DEMO_BARCODE_USER_PASSWORD}'.`;
        } else if (err.code === 'auth/invalid-api-key' || err.code === 'auth/api-key-not-valid') {
            errorMessage = "Firebase API Key is not valid. Please check your .env or Firebase configuration.";
        } else if (err.code === 'auth/network-request-failed') {
          errorMessage = "Network error. Please check your internet connection and try again.";
        }
        setError(errorMessage);
        toast({ title: "Barcode Login Failed", description: errorMessage, variant: "destructive" });
      } finally {
        // setLoading(false); // onAuthStateChanged handles final loading state
      }
    } else {
      setError("Invalid barcode value.");
      toast({ title: "Barcode Login Failed", description: "Invalid barcode value entered.", variant: "destructive" });
      setLoading(false); // Explicitly set loading false as no Firebase call was made for auth state change
    }
  }, [toast]);

  const signInWithGoogle = useCallback(async () => {
    setLoading(true);
    setError(null);
    const provider = new GoogleAuthProvider();
    try {
      await signInWithPopup(auth, provider);
      toast({ title: "Google Sign-In Successful", description: "Welcome!" });
    } catch (err: any) {
      console.error("Google Sign-in error:", err);
      let errorMessage = "Failed to sign in with Google. Please try again.";
      if (err.code === 'auth/popup-closed-by-user' || err.code === 'auth/cancelled-popup-request') {
        errorMessage = "Google Sign-In was cancelled.";
      } else if (err.code === 'auth/popup-blocked' || err.code === 'auth/popup-blocked-by-browser') {
        errorMessage = "Google Sign-In popup was blocked by the browser. Please disable your pop-up blocker and try again.";
      } else if (err.code === 'auth/account-exists-with-different-credential') {
        errorMessage = "An account already exists with this email address using a different sign-in method.";
      } else if (err.code === 'auth/invalid-api-key' || err.code === 'auth/api-key-not-valid') {
        errorMessage = "Firebase API Key is not valid for Google Sign-In. Please check your Firebase configuration.";
      } else if (err.code === 'auth/network-request-failed') {
        errorMessage = "Network error during Google Sign-In. Please check your internet connection.";
      }
      setError(errorMessage);
      toast({ title: "Google Sign-In Failed", description: errorMessage, variant: "destructive" });
    } finally {
      // setLoading(false); // onAuthStateChanged handles this
    }
  }, [toast]);

  const signOutUser = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      await firebaseSignOut(auth);
      toast({ title: "Logged Out", description: "You have been successfully logged out."});
    } catch (err: any) {
      console.error("Sign out error:", err);
      let errorMessage = err.message || "Failed to sign out.";
       if (err.code === 'auth/invalid-api-key' || err.code === 'auth/api-key-not-valid') {
        errorMessage = "Firebase API Key is not valid. Please check your .env or Firebase configuration before signing out.";
      } else if (err.code === 'auth/network-request-failed') {
        errorMessage = "Network error during sign out. Please check your internet connection.";
      }
      setError(errorMessage);
      toast({ title: "Logout Failed", description: errorMessage, variant: "destructive"});
    } finally {
      // setLoading(false); // onAuthStateChanged handles final loading state
    }
  }, [toast]);

  const value = {
    user,
    loading,
    error,
    signInWithEmail,
    signInWithBarcode,
    signInWithGoogle,
    signOutUser,
    setError,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
