import streamlit as st
import pandas as pd
from io import BytesIO


# =========================================================
# V5.1 — DATA EXTRACTION & FILTERING
# =========================================================

st.title("📤 V5.1 — Data Extraction & Filtering")

st.caption(
    "Extract only the records and variables you need from the cleaned dataset "
    "using one or more filtering rules."
)


# =========================================================
# CHECK CLEANED DATASET
# =========================================================

if "working_df" not in st.session_state or st.session_state.working_df is None:

    st.warning(
        "No cleaned dataset is available. Please upload and clean your data "
        "from the main page first."
    )

    st.stop()


source_df = st.session_state.working_df.copy()


if source_df.empty:
    st.warning("The current cleaned dataset has no records.")
    st.stop()


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def is_date_like(series):

    if pd.api.types.is_datetime64_any_dtype(series):
        return True

    if (
        pd.api.types.is_object_dtype(series)
        or pd.api.types.is_string_dtype(series)
    ):

        non_null = series.dropna()

        if non_null.empty:
            return False

        sample = non_null.astype(str).head(100)

        converted = pd.to_datetime(
            sample,
            errors="coerce"
        )

        return converted.notna().mean() >= 0.80

    return False


def build_rule_mask(
    df,
    column,
    operator,
    value1=None,
    value2=None
):

    series = df[column]

    # -----------------------------------------------------
    # MISSING VALUES
    # -----------------------------------------------------

    if operator == "Is Missing":
        return series.isna()

    if operator == "Is Not Missing":
        return series.notna()


    # -----------------------------------------------------
    # NUMERIC VARIABLES
    # -----------------------------------------------------

    if pd.api.types.is_numeric_dtype(series):

        numeric_series = pd.to_numeric(
            series,
            errors="coerce"
        )

        if operator == "=":
            return numeric_series == value1

        if operator == "!=":
            return numeric_series != value1

        if operator == ">":
            return numeric_series > value1

        if operator == ">=":
            return numeric_series >= value1

        if operator == "<":
            return numeric_series < value1

        if operator == "<=":
            return numeric_series <= value1

        if operator == "Between":

            low = min(value1, value2)
            high = max(value1, value2)

            return numeric_series.between(
                low,
                high,
                inclusive="both"
            )


    # -----------------------------------------------------
    # DATE VARIABLES
    # -----------------------------------------------------

    if is_date_like(series):

        date_series = pd.to_datetime(
            series,
            errors="coerce"
        )

        v1 = (
            pd.to_datetime(value1)
            if value1 is not None
            else None
        )

        v2 = (
            pd.to_datetime(value2)
            if value2 is not None
            else None
        )

        if operator == "On":

            return (
                date_series.dt.date
                == v1.date()
            )

        if operator == "Before":
            return date_series < v1

        if operator == "On or Before":
            return date_series <= v1

        if operator == "After":
            return date_series > v1

        if operator == "On or After":
            return date_series >= v1

        if operator == "Between Dates":

            start = min(v1, v2)
            end = max(v1, v2)

            return date_series.between(
                start,
                end,
                inclusive="both"
            )


    # -----------------------------------------------------
    # TEXT / CATEGORICAL VARIABLES
    # -----------------------------------------------------

    text_series = series.astype("string")

    if operator == "Equals":

        return (
            text_series
            == str(value1)
        )

    if operator == "Not Equals":

        return (
            text_series
            != str(value1)
        )

    if operator == "Contains":

        return text_series.str.contains(
            str(value1),
            case=False,
            na=False,
            regex=False
        )

    if operator == "Does Not Contain":

        return ~text_series.str.contains(
            str(value1),
            case=False,
            na=False,
            regex=False
        )

    if operator == "Starts With":

        return text_series.str.startswith(
            str(value1),
            na=False
        )

    if operator == "Ends With":

        return text_series.str.endswith(
            str(value1),
            na=False
        )

    if operator == "In Selected Values":

        selected = (
            value1
            if isinstance(value1, list)
            else []
        )

        return series.isin(selected)

    return pd.Series(
        True,
        index=df.index
    )


def dataframe_to_excel(
    dataframe,
    summary_df
):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        dataframe.to_excel(
            writer,
            index=False,
            sheet_name="Extracted Data"
        )

        summary_df.to_excel(
            writer,
            index=False,
            sheet_name="Extraction Summary"
        )

    output.seek(0)

    return output.getvalue()


# =========================================================
# DATASET OVERVIEW
# =========================================================

st.subheader(
    "1️⃣ Current Cleaned Dataset"
)

m1, m2, m3 = st.columns(3)

m1.metric(
    "Rows",
    f"{len(source_df):,}"
)

m2.metric(
    "Columns",
    len(source_df.columns)
)

m3.metric(
    "Total Cells",
    f"{source_df.shape[0] * source_df.shape[1]:,}"
)


with st.expander(
    "Preview current cleaned data",
    expanded=False
):

    st.dataframe(
        source_df.head(50),
        use_container_width=True
    )


# =========================================================
# COLUMN EXTRACTION
# =========================================================

st.divider()

st.subheader(
    "2️⃣ Select Columns to Extract"
)

selected_columns = st.multiselect(
    "Choose the columns you want in the extracted dataset",
    options=list(source_df.columns),
    default=list(source_df.columns),
    help=(
        "Filtering can use any column in the original cleaned dataset, "
        "even if that column is not selected for final output."
    )
)


if not selected_columns:

    st.warning(
        "Select at least one column for the final extracted dataset."
    )


# =========================================================
# ROW FILTERING RULES
# =========================================================

st.divider()

st.subheader(
    "3️⃣ Create Row Filtering Rules"
)


use_filters = st.checkbox(
    "Enable row filtering",
    value=True,
    help=(
        "Turn this off if you only want to extract selected columns "
        "without filtering rows."
    )
)


rule_masks = []
rule_descriptions = []


if use_filters:

    combine_mode = st.radio(
        "How should multiple rules be combined?",
        options=[
            "AND",
            "OR"
        ],
        horizontal=True,
        help=(
            "AND = a row must satisfy every rule. "
            "OR = a row may satisfy any one of the rules."
        )
    )


    number_of_rules = st.number_input(
        "Number of filtering rules",
        min_value=1,
        max_value=10,
        value=1,
        step=1
    )


    st.info(
        "Example: Salary > 500000 AND Region Equals Dar es Salaam."
    )


    for i in range(
        int(number_of_rules)
    ):

        st.markdown(
            f"### 🔹 Rule {i + 1}"
        )


        rule_col1, rule_col2 = st.columns(2)


        with rule_col1:

            filter_column = st.selectbox(
                f"Column for Rule {i + 1}",
                options=list(source_df.columns),
                key=f"filter_column_{i}"
            )


        series = source_df[
            filter_column
        ]


        # =================================================
        # NUMERIC COLUMN
        # =================================================

        if pd.api.types.is_numeric_dtype(
            series
        ):

            operators = [
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


            with rule_col2:

                operator = st.selectbox(
                    f"Operator for Rule {i + 1}",
                    options=operators,
                    key=f"operator_{i}"
                )


            if operator == "Between":

                val_col1, val_col2 = st.columns(2)


                non_null_numeric = pd.to_numeric(
                    series,
                    errors="coerce"
                ).dropna()


                if non_null_numeric.empty:

                    default_min = 0.0
                    default_max = 0.0

                else:

                    default_min = float(
                        non_null_numeric.min()
                    )

                    default_max = float(
                        non_null_numeric.max()
                    )


                with val_col1:

                    value1 = st.number_input(
                        f"Minimum value — Rule {i + 1}",
                        value=default_min,
                        key=f"value1_{i}"
                    )


                with val_col2:

                    value2 = st.number_input(
                        f"Maximum value — Rule {i + 1}",
                        value=default_max,
                        key=f"value2_{i}"
                    )


                mask = build_rule_mask(
                    source_df,
                    filter_column,
                    operator,
                    value1,
                    value2
                )


                description = (
                    f"{filter_column} "
                    f"Between {value1} and {value2}"
                )


            elif operator in [
                "Is Missing",
                "Is Not Missing"
            ]:

                mask = build_rule_mask(
                    source_df,
                    filter_column,
                    operator
                )

                description = (
                    f"{filter_column} "
                    f"{operator}"
                )


            else:

                non_null_numeric = pd.to_numeric(
                    series,
                    errors="coerce"
                ).dropna()


                if non_null_numeric.empty:

                    default_value = 0.0

                else:

                    default_value = float(
                        non_null_numeric.median()
                    )


                value1 = st.number_input(
                    f"Value for Rule {i + 1}",
                    value=default_value,
                    key=f"value1_{i}"
                )


                mask = build_rule_mask(
                    source_df,
                    filter_column,
                    operator,
                    value1
                )


                description = (
                    f"{filter_column} "
                    f"{operator} "
                    f"{value1}"
                )


        # =================================================
        # DATE COLUMN
        # =================================================

        elif is_date_like(
            series
        ):

            operators = [
                "On",
                "Before",
                "On or Before",
                "After",
                "On or After",
                "Between Dates",
                "Is Missing",
                "Is Not Missing"
            ]


            with rule_col2:

                operator = st.selectbox(
                    f"Operator for Rule {i + 1}",
                    options=operators,
                    key=f"operator_{i}"
                )


            date_series = pd.to_datetime(
                series,
                errors="coerce"
            ).dropna()


            if date_series.empty:

                default_date = (
                    pd.Timestamp.today()
                    .date()
                )

                max_date = (
                    pd.Timestamp.today()
                    .date()
                )

            else:

                default_date = (
                    date_series.min()
                    .date()
                )

                max_date = (
                    date_series.max()
                    .date()
                )


            if operator == "Between Dates":

                val_col1, val_col2 = st.columns(2)


                with val_col1:

                    value1 = st.date_input(
                        f"Start date — Rule {i + 1}",
                        value=default_date,
                        key=f"value1_{i}"
                    )


                with val_col2:

                    value2 = st.date_input(
                        f"End date — Rule {i + 1}",
                        value=max_date,
                        key=f"value2_{i}"
                    )


                mask = build_rule_mask(
                    source_df,
                    filter_column,
                    operator,
                    value1,
                    value2
                )


                description = (
                    f"{filter_column} "
                    f"Between {value1} and {value2}"
                )


            elif operator in [
                "Is Missing",
                "Is Not Missing"
            ]:

                mask = build_rule_mask(
                    source_df,
                    filter_column,
                    operator
                )


                description = (
                    f"{filter_column} "
                    f"{operator}"
                )


            else:

                value1 = st.date_input(
                    f"Date for Rule {i + 1}",
                    value=default_date,
                    key=f"value1_{i}"
                )


                mask = build_rule_mask(
                    source_df,
                    filter_column,
                    operator,
                    value1
                )


                description = (
                    f"{filter_column} "
                    f"{operator} "
                    f"{value1}"
                )


        # =================================================
        # TEXT / CATEGORICAL COLUMN
        # =================================================

        else:

            operators = [
                "Equals",
                "Not Equals",
                "Contains",
                "Does Not Contain",
                "Starts With",
                "Ends With",
                "In Selected Values",
                "Is Missing",
                "Is Not Missing"
            ]


            with rule_col2:

                operator = st.selectbox(
                    f"Operator for Rule {i + 1}",
                    options=operators,
                    key=f"operator_{i}"
                )


            if operator == "In Selected Values":

                unique_values = (
                    series
                    .dropna()
                    .unique()
                    .tolist()
                )


                try:

                    unique_values = sorted(
                        unique_values
                    )

                except TypeError:
                    pass


                value1 = st.multiselect(
                    f"Select accepted values — Rule {i + 1}",
                    options=unique_values,
                    key=f"value1_{i}"
                )


                mask = build_rule_mask(
                    source_df,
                    filter_column,
                    operator,
                    value1
                )


                description = (
                    f"{filter_column} "
                    f"in {value1}"
                )


            elif operator in [
                "Is Missing",
                "Is Not Missing"
            ]:

                mask = build_rule_mask(
                    source_df,
                    filter_column,
                    operator
                )


                description = (
                    f"{filter_column} "
                    f"{operator}"
                )


            else:

                value1 = st.text_input(
                    f"Text/value for Rule {i + 1}",
                    key=f"value1_{i}"
                )


                mask = build_rule_mask(
                    source_df,
                    filter_column,
                    operator,
                    value1
                )


                description = (
                    f"{filter_column} "
                    f"{operator} "
                    f"'{value1}'"
                )


        rule_masks.append(
            mask.fillna(False)
        )

        rule_descriptions.append(
            description
        )


        with st.expander(
            f"Preview Rule {i + 1} result",
            expanded=False
        ):

            matched_rows = int(
                mask
                .fillna(False)
                .sum()
            )

            st.write(
                f"Rows matching this rule: "
                f"**{matched_rows:,}** "
                f"of **{len(source_df):,}**"
            )


        st.divider()


# =========================================================
# APPLY FILTER RULES
# =========================================================

if (
    use_filters
    and rule_masks
):

    combined_mask = (
        rule_masks[0]
        .copy()
    )


    for mask in rule_masks[1:]:

        if combine_mode == "AND":

            combined_mask = (
                combined_mask
                & mask
            )

        else:

            combined_mask = (
                combined_mask
                | mask
            )


    filtered_df = (
        source_df
        .loc[combined_mask]
        .copy()
    )


else:

    filtered_df = (
        source_df
        .copy()
    )


# =========================================================
# APPLY COLUMN SELECTION
# =========================================================

if selected_columns:

    extracted_df = (
        filtered_df[
            selected_columns
        ]
        .copy()
    )

else:

    extracted_df = pd.DataFrame(
        index=filtered_df.index
    )


extracted_df = (
    extracted_df
    .reset_index(drop=True)
)


# =========================================================
# EXTRACTION RESULTS
# =========================================================

st.subheader(
    "4️⃣ Extraction Result"
)


original_rows = len(
    source_df
)

filtered_rows = len(
    filtered_df
)

removed_rows = (
    original_rows
    - filtered_rows
)


if original_rows > 0:

    percentage_kept = (
        filtered_rows
        / original_rows
        * 100
    )

else:

    percentage_kept = 0


r1, r2, r3, r4 = st.columns(4)


r1.metric(
    "Original Rows",
    f"{original_rows:,}"
)

r2.metric(
    "Extracted Rows",
    f"{filtered_rows:,}"
)

r3.metric(
    "Rows Removed",
    f"{removed_rows:,}"
)

r4.metric(
    "Rows Kept",
    f"{percentage_kept:.1f}%"
)


c1, c2 = st.columns(2)

c1.metric(
    "Original Columns",
    len(source_df.columns)
)

c2.metric(
    "Extracted Columns",
    len(selected_columns)
)


# =========================================================
# SHOW RULE SUMMARY
# =========================================================

if use_filters:

    st.markdown(
        "### 📋 Rules Applied"
    )


    for idx, rule_text in enumerate(
        rule_descriptions,
        start=1
    ):

        if idx == 1:

            st.write(
                f"Rule {idx}: {rule_text}"
            )

        else:

            st.write(
                f"{combine_mode} "
                f"Rule {idx}: "
                f"{rule_text}"
            )


# =========================================================
# SHOW EXTRACTED DATA
# =========================================================

if extracted_df.empty:

    st.warning(
        "No records matched the current extraction rules."
    )


elif not selected_columns:

    st.warning(
        "Rows were filtered, but no output columns are selected."
    )


else:

    st.success(
        f"Extraction successful: "
        f"{len(extracted_df):,} rows and "
        f"{len(extracted_df.columns)} columns."
    )


    st.dataframe(
        extracted_df,
        use_container_width=True,
        height=450
    )


# =========================================================
# DOWNLOAD SECTION
# =========================================================

st.divider()

st.subheader(
    "5️⃣ Download Extracted Data"
)


summary_rows = [

    [
        "Original rows",
        original_rows
    ],

    [
        "Rows after filtering",
        filtered_rows
    ],

    [
        "Original columns",
        len(source_df.columns)
    ],

    [
        "Extracted columns",
        len(selected_columns)
    ],

    [
        "Rows kept (%)",
        round(
            percentage_kept,
            2
        )
    ],

    [
        "Rule combination",
        (
            combine_mode
            if use_filters
            else "No row filtering"
        )
    ]

]


for idx, rule_text in enumerate(
    rule_descriptions,
    start=1
):

    summary_rows.append(
        [
            f"Rule {idx}",
            rule_text
        ]
    )


summary_df = pd.DataFrame(
    summary_rows,
    columns=[
        "Item",
        "Value"
    ]
)


if selected_columns:

    csv_data = (
        extracted_df
        .to_csv(
            index=False
        )
        .encode("utf-8")
    )


    d1, d2 = st.columns(2)


    with d1:

        st.download_button(

            label=(
                "⬇️ Download Extracted CSV"
            ),

            data=csv_data,

            file_name=(
                "extracted_data.csv"
            ),

            mime="text/csv",

            use_container_width=True
        )


    with d2:

        excel_data = dataframe_to_excel(
            extracted_df,
            summary_df
        )


        st.download_button(

            label=(
                "⬇️ Download Extracted Excel"
            ),

            data=excel_data,

            file_name=(
                "extracted_data.xlsx"
            ),

            mime=(
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            ),

            use_container_width=True
        )


else:

    st.info(
        "Select at least one output column before downloading."
    )


# =========================================================
# VERSION STATUS
# =========================================================

st.divider()


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
        "🔄 V5.1 — Data Extraction & Filtering"
    )

    st.write(
        "⏳ V5.2 — Data Transformation"
    )

    st.write(
        "⏳ V5.3 — Data Aggregation / Processing"
    )

    st.write(
        "⏳ V5.4 — Advanced Export"
    )