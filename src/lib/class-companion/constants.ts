import type { DayOfWeek, SubjectIconName } from './types';
import { availableSubjectIcons as SIcons } from '@/components/class-companion/icons';


export const DAYS_OF_WEEK: DayOfWeek[] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

// Generates time slots from 00:00 to 23:30 in 30-minute intervals
export const TIME_SLOTS_30_MIN: string[] = Array.from({ length: 24 * 2 }, (_, i) => {
  const hour = Math.floor(i / 2);
  const minute = (i % 2) * 30;
  return `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}`;
});

// Default display range for timetable (e.g., 8 AM to 10 PM)
export const DEFAULT_DISPLAY_START_TIME = "08:00";
export const DEFAULT_DISPLAY_END_TIME = "22:00";

export const AVAILABLE_SUBJECT_ICONS: SubjectIconName[] = SIcons;

export const CLASS_COLORS = [
  'bg-red-200', 'bg-blue-200', 'bg-green-200', 'bg-yellow-200', 'bg-purple-200', 
  'bg-pink-200', 'bg-indigo-200', 'bg-teal-200', 'bg-orange-200'
];
