import { FormEvent, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchLocations, predictPrice, ApiError } from "../api/predictionClient";
import type { PredictionRequest } from "../types/prediction";

type FormState = {
  location: string;
  carpet_area_sqft: string;
  floor_num: string;
  bathroom: string;
  balcony: string;
  furnishing: string;
  transaction: string;
  ownership: string;
  facing: string;
};

const initialState: FormState = {
  location: "",
  carpet_area_sqft: "",
  floor_num: "",
  bathroom: "",
  balcony: "",
  furnishing: "Semi-Furnished",
  transaction: "Resale",
  ownership: "Freehold",
  facing: "East",
};

export default function PredictionForm() {
  const [form, setForm] = useState<FormState>(initialState);
  const [locations, setLocations] = useState<string[]>([]);
  const [fieldErrors, setFieldErrors] = useState<Partial<Record<keyof FormState, string>>>({});
  const [apiError, setApiError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetchLocations().then(setLocations);
  }, []);

  function update<K extends keyof FormState>(key: K, value: string) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  function validate(): boolean {
    const errors: Partial<Record<keyof FormState, string>> = {};

    if (!form.location.trim()) errors.location = "Please select or enter a location.";
    if (!form.carpet_area_sqft || Number(form.carpet_area_sqft) <= 0)
      errors.carpet_area_sqft = "Area must be greater than 0.";
    if (form.floor_num === "" || Number(form.floor_num) < -1)
      errors.floor_num = "Enter a valid floor number.";
    if (form.bathroom === "" || Number(form.bathroom) < 0)
      errors.bathroom = "Enter the number of bathrooms.";
    if (form.balcony === "" || Number(form.balcony) < 0)
      errors.balcony = "Enter the number of balconies.";
    if (!form.furnishing) errors.furnishing = "Required.";
    if (!form.transaction) errors.transaction = "Required.";
    if (!form.ownership.trim()) errors.ownership = "Required.";

    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setApiError(null);

    if (!validate()) return;

    const payload: PredictionRequest = {
      location: form.location.trim(),
      carpet_area_sqft: Number(form.carpet_area_sqft),
      floor_num: Number(form.floor_num),
      bathroom: Number(form.bathroom),
      balcony: Number(form.balcony),
      furnishing: form.furnishing as PredictionRequest["furnishing"],
      transaction: form.transaction as PredictionRequest["transaction"],
      ownership: form.ownership.trim(),
      facing: form.facing.trim() || undefined,
    };

    setLoading(true);
    try {
      const result = await predictPrice(payload);
      navigate("/result", { state: { predictedPrice: result.predicted_price, form: payload } });
    } catch (err) {
      const message = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
      setApiError(message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="card form-grid" onSubmit={handleSubmit} noValidate>
      <div className="form-field full">
        <label htmlFor="location">Location</label>
        {locations.length > 0 ? (
          <select
            id="location"
            value={form.location}
            onChange={(e) => update("location", e.target.value)}
          >
            <option value="">Select a location…</option>
            {locations.map((loc) => (
              <option key={loc} value={loc}>
                {loc}
              </option>
            ))}
          </select>
        ) : (
          <input
            id="location"
            type="text"
            placeholder="e.g. Sector 12, Noida"
            value={form.location}
            onChange={(e) => update("location", e.target.value)}
          />
        )}
        {fieldErrors.location && <span className="error-text">{fieldErrors.location}</span>}
      </div>

      <div className="form-field">
        <label htmlFor="carpet_area_sqft">Carpet area (sqft)</label>
        <input
          id="carpet_area_sqft"
          type="number"
          min={1}
          value={form.carpet_area_sqft}
          onChange={(e) => update("carpet_area_sqft", e.target.value)}
        />
        {fieldErrors.carpet_area_sqft && (
          <span className="error-text">{fieldErrors.carpet_area_sqft}</span>
        )}
      </div>

      <div className="form-field">
        <label htmlFor="floor_num">Floor (0 = Ground)</label>
        <input
          id="floor_num"
          type="number"
          min={-1}
          value={form.floor_num}
          onChange={(e) => update("floor_num", e.target.value)}
        />
        {fieldErrors.floor_num && <span className="error-text">{fieldErrors.floor_num}</span>}
      </div>

      <div className="form-field">
        <label htmlFor="bathroom">Bathrooms</label>
        <input
          id="bathroom"
          type="number"
          min={0}
          value={form.bathroom}
          onChange={(e) => update("bathroom", e.target.value)}
        />
        {fieldErrors.bathroom && <span className="error-text">{fieldErrors.bathroom}</span>}
      </div>

      <div className="form-field">
        <label htmlFor="balcony">Balconies</label>
        <input
          id="balcony"
          type="number"
          min={0}
          value={form.balcony}
          onChange={(e) => update("balcony", e.target.value)}
        />
        {fieldErrors.balcony && <span className="error-text">{fieldErrors.balcony}</span>}
      </div>

      <div className="form-field">
        <label htmlFor="furnishing">Furnishing</label>
        <select
          id="furnishing"
          value={form.furnishing}
          onChange={(e) => update("furnishing", e.target.value)}
        >
          <option value="Furnished">Furnished</option>
          <option value="Semi-Furnished">Semi-Furnished</option>
          <option value="Unfurnished">Unfurnished</option>
        </select>
      </div>

      <div className="form-field">
        <label htmlFor="transaction">Transaction</label>
        <select
          id="transaction"
          value={form.transaction}
          onChange={(e) => update("transaction", e.target.value)}
        >
          <option value="New Property">New Property</option>
          <option value="Resale">Resale</option>
        </select>
      </div>

      <div className="form-field">
        <label htmlFor="ownership">Ownership</label>
        <input
          id="ownership"
          type="text"
          placeholder="Freehold"
          value={form.ownership}
          onChange={(e) => update("ownership", e.target.value)}
        />
        {fieldErrors.ownership && <span className="error-text">{fieldErrors.ownership}</span>}
      </div>

      <div className="form-field">
        <label htmlFor="facing">Facing</label>
        <select id="facing" value={form.facing} onChange={(e) => update("facing", e.target.value)}>
          <option value="East">East</option>
          <option value="West">West</option>
          <option value="North">North</option>
          <option value="South">South</option>
          <option value="North-East">North-East</option>
          <option value="South-West">South-West</option>
        </select>
      </div>

      {apiError && <div className="api-error">{apiError}</div>}

      <div className="submit-row">
        <button type="submit" className="primary" disabled={loading}>
          {loading ? "Predicting…" : "Predict price"}
        </button>
      </div>
    </form>
  );
}
