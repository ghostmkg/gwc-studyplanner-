import type { LucideIcon } from 'lucide-react';

export type DayOfWeek = "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday" | "Saturday" | "Sunday";

export type SubjectIconName = 
  | 'Default' 
  | 'Literature' 
  | 'Science' 
  | 'ComputerScience' 
  | 'Psychology' 
  | 'Physics' 
  | 'Math'
  | 'Art'
  | 'Drama'
  | 'Politics'
  | 'Geography'
  | 'Economics'
  | 'Languages'
  | 'Music'
  | 'Film'
  | 'History'
  | 'Philosophy';

export interface ClassScheduleItem {
  id: string;
  name: string;
  day: DayOfWeek;
  startTime: string; // "HH:mm" format e.g. "09:00"
  endTime: string;   // "HH:mm" format e.g. "10:30"
  location: string;
  iconName: SubjectIconName;
  color?: string; // Optional color for the class block
}

export interface BreakItem {
  id: string;
  day: DayOfWeek;
  startTime: string;
  endTime: string;
  durationMinutes: number;
}

// For GenAI flow input
export interface AIClassScheduleItem {
  className: string;
  dayOfWeek: string; // Matches GenAI schema
  startTime: string; // e.g., "9:00 AM" - needs conversion if UI uses "HH:mm"
  endTime: string;   // e.g., "10:00 AM"
  location: string;
}

export interface StudyTimeSuggestion {
  dayOfWeek: string;
  startTime: string;
  endTime: string;
  reason: string;
}
