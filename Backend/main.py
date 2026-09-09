from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math


app = FastAPI(
    title="SIH26091 Rural Business Advisor",
    description="AI-powered rural business feasibility and financial advisory system",
    version="4.0.0"
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
    block: str
    location: str
    experience: str
    investment: float
    monthly_revenue: float
    monthly_expenses: float


class AdvisorRequest(BaseModel):
    question: str
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
        "status": "success"
    }


# ==================================================
# AI BUSINESS ADVISOR
# ==================================================

@app.post("/advisor")
def business_advisor(data: AdvisorRequest):

    question = data.question.lower().strip()

    if not question:
        return {
            "answer": "Please enter a question about your business."
        }

    business_name = data.business_name or "Your business"

    # ==================================================
    # GREETING
    # ==================================================

    if any(word in question for word in [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good evening"
    ]):

        answer = (
            f"Hello! I am your AI Business Advisor. "
            f"I can help you understand the analysis for {business_name}. "
            f"You can ask me about profit, ROI, expenses, loans, EMI, risks, "
            f"local market demand, competition, or business growth."
        )


    # ==================================================
    # PROFIT / PROFITABILITY
    # ==================================================

    elif any(word in question for word in [
        "profit",
        "profitable",
        "profitability",
        "earning",
        "earnings"
    ]):

        if data.monthly_profit > 0:

            answer = (
                f"{business_name} is currently generating an estimated "
                f"monthly profit of ₹{data.monthly_profit:,.2f}. "
            )

            if data.monthly_revenue > 0:

                profit_margin = (
                    data.monthly_profit
                    / data.monthly_revenue
                ) * 100

                answer += (
                    f"The estimated profit margin is {profit_margin:.2f}%. "
                )

            if data.monthly_profit < 10000:

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
                "You should reduce operating expenses, improve sales, and review the "
                "business model before expanding or taking additional financial risk."
            )


    # ==================================================
    # ROI
    # ==================================================

    elif any(word in question for word in [
        "roi",
        "return on investment",
        "return"
    ]):

        if data.roi_percentage >= 30:

            answer = (
                f"Your estimated ROI is {data.roi_percentage:.2f}%, which indicates "
                "strong financial performance based on the entered business data."
            )

        elif data.roi_percentage >= 15:

            answer = (
                f"Your estimated ROI is {data.roi_percentage:.2f}%, which indicates "
                "reasonable business performance. You can improve ROI by increasing "
                "profit without making a proportional increase in investment."
            )

        elif data.roi_percentage > 0:

            answer = (
                f"Your estimated ROI is {data.roi_percentage:.2f}%, which is relatively "
                "low. Focus on improving revenue, reducing costs, and using investment "
                "more efficiently."
            )

        else:

            answer = (
                "Your current ROI is not positive. The business should improve its "
                "profitability before making additional investments."
            )


    # ==================================================
    # EXPENSES / COST REDUCTION
    # ==================================================

    elif any(word in question for word in [
        "expense",
        "expenses",
        "cost",
        "reduce cost",
        "reduce expense",
        "save money"
    ]):

        if data.monthly_revenue > 0:

            expense_ratio = (
                data.monthly_expenses
                / data.monthly_revenue
            ) * 100

            answer = (
                f"Your estimated monthly expenses are ₹{data.monthly_expenses:,.2f}, "
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
                "Please provide valid revenue information for a detailed expense analysis."
            )


    # ==================================================
    # LOAN / EMI
    # ==================================================

    elif any(word in question for word in [
        "loan",
        "emi",
        "repayment",
        "afford",
        "affordable",
        "pay loan"
    ]):

        answer = (
            f"Your current loan affordability status is "
            f"'{data.affordability_status}'. "
        )

        if data.monthly_emi > 0:

            answer += (
                f"The estimated monthly EMI is ₹{data.monthly_emi:,.2f}. "
            )

        if data.affordability_status == "Affordable":

            answer += (
                "Based on the entered business figures, the repayment burden appears "
                "manageable. However, keep an emergency reserve for unexpected expenses."
            )

        elif data.affordability_status == "Moderately Affordable":

            answer += (
                "The loan may be manageable, but it can place pressure on cash flow. "
                "Maintain a reserve and avoid taking additional debt."
            )

        elif data.affordability_status == "High Repayment Burden":

            answer += (
                "The repayment burden is high. Consider reducing the loan amount, "
                "increasing your own contribution, or improving business cash flow."
            )

        else:

            answer += (
                "The current business figures indicate that loan repayment may be risky. "
                "Improve profitability before taking a large financial commitment."
            )


    # ==================================================
    # RISK
    # ==================================================

    elif any(word in question for word in [
        "risk",
        "risky",
        "danger",
        "problem",
        "threat"
    ]):

        answer = (
            f"The overall business risk level is '{data.overall_risk_level}' and "
            f"the financial risk is '{data.financial_risk}'. "
        )

        if data.overall_risk_level == "High Risk":

            answer += (
                "The priority should be improving profitability, reducing expenses, "
                "and avoiding excessive loan commitments."
            )

        elif data.overall_risk_level == "Medium Risk":

            answer += (
                "The business has important risks that should be monitored carefully. "
                "Focus on financial discipline, market competition, and stable cash flow."
            )

        else:

            answer += (
                "The current risk profile appears manageable, but you should continue "
                "monitoring market conditions, costs, and business performance."
            )


    # ==================================================
    # MARKET / DEMAND / COMPETITION
    # ==================================================

    elif any(word in question for word in [
        "market",
        "demand",
        "competition",
        "customer",
        "customers",
        "local"
    ]):

        answer = (
            f"The estimated local demand is '{data.local_demand}' and "
            f"the competition level is '{data.competition_level}'. "
        )

        if data.local_demand == "High":

            answer += (
                "This suggests good potential for customer acquisition. Focus on "
                "quality, reliability, and building strong local customer relationships."
            )

        elif data.local_demand == "Medium":

            answer += (
                "There is reasonable potential, but marketing and customer feedback "
                "will be important for growing the business."
            )

        else:

            answer += (
                "Demand should be validated carefully before expanding. Start with "
                "a smaller scale and test customer response."
            )


    # ==================================================
    # GROWTH / IMPROVEMENT
    # ==================================================

    elif any(word in question for word in [
        "grow",
        "growth",
        "improve",
        "better",
        "increase",
        "expand",
        "future"
    ]):

        answer = (
            f"To improve {business_name}, focus on these priorities: "
            "1) increase profitable sales, "
            "2) control unnecessary expenses, "
            "3) maintain accurate income and expense records, "
            "4) study customer needs and competitors, "
            "5) build an emergency cash reserve, and "
            "6) expand gradually only after achieving stable profits."
        )


    # ==================================================
    # FEASIBILITY
    # ==================================================

    elif any(word in question for word in [
        "feasible",
        "feasibility",
        "should i start",
        "good business",
        "worth starting"
    ]):

        answer = (
            f"The current feasibility assessment for {business_name} is "
            f"'{data.feasibility}'. "
        )

        if data.feasibility == "Highly Feasible":

            answer += (
                "The entered financial figures show strong potential. Continue "
                "validating actual local demand before making the full investment."
            )

        elif data.feasibility == "Feasible":

            answer += (
                "The business appears viable, but you should carefully manage "
                "expenses and monitor local market performance."
            )

        elif data.feasibility == "Moderately Feasible":

            answer += (
                "The business has potential but should improve profitability and "
                "financial margins before major expansion."
            )

        else:

            answer += (
                "The current financial figures do not support strong feasibility. "
                "Review revenue assumptions, expenses, and investment requirements."
            )


    # ==================================================
    # DEFAULT AI RESPONSE
    # ==================================================

    else:

        answer = (
            f"Based on the analysis of {business_name}, the current feasibility is "
            f"'{data.feasibility}', with an estimated monthly profit of "
            f"₹{data.monthly_profit:,.2f} and ROI of {data.roi_percentage:.2f}%. "
            "You can ask me specifically about profit, ROI, expenses, loan EMI, "
            "risks, market demand, competition, feasibility, or business growth."
        )


    return {
        "answer": answer
    }


# ==================================================
# BUSINESS ANALYSIS
# ==================================================

@app.post("/analyze")
def analyze_business(data: BusinessRequest):

    # ==================================================
    # STEP 1: BASIC FINANCIAL CALCULATIONS
    # ==================================================

    monthly_profit = (
        data.monthly_revenue - data.monthly_expenses
    )

    yearly_profit = monthly_profit * 12

    if data.investment > 0 and yearly_profit > 0:
        roi = (
            yearly_profit / data.investment
        ) * 100
    else:
        roi = 0

    if monthly_profit > 0:
        payback_months = (
            data.investment / monthly_profit
        )
    else:
        payback_months = None


    # ==================================================
    # STEP 2: ADVANCED FINANCIAL ANALYSIS
    # ==================================================

    if data.monthly_revenue > 0:
        profit_margin = (
            monthly_profit / data.monthly_revenue
        ) * 100
    else:
        profit_margin = 0

    if data.monthly_revenue > 0:
        expense_ratio = (
            data.monthly_expenses / data.monthly_revenue
        ) * 100
    else:
        expense_ratio = 0

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
    # 12-MONTH PROFIT PROJECTION
    # ==================================================

    profit_projection = []
    cumulative_profit = 0

    for month in range(1, 13):

        cumulative_profit += monthly_profit

        profit_projection.append({
            "month": f"Month {month}",
            "monthly_profit": round(monthly_profit, 2),
            "cumulative_profit": round(cumulative_profit, 2)
        })


    # ==================================================
    # FEASIBILITY
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
    # Available margin capital represents 10% of project cost.
    # Therefore: project cost = margin capital / 0.10.
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
    moratorium_months = 0
    repayment_months = None

    if project_cost <= 140000:

        scheme_name = "Micro Finance Scheme"
        eligible_loan = min(eligible_loan, 125000)
        interest_rate = 6.5
        repayment_period = "3 years including 3-month moratorium"
        loan_tenure_months = 36
        moratorium_months = 3

        scheme_message = (
            "Eligible for the Micro Finance Scheme."
        )

    elif project_cost <= 5000000:

        scheme_name = "Term Loan Scheme"
        eligible_loan = min(eligible_loan, 4500000)
        interest_rate = 8.0
        repayment_period = "7 years including 6-month moratorium"
        loan_tenure_months = 84
        moratorium_months = 6

        scheme_message = (
            "Eligible for the Term Loan Scheme."
        )

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

    repayment_schedule = []
    quarterly_repayment_schedule = []

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

        repayment_months = loan_tenure_months - moratorium_months
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

            outstanding_principal = round(eligible_loan, 2)
            total_regular_interest = 0.0
            total_moratorium_interest = 0.0

            # Moratorium interest is shown separately.
            # The PS does not specify capitalization, so it is not
            # silently added to principal.
            for month in range(1, loan_tenure_months + 1):

                monthly_interest = round(
                    outstanding_principal * monthly_interest_rate,
                    2
                )

                if month <= moratorium_months:

                    principal_payment = 0.0
                    emi_payment = 0.0
                    total_moratorium_interest += monthly_interest

                else:

                    emi_payment = monthly_emi
                    principal_payment = round(
                        emi_payment - monthly_interest,
                        2
                    )

                    if month == loan_tenure_months:
                        principal_payment = round(
                            outstanding_principal,
                            2
                        )
                        emi_payment = round(
                            principal_payment + monthly_interest,
                            2
                        )

                    elif principal_payment > outstanding_principal:
                        principal_payment = round(
                            outstanding_principal,
                            2
                        )
                        emi_payment = round(
                            principal_payment + monthly_interest,
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

            total_interest = round(
                total_regular_interest + total_moratorium_interest,
                2
            )

            total_repayment = round(
                eligible_loan + total_interest,
                2
            )

            # Build the PS-required quarterly repayment summary.
            for quarter_start in range(1, loan_tenure_months + 1, 3):
                quarter_end = min(
                    quarter_start + 2,
                    loan_tenure_months
                )

                quarter_rows = repayment_schedule[
                    quarter_start - 1:quarter_end
                ]

                quarterly_repayment_schedule.append({
                    "quarter": ((quarter_start - 1) // 3) + 1,
                    "months": f"{quarter_start}-{quarter_end}",
                    "phase": (
                        "Moratorium"
                        if quarter_end <= moratorium_months
                        else (
                            "Mixed"
                            if quarter_start <= moratorium_months
                            else "Repayment"
                        )
                    ),
                    "emi_total": round(
                        sum(row["emi"] for row in quarter_rows),
                        2
                    ),
                    "interest_total": round(
                        sum(row["interest"] for row in quarter_rows),
                        2
                    ),
                    "principal_total": round(
                        sum(row["principal"] for row in quarter_rows),
                        2
                    ),
                    "outstanding_principal": round(
                        quarter_rows[-1]["outstanding_principal"],
                        2
                    )
                })

            if data.monthly_revenue > 0:

                emi_to_income_ratio = round(
                    (monthly_emi / data.monthly_revenue) * 100,
                    2
                )

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
                        "Loan is possible but will put pressure on cash flow."
                    )

                else:

                    affordability_status = "Affordable"
                    affordability_message = (
                        "EMI appears manageable based on current figures."
                    )


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
                2
            ),
            "interest_rate": 6.5,
            "repayment_period": "3 years including 3-month moratorium",
            "moratorium_months": 3,
            "match_score": 95,
            "reason": (
                "Project cost falls within the Micro Finance Scheme limit."
            )
        })

    elif project_cost <= 5000000:

        matching_schemes.append({
            "scheme_name": "Term Loan Scheme",
            "project_cost_limit": "₹1.40 lakh to ₹50 lakh",
            "maximum_loan": 4500000,
            "eligible_loan": round(
                min(maximum_loan, 4500000),
                2
            ),
            "interest_rate": 8.0,
            "repayment_period": "7 years including 6-month moratorium",
            "moratorium_months": 6,
            "match_score": 95,
            "reason": (
                "Project cost falls within the Term Loan Scheme limit."
            )
        })

    if matching_schemes:

        recommended_scheme = max(
            matching_schemes,
            key=lambda scheme: scheme["match_score"]
        )

    else:

        recommended_scheme = {
            "scheme_name": "No Standard Scheme Match",
            "match_score": 0,
            "reason": "No standard scheme match found."
        }


    # ==================================================
    # HYPER-LOCAL MARKET ANALYSIS
    # ==================================================

    business = data.business_name.lower()
    category = data.category.lower()

    if category in [
        "dairy",
        "agriculture",
        "poultry",
        "fishery"
    ]:
        local_demand = "High"

    else:
        local_demand = "Medium"

    if category in [
        "retail",
        "service"
    ]:
        competition_level = "High"

    elif category in [
        "dairy",
        "poultry",
        "agriculture"
    ]:
        competition_level = "Medium"

    else:
        competition_level = "Medium"

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

    if market_potential_score >= 80:
        location_suitability = "Highly Suitable"
    elif market_potential_score >= 60:
        location_suitability = "Suitable"
    else:
        location_suitability = "Needs Improvement"


    # ==================================================
    # PS REQUIREMENT 1: MARKET REACH
    # ==================================================

    # The PS requires the immediate consumer market to be assessed
    # within a 5–10 km radius and the primary distribution channels
    # to be identified.
    #
    # The current location_data.py contains state/UT names only, so
    # we do not fabricate village-level population counts. The
    # consumer-base field is therefore explicitly marked as an
    # estimate until verified demographic data is connected.

    # Do not invent village/block population numbers.  The current
    # location dataset does not contain verified village-level demographic
    # counts, so the system explicitly reports the limitation instead of
    # presenting a fabricated consumer count.
    market_reach = {
        "primary_radius_km": 5,
        "extended_radius_km": 10,
        "service_area": (
            f"5–10 km from {data.location}, {data.block}, {data.district}"
        ),
        "consumer_base": (
            "Not numerically estimated: verified village/block demographic "
            "data is not currently available in the configured dataset."
        ),
        "consumer_base_status": "Data required",
        "data_source": "No verified local demographic dataset connected",
        "confidence": "Low",
        "reach_type": "Estimated service area; population count unavailable",
        "distribution_channels": []
    }

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

    if local_demand == "High":
        market_reach["reach_assessment"] = (
            "The business has strong potential to serve customers "
            "within the 5–10 km local service area."
        )
    else:
        market_reach["reach_assessment"] = (
            "The business can serve the local 5–10 km market, but "
            "demand should be validated before expansion."
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
    # PS REQUIREMENT 2: OPPORTUNITY ANALYSIS
    # ==================================================
    # The PS asks the system to highlight unserved/underserved niches
    # in the selected business sector for the specific local economy.
    # The current dataset does not contain verified establishment-level
    # demand-gap data, so these are explicitly presented as candidate
    # niches/hypotheses requiring local validation rather than factual
    # claims about an unserved market.

    opportunity_analysis = {
        "status": "Needs local validation",
        "focus": "Potential unserved/underserved niches",
        "location_scope": (
            f"{data.location}, {data.block}, {data.district}, {data.state}"
        ),
        "identified_niches": [],
        "evidence_basis": [
            f"Selected business category: {data.category}",
            f"Local demand indicator: {local_demand}",
            f"Competition indicator: {competition_level}",
            "No verified establishment-level demand-gap dataset is connected."
        ],
        "data_source": "Rule-based sector hypotheses; local validation data required",
        "confidence": "Low",
        "methodology": (
            "Candidate niches are generated from the selected sector and "
            "local demand/competition indicators, then must be validated "
            "through local customer interviews, competitor checks and "
            "current market-price observations."
        )
    }

    if category == "dairy":
        opportunity_analysis["identified_niches"] = [
            "Hygienic packaged milk for nearby households",
            "Value-added dairy products such as paneer, curd and ghee",
            "Doorstep dairy delivery for nearby customers",
            "Bulk dairy supply to tea shops, restaurants and small institutions"
        ]
    elif category == "poultry":
        opportunity_analysis["identified_niches"] = [
            "Cleaned and graded egg supply for local retailers",
            "Direct household egg and poultry delivery",
            "Regular poultry supply contracts with restaurants and hotels",
            "Bundled poultry feed/essential support for nearby small producers"
        ]
    elif category == "agriculture":
        opportunity_analysis["identified_niches"] = [
            "Last-mile agricultural input delivery",
            "Custom farm services for small and marginal farmers",
            "Crop aggregation, grading and local market linkage",
            "Value-added processing of locally suitable agricultural produce"
        ]
    elif category == "fishery":
        opportunity_analysis["identified_niches"] = [
            "Cleaned and ready-to-cook fish for nearby households",
            "Doorstep fresh-fish delivery",
            "Regular fresh-fish supply to restaurants and local retailers",
            "Small-scale ice/cold-chain support for local fish sellers"
        ]
    elif category == "retail":
        opportunity_analysis["identified_niches"] = [
            "Last-mile delivery of essential goods to nearby households",
            "Digital/phone-based ordering for repeat local customers",
            "Focused stocking of frequently requested local products",
            "Home-delivery service for elderly or mobility-limited customers"
        ]
    elif category == "service":
        opportunity_analysis["identified_niches"] = [
            "Mobile repair and maintenance services",
            "Local bookkeeping and digital business support",
            "Farm equipment rental or on-demand service support",
            "Hyper-local transport, delivery or logistics assistance"
        ]
    else:
        opportunity_analysis["identified_niches"] = [
            "Unmet convenience or last-mile service needs",
            "Direct local delivery or doorstep service",
            "Niche products/services requested repeatedly by local customers",
            "Small institutional or business-to-business supply opportunities"
        ]

    # Make the rule-based result slightly more conservative when local
    # demand is weak or competition is high.
    if local_demand == "Low" or competition_level == "High":
        opportunity_analysis["validation_priority"] = "High"
        opportunity_analysis["note"] = (
            "Validate each candidate niche carefully because the available "
            "indicators do not establish a local supply-demand gap."
        )
    else:
        opportunity_analysis["validation_priority"] = "Medium"
        opportunity_analysis["note"] = (
            "Candidate niches may be worth testing, but local supply-demand "
            "evidence is still required before investment."
        )


    # ==================================================
    # PS REQUIREMENT 3: GENERAL BUSINESS ANALYSIS (SWOT)
    # ==================================================
    # SWOT is tailored to the selected micro-enterprise, current financial
    # figures, experience level, local demand/competition indicators, and
    # available margin capital. It uses the existing local risk/opportunity
    # logic without replacing those features.

    swot_analysis = {
        "scope": (
            f"{data.business_name} | {data.category} | "
            f"{data.location}, {data.block}, {data.district}, {data.state}"
        ),
        "budget_context": {
            "available_margin_capital": round(data.investment, 2),
            "monthly_revenue": round(data.monthly_revenue, 2),
            "monthly_expenses": round(data.monthly_expenses, 2),
            "monthly_profit": round(monthly_profit, 2)
        },
        "strengths": [],
        "weaknesses": [],
        "opportunities": [],
        "threats": [],
        "methodology": (
            "SWOT is generated from the entered micro-enterprise budget, "
            "financial indicators, experience level, local demand and "
            "competition indicators, plus the existing local opportunity "
            "and risk assessment."
        ),
        "confidence": "Moderate - rule-based assessment"
    }

    # Strengths: positive current economics, experience and/or local demand.
    if monthly_profit > 0:
        swot_analysis["strengths"].append(
            f"Positive estimated monthly cash surplus of ₹{monthly_profit:,.2f}."
        )
    else:
        swot_analysis["strengths"].append(
            "The current plan can be improved through controlled pilot operations and cost monitoring."
        )

    if data.experience == "Experienced":
        swot_analysis["strengths"].append(
            "Experienced operator profile can support execution and customer management."
        )
    elif data.experience == "Intermediate":
        swot_analysis["strengths"].append(
            "Intermediate experience provides an existing operational base to build on."
        )
    else:
        swot_analysis["strengths"].append(
            "Beginner profile allows a structured pilot approach before major expansion."
        )

    if local_demand == "High":
        swot_analysis["strengths"].append(
            "The selected sector has a high local-demand indicator in the current rule-based assessment."
        )

    # Weaknesses: cost pressure, low/negative profit, high competition, beginner profile.
    if monthly_profit <= 0:
        swot_analysis["weaknesses"].append(
            "Current estimated monthly profit is not positive."
        )
    elif expense_ratio >= 65:
        swot_analysis["weaknesses"].append(
            f"Operating expenses consume about {expense_ratio:.2f}% of estimated monthly revenue."
        )

    if data.experience == "Beginner":
        swot_analysis["weaknesses"].append(
            "Limited operating experience may increase execution and market-learning requirements."
        )

    if competition_level == "High":
        swot_analysis["weaknesses"].append(
            "High competition indicator may make customer acquisition more difficult."
        )

    # Opportunities: reuse the new PS opportunity-analysis candidates, without
    # claiming that any niche is already verified as unserved.
    swot_analysis["opportunities"] = [
        f"Test candidate niche: {item}."
        for item in opportunity_analysis["identified_niches"][:3]
    ]
    swot_analysis["opportunities"].append(
        "Validate local customer demand, competitor coverage and pricing before scaling."
    )

    # Threats: existing local risks plus financial/market pressure.
    swot_analysis["threats"] = list(local_risks[:3])
    if affordability_status in ["Not Affordable", "High Repayment Burden"]:
        swot_analysis["threats"].append(
            "Loan repayment pressure could strain cash flow if the business does not achieve projected sales."
        )
    if competition_level == "High":
        swot_analysis["threats"].append(
            "Competitive pressure may reduce achievable market share or pricing power."
        )

    # Ensure every SWOT quadrant remains populated even when a condition does not apply.
    if not swot_analysis["weaknesses"]:
        swot_analysis["weaknesses"].append(
            "No major financial weakness was detected from the entered figures; validate operating assumptions locally."
        )
    if not swot_analysis["threats"]:
        swot_analysis["threats"].append(
            "Local demand, input costs and competitor behavior may change over time."
        )


    hyper_local_recommendation = (
        f"{data.business_name} in {data.location}, {data.district}, "
        f"{data.state} has {location_suitability.lower()} market suitability. "
        f"Estimated local demand is {local_demand.lower()} with "
        f"{competition_level.lower()} competition."
    )

    hyper_local_profile = {
        "state": data.state,
        "district": data.district,
        "block": data.block,
        "location": data.location,
        "category": data.category,
        "profile_summary": (
            f"Business analysis prepared for {data.business_name} "
            f"in {data.location}, {data.block}, {data.district}, {data.state}."
        ),
        "local_demand": local_demand,
        "competition_level": competition_level,
        "market_potential_score": market_potential_score,
        "location_suitability": location_suitability,
        "market_reach": market_reach,
        "opportunity_analysis": opportunity_analysis,
        "swot_analysis": swot_analysis,
        "local_opportunities": local_opportunities,
        "local_risks": local_risks,
        "recommendation": hyper_local_recommendation
    }


    # ==================================================
    # OVERALL BUSINESS RISK ANALYSIS
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

        risk_factors.append(
            "The profit margin is low."
        )

        risk_recommendations.append(
            "Improve profit margins by controlling expenses and increasing sales."
        )

    elif profit_margin < 20:

        risk_score += 15

        risk_factors.append(
            "The profit margin is moderate."
        )

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
            "Important risks should be managed through regular financial and market monitoring."
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
        "risk_recommendations": risk_recommendations
    }


    # ==================================================
    # BUSINESS ADVICE
    # ==================================================

    if category == "dairy":

        business_advice = [
            "Consider starting with a manageable number of cattle.",
            "Maintain proper cattle nutrition and veterinary care.",
            "Build a reliable local milk collection and customer network.",
            "Monitor feed and healthcare costs carefully.",
            "Consider value-added products such as curd, paneer and ghee."
        ]

    elif category == "poultry":

        business_advice = [
            "Start with a manageable number of birds.",
            "Maintain proper hygiene and vaccination schedules.",
            "Monitor feed costs carefully.",
            "Develop reliable local buyers before expanding.",
            "Keep emergency funds for disease and market risks."
        ]

    elif category == "fishery":

        business_advice = [
            "Check water availability and quality before starting.",
            "Select fish species suitable for the local climate.",
            "Monitor feed and water management costs.",
            "Build connections with local fish markets.",
            "Plan for seasonal demand and weather-related risks."
        ]

    elif category == "agriculture":

        business_advice = [
            "Choose crops suitable for local soil and climate.",
            "Use efficient irrigation methods.",
            "Monitor fertilizer and input costs.",
            "Consider direct-to-market selling.",
            "Explore value-added agricultural products."
        ]

    else:

        business_advice = [
            "Start with a small pilot before making a large investment.",
            "Study local demand and competitors.",
            "Maintain accurate records of revenue and expenses.",
            "Keep a financial reserve for unexpected expenses.",
            "Consider expanding after achieving stable profits."
        ]


    # ==================================================
    # FINAL RECOMMENDATION
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
        "category": data.category,
        "state": data.state,
        "district": data.district,
        "block": data.block,
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
            )
        },

        "advanced_financial_analysis": {
            "profit_margin": round(profit_margin, 2),
            "expense_ratio": round(expense_ratio, 2),
            "break_even_revenue": round(break_even_revenue, 2),
            "monthly_cash_surplus": round(monthly_cash_surplus, 2),
            "financial_strength": financial_strength,
            "financial_risk": financial_risk
        },

        "profit_projection": profit_projection,

        "feasibility": feasibility,

        "recommendation": recommendation,

        "scheme_analysis": {
            "scheme_name": scheme_name,
            "margin_capital": round(margin_capital, 2),
            "project_cost": round(project_cost, 2),
            "beneficiary_contribution": round(
                beneficiary_contribution,
                2
            ),
            "contribution_percentage": 10,
            "maximum_loan": round(maximum_loan, 2),
            "eligible_loan": round(eligible_loan, 2),
            "interest_rate": interest_rate,
            "repayment_period": repayment_period,
            "message": scheme_message
        },

        "smart_scheme_matching": {
            "matching_schemes": matching_schemes,
            "recommended_scheme": recommended_scheme
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
                monthly_operational_cost, 2
            ),
            "estimated_working_capital": round(
                estimated_working_capital, 2
            ),
            "repayment_schedule": repayment_schedule,
            "quarterly_repayment_schedule": quarterly_repayment_schedule
        },

        "business_advice": business_advice
    }