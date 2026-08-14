import { EntityCard } from "@/components/entity-card";
import { apiClient } from "@/lib/api/client";
import { unwrap } from "@/lib/api/unwrap";

export default async function Home() {
  const projects = unwrap(
    await apiClient.GET("/api/v1/projects"),
    "projects",
  );

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
                <EntityCard
                  title={project.title}
                  status={project.status}
                  description={project.description}
                  href={`/projects/${project.id}`}
                />
              </li>
            ))}
          </ul>
        )}
      </main>
    </div>
  );
}
