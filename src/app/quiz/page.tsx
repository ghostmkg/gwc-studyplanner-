
import Link from 'next/link';
import { سوالات } from '@/lib/quiz/questions-data';
import { AppHeader } from '@/components/class-companion/header';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from '@/components/ui/button';
import { getSubjectIcon } from '@/components/class-companion/icons';
import type { SubjectIconName } from '@/lib/class-companion/types';
import { Footer } from '@/components/layout/footer';
import { ArrowRight } from 'lucide-react';

export default function QuizHomePage() {
  return (
    <div className="flex flex-col min-h-screen">
      <AppHeader />
      <main className="flex-grow container mx-auto px-4 py-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-5xl lg:text-6xl">
            Quiz Zone
          </h1>
          <p className="mt-4 text-lg leading-8 text-muted-foreground sm:text-xl">
            Test your knowledge across various subjects. Choose a category to begin!
          </p>
        </div>

        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {سوالات.map((category) => {
            const IconComponent = getSubjectIcon(category.icon as SubjectIconName || 'Default');
            return (
              <Card 
                key={category.slug} 
                className="flex flex-col overflow-hidden rounded-lg shadow-lg transition-all duration-300 ease-in-out hover:shadow-xl hover:scale-105 bg-card"
              >
                <CardHeader className="p-6">
                  <div className="flex items-center gap-4 mb-4">
                    <div className="p-3 rounded-lg bg-primary/10 text-primary">
                      <IconComponent className="h-8 w-8" />
                    </div>
                    <CardTitle className="text-2xl font-semibold leading-tight text-foreground">
                      {category.category}
                    </CardTitle>
                  </div>
                  <CardDescription className="text-sm text-muted-foreground min-h-[40px] line-clamp-2">
                    {category.description || `Test your knowledge in ${category.category}.`}
                  </CardDescription>
                </CardHeader>
                <CardContent className="flex-grow p-6 pt-0">
                  {/* You can add more details here if needed, e.g., number of questions */}
                  <p className="text-xs text-muted-foreground">
                    {category.questions.length} questions available.
                  </p>
                </CardContent>
                <CardFooter className="p-6 mt-auto bg-muted/30 dark:bg-muted/10">
                  <Button asChild className="w-full" size="lg" variant="default">
                    <Link href={`/quiz/${category.slug}`}>
                      Start Quiz <ArrowRight className="ml-2 h-5 w-5" />
                    </Link>
                  </Button>
                </CardFooter>
              </Card>
            );
          })}
        </div>
      </main>
      <Footer />
    </div>
  );
}
