import type { ClassScheduleItem, AIClassScheduleItem, DayOfWeek } from './types';
import { TIME_SLOTS_30_MIN } from './constants';
import { format, parse } from 'date-fns';

export function timeToMinutes(time: string): number {
  const [hours, minutes] = time.split(':').map(Number);
  return hours * 60 + minutes;
}

export function minutesToTime(minutes: number): string {
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
}

export function getTimelinePosition(time: string, displayStartTime: string = "00:00"): number {
  const minutes = timeToMinutes(time) - timeToMinutes(displayStartTime);
  return (minutes / 30); // 30 minute intervals
}

export function getTimelineDuration(startTime: string, endTime: string): number {
  const durationMinutes = timeToMinutes(endTime) - timeToMinutes(startTime);
  return durationMinutes / 30; // 30 minute intervals
}

export function formatTimeForAI(time: string): string {
  // Converts "HH:mm" to "h:mm AM/PM" (e.g. "09:00" to "9:00 AM", "13:00" to "1:00 PM")
  try {
    const date = parse(time, 'HH:mm', new Date());
    return format(date, 'h:mm a');
  } catch (error) {
    console.error("Error formatting time for AI:", error);
    return time; // fallback
  }
}

export function convertToAISchedule(classes: ClassScheduleItem[]): AIClassScheduleItem[] {
  return classes.map(c => ({
    className: c.name,
    dayOfWeek: c.day,
    startTime: formatTimeForAI(c.startTime),
    endTime: formatTimeForAI(c.endTime),
    location: c.location,
  }));
}

export function sortClasses(classes: ClassScheduleItem[]): ClassScheduleItem[] {
  return [...classes].sort((a, b) => {
    if (a.day !== b.day) {
      const dayOrder = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
      return dayOrder.indexOf(a.day) - dayOrder.indexOf(b.day);
    }
    return timeToMinutes(a.startTime) - timeToMinutes(b.startTime);
  });
}

export function checkOverlap(newClass: Omit<ClassScheduleItem, 'id' | 'color'>, existingClasses: ClassScheduleItem[]): boolean {
  const newStartTime = timeToMinutes(newClass.startTime);
  const newEndTime = timeToMinutes(newClass.endTime);

  return existingClasses.some(existing => {
    if (existing.day !== newClass.day) return false;
    const existingStartTime = timeToMinutes(existing.startTime);
    const existingEndTime = timeToMinutes(existing.endTime);
    // Check for overlap: (StartA < EndB) and (StartB < EndA)
    return newStartTime < existingEndTime && existingStartTime < newEndTime;
  });
}
