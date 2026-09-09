import { useState } from "react";
import "./App.css";
import locationData from "./locationData";

function App() {
  const [formData, setFormData] = useState({
    business_name: "",
    category: "",
    state: "",
    district: "",
    block: "",
    location: "",
    experience: "Beginner",
    investment: "",
    monthly_revenue: "",
    monthly_expenses: "",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // AI ADVISOR STATES
  const [advisorQuestion, setAdvisorQuestion] = useState("");
  const [advisorAnswer, setAdvisorAnswer] = useState("");
  const [advisorLoading, setAdvisorLoading] = useState(false);
  const [advisorError, setAdvisorError] = useState("");

  // ==========================================
  // HANDLE INPUT CHANGE
  // ==========================================

  const handleChange = (e) => {
    const { name, value } = e.target;

    setError("");

    // Reset district and location when state changes
    if (name === "state") {
      setFormData((previousData) => ({
        ...previousData,
        state: value,
        district: "",
        block: "",
        location: "",
      }));
      return;
    }

    // Reset location when district changes
    if (name === "district") {
      setFormData((previousData) => ({
        ...previousData,
        district: value,
        block: "",
        location: "",
      }));
      return;
    }

    setFormData((previousData) => ({
      ...previousData,
      [name]: value,
    }));
  };

  // ==========================================
  // FORMAT CURRENCY
  // ==========================================

  const formatCurrency = (value) => {
    if (value === null || value === undefined || value === "") {
      return "N/A";
    }

    const numberValue = Number(value);

    if (!Number.isFinite(numberValue)) {
      return "N/A";
    }

    return `₹${numberValue.toLocaleString("en-IN", {
      maximumFractionDigits: 2,
    })}`;
  };

  // ==========================================
  // FORM VALIDATION
  // ==========================================

  const validateForm = () => {
    if (!formData.business_name.trim()) {
      return "Please enter a valid business name.";
    }

    if (formData.business_name.trim().length < 3) {
      return "Business name must contain at least 3 characters.";
    }

    if (!formData.category) {
      return "Please select a business category.";
    }

    if (!formData.state) {
      return "Please select a state.";
    }

    if (!formData.district) {
      return "Please select a district.";
    }

    if (!formData.block.trim()) {
      return "Please enter a block name.";
    }

    if (!formData.location.trim()) {
      return "Please enter a location or village.";
    }

    const marginCapital = Number(formData.investment);
const monthlyRevenue = Number(formData.monthly_revenue);
const monthlyExpenses = Number(formData.monthly_expenses);

if (
  formData.investment === "" ||
  !Number.isFinite(marginCapital) ||
  marginCapital <= 0
) {
  return "Available margin capital must be greater than ₹0.";
}

    if (
      formData.monthly_revenue === "" ||
      !Number.isFinite(monthlyRevenue) ||
      monthlyRevenue <= 0
    ) {
      return "Expected monthly revenue must be greater than ₹0.";
    }

    if (
      formData.monthly_expenses === "" ||
      !Number.isFinite(monthlyExpenses) ||
      monthlyExpenses < 0
    ) {
      return "Monthly expenses cannot be negative.";
    }

    return "";
  };

  // ==========================================
  // ANALYZE BUSINESS
  // ==========================================

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");
    setResult(null);

    // Reset previous AI advisor response
    setAdvisorQuestion("");
    setAdvisorAnswer("");
    setAdvisorError("");

    const validationError = validateForm();

    if (validationError) {
      setError(validationError);
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/analyze",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            ...formData,
            business_name: formData.business_name.trim(),
            block: formData.block.trim(),
            location: formData.location.trim(),
            investment: Number(formData.investment),
            monthly_revenue: Number(formData.monthly_revenue),
            monthly_expenses: Number(formData.monthly_expenses),
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to analyze business");
      }

      const data = await response.json();

      setResult(data);
    } catch (err) {
      console.error("Analysis Error:", err);

      setError(
        "Unable to connect to the backend. Please make sure the FastAPI server is running."
      );
    } finally {
      setLoading(false);
    }
  };

  // ==========================================
  // AI ADVISOR - CORRECTED VERSION
  // ==========================================

  const askAdvisor = async (questionText = advisorQuestion) => {
    const question = questionText.trim();

    if (!question) {
      setAdvisorError("Please enter a question for the AI Advisor.");
      return;
    }

    if (!result) {
      setAdvisorError(
        "Please analyze your business first before asking the AI Advisor."
      );
      return;
    }

    setAdvisorLoading(true);
    setAdvisorError("");
    setAdvisorAnswer("");
    setAdvisorQuestion(question);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/advisor",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            question: question,

            business_name:
              result.business ?? formData.business_name,

            category:
              result.category ?? formData.category,

            monthly_revenue:
              result.financial_analysis?.monthly_revenue ??
              Number(formData.monthly_revenue),

            monthly_expenses:
              result.financial_analysis?.monthly_expenses ??
              Number(formData.monthly_expenses),

            monthly_profit:
              result.financial_analysis?.monthly_profit ?? 0,

            roi_percentage:
              result.financial_analysis?.roi_percentage ?? 0,

            feasibility:
              result.feasibility ?? "",

            financial_risk:
              result.advanced_financial_analysis?.financial_risk ?? "",

            overall_risk_level:
              result.risk_analysis?.overall_risk_level ?? "",

            affordability_status:
              result.loan_affordability?.affordability_status ?? "",

            monthly_emi:
              result.loan_affordability?.monthly_emi ?? 0,

            local_demand:
              result.hyper_local_profile?.local_demand ?? "",

            competition_level:
              result.hyper_local_profile?.competition_level ?? "",
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to get AI advice");
      }

      const data = await response.json();

      setAdvisorAnswer(
        data.answer ??
          data.response ??
          data.advice ??
          "The AI Advisor did not return a response."
      );
    } catch (err) {
      console.error("AI Advisor Error:", err);

      setAdvisorError(
        "Unable to connect to the AI Advisor. Please make sure the FastAPI backend is running and the /advisor endpoint is available."
      );
    } finally {
      setAdvisorLoading(false);
    }
  };

  // ==========================================
  // HANDLE AI ADVISOR SUBMIT
  // ==========================================

  const handleAdvisorSubmit = (e) => {
    e.preventDefault();
    askAdvisor();
  };

  // ==========================================
  // SUGGESTED AI QUESTIONS
  // ==========================================

  const suggestedQuestions = [
    "Is this business profitable?",
    "How can I improve my profit?",
    "Can I afford this loan EMI?",
    "What are the biggest risks?",
    "How can I reduce my business expenses?",
    "Should I expand this business?",
  ];

  return (
    <div className="app">

      {/* ================= HEADER ================= */}

      <header className="topbar">

        <div>
          <p className="eyebrow">SIH 2026 • SIH26091</p>

          <h1>Rural Business Advisor</h1>

          <p className="subtitle">
            Business feasibility, financial planning and scheme recommendations
          </p>
        </div>

        <div className="header-badge">
          AI-Powered Advisory
        </div>

      </header>


      {/* ================= MAIN ================= */}

      <main className="container">

        {/* ================= INPUT FORM ================= */}

        <section className="form-section">

          <div className="section-heading">
            <div>
              <h2>Business Information</h2>

              <p>
                Enter your proposed business details for analysis.
              </p>
            </div>
          </div>


          <form onSubmit={handleSubmit} noValidate>

            <div className="form-grid">

              {/* BUSINESS NAME */}

              <div className="input-group">
                <label>Business Name</label>

                <input
                  type="text"
                  name="business_name"
                  placeholder="e.g. Dairy Farming"
                  value={formData.business_name}
                  onChange={handleChange}
                />
              </div>


              {/* BUSINESS CATEGORY */}

              <div className="input-group">
                <label>Business Category</label>

                <select
                  name="category"
                  value={formData.category}
                  onChange={handleChange}
                >
                  <option value="">Select Category</option>
                  <option value="Dairy">Dairy</option>
                  <option value="Poultry">Poultry</option>
                  <option value="Agriculture">Agriculture</option>
                  <option value="Fishery">Fishery</option>
                  <option value="Retail">Retail</option>
                  <option value="Service">Service</option>
                  <option value="Manufacturing">Manufacturing</option>
                </select>
              </div>


              {/* STATE */}

              <div className="input-group">
                <label>State / Union Territory</label>

                <select
                  name="state"
                  value={formData.state}
                  onChange={handleChange}
                >
                  <option value="">Select State / UT</option>

                  {Object.keys(locationData)
                    .sort()
                    .map((state) => (
                      <option
                        key={state}
                        value={state}
                      >
                        {state}
                      </option>
                    ))}

                </select>
              </div>


              {/* DISTRICT */}

              <div className="input-group">
                <label>District</label>

                <select
                  name="district"
                  value={formData.district}
                  onChange={handleChange}
                  disabled={!formData.state}
                >
                  <option value="">
                    {formData.state
                      ? "Select District"
                      : "First select a State / UT"}
                  </option>

                  {formData.state &&
                    locationData[formData.state]
                      ?.slice()
                      .sort()
                      .map((district) => (
                        <option
                          key={district}
                          value={district}
                        >
                          {district}
                        </option>
                      ))}

                </select>
              </div>


              {/* BLOCK */}

              <div className="input-group">
                <label>Block</label>

                <input
                  type="text"
                  name="block"
                  placeholder={
                    formData.district
                      ? "Enter block name"
                      : "First select a District"
                  }
                  value={formData.block}
                  onChange={handleChange}
                  disabled={!formData.district}
                />
              </div>


              {/* LOCATION */}

              <div className="input-group">
                <label>Location / Village</label>

                <input
                  type="text"
                  name="location"
                  placeholder={
                    formData.district
                      ? "Enter village, town or locality"
                      : "First select a District"
                  }
                  value={formData.location}
                  onChange={handleChange}
                  disabled={!formData.district}
                />
              </div>


              {/* EXPERIENCE */}

              <div className="input-group">
                <label>Experience Level</label>

                <select
                  name="experience"
                  value={formData.experience}
                  onChange={handleChange}
                >
                  <option value="Beginner">Beginner</option>
                  <option value="Intermediate">Intermediate</option>
                  <option value="Experienced">Experienced</option>
                </select>
              </div>


              {/* AVAILABLE MARGIN CAPITAL */}

<div className="input-group">
  <label>Available Margin Capital (₹)</label>

                <input
                  type="number"
                  name="investment"
                  placeholder="100000"
                  min="1"
                  value={formData.investment}
                  onChange={handleChange}
                />
              </div>


              {/* MONTHLY REVENUE */}

              <div className="input-group">
                <label>Expected Monthly Revenue (₹)</label>

                <input
                  type="number"
                  name="monthly_revenue"
                  placeholder="30000"
                  min="1"
                  value={formData.monthly_revenue}
                  onChange={handleChange}
                />
              </div>


              {/* MONTHLY EXPENSES */}

              <div className="input-group">
                <label>Expected Monthly Expenses (₹)</label>

                <input
                  type="number"
                  name="monthly_expenses"
                  placeholder="18000"
                  min="0"
                  value={formData.monthly_expenses}
                  onChange={handleChange}
                />
              </div>

            </div>


            <button
              type="submit"
              className="analyze-btn"
              disabled={loading}
            >
              {loading
                ? "Analyzing Business..."
                : "Analyze Business"}
            </button>

          </form>

        </section>


        {/* ================= ERROR ================= */}

        {error && (
          <div className="error-box">
            ⚠️ {error}
          </div>
        )}


        {/* ================= RESULTS ================= */}

        {result && (

          <section className="results-section">

            {/* ================= OVERVIEW ================= */}

            <div className="results-header">

              <div>

                <p className="eyebrow">
                  ANALYSIS COMPLETE
                </p>

                <h2>{result.business ?? formData.business_name}</h2>

                <p className="location-text">
                  📍 {result.location ?? formData.location},{" "}
                  {result.block ?? formData.block},{" "}
                  {result.district ?? formData.district},{" "}
                  {result.state ?? formData.state}
                </p>

              </div>


              <div className="feasibility-badge">
                {result.feasibility ?? "N/A"}
              </div>

            </div>


            {/* ================= KPI CARDS ================= */}

            <div className="stats-grid">

              <div className="stat-card">
                <span>Monthly Profit</span>

                <strong>
                  {formatCurrency(
                    result.financial_analysis?.monthly_profit
                  )}
                </strong>
              </div>


              <div className="stat-card">
                <span>Yearly Profit</span>

                <strong>
                  {formatCurrency(
                    result.financial_analysis?.yearly_profit
                  )}
                </strong>
              </div>


              <div className="stat-card">
                <span>ROI</span>

                <strong>
                  {result.financial_analysis?.roi_percentage != null
                    ? `${result.financial_analysis.roi_percentage}%`
                    : "N/A"}
                </strong>
              </div>


              <div className="stat-card">
                <span>Payback Period</span>

                <strong>
                  {result.financial_analysis?.payback_period_months != null
                    ? `${result.financial_analysis.payback_period_months} months`
                    : "N/A"}
                </strong>
              </div>

            </div>


            {/* ================= FINANCIAL + LOCAL ================= */}

            <div className="dashboard-grid">

              {/* FINANCIAL */}

              <div className="dashboard-card">

                <div className="card-title">
                  <span className="icon">📊</span>

                  <div>
                    <h3>Financial Analysis</h3>

                    <p>
                      Current business financial health
                    </p>
                  </div>
                </div>


                <div className="data-list">

                  <div className="data-row">
                    <span>Profit Margin</span>

                    <strong>
                      {result.advanced_financial_analysis?.profit_margin != null
                        ? `${result.advanced_financial_analysis.profit_margin}%`
                        : "N/A"}
                    </strong>
                  </div>


                  <div className="data-row">
                    <span>Expense Ratio</span>

                    <strong>
                      {result.advanced_financial_analysis?.expense_ratio != null
                        ? `${result.advanced_financial_analysis.expense_ratio}%`
                        : "N/A"}
                    </strong>
                  </div>


                  <div className="data-row">
                    <span>Break-even Revenue</span>

                    <strong>
                      {formatCurrency(
                        result.advanced_financial_analysis
                          ?.break_even_revenue
                      )}
                    </strong>
                  </div>


                  <div className="data-row">
                    <span>Monthly Cash Surplus</span>

                    <strong>
                      {formatCurrency(
                        result.advanced_financial_analysis
                          ?.monthly_cash_surplus
                      )}
                    </strong>
                  </div>


                  <div className="data-row">
                    <span>Financial Strength</span>

                    <strong>
                      {result.advanced_financial_analysis
                        ?.financial_strength ?? "N/A"}
                    </strong>
                  </div>


                  <div className="data-row">
                    <span>Financial Risk</span>

                    <strong>
                      {result.advanced_financial_analysis
                        ?.financial_risk ?? "N/A"}
                    </strong>
                  </div>

                </div>

              </div>


              {/* LOCAL MARKET */}

              <div className="dashboard-card">

                <div className="card-title">
                  <span className="icon">📍</span>

                  <div>
                    <h3>Hyper-Local Market</h3>

                    <p>
                      Local demand and market potential
                    </p>
                  </div>
                </div>


                <div className="data-list">

                  <div className="data-row">
                    <span>Local Demand</span>

                    <strong>
                      {result.hyper_local_profile?.local_demand ?? "N/A"}
                    </strong>
                  </div>


                  <div className="data-row">
                    <span>Competition</span>

                    <strong>
                      {result.hyper_local_profile?.competition_level ?? "N/A"}
                    </strong>
                  </div>


                  <div className="data-row">
                    <span>Market Potential</span>

                    <strong>
                      {result.hyper_local_profile
                        ?.market_potential_score != null
                        ? `${result.hyper_local_profile.market_potential_score}/100`
                        : "N/A"}
                    </strong>
                  </div>


                  <div className="data-row">
                    <span>Location Suitability</span>

                    <strong>
                      {result.hyper_local_profile
                        ?.location_suitability ?? "N/A"}
                    </strong>
                  </div>


                  <div className="local-summary">
                    {result.hyper_local_profile?.recommendation ??
                      "No local recommendation available."}
                  </div>

                </div>

              </div>

            </div>


            {/* ================= RECOMMENDATION ================= */}

            <div className="recommendation-card">

              <div className="card-title">
                <span className="icon">💡</span>

                <div>
                  <h3>Business Recommendation</h3>
                </div>
              </div>

              <p>
                {result.recommendation ??
                  "No business recommendation available."}
              </p>

            </div>


            {/* ================= LOAN ================= */}

            <div className="dashboard-card full-width">

              <div className="card-title">
                <span className="icon">💰</span>

                <div>
                  <h3>Loan & Scheme Analysis</h3>

                  <p>
                    Recommended financing based on project cost
                  </p>
                </div>
              </div>


              <div className="loan-grid">

                <div>
                  <span>Recommended Scheme</span>

                  <strong>
                    {result.scheme_analysis?.scheme_name ?? "N/A"}
                  </strong>
                </div>


                <div>
                  <span>Project Cost</span>

                  <strong>
                    {formatCurrency(
                      result.scheme_analysis?.project_cost
                    )}
                  </strong>
                </div>


                <div>
                  <span>Required Contribution</span>

                  <strong>
                    {formatCurrency(
                      result.scheme_analysis?.beneficiary_contribution
                    )}
                  </strong>
                </div>


                <div>
                  <span>Eligible Loan</span>

                  <strong>
                    {formatCurrency(
                      result.scheme_analysis?.eligible_loan
                    )}
                  </strong>
                </div>


                <div>
                  <span>Interest Rate</span>

                  <strong>
                    {result.scheme_analysis?.interest_rate != null
                      ? `${result.scheme_analysis.interest_rate}% p.a.`
                      : "N/A"}
                  </strong>
                </div>


                <div>
                  <span>Repayment Period</span>

                  <strong>
                    {result.scheme_analysis?.repayment_period ?? "N/A"}
                  </strong>
                </div>

              </div>

            </div>


            {/* ================= EMI ================= */}

            <div className="dashboard-card full-width">

              <div className="card-title">
                <span className="icon">🏦</span>

                <div>
                  <h3>EMI & Loan Affordability</h3>

                  <p>
                    Estimated repayment capacity
                  </p>
                </div>
              </div>


              <div className="loan-grid">

                <div>
                  <span>Monthly EMI</span>

                  <strong>
                    {formatCurrency(
                      result.loan_affordability?.monthly_emi
                    )}
                  </strong>
                </div>


                <div>
                  <span>Loan Tenure</span>

                  <strong>
                    {result.loan_affordability?.loan_tenure_months != null
                      ? `${result.loan_affordability.loan_tenure_months} months`
                      : "N/A"}
                  </strong>
                </div>


                <div>
                  <span>Total Repayment</span>

                  <strong>
                    {formatCurrency(
                      result.loan_affordability?.total_repayment
                    )}
                  </strong>
                </div>


                <div>
                  <span>Total Interest</span>

                  <strong>
                    {formatCurrency(
                      result.loan_affordability?.total_interest
                    )}
                  </strong>
                </div>


                <div>
                  <span>EMI to Income Ratio</span>

                  <strong>
                    {result.loan_affordability?.emi_to_income_ratio != null
                      ? `${result.loan_affordability.emi_to_income_ratio}%`
                      : "N/A"}
                  </strong>
                </div>


                <div>
                  <span>Affordability</span>

                  <strong>
                    {result.loan_affordability?.affordability_status ?? "N/A"}
                  </strong>
                </div>

              </div>


              <div className="local-summary">
                {result.loan_affordability?.affordability_message ??
                  "No affordability information available."}
              </div>

            </div>


            {/* ================= RISK ANALYSIS ================= */}

            <div className="dashboard-card full-width">

              <div className="card-title">
                <span className="icon">🛡️</span>

                <div>
                  <h3>Overall Business Risk Analysis</h3>

                  <p>
                    Combined financial, market and business risk assessment
                  </p>
                </div>
              </div>


              <div className="stats-grid risk-stats">

                <div className="stat-card">
                  <span>Overall Risk Score</span>

                  <strong>
                    {result.risk_analysis?.risk_score != null
                      ? `${result.risk_analysis.risk_score}/100`
                      : "N/A"}
                  </strong>
                </div>


                <div className="stat-card">
                  <span>Risk Level</span>

                  <strong>
                    {result.risk_analysis?.overall_risk_level ??
                      result.risk_analysis?.risk_level ??
                      "N/A"}
                  </strong>
                </div>


                <div className="stat-card">
                  <span>Financial Risk</span>

                  <strong>
                    {result.risk_analysis?.financial_risk ??
                      result.advanced_financial_analysis?.financial_risk ??
                      "N/A"}
                  </strong>
                </div>


                <div className="stat-card">
                  <span>Market Risk</span>

                  <strong>
                    {result.risk_analysis?.market_risk ??
                      result.hyper_local_profile?.competition_level ??
                      "N/A"}
                  </strong>
                </div>

              </div>


              <div className="risk-analysis-grid">

                <div className="risk-column">

                  <h4>⚠️ Key Risk Factors</h4>

                  <ul className="professional-list">

                    {(result.risk_analysis?.risk_factors ?? []).length > 0
                      ? result.risk_analysis.risk_factors.map(
                          (risk, index) => (
                            <li key={index}>{risk}</li>
                          )
                        )
                      : <li>No major risk factors identified.</li>}

                  </ul>

                </div>


                <div className="risk-column">

                  <h4>✅ Risk Reduction Recommendations</h4>

                  <ul className="professional-list">

                    {(result.risk_analysis?.risk_recommendations ?? []).length > 0
                      ? result.risk_analysis.risk_recommendations.map(
                          (recommendation, index) => (
                            <li key={index}>{recommendation}</li>
                          )
                        )
                      : <li>No additional risk recommendations available.</li>}

                  </ul>

                </div>

              </div>


              <div className="local-summary">

                {result.risk_analysis?.risk_summary ??
                  "Overall business risk information is not available."}

              </div>

            </div>


            {/* ================= AI BUSINESS ADVISOR ================= */}

            <div className="dashboard-card full-width advisor-card">

              <div className="card-title">
                <span className="icon">🤖</span>

                <div>
                  <h3>AI Business Advisor</h3>

                  <p>
                    Ask questions about your business analysis, profit, loan,
                    EMI, risks and growth strategy.
                  </p>
                </div>
              </div>


              {/* SUGGESTED QUESTIONS */}

              <div className="suggested-questions">

                <p className="suggested-title">
                  Try asking:
                </p>

                <div className="question-buttons">

                  {suggestedQuestions.map((question, index) => (

                    <button
                      key={index}
                      type="button"
                      className="question-btn"
                      onClick={() => askAdvisor(question)}
                      disabled={advisorLoading}
                    >
                      {question}
                    </button>

                  ))}

                </div>

              </div>


              {/* ADVISOR FORM */}

              <form
                className="advisor-form"
                onSubmit={handleAdvisorSubmit}
              >

                <textarea
                  value={advisorQuestion}
                  onChange={(e) => {
                    setAdvisorQuestion(e.target.value);
                    setAdvisorError("");
                  }}
                  placeholder="Ask the AI Advisor about your business..."
                  rows="4"
                  disabled={advisorLoading}
                />

                <button
                  type="submit"
                  className="advisor-btn"
                  disabled={advisorLoading}
                >
                  {advisorLoading
                    ? "Thinking..."
                    : "Ask AI Advisor"}
                </button>

              </form>


              {/* ADVISOR ERROR */}

              {advisorError && (

                <div className="error-box advisor-error">
                  ⚠️ {advisorError}
                </div>

              )}


              {/* ADVISOR LOADING */}

              {advisorLoading && (

                <div className="advisor-loading">
                  🤖 AI Advisor is analyzing your business data...
                </div>

              )}


              {/* ADVISOR ANSWER */}

              {advisorAnswer && !advisorLoading && (

                <div className="advisor-answer">

                  <div className="advisor-answer-header">
                    🤖 AI Advisor Response
                  </div>

                  <p>
                    {advisorAnswer}
                  </p>

                </div>

              )}

            </div>


            {/* ================= OPPORTUNITIES + RISKS ================= */}

            <div className="dashboard-grid">

              <div className="dashboard-card">

                <div className="card-title">
                  <span className="icon">🚀</span>

                  <div>
                    <h3>Local Opportunities</h3>

                    <p>
                      Potential areas for growth
                    </p>
                  </div>
                </div>


                <ul className="professional-list">

                  {(result.hyper_local_profile?.local_opportunities ?? []).length > 0
                    ? result.hyper_local_profile.local_opportunities.map(
                        (item, index) => (
                          <li key={index}>{item}</li>
                        )
                      )
                    : <li>No opportunities available.</li>}

                </ul>

              </div>


              <div className="dashboard-card">

                <div className="card-title">
                  <span className="icon">⚠️</span>

                  <div>
                    <h3>Local Risks</h3>

                    <p>
                      Important factors to monitor
                    </p>
                  </div>
                </div>


                <ul className="professional-list">

                  {(result.hyper_local_profile?.local_risks ?? []).length > 0
                    ? result.hyper_local_profile.local_risks.map(
                        (item, index) => (
                          <li key={index}>{item}</li>
                        )
                      )
                    : <li>No risks available.</li>}

                </ul>

              </div>

            </div>


            {/* ================= BUSINESS ADVICE ================= */}

            <div className="dashboard-card full-width">

              <div className="card-title">
                <span className="icon">💡</span>

                <div>
                  <h3>Business Advice</h3>

                  <p>
                    Practical recommendations for the entrepreneur
                  </p>
                </div>
              </div>


              <ul className="professional-list advice-list">

                {(result.business_advice ?? []).length > 0
                  ? result.business_advice.map((advice, index) => (
                      <li key={index}>{advice}</li>
                    ))
                  : <li>No business advice available.</li>}

              </ul>

            </div>


            {/* ================= PROJECTION ================= */}

            <div className="dashboard-card full-width">

              <div className="card-title">
                <span className="icon">📈</span>

                <div>
                  <h3>12-Month Profit Projection</h3>

                  <p>
                    Estimated profit growth based on current inputs
                  </p>
                </div>
              </div>


              <div className="table-wrapper">

                <table>

                  <thead>
                    <tr>
                      <th>Month</th>
                      <th>Monthly Profit</th>
                      <th>Cumulative Profit</th>
                    </tr>
                  </thead>


                  <tbody>

                    {(result.profit_projection ?? []).length > 0 ? (
                      result.profit_projection.map(
                        (item, index) => (
                          <tr key={index}>
                            <td>{item.month}</td>

                            <td>
                              {formatCurrency(item.monthly_profit)}
                            </td>

                            <td>
                              {formatCurrency(item.cumulative_profit)}
                            </td>
                          </tr>
                        )
                      )
                    ) : (
                      <tr>
                        <td colSpan="3">
                          No profit projection available.
                        </td>
                      </tr>
                    )}

                  </tbody>

                </table>

              </div>

            </div>

          </section>

        )}

      </main>

    </div>
  );
}

export default App;