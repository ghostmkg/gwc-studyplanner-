import { سوالات } from '@/lib/quiz/questions-data'; // Using the provided name
import { QuizClient } from '@/components/quiz/quiz-client';
import { AppHeader } from '@/components/class-companion/header';
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from '@/components/ui/button';
import Link from 'next/link';
import { Footer } from '@/components/layout/footer';


export async function generateStaticParams() {
  return سوالات.map((category) => ({
    categorySlug: category.slug,
  }));
}

interface QuizPageProps {
  params: {
    categorySlug: string;
  };
}

export default function QuizPage({ params }: QuizPageProps) {
  const { categorySlug } = params;
  const categoryData = سوالات.find(cat => cat.slug === categorySlug);

  if (!categoryData) {
    return (
       <>
        <AppHeader />
        <main className="quiz-body-container flex-grow">
          <div className="text-center">
            <Alert variant="destructive" className="max-w-md mx-auto">
              {/* Using a generic SVG for triangle to avoid lucide-react import here if not already used */}
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
              <AlertTitle>Category Not Found</AlertTitle>
              <AlertDescription>
                The quiz category you are looking for does not exist.
              </AlertDescription>
            </Alert>
            <Button asChild className="mt-6">
              <Link href="/quiz">Back to Quiz Categories</Link>
            </Button>
          </div>
        </main>
        <Footer />
      </>
    );
  }
  // The QuizClient will handle the actual quiz UI and logic
  return <QuizClient category={categoryData} categorySlug={categorySlug} />;
}
