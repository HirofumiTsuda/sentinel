import Link from "next/link";

import { EntityCard } from "@/components/entity-card";
import { apiClient } from "@/lib/api/client";
import { unwrap } from "@/lib/api/unwrap";

export default async function ProjectPage({
  params,
}: PageProps<"/projects/[id]">) {
  const { id } = await params;

  // Both endpoints 404 on an unknown project, so they can be fetched together
  // and either result will send the page to notFound().
  const [projectResult, chartersResult] = await Promise.all([
    apiClient.GET("/api/v1/projects/{project_id}", {
      params: { path: { project_id: id } },
    }),
    apiClient.GET("/api/v1/projects/{project_id}/charters", {
      params: { path: { project_id: id } },
    }),
  ]);

  const project = unwrap(projectResult, "project");
  const charters = unwrap(chartersResult, "charters");

  return (
    <div className="min-h-screen bg-zinc-50 px-6 py-16 dark:bg-black">
      <main className="mx-auto flex max-w-2xl flex-col gap-8">
        <div className="flex flex-col gap-4">
          <Link
            href="/"
            className="text-sm text-zinc-500 transition-colors hover:text-black dark:text-zinc-400 dark:hover:text-zinc-50"
          >
            ← Projects
          </Link>

          <div className="flex items-baseline justify-between gap-4">
            <h1 className="text-3xl font-semibold tracking-tight text-black dark:text-zinc-50">
              {project.title}
            </h1>
            <span className="text-sm text-zinc-500 dark:text-zinc-400">
              {project.status}
            </span>
          </div>

          {project.description && (
            <p className="text-zinc-600 dark:text-zinc-400">
              {project.description}
            </p>
          )}
        </div>

        <section className="flex flex-col gap-3">
          <h2 className="text-sm font-medium tracking-wide text-zinc-500 uppercase dark:text-zinc-400">
            Charters
          </h2>

          {charters.length === 0 ? (
            <p className="text-zinc-600 dark:text-zinc-400">No charters yet.</p>
          ) : (
            <ul className="flex flex-col gap-3">
              {charters.map((charter) => (
                <li key={charter.id}>
                  {/* No charter detail page yet, so these stay unlinked. */}
                  <EntityCard
                    title={charter.title}
                    status={charter.status}
                    description={charter.description}
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
