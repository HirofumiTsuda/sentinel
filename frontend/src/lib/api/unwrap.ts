import { notFound } from "next/navigation";

type ApiResult<T> = {
  data?: T;
  response: Response;
};

/**
 * Unwraps an openapi-fetch result into its payload.
 *
 * Every page needs the same two branches — a missing row should render the 404
 * page, anything else is a genuine failure — so the decision lives here instead
 * of being restated at each call site. `resource` only labels the thrown error.
 */
export function unwrap<T>(result: ApiResult<T>, resource: string): T {
  // 404 means the row is missing; 422 means the id in the URL isn't even a
  // valid UUID, which FastAPI rejects before the route runs. Both mean the URL
  // points at nothing, so both belong on the not-found page rather than the
  // error page — a mistyped URL is not a server fault.
  if (result.response.status === 404 || result.response.status === 422) {
    notFound();
  }
  if (result.data === undefined) {
    throw new Error(
      `Failed to load ${resource} (HTTP ${result.response.status})`,
    );
  }
  return result.data;
}
