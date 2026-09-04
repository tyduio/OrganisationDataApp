import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Organisation Data Processing System",
    page_icon="📊",
    layout="wide"
)


# ==========================================================
# SESSION STATE
# ==========================================================

if "working_df" not in st.session_state:
    st.session_state.working_df = None

if "file_key" not in st.session_state:
    st.session_state.file_key = None

if "processing_stats" not in st.session_state:
    st.session_state.processing_stats = {}

if "processing_history" not in st.session_state:
    st.session_state.processing_history = []


# ==========================================================
# TITLE
# ==========================================================

st.title("📊 Organisation Data Processing System")

st.write(
    "Welcome to the Organisation Data Processing and "
    "Statistical Analysis Application."
)

st.info("Version 1.6: Data Upload, Cleaning, Validation & Processing History")


# ==========================================================
# 1. DEPARTMENT SELECTION
# ==========================================================

st.header("1. Select Department")

department = st.selectbox(
    "Choose the department",
    [
        "GFS (Government Financial Statistics)",
        "Industry and Trade"
    ]
)

st.success(f"Selected Department: {department}")


# ==========================================================
# 2. DATA UPLOAD
# ==========================================================

st.header("2. Upload Data")

uploaded_file = st.file_uploader(
    "Upload your data file",
    type=["csv", "xlsx"],
    help="Supported formats: CSV and Excel (.xlsx)"
)


# ==========================================================
# READ DATA
# ==========================================================

if uploaded_file is not None:

    try:

        # --------------------------------------------------
        # CREATE UNIQUE FILE KEY
        # --------------------------------------------------

        current_file_key = (
            f"{uploaded_file.name}_{uploaded_file.size}"
        )

        # --------------------------------------------------
        # LOAD NEW FILE ONLY
        # --------------------------------------------------

        if st.session_state.file_key != current_file_key:

            if uploaded_file.name.lower().endswith(".csv"):

                original_df = pd.read_csv(uploaded_file)

            elif uploaded_file.name.lower().endswith(".xlsx"):

                original_df = pd.read_excel(uploaded_file)

            else:

                st.error("Unsupported file format.")
                st.stop()

            # Save working copy
            st.session_state.working_df = original_df.copy()

            st.session_state.file_key = current_file_key

            # Reset statistics
            st.session_state.processing_stats = {
                "original_rows": len(original_df),
                "original_columns": len(original_df.columns),
                "duplicate_rows_removed": 0,
                "missing_values_handled": 0,
                "rows_removed_missing": 0,
                "empty_columns_removed": 0,
                "columns_standardized": 0,
                "numeric_columns_converted": 0
            }

        # Current working dataset
        df = st.session_state.working_df

        stats = st.session_state.processing_stats

        st.success(
            f"File uploaded successfully: {uploaded_file.name}"
        )


        # ==================================================
        # 3. DATA PREVIEW
        # ==================================================

        st.subheader("3. Data Preview")

        st.dataframe(
            df,
            use_container_width=True
        )


        # ==================================================
        # 4. DATA INFORMATION
        # ==================================================

        st.subheader("4. Data Information")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Number of Rows",
                df.shape[0]
            )

        with col2:
            st.metric(
                "Number of Columns",
                df.shape[1]
            )

        with col3:
            st.metric(
                "Missing Values",
                int(df.isnull().sum().sum())
            )


        # ==================================================
        # 5. COLUMN INFORMATION
        # ==================================================

        st.subheader("5. Column Information")

        column_info = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str),
            "Missing Values": df.isnull().sum().values,
            "Unique Values": df.nunique().values
        })

        st.dataframe(
            column_info,
            use_container_width=True
        )


        # ==================================================
        # 6. DUPLICATE DATA CHECK
        # ==================================================

        st.subheader("6. Duplicate Data Check")

        duplicate_count = int(df.duplicated().sum())

        if duplicate_count == 0:

            st.success(
                "No duplicate rows found."
            )

        else:

            st.warning(
                f"{duplicate_count} duplicate row(s) found."
            )

            remove_duplicates = st.checkbox(
                "Remove duplicate rows",
                key="remove_duplicates"
            )

            if remove_duplicates:

                df = st.session_state.working_df

                current_duplicates = int(
                    df.duplicated().sum()
                )

                if current_duplicates > 0:

                    df = df.drop_duplicates()

                    st.session_state.working_df = df

                    stats["duplicate_rows_removed"] += (
                        current_duplicates
                    )

                    st.success(
                        f"{current_duplicates} duplicate row(s) "
                        "removed successfully."
                    )


        # ==================================================
        # 7. MISSING VALUES CLEANING
        # ==================================================

        st.subheader("7. Missing Values Cleaning")

        df = st.session_state.working_df

        total_missing = int(
            df.isnull().sum().sum()
        )

        if total_missing == 0:

            st.success(
                "No missing values found in the dataset."
            )

        else:

            st.warning(
                f"{total_missing} missing value(s) found."
            )

            missing_method = st.radio(
                "Choose missing values treatment",
                [
                    "Remove rows with missing values",
                    "Fill missing values automatically"
                ],
                key="missing_method"
            )

            if missing_method == "Remove rows with missing values":

                if st.button(
                    "Remove Missing Rows",
                    key="remove_missing_rows"
                ):

                    before_rows = len(df)
                    missing_before = int(
                        df.isnull().sum().sum()
                    )

                    df = df.dropna()

                    after_rows = len(df)

                    rows_removed = (
                        before_rows - after_rows
                    )

                    st.session_state.working_df = df

                    stats["missing_values_handled"] += (
                        missing_before
                    )

                    stats["rows_removed_missing"] += (
                        rows_removed
                    )

                    st.success(
                        f"{rows_removed} row(s) removed successfully."
                    )

            else:

                if st.button(
                    "Fill Missing Values",
                    key="fill_missing_values"
                ):

                    missing_before = int(
                        df.isnull().sum().sum()
                    )

                    for column in df.columns:

                        if df[column].isnull().sum() > 0:

                            # Numeric column
                            if pd.api.types.is_numeric_dtype(
                                df[column]
                            ):

                                mean_value = df[column].mean()

                                df[column] = df[column].fillna(
                                    mean_value
                                )

                            # Text / categorical column
                            else:

                                mode_value = df[column].mode()

                                if not mode_value.empty:

                                    df[column] = df[column].fillna(
                                        mode_value[0]
                                    )

                    missing_after = int(
                        df.isnull().sum().sum()
                    )

                    values_handled = (
                        missing_before - missing_after
                    )

                    st.session_state.working_df = df

                    stats["missing_values_handled"] += (
                        values_handled
                    )

                    st.success(
                        "Missing values have been filled successfully."
                    )

                    st.write(
                        f"Missing values handled: {values_handled}"
                    )


        # ==================================================
        # 8. DATA VALIDATION & STANDARDIZATION
        # ==================================================

        st.subheader(
            "8. Data Validation & Standardization"
        )

        st.write(
            "This section checks the structure and quality "
            "of the dataset before statistical analysis."
        )


        # --------------------------------------------------
        # 8.1 COLUMN NAME CHECK
        # --------------------------------------------------

        st.markdown("### 8.1 Column Name Check")

        df = st.session_state.working_df

        original_column_names = list(df.columns)

        standardized_columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_", regex=False)
            .str.replace(r"[^\w]", "", regex=True)
        )

        changed_columns = (
            original_column_names
            != list(standardized_columns)
        )

        if changed_columns:

            st.warning(
                "Some column names can be standardized."
            )

            column_name_table = pd.DataFrame({
                "Original Column Name": original_column_names,
                "Standardized Column Name": standardized_columns
            })

            st.dataframe(
                column_name_table,
                use_container_width=True
            )

            standardize_columns = st.checkbox(
                "Standardize column names",
                key="standardize_columns"
            )

            if standardize_columns:

                changed_count = sum(
                    old != new
                    for old, new in zip(
                        original_column_names,
                        standardized_columns
                    )
                )

                df.columns = standardized_columns

                st.session_state.working_df = df

                stats["columns_standardized"] += changed_count

                st.success(
                    f"{changed_count} column name(s) "
                    "standardized successfully."
                )

        else:

            st.success(
                "Column names are already standardized."
            )


        # --------------------------------------------------
        # 8.2 EMPTY COLUMN CHECK
        # --------------------------------------------------

        st.markdown("### 8.2 Empty Column Check")

        df = st.session_state.working_df

        empty_columns = [
            column
            for column in df.columns
            if df[column].isnull().all()
        ]

        if len(empty_columns) == 0:

            st.success(
                "No completely empty columns found."
            )

        else:

            st.warning(
                f"{len(empty_columns)} completely empty "
                "column(s) found."
            )

            for column in empty_columns:
                st.write(f"- {column}")

            remove_empty_columns = st.checkbox(
                "Remove completely empty columns",
                key="remove_empty_columns"
            )

            if remove_empty_columns:

                number_removed = len(empty_columns)

                df = df.drop(
                    columns=empty_columns
                )

                st.session_state.working_df = df

                stats["empty_columns_removed"] += (
                    number_removed
                )

                st.success(
                    f"{number_removed} empty column(s) "
                    "removed successfully."
                )


        # --------------------------------------------------
        # 8.3 DATA TYPE VALIDATION
        # --------------------------------------------------

        st.markdown("### 8.3 Data Type Validation")

        df = st.session_state.working_df

        datatype_report = pd.DataFrame({
            "Column": df.columns,
            "Data Type": [
                str(dtype)
                for dtype in df.dtypes
            ],
            "Numeric": [
                "Yes"
                if pd.api.types.is_numeric_dtype(df[column])
                else "No"
                for column in df.columns
            ],
            "Missing Values": [
                int(df[column].isnull().sum())
                for column in df.columns
            ]
        })

        st.dataframe(
            datatype_report,
            use_container_width=True
        )


        # --------------------------------------------------
        # 8.4 NUMERIC DATA STORED AS TEXT
        # --------------------------------------------------

        st.markdown(
            "### 8.4 Numeric Data Stored as Text"
        )

        df = st.session_state.working_df

        possible_numeric_columns = []

        for column in df.columns:

            if df[column].dtype == "object":

                converted = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )

                non_missing_original = (
                    df[column].notna().sum()
                )

                non_missing_converted = (
                    converted.notna().sum()
                )

                if (
                    non_missing_original > 0
                    and non_missing_converted
                    == non_missing_original
                ):

                    possible_numeric_columns.append(
                        column
                    )

        if len(possible_numeric_columns) == 0:

            st.success(
                "No numeric columns stored as text detected."
            )

        else:

            st.warning(
                "The following columns may contain "
                "numeric values stored as text:"
            )

            for column in possible_numeric_columns:
                st.write(f"- {column}")

            convert_numeric = st.checkbox(
                "Convert detected columns to numeric",
                key="convert_numeric"
            )

            if convert_numeric:

                converted_count = 0

                for column in possible_numeric_columns:

                    df[column] = pd.to_numeric(
                        df[column],
                        errors="coerce"
                    )

                    converted_count += 1

                st.session_state.working_df = df

                stats["numeric_columns_converted"] += (
                    converted_count
                )

                st.success(
                    f"{converted_count} numeric column(s) "
                    "converted successfully."
                )


        # ==================================================
        # 9. VALIDATION SUMMARY
        # ==================================================

        st.subheader("9. Validation Summary")

        df = st.session_state.working_df

        validation_col1, validation_col2, validation_col3 = (
            st.columns(3)
        )

        with validation_col1:

            st.metric(
                "Rows",
                df.shape[0]
            )

        with validation_col2:

            st.metric(
                "Columns",
                df.shape[1]
            )

        with validation_col3:

            st.metric(
                "Missing Values",
                int(df.isnull().sum().sum())
            )

        st.success(
            "Data validation check completed."
        )


        # ==================================================
        # 10. FINAL CLEANED DATASET
        # ==================================================

        st.header("10. Final Cleaned Dataset")

        df = st.session_state.working_df

        final_rows = len(df)
        final_columns = len(df.columns)

        final_missing = int(
            df.isnull().sum().sum()
        )

        final_duplicates = int(
            df.duplicated().sum()
        )

        # --------------------------------------------------
        # FINAL SUMMARY
        # --------------------------------------------------

        summary_col1, summary_col2, summary_col3, summary_col4 = (
            st.columns(4)
        )

        with summary_col1:

            st.metric(
                "Original Rows",
                stats["original_rows"]
            )

        with summary_col2:

            st.metric(
                "Final Rows",
                final_rows
            )

        with summary_col3:

            st.metric(
                "Final Columns",
                final_columns
            )

        with summary_col4:

            st.metric(
                "Remaining Missing",
                final_missing
            )


        # --------------------------------------------------
        # FINAL STATUS
        # --------------------------------------------------

        if final_missing == 0 and final_duplicates == 0:

            st.success(
                "🎉 Dataset is clean and ready for "
                "statistical analysis."
            )

        else:

            st.warning(
                "⚠️ Dataset still requires additional "
                "cleaning before statistical analysis."
            )


        # --------------------------------------------------
        # FINAL DATA PREVIEW
        # --------------------------------------------------

        st.subheader("Final Data Preview")

        st.dataframe(
            df,
            use_container_width=True
        )


        # ==================================================
        # 11. CLEANING REPORT
        # ==================================================

        st.header("11. Cleaning Report")

        st.write(
            "Summary of all cleaning and processing "
            "activities performed on the dataset."
        )

        report_data = {
            "Processing Step": [
                "Original Rows",
                "Final Rows",
                "Duplicate Rows Removed",
                "Missing Values Handled",
                "Rows Removed Due to Missing Values",
                "Empty Columns Removed",
                "Column Names Standardized",
                "Numeric Columns Converted",
                "Final Missing Values",
                "Final Duplicate Rows"
            ],
            "Result": [
                stats["original_rows"],
                final_rows,
                stats["duplicate_rows_removed"],
                stats["missing_values_handled"],
                stats["rows_removed_missing"],
                stats["empty_columns_removed"],
                stats["columns_standardized"],
                stats["numeric_columns_converted"],
                final_missing,
                final_duplicates
            ]
        }

        cleaning_report = pd.DataFrame(
            report_data
        )

        st.dataframe(
            cleaning_report,
            use_container_width=True
        )


        # ==================================================
        # 12. PROCESSING STATUS
        # ==================================================

        st.header("12. Processing Status")

        if final_missing == 0 and final_duplicates == 0:

            status = "READY FOR STATISTICAL ANALYSIS"

            st.success(
                f"✅ {status}"
            )

        else:

            status = "ADDITIONAL CLEANING REQUIRED"

            st.warning(
                f"⚠️ {status}"
            )


        # ==================================================
        # 13. SAVE PROCESSING HISTORY
        # ==================================================

        st.header("13. Processing History")

        st.write(
            "Save this cleaning session to the processing history."
        )

        if st.button(
            "💾 Save Processing Report to History",
            key="save_history"
        ):

            history_record = {
                "Date & Time": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "Department": department,
                "File": uploaded_file.name,
                "Original Rows": stats["original_rows"],
                "Final Rows": final_rows,
                "Duplicates Removed": stats[
                    "duplicate_rows_removed"
                ],
                "Missing Values Handled": stats[
                    "missing_values_handled"
                ],
                "Empty Columns Removed": stats[
                    "empty_columns_removed"
                ],
                "Columns Standardized": stats[
                    "columns_standardized"
                ],
                "Numeric Columns Converted": stats[
                    "numeric_columns_converted"
                ],
                "Final Missing": final_missing,
                "Final Duplicates": final_duplicates,
                "Status": status
            }

            st.session_state.processing_history.append(
                history_record
            )

            st.success(
                "✅ Processing report saved to history."
            )


        # --------------------------------------------------
        # DISPLAY HISTORY
        # --------------------------------------------------

        if len(st.session_state.processing_history) > 0:

            history_df = pd.DataFrame(
                st.session_state.processing_history
            )

            st.subheader(
                "📋 Processing History Records"
            )

            st.dataframe(
                history_df,
                use_container_width=True
            )

            # Download history
            history_csv = history_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="📥 Download Processing History",
                data=history_csv,
                file_name="processing_history.csv",
                mime="text/csv"
            )


        # ==================================================
        # 14. DOWNLOAD CLEANED DATA
        # ==================================================

        st.header("14. Download Cleaned Data")

        st.write(
            "Download the final cleaned dataset."
        )


        # --------------------------------------------------
        # CSV
        # --------------------------------------------------

        csv_data = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv_data,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )


        # --------------------------------------------------
        # EXCEL
        # --------------------------------------------------

        excel_buffer = BytesIO()

        with pd.ExcelWriter(
            excel_buffer,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False,
                sheet_name="Cleaned Data"
            )

            cleaning_report.to_excel(
                writer,
                index=False,
                sheet_name="Cleaning Report"
            )

        excel_data = excel_buffer.getvalue()

        st.download_button(
            label="📊 Download Cleaned Excel + Report",
            data=excel_data,
            file_name="cleaned_data_with_report.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )
        )        # ==================================================
        # 15. V2.1 - DESCRIPTIVE STATISTICS
        # ==================================================

        st.header("📊 V2.1 — Descriptive Statistics")

        st.write(
            "Descriptive statistics provide a summary of "
            "the numerical characteristics of the cleaned dataset."
        )

        # --------------------------------------------------
        # CHECK NUMERIC VARIABLES
        # --------------------------------------------------

        numeric_columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

        if len(numeric_columns) == 0:

            st.warning(
                "No numeric variables are available for "
                "descriptive statistical analysis."
            )

        else:

            st.success(
                f"{len(numeric_columns)} numeric variable(s) "
                "available for analysis."
            )

            # --------------------------------------------------
            # VARIABLE SELECTION
            # --------------------------------------------------

            st.subheader("15.1 Select Variables")

            selected_variables = st.multiselect(
                "Select numeric variable(s) to analyse:",
                numeric_columns,
                default=numeric_columns
            )

            if len(selected_variables) == 0:

                st.info(
                    "Please select at least one numeric variable."
                )

            else:

                # --------------------------------------------------
                # CALCULATE DESCRIPTIVE STATISTICS
                # --------------------------------------------------

                results = []

                for column in selected_variables:

                    series = df[column].dropna()

                    count = int(series.count())

                    mean_value = series.mean()

                    median_value = series.median()

                    mode_values = series.mode()

                    if len(mode_values) > 0:
                        mode_value = mode_values.iloc[0]
                    else:
                        mode_value = None

                    minimum = series.min()

                    maximum = series.max()

                    data_range = maximum - minimum

                    variance = series.var()

                    standard_deviation = series.std()

                    q1 = series.quantile(0.25)

                    q2 = series.quantile(0.50)

                    q3 = series.quantile(0.75)

                    results.append({
                        "Variable": column,
                        "Count": count,
                        "Mean": mean_value,
                        "Median": median_value,
                        "Mode": mode_value,
                        "Minimum": minimum,
                        "Maximum": maximum,
                        "Range": data_range,
                        "Variance": variance,
                        "Standard Deviation": standard_deviation,
                        "Q1 (25%)": q1,
                        "Q2 (50%)": q2,
                        "Q3 (75%)": q3
                    })

                descriptive_df = pd.DataFrame(
                    results
                )

                # --------------------------------------------------
                # RESULTS
                # --------------------------------------------------

                st.subheader(
                    "15.2 Descriptive Statistics Results"
                )

                st.dataframe(
                    descriptive_df,
                    use_container_width=True
                )

                # --------------------------------------------------
                # SELECT ONE VARIABLE FOR DETAILED VIEW
                # --------------------------------------------------

                st.subheader(
                    "15.3 Detailed Variable Statistics"
                )

                detail_variable = st.selectbox(
                    "Select a variable for detailed statistics:",
                    selected_variables
                )

                detail_series = df[
                    detail_variable
                ].dropna()

                detail_count = int(
                    detail_series.count()
                )

                detail_mean = detail_series.mean()

                detail_median = detail_series.median()

                detail_mode = detail_series.mode()

                if len(detail_mode) > 0:
                    detail_mode_value = detail_mode.iloc[0]
                else:
                    detail_mode_value = "No mode"

                detail_min = detail_series.min()

                detail_max = detail_series.max()

                detail_range = (
                    detail_max - detail_min
                )

                detail_variance = detail_series.var()

                detail_std = detail_series.std()

                detail_q1 = detail_series.quantile(
                    0.25
                )

                detail_q2 = detail_series.quantile(
                    0.50
                )

                detail_q3 = detail_series.quantile(
                    0.75
                )

                # --------------------------------------------------
                # METRICS
                # --------------------------------------------------

                metric1, metric2, metric3, metric4 = (
                    st.columns(4)
                )

                with metric1:
                    st.metric(
                        "Count",
                        detail_count
                    )

                with metric2:
                    st.metric(
                        "Mean",
                        f"{detail_mean:,.4f}"
                    )

                with metric3:
                    st.metric(
                        "Median",
                        f"{detail_median:,.4f}"
                    )

                with metric4:
                    st.metric(
                        "Std. Deviation",
                        f"{detail_std:,.4f}"
                    )

                metric5, metric6, metric7, metric8 = (
                    st.columns(4)
                )

                with metric5:
                    st.metric(
                        "Minimum",
                        f"{detail_min:,.4f}"
                    )

                with metric6:
                    st.metric(
                        "Maximum",
                        f"{detail_max:,.4f}"
                    )

                with metric7:
                    st.metric(
                        "Range",
                        f"{detail_range:,.4f}"
                    )

                with metric8:
                    st.metric(
                        "Variance",
                        f"{detail_variance:,.4f}"
                    )

                # --------------------------------------------------
                # QUARTILES
                # --------------------------------------------------

                st.subheader(
                    "15.4 Quartile Statistics"
                )

                quartile_df = pd.DataFrame({
                    "Statistic": [
                        "Q1 (25%)",
                        "Q2 (50%) / Median",
                        "Q3 (75%)"
                    ],
                    "Value": [
                        detail_q1,
                        detail_q2,
                        detail_q3
                    ]
                })

                st.dataframe(
                    quartile_df,
                    use_container_width=True
                )

                # --------------------------------------------------
                # MODE
                # --------------------------------------------------

                st.subheader(
                    "15.5 Mode"
                )

                st.write(
                    f"**{detail_variable} Mode:** "
                    f"{detail_mode_value}"
                )

                # --------------------------------------------------
                # DOWNLOAD CSV
                # --------------------------------------------------

                st.subheader(
                    "15.6 Download Statistical Results"
                )

                descriptive_csv = (
                    descriptive_df
                    .to_csv(index=False)
                    .encode("utf-8")
                )

                st.download_button(
                    label="📥 Download Descriptive Statistics CSV",
                    data=descriptive_csv,
                    file_name="descriptive_statistics.csv",
                    mime="text/csv"
                )

                # --------------------------------------------------
                # DOWNLOAD EXCEL
                # --------------------------------------------------

                statistics_excel_buffer = BytesIO()

                with pd.ExcelWriter(
                    statistics_excel_buffer,
                    engine="openpyxl"
                ) as writer:

                    descriptive_df.to_excel(
                        writer,
                        index=False,
                        sheet_name="Descriptive Statistics"
                    )

                    quartile_df.to_excel(
                        writer,
                        index=False,
                        sheet_name="Quartiles"
                    )

                statistics_excel_data = (
                    statistics_excel_buffer.getvalue()
                )

                st.download_button(
                    label="📊 Download Descriptive Statistics Excel",
                    data=statistics_excel_data,
                    file_name="descriptive_statistics.xlsx",
                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "spreadsheetml.sheet"
                    )
                )

                # --------------------------------------------------
                # COMPLETION STATUS
                # --------------------------------------------------

                st.success(
                    "✅ V2.1 Descriptive Statistics completed successfully."
                )        # ==================================================
        # 16. V2.2 - FREQUENCY & DISTRIBUTION ANALYSIS
        # ==================================================

        st.header("📊 V2.2 — Frequency & Distribution Analysis")

        st.write(
            "This section analyses the frequency and distribution "
            "of variables in the cleaned dataset."
        )

        # --------------------------------------------------
        # 16.1 VARIABLE SELECTION
        # --------------------------------------------------

        st.subheader("16.1 Select Variable")

        all_columns = df.columns.tolist()

        frequency_variable = st.selectbox(
            "Select a variable for frequency analysis:",
            all_columns,
            key="frequency_variable"
        )

        selected_series = df[frequency_variable].dropna()

        if selected_series.empty:

            st.warning(
                "The selected variable contains no valid observations."
            )

        else:

            # --------------------------------------------------
            # IDENTIFY VARIABLE TYPE
            # --------------------------------------------------

            if pd.api.types.is_numeric_dtype(
                selected_series
            ):

                variable_type = "Numeric"

            else:

                variable_type = "Categorical"

            st.info(
                f"Variable: **{frequency_variable}** | "
                f"Type: **{variable_type}** | "
                f"Observations: **{len(selected_series)}**"
            )


            # ==================================================
            # 16.2 CATEGORICAL FREQUENCY ANALYSIS
            # ==================================================

            if variable_type == "Categorical":

                st.subheader(
                    "16.2 Categorical Frequency Table"
                )

                frequency_table = (
                    selected_series
                    .value_counts(dropna=False)
                    .reset_index()
                )

                frequency_table.columns = [
                    "Value",
                    "Frequency"
                ]

                frequency_table[
                    "Percentage"
                ] = (
                    frequency_table["Frequency"]
                    / frequency_table["Frequency"].sum()
                    * 100
                )

                frequency_table[
                    "Cumulative Frequency"
                ] = frequency_table[
                    "Frequency"
                ].cumsum()

                frequency_table[
                    "Cumulative Percentage"
                ] = (
                    frequency_table["Percentage"]
                    .cumsum()
                )

                # Round percentages
                frequency_table[
                    "Percentage"
                ] = frequency_table[
                    "Percentage"
                ].round(2)

                frequency_table[
                    "Cumulative Percentage"
                ] = frequency_table[
                    "Cumulative Percentage"
                ].round(2)

                st.dataframe(
                    frequency_table,
                    use_container_width=True
                )


                # --------------------------------------------------
                # SUMMARY
                # --------------------------------------------------

                st.subheader(
                    "16.3 Frequency Summary"
                )

                most_common = (
                    frequency_table.iloc[0]["Value"]
                )

                highest_frequency = int(
                    frequency_table.iloc[0]["Frequency"]
                )

                summary1, summary2, summary3 = (
                    st.columns(3)
                )

                with summary1:

                    st.metric(
                        "Total Observations",
                        len(selected_series)
                    )

                with summary2:

                    st.metric(
                        "Unique Categories",
                        selected_series.nunique()
                    )

                with summary3:

                    st.metric(
                        "Most Common",
                        str(most_common)
                    )

                st.write(
                    f"The most frequent category is "
                    f"**{most_common}**, appearing "
                    f"**{highest_frequency}** time(s)."
                )


                # --------------------------------------------------
                # BAR CHART
                # --------------------------------------------------

                st.subheader(
                    "16.4 Frequency Distribution"
                )

                chart_data = frequency_table[
                    ["Value", "Frequency"]
                ].set_index("Value")

                st.bar_chart(
                    chart_data
                )


            # ==================================================
            # 16.5 NUMERIC FREQUENCY DISTRIBUTION
            # ==================================================

            else:

                st.subheader(
                    "16.5 Numeric Frequency Distribution"
                )

                # --------------------------------------------------
                # NUMBER OF BINS
                # --------------------------------------------------

                if len(selected_series) >= 2:

                    default_bins = min(
                        10,
                        max(
                            2,
                            int(len(selected_series) ** 0.5)
                        )
                    )

                    number_of_bins = st.slider(
                        "Number of groups / bins:",
                        min_value=2,
                        max_value=30,
                        value=default_bins,
                        key="number_of_bins"
                    )

                    # --------------------------------------------------
                    # CREATE INTERVALS
                    # --------------------------------------------------

                    try:

                        binned_data = pd.cut(
                            selected_series,
                            bins=number_of_bins,
                            include_lowest=True
                        )

                        numeric_frequency = (
                            binned_data
                            .value_counts(sort=False)
                            .reset_index()
                        )

                        numeric_frequency.columns = [
                            "Interval",
                            "Frequency"
                        ]

                        numeric_frequency[
                            "Percentage"
                        ] = (
                            numeric_frequency["Frequency"]
                            / numeric_frequency["Frequency"].sum()
                            * 100
                        )

                        numeric_frequency[
                            "Cumulative Frequency"
                        ] = (
                            numeric_frequency["Frequency"]
                            .cumsum()
                        )

                        numeric_frequency[
                            "Cumulative Percentage"
                        ] = (
                            numeric_frequency["Percentage"]
                            .cumsum()
                        )

                        numeric_frequency[
                            "Percentage"
                        ] = numeric_frequency[
                            "Percentage"
                        ].round(2)

                        numeric_frequency[
                            "Cumulative Percentage"
                        ] = numeric_frequency[
                            "Cumulative Percentage"
                        ].round(2)


                        # --------------------------------------------------
                        # DISPLAY TABLE
                        # --------------------------------------------------

                        st.dataframe(
                            numeric_frequency,
                            use_container_width=True
                        )

                        #---HISTOGRAM---#
                        #___HISTOGRAM__#
                        
                        st.subheader(
                            "16.6 HISTOGRAM "
                        )
                        histogram_counts = (
                            numeric_frequency[
                                ["Interval", "Frequency"]
                            ]
                            .copy()
                        )
                        histogram_counts["Intervals"] = (
                            histogram_counts["Interval"]
                            .astype(str)
                        )
                        
                        histogram_counts = histogram_counts.set_index(
                            "Interval"
                        )
                        
                        st.bar_chart(
                            histogram_counts,
                            use_container_width=True
                        )
                        
                        
                        # --------------------------------------------------
                        # NUMERIC SUMMARY
                        # --------------------------------------------------

                        st.subheader(
                            "16.7 Distribution Summary"
                        )

                        numeric_summary1, numeric_summary2, numeric_summary3, numeric_summary4 = (
                            st.columns(4)
                        )

                        with numeric_summary1:

                            st.metric(
                                "Observations",
                                len(selected_series)
                            )

                        with numeric_summary2:

                            st.metric(
                                "Minimum",
                                f"{selected_series.min():,.2f}"
                            )

                        with numeric_summary3:

                            st.metric(
                                "Maximum",
                                f"{selected_series.max():,.2f}"
                            )

                        with numeric_summary4:

                            st.metric(
                                "Groups",
                                number_of_bins
                            )


                        # --------------------------------------------------
                        # DOWNLOAD NUMERIC RESULTS
                        # --------------------------------------------------

                        st.subheader(
                            "16.8 Download Frequency Results"
                        )

                        numeric_csv = (
                            numeric_frequency
                            .to_csv(index=False)
                            .encode("utf-8")
                        )

                        st.download_button(
                            label="📥 Download Frequency Table CSV",
                            data=numeric_csv,
                            file_name="numeric_frequency_distribution.csv",
                            mime="text/csv"
                        )


                        numeric_excel_buffer = BytesIO()

                        with pd.ExcelWriter(
                            numeric_excel_buffer,
                            engine="openpyxl"
                        ) as writer:

                            numeric_frequency.to_excel(
                                writer,
                                index=False,
                                sheet_name="Frequency Distribution"
                            )

                        numeric_excel_data = (
                            numeric_excel_buffer.getvalue()
                        )

                        st.download_button(
                            label="📊 Download Frequency Distribution Excel",
                            data=numeric_excel_data,
                            file_name="numeric_frequency_distribution.xlsx",
                            mime=(
                                "application/vnd.openxmlformats-officedocument."
                                "spreadsheetml.sheet"
                            )
                        )

                    except Exception as frequency_error:

                        st.error(
                            "Unable to create numeric frequency "
                            f"distribution: {frequency_error}"
                        )

                else:

                    st.warning(
                        "At least two observations are required "
                        "for numeric frequency distribution."
                    )


            # ==================================================
            # 16.9 CATEGORICAL DOWNLOAD
            # ==================================================

            if variable_type == "Categorical":

                st.subheader(
                    "16.5 Download Frequency Results"
                )

                categorical_csv = (
                    frequency_table
                    .to_csv(index=False)
                    .encode("utf-8")
                )

                st.download_button(
                    label="📥 Download Frequency Table CSV",
                    data=categorical_csv,
                    file_name="categorical_frequency_table.csv",
                    mime="text/csv"
                )


                categorical_excel_buffer = BytesIO()

                with pd.ExcelWriter(
                    categorical_excel_buffer,
                    engine="openpyxl"
                ) as writer:

                    frequency_table.to_excel(
                        writer,
                        index=False,
                        sheet_name="Frequency Table"
                    )

                categorical_excel_data = (
                    categorical_excel_buffer.getvalue()
                )

                st.download_button(
                    label="📊 Download Frequency Table Excel",
                    data=categorical_excel_data,
                    file_name="categorical_frequency_table.xlsx",
                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "spreadsheetml.sheet"
                    )
                )


            # ==================================================
            # 16.10 COMPLETION STATUS
            # ==================================================

            st.success(
                "✅ V2.2 Frequency & Distribution Analysis "
                "completed successfully."
            )
            
               
               
               
            


    except Exception as e:

        st.error(
            f"An error occurred while processing the file: {e}"
        )