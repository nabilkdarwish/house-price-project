import PredictionForm from "../components/PredictionForm";

export default function HomePage() {
  return (
    <>
      <header className="site-header">
        <h1>🏠 House Price Predictor</h1>
        <p>Enter the property details below to get an estimated price.</p>
      </header>
      <PredictionForm />
    </>
  );
}
