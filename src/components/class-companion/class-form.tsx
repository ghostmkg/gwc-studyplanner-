
"use client";

import type { FC } from 'react';
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PlusCircle, Trash2 } from "lucide-react";
import type { ClassScheduleItem, DayOfWeek, SubjectIconName } from "@/lib/class-companion/types";
import { DAYS_OF_WEEK, TIME_SLOTS_30_MIN, AVAILABLE_SUBJECT_ICONS, CLASS_COLORS } from "@/lib/class-companion/constants";
import { getSubjectIcon, subjectIcons } from './icons';
import { checkOverlap, timeToMinutes } from '@/lib/class-companion/utils';
import { useToast } from '@/hooks/use-toast';

const classFormSchema = z.object({
  name: z.string().min(1, "Class name is required"),
  day: z.enum(DAYS_OF_WEEK),
  startTime: z.string().min(1, "Start time is required"),
  endTime: z.string().min(1, "End time is required"),
  location: z.string().optional(),
  iconName: z.enum(AVAILABLE_SUBJECT_ICONS),
}).refine(data => timeToMinutes(data.startTime) < timeToMinutes(data.endTime), {
  message: "End time must be after start time",
  path: ["endTime"],
});

type ClassFormData = z.infer<typeof classFormSchema>;

interface ClassFormProps {
  onAddClass: (newClass: ClassScheduleItem) => void;
  existingClasses: ClassScheduleItem[];
}

export const ClassForm: FC<ClassFormProps> = ({ onAddClass, existingClasses }) => {
  const { toast } = useToast();
  const form = useForm<ClassFormData>({
    resolver: zodResolver(classFormSchema),
    defaultValues: {
      name: "",
      day: "Monday",
      startTime: "09:00",
      endTime: "10:00",
      location: "",
      iconName: "Default",
    },
  });

  const onSubmit = (data: ClassFormData) => {
    const newClassData = {
      ...data,
      location: data.location || "N/A",
    };

    if (checkOverlap(newClassData, existingClasses)) {
      toast({
        title: "Overlap Detected",
        description: "This class overlaps with an existing class on the same day.",
        variant: "destructive",
      });
      return;
    }
    
    const randomColor = CLASS_COLORS[Math.floor(Math.random() * CLASS_COLORS.length)];

    onAddClass({
      id: crypto.randomUUID(),
      ...newClassData,
      color: randomColor,
    });
    form.reset();
    toast({
      title: "Class Added",
      description: `${data.name} has been added to your timetable.`,
    });
  };

  const IconComponent = getSubjectIcon(form.watch('iconName'));

  return (
    <Card className="shadow-lg">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <PlusCircle className="text-primary" /> Add New Class
        </CardTitle>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Class Name</FormLabel>
                  <FormControl>
                    <Input placeholder="e.g., Calculus 101" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="day"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Day of Week</FormLabel>
                  <Select onValueChange={field.onChange} defaultValue={field.value}>
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="Select a day" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {DAYS_OF_WEEK.map((day) => (
                        <SelectItem key={day} value={day}>
                          {day}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />

            <div className="grid grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="startTime"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Start Time</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select start time" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent className="max-h-60 overflow-y-auto">
                        {TIME_SLOTS_30_MIN.map((time) => (
                          <SelectItem key={`start-${time}`} value={time}>
                            {time}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="endTime"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>End Time</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select end time" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent className="max-h-60 overflow-y-auto">
                        {TIME_SLOTS_30_MIN.map((time) => (
                          <SelectItem key={`end-${time}`} value={time}>
                            {time}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <FormField
              control={form.control}
              name="location"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Location (Optional)</FormLabel>
                  <FormControl>
                    <Input placeholder="e.g., Room 3B, Online" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            
            <FormField
              control={form.control}
              name="iconName"
              render={({ field }) => (
                <FormItem>
                  <FormLabel className="flex items-center gap-2">
                    Subject Icon <IconComponent className="w-4 h-4" />
                  </FormLabel>
                  <Select onValueChange={field.onChange} defaultValue={field.value}>
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="Select an icon" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent className="max-h-60 overflow-y-auto">
                      {AVAILABLE_SUBJECT_ICONS.map((iconName) => {
                        const CurrentIcon = subjectIcons[iconName];
                        return (
                          <SelectItem key={iconName} value={iconName} className="flex items-center">
                             <CurrentIcon className="w-4 h-4 mr-2 inline-block" /> {iconName}
                          </SelectItem>
                        );
                      })}
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />

            <Button type="submit" className="w-full">
              <PlusCircle className="mr-2 h-4 w-4" /> Add Class
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
};
