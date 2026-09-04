import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# V3.1 — DASHBOARD & VISUALIZATION
# Uses the cleaned dataset from app.py through Streamlit
# session_state.
# ============================================================

st.title("📊 V3.1 — Dashboard & Visualization")

st.markdown(
    """
    ### Organisation Data Processing System

    This dashboard uses the **cleaned dataset** produced in the
    main application (V1 & V2).
    """
)

# ============================================================
# VERSION PROGRESS
# ============================================================

with st.expander("📌 Project Version Progress", expanded=False):

    progress_data = pd.DataFrame(
        {
            "Version": [
                "V1",
                "V2",
                "V3.1",
                "V3.2",
                "V4",
                "V5",
                "V6",
                "V7",
                "V8",
            ],
            "Task": [
                "Data Upload & Cleaning",
                "Descriptive / Statistical Analysis",
                "Dashboard Foundation",
                "Advanced Visualization",
                "Department Analysis",
                "Data Extraction / Processing",
                "Authentication & User Management",
                "Final Testing",
                "GitHub & Deployment",
            ],
            "Status": [
                "✅ Complete",
                "✅ Complete",
                "🔄 Current",
                "⏳ Pending",
                "⏳ Pending",
                "⏳ Pending",
                "⏳ Pending",
                "⏳ Pending",
                "⏳ Pending",
            ],
        }
    )

    st.dataframe(
        progress_data,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# CHECK DATA FROM MAIN APP
# ============================================================

if (
    "working_df" not in st.session_state
    or st.session_state.working_df is None
    or st.session_state.working_df.empty
):

    st.warning(
        "⚠️ No cleaned dataset is currently available."
    )

    st.info(
        "Go back to the main application, upload your CSV/XLSX "
        "file and complete the V1 cleaning process first."
    )

    st.stop()


# Make a copy so the dashboard never modifies the original data
df = st.session_state.working_df.copy()


# ============================================================
# BASIC DATA INFORMATION
# ============================================================

numeric_columns = df.select_dtypes(
    include="number"
).columns.tolist()

categorical_columns = df.select_dtypes(
    exclude="number"
).columns.tolist()

total_rows = len(df)
total_columns = len(df.columns)

numeric_count = len(numeric_columns)
categorical_count = len(categorical_columns)

missing_count = int(df.isna().sum().sum())

duplicate_count = int(df.duplicated().sum())


# ============================================================
# DASHBOARD METRICS
# ============================================================

st.subheader("📌 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Observations",
        f"{total_rows:,}"
    )

with col2:
    st.metric(
        "Total Variables",
        f"{total_columns:,}"
    )

with col3:
    st.metric(
        "Numeric Variables",
        f"{numeric_count:,}"
    )

with col4:
    st.metric(
        "Categorical Variables",
        f"{categorical_count:,}"
    )


col5, col6, col7 = st.columns(3)

with col5:
    st.metric(
        "Missing Values",
        f"{missing_count:,}"
    )

with col6:
    st.metric(
        "Duplicate Rows",
        f"{duplicate_count:,}"
    )

with col7:

    if missing_count == 0 and duplicate_count == 0:
        st.metric(
            "Data Status",
            "READY ✅"
        )
    else:
        st.metric(
            "Data Status",
            "CHECK ⚠️"
        )


# ============================================================
# DATA QUALITY STATUS
# ============================================================

st.subheader("🔎 Data Quality Status")

if missing_count == 0 and duplicate_count == 0:

    st.success(
        "✅ The current dataset has no missing values "
        "and no duplicate rows."
    )

else:

    if missing_count > 0:
        st.warning(
            f"⚠️ The dataset contains {missing_count:,} missing values."
        )

    if duplicate_count > 0:
        st.warning(
            f"⚠️ The dataset contains {duplicate_count:,} duplicate rows."
        )


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "📋 Overview",
        "📈 Distributions",
        "📊 Categorical",
        "🔗 Correlation",
        "🚨 Outliers",
        "👀 Data Preview",
    ]
)


# ============================================================
# TAB 1 — OVERVIEW
# ============================================================

with tab1:

    st.subheader("📋 Numeric Variables Overview")

    if numeric_count == 0:

        st.info(
            "No numeric variables were found in the dataset."
        )

    else:

        numeric_summary = df[numeric_columns].describe().T

        numeric_summary = numeric_summary.rename(
            columns={
                "count": "Count",
                "mean": "Mean",
                "std": "Std. Deviation",
                "min": "Minimum",
                "25%": "Q1",
                "50%": "Median",
                "75%": "Q3",
                "max": "Maximum",
            }
        )

        st.dataframe(
            numeric_summary.round(3),
            use_container_width=True,
        )


    st.subheader("🔤 Categorical Variables Overview")

    if categorical_count == 0:

        st.info(
            "No categorical variables were found."
        )

    else:

        categorical_summary = []

        for column in categorical_columns:

            categorical_summary.append(
                {
                    "Variable": column,
                    "Unique Values": df[column].nunique(
                        dropna=True
                    ),
                    "Missing Values": int(
                        df[column].isna().sum()
                    ),
                }
            )

        categorical_summary_df = pd.DataFrame(
            categorical_summary
        )

        st.dataframe(
            categorical_summary_df,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# TAB 2 — NUMERIC DISTRIBUTIONS
# ============================================================

with tab2:

    st.subheader("📈 Numeric Variable Distribution")

    if numeric_count == 0:

        st.info(
            "No numeric variables are available for visualization."
        )

    else:

        selected_numeric = st.selectbox(
            "Select a numeric variable",
            numeric_columns,
            key="v31_numeric_distribution",
        )

        selected_data = df[selected_numeric].dropna()

        if selected_data.empty:

            st.warning(
                "The selected variable does not contain usable numeric data."
            )

        else:

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Mean",
                    f"{selected_data.mean():,.3f}"
                )

            with col2:
                st.metric(
                    "Median",
                    f"{selected_data.median():,.3f}"
                )

            with col3:
                st.metric(
                    "Standard Deviation",
                    f"{selected_data.std():,.3f}"
                )


            # -------------------------------
            # Histogram
            # -------------------------------

            st.markdown("### 📊 Histogram")

            fig, ax = plt.subplots(figsize=(10, 5))

            ax.hist(
                selected_data,
                bins=10,
                edgecolor="black",
            )

            ax.set_title(
                f"Distribution of {selected_numeric}"
            )

            ax.set_xlabel(selected_numeric)
            ax.set_ylabel("Frequency")

            ax.grid(axis="y", alpha=0.3)

            st.pyplot(fig)

            plt.close(fig)


            # -------------------------------
            # Box Plot
            # -------------------------------

            st.markdown("### 📦 Box Plot")

            fig, ax = plt.subplots(figsize=(10, 3))

            ax.boxplot(
                selected_data,
                vert=False,
            )

            ax.set_title(
                f"Box Plot of {selected_numeric}"
            )

            ax.set_xlabel(selected_numeric)

            ax.grid(axis="x", alpha=0.3)

            st.pyplot(fig)

            plt.close(fig)


# ============================================================
# TAB 3 — CATEGORICAL VARIABLES
# ============================================================

with tab3:

    st.subheader("📊 Categorical Variable Analysis")

    if categorical_count == 0:

        st.info(
            "No categorical variables are available."
        )

    else:

        selected_category = st.selectbox(
            "Select a categorical variable",
            categorical_columns,
            key="v31_category",
        )

        frequency = (
            df[selected_category]
            .fillna("Missing")
            .value_counts()
            .reset_index()
        )

        frequency.columns = [
            selected_category,
            "Frequency",
        ]

        frequency["Percentage"] = (
            frequency["Frequency"]
            / frequency["Frequency"].sum()
            * 100
        )

        st.dataframe(
            frequency.round(2),
            use_container_width=True,
            hide_index=True,
        )


        st.markdown("### 📊 Bar Chart")

        # Limit chart to top 15 categories
        chart_data = frequency.head(15)

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.bar(
            chart_data[selected_category].astype(str),
            chart_data["Frequency"],
        )

        ax.set_title(
            f"Distribution of {selected_category}"
        )

        ax.set_xlabel(selected_category)
        ax.set_ylabel("Frequency")

        plt.xticks(
            rotation=45,
            ha="right",
        )

        ax.grid(axis="y", alpha=0.3)

        plt.tight_layout()

        st.pyplot(fig)

        plt.close(fig)


# ============================================================
# TAB 4 — CORRELATION
# ============================================================

with tab4:

    st.subheader("🔗 Correlation Analysis")

    if numeric_count < 2:

        st.info(
            "At least two numeric variables are required "
            "for correlation analysis."
        )

    else:

        correlation_matrix = df[
            numeric_columns
        ].corr()

        st.markdown("### Pearson Correlation Matrix")

        st.dataframe(
            correlation_matrix.round(3),
            use_container_width=True,
        )


        st.markdown("### 🔥 Correlation Heatmap")

        fig, ax = plt.subplots(
            figsize=(
                max(8, numeric_count * 0.8),
                max(6, numeric_count * 0.7),
            )
        )

        image = ax.imshow(
            correlation_matrix,
            aspect="auto",
        )

        ax.set_xticks(
            range(len(correlation_matrix.columns))
        )

        ax.set_yticks(
            range(len(correlation_matrix.columns))
        )

        ax.set_xticklabels(
            correlation_matrix.columns,
            rotation=45,
            ha="right",
        )

        ax.set_yticklabels(
            correlation_matrix.columns
        )

        ax.set_title(
            "Pearson Correlation Heatmap"
        )

        # Display correlation values
        for i in range(
            len(correlation_matrix.columns)
        ):
            for j in range(
                len(correlation_matrix.columns)
            ):

                value = correlation_matrix.iloc[i, j]

                if pd.notna(value):

                    ax.text(
                        j,
                        i,
                        f"{value:.2f}",
                        ha="center",
                        va="center",
                    )

        fig.colorbar(
            image,
            ax=ax,
            label="Correlation",
        )

        plt.tight_layout()

        st.pyplot(fig)

        plt.close(fig)

# ============================================================
# V3.2.1 — SCATTER PLOT & VARIABLE COMPARISON
# ============================================================

st.divider()

st.subheader("🔵 V3.2.1 — Scatter Plot & Variable Comparison")

st.markdown(
    """
    Compare two numeric variables to visually examine their
    relationship using a scatter plot.
    """
)

if numeric_count < 2:

    st.info(
        "At least two numeric variables are required "
        "for variable comparison."
    )

else:

    col1, col2 = st.columns(2)

    with col1:

        x_variable = st.selectbox(
            "Select X-axis variable",
            numeric_columns,
            key="v321_x_variable",
        )

    with col2:

        y_options = [
            column
            for column in numeric_columns
            if column != x_variable
        ]

        y_variable = st.selectbox(
            "Select Y-axis variable",
            y_options,
            key="v321_y_variable",
        )


    # --------------------------------------------------------
    # PREPARE DATA
    # --------------------------------------------------------

    comparison_df = df[
        [x_variable, y_variable]
    ].dropna()


    if comparison_df.empty:

        st.warning(
            "There is no usable data for the selected variables."
        )

    else:

        # ----------------------------------------------------
        # CORRELATION
        # ----------------------------------------------------

        correlation = comparison_df[
            x_variable
        ].corr(
            comparison_df[y_variable]
        )


        # ----------------------------------------------------
        # CORRELATION INTERPRETATION
        # ----------------------------------------------------

        absolute_correlation = abs(correlation)

        if absolute_correlation < 0.20:
            strength = "Very Weak"

        elif absolute_correlation < 0.40:
            strength = "Weak"

        elif absolute_correlation < 0.60:
            strength = "Moderate"

        elif absolute_correlation < 0.80:
            strength = "Strong"

        else:
            strength = "Very Strong"


        if correlation > 0:
            direction = "Positive"

        elif correlation < 0:
            direction = "Negative"

        else:
            direction = "No Linear Relationship"


        # ----------------------------------------------------
        # SUMMARY METRICS
        # ----------------------------------------------------

        metric1, metric2, metric3, metric4 = st.columns(4)

        with metric1:

            st.metric(
                "Observations",
                f"{len(comparison_df):,}",
            )

        with metric2:

            st.metric(
                "Pearson Correlation",
                f"{correlation:.3f}",
            )

        with metric3:

            st.metric(
                "Direction",
                direction,
            )

        with metric4:

            st.metric(
                "Strength",
                strength,
            )


        # ----------------------------------------------------
        # SCATTER PLOT
        # ----------------------------------------------------

        st.markdown("### 🔵 Scatter Plot")

        fig, ax = plt.subplots(
            figsize=(10, 6)
        )

        ax.scatter(
            comparison_df[x_variable],
            comparison_df[y_variable],
            alpha=0.7,
        )

        ax.set_title(
            f"{y_variable} vs {x_variable}"
        )

        ax.set_xlabel(
            x_variable
        )

        ax.set_ylabel(
            y_variable
        )

        ax.grid(
            alpha=0.3
        )

        plt.tight_layout()

        st.pyplot(fig)

        plt.close(fig)


        # ----------------------------------------------------
        # INTERPRETATION
        # ----------------------------------------------------

        st.markdown("### 📝 Interpretation")

        if correlation > 0.79:

            st.success(
                f"There is a very strong positive relationship "
                f"between {x_variable} and {y_variable} "
                f"(r = {correlation:.3f})."
            )

        elif correlation > 0.59:

            st.info(
                f"There is a strong positive relationship "
                f"between {x_variable} and {y_variable} "
                f"(r = {correlation:.3f})."
            )

        elif correlation > 0.39:

            st.info(
                f"There is a moderate positive relationship "
                f"between {x_variable} and {y_variable} "
                f"(r = {correlation:.3f})."
            )

        elif correlation > 0.19:

            st.info(
                f"There is a weak positive relationship "
                f"between {x_variable} and {y_variable} "
                f"(r = {correlation:.3f})."
            )

        elif correlation >= -0.19:

            st.info(
                f"There is a very weak or no linear relationship "
                f"between {x_variable} and {y_variable} "
                f"(r = {correlation:.3f})."
            )

        elif correlation >= -0.39:

            st.info(
                f"There is a weak negative relationship "
                f"between {x_variable} and {y_variable} "
                f"(r = {correlation:.3f})."
            )

        elif correlation >= -0.59:

            st.info(
                f"There is a moderate negative relationship "
                f"between {x_variable} and {y_variable} "
                f"(r = {correlation:.3f})."
            )

        elif correlation >= -0.79:

            st.info(
                f"There is a strong negative relationship "
                f"between {x_variable} and {y_variable} "
                f"(r = {correlation:.3f})."
            )

        else:

            st.success(
                f"There is a very strong negative relationship "
                f"between {x_variable} and {y_variable} "
                f"(r = {correlation:.3f})."
            )


        # ----------------------------------------------------
        # COMPARISON TABLE
        # ----------------------------------------------------

        st.markdown("### 📋 Variable Comparison")

        comparison_summary = pd.DataFrame(
            {
                "Variable": [
                    x_variable,
                    y_variable,
                ],
                "Mean": [
                    comparison_df[x_variable].mean(),
                    comparison_df[y_variable].mean(),
                ],
                "Median": [
                    comparison_df[x_variable].median(),
                    comparison_df[y_variable].median(),
                ],
                "Minimum": [
                    comparison_df[x_variable].min(),
                    comparison_df[y_variable].min(),
                ],
                "Maximum": [
                    comparison_df[x_variable].max(),
                    comparison_df[y_variable].max(),
                ],
                "Std. Deviation": [
                    comparison_df[x_variable].std(),
                    comparison_df[y_variable].std(),
                ],
            }
        )

        st.dataframe(
            comparison_summary.round(3),
            use_container_width=True,
            hide_index=True,
        )


        # ----------------------------------------------------
        # DOWNLOAD COMPARISON DATA
        # ----------------------------------------------------

        csv_data = comparison_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Comparison Data (CSV)",
            data=csv_data,
            file_name="V3_2_1_variable_comparison.csv",
            mime="text/csv",
            key="v321_download_csv",
        )
# ============================================================
# TAB 5 — OUTLIERS
# ============================================================

with tab5:

    st.subheader("🚨 Outlier Overview")

    if numeric_count == 0:

        st.info(
            "No numeric variables are available "
            "for outlier analysis."
        )

    else:

        outlier_results = []

        for column in numeric_columns:

            values = df[column].dropna()

            if values.empty:

                continue

            q1 = values.quantile(0.25)
            q3 = values.quantile(0.75)

            iqr = q3 - q1

            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            outliers = values[
                (values < lower_bound)
                | (values > upper_bound)
            ]

            outlier_count = len(outliers)

            percentage = (
                outlier_count
                / len(values)
                * 100
            )

            outlier_results.append(
                {
                    "Variable": column,
                    "Q1": q1,
                    "Median": values.median(),
                    "Q3": q3,
                    "IQR": iqr,
                    "Lower Bound": lower_bound,
                    "Upper Bound": upper_bound,
                    "Outliers": outlier_count,
                    "Outlier %": percentage,
                }
            )

        outlier_summary = pd.DataFrame(
            outlier_results
        )

        if outlier_summary.empty:

            st.info(
                "No outlier results could be calculated."
            )

        else:

            st.dataframe(
                outlier_summary.round(3),
                use_container_width=True,
                hide_index=True,
            )


            total_outliers = int(
                outlier_summary["Outliers"].sum()
            )

            st.metric(
                "Total Detected Outliers",
                f"{total_outliers:,}",
            )


# ============================================================
# TAB 6 — DATA PREVIEW
# ============================================================

with tab6:

    st.subheader("👀 Current Cleaned Dataset")

    st.write(
        f"Showing the current cleaned dataset with "
        f"**{total_rows:,} observations** and "
        f"**{total_columns:,} variables**."
    )

    st.dataframe(
        df,
        use_container_width=True,
        height=500,
    )


# ============================================================
# V3.1 COMPLETION
# ============================================================

st.divider()

st.success(
    "✅ V3.1 Dashboard Foundation is running successfully."
)

st.caption(
    "V1 ✅ Data Cleaning | "
    "V2 ✅ Statistical Analysis | "
    "V3.1 🔄 Dashboard Foundation"
)

# ============================================================
# V3.2.2 — TIME SERIES / LINE CHART & TREND ANALYSIS
# ============================================================

st.divider()

st.subheader("📈 V3.2.2 — Time Series & Trend Analysis")

st.markdown(
    """
    Analyze how a numeric variable changes over time using
    a line chart and basic trend indicators.
    """
)


# ------------------------------------------------------------
# IDENTIFY POSSIBLE DATE / TIME COLUMNS
# ------------------------------------------------------------

possible_date_columns = []

for column in df.columns:

    # Already datetime
    if pd.api.types.is_datetime64_any_dtype(df[column]):
        possible_date_columns.append(column)

    else:
        # Try identifying text columns that look like dates
        if df[column].dtype == "object":

            try:
                converted = pd.to_datetime(
                    df[column],
                    errors="coerce"
                )

                valid_ratio = converted.notna().mean()

                if valid_ratio >= 0.70:
                    possible_date_columns.append(column)

            except Exception:
                pass


# ------------------------------------------------------------
# CHECK REQUIREMENTS
# ------------------------------------------------------------

if numeric_count == 0:

    st.info(
        "No numeric variables are available for trend analysis."
    )

elif len(possible_date_columns) == 0:

    st.warning(
        "⚠️ No suitable date/time variable was automatically detected."
    )

    st.info(
        "A date column such as Date, Month, Year-Month or Time "
        "is required for time series visualization."
    )

else:

    # --------------------------------------------------------
    # VARIABLE SELECTION
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        time_variable = st.selectbox(
            "Select date / time variable",
            possible_date_columns,
            key="v322_time_variable",
        )

    with col2:

        trend_variable = st.selectbox(
            "Select numeric variable",
            numeric_columns,
            key="v322_numeric_variable",
        )


    # --------------------------------------------------------
    # PREPARE TIME SERIES DATA
    # --------------------------------------------------------

    trend_df = df[
        [time_variable, trend_variable]
    ].copy()

    trend_df[time_variable] = pd.to_datetime(
        trend_df[time_variable],
        errors="coerce"
    )

    trend_df[trend_variable] = pd.to_numeric(
        trend_df[trend_variable],
        errors="coerce"
    )

    trend_df = trend_df.dropna(
        subset=[
            time_variable,
            trend_variable,
        ]
    )

    trend_df = trend_df.sort_values(
        by=time_variable
    )


    if trend_df.empty:

        st.warning(
            "No usable observations were found for the selected variables."
        )

    else:

        # ----------------------------------------------------
        # BASIC TREND STATISTICS
        # ----------------------------------------------------

        first_value = trend_df[
            trend_variable
        ].iloc[0]

        last_value = trend_df[
            trend_variable
        ].iloc[-1]

        change = last_value - first_value


        if first_value != 0:

            percentage_change = (
                change / abs(first_value)
            ) * 100

        else:
            percentage_change = None


        minimum_value = trend_df[
            trend_variable
        ].min()

        maximum_value = trend_df[
            trend_variable
        ].max()


        # ----------------------------------------------------
        # TREND DIRECTION
        # ----------------------------------------------------

        if change > 0:

            trend_direction = "Increasing 📈"

        elif change < 0:

            trend_direction = "Decreasing 📉"

        else:

            trend_direction = "No Overall Change ➡️"


        # ----------------------------------------------------
        # METRICS
        # ----------------------------------------------------

        metric1, metric2, metric3, metric4 = st.columns(4)

        with metric1:

            st.metric(
                "First Value",
                f"{first_value:,.3f}"
            )

        with metric2:

            st.metric(
                "Latest Value",
                f"{last_value:,.3f}",
                delta=f"{change:,.3f}"
            )

        with metric3:

            if percentage_change is not None:

                st.metric(
                    "Overall % Change",
                    f"{percentage_change:,.2f}%"
                )

            else:

                st.metric(
                    "Overall % Change",
                    "N/A"
                )

        with metric4:

            st.metric(
                "Trend Direction",
                trend_direction
            )


        # ----------------------------------------------------
        # LINE CHART
        # ----------------------------------------------------

        st.markdown("### 📈 Time Series Line Chart")

        fig, ax = plt.subplots(
            figsize=(11, 6)
        )

        ax.plot(
            trend_df[time_variable],
            trend_df[trend_variable],
            marker="o",
            linewidth=2,
        )

        ax.set_title(
            f"{trend_variable} Over Time"
        )

        ax.set_xlabel(
            time_variable
        )

        ax.set_ylabel(
            trend_variable
        )

        ax.grid(
            alpha=0.3
        )

        plt.xticks(
            rotation=45
        )

        plt.tight_layout()

        st.pyplot(fig)

        plt.close(fig)


        # ----------------------------------------------------
        # MOVING AVERAGE
        # ----------------------------------------------------

        st.markdown("### 📉 Moving Average")

        max_window = min(
            12,
            len(trend_df)
        )

        if max_window >= 2:

            moving_window = st.slider(
                "Select moving average window",
                min_value=2,
                max_value=max_window,
                value=min(3, max_window),
                key="v322_moving_average",
            )

            moving_df = trend_df.copy()

            moving_df["Moving Average"] = (
                moving_df[trend_variable]
                .rolling(
                    window=moving_window
                )
                .mean()
            )


            fig, ax = plt.subplots(
                figsize=(11, 6)
            )

            ax.plot(
                moving_df[time_variable],
                moving_df[trend_variable],
                marker="o",
                label="Actual",
            )

            ax.plot(
                moving_df[time_variable],
                moving_df["Moving Average"],
                linewidth=2,
                label=f"{moving_window}-Period Moving Average",
            )

            ax.set_title(
                f"{trend_variable} with Moving Average"
            )

            ax.set_xlabel(
                time_variable
            )

            ax.set_ylabel(
                trend_variable
            )

            ax.legend()

            ax.grid(
                alpha=0.3
            )

            plt.xticks(
                rotation=45
            )

            plt.tight_layout()

            st.pyplot(fig)

            plt.close(fig)

        else:

            st.info(
                "More observations are required "
                "to calculate a moving average."
            )


        # ----------------------------------------------------
        # PERIOD-TO-PERIOD CHANGE
        # ----------------------------------------------------

        st.markdown("### 🔄 Period-to-Period Change")

        change_df = trend_df.copy()

        change_df["Absolute Change"] = (
            change_df[trend_variable].diff()
        )

        change_df["Percentage Change (%)"] = (
            change_df[trend_variable]
            .pct_change()
            * 100
        )

        st.dataframe(
            change_df.round(3),
            use_container_width=True,
            hide_index=True,
        )


        # ----------------------------------------------------
        # HIGHEST AND LOWEST VALUES
        # ----------------------------------------------------

        st.markdown("### 📌 Trend Summary")

        highest_row = trend_df.loc[
            trend_df[trend_variable].idxmax()
        ]

        lowest_row = trend_df.loc[
            trend_df[trend_variable].idxmin()
        ]

        col1, col2 = st.columns(2)

        with col1:

            st.success(
                f"""
                **Highest value**

                {maximum_value:,.3f}

                Date: {highest_row[time_variable].strftime('%Y-%m-%d')}
                """
            )

        with col2:

            st.info(
                f"""
                **Lowest value**

                {minimum_value:,.3f}

                Date: {lowest_row[time_variable].strftime('%Y-%m-%d')}
                """
            )


        # ----------------------------------------------------
        # INTERPRETATION
        # ----------------------------------------------------

        st.markdown("### 📝 Interpretation")

        if change > 0:

            st.success(
                f"{trend_variable} increased from "
                f"{first_value:,.3f} to {last_value:,.3f}. "
                f"The overall increase was {change:,.3f}."
            )

        elif change < 0:

            st.warning(
                f"{trend_variable} decreased from "
                f"{first_value:,.3f} to {last_value:,.3f}. "
                f"The overall decrease was {abs(change):,.3f}."
            )

        else:

            st.info(
                f"{trend_variable} had no overall change "
                f"between the first and final observation."
            )


        # ----------------------------------------------------
        # DOWNLOAD TIME SERIES DATA
        # ----------------------------------------------------

        trend_csv = change_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Trend Analysis Data (CSV)",
            data=trend_csv,
            file_name="V3_2_2_trend_analysis.csv",
            mime="text/csv",
            key="v322_download_csv",
        )