import streamlit as st


# =========================================================
# DEVELOPERS PAGE
# =========================================================

st.title("👨‍💻 About the Developers")

st.caption(
    "Meet the people behind the Organisation Data Processing System"
)


# =========================================================
# INTRODUCTION
# =========================================================

st.markdown(
    """
    ## 🌍 Organisation Data Processing System

    This system is the result of collaboration, shared ideas,
    consultation, academic knowledge, field experience, and
    technical development.

    The three developers presented below are the main references
    for this project.
    """
)

st.info(
    """
    🤝 SPECIAL APPRECIATION

    We sincerely appreciate everyone who contributed ideas,
    suggestions, knowledge, consultation, encouragement and
    field experience during the development of this system.

    Special appreciation goes to the wider Field Student OCGS 2026
    community and all other contributors who supported this project.
    """
)


# =========================================================
# DEVELOPER 1
# =========================================================

st.divider()

st.header("🥇 Developer 1 — Muhammad Muhamed")

col1, col2 = st.columns([1, 2])

with col1:

    st.subheader("📸 Profile Photo")

    st.image(
        "assets/muhammad.jpg",
        caption="Muhammad Muhamed",
        use_container_width=True
    )


with col2:

    st.subheader("👤 About Muhammad Muhamed")

    st.write(
        """
        Muhammad Muhamed is a Data Science student with a strong
        interest in technology, statistics, data analysis and
        software/system development.

        He is particularly interested in applying data and
        technology to practical problems and developing useful
        digital systems.

        His learning and development interests include Python,
        Streamlit, statistical analysis, time-series analysis,
        data visualization and web-based data applications.
        """
    )

    st.markdown("### 🎓 Education & Academic Interests")

    st.write(
        """
        • Data Science student

        • East African Statistical Training Centre (EASTC)

        • Statistics and Data Science

        • Statistical modelling and analysis

        • Time-series analysis

        • Practical application of data
        """
    )

    st.markdown("### 💻 Technical Interests")

    st.write(
        """
        • Python

        • Streamlit

        • Data Analysis

        • Statistical Analysis

        • Data Visualization

        • Time-Series Analysis

        • Web Application Development

        • Database Concepts

        • System Development
        """
    )

    st.markdown("### 🎯 Hobbies & Personal Interests")

    st.write(
        """
        🏊 Swimming

        🎮 Playing Games

        📚 Reading and learning

        🕌 Learning Arabic

        💻 Technology and Programming
        """
    )

    st.markdown("### 📞 Contact")

    st.write("📧 Email: muhsul211@gmail.com")

    st.write("📱 Phone: 0679546473")

    st.write("📱 Phone: 0627730671")


# =========================================================
# DEVELOPER 2
# =========================================================

st.divider()

st.header("🥈 Developer 2 — Abdul-rahman-Simai")

col1, col2 = st.columns([1, 2])

with col1:

    st.subheader("📸 Profile Photo")

    st.image(
        "assets/abdulrahman.jpg",
        caption="Abdul-rahman-Simai",
        use_container_width=True
    )


with col2:

    st.subheader("👤 About Abdul-rahman-Simai")

    st.write(
        """
        Abdul-rahman-Simai is a second-year Data Science student
        with a strong interest in technology and modern digital
        solutions.

        He contributes to the collaborative development process
        through ideas, discussions, academic perspectives and
        shared interest in technology.
        """
    )

    st.markdown("### 🎓 Education")

    st.write(
        """
        • Second-year Data Science student
        """
    )

    st.markdown("### 💡 Interests & Hobbies")

    st.write(
        """
        💻 Technology

        🎬 Watching Movies

        🏊 Swimming

        📊 Data Science
        """
    )

    st.markdown("### 📞 Contact")

    st.write(
        "📱 Phone: 0623963030"
    )


# =========================================================
# DEVELOPER 3
# =========================================================

st.divider()

st.header("🥉 Developer 3 — Abubakar")

col1, col2 = st.columns([1, 2])

with col1:

    st.subheader("📸 Profile Photo")

    st.image(
        "assets/abubakar.jpg",
        caption="Abubakar",
        use_container_width=True
    )


with col2:

    st.subheader("👤 About Abubakar")

    st.write(
        """
        Abubakar is a second-year Data Science student with a
        strong interest in technology, digital innovation and
        practical technological solutions.

        He contributes to the collaborative development process
        through ideas, discussions and shared technical interests.
        """
    )

    st.markdown("### 🎓 Education")

    st.write(
        """
        • Second-year Data Science student
        """
    )

    st.markdown("### 💡 Interests & Hobbies")

    st.write(
        """
        🚶 Walking and travelling

        🎮 Playing Games

        💻 Technology

        📊 Data Science
        """
    )

    st.markdown("### 📞 Contact")

    st.write(
        "📱 Phone: 0654289281"
    )

    st.write(
        "📱 Phone: 0772534844"
    )


# =========================================================
# COLLABORATION
# =========================================================

st.divider()

st.header("🤝 Collaboration & Appreciation")

st.markdown(
    """
    ## 🌟 This Is a Collaborative Achievement

    The Organisation Data Processing System is not presented as
    the work of only three individuals.

    Its development has benefited from consultation, collaborative
    thinking, academic knowledge, field perspectives, technical
    discussions, ideas and suggestions from different contributors.

    The three developers shown on this page are presented as the
    main project references.

    However, we sincerely acknowledge and appreciate everyone who
    contributed to the journey.
    """
)

st.markdown(
    """
    ### ❤️ Special Thanks To

    • 🤝 The consultant who contributed to the development process

    • 🎓 Field Student OCGS 2026

    • 💡 Students and contributors who shared ideas and suggestions

    • 🧑‍🏫 Academic and field contributors

    • 🌍 Everyone who supported this project
    """
)

st.success(
    """
    Every idea, suggestion, discussion and contribution helped
    shape the Organisation Data Processing System.

    To everyone who contributed — THANK YOU! ❤️
    """
)


# =========================================================
# PROJECT VISION
# =========================================================

st.divider()

st.header("🚀 Our Vision")

st.write(
    """
    Our vision is to continue improving the Organisation Data
    Processing System into a reliable, user-friendly and powerful
    platform for data processing, statistical analysis,
    visualization, calculation and data extraction.

    As development continues, the system may introduce more
    advanced backend functionality, permanent storage, improved
    user management and additional analytical capabilities.
    """
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    ### 🌐 Organisation Data Processing System

    **Built through collaboration, learning, innovation and
    shared ideas.**

    *Thank you for being part of the journey.* ❤️
    """
)