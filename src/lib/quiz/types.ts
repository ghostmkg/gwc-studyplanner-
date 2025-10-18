import type { Timestamp } from 'firebase/firestore';

export interface Question {
  question: string;
  options: string[];
  correctAnswer: number; // index of the correct option
}

export interface QuizCategory {
  category: string; // e.g., "Programming", "Geography"
  slug: string; // e.g., "programming", "geography"
  questions: Question[];
  icon?: string; // Optional: Lucide icon name or path to SVG
  description?: string; // Optional: short description of the category
}

export interface AnsweredQuestionRecord {
  questionText: string;
  options: string[];
  selectedOption: string; // The text of the selected option, or "Timed Out"
  correctAnswerIndex: number;
  isCorrect: boolean;
  timeTaken?: number; // Time taken for this question in seconds
}

export interface QuizAttempt {
  userId: string;
  categorySlug: string;
  categoryName: string;
  score: number;
  totalQuestionsAttempted: number;
  answeredQuestions: AnsweredQuestionRecord[];
  timestamp: Timestamp | ReturnType<typeof serverTimestamp>; // For Firestore
}
