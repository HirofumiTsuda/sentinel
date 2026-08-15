import Link from "next/link";

import type { components } from "@/lib/api/generated/schema";

type Status = components["schemas"]["Status"];
type Priority = components["schemas"]["Priority"];

type EntityCardProps = {
  title: string;
  status: Status;
  description?: string | null;
  /** Only stories and tasks carry a priority; the badge is omitted without one. */
  priority?: Priority;
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
  priority,
  href,
}: EntityCardProps) {
  const body = (
    <>
      <div className="flex items-center justify-between gap-4">
        <span className="font-medium text-black dark:text-zinc-50">
          {title}
        </span>
        <span className="flex shrink-0 items-center gap-2">
          {priority && (
            <span
              className={`rounded-full px-2 py-0.5 text-xs font-medium ${PRIORITY_STYLES[priority]}`}
            >
              {PRIORITY_LABELS[priority]}
            </span>
          )}
          <span className="text-sm text-zinc-500 dark:text-zinc-400">
            {STATUS_LABELS[status]}
          </span>
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
// Typing these as Record over the generated unions means adding a status or a
// priority to the backend breaks the build here until the label is added too.
const STATUS_LABELS: Record<Status, string> = {
  todo: "Todo",
  in_progress: "In progress",
  done: "Done",
};

const PRIORITY_LABELS: Record<Priority, string> = {
  high: "High",
  mid: "Mid",
  low: "Low",
};

// Only high is coloured: the badge is there to make the exceptions stand out,
// not to paint every card.
const PRIORITY_STYLES: Record<Priority, string> = {
  high: "bg-red-500/10 text-red-700 dark:text-red-400",
  mid: "bg-black/[.06] text-zinc-600 dark:bg-white/[.08] dark:text-zinc-400",
  low: "bg-black/[.06] text-zinc-500 dark:bg-white/[.08] dark:text-zinc-500",
};
