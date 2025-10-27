import { BookMarked, Github } from 'lucide-react';

export function Footer() {
  return (
    <footer className="py-6 md:py-8 mt-auto border-t border-border">
      <div className="container mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <BookMarked className="h-6 w-6 text-primary" />
          <p className="text-sm text-muted-foreground">
            Class Companion & Quiz Zone
          </p>
        </div>
        <p className="text-sm text-muted-foreground">
          Built with Next.js, Firebase & Genkit.
        </p>
        {/* Optional: Add a link to your GitHub repo or portfolio */}
        {/* <a
          href="https://github.com/your-repo"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-2 text-sm text-muted-foreground hover:text-primary transition-colors"
        >
          <Github className="h-4 w-4" />
          View on GitHub
        </a> */}
      </div>
    </footer>
  );
}
