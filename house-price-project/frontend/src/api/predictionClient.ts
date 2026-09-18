import type { PredictionRequest, PredictionResponse } from "../types/prediction";

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export class ApiError extends Error {}

export async function fetchLocations(): Promise<string[]> {
  try {
    const res = await fetch("/locations.json");
    if (!res.ok) throw new Error("Failed to load locations");
    return await res.json();
  } catch {
    return [];
  }
}

export async function predictPrice(payload: PredictionRequest): Promise<PredictionResponse> {
  let res: Response;
  try {
    res = await fetch(`${BASE_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  } catch (err) {
    throw new ApiError("Could not reach the prediction server. Is the backend running?");
  }

  if (!res.ok) {
    let detail = "Prediction request failed.";
    try {
      const body = await res.json();
      detail = body.detail ? JSON.stringify(body.detail) : detail;
    } catch {
      // ignore parse errors
    }
    throw new ApiError(detail);
  }

  return res.json();
}
