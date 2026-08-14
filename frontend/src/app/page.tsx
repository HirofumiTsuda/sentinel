import Link from "next/link";

import { apiClient } from "@/lib/api/client";

export default async function Home() {
  const { data: projects, error } = await apiClient.GET("/api/v1/projects");

  if (error) {
    throw new Error("Failed to load projects");
  }

  return (
    <div className="min-h-screen bg-zinc-50 px-6 py-16 dark:bg-black">
      <main className="mx-auto flex max-w-2xl flex-col gap-8">
        <h1 className="text-3xl font-semibold tracking-tight text-black dark:text-zinc-50">
          sentinel
        </h1>

        {projects.length === 0 ? (
          <p className="text-zinc-600 dark:text-zinc-400">No projects yet.</p>
        ) : (
          <ul className="flex flex-col gap-3">
            {projects.map((project) => (
              <li key={project.id}>
                <Link
                  href={`/projects/${project.id}`}
                  className="block rounded-lg border border-black/[.08] p-4 transition-colors hover:bg-black/[.04] dark:border-white/[.145] dark:hover:bg-white/[.06]"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-black dark:text-zinc-50">
                      {project.title}
                    </span>
                    <span className="text-sm text-zinc-500 dark:text-zinc-400">
                      {project.status}
                    </span>
                  </div>
                  {project.description && (
                    <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
                      {project.description}
                    </p>
                  )}
                </Link>
              </li>
            ))}
          </ul>
        )}
      </main>
    </div>
  );
}
