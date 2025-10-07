import type { LucideIcon } from 'lucide-react';
import { BookOpen, Beaker, Laptop, Brain, Atom, Sigma, Palette, Drama, Landmark, Globe, Calculator, Languages, Music, Film, History, LightbulbIcon as PhilosophyIcon, Briefcase, School, Users, BarChart } from 'lucide-react';
import type { SubjectIconName } from '@/lib/class-companion/types';

export const subjectIcons: Record<SubjectIconName, LucideIcon> = {
  Default: BookOpen,
  Literature: BookOpen,
  Science: Beaker,
  ComputerScience: Laptop,
  Psychology: Brain,
  Physics: Atom,
  Math: Sigma,
  Art: Palette,
  Drama: Drama,
  Politics: Landmark,
  Geography: Globe,
  Economics: Calculator, // Can also use BarChart or Briefcase
  Languages: Languages,
  Music: Music,
  Film: Film,
  History: History,
  Philosophy: PhilosophyIcon,
};

export const getSubjectIcon = (iconName?: SubjectIconName): LucideIcon => {
  return subjectIcons[iconName || 'Default'] || BookOpen;
};

export const availableSubjectIcons = Object.keys(subjectIcons) as SubjectIconName[];
