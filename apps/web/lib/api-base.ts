export function getApiBase() {
  if (typeof window === "undefined") {
    return (
      process.env.API_INTERNAL_BASE_URL ||
      getPublicApiBase() ||
      "http://localhost:8000"
    );
  }

  return getPublicApiBase();
}

export function getPublicApiBase() {
  return process.env.NEXT_PUBLIC_API_BASE_URL || "";
}
