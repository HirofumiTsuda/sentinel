import Link from "next/link";

import type { components } from "@/lib/api/generated/schema";

type Status = components["schemas"]["Status"];

type EntityCardProps = {
  title: string;
  status: Status;
  description?: string | null;
  /** Renders the card as a link when the entity has a page to open. */
  href?: string;
};

// Every level of the hierarchy (project, charter, story, task) shows the same
// title/status/description summary, so they share one card. Levels that have no
// detail page yet simply omit `href` and render as a static card.
export function EntityCard({
  title,
  status,
  description,
  href,
}: EntityCardProps) {
  const body = (
    <>
      <div className="flex items-center justify-between gap-4">
        <span className="font-medium text-black dark:text-zinc-50">
          {title}
        </span>
        <span className="text-sm text-zinc-500 dark:text-zinc-400">
          {STATUS_LABELS[status]}
        </span>
      </div>
      {description && (
        <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
          {description}
        </p>
      )}
    </>
  );

  const base = "rounded-lg border border-black/[.08] p-4 dark:border-white/[.145]";

  if (!href) {
    return <div className={base}>{body}</div>;
  }

  return (
    <Link
      href={href}
      className={`${base} block transition-colors hover:bg-black/[.04] dark:hover:bg-white/[.06]`}
    >
      {body}
    </Link>
  );
}

// The API's raw values are snake_case; keep the display strings in one place.
const STATUS_LABELS: Record<Status, string> = {
  todo: "Todo",
  in_progress: "In progress",
  done: "Done",
};
