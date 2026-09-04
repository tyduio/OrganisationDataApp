import streamlit as st
import pandas as pd
import numpy as np
import ast
import operator as op
from io import BytesIO


# =========================================================
# V5.2 — USER-DEFINED DATA CALCULATION
# =========================================================

st.title("🧮 V5.2 — User-Defined Data Calculation")

st.caption(
    "Create a new variable by writing your own mathematical formula "
    "using columns from the current cleaned dataset."
)


# =========================================================
# CHECK DATASET
# =========================================================

if (
    "working_df" not in st.session_state
    or st.session_state.working_df is None
):

    st.warning(
        "No cleaned dataset is available. "
        "Please upload and clean your data from the main page first."
    )

    st.stop()


source_df = st.session_state.working_df.copy()


if source_df.empty:

    st.warning(
        "The current cleaned dataset has no records."
    )

    st.stop()


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def safe_calculate(expression, variables):
    """
    Safely evaluate mathematical expressions.

    Supported:
    +  -  *  /  **  %
    ( )
    abs()
    round()
    sqrt()
    log()
    exp()
    """

    allowed_functions = {
        "abs": np.abs,
        "round": np.round,
        "sqrt": np.sqrt,
        "log": np.log,
        "log10": np.log10,
        "exp": np.exp,
    }

    binary_operations = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.Pow: op.pow,
        ast.Mod: op.mod,
    }

    unary_operations = {
        ast.UAdd: op.pos,
        ast.USub: op.neg,
    }


    def evaluate(node):

        # -------------------------------------------------
        # NUMBER
        # -------------------------------------------------

        if isinstance(node, ast.Constant):

            if isinstance(
                node.value,
                (int, float)
            ):

                return node.value

            raise ValueError(
                "Only numeric values are allowed."
            )


        # -------------------------------------------------
        # VARIABLE / COLUMN
        # -------------------------------------------------

        if isinstance(node, ast.Name):

            if node.id in variables:

                return variables[node.id]

            raise ValueError(
                f"Unknown variable: {node.id}"
            )


        # -------------------------------------------------
        # BINARY OPERATION
        # -------------------------------------------------

        if isinstance(
            node,
            ast.BinOp
        ):

            operation_type = type(
                node.op
            )

            if operation_type not in binary_operations:

                raise ValueError(
                    "This mathematical operator is not allowed."
                )

            left = evaluate(
                node.left
            )

            right = evaluate(
                node.right
            )

            return binary_operations[
                operation_type
            ](
                left,
                right
            )


        # -------------------------------------------------
        # UNARY OPERATION
        # -------------------------------------------------

        if isinstance(
            node,
            ast.UnaryOp
        ):

            operation_type = type(
                node.op
            )

            if operation_type not in unary_operations:

                raise ValueError(
                    "This unary operator is not allowed."
                )

            return unary_operations[
                operation_type
            ](
                evaluate(node.operand)
            )


        # -------------------------------------------------
        # FUNCTION
        # -------------------------------------------------

        if isinstance(
            node,
            ast.Call
        ):

            if not isinstance(
                node.func,
                ast.Name
            ):

                raise ValueError(
                    "Invalid function."
                )


            function_name = (
                node.func.id
            )


            if function_name not in allowed_functions:

                raise ValueError(
                    f"Function '{function_name}' "
                    "is not supported."
                )


            arguments = [
                evaluate(argument)
                for argument in node.args
            ]


            return allowed_functions[
                function_name
            ](
                *arguments
            )


        # -------------------------------------------------
        # PARENTHESES / EXPRESSION
        # -------------------------------------------------

        if isinstance(
            node,
            ast.Expression
        ):

            return evaluate(
                node.body
            )


        raise ValueError(
            "Invalid expression."
        )


    parsed = ast.parse(
        expression,
        mode="eval"
    )

    return evaluate(
        parsed
    )


def convert_formula_columns(
    formula,
    selected_columns
):
    """
    Convert column names into safe variable names.

    Example:
    GDP Growth Rate
    becomes
    GDP_Growth_Rate
    """

    mapping = {}

    for column in selected_columns:

        safe_name = (
            str(column)
            .strip()
            .replace(" ", "_")
            .replace("-", "_")
            .replace("/", "_")
            .replace("(", "")
            .replace(")", "")
        )

        mapping[column] = safe_name


    converted_formula = formula


    # Replace longest names first
    # to reduce partial replacement problems.

    for column in sorted(
        selected_columns,
        key=lambda x: len(str(x)),
        reverse=True
    ):

        safe_name = mapping[column]

        converted_formula = (
            converted_formula
            .replace(
                f"`{column}`",
                safe_name
            )
        )


    return converted_formula, mapping


# =========================================================
# DATASET INFORMATION
# =========================================================

st.subheader(
    "1️⃣ Current Dataset"
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


numeric_columns = (
    source_df
    .select_dtypes(
        include=np.number
    )
    .columns
    .tolist()
)


m3.metric(
    "Numeric Columns",
    len(numeric_columns)
)


with st.expander(
    "View current dataset",
    expanded=False
):

    st.dataframe(
        source_df.head(50),
        use_container_width=True
    )


# =========================================================
# SELECT VARIABLES
# =========================================================

st.divider()

st.subheader(
    "2️⃣ Select Variables for Calculation"
)


st.info(
    "Select the columns that will be used in your formula. "
    "For mathematical calculations, numeric columns are recommended."
)


selected_columns = st.multiselect(
    "Available columns",
    options=list(source_df.columns),
    default=numeric_columns[:5]
)


if not selected_columns:

    st.warning(
        "Please select at least one column."
    )

    st.stop()


# =========================================================
# VARIABLE REFERENCE
# =========================================================

st.markdown(
    "### 🔤 Formula Variable Names"
)


reference_rows = []


for column in selected_columns:

    safe_name = (
        str(column)
        .strip()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        .replace("(", "")
        .replace(")", "")
    )

    reference_rows.append(
        {
            "Original Column": column,
            "Use in Formula": safe_name
        }
    )


reference_df = pd.DataFrame(
    reference_rows
)


st.dataframe(
    reference_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# FORMULA
# =========================================================

st.divider()

st.subheader(
    "3️⃣ Write Your Formula"
)


st.markdown(
    """
Use the **Use in Formula** names shown above.

Examples:

- `GDP / Population`
- `Quantity * Price`
- `Revenue - Cost`
- `(Revenue - Cost) / Revenue * 100`
- `A + B - C`
- `sqrt(GDP)`
- `round(GDP / Population, 2)`
"""
)


formula = st.text_input(
    "Mathematical Formula",
    placeholder=(
        "Example: Revenue - Cost"
    )
)


# =========================================================
# OUTPUT VARIABLE
# =========================================================

st.subheader(
    "4️⃣ Name the New Variable"
)


new_variable = st.text_input(
    "New variable name",
    placeholder=(
        "Example: Profit"
    )
)


# =========================================================
# CALCULATE BUTTON
# =========================================================

st.divider()

calculate_button = st.button(
    "🧮 Calculate New Variable",
    type="primary",
    use_container_width=True
)


if calculate_button:

    if not formula.strip():

        st.error(
            "Please enter a mathematical formula."
        )

        st.stop()


    if not new_variable.strip():

        st.error(
            "Please enter a name for the new variable."
        )

        st.stop()


    # -----------------------------------------------------
    # CLEAN OUTPUT NAME
    # -----------------------------------------------------

    output_name = (
        new_variable
        .strip()
        .replace(" ", "_")
    )


    # -----------------------------------------------------
    # CHECK DUPLICATE VARIABLE
    # -----------------------------------------------------

    if output_name in source_df.columns:

        st.error(
            f"The variable '{output_name}' "
            "already exists in the dataset. "
            "Please choose another name."
        )

        st.stop()


    # -----------------------------------------------------
    # CONVERT FORMULA
    # -----------------------------------------------------

    converted_formula, mapping = (
        convert_formula_columns(
            formula,
            selected_columns
        )
    )


    # -----------------------------------------------------
    # BUILD VARIABLE DICTIONARY
    # -----------------------------------------------------

    variables = {}


    try:

        for column in selected_columns:

            safe_name = mapping[column]


            if not pd.api.types.is_numeric_dtype(
                source_df[column]
            ):

                st.error(
                    f"Column '{column}' is not numeric. "
                    "Please use numeric columns for this calculation."
                )

                st.stop()


            variables[
                safe_name
            ] = pd.to_numeric(
                source_df[column],
                errors="coerce"
            )


        # -------------------------------------------------
        # CALCULATE
        # -------------------------------------------------

        result = safe_calculate(
            converted_formula,
            variables
        )


        # -------------------------------------------------
        # RESULT VALIDATION
        # -------------------------------------------------

        if np.isscalar(result):

            result = pd.Series(
                result,
                index=source_df.index
            )


        result = pd.Series(
            result,
            index=source_df.index
        )


        # -------------------------------------------------
        # SAVE NEW VARIABLE
        # -------------------------------------------------

        calculated_df = (
            source_df.copy()
        )


        calculated_df[
            output_name
        ] = result


        # -------------------------------------------------
        # STORE IN SESSION
        # -------------------------------------------------

        st.session_state.calculated_df = (
            calculated_df
        )

        st.session_state.calculation_info = {

            "formula": formula,

            "converted_formula":
                converted_formula,

            "new_variable":
                output_name,

            "selected_columns":
                selected_columns.copy()

        }


        st.success(
            f"Calculation completed successfully. "
            f"New variable '{output_name}' "
            f"has been created for "
            f"{len(calculated_df):,} rows."
        )


    except ZeroDivisionError:

        st.error(
            "The formula contains division by zero."
        )


    except Exception as e:

        st.error(
            f"Could not calculate the formula: {e}"
        )


# =========================================================
# DISPLAY CALCULATION RESULT
# =========================================================

if (
    "calculated_df" in st.session_state
    and st.session_state.calculated_df is not None
):

    calculated_df = (
        st.session_state.calculated_df
    )

    calculation_info = (
        st.session_state.calculation_info
    )


    st.divider()

    st.subheader(
        "5️⃣ Calculation Result"
    )


    # -----------------------------------------------------
    # FORMULA SUMMARY
    # -----------------------------------------------------

    st.markdown(
        "### 📐 Calculation Summary"
    )


    c1, c2 = st.columns(2)


    with c1:

        st.write(
            "**Formula entered:**"
        )

        st.code(
            calculation_info[
                "formula"
            ]
        )


    with c2:

        st.write(
            "**New variable:**"
        )

        st.code(
            calculation_info[
                "new_variable"
            ]
        )


    # -----------------------------------------------------
    # RESULT STATISTICS
    # -----------------------------------------------------

    output_column = (
        calculation_info[
            "new_variable"
        ]
    )


    result_series = (
        calculated_df[
            output_column
        ]
    )


    valid_values = (
        result_series
        .replace(
            [np.inf, -np.inf],
            np.nan
        )
        .dropna()
    )


    r1, r2, r3, r4 = st.columns(4)


    r1.metric(
        "Rows",
        f"{len(calculated_df):,}"
    )


    r2.metric(
        "Valid Results",
        f"{len(valid_values):,}"
    )


    r3.metric(
        "Missing Results",
        f"{result_series.isna().sum():,}"
    )


    if len(valid_values) > 0:

        r4.metric(
            "Mean",
            f"{valid_values.mean():,.4f}"
        )

    else:

        r4.metric(
            "Mean",
            "N/A"
        )


    # -----------------------------------------------------
    # PREVIEW
    # -----------------------------------------------------

    st.markdown(
        "### 👀 Preview"
    )


    st.dataframe(
        calculated_df,
        use_container_width=True,
        height=450
    )


    # -----------------------------------------------------
    # DOWNLOAD
    # -----------------------------------------------------

    st.divider()

    st.subheader(
        "6️⃣ Download Calculated Dataset"
    )


    csv_data = (
        calculated_df
        .to_csv(
            index=False
        )
        .encode("utf-8")
    )


    summary_df = pd.DataFrame(
        [
            [
                "Formula",
                calculation_info["formula"]
            ],

            [
                "New Variable",
                output_column
            ],

            [
                "Rows",
                len(calculated_df)
            ],

            [
                "Valid Results",
                len(valid_values)
            ],

            [
                "Missing Results",
                int(
                    result_series.isna().sum()
                )
            ],

            [
                "Mean",
                (
                    valid_values.mean()
                    if len(valid_values) > 0
                    else np.nan
                )
            ],

            [
                "Minimum",
                (
                    valid_values.min()
                    if len(valid_values) > 0
                    else np.nan
                )
            ],

            [
                "Maximum",
                (
                    valid_values.max()
                    if len(valid_values) > 0
                    else np.nan
                )
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

        calculated_df.to_excel(
            writer,
            index=False,
            sheet_name="Calculated Data"
        )

        summary_df.to_excel(
            writer,
            index=False,
            sheet_name="Calculation Summary"
        )


    excel_output.seek(0)


    d1, d2 = st.columns(2)


    with d1:

        st.download_button(
            label=(
                "⬇️ Download CSV"
            ),

            data=csv_data,

            file_name=(
                "calculated_data.csv"
            ),

            mime="text/csv",

            use_container_width=True
        )


    with d2:

        st.download_button(
            label=(
                "⬇️ Download Excel"
            ),

            data=excel_output.getvalue(),

            file_name=(
                "calculated_data.xlsx"
            ),

            mime=(
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            ),

            use_container_width=True
        )


# =========================================================
# SUPPORTED OPERATIONS
# =========================================================

st.divider()


with st.expander(
    "📚 Supported Mathematical Operations",
    expanded=False
):

    st.markdown(
        """
### Operators

| Operator | Meaning |
|---|---|
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |
| `**` | Power |
| `%` | Modulo |
| `( )` | Grouping |

### Functions

| Function | Example |
|---|---|
| `abs()` | `abs(Profit)` |
| `round()` | `round(GDP, 2)` |
| `sqrt()` | `sqrt(GDP)` |
| `log()` | `log(GDP)` |
| `log10()` | `log10(GDP)` |
| `exp()` | `exp(GDP)` |

"""
    )


# =========================================================
# VERSION STATUS
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
        "🔄 V5.2 — User-Defined Data Calculation"
    )

    st.write(
        "⏳ V5.3 — Data Aggregation / Processing"
    )

    st.write(
        "⏳ V5.4 — Advanced Export"
    )