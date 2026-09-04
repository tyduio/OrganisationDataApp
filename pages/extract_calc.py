import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO


# =========================================================
# V5.3 — EXTRACTION OF CALCULATED / GENERATED DATA
# =========================================================

st.title("🔎 V5.3 — Extract Calculated Data")

st.caption(
    "Extract specific records from calculated variables created "
    "in V5.2 using custom filtering rules."
)


# =========================================================
# CHECK CALCULATED DATA
# =========================================================

if (
    "calculated_df" not in st.session_state
    or st.session_state.calculated_df is None
):

    st.warning(
        "No calculated dataset is available yet."
    )

    st.info(
        "Please go to V5.2 — User-Defined Data Calculation, "
        "create at least one calculated variable, and then return here."
    )

    st.stop()


calculated_df = (
    st.session_state.calculated_df.copy()
)


if calculated_df.empty:

    st.warning(
        "The calculated dataset contains no records."
    )

    st.stop()


# =========================================================
# CALCULATION INFORMATION
# =========================================================

calculation_info = (
    st.session_state.get(
        "calculation_info",
        {}
    )
)


generated_variable = (
    calculation_info.get(
        "new_variable",
        None
    )
)


formula_used = (
    calculation_info.get(
        "formula",
        ""
    )
)


# =========================================================
# IDENTIFY GENERATED VARIABLES
# =========================================================

if generated_variable is not None:

    generated_variables = [
        generated_variable
    ]

else:

    generated_variables = []


# Also detect calculated variables that are not
# present in the original cleaned dataset.

if (
    "working_df" in st.session_state
    and st.session_state.working_df is not None
):

    original_df = (
        st.session_state.working_df
    )

    detected_generated = [
        column
        for column in calculated_df.columns
        if column not in original_df.columns
    ]

    for column in detected_generated:

        if column not in generated_variables:

            generated_variables.append(
                column
            )


# =========================================================
# CHECK GENERATED VARIABLES
# =========================================================

if not generated_variables:

    st.warning(
        "No generated/calculated variable was detected."
    )

    st.info(
        "Create a new variable in V5.2 first."
    )

    st.stop()


# =========================================================
# DATASET OVERVIEW
# =========================================================

st.subheader(
    "1️⃣ Calculated Dataset"
)


m1, m2, m3 = st.columns(3)


m1.metric(
    "Rows",
    f"{len(calculated_df):,}"
)


m2.metric(
    "Columns",
    len(calculated_df.columns)
)


m3.metric(
    "Generated Variables",
    len(generated_variables)
)


with st.expander(
    "View calculated dataset",
    expanded=False
):

    st.dataframe(
        calculated_df.head(50),
        use_container_width=True
    )


# =========================================================
# GENERATED VARIABLE INFORMATION
# =========================================================

st.divider()

st.subheader(
    "2️⃣ Generated Variable"
)


selected_generated = st.selectbox(
    "Select the calculated variable to analyse",
    options=generated_variables
)


if formula_used:

    st.write(
        "**Formula used to create this variable:**"
    )

    st.code(
        formula_used
    )


# =========================================================
# GENERATED VARIABLE SUMMARY
# =========================================================

generated_series = (
    calculated_df[
        selected_generated
    ]
)


numeric_generated = pd.to_numeric(
    generated_series,
    errors="coerce"
)


valid_generated = (
    numeric_generated
    .replace(
        [np.inf, -np.inf],
        np.nan
    )
    .dropna()
)


s1, s2, s3, s4 = st.columns(4)


s1.metric(
    "Valid Values",
    f"{len(valid_generated):,}"
)


s2.metric(
    "Missing Values",
    f"{generated_series.isna().sum():,}"
)


if len(valid_generated) > 0:

    s3.metric(
        "Minimum",
        f"{valid_generated.min():,.4f}"
    )

    s4.metric(
        "Maximum",
        f"{valid_generated.max():,.4f}"
    )

else:

    s3.metric(
        "Minimum",
        "N/A"
    )

    s4.metric(
        "Maximum",
        "N/A"
    )


# =========================================================
# EXTRACTION RULE
# =========================================================

st.divider()

st.subheader(
    "3️⃣ Set Extraction Rule"
)


st.info(
    "The rule below determines which rows will be extracted "
    "from the calculated dataset."
)


operator = st.selectbox(
    "Select comparison rule",
    options=[
        "=",
        "!=",
        ">",
        ">=",
        "<",
        "<=",
        "Between",
        "Is Missing",
        "Is Not Missing"
    ]
)


# =========================================================
# NUMERIC FILTER
# =========================================================

if operator == "Between":

    if valid_generated.empty:

        st.error(
            "The selected generated variable has no valid numeric values."
        )

        st.stop()


    default_min = float(
        valid_generated.min()
    )

    default_max = float(
        valid_generated.max()
    )


    c1, c2 = st.columns(2)


    with c1:

        minimum_value = st.number_input(
            "Minimum value",
            value=default_min
        )


    with c2:

        maximum_value = st.number_input(
            "Maximum value",
            value=default_max
        )


    lower_value = min(
        minimum_value,
        maximum_value
    )

    upper_value = max(
        minimum_value,
        maximum_value
    )


    filter_mask = (
        numeric_generated
        .between(
            lower_value,
            upper_value,
            inclusive="both"
        )
    )


    rule_description = (
        f"{selected_generated} "
        f"Between {lower_value} "
        f"and {upper_value}"
    )


elif operator in [
    "Is Missing",
    "Is Not Missing"
]:

    if operator == "Is Missing":

        filter_mask = (
            generated_series
            .isna()
        )

    else:

        filter_mask = (
            generated_series
            .notna()
        )


    rule_description = (
        f"{selected_generated} "
        f"{operator}"
    )


else:

    if valid_generated.empty:

        st.error(
            "The selected generated variable has no valid numeric values."
        )

        st.stop()


    default_value = float(
        valid_generated.median()
    )


    comparison_value = st.number_input(
        "Enter comparison value",
        value=default_value
    )


    if operator == "=":

        filter_mask = (
            numeric_generated
            == comparison_value
        )

    elif operator == "!=":

        filter_mask = (
            numeric_generated
            != comparison_value
        )

    elif operator == ">":

        filter_mask = (
            numeric_generated
            > comparison_value
        )

    elif operator == ">=":

        filter_mask = (
            numeric_generated
            >= comparison_value
        )

    elif operator == "<":

        filter_mask = (
            numeric_generated
            < comparison_value
        )

    elif operator == "<=":

        filter_mask = (
            numeric_generated
            <= comparison_value
        )

    else:

        filter_mask = pd.Series(
            False,
            index=calculated_df.index
        )


    rule_description = (
        f"{selected_generated} "
        f"{operator} "
        f"{comparison_value}"
    )


filter_mask = (
    filter_mask
    .fillna(False)
)


# =========================================================
# RULE RESULT
# =========================================================

matched_rows = int(
    filter_mask.sum()
)


st.markdown(
    "### 📊 Rule Result"
)


r1, r2, r3 = st.columns(3)


r1.metric(
    "Total Rows",
    f"{len(calculated_df):,}"
)


r2.metric(
    "Matching Rows",
    f"{matched_rows:,}"
)


r3.metric(
    "Rows Excluded",
    f"{len(calculated_df) - matched_rows:,}"
)


st.write(
    "**Current rule:**"
)

st.code(
    rule_description
)


# =========================================================
# COLUMN SELECTION
# =========================================================

st.divider()

st.subheader(
    "4️⃣ Select Output Columns"
)


st.info(
    "The filtering variable does not have to appear in the final output. "
    "You can use one variable for filtering and select completely different "
    "columns for the extracted dataset."
)


selected_columns = st.multiselect(
    "Columns to include in extracted data",
    options=list(calculated_df.columns),
    default=list(calculated_df.columns)
)


if not selected_columns:

    st.warning(
        "Select at least one output column."
    )

    st.stop()


# =========================================================
# APPLY EXTRACTION
# =========================================================

extracted_df = (
    calculated_df
    .loc[
        filter_mask,
        selected_columns
    ]
    .copy()
    .reset_index(drop=True)
)


# =========================================================
# EXTRACTION SUMMARY
# =========================================================

st.divider()

st.subheader(
    "5️⃣ Extracted Data"
)


original_rows = len(
    calculated_df
)

extracted_rows = len(
    extracted_df
)

removed_rows = (
    original_rows
    - extracted_rows
)


if original_rows > 0:

    percentage = (
        extracted_rows
        / original_rows
        * 100
    )

else:

    percentage = 0


e1, e2, e3, e4 = st.columns(4)


e1.metric(
    "Original Rows",
    f"{original_rows:,}"
)


e2.metric(
    "Extracted Rows",
    f"{extracted_rows:,}"
)


e3.metric(
    "Rows Excluded",
    f"{removed_rows:,}"
)


e4.metric(
    "Rows Kept",
    f"{percentage:.1f}%"
)


if extracted_df.empty:

    st.warning(
        "No rows satisfy the current extraction rule."
    )

else:

    st.success(
        f"Extraction successful. "
        f"{extracted_rows:,} rows matched the rule."
    )


    st.dataframe(
        extracted_df,
        use_container_width=True,
        height=450
    )


# =========================================================
# OPTIONAL: SAVE AS WORKING DATASET
# =========================================================

st.divider()

st.subheader(
    "6️⃣ Result Handling"
)


st.info(
    "The original cleaned dataset will not be changed automatically."
)


save_as_working = st.checkbox(
    "Save extracted result as the current working dataset"
)


if save_as_working:

    st.warning(
        "This will replace the current working dataset with "
        "the extracted result for subsequent analysis."
    )


    if st.button(
        "💾 Save Extracted Data as Working Dataset",
        type="primary"
    ):

        if extracted_df.empty:

            st.error(
                "Cannot save an empty dataset."
            )

        else:

            st.session_state.working_df = (
                extracted_df.copy()
            )

            st.success(
                "Extracted dataset has been saved as the current working dataset."
            )

            st.info(
                "You can now return to the Dashboard or other modules "
                "to analyse this extracted dataset."
            )


# =========================================================
# DOWNLOAD
# =========================================================

st.divider()

st.subheader(
    "7️⃣ Download Extracted Data"
)


if not extracted_df.empty:

    csv_data = (
        extracted_df
        .to_csv(
            index=False
        )
        .encode("utf-8")
    )


    summary_df = pd.DataFrame(
        [
            [
                "Generated Variable",
                selected_generated
            ],

            [
                "Formula",
                formula_used
            ],

            [
                "Extraction Rule",
                rule_description
            ],

            [
                "Original Rows",
                original_rows
            ],

            [
                "Extracted Rows",
                extracted_rows
            ],

            [
                "Excluded Rows",
                removed_rows
            ],

            [
                "Rows Kept (%)",
                round(
                    percentage,
                    2
                )
            ],

            [
                "Output Columns",
                len(selected_columns)
            ]
        ],
        columns=[
            "Item",
            "Value"
        ]
    )


    excel_output = BytesIO()


    with pd.ExcelWriter(
        excel_output,
        engine="openpyxl"
    ) as writer:

        extracted_df.to_excel(
            writer,
            index=False,
            sheet_name="Extracted Data"
        )

        summary_df.to_excel(
            writer,
            index=False,
            sheet_name="Extraction Summary"
        )


    excel_output.seek(0)


    d1, d2 = st.columns(2)


    with d1:

        st.download_button(
            label="⬇️ Download CSV",
            data=csv_data,
            file_name="calculated_extracted_data.csv",
            mime="text/csv",
            use_container_width=True
        )


    with d2:

        st.download_button(
            label="⬇️ Download Excel",
            data=excel_output.getvalue(),
            file_name="calculated_extracted_data.xlsx",
            mime=(
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            ),
            use_container_width=True
        )


# =========================================================
# WORKFLOW EXPLANATION
# =========================================================

st.divider()


with st.expander(
    "📚 How V5.3 Works",
    expanded=False
):

    st.markdown(
        """
### V5.3 Workflow

**Step 1 — V5.2 creates a variable**

Example:

`Revenue_GDP_Pct * Expenditure_GDP_Pct`

produces:

`height`

**Step 2 — V5.3 selects the generated variable**

Example:

`height`

**Step 3 — User defines the extraction rule**

Example:

`height > 300`

**Step 4 — System checks every row**

Only rows satisfying the rule are retained.

**Step 5 — User chooses output columns**

The filtering variable can be included or excluded from the final dataset.

**Step 6 — User downloads or saves the extracted data.**

The original cleaned dataset is not changed unless the user explicitly chooses:

`Save Extracted Data as Working Dataset`
"""
    )


# =========================================================
# PROJECT STATUS
# =========================================================

with st.expander(
    "📌 Project Version Status",
    expanded=False
):

    st.write(
        "✅ V1 — Data Upload & Cleaning"
    )

    st.write(
        "✅ V2 — Statistical Analysis"
    )

    st.write(
        "✅ V3 — Dashboard & Visualization"
    )

    st.write(
        "⏸️ V4 — Department Analysis "
        "(parked for later improvement)"
    )

    st.write(
        "✅ V5.1 — Data Extraction & Filtering"
    )

    st.write(
        "✅ V5.2 — User-Defined Data Calculation"
    )

    st.write(
        "🔄 V5.3 — Calculated Data Extraction"
    )

    st.write(
        "⏳ V5.4 — Advanced Export"
    )