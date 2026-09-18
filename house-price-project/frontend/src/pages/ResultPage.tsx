import { useLocation, useNavigate } from "react-router-dom";
import type { PredictionRequest } from "../types/prediction";

function formatIndianPrice(price: number): string {
  if (price >= 1e7) return `₹ ${(price / 1e7).toFixed(2)} Cr`;
  if (price >= 1e5) return `₹ ${(price / 1e5).toFixed(2)} Lac`;
  return `₹ ${price.toLocaleString("en-IN")}`;
}

interface LocationState {
  predictedPrice: number;
  form: PredictionRequest;
}

export default function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const state = location.state as LocationState | undefined;

  if (!state) {
    return (
      <div className="card result-page">
        <p>No prediction found. Please fill out the form first.</p>
        <button className="link-btn" onClick={() => navigate("/")}>
          ← Back to form
        </button>
      </div>
    );
  }

  const { predictedPrice, form } = state;

  return (
    <>
      <header className="site-header">
        <h1>Estimated price</h1>
      </header>
      <div className="card result-page">
        <div className="result-price">{formatIndianPrice(predictedPrice)}</div>
        <p className="result-summary">
          {form.carpet_area_sqft} sqft · {form.bathroom} bath · {form.furnishing} ·{" "}
          {form.transaction} in {form.location}
        </p>
        <button className="link-btn" onClick={() => navigate("/")}>
          ← Predict another property
        </button>
      </div>
    </>
  );
}
