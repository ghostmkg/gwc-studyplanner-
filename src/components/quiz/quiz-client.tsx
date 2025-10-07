"use client";

import type { FC } from 'react';
import React, { useState, useEffect, useCallback, useMemo } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/use-auth';
import { db } from '@/lib/firebase/clientApp';
import { collection, addDoc, serverTimestamp } from 'firebase/firestore';
import { useToast } from "@/hooks/use-toast";
import type { QuizCategory, Question, QuizAttempt } from '@/lib/quiz/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { Progress } from "@/components/ui/progress";


const QUIZ_TIME_LIMIT_PER_QUESTION = 15; // seconds

interface QuizClientProps {
  category: QuizCategory;
  categorySlug: string;
}

interface AnsweredQuestionRecord {
  questionText: string;
  options: string[];
  selectedOption: string;
  correctAnswerIndex: number;
  isCorrect: boolean;
  timeTaken?: number; // Optional: time taken for this question
}

export const QuizClient: FC<QuizClientProps> = ({ category, categorySlug }) => {
  const { user } = useAuth();
  const { toast } = useToast();
  const router = useRouter();

  const [numberOfQuestions, setNumberOfQuestions] = useState(10);
  const [quizStarted, setQuizStarted] = useState(false);
  
  const allQuestions = useMemo(() => category.questions, [category.questions]);
  
  const [shuffledQuestions, setShuffledQuestions] = useState<Question[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [isAnswerCorrect, setIsAnswerCorrect] = useState<boolean | null>(null);
  const [score, setScore] = useState(0);
  const [timeLeft, setTimeLeft] = useState(QUIZ_TIME_LIMIT_PER_QUESTION);
  const [timerId, setTimerId] = useState<NodeJS.Timeout | null>(null);
  const [quizOver, setQuizOver] = useState(false);
  const [showFeedback, setShowFeedback] = useState(false);
  const [answeredQuestionsHistory, setAnsweredQuestionsHistory] = useState<AnsweredQuestionRecord[]>([]);
  const [isSavingResult, setIsSavingResult] = useState(false);


  const startQuiz = useCallback(() => {
    const selectedNum = Math.min(numberOfQuestions, allQuestions.length);
    const questionsToPlay = [...allQuestions].sort(() => 0.5 - Math.random()).slice(0, selectedNum);
    setShuffledQuestions(questionsToPlay);
    setCurrentQuestionIndex(0);
    setSelectedAnswer(null);
    setIsAnswerCorrect(null);
    setScore(0);
    setTimeLeft(QUIZ_TIME_LIMIT_PER_QUESTION);
    setQuizOver(false);
    setShowFeedback(false);
    setAnsweredQuestionsHistory([]);
    setQuizStarted(true);
  }, [numberOfQuestions, allQuestions]);

  useEffect(() => {
    if (quizStarted && !quizOver && !showFeedback) {
      const timer = setInterval(() => {
        setTimeLeft((prevTime) => {
          if (prevTime <= 1) {
            clearInterval(timer);
            handleTimeOut();
            return 0;
          }
          return prevTime - 1;
        });
      }, 1000);
      setTimerId(timer);
      return () => clearInterval(timer);
    }
  }, [currentQuestionIndex, quizStarted, quizOver, showFeedback]);

  const currentQuestion = useMemo(() => {
    return shuffledQuestions[currentQuestionIndex];
  }, [shuffledQuestions, currentQuestionIndex]);


  const handleAnswerSelection = (optionIndex: number) => {
    if (showFeedback) return; // Don't allow selection if feedback is shown

    if (timerId) clearInterval(timerId);
    setShowFeedback(true);
    setSelectedAnswer(optionIndex);
    const correct = currentQuestion.correctAnswer === optionIndex;
    setIsAnswerCorrect(correct);

    const answeredRecord: AnsweredQuestionRecord = {
        questionText: currentQuestion.question,
        options: currentQuestion.options,
        selectedOption: currentQuestion.options[optionIndex],
        correctAnswerIndex: currentQuestion.correctAnswer,
        isCorrect: correct,
        timeTaken: QUIZ_TIME_LIMIT_PER_QUESTION - timeLeft,
    };
    setAnsweredQuestionsHistory(prev => [...prev, answeredRecord]);

    if (correct) {
      setScore((prevScore) => prevScore + 1);
    }
  };

  const handleTimeOut = () => {
    if (showFeedback) return;
    if (timerId) clearInterval(timerId);
    setShowFeedback(true);
    setSelectedAnswer(null); // No answer selected
    setIsAnswerCorrect(false); // Timed out counts as incorrect

     const answeredRecord: AnsweredQuestionRecord = {
        questionText: currentQuestion.question,
        options: currentQuestion.options,
        selectedOption: "Timed Out",
        correctAnswerIndex: currentQuestion.correctAnswer,
        isCorrect: false,
        timeTaken: QUIZ_TIME_LIMIT_PER_QUESTION,
    };
    setAnsweredQuestionsHistory(prev => [...prev, answeredRecord]);
  };

  const saveQuizAttempt = async () => {
    if (!user) return;
    setIsSavingResult(true);
    try {
      const attemptData: QuizAttempt = {
        userId: user.uid,
        categorySlug: categorySlug,
        categoryName: category.category,
        score: score,
        totalQuestionsAttempted: shuffledQuestions.length,
        answeredQuestions: answeredQuestionsHistory,
        timestamp: serverTimestamp(),
      };
      await addDoc(collection(db, `users/${user.uid}/quizAttempts`), attemptData);
      toast({
        title: "Quiz Result Saved",
        description: "Your quiz performance has been saved.",
      });
    } catch (error) {
      console.error("Error saving quiz attempt:", error);
      toast({
        title: "Error Saving Result",
        description: "Could not save your quiz result. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsSavingResult(false);
    }
  };


  const handleNextQuestion = () => {
    setShowFeedback(false);
    setSelectedAnswer(null);
    setIsAnswerCorrect(null);
    setTimeLeft(QUIZ_TIME_LIMIT_PER_QUESTION);
    if (currentQuestionIndex < shuffledQuestions.length - 1) {
      setCurrentQuestionIndex((prevIndex) => prevIndex + 1);
    } else {
      setQuizOver(true);
      if (user) {
        saveQuizAttempt();
      }
    }
  };

  const handleTryAgainSameCategory = () => {
    // Reset state for a new quiz with the same settings
    startQuiz();
  };
  
  const questionOptions = [5, 10, 15, 20, 25];


  if (!quizStarted) {
    return (
      <div className="quiz-view-container">
        <Card className="config-container quiz-box w-full">
          <CardHeader>
            <CardTitle className="config-title">Configure Quiz: {category.category}</CardTitle>
            <CardDescription>Select the number of questions for your quiz.</CardDescription>
          </CardHeader>
          <CardContent className="config-option">
            <Label htmlFor="num-questions" className="option-title sr-only">Number of Questions</Label>
             <Select
                value={String(numberOfQuestions)}
                onValueChange={(value) => setNumberOfQuestions(Number(value))}
              >
                <SelectTrigger id="num-questions" className="w-full md:w-[280px] mx-auto mb-6">
                  <SelectValue placeholder="Select number of questions" />
                </SelectTrigger>
                <SelectContent>
                  {questionOptions.map(num => (
                    <SelectItem key={num} value={String(num)} disabled={num > allQuestions.length}>
                      {num} Questions {num > allQuestions.length ? `(Only ${allQuestions.length} available)` : ''}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            <Button onClick={startQuiz} size="lg" className="w-full">Start Quiz</Button>
          </CardContent>
           <CardFooter>
             <Button variant="outline" onClick={() => router.push('/quiz')} className="w-full">
                Back to Categories
             </Button>
           </CardFooter>
        </Card>
      </div>
    );
  }


  if (quizOver) {
    return (
      <div className="quiz-view-container">
        <div className="result-container quiz-box">
          <Image 
            src="https://placehold.co/110x110.png" 
            alt="Quiz Over" 
            width={110} 
            height={110} 
            className="result-img"
            data-ai-hint="trophy celebration" 
          />
          <h2 className="result-title">Quiz Completed!</h2>
          <p className="result-message">
            You answered <b>{score}</b> out of <b>{shuffledQuestions.length}</b> questions correctly.
            {score / shuffledQuestions.length >= 0.8 ? " Excellent work!" : (score / shuffledQuestions.length >= 0.5 ? " Good effort!" : " Keep practicing!")}
          </p>
          <div className="result-buttons mt-6 flex flex-col sm:flex-row gap-3 justify-center">
            <Button onClick={handleTryAgainSameCategory} size="lg" disabled={isSavingResult}>
              {isSavingResult ? "Saving..." : "Try Again (Same Category)"}
            </Button>
            <Button variant="outline" size="lg" onClick={() => router.push('/quiz')}>
              Back to Categories
            </Button>
          </div>
        </div>
      </div>
    );
  }

  if (!currentQuestion) {
    // This case should ideally not be reached if questions are loaded
    return (
        <div className="quiz-view-container">
             <Alert variant="destructive">
                <AlertTriangle className="h-4 w-4" />
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>No questions available for this category or an error occurred.</AlertDescription>
            </Alert>
            <Button onClick={() => router.push('/quiz')} className="mt-4">Back to Categories</Button>
        </div>
    );
  }
  
  const progressPercentage = ((currentQuestionIndex + 1) / shuffledQuestions.length) * 100;


  return (
    <div className="quiz-view-container">
        <div className="quiz-container quiz-box">
            <header className="quiz-header">
                <h2 className="quiz-title">{category.category} Quiz</h2>
                <div className={`quiz-timer ${timeLeft === 0 && !showFeedback ? 'timed-out' : ''}`}>
                    <span className="material-symbols-rounded">timer</span>
                    <p className="timer-duration">{timeLeft}s</p>
                </div>
            </header>

            <Progress value={progressPercentage} className="w-full h-2 rounded-none" />


            <div className="quiz-content">
                <h1 className="question-text">
                  {currentQuestion.question}
                </h1>
                <ul className="answer-options">
                {currentQuestion.options.map((option, index) => {
                    let itemClass = "answer-option";
                    if (showFeedback) {
                        itemClass += " disabled";
                        if (index === currentQuestion.correctAnswer) {
                            itemClass += " correct";
                        } else if (index === selectedAnswer) {
                            itemClass += " incorrect";
                        }
                    }
                    return (
                    <li
                        key={index}
                        className={itemClass}
                        onClick={() => handleAnswerSelection(index)}
                        role="button"
                        tabIndex={showFeedback ? -1 : 0}
                        aria-pressed={selectedAnswer === index}
                        onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') handleAnswerSelection(index);}}
                    >
                        <span className="option-text">{option}</span>
                        {showFeedback && index === currentQuestion.correctAnswer && (
                          <span className="material-symbols-rounded">check_circle</span>
                        )}
                        {showFeedback && index === selectedAnswer && index !== currentQuestion.correctAnswer && (
                          <span className="material-symbols-rounded">cancel</span>
                        )}
                    </li>
                    );
                })}
                </ul>
            </div>
            <div className="quiz-footer">
                <p className="question-status">
                    <b>{currentQuestionIndex + 1}</b> of <b>{shuffledQuestions.length}</b> Questions
                </p>
                {showFeedback && (
                <Button onClick={handleNextQuestion} className="next-question-btn">
                    {currentQuestionIndex < shuffledQuestions.length - 1 ? "Next" : "Finish"}
                    <span className="material-symbols-rounded">arrow_right_alt</span>
                </Button>
                )}
            </div>
        </div>
    </div>
  );
};

// Helper Icon for Alert (if not using Lucide directly in Alert component)
const AlertTriangle: FC<React.SVGProps<SVGSVGElement>> = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    {...props}
  >
    <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
    <line x1="12" y1="9" x2="12" y2="13" />
    <line x1="12" y1="17" x2="12.01" y2="17" />
  </svg>
);
