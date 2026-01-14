import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import hashlib

# Page configuration
st.set_page_config(
    page_title="Micro Brewery Financial Analyzer",
    page_icon="🍺",
    layout="wide"
)

# ==================== AUTHENTICATION SYSTEM ====================
def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

# User credentials (username: password_hash)
# Default credentials - CHANGE THESE FOR PRODUCTION
USERS = {
    "partner1": hash_password("brew2026"),  # username: partner1, password: brew2026
    "partner2": hash_password("brew2026"),  # username: partner2, password: brew2026
    "partner3": hash_password("brew2026"),  # username: partner3, password: brew2026
    "admin": hash_password("admin123")      # username: admin, password: admin123
}

def check_password():
    """Returns True if user entered correct password"""
    
    def login_form():
        """Display login form"""
        st.markdown("### 🔐 Secure Login")
        st.markdown("*Three-Investor Partnership Access*")
        
        with st.form("login_form"):
            username = st.text_input("Username", key="username_input")
            password = st.text_input("Password", type="password", key="password_input")
            submit = st.form_submit_button("Login")
            
            if submit:
                if username in USERS and USERS[username] == hash_password(password):
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
                    st.info("""
                    **Default Credentials:**
                    - Username: partner1, partner2, partner3, or admin
                    - Password: brew2026 (partners) or admin123 (admin)
                    
                    ⚠️ Change these credentials in production!
                    """)
    
    def logout():
        """Logout function"""
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        st.rerun()
    
    # Check if already authenticated
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if not st.session_state["authenticated"]:
        # Show login page
        st.title("🍺 Charlotte-Concord Micro Brewery Financial Analyzer")
        st.markdown("### Business Feasibility Analysis Tool")
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            login_form()
            
        st.markdown("---")
        st.info("""
        **About This Tool:**
        This financial analyzer helps evaluate the feasibility of starting a micro brewery 
        in the Charlotte-Concord region with three investor partners.
        
        **Features:**
        - Market analysis of 30+ local breweries
        - Complete financial modeling
        - Revenue projections and expense analysis
        - 3-investor ROI calculations
        - 36-month cashflow projections
        """)
        return False
    else:
        # User is authenticated - show logout button in sidebar
        with st.sidebar:
            st.success(f"✅ Logged in as: **{st.session_state['username']}**")
            if st.button("🚪 Logout", type="secondary"):
                logout()
            st.markdown("---")
        return True

# Check authentication before showing app
if not check_password():
    st.stop()

# Title and Introduction (only shown after login)
st.title("🍺 Charlotte-Concord Micro Brewery Financial Analyzer")
st.markdown("### Business Feasibility Analysis Tool for Three Investor Partners")

# Sidebar for navigation
page = st.sidebar.selectbox(
    "Navigate",
    ["Market Overview", "Financial Inputs", "Revenue Projections", "Expense Analysis", "Investor Analysis", "Dashboard"]
)

# Initialize session state for data persistence
if 'data_initialized' not in st.session_state:
    st.session_state.data_initialized = True
    # Default values based on research
    st.session_state.initial_capital = 400000
    st.session_state.monthly_rent = 5000
    st.session_state.monthly_payroll = 15000
    st.session_state.monthly_insurance = 1500
    st.session_state.monthly_utilities = 2500
    st.session_state.monthly_marketing = 3000
    st.session_state.equipment_cost = 150000

# ==================== MARKET OVERVIEW PAGE ====================
if page == "Market Overview":
    st.header("Market Research: Charlotte-Concord Region")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🍺 Local Craft Breweries")
        st.markdown("**Charlotte has 30+ craft breweries** - one of the fastest-growing craft beer scenes in the Southeast")
        
        breweries = pd.DataFrame({
            'Brewery': [
                'Olde Mecklenburg Brewery (OMB)',
                'NoDa Brewing Company',
                'Wooden Robot Brewery',
                'Divine Barrel Brewing',
                'Cabarrus Brewing Co.',
                'Birdsong Brewing',
                'Lower Left Brewing',
                'Petty Thieves Brewing',
                'HopFly Brewing',
                'Southern Strain (Concord)'
            ],
            'Location': [
                'Charlotte (Since 2009)',
                'Charlotte NoDa',
                'Charlotte (NoDa & South End)',
                'Charlotte NoDa',
                'Concord',
                'Charlotte Belmont',
                'Charlotte LoSo',
                'Charlotte (Camp North End)',
                'Charlotte',
                'Concord'
            ],
            'Specialties': [
                'German-style lagers',
                'IPAs, Wide variety',
                'Good Morning Vietnam blonde ale',
                'West Coast IPAs, Lagers',
                'Core beers, Local focus',
                'American-style unfiltered ale',
                'IPAs, Sours, Belgian styles',
                'Saisons, Sours, Lagers',
                'Hazy IPAs, West Coast IPAs',
                'Various craft styles'
            ],
            'Features': [
                'Largest biergarten in Southeast',
                'Beer garden, Established 2011',
                'Two locations, Innovation',
                'Rotating selections',
                '100% local, Events venue',
                'Est. 2011, Community focus',
                '7-barrel brewhouse, Opened 2019',
                'Eclectic, unique styles',
                'Rocky Mount expansion',
                'Plaza Midwood taproom'
            ]
        })
        
        st.dataframe(breweries, use_container_width=True, hide_index=True)
        
        st.success("""
        **Key Insights**: 
        - Charlotte established its craft beer scene in 2009 (OMB)
        - 30+ breweries currently operating
        - Strong brewery tourism and taproom culture
        - Concord area has active breweries with Charlotte access
        """)
    
    with col2:
        st.subheader("📊 Industry Statistics")
        
        metrics_col1, metrics_col2 = st.columns(2)
        with metrics_col1:
            st.metric("US Craft Breweries", "9,552", help="Total craft breweries (2022)")
            st.metric("Charlotte Metro Breweries", "30+", help="Within Charlotte-Concord region")
            st.metric("Typical Profit Margin", "20-25%", help="Net profit margin for successful breweries")
        with metrics_col2:
            st.metric("Gross Margin on Beer", "74-92%", help="Before operating expenses")
            st.metric("Taproom Advantage", "Higher", help="Direct sales = better margins")
            st.metric("Avg Annual Revenue", "$1-3M", help="Small craft brewery range")
        
        st.subheader("💰 Market Opportunity")
        st.markdown("""
        **Revenue Channels:**
        - **Taproom Sales**: Highest margins (direct-to-consumer)
        - **Self-Distribution**: Better margins than distributors
        - **Distribution Partnerships**: Volume sales, lower margins
        - **Tours & Events**: Additional revenue + marketing
        - **Merchandise**: Branded items (t-shirts, glassware)
        - **Food Service** (optional): Gastropub model
        
        **Charlotte-Concord Advantages:**
        - Established craft beer culture (15+ years)
        - Growing population and tourism
        - Brewery-hopping is popular activity
        - Strong local support for craft businesses
        - Lower costs than major metro areas
        - NC beer-friendly regulations
        """)
        
        st.info("""
        **Competitive Positioning Tips:**
        - Differentiate with unique beer styles
        - Focus on quality and consistency
        - Build strong taproom experience
        - Engage local community
        - Consider niche markets (sours, lagers, sessionable beers)
        """)

# ==================== FINANCIAL INPUTS PAGE ====================
elif page == "Financial Inputs":
    st.header("💵 Capital & Fixed Expenses Input")
    
    tab1, tab2 = st.tabs(["Initial Capital", "Monthly Operating Expenses"])
    
    with tab1:
        st.subheader("One-Time Startup Costs")
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.equipment_cost = st.number_input(
                "Brewing Equipment (Brewhouse, Fermenters, etc.)",
                min_value=0,
                value=st.session_state.equipment_cost,
                step=10000,
                help="7-barrel system: ~$150K; 15-barrel: ~$250K; includes brewhouse, fermenters, bright tanks"
            )
            
            facility_buildout = st.number_input(
                "Facility Build-out & Renovations",
                min_value=0,
                value=50000,
                step=5000,
                help="Production space, taproom, plumbing, electrical, $10-30/sq ft typical"
            )
            
            licensing_fees = st.number_input(
                "Licensing & Legal Fees",
                min_value=0,
                value=10000,
                step=1000,
                help="TTB Brewer's Notice (federal), state licenses, legal counsel"
            )
            
            pos_system = st.number_input(
                "POS System & Technology",
                min_value=0,
                value=8000,
                step=1000,
                help="Point of sale, draft system, inventory management software"
            )
        
        with col2:
            initial_inventory = st.number_input(
                "Initial Inventory (Malt, Hops, Yeast, etc.)",
                min_value=0,
                value=15000,
                step=2500,
                help="Ingredients for first batches, ~$1/pint production cost"
            )
            
            kegs_cans = st.number_input(
                "Kegs, Canning/Bottling Equipment",
                min_value=0,
                value=30000,
                step=5000,
                help="Kegs ($100-150 each), canning line or bottling equipment"
            )
            
            taproom_setup = st.number_input(
                "Taproom Furniture & Bar Equipment",
                min_value=0,
                value=35000,
                step=5000,
                help="Bar setup, draft system, glassware, seating, decor"
            )
            
            contingency = st.number_input(
                "Contingency Fund (10-20% recommended)",
                min_value=0,
                value=40000,
                step=5000,
                help="Buffer for unexpected expenses, delays, cost overruns"
            )
        
        total_startup = (st.session_state.equipment_cost + facility_buildout + 
                        licensing_fees + initial_inventory + kegs_cans + 
                        taproom_setup + pos_system + contingency)
        
        st.session_state.initial_capital = total_startup
        
        st.success(f"### Total Initial Capital Required: ${total_startup:,.0f}")
        
        # Equipment size guidance
        st.info("""
        **Brewery Size Guidance (First Year):**
        - **Nano (1-3 BBL)**: $100K-$200K equipment | 50-150 BBL/year production
        - **Micro (7-10 BBL)**: $150K-$300K equipment | 300-800 BBL/year production  
        - **Small (15-30 BBL)**: $300K-$600K equipment | 1,000-3,000 BBL/year production
        
        *1 BBL (barrel) = 31 gallons = 248 pints*
        
        **Taproom Rule of Thumb**: 1,000-1,500 pints per seat per year capacity
        """)
    
    with tab2:
        st.subheader("Fixed Monthly Operating Expenses")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.monthly_rent = st.number_input(
                "Facility Rent/Lease",
                min_value=0,
                value=st.session_state.monthly_rent,
                step=500,
                help="Varies by location and size. Typical: $3,000-$8,000/month"
            )
            
            st.session_state.monthly_payroll = st.number_input(
                "Monthly Payroll (All Staff)",
                min_value=0,
                value=st.session_state.monthly_payroll,
                step=1000,
                help="Head Brewer ($40K-$70K), Assistants, Taproom staff ($30K-$50K each)"
            )
            
            st.session_state.monthly_insurance = st.number_input(
                "Insurance (Liability, Property, Workers Comp)",
                min_value=0,
                value=st.session_state.monthly_insurance,
                step=100,
                help="General liability, product liability, property insurance"
            )
        
        with col2:
            st.session_state.monthly_utilities = st.number_input(
                "Utilities (Electric, Water, Gas, Sewer)",
                min_value=0,
                value=st.session_state.monthly_utilities,
                step=100,
                help="Brewing uses significant water and energy. Typical: $2,000-$4,000/month"
            )
            
            st.session_state.monthly_marketing = st.number_input(
                "Marketing & Advertising",
                min_value=0,
                value=st.session_state.monthly_marketing,
                step=500,
                help="Social media, events, merchandise, local advertising"
            )
            
            monthly_other = st.number_input(
                "Other Fixed Expenses (Accounting, Maintenance, etc.)",
                min_value=0,
                value=2000,
                step=100,
                help="Accounting, legal, software subscriptions, routine maintenance"
            )
        
        total_monthly_fixed = (st.session_state.monthly_rent + st.session_state.monthly_payroll + 
                              st.session_state.monthly_insurance + st.session_state.monthly_utilities + 
                              st.session_state.monthly_marketing + monthly_other)
        
        st.warning(f"### Total Monthly Fixed Expenses: ${total_monthly_fixed:,.0f}")
        st.caption(f"Annual Fixed Overhead: ${total_monthly_fixed * 12:,.0f}")
        
        st.info("""
        **Labor Cost Breakdown (Typical Micro Brewery):**
        - Head Brewer/Brewmaster: $40,000-$100,000/year
        - Assistant Brewer(s): $30,000-$50,000/year each
        - Taproom Manager: $35,000-$50,000/year
        - Taproom Staff (2-4): $25,000-$35,000/year each
        - Part-time/Seasonal help as needed
        """)

# ==================== REVENUE PROJECTIONS PAGE ====================
elif page == "Revenue Projections":
    st.header("📈 Revenue Projections & Product Mix")
    
    st.info("""
    **Brewery Revenue Model**: Unlike distilleries, breweries have faster production cycles (2-4 weeks) 
    allowing for quicker revenue generation and more responsive production to customer preferences.
    """)
    
    tab1, tab2, tab3 = st.tabs(["Beer Pricing", "Sales Volume", "Revenue Forecast"])
    
    with tab1:
        st.subheader("Beer Portfolio & Pricing Strategy")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Taproom (Direct Sales)")
            pint_price = st.number_input("Pint Price (16 oz)", min_value=0.0, value=7.0, step=0.25,
                                        help="Typical range: $6-$9 depending on style")
            flight_price = st.number_input("Flight Price (4x 5oz samples)", min_value=0.0, value=12.0, step=0.50)
            growler_price = st.number_input("Growler Fill (64 oz)", min_value=0.0, value=16.0, step=1.0)
            
            # Calculate costs
            pint_cogs = st.slider("Cost per Pint (COGS)", 0.50, 3.00, 1.00, 0.10,
                                 help="Ingredients + packaging for one pint")
            
            pint_margin = ((pint_price - pint_cogs) / pint_price) * 100
            st.metric("Pint Gross Margin", f"{pint_margin:.1f}%",
                     help=f"Price: ${pint_price} | COGS: ${pint_cogs}")
        
        with col2:
            st.markdown("#### Wholesale/Distribution")
            keg_price = st.number_input("Keg Price (1/2 BBL, 15.5 gal)", min_value=0.0, value=200.0, step=10.0,
                                       help="Price to distributor or direct to accounts. Typical: $150-$250")
            case_price = st.number_input("Case Price (4-pack x 6 = 24 cans)", min_value=0.0, value=32.0, step=2.0,
                                        help="Wholesale case price to distributor")
            
            keg_cogs = st.slider("Cost per Keg (COGS)", 20.0, 80.0, 40.0, 5.0,
                                help="Ingredients + keg for 1/2 barrel")
            
            keg_margin = ((keg_price - keg_cogs) / keg_price) * 100
            st.metric("Keg Gross Margin", f"{keg_margin:.1f}%",
                     help=f"Price: ${keg_price} | COGS: ${keg_cogs}")
            
            st.caption("Note: 1 keg = 124 pints | Taproom pint more profitable than wholesale")
        
        st.markdown("---")
        
        # Additional revenue streams
        col1, col2, col3 = st.columns(3)
        with col1:
            tour_price = st.number_input("Brewery Tour Price", min_value=0.0, value=15.0, step=5.0)
        with col2:
            merch_avg = st.number_input("Avg Merch Sale", min_value=0.0, value=25.0, step=5.0,
                                       help="T-shirts, glassware, etc.")
        with col3:
            food_enabled = st.checkbox("Include Food Sales", value=False,
                                      help="Check if running gastropub model")
    
    with tab2:
        st.subheader("Monthly Sales Volume Projections")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Taproom Sales (Per Month)")
            monthly_pints = st.number_input("Pints Sold", min_value=0, value=3000, step=100,
                                           help="Typical small taproom: 2,000-5,000 pints/month")
            monthly_flights = st.number_input("Flights Sold", min_value=0, value=200, step=10)
            monthly_growlers = st.number_input("Growler Fills", min_value=0, value=150, step=10)
            monthly_tours = st.number_input("Tour Participants", min_value=0, value=100, step=10)
            monthly_merch = st.number_input("Merchandise Transactions", min_value=0, value=50, step=5)
        
        with col2:
            st.markdown("#### Wholesale Distribution (Per Month)")
            monthly_kegs = st.number_input("Kegs Sold", min_value=0, value=30, step=5,
                                          help="Typical start: 20-50 kegs/month to local accounts")
            monthly_cases = st.number_input("Cases Sold (24-count)", min_value=0, value=100, step=10,
                                           help="For canned/bottled distribution")
            
            if food_enabled:
                monthly_food = st.number_input("Monthly Food Sales", min_value=0, value=8000, step=500,
                                             help="If operating as gastropub")
            else:
                monthly_food = 0
        
        # Calculate monthly revenue
        taproom_revenue = (monthly_pints * pint_price + 
                          monthly_flights * flight_price +
                          monthly_growlers * growler_price +
                          monthly_tours * tour_price +
                          monthly_merch * merch_avg)
        
        wholesale_revenue = (monthly_kegs * keg_price + monthly_cases * case_price)
        
        total_monthly_revenue = taproom_revenue + wholesale_revenue + monthly_food
        
        st.success(f"### Projected Monthly Revenue: ${total_monthly_revenue:,.0f}")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Taproom Revenue", f"${taproom_revenue:,.0f}", 
                   f"{(taproom_revenue/total_monthly_revenue*100):.1f}%")
        col2.metric("Wholesale Revenue", f"${wholesale_revenue:,.0f}",
                   f"{(wholesale_revenue/total_monthly_revenue*100):.1f}%")
        if food_enabled:
            col3.metric("Food Revenue", f"${monthly_food:,.0f}",
                       f"{(monthly_food/total_monthly_revenue*100):.1f}%")
        col4.metric("Annual Projection", f"${total_monthly_revenue * 12:,.0f}")
        
        # Production capacity check
        total_bbls_needed = (monthly_pints / 248 + monthly_flights * 4 * 5 / 128 + 
                            monthly_growlers * 64 / 128 + monthly_kegs * 15.5 + monthly_cases * 0.75)
        
        st.info(f"""
        **Production Requirements**: ~{total_bbls_needed:.0f} barrels/month ({total_bbls_needed * 12:.0f} BBL/year)
        
        This volume requires approximately:
        - 7-BBL system: {total_bbls_needed/7:.1f} brews per month (brewing ~{total_bbls_needed/7/4:.1f}x per week)
        - 10-BBL system: {total_bbls_needed/10:.1f} brews per month
        - 15-BBL system: {total_bbls_needed/15:.1f} brews per month
        """)
    
    with tab3:
        st.subheader("12-Month Revenue Forecast")
        
        # Growth assumptions
        monthly_growth = st.slider("Month-over-Month Growth Rate %", 0.0, 15.0, 3.0, 0.5,
                                   help="Typical: 2-5% per month as brand grows")
        
        # Generate 12-month forecast
        months = []
        revenues = []
        taproom_revenues = []
        wholesale_revenues = []
        base_revenue = total_monthly_revenue
        base_taproom = taproom_revenue
        base_wholesale = wholesale_revenue
        
        for month in range(1, 13):
            month_revenue = base_revenue * ((1 + monthly_growth/100) ** (month - 1))
            month_taproom = base_taproom * ((1 + monthly_growth/100) ** (month - 1))
            month_wholesale = base_wholesale * ((1 + monthly_growth/100) ** (month - 1))
            
            months.append(f"Month {month}")
            revenues.append(month_revenue)
            taproom_revenues.append(month_taproom)
            wholesale_revenues.append(month_wholesale)
        
        # Create dataframe
        forecast_df = pd.DataFrame({
            'Month': months,
            'Taproom': taproom_revenues,
            'Wholesale': wholesale_revenues,
            'Total Revenue': revenues
        })
        
        # Stacked bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Taproom Sales',
            x=forecast_df['Month'],
            y=forecast_df['Taproom'],
            marker_color='gold'
        ))
        
        fig.add_trace(go.Bar(
            name='Wholesale Distribution',
            x=forecast_df['Month'],
            y=forecast_df['Wholesale'],
            marker_color='lightseagreen'
        ))
        
        fig.update_layout(
            title="12-Month Revenue Projection by Channel",
            xaxis_title="Month",
            yaxis_title="Revenue ($)",
            barmode='stack',
            height=500,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary metrics
        total_year1_revenue = forecast_df['Total Revenue'].sum()
        avg_monthly_revenue = forecast_df['Total Revenue'].mean()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Year 1 Total Revenue", f"${total_year1_revenue:,.0f}")
        col2.metric("Average Monthly Revenue", f"${avg_monthly_revenue:,.0f}")
        col3.metric("Month 12 Revenue", f"${revenues[-1]:,.0f}")

# ==================== EXPENSE ANALYSIS PAGE ====================
elif page == "Expense Analysis":
    st.header("💸 Comprehensive Expense Analysis")
    
    # Calculate totals from inputs
    total_monthly_fixed = (st.session_state.monthly_rent + st.session_state.monthly_payroll + 
                          st.session_state.monthly_insurance + st.session_state.monthly_utilities + 
                          st.session_state.monthly_marketing + 2000)
    
    tab1, tab2, tab3 = st.tabs(["Fixed Expenses", "Variable Expenses", "Total Cost Structure"])
    
    with tab1:
        st.subheader("Monthly Fixed Operating Expenses Breakdown")
        
        # Create breakdown dataframe
        fixed_expenses = pd.DataFrame({
            'Expense Category': ['Rent/Lease', 'Payroll', 'Insurance', 'Utilities', 
                                'Marketing', 'Other (Accounting, etc.)'],
            'Monthly Cost': [st.session_state.monthly_rent, st.session_state.monthly_payroll,
                           st.session_state.monthly_insurance, st.session_state.monthly_utilities,
                           st.session_state.monthly_marketing, 2000],
            'Annual Cost': [st.session_state.monthly_rent * 12, st.session_state.monthly_payroll * 12,
                          st.session_state.monthly_insurance * 12, st.session_state.monthly_utilities * 12,
                          st.session_state.monthly_marketing * 12, 24000]
        })
        
        # Display table
        st.dataframe(fixed_expenses, use_container_width=True, hide_index=True)
        
        # Pie chart
        fig = px.pie(fixed_expenses, values='Monthly Cost', names='Expense Category',
                    title='Fixed Expense Distribution',
                    color_discrete_sequence=px.colors.sequential.YlOrBr)
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        col1.metric("Total Monthly Fixed Expenses", f"${total_monthly_fixed:,.0f}")
        col2.metric("Total Annual Fixed Expenses", f"${total_monthly_fixed * 12:,.0f}")
    
    with tab2:
        st.subheader("Variable Expenses (Scale with Production)")
        
        st.markdown("""
        Variable costs change with your sales volume:
        - **Ingredients** (malt, hops, yeast, water)
        - **Packaging** (cans, bottles, labels, boxes, kegs)
        - **Federal Excise Tax** ($3.50/barrel for first 60K BBL, then $18/BBL)
        - **Distribution** (if using 3rd party)
        - **Credit Card Fees** (taproom sales)
        """)
        
        # User inputs for variable costs
        col1, col2 = st.columns(2)
        
        with col1:
            ingredients_per_bbl = st.slider("Ingredients Cost per Barrel", 50, 150, 80,
                                           help="Malt, hops, yeast. Typical: $60-$100/BBL")
            packaging_per_unit = st.slider("Packaging Cost per Unit", 0.20, 2.00, 0.60, 0.10,
                                          help="Cans, labels, boxes. Typical: $0.40-$0.80/unit")
        
        with col2:
            cc_fee_pct = st.slider("Credit Card Processing %", 2.0, 4.0, 2.8, 0.1,
                                  help="Taproom card transactions")
            distribution_pct = st.slider("Distribution Cost % (if applicable)", 0, 30, 20,
                                        help="3rd party distributor margin. 0 if self-distributing")
        
        # Calculate as percentage of revenue (simplified)
        # Assuming 100 BBL/month at avg $200/BBL revenue = $20K
        example_revenue = 50000
        example_bbls = 100
        
        var_ingredients = example_bbls * ingredients_per_bbl
        var_packaging = 500 * packaging_per_unit * 31  # 500 pints equivalent
        var_excise = example_bbls * 3.50  # Federal excise tax
        var_cc = example_revenue * 0.30 * (cc_fee_pct / 100)  # 30% of revenue through cards
        var_distribution = example_revenue * 0.40 * (distribution_pct / 100)  # 40% through distribution
        
        total_variable = var_ingredients + var_packaging + var_excise + var_cc + var_distribution
        variable_pct = (total_variable / example_revenue) * 100
        
        st.info(f"""
        **Estimated Variable Costs**: {variable_pct:.1f}% of Revenue
        
        On ${example_revenue:,.0f} monthly revenue (~{example_bbls} BBL):
        - Ingredients: ${var_ingredients:,.0f}
        - Packaging: ${var_packaging:,.0f}
        - Federal Excise Tax: ${var_excise:,.0f}
        - Credit Card Fees: ${var_cc:,.0f}
        - Distribution: ${var_distribution:,.0f}
        - **Total Variable**: ${total_variable:,.0f}
        
        Industry Benchmark: 20-30% of revenue for variable costs
        """)
    
    with tab3:
        st.subheader("Total Cost Structure & Profitability Analysis")
        
        # Revenue input for analysis
        analysis_revenue = st.number_input(
            "Enter Monthly Revenue for Analysis",
            min_value=0,
            value=50000,
            step=1000,
            help="Use revenue projection from previous page"
        )
        
        # Calculate costs
        variable_costs = analysis_revenue * (variable_pct / 100)
        total_costs = total_monthly_fixed + variable_costs
        gross_profit = analysis_revenue - total_costs
        gross_margin_pct = (gross_profit / analysis_revenue * 100) if analysis_revenue > 0 else 0
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Revenue", f"${analysis_revenue:,.0f}")
        col2.metric("Variable Costs", f"${variable_costs:,.0f}", f"{variable_pct:.1f}%")
        col3.metric("Fixed Costs", f"${total_monthly_fixed:,.0f}")
        col4.metric("Net Profit", f"${gross_profit:,.0f}", f"{gross_margin_pct:.1f}%",
                   delta_color="normal" if gross_profit > 0 else "inverse")
        
        # Waterfall chart
        fig = go.Figure(go.Waterfall(
            name="Cost Structure",
            orientation="v",
            measure=["relative", "relative", "relative", "total"],
            x=["Revenue", "Variable Costs", "Fixed Costs", "Net Profit"],
            y=[analysis_revenue, -variable_costs, -total_monthly_fixed, gross_profit],
            text=[f"${analysis_revenue:,.0f}", f"-${variable_costs:,.0f}", 
                 f"-${total_monthly_fixed:,.0f}", f"${gross_profit:,.0f}"],
            textposition="outside",
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))
        
        fig.update_layout(
            title="Monthly Profit & Loss Waterfall",
            showlegend=False,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Breakeven analysis
        breakeven_revenue = total_monthly_fixed / (1 - (variable_pct / 100))
        breakeven_pints = breakeven_revenue / 7  # Assuming $7/pint average
        
        st.warning(f"""
        ### Breakeven Analysis
        - **Monthly Breakeven Revenue**: ${breakeven_revenue:,.0f}
        - **Breakeven in Pints**: {breakeven_pints:,.0f} pints/month (~{breakeven_pints/30:.0f}/day)
        - **Annual Breakeven Revenue**: ${breakeven_revenue * 12:,.0f}
        - Current revenue is {((analysis_revenue / breakeven_revenue - 1) * 100):.1f}% {'above' if analysis_revenue > breakeven_revenue else 'below'} breakeven
        
        **Industry Benchmark**: Most breweries become profitable within 18-36 months
        """)
        
        # Profitability tips
        with st.expander("💡 Tips to Improve Profitability"):
            st.markdown("""
            **Increase Margins:**
            1. **Maximize Taproom Sales** - Higher margins than wholesale (50%+ vs 20-30%)
            2. **Self-Distribute Initially** - Keep distributor margin (25-35%)
            3. **Premium Pricing for Unique Beers** - Specialty/limited releases
            4. **Merchandise Sales** - T-shirts, glassware (70%+ margins)
            5. **Brewery Tours & Events** - High-margin experiential revenue
            
            **Reduce Costs:**
            1. **Negotiate Bulk Ingredient Contracts** - Annual commitments
            2. **Improve Production Efficiency** - Reduce waste, optimize recipes
            3. **Energy Efficiency** - LED lighting, heat recovery systems
            4. **Smart Staffing** - Cross-train employees, optimize scheduling
            5. **DIY Marketing** - Social media, grassroots community building
            """)

# ==================== INVESTOR ANALYSIS PAGE ====================
elif page == "Investor Analysis":
    st.header("👥 Three-Investor Partnership Analysis")
    
    st.info("""
    **Key Performance Indicators for Investors:**
    1. Initial Capital Contribution per Partner
    2. Time to Positive Cashflow
    3. Return on Investment (ROI)
    4. Monthly Profit Distribution
    """)
    
    tab1, tab2, tab3 = st.tabs(["Capital Requirements", "Cashflow Projections", "ROI Analysis"])
    
    with tab1:
        st.subheader("Initial Capital Investment (3 Partners)")
        
        total_startup = st.session_state.initial_capital
        
        # Equal vs unequal split
        investment_split = st.radio(
            "Investment Structure",
            ["Equal Split (33.3% each)", "Custom Split"]
        )
        
        if investment_split == "Equal Split (33.3% each)":
            partner_1_pct = 33.33
            partner_2_pct = 33.33
            partner_3_pct = 33.34
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                partner_1_pct = st.number_input("Partner 1 Ownership %", 0.0, 100.0, 33.33, 0.01)
            with col2:
                partner_2_pct = st.number_input("Partner 2 Ownership %", 0.0, 100.0, 33.33, 0.01)
            with col3:
                partner_3_pct = st.number_input("Partner 3 Ownership %", 0.0, 100.0, 33.34, 0.01)
            
            if abs((partner_1_pct + partner_2_pct + partner_3_pct) - 100) > 0.01:
                st.error("⚠️ Ownership percentages must sum to 100%")
        
        # Calculate contributions
        partner_1_investment = total_startup * (partner_1_pct / 100)
        partner_2_investment = total_startup * (partner_2_pct / 100)
        partner_3_investment = total_startup * (partner_3_pct / 100)
        
        # Display investment summary
        investment_df = pd.DataFrame({
            'Partner': ['Partner 1', 'Partner 2', 'Partner 3', 'TOTAL'],
            'Ownership %': [f"{partner_1_pct:.2f}%", f"{partner_2_pct:.2f}%", 
                           f"{partner_3_pct:.2f}%", "100.00%"],
            'Initial Investment': [f"${partner_1_investment:,.0f}", f"${partner_2_investment:,.0f}",
                                  f"${partner_3_investment:,.0f}", f"${total_startup:,.0f}"]
        })
        
        st.table(investment_df)
        
        st.success(f"**Total Initial Capital**: ${total_startup:,.0f}")
        
        # Additional funding discussion
        with st.expander("💡 Funding Options & Considerations"):
            st.markdown("""
            **Financing Options for Micro Breweries:**
            
            1. **Personal Investment & Friends/Family**
               - Simplest, maintains control
               - Limited by personal resources
            
            2. **Small Business Loans (SBA 7(a) & 504)**
               - Up to $5 million available
               - Equipment can serve as collateral
               - Requires strong credit and business plan
            
            3. **Equipment Financing**
               - Leasing or financing brewing equipment
               - Preserves working capital
               - Terms: 5-7 years typically
            
            4. **Crowdfunding (Regulation CF or Debt)**
               - Build customer base while raising funds
               - Platforms: StartEngine, Wefunder, Mainvest
               - Can raise up to $5M/year
            
            5. **Local Grants & Economic Development**
               - Check Charlotte-Concord economic development programs
               - Some cities offer brewery-specific incentives
               - Tourism/downtown revitalization grants
            
            6. **Angel Investors / VC**
               - For scalable, high-growth concepts
               - May require giving up equity
               - Look for food/beverage industry experience
            
            **Tip**: Many successful breweries use a mix of personal investment (50%), 
            equipment financing (30%), and SBA loans (20%)
            """)
    
    with tab2:
        st.subheader("36-Month Cashflow Projection")
        
        # Inputs for cashflow modeling
        col1, col2 = st.columns(2)
        
        with col1:
            starting_monthly_revenue = st.number_input(
                "Starting Monthly Revenue (Month 1)",
                min_value=0,
                value=35000,
                step=1000,
                help="Conservative estimate - taproom + initial accounts"
            )
            
            monthly_revenue_growth = st.slider(
                "Average Monthly Revenue Growth %",
                0.0, 15.0, 4.0, 0.5,
                help="Typical: 3-5% per month Year 1, slowing to 2-3% Year 2-3"
            )
        
        with col2:
            profit_distribution_pct = st.slider(
                "% of Profit Distributed to Partners",
                0, 100, 70, 5,
                help="Remaining % retained for growth, equipment, inventory"
            )
        
        # Calculate 36-month cashflow
        total_monthly_fixed = (st.session_state.monthly_rent + st.session_state.monthly_payroll + 
                              st.session_state.monthly_insurance + st.session_state.monthly_utilities + 
                              st.session_state.monthly_marketing + 2000)
        
        months_list = []
        revenue_list = []
        expenses_list = []
        profit_list = []
        cumulative_cashflow = []
        
        cumulative = -total_startup  # Start with negative initial investment
        
        for month in range(1, 37):
            # Revenue with growth (declining growth rate over time)
            if month <= 12:
                growth_rate = monthly_revenue_growth / 100
            elif month <= 24:
                growth_rate = (monthly_revenue_growth * 0.6) / 100
            else:
                growth_rate = (monthly_revenue_growth * 0.4) / 100
            
            revenue = starting_monthly_revenue * ((1 + growth_rate) ** (month - 1))
            
            # Expenses (variable costs approximately 25% of revenue)
            variable_costs = revenue * 0.25
            total_expenses = total_monthly_fixed + variable_costs
            
            # Profit
            monthly_profit = revenue - total_expenses
            
            # Cumulative cashflow
            cumulative += monthly_profit
            
            months_list.append(month)
            revenue_list.append(revenue)
            expenses_list.append(total_expenses)
            profit_list.append(monthly_profit)
            cumulative_cashflow.append(cumulative)
        
        # Create dataframe
        cashflow_df = pd.DataFrame({
            'Month': months_list,
            'Revenue': revenue_list,
            'Expenses': expenses_list,
            'Profit': profit_list,
            'Cumulative Cashflow': cumulative_cashflow
        })
        
        # Find breakeven month
        breakeven_month = None
        for idx, cf in enumerate(cumulative_cashflow):
            if cf >= 0:
                breakeven_month = idx + 1
                break
        
        # Plot cumulative cashflow
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=cashflow_df['Month'],
            y=cashflow_df['Cumulative Cashflow'],
            mode='lines',
            name='Cumulative Cashflow',
            line=dict(color='darkgoldenrod', width=3),
            fill='tozeroy',
            fillcolor='rgba(218, 165, 32, 0.3)'
        ))
        
        # Add breakeven line
        fig.add_hline(y=0, line_dash="dash", line_color="red", 
                     annotation_text="Breakeven", annotation_position="right")
        
        if breakeven_month:
            fig.add_annotation(
                x=breakeven_month,
                y=0,
                text=f"Breakeven: Month {breakeven_month}",
                showarrow=True,
                arrowhead=2,
                ax=40,
                ay=-40
            )
        
        fig.update_layout(
            title="36-Month Cumulative Cashflow Projection",
            xaxis_title="Month",
            yaxis_title="Cumulative Cashflow ($)",
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Key metrics
        year1_profit = sum(profit_list[:12])
        year2_profit = sum(profit_list[12:24])
        year3_profit = sum(profit_list[24:36])
        
        col1, col2, col3, col4 = st.columns(4)
        
        if breakeven_month:
            col1.metric("Breakeven Month", f"Month {breakeven_month}",
                       help="When cumulative cashflow becomes positive")
        else:
            col1.metric("Breakeven Month", "After Month 36",
                       help="Cumulative cashflow still negative after 36 months")
        
        col2.metric("Year 1 Net Profit", f"${year1_profit:,.0f}")
        col3.metric("Year 2 Net Profit", f"${year2_profit:,.0f}")
        col4.metric("Year 3 Net Profit", f"${year3_profit:,.0f}")
        
        # Monthly distribution to partners
        if year1_profit > 0:
            monthly_avg_profit_yr1 = year1_profit / 12
            distributable = monthly_avg_profit_yr1 * (profit_distribution_pct / 100)
            partner_1_monthly = distributable * (partner_1_pct / 100)
            
            st.info(f"""
            **Average Monthly Distribution (Year 1)**:
            - Total Distributable Profit: ${distributable:,.0f}
            - Partner 1 ({partner_1_pct:.2f}%): ${partner_1_monthly:,.0f}/month
            - Partner 2 ({partner_2_pct:.2f}%): ${distributable * (partner_2_pct / 100):,.0f}/month
            - Partner 3 ({partner_3_pct:.2f}%): ${distributable * (partner_3_pct / 100):,.0f}/month
            
            *Note: Most owners work for reduced/no salary in Year 1-2 and reinvest profits*
            """)
    
    with tab3:
        st.subheader("Return on Investment (ROI) Analysis")
        
        # Calculate 3-year totals
        total_3yr_profit = sum(profit_list)
        total_3yr_distributed = total_3yr_profit * (profit_distribution_pct / 100)
        
        # Per partner ROI
        partner_1_total_dist = total_3yr_distributed * (partner_1_pct / 100)
        partner_2_total_dist = total_3yr_distributed * (partner_2_pct / 100)
        partner_3_total_dist = total_3yr_distributed * (partner_3_pct / 100)
        
        partner_1_roi = ((partner_1_total_dist / partner_1_investment - 1) * 100) if partner_1_investment > 0 else 0
        partner_2_roi = ((partner_2_total_dist / partner_2_investment - 1) * 100) if partner_2_investment > 0 else 0
        partner_3_roi = ((partner_3_total_dist / partner_3_investment - 1) * 100) if partner_3_investment > 0 else 0
        
        # Business valuation (revenue multiple for craft breweries)
        final_year_revenue = sum(revenue_list[24:36])
        estimated_valuation = final_year_revenue * 2.0  # Conservative 2x annual revenue
        
        # Display ROI summary
        roi_df = pd.DataFrame({
            'Partner': ['Partner 1', 'Partner 2', 'Partner 3'],
            'Initial Investment': [f"${partner_1_investment:,.0f}", f"${partner_2_investment:,.0f}",
                                  f"${partner_3_investment:,.0f}"],
            '3-Year Cash Distributions': [f"${partner_1_total_dist:,.0f}", f"${partner_2_total_dist:,.0f}",
                                          f"${partner_3_total_dist:,.0f}"],
            'Ownership Value (Estimated)': [f"${estimated_valuation * (partner_1_pct/100):,.0f}",
                                           f"${estimated_valuation * (partner_2_pct/100):,.0f}",
                                           f"${estimated_valuation * (partner_3_pct/100):,.0f}"],
            'Cash ROI (3yr)': [f"{partner_1_roi:.1f}%", f"{partner_2_roi:.1f}%", f"{partner_3_roi:.1f}%"]
        })
        
        st.table(roi_df)
        
        # Visualize ROI
        fig = go.Figure()
        
        partners = ['Partner 1', 'Partner 2', 'Partner 3']
        investments = [partner_1_investment, partner_2_investment, partner_3_investment]
        returns = [partner_1_total_dist, partner_2_total_dist, partner_3_total_dist]
        equity_value = [estimated_valuation * (partner_1_pct/100),
                       estimated_valuation * (partner_2_pct/100),
                       estimated_valuation * (partner_3_pct/100)]
        
        fig.add_trace(go.Bar(
            name='Initial Investment',
            x=partners,
            y=investments,
            marker_color='indianred'
        ))
        
        fig.add_trace(go.Bar(
            name='3-Year Cash Returns',
            x=partners,
            y=returns,
            marker_color='gold'
        ))
        
        fig.add_trace(go.Bar(
            name='Equity Value (Est.)',
            x=partners,
            y=equity_value,
            marker_color='lightseagreen'
        ))
        
        fig.update_layout(
            title="Investment, Returns & Equity Value (3 Years)",
            xaxis_title="Partner",
            yaxis_title="Amount ($)",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("3-Year Total Profit", f"${total_3yr_profit:,.0f}")
        col2.metric("Estimated Business Value", f"${estimated_valuation:,.0f}",
                   help="Based on 2x Year 3 annual revenue (conservative for profitable breweries)")
        col3.metric("Average Annual ROI", f"{(partner_1_roi / 3):.1f}%",
                   help="Cash return only, not including equity value")
        
        # Comparison to other investments
        with st.expander("📊 ROI Comparison to Other Investments"):
            st.markdown(f"""
            **3-Year ROI Comparison:**
            - **Your Brewery**: {partner_1_roi:.1f}% cash + equity value
            - **S&P 500 (historical avg)**: ~30% (10% annually)
            - **Small Business Average**: 20-40% (varies widely)
            - **Real Estate**: 15-30% (depending on market)
            
            **Key Differences:**
            - Brewery requires active involvement (not passive)
            - Higher risk, potentially higher reward
            - Building a business asset with ongoing value
            - Personal fulfillment & community impact
            - Less liquid than stocks (harder to sell quickly)
            
            **Note**: Most brewery owners view first 2-3 years as "building phase" 
            with full ROI potential realized in years 4-7 as business matures.
            """)
        
        # Risk considerations
        with st.expander("⚠️ Risk Factors & Mitigation"):
            st.markdown("""
            **Key Risks for Micro Brewery Ventures:**
            
            1. **Market Competition**
               - 30+ existing breweries in Charlotte metro
               - **Mitigation**: Unique beer styles, strong brand identity, niche focus
            
            2. **Operating Complexity**
               - Brewing requires technical skill
               - Quality control critical
               - **Mitigation**: Hire experienced brewmaster, invest in training, QC processes
            
            3. **Capital Intensity**
               - High upfront equipment costs
               - Working capital needs (ingredients, payroll)
               - **Mitigation**: Phased growth, equipment financing, maintain reserves
            
            4. **Regulatory Requirements**
               - Federal (TTB) and state licensing
               - Ongoing compliance and reporting
               - **Mitigation**: Work with experienced beverage attorney, maintain good records
            
            5. **Market Shifts**
               - Consumer preferences change
               - Economic downturns affect discretionary spending
               - **Mitigation**: Diversify beer styles, build loyal community, maintain quality
            
            6. **Distribution Challenges**
               - Getting tap handles in crowded market
               - Distributor relationships
               - **Mitigation**: Focus on taproom first, self-distribute initially, build reputation
            
            **Success Factors:**
            - Strong business plan with realistic projections
            - Experienced brewing talent
            - Differentiated product offering
            - Community engagement and marketing
            - Financial discipline and contingency planning
            - Location with good foot traffic and visibility
            """)

# ==================== DASHBOARD PAGE ====================
elif page == "Dashboard":
    st.header("📊 Executive Dashboard")
    
    # Calculate key metrics
    total_monthly_fixed = (st.session_state.monthly_rent + st.session_state.monthly_payroll + 
                          st.session_state.monthly_insurance + st.session_state.monthly_utilities + 
                          st.session_state.monthly_marketing + 2000)
    
    # Top-level metrics
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric(
        "Initial Capital Required",
        f"${st.session_state.initial_capital:,.0f}",
        help="Total startup costs including equipment, build-out, inventory"
    )
    
    col2.metric(
        "Monthly Fixed Costs",
        f"${total_monthly_fixed:,.0f}",
        help="Fixed operating expenses that must be covered monthly"
    )
    
    col3.metric(
        "Breakeven Revenue",
        f"${(total_monthly_fixed / 0.75):,.0f}/mo",
        help="Monthly revenue needed to break even (assuming 25% variable costs)"
    )
    
    col4.metric(
        "Investment per Partner",
        f"${(st.session_state.initial_capital / 3):,.0f}",
        help="Equal split among 3 investors"
    )
    
    st.markdown("---")
    
    # Summary sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💼 Market Position")
        st.markdown("""
        **Charlotte-Concord Region Analysis:**
        - 30+ established craft breweries
        - Vibrant craft beer culture (since 2009)
        - Strong brewery tourism
        - Supportive craft beer community
        - Growing population base
        
        **Competitive Advantages:**
        - Unique beer styles and recipes
        - Strong taproom experience (highest margins)
        - Local community engagement
        - Quality and consistency
        - Strategic location selection
        
        **Market Opportunity:**
        - $26.8B US craft beer market
        - Charlotte designated as craft beer destination
        - Brewery-hopping culture well-established
        - Tourism and events drive taproom traffic
        """)
        
        st.subheader("🎯 Revenue Targets")
        target_monthly = 50000
        target_annual = target_monthly * 12
        
        st.markdown(f"""
        **Conservative Year 1 Targets:**
        - **Monthly Revenue**: ${target_monthly:,.0f}
        - **Annual Revenue**: ${target_annual:,.0f}
        - **Taproom Sales**: 60% (higher margin)
        - **Wholesale**: 40% (volume)
        
        **Production Targets:**
        - Year 1: 300-500 barrels
        - Year 2: 500-800 barrels
        - Year 3: 800-1,200 barrels
        
        **Industry Benchmarks:**
        - Small craft brewery: $1M-$3M annual revenue
        - Net profit margins: 20-25%
        - Gross margins: 74-92% (before expenses)
        - Breakeven timeline: 18-36 months typical
        """)
    
    with col2:
        st.subheader("💰 Financial Summary")
        
        # Create sample P&L
        sample_revenue = 50000
        sample_var_costs = sample_revenue * 0.25
        sample_profit = sample_revenue - sample_var_costs - total_monthly_fixed
        sample_margin = (sample_profit / sample_revenue * 100) if sample_revenue > 0 else 0
        
        pl_df = pd.DataFrame({
            'Item': ['Monthly Revenue', 'Variable Costs (25%)', 'Fixed Operating Costs', 
                    'Net Profit', 'Profit Margin %'],
            'Amount': [f"${sample_revenue:,.0f}", f"(${sample_var_costs:,.0f})", 
                      f"(${total_monthly_fixed:,.0f})", f"${sample_profit:,.0f}", 
                      f"{sample_margin:.1f}%"]
        })
        
        st.dataframe(pl_df, use_container_width=True, hide_index=True)
        
        st.subheader("📈 Growth Strategy")
        st.markdown("""
        **Phase 1 (Months 1-6): Launch & Build Foundation**
        - Focus on core beer lineup (4-6 styles)
        - Build taproom traffic and regulars
        - Establish quality and consistency
        - Begin self-distribution to select accounts
        - Target: Cover operating costs, build awareness
        
        **Phase 2 (Months 7-12): Scale & Refine**
        - Increase production by 30-50%
        - Expand distribution strategically
        - Launch seasonal and specialty releases
        - Build event calendar (tours, music, food trucks)
        - Target: Achieve positive cashflow
        
        **Phase 3 (Year 2): Expand & Optimize**
        - Consider equipment upgrades if at capacity
        - Expand wholesale accounts or add distributor
        - Develop barrel-aging program
        - Enhance merchandise and events
        - Target: 20%+ profit margins
        
        **Phase 4 (Year 3+): Mature & Grow**
        - Consider second location or expansion
        - Premium/limited release series
        - Regional distribution
        - Build brand equity for potential exit
        """)
    
    st.markdown("---")
    
    # Decision matrix
    st.subheader("✅ Investment Decision Matrix")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🟢 Strengths")
        st.markdown("""
        - Established market (30+ breweries = proven demand)
        - High gross margins (74-92%)
        - Multiple revenue streams (taproom, wholesale, events)
        - Faster production cycle than spirits (2-4 weeks)
        - Charlotte's craft beer tourism
        - Taproom = highest margin channel
        - Creative differentiation opportunities
        - Community-building potential
        """)
    
    with col2:
        st.markdown("### 🟡 Considerations")
        st.markdown("""
        - Competitive market (30+ breweries)
        - Requires brewing expertise
        - Labor-intensive operations
        - Working capital needs (ingredients, kegs)
        - Quality control critical
        - Location selection important
        - Regulatory compliance (TTB, state, local)
        - 18-36 month breakeven typical
        """)
    
    with col3:
        st.markdown("### 🔴 Risks")
        st.markdown("""
        - Market saturation potential
        - Changing consumer preferences
        - Distribution challenges
        - Equipment maintenance/failure
        - Staffing and retention
        - Economic sensitivity (discretionary spending)
        - Quality consistency issues
        - Cash flow management during growth
        """)
    
    st.markdown("---")
    
    # Next steps
    st.subheader("🚀 Recommended Next Steps")
    
    st.markdown("""
    ### Immediate Actions (Weeks 1-4)
    1. **Market Validation**
       - Visit 10+ Charlotte-Concord breweries for competitive analysis
       - Identify gaps in market (underserved styles, locations)
       - Talk to brewery owners about lessons learned
       - Survey potential customers on preferences
    
    2. **Team Building**
       - Identify and recruit experienced head brewer
       - Build advisory board with brewery operators
       - Connect with Charlotte brewing community
    
    3. **Financial Planning**
       - Finalize partnership agreement and ownership structure
       - Get pre-qualification from SBA lenders
       - Identify equipment financing options
       - Create detailed 5-year financial model
    
    ### Short Term (Months 2-4)
    4. **Business Planning**
       - Develop comprehensive business plan
       - Create beer lineup and recipes
       - Define brand identity and story
       - Outline marketing strategy
    
    5. **Location Scouting**
       - Identify 3-5 potential locations
       - Analyze foot traffic, accessibility, parking
       - Consider zoning and lease terms
       - Evaluate build-out requirements
    
    6. **Legal & Regulatory**
       - Hire beverage attorney (TTB experience)
       - Begin TTB Brewer's Notice application (4-6 months)
       - Research NC ABC requirements
       - Structure business entity (LLC, S-Corp, etc.)
    
    ### Medium Term (Months 5-8)
    7. **Equipment & Build-Out**
       - Get quotes from 3+ equipment vendors
       - Compare new vs. used equipment options
       - Design brewery layout and workflow
       - Plan taproom design and capacity
    
    8. **Financing**
       - Finalize investor agreements
       - Close on SBA loan (if applicable)
       - Arrange equipment financing
       - Establish business banking relationships
    
    9. **Operations Planning**
       - Develop production schedule
       - Create recipes and brewing procedures
       - Plan quality control processes
       - Design inventory management system
    
    ### Pre-Launch (Months 9-12)
    10. **Marketing & Brand**
        - Develop brand identity (logo, colors, story)
        - Create website and social media presence
        - Plan grand opening events
        - Build email list and community
    
    11. **Hiring & Training**
        - Hire initial team (2-4 people)
        - Train on brewing and taproom operations
        - Develop standard operating procedures
    
    12. **Soft Opening**
        - Friends & family events
        - Limited taproom hours
        - Test operations and refine
        - Build initial customer base
    """)
    
    # Export options
    st.markdown("---")
    st.subheader("📥 Export Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate PDF Report"):
            st.info("PDF export functionality coming soon! Contact support for custom reports.")
    with col2:
        if st.button("Download Financial Model (Excel)"):
            st.info("Excel export functionality coming soon! Use screenshots or contact support.")
    
    # Resources
    with st.expander("📚 Useful Resources"):
        st.markdown("""
        **Industry Organizations:**
        - Brewers Association: www.brewersassociation.org
        - North Carolina Craft Brewers Guild: ncbeer.org
        - American Brewers Guild (education): abgbrew.com
        
        **Regulatory:**
        - TTB (Federal): www.ttb.gov
        - NC ABC Commission: abc.nc.gov
        
        **Equipment Vendors:**
        - Research multiple vendors for quotes
        - Consider used equipment marketplaces
        - Attend brewery equipment expos
        
        **Software & Tools:**
        - Ekos Brewmaster (inventory/production)
        - Toast POS (taproom point of sale)
        - BeerMenus (online presence)
        - Untappd (customer engagement)
        
        **Education:**
        - Siebel Institute of Technology
        - American Brewers Guild
        - UC Davis Master Brewers Program
        - Local homebrewing clubs and workshops
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p><strong>Micro Brewery Financial Analyzer</strong></p>
    <p>Data sources: Brewers Association, Charlotte-Concord brewery market analysis, industry financial benchmarks</p>
    <p>⚠️ This tool provides estimates for planning purposes. Consult with legal, financial, and industry professionals before making investment decisions.</p>
    <p><em>Built for Charlotte-Concord Craft Beer Entrepreneurs</em> 🍺</p>
</div>
""", unsafe_allow_html=True)
