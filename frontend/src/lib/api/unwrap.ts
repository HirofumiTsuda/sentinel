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
  if (result.response.status === 404) {
    notFound();
  }
  if (result.data === undefined) {
    throw new Error(
      `Failed to load ${resource} (HTTP ${result.response.status})`,
    );
  }
  return result.data;
}
