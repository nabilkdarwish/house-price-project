import { Link } from "react-router-dom";

export default function NotFoundPage() {
  return (
    <div className="card result-page">
      <h1>404</h1>
      <p>Page not found.</p>
      <Link className="back-link" to="/">
        ← Back home
      </Link>
    </div>
  );
}
