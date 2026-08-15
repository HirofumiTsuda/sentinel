import Link from "next/link";

// Rendered both for unmatched URLs and for notFound() calls inside a page —
// in this app they mean the same thing to the reader, so they share one screen.
export default function NotFound() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 px-6 dark:bg-black">
      <main className="flex max-w-md flex-col items-start gap-4">
        <p className="text-sm font-medium tracking-wide text-zinc-500 uppercase dark:text-zinc-400">
          404
        </p>
        <h1 className="text-3xl font-semibold tracking-tight text-black dark:text-zinc-50">
          Not found
        </h1>
        <p className="text-zinc-600 dark:text-zinc-400">
          This page doesn&apos;t exist. It may have been deleted, or the address
          may be wrong.
        </p>
        <Link
          href="/"
          className="mt-2 rounded-lg border border-black/[.08] px-4 py-2 text-sm font-medium text-black transition-colors hover:bg-black/[.04] dark:border-white/[.145] dark:text-zinc-50 dark:hover:bg-white/[.06]"
        >
          Back to projects
        </Link>
      </main>
    </div>
  );
}
