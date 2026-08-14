import createClient from "openapi-fetch";

import type { paths } from "./generated/schema";

// Set in .env.local; see .env.example. No fallback default on purpose:
// fail loudly at startup instead of silently pointing at the wrong API.
const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
if (!baseUrl) {
  throw new Error("NEXT_PUBLIC_API_BASE_URL is not set. Copy .env.example to .env.local.");
}

export const apiClient = createClient<paths>({ baseUrl });
