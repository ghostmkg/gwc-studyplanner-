
"use client";

import type { FC } from 'react';
import React, { useRef, useMemo } from 'react';
import type { ClassScheduleItem, BreakItem, DayOfWeek } from '@/lib/class-companion/types';
import { DAYS_OF_WEEK, TIME_SLOTS_30_MIN, DEFAULT_DISPLAY_START_TIME, DEFAULT_DISPLAY_END_TIME } from '@/lib/class-companion/constants';
import { getTimelinePosition, getTimelineDuration, timeToMinutes, minutesToTime } from '@/lib/class-companion/utils';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Download, Coffee, Trash2, Loader2, CalendarDays } from 'lucide-react';
import { getSubjectIcon } from './icons';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { cn } from '@/lib/utils';

interface TimetableProps {
  classes: ClassScheduleItem[];
  onDeleteClass: (id: string) => void;
  isUpdating?: boolean; // Optional prop to indicate if an add/delete operation is in progress
}

const calculateBreaks = (classesForDay: ClassScheduleItem[], day: DayOfWeek, dayStartTime: string, dayEndTime: string): BreakItem[] => {
  const breaks: BreakItem[] = [];
  const sortedClasses = [...classesForDay].sort((a, b) => timeToMinutes(a.startTime) - timeToMinutes(b.startTime));
  
  let lastEndTimeMinutes = timeToMinutes(dayStartTime);

  if (sortedClasses.length === 0) {
    const duration = timeToMinutes(dayEndTime) - lastEndTimeMinutes;
    if (duration > 60) {
      breaks.push({
        id: `break-${day}-full`,
        day,
        startTime: minutesToTime(lastEndTimeMinutes),
        endTime: dayEndTime,
        durationMinutes: duration,
      });
    }
    return breaks;
  }

  // Break before first class
  const firstClassStartTimeMinutes = timeToMinutes(sortedClasses[0].startTime);
  if (firstClassStartTimeMinutes > lastEndTimeMinutes) {
    const duration = firstClassStartTimeMinutes - lastEndTimeMinutes;
    if (duration > 60) {
      breaks.push({
        id: `break-${day}-start`,
        day,
        startTime: minutesToTime(lastEndTimeMinutes),
        endTime: sortedClasses[0].startTime,
        durationMinutes: duration,
      });
    }
  }
  lastEndTimeMinutes = timeToMinutes(sortedClasses[0].endTime);

  // Breaks between classes
  for (let i = 0; i < sortedClasses.length - 1; i++) {
    const currentClassEndTimeMinutes = timeToMinutes(sortedClasses[i].endTime);
    const nextClassStartTimeMinutes = timeToMinutes(sortedClasses[i+1].startTime);
    
    if (nextClassStartTimeMinutes > currentClassEndTimeMinutes) {
      const duration = nextClassStartTimeMinutes - currentClassEndTimeMinutes;
      if (duration > 60) {
         breaks.push({
          id: `break-${day}-${i}`,
          day,
          startTime: sortedClasses[i].endTime,
          endTime: sortedClasses[i+1].startTime,
          durationMinutes: duration,
        });
      }
    }
    lastEndTimeMinutes = Math.max(lastEndTimeMinutes, timeToMinutes(sortedClasses[i+1].endTime));
  }
  
  // Break after last class
   const dayEndTimeMinutes = timeToMinutes(dayEndTime);
   if (dayEndTimeMinutes > lastEndTimeMinutes) {
    const duration = dayEndTimeMinutes - lastEndTimeMinutes;
    if (duration > 60) {
      breaks.push({
        id: `break-${day}-end`,
        day,
        startTime: minutesToTime(lastEndTimeMinutes),
        endTime: dayEndTime,
        durationMinutes: duration,
      });
    }
  }

  return breaks;
};

const formatBreakDuration = (durationMinutes: number): string => {
  const hours = Math.floor(durationMinutes / 60);
  const minutes = durationMinutes % 60;
  let durationStr = "";
  if (hours > 0) durationStr += `${hours}h `;
  if (minutes > 0) durationStr += `${minutes}m`;
  return durationStr.trim() || "Break";
};

export const Timetable: FC<TimetableProps> = ({ classes, onDeleteClass, isUpdating }) => {
  const timetableRef = useRef<HTMLDivElement>(null);

  const displayTimeSlots = useMemo(() => 
    TIME_SLOTS_30_MIN.filter(slot => slot >= DEFAULT_DISPLAY_START_TIME && slot <= DEFAULT_DISPLAY_END_TIME),
    []
  );
  const totalDisplaySlots = displayTimeSlots.length;


  const allItemsByDay = useMemo(() => {
    const itemsMap = new Map<DayOfWeek, (ClassScheduleItem | BreakItem)[]>();
    DAYS_OF_WEEK.forEach(day => {
      const classesForDay = classes.filter(c => c.day === day);
      const breaksForDay = calculateBreaks(classesForDay, day, DEFAULT_DISPLAY_START_TIME, DEFAULT_DISPLAY_END_TIME);
      itemsMap.set(day, [...classesForDay, ...breaksForDay].sort((a,b) => timeToMinutes(a.startTime) - timeToMinutes(b.startTime)));
    });
    return itemsMap;
  }, [classes]);


  const handleExportPDF = async () => {
    if (timetableRef.current) {
      // Temporarily remove delete buttons for PDF export
      const deleteButtons = timetableRef.current.querySelectorAll('.delete-class-btn');
      deleteButtons.forEach(btn => (btn as HTMLElement).style.display = 'none');
      
      const canvas = await html2canvas(timetableRef.current, { 
        scale: 2,
        logging: false,
        useCORS: true,
        backgroundColor: getComputedStyle(document.documentElement).getPropertyValue('--background').trim() === '0 0% 100%' ? '#FFFFFF' : '#111827', // Use theme background
      });

      // Restore delete buttons
      deleteButtons.forEach(btn => (btn as HTMLElement).style.display = '');

      const imgData = canvas.toDataURL('image/png');
      
      const pdf = new jsPDF({
        orientation: 'landscape',
        unit: 'pt',
        format: 'a4' 
      });

      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = pdf.internal.pageSize.getHeight();
      const imgProps = pdf.getImageProperties(imgData);
      const imgWidth = imgProps.width;
      const imgHeight = imgProps.height;
      
      const ratio = Math.min(pdfWidth / imgWidth, pdfHeight / imgHeight);
      const newImgWidth = imgWidth * ratio * 0.95; // Add some margin
      const newImgHeight = imgHeight * ratio * 0.95;

      const xOffset = (pdfWidth - newImgWidth) / 2;
      const yOffset = (pdfHeight - newImgHeight) / 2;

      pdf.addImage(imgData, 'PNG', xOffset, yOffset, newImgWidth, newImgHeight);
      pdf.save('timetable.pdf');
    }
  };
  
  const minRowHeight = 'min-h-[40px]';

  return (
    <Card className="shadow-xl w-full bg-card">
      <CardHeader className="flex flex-row items-center justify-between">
        <div className="flex items-center gap-2">
          <CalendarDays className="h-6 w-6 text-primary" />
          <CardTitle className="text-xl sm:text-2xl">Weekly Timetable</CardTitle>
        </div>
        <div className="flex items-center gap-2">
          {isUpdating && <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />}
          <Button onClick={handleExportPDF} variant="outline" size="sm" className="hidden sm:flex">
            <Download className="mr-2 h-4 w-4" /> Export PDF
          </Button>
           <Button onClick={handleExportPDF} variant="outline" size="icon" className="flex sm:hidden">
            <Download className="h-4 w-4" />
            <span className="sr-only">Export PDF</span>
          </Button>
        </div>
      </CardHeader>
      <CardContent className="p-0 sm:p-2 md:p-4">
        {classes.length === 0 && !isUpdating ? (
          <div className="text-center py-16 flex flex-col items-center justify-center text-muted-foreground">
            <Coffee size={48} className="mb-4 opacity-50" />
            <p className="text-lg font-medium">Your timetable is empty.</p>
            <p className="text-sm">Add some classes using the form to get started!</p>
          </div>
        ) : (
        <ScrollArea className="w-full">
          <div ref={timetableRef} className="grid grid-cols-[auto_repeat(7,1fr)] border border-border bg-card relative rounded-lg overflow-hidden">
            {/* Time Gutter */}
            <div className="sticky left-0 bg-card z-10 border-r border-border">
              <div className={`h-10 border-b border-border`}></div> {/* Empty corner cell */}
              {displayTimeSlots.map((time, index) => (
                (index % 2 === 0) && // Display time every hour
                <div key={`time-${time}`} className={`flex items-center justify-center text-xs text-muted-foreground ${minRowHeight} h-[80px] border-b border-border pr-1`}>
                  {time}
                </div>
              ))}
            </div>

            {/* Days Headers & Columns */}
            {DAYS_OF_WEEK.map((day) => (
              <div key={day} className="relative border-r border-border last:border-r-0 min-w-[80px] sm:min-w-[100px]">
                <div className={`h-10 flex items-center justify-center font-semibold text-sm border-b border-border sticky top-0 bg-card z-10`}>
                  <span className="hidden sm:inline">{day}</span>
                  <span className="sm:hidden">{day.substring(0,3)}</span>
                </div>
                {/* Grid lines for time slots */}
                {displayTimeSlots.map((_, slotIndex) => (
                  <div key={`${day}-slot-${slotIndex}`} className={`${minRowHeight} border-b border-border last:border-b-0`}></div>
                ))}

                {(allItemsByDay.get(day) || []).map((item) => {
                  const isClass = 'name' in item;
                  const Icon = isClass ? getSubjectIcon(item.iconName) : Coffee;
                  
                  const startMinutes = timeToMinutes(item.startTime);
                  const endMinutes = timeToMinutes(item.endTime);
                  const displayStartMinutes = timeToMinutes(DEFAULT_DISPLAY_START_TIME);
                  const displayEndMinutes = timeToMinutes(DEFAULT_DISPLAY_END_TIME);

                  // Ensure item is within the display range before calculating position/duration based on display range
                  if (endMinutes <= displayStartMinutes || startMinutes >= displayEndMinutes) {
                    return null; 
                  }
                  
                  const clampedStartTime = Math.max(startMinutes, displayStartMinutes);
                  const clampedEndTime = Math.min(endMinutes, displayEndMinutes);

                  const topOffsetSlots = (clampedStartTime - displayStartMinutes) / 30;
                  const durationSlots = (clampedEndTime - clampedStartTime) / 30;

                  if (durationSlots <= 0) return null;

                  const itemStyle = {
                    top: `${topOffsetSlots * 40}px`, 
                    height: `${durationSlots * 40}px`,
                  };

                  if (isClass) { // It's a ClassScheduleItem
                    return (
                      <div
                        key={item.id}
                        className={cn(
                          `absolute w-[calc(100%-4px)] left-[2px] p-1.5 rounded-md shadow-sm text-xs overflow-hidden transition-all duration-200 ease-in-out group`,
                          item.color || 'bg-primary/20', // Use a light variant of primary if no color
                          `text-neutral-800 dark:text-neutral-200` // Ensure text contrast on custom backgrounds
                        )}
                        style={itemStyle}
                        title={`${item.name} (${item.startTime} - ${item.endTime}) at ${item.location}`}
                      >
                        <div className="flex items-start justify-between">
                           <div className="font-semibold truncate flex-grow mr-1">{item.name}</div>
                           <Button 
                             variant="ghost" 
                             size="icon" 
                             className="delete-class-btn h-5 w-5 text-neutral-700 dark:text-neutral-300 hover:bg-destructive/20 hover:text-destructive opacity-50 group-hover:opacity-100 transition-opacity" 
                             onClick={() => onDeleteClass(item.id)}
                           >
                             <Trash2 className="h-3.5 w-3.5"/>
                           </Button>
                        </div>
                        <div className="truncate opacity-80 text-current">{item.location}</div>
                        <div className="truncate opacity-80 text-current text-[0.65rem]">{item.startTime} - {item.endTime}</div>
                        <Icon className="w-3.5 h-3.5 mt-0.5 opacity-80 text-current" />
                      </div>
                    );
                  } else { // It's a BreakItem
                    return (
                      <div
                        key={item.id}
                        className="absolute w-[calc(100%-4px)] left-[2px] px-1.5 py-1 rounded-md bg-accent/20 text-accent-foreground border border-dashed border-accent/50 flex flex-col items-center justify-center text-xs"
                        style={itemStyle}
                        title={`Break (${item.startTime} - ${item.endTime})`}
                      >
                        <Coffee className="w-4 h-4 mb-0.5 text-accent" />
                        <span className="font-medium text-accent dark:text-accent-foreground/80">{formatBreakDuration(item.durationMinutes)}</span>
                      </div>
                    );
                  }
                })}
              </div>
            ))}
          </div>
          <ScrollBar orientation="horizontal" />
        </ScrollArea>
        )}
      </CardContent>
    </Card>
  );
};

