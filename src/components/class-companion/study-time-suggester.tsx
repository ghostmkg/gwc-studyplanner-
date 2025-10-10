
"use client";

import type { FC } from 'react';
import { useState } from 'react';
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Brain, Loader2, AlertTriangle } from "lucide-react";
import { suggestStudyTimes, type SuggestStudyTimesInput, type SuggestStudyTimesOutput } from '@/ai/flows/suggest-study-times';
import type { ClassScheduleItem, StudyTimeSuggestion } from '@/lib/class-companion/types';
import { convertToAISchedule } from '@/lib/class-companion/utils';
import { useToast } from "@/hooks/use-toast";

interface StudyTimeSuggesterProps {
  classSchedule: ClassScheduleItem[];
}

export const StudyTimeSuggester: FC<StudyTimeSuggesterProps> = ({ classSchedule }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [additionalTasks, setAdditionalTasks] = useState("");
  const [preferredStudyStyle, setPreferredStudyStyle] = useState("");
  const [suggestions, setSuggestions] = useState<SuggestStudyTimesOutput | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  const handleSubmit = async () => {
    if (classSchedule.length === 0) {
      toast({
        title: "No Classes",
        description: "Please add some classes to your timetable first.",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    setError(null);
    setSuggestions(null);

    const aiSchedule = convertToAISchedule(classSchedule);
    const input: SuggestStudyTimesInput = {
      classSchedule: aiSchedule,
      additionalTasks: additionalTasks || undefined,
      preferredStudyStyle: preferredStudyStyle || undefined,
    };

    try {
      const result = await suggestStudyTimes(input);
      setSuggestions(result);
    } catch (e) {
      console.error("Error fetching study suggestions:", e);
      setError("Failed to get study suggestions. Please try again.");
      toast({
        title: "Error",
        description: "Failed to get study suggestions. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="mt-6 shadow-lg">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Brain className="text-accent" /> AI Study Planner
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground mb-4">
          Get AI-powered suggestions for optimal study times based on your schedule.
        </p>
        <Dialog open={isOpen} onOpenChange={setIsOpen}>
          <DialogTrigger asChild>
            <Button className="w-full bg-accent hover:bg-accent/90 text-accent-foreground">
              Get Study Suggestions
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[525px]">
            <DialogHeader>
              <DialogTitle>Study Time Preferences</DialogTitle>
              <DialogDescription>
                Provide additional details to help us tailor your study plan.
              </DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="additional-tasks" className="text-right col-span-1">
                  Additional Tasks
                </Label>
                <Textarea
                  id="additional-tasks"
                  value={additionalTasks}
                  onChange={(e) => setAdditionalTasks(e.target.value)}
                  placeholder="e.g., Work part-time, gym sessions, club meetings"
                  className="col-span-3"
                />
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="study-style" className="text-right col-span-1">
                  Study Style
                </Label>
                <Input
                  id="study-style"
                  value={preferredStudyStyle}
                  onChange={(e) => setPreferredStudyStyle(e.target.value)}
                  placeholder="e.g., Pomodoro, short breaks, group study"
                  className="col-span-3"
                />
              </div>
            </div>

            {isLoading && (
              <div className="flex justify-center items-center my-4">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
                <p className="ml-2">Generating suggestions...</p>
              </div>
            )}

            {error && (
              <div className="my-4 p-3 bg-destructive/10 border border-destructive text-destructive rounded-md flex items-center gap-2">
                <AlertTriangle className="h-5 w-5" />
                <p>{error}</p>
              </div>
            )}

            {suggestions && (
              <div className="my-4 max-h-[300px] overflow-y-auto p-1">
                <h4 className="font-semibold mb-2 text-lg">Suggested Study Plan:</h4>
                <p className="text-sm text-muted-foreground mb-3">{suggestions.overallSummary}</p>
                <ul className="space-y-2">
                  {suggestions.suggestedStudyTimes.map((slot, index) => (
                    <li key={index} className="p-3 bg-secondary rounded-md border">
                      <p className="font-medium">
                        {slot.dayOfWeek}: {slot.startTime} - {slot.endTime}
                      </p>
                      <p className="text-xs text-muted-foreground">{slot.reason}</p>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setIsOpen(false)}>Cancel</Button>
              <Button type="button" onClick={handleSubmit} disabled={isLoading}>
                {isLoading ? "Thinking..." : "Suggest Times"}
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </CardContent>
    </Card>
  );
};
