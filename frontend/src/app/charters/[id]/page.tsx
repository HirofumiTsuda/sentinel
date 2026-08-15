import Link from "next/link";

import { EntityCard } from "@/components/entity-card";
import { apiClient } from "@/lib/api/client";
import { unwrap } from "@/lib/api/unwrap";

export default async function CharterPage({
  params,
}: PageProps<"/charters/[id]">) {
  const { id } = await params;

  // Both endpoints 404 on an unknown charter, so they can be fetched together
  // and either result will send the page to notFound().
  const [charterResult, storiesResult] = await Promise.all([
    apiClient.GET("/api/v1/charters/{charter_id}", {
      params: { path: { charter_id: id } },
    }),
    apiClient.GET("/api/v1/charters/{charter_id}/stories", {
      params: { path: { charter_id: id } },
    }),
  ]);

  const charter = unwrap(charterResult, "charter");
  const stories = unwrap(storiesResult, "stories");

  return (
    <div className="min-h-screen bg-zinc-50 px-6 py-16 dark:bg-black">
      <main className="mx-auto flex max-w-2xl flex-col gap-8">
        <div className="flex flex-col gap-4">
          <Link
            href={`/projects/${charter.project_id}`}
            className="text-sm text-zinc-500 transition-colors hover:text-black dark:text-zinc-400 dark:hover:text-zinc-50"
          >
            ← Project
          </Link>

          <div className="flex items-baseline justify-between gap-4">
            <h1 className="text-3xl font-semibold tracking-tight text-black dark:text-zinc-50">
              {charter.title}
            </h1>
            <span className="text-sm text-zinc-500 dark:text-zinc-400">
              {charter.status}
            </span>
          </div>

          {charter.description && (
            <p className="text-zinc-600 dark:text-zinc-400">
              {charter.description}
            </p>
          )}
        </div>

        <section className="flex flex-col gap-3">
          <h2 className="text-sm font-medium tracking-wide text-zinc-500 uppercase dark:text-zinc-400">
            Stories
          </h2>

          {stories.length === 0 ? (
            <p className="text-zinc-600 dark:text-zinc-400">No stories yet.</p>
          ) : (
            <ul className="flex flex-col gap-3">
              {stories.map((story) => (
                <li key={story.id}>
                  {/* No story detail page yet, so these stay unlinked. */}
                  <EntityCard
                    title={story.title}
                    status={story.status}
                    description={story.description}
                    priority={story.priority}
                  />
                </li>
              ))}
            </ul>
          )}
        </section>
      </main>
    </div>
  );
}
