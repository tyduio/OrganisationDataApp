import streamlit as st


st.title("👋 Welcome to Organisation Data Processing System")

st.caption("Important information for all system users")


# =========================================================
# IMPORTANT INFORMATION
# =========================================================

st.warning(
    """
    ⚠️ IMPORTANT INFORMATION FOR USERS

    Your work in this system is currently session-based.

    The system is still under backend development and does not
    currently provide permanent storage of your previous tasks
    under a personal user account.

    If you leave the system, close the browser, restart the session,
    or your session expires, you may not be able to recover your
    previous work automatically.
    """
)


# =========================================================
# APOLOGY
# =========================================================

st.subheader("🙏 We Are Sorry for This Limitation")

st.write(
    """
    We sincerely apologize for this limitation.

    The system is still being improved, especially on the backend
    side where permanent storage, user accounts, saved projects,
    and recovery of previous work are being developed.

    Until these features are available, we strongly recommend that
    you download every important file, dataset, analysis result,
    calculation result, extraction result, or other information
    that you may need before leaving the system.
    """
)


# =========================================================
# IMPORTANT ADVICE
# =========================================================

st.info(
    """
    💡 IMPORTANT ADVICE

    Please download and keep all important results before leaving
    the system.

    If you leave without saving or downloading your work and the
    session is lost, you may need to start again from the beginning
    by uploading and processing your data again.
    """
)


# =========================================================
# BEFORE YOU LEAVE
# =========================================================

st.subheader("📌 Before You Leave the System")

st.write(
    """
    Please make sure that you have downloaded everything important
    from your current work, including:
    """
)

st.markdown(
    """
    - 📂 Important datasets
    - 🧹 Cleaned data
    - 📊 Statistical analysis results
    - 📈 Important visualization results
    - 🧮 Calculated data
    - 🔎 Extracted data
    - 📄 Reports and other important results
    """
)


# =========================================================
# SYSTEM WORKFLOW
# =========================================================

st.divider()

st.subheader("🔄 Current System Workflow")

st.markdown(
    """
    Upload Data
        ↓
    Clean Data
        ↓
    Analyze Data
        ↓
    Visualize Data
        ↓
    Extract Data
        ↓
    Calculate Data
        ↓
    Extract Calculated Data
        ↓
    Download Important Results
    """
)


# =========================================================
# ABOUT DEVELOPERS
# =========================================================

st.divider()

st.subheader("👨‍💻 Developers")

st.write(
    """
    Would you like to know more about the developers behind
    this Organisation Data Processing System?
    """
)

if st.button(
    "👨‍💻 About Developers",
    use_container_width=True
):
    st.switch_page("pages/developers.py")


# =========================================================
# FINAL MESSAGE
# =========================================================

st.divider()

st.success(
    """
    🎉 Thank you for using the Organisation Data Processing System.

    We appreciate your patience and understanding while the system
    continues to be improved.

    Please remember to download your important work before leaving.
    """
)