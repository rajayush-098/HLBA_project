from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import math

app = FastAPI(
    title="SIH26091 Rural Business Advisor",
    description="AI-powered rural business feasibility and financial advisory system",
    version="5.0.0",
)

# ==================================================
# CORS
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================================================
# REQUEST MODELS
# ==================================================

class BusinessRequest(BaseModel):
    business_name: str
    category: str
    state: str
    district: str
    location: str
    experience: str
    investment: float
    monthly_revenue: float
    monthly_expenses: float


class AdvisorRequest(BaseModel):
    # Current frontend sends question + business_data.
    question: str
    business_data: dict = Field(default_factory=dict)

    # These fields also allow direct/older frontend requests.
    business_name: str = ""
    category: str = ""
    monthly_revenue: float = 0
    monthly_expenses: float = 0
    monthly_profit: float = 0
    roi_percentage: float = 0
    feasibility: str = ""
    financial_risk: str = ""
    overall_risk_level: str = ""
    affordability_status: str = ""
    monthly_emi: float = 0
    local_demand: str = ""
    competition_level: str = ""


# ==================================================
# HOME ENDPOINT
# ==================================================

@app.get("/")
def home():
    return {
        "message": "SIH26091 Rural Business Advisor API is running!",
        "status": "success",
    }


# ==================================================
# AI BUSINESS ADVISOR
# ==================================================

@app.post("/advisor")
def business_advisor(data: AdvisorRequest):
    question = data.question.strip().lower()

    if not question:
        return {
            "answer": "Please enter a question about your business."
        }

    # Support the current React payload as well as older flat payloads.
    bd = data.business_data or {}

    analysis = bd.get("analysis", {}) or {}
    financial = analysis.get("financial_analysis", {}) or {}
    advanced = analysis.get("advanced_financial_analysis", {}) or {}
    risk = analysis.get("risk_analysis", {}) or {}
    hyper_local = analysis.get("hyper_local_profile", {}) or {}
    affordability = analysis.get("loan_affordability", {}) or {}

    business_name = (
        bd.get("business_name")
        or data.business_name
        or analysis.get("business")
        or "Your business"
    )

    category = (
        bd.get("category")
        or data.category
        or analysis.get("category")
        or ""
    )

    monthly_revenue = float(
        financial.get("monthly_revenue", bd.get("monthly_revenue", data.monthly_revenue)) or 0
    )
    monthly_expenses = float(
        financial.get("monthly_expenses", bd.get("monthly_expenses", data.monthly_expenses)) or 0
    )
    monthly_profit = float(
        financial.get("monthly_profit", bd.get("monthly_profit", data.monthly_profit)) or 0
    )
    roi_percentage = float(
        financial.get("roi_percentage", bd.get("roi_percentage", data.roi_percentage)) or 0
    )

    feasibility = (
        analysis.get("feasibility")
        or bd.get("feasibility")
        or data.feasibility
        or "Not Available"
    )

    financial_risk = (
        advanced.get("financial_risk")
        or bd.get("financial_risk")
        or data.financial_risk
        or "Not Available"
    )

    overall_risk_level = (
        risk.get("overall_risk_level")
        or bd.get("overall_risk_level")
        or data.overall_risk_level
        or "Not Available"
    )

    affordability_status = (
        affordability.get("affordability_status")
        or bd.get("affordability_status")
        or data.affordability_status
        or "Not Available"
    )

    monthly_emi = float(
        affordability.get("monthly_emi", bd.get("monthly_emi", data.monthly_emi)) or 0
    )

    local_demand = (
        hyper_local.get("local_demand")
        or bd.get("local_demand")
        or data.local_demand
        or "Not Available"
    )

    competition_level = (
        hyper_local.get("competition_level")
        or bd.get("competition_level")
        or data.competition_level
        or "Not Available"
    )

    # --------------------------------------------------
    # GREETING
    # --------------------------------------------------

    if any(word in question for word in [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good evening",
    ]):
        answer = (
            f"Hello! I am your AI Business Advisor for {business_name}. "
            "You can ask me about profit, ROI, expenses, loans, EMI, "
            "business risks, local demand, competition, feasibility, or growth."
        )

    # --------------------------------------------------
    # PROFIT
    # --------------------------------------------------

    elif any(word in question for word in [
        "profit",
        "profitable",
        "profitability",
        "earning",
        "earnings",
    ]):
        if monthly_profit > 0:
            profit_margin = (
                (monthly_profit / monthly_revenue) * 100
                if monthly_revenue > 0
                else 0
            )

            answer = (
                f"{business_name} is currently generating an estimated "
                f"monthly profit of ₹{monthly_profit:,.2f}. "
                f"The estimated profit margin is {profit_margin:.2f}%. "
            )

            if monthly_profit < 10000:
                answer += (
                    "The business is profitable, but the profit level is relatively "
                    "low. Focus on increasing sales and controlling expenses."
                )
            else:
                answer += (
                    "The business is generating positive profit. Continue monitoring "
                    "expenses and maintain stable revenue growth."
                )
        else:
            answer = (
                f"{business_name} is currently not generating positive monthly profit. "
                "Reduce unnecessary expenses, improve sales, and review the business "
                "model before taking additional financial risk."
            )

    # --------------------------------------------------
    # ROI
    # --------------------------------------------------

    elif any(word in question for word in [
        "roi",
        "return on investment",
        "return",
    ]):
        if roi_percentage >= 30:
            answer = (
                f"Your estimated ROI is {roi_percentage:.2f}%, which indicates "
                "strong financial performance based on the entered business data."
            )
        elif roi_percentage >= 15:
            answer = (
                f"Your estimated ROI is {roi_percentage:.2f}%, which indicates "
                "reasonable business performance. You can improve ROI by increasing "
                "profit without making a proportional increase in investment."
            )
        elif roi_percentage > 0:
            answer = (
                f"Your estimated ROI is {roi_percentage:.2f}%, which is relatively "
                "low. Focus on improving revenue, reducing costs, and using investment "
                "more efficiently."
            )
        else:
            answer = (
                "Your current ROI is not positive. Improve profitability before "
                "making additional investments."
            )

    # --------------------------------------------------
    # EXPENSES
    # --------------------------------------------------

    elif any(word in question for word in [
        "expense",
        "expenses",
        "cost",
        "reduce cost",
        "reduce expense",
        "save money",
    ]):
        if monthly_revenue > 0:
            expense_ratio = (monthly_expenses / monthly_revenue) * 100

            answer = (
                f"Your estimated monthly expenses are ₹{monthly_expenses:,.2f}, "
                f"which is approximately {expense_ratio:.2f}% of monthly revenue. "
            )

            if expense_ratio >= 80:
                answer += (
                    "Your expense ratio is high. Review your largest costs first, "
                    "negotiate with suppliers, reduce wastage, and avoid unnecessary "
                    "operational spending."
                )
            elif expense_ratio >= 60:
                answer += (
                    "Your expenses need regular monitoring. Identify recurring costs "
                    "that can be reduced without affecting product or service quality."
                )
            else:
                answer += (
                    "Your expense ratio appears relatively manageable. Continue "
                    "monitoring costs and maintain financial discipline."
                )
        else:
            answer = (
                "Please provide valid monthly revenue information for a detailed "
                "expense analysis."
            )

    # --------------------------------------------------
    # LOAN / EMI
    # --------------------------------------------------

    elif any(word in question for word in [
        "loan",
        "emi",
        "repayment",
        "afford",
        "affordable",
        "pay loan",
    ]):
        answer = (
            f"Your current loan affordability status is '{affordability_status}'. "
        )

        if monthly_emi > 0:
            answer += f"The estimated monthly EMI is ₹{monthly_emi:,.2f}. "

        if affordability_status == "Affordable":
            answer += (
                "Based on the entered business figures, the repayment burden appears "
                "manageable. Keep an emergency reserve for unexpected expenses."
            )
        elif affordability_status == "Moderately Affordable":
            answer += (
                "The loan may be manageable, but it can put pressure on cash flow. "
                "Maintain a reserve and avoid taking additional debt."
            )
        elif affordability_status == "High Repayment Burden":
            answer += (
                "The repayment burden is high. Consider reducing the loan amount, "
                "increasing your own contribution, or improving business cash flow."
            )
        elif affordability_status == "Not Affordable":
            answer += (
                "The current business figures indicate that the EMI may not be "
                "manageable. Improve profitability or reduce the loan amount."
            )
        else:
            answer += (
                "Loan repayment should be evaluated carefully against stable monthly "
                "cash flow before borrowing."
            )

    # --------------------------------------------------
    # RISK
    # --------------------------------------------------

    elif any(word in question for word in [
        "risk",
        "risky",
        "danger",
        "problem",
        "threat",
    ]):
        answer = (
            f"The overall business risk level is '{overall_risk_level}' and "
            f"the financial risk is '{financial_risk}'. "
        )

        risk_factors = risk.get("risk_factors", [])
        if risk_factors:
            answer += "Key risk factors include: " + "; ".join(risk_factors[:3]) + ". "

        if overall_risk_level == "High Risk":
            answer += (
                "Prioritize improving profitability, reducing expenses, and avoiding "
                "excessive loan commitments."
            )
        elif overall_risk_level == "Medium Risk":
            answer += (
                "Monitor financial discipline, market competition, and stable cash flow."
            )
        else:
            answer += (
                "The current risk profile appears manageable, but continue monitoring "
                "costs, market conditions, and business performance."
            )

    # --------------------------------------------------
    # MARKET / DEMAND / COMPETITION
    # --------------------------------------------------

    elif any(word in question for word in [
        "market",
        "demand",
        "competition",
        "customer",
        "customers",
        "local",
    ]):
        answer = (
            f"The estimated local demand is '{local_demand}' and the competition "
            f"level is '{competition_level}'. "
        )

        if local_demand == "High":
            answer += (
                "This suggests good potential for customer acquisition. Focus on "
                "quality, reliability, and strong local customer relationships."
            )
        elif local_demand == "Medium":
            answer += (
                "There is reasonable potential, but local marketing and customer "
                "feedback will be important for growth."
            )
        else:
            answer += (
                "Demand should be validated carefully before expansion. Start smaller "
                "and test customer response."
            )

    # --------------------------------------------------
    # GROWTH / IMPROVEMENT
    # --------------------------------------------------

    elif any(word in question for word in [
        "grow",
        "growth",
        "improve",
        "better",
        "increase",
        "expand",
        "future",
    ]):
        answer = (
            f"To improve {business_name}, focus on these priorities: "
            "1) increase profitable sales, "
            "2) control unnecessary expenses, "
            "3) maintain accurate income and expense records, "
            "4) study customer needs and competitors, "
            "5) build an emergency cash reserve, and "
            "6) expand gradually after achieving stable profits."
        )

    # --------------------------------------------------
    # FEASIBILITY
    # --------------------------------------------------

    elif any(word in question for word in [
        "feasible",
        "feasibility",
        "should i start",
        "good business",
        "worth starting",
    ]):
        answer = (
            f"The current feasibility assessment for {business_name} is "
            f"'{feasibility}'. "
        )

        if feasibility == "Highly Feasible":
            answer += (
                "The entered financial figures show strong potential. Continue "
                "validating actual local demand before making the full investment."
            )
        elif feasibility == "Feasible":
            answer += (
                "The business appears viable, but carefully manage expenses and "
                "monitor local market performance."
            )
        elif feasibility == "Moderately Feasible":
            answer += (
                "The business has potential but should improve profitability and "
                "financial margins before major expansion."
            )
        else:
            answer += (
                "The current financial figures do not support strong feasibility. "
                "Review revenue assumptions, expenses, and investment requirements."
            )

    # --------------------------------------------------
    # DEFAULT
    # --------------------------------------------------

    else:
        answer = (
            f"Based on the analysis of {business_name}, the current feasibility is "
            f"'{feasibility}', estimated monthly profit is ₹{monthly_profit:,.2f}, "
            f"and ROI is {roi_percentage:.2f}%. "
            "Ask me about profit, ROI, expenses, loan EMI, risks, market demand, "
            "competition, feasibility, or business growth."
        )

    return {"answer": answer}


# ==================================================
# BUSINESS ANALYSIS
# ==================================================

@app.post("/analyze")
def analyze_business(data: BusinessRequest):

    # ==================================================
    # STEP 1: BASIC FINANCIAL CALCULATIONS
    # ==================================================

    monthly_profit = data.monthly_revenue - data.monthly_expenses
    yearly_profit = monthly_profit * 12

    if data.investment > 0 and yearly_profit > 0:
        roi = (yearly_profit / data.investment) * 100
    else:
        roi = 0

    if monthly_profit > 0:
        payback_months = data.investment / monthly_profit
    else:
        payback_months = None

    # ==================================================
    # STEP 2: ADVANCED FINANCIAL ANALYSIS
    # ==================================================

    if data.monthly_revenue > 0:
        profit_margin = (monthly_profit / data.monthly_revenue) * 100
        expense_ratio = (data.monthly_expenses / data.monthly_revenue) * 100
    else:
        profit_margin = 0
        expense_ratio = 0

    # Simplified monthly break-even revenue for this prototype.
    break_even_revenue = data.monthly_expenses
    monthly_cash_surplus = monthly_profit

    if monthly_profit <= 0:
        financial_strength = "Weak"
    elif profit_margin >= 30:
        financial_strength = "Strong"
    elif profit_margin >= 15:
        financial_strength = "Moderate"
    else:
        financial_strength = "Weak"

    if monthly_profit <= 0:
        financial_risk = "High"
    elif expense_ratio >= 85:
        financial_risk = "High"
    elif expense_ratio >= 65:
        financial_risk = "Medium"
    else:
        financial_risk = "Low"

    # ==================================================
    # STEP 3: 12-MONTH PROFIT PROJECTION
    # ==================================================

    profit_projection = []
    cumulative_profit = 0

    for month in range(1, 13):
        cumulative_profit += monthly_profit
        profit_projection.append({
            "month": f"Month {month}",
            "monthly_profit": round(monthly_profit, 2),
            "cumulative_profit": round(cumulative_profit, 2),
        })

    # ==================================================
    # STEP 4: FEASIBILITY
    # ==================================================

    if monthly_profit <= 0:
        feasibility = "Not Feasible"
    elif roi >= 30 and profit_margin >= 20:
        feasibility = "Highly Feasible"
    elif roi >= 15:
        feasibility = "Feasible"
    else:
        feasibility = "Moderately Feasible"

    # ==================================================
    # STEP 5: GOVERNMENT LOAN SCHEME ANALYSIS
    # ==================================================

    # PS requirement:
    # Beneficiary margin contribution is 10% of project cost.
    # Therefore estimated project cost = margin capital / 10%.
    margin_capital = data.investment
    project_cost = margin_capital / 0.10
    maximum_loan = project_cost * 0.90

    beneficiary_contribution = margin_capital
    eligible_loan = maximum_loan

    scheme_name = "Not Eligible"
    scheme_message = "No suitable scheme found."
    interest_rate = None
    repayment_period = None
    loan_tenure_months = None

    if project_cost <= 140000:
        scheme_name = "Micro Finance Scheme"
        eligible_loan = min(eligible_loan, 125000)
        interest_rate = 6.5
        repayment_period = "3 years including 3-month moratorium"
        loan_tenure_months = 36
        scheme_message = "Eligible for the Micro Finance Scheme."

    elif project_cost <= 5000000:
        scheme_name = "Term Loan Scheme"
        eligible_loan = min(eligible_loan, 4500000)
        interest_rate = 8.0
        repayment_period = "7 years including 6-month moratorium"
        loan_tenure_months = 84
        scheme_message = "Eligible for the Term Loan Scheme."

    else:
        scheme_name = "Above Standard Scheme Limit"
        eligible_loan = 0
        scheme_message = (
            "Project cost is above ₹50 lakh. Check other financing options."
        )

        # ==================================================
    # STEP 6: EMI + LOAN AFFORDABILITY + MORATORIUM
    # ==================================================

    monthly_emi = None
    total_repayment = None
    total_interest = None
    emi_to_income_ratio = None

    # PS-required moratorium handling
    moratorium_months = 0
    repayment_months = None

    # PS-required repayment schedule
    repayment_schedule = []

    # Financial planning indicators
    estimated_working_capital = max(data.monthly_expenses, 0)
    monthly_operational_cost = max(data.monthly_expenses, 0)

    affordability_status = "Not Available"
    affordability_message = (
        "Loan affordability could not be calculated."
    )

    if (
        eligible_loan > 0
        and interest_rate is not None
        and loan_tenure_months is not None
    ):

        # --------------------------------------------------
        # MORATORIUM
        # --------------------------------------------------
        if scheme_name == "Micro Finance Scheme":
            moratorium_months = 3

        elif scheme_name == "Term Loan Scheme":
            moratorium_months = 6

        repayment_months = loan_tenure_months - moratorium_months

        # --------------------------------------------------
        # EMI CALCULATION
        #
        # Important:
        # The PS says the stated tenure INCLUDES the
        # moratorium period.
        #
        # Therefore EMI repayment is calculated over:
        # total tenure - moratorium months
        # --------------------------------------------------
        monthly_interest_rate = interest_rate / (12 * 100)

        if repayment_months > 0:

            if monthly_interest_rate > 0:

                emi = (
                    eligible_loan
                    * monthly_interest_rate
                    * math.pow(
                        1 + monthly_interest_rate,
                        repayment_months
                    )
                ) / (
                    math.pow(
                        1 + monthly_interest_rate,
                        repayment_months
                    ) - 1
                )

            else:
                emi = eligible_loan / repayment_months

            monthly_emi = round(emi, 2)

            # --------------------------------------------------
            # REPAYMENT SCHEDULE
            #
            # During moratorium:
            # - EMI = 0
            # - Principal repayment = 0
            # - Interest is shown separately as accrued interest.
            #
            # The PS does not specify whether moratorium
            # interest is capitalized, so we do NOT silently
            # assume capitalization.
            # --------------------------------------------------

            outstanding_principal = eligible_loan
            total_regular_interest = 0
            total_moratorium_interest = 0

            for month in range(1, loan_tenure_months + 1):

                monthly_interest = round(
                    outstanding_principal * monthly_interest_rate,
                    2
                )

                if month <= moratorium_months:

                    # No EMI during moratorium
                    principal_payment = 0
                    emi_payment = 0

                    total_moratorium_interest += monthly_interest

                else:

                    emi_payment = monthly_emi

                    # Principal component of EMI
                    principal_payment = round(
                        emi_payment - monthly_interest,
                        2
                    )

                    # Prevent tiny floating-point overpayment
                    if principal_payment > outstanding_principal:
                        principal_payment = round(
                            outstanding_principal,
                            2
                        )

                    outstanding_principal = round(
                        outstanding_principal - principal_payment,
                        2
                    )

                    total_regular_interest += monthly_interest

                repayment_schedule.append({
                    "month": month,
                    "phase": (
                        "Moratorium"
                        if month <= moratorium_months
                        else "Repayment"
                    ),
                    "emi": round(emi_payment, 2),
                    "interest": round(monthly_interest, 2),
                    "principal": round(principal_payment, 2),
                    "outstanding_principal": round(
                        outstanding_principal,
                        2
                    )
                })

            # --------------------------------------------------
            # TOTALS
            # --------------------------------------------------

            total_interest = round(
                total_regular_interest
                + total_moratorium_interest,
                2
            )

            # Regular EMI payments + interest accrued
            # during the moratorium.
            total_repayment = round(
                (monthly_emi * repayment_months)
                + total_moratorium_interest,
                2
            )

            # --------------------------------------------------
            # EMI / INCOME RATIO
            # --------------------------------------------------

            if data.monthly_revenue > 0:

                emi_to_income_ratio = round(
                    (monthly_emi / data.monthly_revenue) * 100,
                    2
                )

                # --------------------------------------------------
                # LOAN AFFORDABILITY
                # --------------------------------------------------

                if monthly_profit <= 0:

                    affordability_status = "Not Affordable"

                    affordability_message = (
                        "Business has no positive monthly profit."
                    )

                elif monthly_emi > monthly_cash_surplus:

                    affordability_status = "Not Affordable"

                    affordability_message = (
                        "EMI is higher than monthly cash surplus."
                    )

                elif emi_to_income_ratio > 40:

                    affordability_status = "High Repayment Burden"

                    affordability_message = (
                        "EMI creates a significant financial burden."
                    )

                elif emi_to_income_ratio > 25:

                    affordability_status = "Moderately Affordable"

                    affordability_message = (
                        "Loan is possible but will put pressure "
                        "on cash flow."
                    )

                else:

                    affordability_status = "Affordable"

                    affordability_message = (
                        "EMI appears manageable based on current figures."
                    )


        # --------------------------------------------------
        # QUARTERLY REPAYMENT SUMMARY
        #
        # Required by the PS for an expected quarterly
        # repayment schedule.
        # --------------------------------------------------

        quarterly_repayment_schedule = []

        for quarter_start in range(1, loan_tenure_months + 1, 3):

            quarter_end = min(
                quarter_start + 2,
                loan_tenure_months
            )

            quarter_rows = [
                row
                for row in repayment_schedule
                if quarter_start <= row["month"] <= quarter_end
            ]

            quarterly_emi = round(
                sum(row["emi"] for row in quarter_rows),
                2
            )

            quarterly_interest = round(
                sum(row["interest"] for row in quarter_rows),
                2
            )

            quarterly_principal = round(
                sum(row["principal"] for row in quarter_rows),
                2
            )

            ending_balance = (
                quarter_rows[-1]["outstanding_principal"]
                if quarter_rows
                else eligible_loan
            )

            if all(
                row["phase"] == "Moratorium"
                for row in quarter_rows
            ):
                quarter_phase = "Moratorium"

            elif any(
                row["phase"] == "Moratorium"
                for row in quarter_rows
            ):
                quarter_phase = "Moratorium + Repayment"

            else:
                quarter_phase = "Repayment"

            quarterly_repayment_schedule.append({
                "quarter": (
                    (quarter_start - 1) // 3
                ) + 1,
                "months": f"{quarter_start}-{quarter_end}",
                "phase": quarter_phase,
                "emi_total": quarterly_emi,
                "interest_total": quarterly_interest,
                "principal_total": quarterly_principal,
                "outstanding_principal": round(
                    ending_balance,
                    2
                )
            })

    # ==================================================
    # STEP 7: SMART SCHEME MATCHING
    # ==================================================

    matching_schemes = []

    if project_cost <= 140000:
        matching_schemes.append({
            "scheme_name": "Micro Finance Scheme",
            "project_cost_limit": "Up to ₹1.40 lakh",
            "maximum_loan": 125000,
            "eligible_loan": round(
                min(maximum_loan, 125000),
                2,
            ),
            "interest_rate": 6.5,
            "repayment_period": "3 years including 3-month moratorium",
            "match_score": 95,
            "reason": (
                "Project cost falls within the Micro Finance Scheme limit."
            ),
        })

    elif project_cost <= 5000000:
        matching_schemes.append({
            "scheme_name": "Term Loan Scheme",
            "project_cost_limit": "₹1.40 lakh to ₹50 lakh",
            "maximum_loan": 4500000,
            "eligible_loan": round(
                min(maximum_loan, 4500000),
                2,
            ),
            "interest_rate": 8.0,
            "repayment_period": "7 years including 6-month moratorium",
            "match_score": 95,
            "reason": (
                "Project cost falls within the Term Loan Scheme limit."
            ),
        })

    recommended_scheme = (
        matching_schemes[0] if matching_schemes else None
    )

        # ==================================================
    # STEP 8: HYPER-LOCAL MARKET ANALYSIS
    # ==================================================

    business = data.business_name.lower().strip()
    category = data.category.lower().strip()

    # --------------------------------------------------
    # LOCAL DEMAND
    # --------------------------------------------------

    if category in [
        "dairy",
        "agriculture",
        "poultry",
        "fishery",
    ]:
        local_demand = "High"
    else:
        local_demand = "Medium"

    # --------------------------------------------------
    # COMPETITION
    # --------------------------------------------------

    if category in [
        "retail",
        "service",
    ]:
        competition_level = "High"

    elif category in [
        "dairy",
        "poultry",
        "agriculture",
    ]:
        competition_level = "Medium"

    else:
        competition_level = "Medium"

    # --------------------------------------------------
    # MARKET POTENTIAL SCORE
    # --------------------------------------------------

    market_potential_score = 50

    if local_demand == "High":
        market_potential_score += 30
    else:
        market_potential_score += 15

    if competition_level == "Low":
        market_potential_score += 15

    elif competition_level == "Medium":
        market_potential_score += 5

    else:
        market_potential_score -= 10

    if monthly_profit > 0:
        market_potential_score += 10

    if data.experience == "Experienced":
        market_potential_score += 10

    elif data.experience == "Intermediate":
        market_potential_score += 5

    market_potential_score = min(
        max(market_potential_score, 0),
        100
    )

    # --------------------------------------------------
    # LOCATION SUITABILITY
    # --------------------------------------------------

    if market_potential_score >= 80:
        location_suitability = "Highly Suitable"

    elif market_potential_score >= 60:
        location_suitability = "Suitable"

    else:
        location_suitability = "Needs Improvement"

    # ==================================================
    # PS REQUIREMENT 1: MARKET REACH
    # ==================================================

    # The PS requires analysis of the immediate market
    # within approximately 5–10 km.
    #
    # We do not invent population numbers because the
    # current location_data.py does not contain verified
    # village-level population data.

    market_reach = {
        "primary_radius_km": 5,
        "extended_radius_km": 10,

        "consumer_base": (
            "Estimated local consumer base within the "
            "5–10 km service area. Exact consumer count "
            "requires verified local demographic data."
        ),

        "reach_type": "Estimated",

        "distribution_channels": []
    }

    # --------------------------------------------------
    # DISTRIBUTION CHANNELS
    # --------------------------------------------------

    if category == "dairy":

        market_reach["distribution_channels"] = [
            "Nearby households",
            "Local milk collection centers",
            "Local grocery shops",
            "Restaurants and tea shops",
            "Direct home delivery"
        ]

    elif category == "poultry":

        market_reach["distribution_channels"] = [
            "Nearby households",
            "Local grocery shops",
            "Restaurants and hotels",
            "Local poultry retailers",
            "Direct local delivery"
        ]

    elif category == "agriculture":

        market_reach["distribution_channels"] = [
            "Local markets",
            "Nearby households",
            "Local traders",
            "Retailers and wholesalers",
            "Direct-to-consumer sales"
        ]

    elif category == "fishery":

        market_reach["distribution_channels"] = [
            "Local fish markets",
            "Nearby households",
            "Restaurants and hotels",
            "Local retailers",
            "Direct local delivery"
        ]

    elif category == "retail":

        market_reach["distribution_channels"] = [
            "Nearby households",
            "Walk-in local customers",
            "Local institutions",
            "Local delivery",
            "Repeat neighborhood customers"
        ]

    elif category == "service":

        market_reach["distribution_channels"] = [
            "Nearby households",
            "Local customers",
            "Local institutions",
            "Referral customers",
            "Digital/local communication channels"
        ]

    else:

        market_reach["distribution_channels"] = [
            "Nearby households",
            "Local customers",
            "Nearby retailers",
            "Local institutions",
            "Direct/local delivery"
        ]

    # --------------------------------------------------
    # MARKET REACH ASSESSMENT
    # --------------------------------------------------

    if local_demand == "High":

        market_reach["reach_assessment"] = (
            "The business has strong potential to serve "
            "customers within the 5–10 km local service area."
        )

    else:

        market_reach["reach_assessment"] = (
            "The business can serve the local 5–10 km market, "
            "but demand should be validated before expansion."
        )

    # ==================================================
    # LOCAL OPPORTUNITIES AND RISKS
    # ==================================================

    if category == "dairy":

        local_opportunities = [
            "Growing demand for milk and dairy products.",
            "Opportunity to supply nearby households and milk collection centers.",
            "Potential for value-added products such as paneer, curd and ghee."
        ]

        local_risks = [
            "High cattle feed and healthcare costs.",
            "Milk price fluctuations.",
            "Dependence on reliable veterinary services."
        ]

    elif category == "poultry":

        local_opportunities = [
            "Regular demand for eggs and poultry products.",
            "Opportunity to supply local shops and restaurants.",
            "Potential for gradual expansion after stable operations."
        ]

        local_risks = [
            "Disease and infection risks.",
            "Fluctuating feed costs.",
            "Changes in local poultry market prices."
        ]

    elif category == "agriculture":

        local_opportunities = [
            "Opportunity to select crops suitable for local conditions.",
            "Potential for direct-to-market selling.",
            "Scope for value-added agricultural products."
        ]

        local_risks = [
            "Weather and seasonal risks.",
            "Fluctuating crop prices.",
            "Water availability and irrigation dependency."
        ]

    elif category == "fishery":

        local_opportunities = [
            "Growing demand for fresh fish products.",
            "Opportunity to supply nearby markets and restaurants.",
            "Potential to select high-demand fish species."
        ]

        local_risks = [
            "Water quality and availability risks.",
            "Fish disease risks.",
            "Seasonal and market price fluctuations."
        ]

    elif category == "retail":

        local_opportunities = [
            "Opportunity to serve daily local consumer needs.",
            "Potential to build repeat customers.",
            "Possibility of adding new products based on demand."
        ]

        local_risks = [
            "High local competition.",
            "Inventory management challenges.",
            "Changing customer preferences."
        ]

    else:

        local_opportunities = [
            "Opportunity to identify unmet local customer needs.",
            "Potential to build a strong local customer base.",
            "Possibility of gradual expansion after validation."
        ]

        local_risks = [
            "Uncertain local demand.",
            "Competition from existing businesses.",
            "Need for continuous market monitoring."
        ]

    # ==================================================
    # HYPER-LOCAL RECOMMENDATION
    # ==================================================

    hyper_local_recommendation = (
        f"{data.business_name} in {data.location}, "
        f"{data.district}, {data.state} has "
        f"{location_suitability.lower()} market suitability. "
        f"Estimated local demand is {local_demand.lower()} "
        f"with {competition_level.lower()} competition. "
        f"The recommended service area is approximately "
        f"5–10 km around the selected location."
    )

    # ==================================================
    # HYPER-LOCAL PROFILE
    # ==================================================

    hyper_local_profile = {
        "state": data.state,
        "district": data.district,
        "location": data.location,
        "category": data.category,

        "profile_summary": (
            f"Business analysis prepared for "
            f"{data.business_name} in {data.location}, "
            f"{data.district}, {data.state}."
        ),

        "local_demand": local_demand,
        "competition_level": competition_level,
        "market_potential_score": market_potential_score,
        "location_suitability": location_suitability,

        "market_reach": market_reach,

        "local_opportunities": local_opportunities,
        "local_risks": local_risks,

        "recommendation": hyper_local_recommendation
    }

    # ==================================================
    # STEP 9: LOCAL OPPORTUNITIES AND RISKS
    # ==================================================

    if category == "dairy":
        local_opportunities = [
            "Growing demand for milk and dairy products.",
            "Opportunity to supply nearby households and milk collection centers.",
            "Potential for value-added products such as paneer, curd and ghee.",
        ]

        local_risks = [
            "High cattle feed and healthcare costs.",
            "Milk price fluctuations.",
            "Dependence on reliable veterinary services.",
        ]

    elif category == "poultry":
        local_opportunities = [
            "Regular demand for eggs and poultry products.",
            "Opportunity to supply local shops and restaurants.",
            "Potential for gradual expansion after stable operations.",
        ]

        local_risks = [
            "Disease and infection risks.",
            "Fluctuating feed costs.",
            "Changes in local poultry market prices.",
        ]

    elif category == "agriculture":
        local_opportunities = [
            "Opportunity to select crops suitable for local conditions.",
            "Potential for direct-to-market selling.",
            "Scope for value-added agricultural products.",
        ]

        local_risks = [
            "Weather and seasonal risks.",
            "Fluctuating crop prices.",
            "Water availability and irrigation dependency.",
        ]

    elif category == "fishery":
        local_opportunities = [
            "Growing demand for fresh fish products.",
            "Opportunity to supply nearby markets and restaurants.",
            "Potential to select high-demand fish species.",
        ]

        local_risks = [
            "Water quality and availability risks.",
            "Fish disease risks.",
            "Seasonal and market price fluctuations.",
        ]

    elif category == "retail":
        local_opportunities = [
            "Opportunity to serve daily local consumer needs.",
            "Potential to build repeat customers.",
            "Possibility of adding new products based on demand.",
        ]

        local_risks = [
            "High local competition.",
            "Inventory management challenges.",
            "Changing customer preferences.",
        ]

    else:
        local_opportunities = [
            "Opportunity to identify unmet local customer needs.",
            "Potential to build a strong local customer base.",
            "Possibility of gradual expansion after validation.",
        ]

        local_risks = [
            "Uncertain local demand.",
            "Competition from existing businesses.",
            "Need for continuous market monitoring.",
        ]

    hyper_local_recommendation = (
        f"{data.business_name} in {data.location}, {data.district}, "
        f"{data.state} has {location_suitability.lower()} market suitability. "
        f"Estimated local demand is {local_demand.lower()} with "
        f"{competition_level.lower()} competition."
    )
    hyper_local_profile = {
                "state": data.state,
                "district": data.district,
                "location": data.location,
                "category": data.category,

                "profile_summary": (
                    f"Business analysis prepared for {data.business_name} "
                    f"in {data.location}, {data.district}, {data.state}."
                ),

                "local_demand": local_demand,
                "competition_level": competition_level,
                "market_potential_score": market_potential_score,
                "location_suitability": location_suitability,

                "market_reach": market_reach,

                "local_opportunities": local_opportunities,
                "local_risks": local_risks,

                "recommendation": hyper_local_recommendation
            }

                

    # ==================================================
    # STEP 10: OVERALL BUSINESS RISK ANALYSIS
    # ==================================================

    risk_score = 0
    risk_factors = []
    risk_recommendations = []

    if monthly_profit <= 0:
        risk_score += 35
        risk_factors.append(
            "The business is currently generating no positive monthly profit."
        )
        risk_recommendations.append(
            "Reduce operating expenses and improve monthly revenue."
        )
    elif profit_margin < 10:
        risk_score += 25
        risk_factors.append("The profit margin is low.")
        risk_recommendations.append(
            "Improve profit margins by controlling expenses and increasing sales."
        )
    elif profit_margin < 20:
        risk_score += 15
        risk_factors.append("The profit margin is moderate.")
        risk_recommendations.append(
            "Monitor costs and work toward improving profit margins."
        )

    if expense_ratio >= 90:
        risk_score += 25
        risk_factors.append(
            "Expenses consume more than 90% of monthly revenue."
        )
        risk_recommendations.append(
            "Urgently review major operating expenses."
        )
    elif expense_ratio >= 75:
        risk_score += 15
        risk_factors.append(
            "A high percentage of revenue is spent on expenses."
        )
        risk_recommendations.append(
            "Control operating costs to improve cash surplus."
        )

    if affordability_status == "Not Affordable":
        risk_score += 25
        risk_factors.append(
            "Loan EMI may not be manageable with current income."
        )
        risk_recommendations.append(
            "Avoid large loans until cash flow improves."
        )
    elif affordability_status == "High Repayment Burden":
        risk_score += 15
        risk_factors.append(
            "Loan EMI may create a significant repayment burden."
        )
        risk_recommendations.append(
            "Consider reducing the loan amount."
        )
    elif affordability_status == "Moderately Affordable":
        risk_score += 8
        risk_factors.append(
            "Loan repayment may put pressure on cash flow."
        )
        risk_recommendations.append(
            "Maintain an emergency reserve for EMI payments."
        )

    if competition_level == "High":
        risk_score += 15
        risk_factors.append(
            "High local competition may affect customer acquisition."
        )
        risk_recommendations.append(
            "Differentiate through better service, pricing, or products."
        )
    elif competition_level == "Medium":
        risk_score += 8
        risk_factors.append(
            "Moderate competition requires regular market monitoring."
        )
        risk_recommendations.append(
            "Study competitors and improve customer value."
        )

    if local_demand == "Medium":
        risk_score += 8
        risk_factors.append(
            "Local demand is moderate and may require marketing efforts."
        )
        risk_recommendations.append(
            "Use local marketing and customer feedback."
        )

    if data.experience == "Beginner":
        risk_score += 10
        risk_factors.append(
            "Limited business experience may increase operational risk."
        )
        risk_recommendations.append(
            "Seek training, mentorship, or expert guidance."
        )
    elif data.experience == "Intermediate":
        risk_score += 5

    if category == "dairy":
        risk_score += 5
        risk_factors.append(
            "Dairy operations are affected by cattle health and feed costs."
        )
        risk_recommendations.append(
            "Maintain veterinary care and monitor feed costs."
        )
    elif category == "poultry":
        risk_score += 5
        risk_factors.append(
            "Poultry businesses face disease and feed price risks."
        )
        risk_recommendations.append(
            "Follow hygiene and disease prevention practices."
        )
    elif category == "agriculture":
        risk_score += 8
        risk_factors.append(
            "Agriculture is exposed to weather and crop price risks."
        )
        risk_recommendations.append(
            "Use suitable crops and efficient irrigation."
        )
    elif category == "fishery":
        risk_score += 8
        risk_factors.append(
            "Fishery operations can be affected by water quality and disease."
        )
        risk_recommendations.append(
            "Monitor water quality and fish health."
        )

    risk_score = min(max(risk_score, 0), 100)

    if risk_score >= 70:
        overall_risk_level = "High Risk"
        risk_summary = (
            "Significant financial, market, or operational risks require attention."
        )
    elif risk_score >= 40:
        overall_risk_level = "Medium Risk"
        risk_summary = (
            "Important risks should be managed through regular financial "
            "and market monitoring."
        )
    else:
        overall_risk_level = "Low Risk"
        risk_summary = (
            "The business currently shows a relatively manageable risk profile."
        )

    if not risk_factors:
        risk_factors.append(
            "No major risk factors were identified from the entered information."
        )

    if not risk_recommendations:
        risk_recommendations.append(
            "Continue monitoring business performance and maintain an emergency reserve."
        )

    risk_analysis = {
        "risk_score": risk_score,
        "overall_risk_level": overall_risk_level,
        "risk_summary": risk_summary,
        "risk_factors": risk_factors,
        "risk_recommendations": risk_recommendations,
    }

    # ==================================================
    # STEP 11: BUSINESS ADVICE
    # ==================================================

    if category == "dairy":
        business_advice = [
            "Consider starting with a manageable number of cattle.",
            "Maintain proper cattle nutrition and veterinary care.",
            "Build a reliable local milk collection and customer network.",
            "Monitor feed and healthcare costs carefully.",
            "Consider value-added products such as curd, paneer and ghee.",
        ]

    elif category == "poultry":
        business_advice = [
            "Start with a manageable number of birds.",
            "Maintain proper hygiene and vaccination schedules.",
            "Monitor feed costs carefully.",
            "Develop reliable local buyers before expanding.",
            "Keep emergency funds for disease and market risks.",
        ]

    elif category == "fishery":
        business_advice = [
            "Check water availability and quality before starting.",
            "Select fish species suitable for the local climate.",
            "Monitor feed and water management costs.",
            "Build connections with local fish markets.",
            "Plan for seasonal demand and weather-related risks.",
        ]

    elif category == "agriculture":
        business_advice = [
            "Choose crops suitable for local soil and climate.",
            "Use efficient irrigation methods.",
            "Monitor fertilizer and input costs.",
            "Consider direct-to-market selling.",
            "Explore value-added agricultural products.",
        ]

    else:
        business_advice = [
            "Start with a small pilot before making a large investment.",
            "Study local demand and competitors.",
            "Maintain accurate records of revenue and expenses.",
            "Keep a financial reserve for unexpected expenses.",
            "Consider expanding after achieving stable profits.",
        ]

    # ==================================================
    # STEP 12: FINAL RECOMMENDATION
    # ==================================================

    if feasibility == "Not Feasible":
        recommendation = (
            f"{data.business_name} is currently not feasible based on "
            "the provided financial information. Review expenses and revenue."
        )
    elif feasibility == "Highly Feasible":
        recommendation = (
            f"{data.business_name} appears highly feasible based on "
            "the provided financial information."
        )
    elif feasibility == "Feasible":
        recommendation = (
            f"{data.business_name} appears feasible. Continue monitoring "
            "expenses and market demand."
        )
    else:
        recommendation = (
            f"{data.business_name} is moderately feasible. Consider improving "
            "profit margins before major expansion."
        )

    # ==================================================
    # FINAL RESPONSE
    # ==================================================
    
    return {


        "business": data.business_name,
        "business_name": data.business_name,
        "category": data.category,
        "state": data.state,
        "district": data.district,
        "location": data.location,
        "experience": data.experience,

        "hyper_local_profile": hyper_local_profile,

        "risk_analysis": risk_analysis,

        "financial_analysis": {
            "initial_investment": round(data.investment, 2),
            "monthly_revenue": round(data.monthly_revenue, 2),
            "monthly_expenses": round(data.monthly_expenses, 2),
            "monthly_profit": round(monthly_profit, 2),
            "yearly_profit": round(yearly_profit, 2),
            "roi_percentage": round(roi, 2),
            "payback_period_months": (
                round(payback_months, 2)
                if payback_months is not None
                else None
            ),
        },

        "advanced_financial_analysis": {
            "profit_margin": round(profit_margin, 2),
            "expense_ratio": round(expense_ratio, 2),
            "break_even_revenue": round(break_even_revenue, 2),
            "monthly_cash_surplus": round(monthly_cash_surplus, 2),
            "financial_strength": financial_strength,
            "financial_risk": financial_risk,
        },

        "profit_projection": profit_projection,

        "feasibility": feasibility,

        "recommendation": recommendation,

        "scheme_analysis": {
            "scheme_name": scheme_name,
            "project_cost": round(project_cost, 2),
            "beneficiary_contribution": round(
                beneficiary_contribution,
                2,
            ),
            "contribution_percentage": 10,
            "eligible_loan": round(eligible_loan, 2),
            "interest_rate": interest_rate,
            "repayment_period": repayment_period,
            "message": scheme_message,
        },

        "smart_scheme_matching": {
            "matching_schemes": matching_schemes,
            "recommended_scheme": recommended_scheme,
        },

        "loan_affordability": {
    "monthly_emi": monthly_emi,
    "loan_tenure_months": loan_tenure_months,

    "moratorium_months": moratorium_months,
    "repayment_months": repayment_months,

    "total_repayment": total_repayment,
    "total_interest": total_interest,

    "emi_to_income_ratio": emi_to_income_ratio,

    "affordability_status": affordability_status,
    "affordability_message": affordability_message,

    "monthly_operational_cost": round(
        monthly_operational_cost,
        2
    ),

    "estimated_working_capital": round(
        estimated_working_capital,
        2
    ),

    "repayment_schedule": repayment_schedule,

    "quarterly_repayment_schedule": (
        quarterly_repayment_schedule
    )
},

        "business_advice": business_advice,
    }
