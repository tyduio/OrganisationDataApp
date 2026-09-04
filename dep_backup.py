import streamlit as st
import pandas as pd


# ============================================================
# V4.1 — DEPARTMENT ANALYSIS
# Department Selection & Department Summary
# ============================================================


st.title("🏢 V4.1 — Department Analysis")

st.markdown(
    """
    This module provides a basic analysis of a selected
    department using the cleaned dataset from the main
    application.
    """
)


# ============================================================
# CHECK CLEANED DATA
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
        "Please return to the main application, upload your "
        "dataset and complete the data cleaning process first."
    )

    st.stop()


# ============================================================
# GET CLEANED DATASET
# ============================================================

df = st.session_state.working_df.copy()


# ============================================================
# DATASET INFORMATION
# ============================================================

total_rows = len(df)
total_columns = len(df.columns)


st.subheader("📋 Current Dataset")

st.write(
    f"The current cleaned dataset contains "
    f"**{total_rows:,} records** and "
    f"**{total_columns:,} variables**."
)


# ============================================================
# DEPARTMENT COLUMN SELECTION
# ============================================================

st.divider()

st.subheader("🏢 Department Selection")

st.write(
    "Select the column that contains the department "
    "information from the dataset."
)


# Get all columns
available_columns = df.columns.tolist()


if not available_columns:

    st.error(
        "❌ No columns were found in the current dataset."
    )

    st.stop()


# Manual department column selection
department_column = st.selectbox(
    "Select Department Column",
    available_columns,
    key="v41_department_column",
)


st.success(
    f"Department column selected: **{department_column}**"
)


# ============================================================
# GET DEPARTMENT VALUES
# ============================================================

department_values = (
    df[department_column]
    .dropna()
    .astype(str)
    .str.strip()
)


# Remove empty values
department_values = department_values[
    department_values != ""
]


available_departments = sorted(
    department_values.unique().tolist()
)


if not available_departments:

    st.warning(
        "⚠️ The selected column does not contain usable "
        "department values."
    )

    st.stop()


# ============================================================
# AVAILABLE DEPARTMENTS
# ============================================================

st.subheader("📋 Available Departments")

st.write(
    f"Found **{len(available_departments)}** "
    f"unique department/category values."
)


available_department_df = pd.DataFrame(
    {
        "Department / Category": available_departments
    }
)


st.dataframe(
    available_department_df,
    use_container_width=True,
    hide_index=True,
)


# ============================================================
# SELECT DEPARTMENT
# ============================================================

st.subheader("🎯 Select Department to Analyse")


selected_department = st.selectbox(
    "Department",
    available_departments,
    key="v41_selected_department",
)


# ============================================================
# FILTER SELECTED DEPARTMENT
# ============================================================

department_df = df[
    df[department_column]
    .astype(str)
    .str.strip()
    == selected_department
].copy()


# ============================================================
# CHECK FILTER RESULT
# ============================================================

if department_df.empty:

    st.warning(
        "⚠️ No records were found for the selected department."
    )

    st.stop()


# ============================================================
# DEPARTMENT SUMMARY
# ============================================================

st.divider()

st.subheader(
    f"📊 Department Summary — {selected_department}"
)


department_rows = len(department_df)
department_columns = len(department_df.columns)


department_numeric = department_df.select_dtypes(
    include="number"
).columns.tolist()


department_categorical = department_df.select_dtypes(
    exclude="number"
).columns.tolist()


department_missing = int(
    department_df.isna().sum().sum()
)


# ============================================================
# SUMMARY METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Department Records",
        f"{department_rows:,}"
    )


with col2:

    st.metric(
        "Variables",
        f"{department_columns:,}"
    )


with col3:

    st.metric(
        "Numeric Variables",
        f"{len(department_numeric):,}"
    )


with col4:

    st.metric(
        "Missing Values",
        f"{department_missing:,}"
    )


# ============================================================
# NUMERIC VARIABLES SUMMARY
# ============================================================

st.divider()

st.subheader("🔢 Numeric Variables Summary")


if not department_numeric:

    st.info(
        "No numeric variables were found "
        "for this department."
    )

else:

    numeric_summary = (
        department_df[
            department_numeric
        ]
        .describe()
        .T
    )


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


# ============================================================
# CATEGORICAL VARIABLES SUMMARY
# ============================================================

st.divider()

st.subheader("🔤 Categorical Variables Summary")


if not department_categorical:

    st.info(
        "No categorical variables were found."
    )

else:

    categorical_summary = []


    for column in department_categorical:

        categorical_summary.append(
            {
                "Variable": column,
                "Unique Values": department_df[
                    column
                ].nunique(dropna=True),
                "Missing Values": int(
                    department_df[column].isna().sum()
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
# SELECTED DEPARTMENT DATA
# ============================================================

st.divider()

st.subheader("👀 Selected Department Data")

st.write(
    f"Showing **{department_rows:,} records** "
    f"belonging to **{selected_department}**."
)


st.dataframe(
    department_df,
    use_container_width=True,
    height=450,
)


# ============================================================
# DOWNLOAD DEPARTMENT DATA
# ============================================================

st.divider()

st.subheader("💾 Department Data Export")


department_csv = department_df.to_csv(
    index=False
).encode("utf-8")


safe_department_name = (
    selected_department
    .lower()
    .replace(" ", "_")
    .replace("(", "")
    .replace(")", "")
    .replace("/", "_")
    .replace("\\", "_")
)


st.download_button(
    label="⬇️ Download Selected Department Data (CSV)",
    data=department_csv,
    file_name=(
        f"department_{safe_department_name}.csv"
    ),
    mime="text/csv",
    key="v41_department_download",
)


# ============================================================
# V4.1 STATUS
# ============================================================

st.divider()

st.success(
    "✅ V4.1 Department Selection & Summary "
    "is running successfully."
)


st.caption(
    "V1 ✅ Data Cleaning | "
    "V2 ✅ Statistical Analysis | "
    "V3 ✅ Dashboard & Visualization | "
    "V4.1 🔄 Department Analysis"
)