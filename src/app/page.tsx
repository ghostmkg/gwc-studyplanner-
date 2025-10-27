
"use client";

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/use-auth';
import { AppHeader } from '@/components/class-companion/header';
import { ClassForm } from '@/components/class-companion/class-form';
import { Timetable } from '@/components/class-companion/timetable';
import { StudyTimeSuggester } from '@/components/class-companion/study-time-suggester';
import type { ClassScheduleItem } from '@/lib/class-companion/types';
import { sortClasses } from '@/lib/class-companion/utils';
import { useToast } from "@/hooks/use-toast";
import { Loader2 } from 'lucide-react';
import { db } from '@/lib/firebase/clientApp';
import { collection, doc, getDocs, setDoc, deleteDoc, query } from 'firebase/firestore';
import { Footer } from '@/components/layout/footer';


export default function ClassCompanionPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [classes, setClasses] = useState<ClassScheduleItem[]>([]);
  const [firestoreLoading, setFirestoreLoading] = useState(true);
  const [isUpdating, setIsUpdating] = useState(false); // For add/delete operations
  const { toast } = useToast();

  useEffect(() => {
    if (!authLoading && !user) {
      router.replace('/login');
    }
  }, [user, authLoading, router]);

  useEffect(() => {
    if (user && !authLoading) {
      const fetchClasses = async () => {
        setFirestoreLoading(true);
        try {
          const timetableColRef = collection(db, `users/${user.uid}/timetable`);
          const q = query(timetableColRef);
          const querySnapshot = await getDocs(q);
          const fetchedClasses: ClassScheduleItem[] = [];
          querySnapshot.forEach((doc) => {
            fetchedClasses.push({ id: doc.id, ...(doc.data() as Omit<ClassScheduleItem, 'id'>) });
          });
          setClasses(sortClasses(fetchedClasses));
        } catch (error) {
          console.error("Error fetching classes from Firestore:", error);
          toast({
            title: "Error Loading Timetable",
            description: "Could not fetch your classes. Please try again.",
            variant: "destructive",
          });
          setClasses([]);
        } finally {
          setFirestoreLoading(false);
        }
      };
      fetchClasses();
    } else if (!user && !authLoading) {
      setClasses([]);
      setFirestoreLoading(false);
    }
  }, [user, authLoading, toast]);

  const handleAddClass = useCallback(async (newClass: ClassScheduleItem) => {
    if (!user) {
      toast({ title: "Not Authenticated", description: "You must be logged in to add classes.", variant: "destructive" });
      return;
    }
    setIsUpdating(true);
    try {
      const classDocRef = doc(db, `users/${user.uid}/timetable`, newClass.id);
      const { id, ...classData } = newClass;
      await setDoc(classDocRef, classData);
      setClasses(prevClasses => sortClasses([...prevClasses, newClass]));
      toast({
        title: "Class Added",
        description: `${newClass.name} has been saved.`,
      });
    } catch (error) {
      console.error("Error adding class to Firestore:", error);
      toast({
        title: "Error Adding Class",
        description: "Could not save the class. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsUpdating(false);
    }
  }, [user, toast]);
  
  const handleDeleteClass = useCallback(async (id: string) => {
    if (!user) {
      toast({ title: "Not Authenticated", description: "You must be logged in to delete classes.", variant: "destructive" });
      return;
    }
    setIsUpdating(true);
    const classToDelete = classes.find(c => c.id === id);
    setClasses(prevClasses => sortClasses(prevClasses.filter(c => c.id !== id)));

    try {
      const classDocRef = doc(db, `users/${user.uid}/timetable`, id);
      await deleteDoc(classDocRef);
      toast({
          title: "Class Removed",
          description: `${classToDelete?.name || 'The class'} has been removed.`,
      });
    } catch (error) {
      console.error("Error deleting class from Firestore:", error);
      if (classToDelete) {
        setClasses(prevClasses => sortClasses([...prevClasses, classToDelete]));
      }
      toast({
        title: "Error Removing Class",
        description: "Could not remove the class. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsUpdating(false);
    }
  }, [user, toast, classes]);

  if (authLoading || (!user && !authLoading && !firestoreLoading)) {
    return (
      <div className="min-h-screen bg-background flex flex-col items-center justify-center">
        <Loader2 className="h-12 w-12 animate-spin text-primary mb-4" />
        <p className="text-muted-foreground">Loading your Class Companion...</p>
      </div>
    );
  }
  
  if (user && firestoreLoading) {
     return (
      <div className="min-h-screen bg-background flex flex-col items-center justify-center">
        <AppHeader /> {/* Show header even when loading timetable */}
        <main className="flex-grow container mx-auto flex items-center justify-center">
          <div className="text-center">
            <Loader2 className="h-12 w-12 animate-spin text-primary mb-4" />
            <p className="text-muted-foreground">Preparing your timetable...</p>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen bg-background">
      <AppHeader />
      <main className="flex-grow container mx-auto py-8 px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8">
          <aside className="md:col-span-1 space-y-6">
            <ClassForm onAddClass={handleAddClass} existingClasses={classes} />
            <StudyTimeSuggester classSchedule={classes} />
          </aside>
          <section className="md:col-span-2">
            <Timetable classes={classes} onDeleteClass={handleDeleteClass} isUpdating={isUpdating} />
          </section>
        </div>
      </main>
      <Footer />
    </div>
  );
}
