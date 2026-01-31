import streamlit as st
import pysolr
import re
import base64
import time

# Page Config (MUST be first)
st.set_page_config(
    page_title="Movie Search App",
    page_icon="🎬",
    layout="wide"
)

# Splash Page Functions
def get_base64_of_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def show_splash(image_path, duration=3):
    encoded = get_base64_of_image(image_path)
    placeholder = st.empty()
    placeholder.markdown(
        f"""
        <style>
        .splash {{
            background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            text-align: center;
            font-family: Arial, sans-serif;
            backdrop-filter: blur(5px); /* بلور خفيف على الخلفية */
        }}
        h1 {{
            font-size: 60px;
            margin-bottom: 20px;
        }}
        p {{
            font-size: 25px;
        }}
        </style>
        <div class="splash">
            <div>
                <h1>🎬 Welcome to Movie Search App</h1>
                <p>You can search movies by Title, Plot, Director, or Origin/Ethnicity.<br>
                Use the sidebar to enter a keyword and select the fields you want to search in.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    time.sleep(duration)
    placeholder.empty()

# Show Splash Page only once
if "splash_shown" not in st.session_state:
    show_splash(r"C:\Users\hadee\Desktop\IR\Project\photo_2025-03-28_19-27-49.jpg", duration=3)
    st.session_state.splash_shown = True

# Connect to Solr Core
solr = pysolr.Solr('http://localhost:8983/solr/movies', always_commit=True)

# Sidebar - Inputs
st.sidebar.title("🔍 Movie Search Options")

keyword = st.sidebar.text_input("Enter keyword to search:")

# Fields to Search In
search_fields = st.sidebar.multiselect(
    "Select fields to search in:",
    ["Title", "Plot", "Director", "Origin/Ethnicity"],
    default=["Title", "Plot"]
)

# Advanced Filters (Collapsible)
with st.sidebar.expander("Advanced Filters"):
    genres = ["", "comedy", "drama", "romance", "thriller", "anime", "musical comedy", "sci-fi / comedy"]
    genre_filter = st.selectbox("Filter by Genre (optional):", genres)

    use_year_filter = st.checkbox("Use Year Range Filter?", value=False)
    years_options = [str(y) for y in range(1900, 2026)]
    year_range = None
    if use_year_filter:
        year_range = st.select_slider(
            "Select Year Range:",
            options=years_options,
            value=(years_options[60], years_options[-1])
        )

# Number of Results and Columns
num_results = st.sidebar.slider(
    "Number of results to show:",
    1, 1000, 6,
    help="Adjust the number of search results displayed."
)

num_cols = st.sidebar.slider(
    "Number of columns:",
    1, 10, 3,
    help="Adjust the number of columns for displaying results."
)


# Build Solr Query
if keyword:
    query_parts = []
    for field in search_fields:
        solr_field = field.lower().replace("/", "_").replace(" ", "_")
        if field == "Title":
            query_parts.append(f'{solr_field}:"{keyword}"^5')  
            query_parts.append(f"{solr_field}:{keyword}^2")    
        elif field == "Plot":
            # proximity example
            query_parts.append(f'{solr_field}:"{keyword}"~5')  
        elif field in ["Director", "Origin/Ethnicity"]:
            # simple match
            query_parts.append(f"{solr_field}:{keyword}")
    query = " OR ".join(query_parts)
else:
    query = "*:*"

filters = []
if genre_filter:
    filters.append(f"genre:{genre_filter}")

if year_range:  
    filters.append(f"year:[{year_range[0]} TO {year_range[1]}]")

# Execute Search
results = solr.search(query, fq=filters, rows=num_results)

# Highlight Functions - Improved
def highlight_text(text, keywords):
    if not keywords:
        return text
    if isinstance(keywords, str):
        keywords = keywords.split()
    for word in keywords:
        if word.strip() == "":
            continue
        pattern = re.compile(f"({re.escape(word)})", re.IGNORECASE)
        text = pattern.sub(r'<mark>\1</mark>', text)
    return text

def highlight_field(text, keyword):
    return highlight_text(text, keyword)

# Genre Colors & Text Color
genre_colors = {
    "comedy": "#FFFACD",
    "drama": "#E6E6FA",
    "romance": "#FFD1DC",
    "thriller": "#D3D3D3",
    "anime": "#F0FFF0",
    "musical comedy": "#FFE4B5",
    "sci-fi / comedy": "#E0FFFF"
}

def get_text_color(bg_color):
    bg_color = bg_color.lstrip("#")
    r, g, b = int(bg_color[0:2],16), int(bg_color[2:4],16), int(bg_color[4:6],16)
    brightness = (r*299 + g*587 + b*114)/1000
    return "#000000" if brightness > 160 else "#FFFFFF"

# Page Title
st.title("🎬 Movie Search App")
st.write("Search for movies based on selected fields!")

# Show number of results
st.info(f"Found {results.hits} movies matching your query.")

# Display Results
if results.hits > 0:
    cols = st.columns(num_cols)
    for idx, r in enumerate(results):
        col = cols[idx % num_cols]
        genre = r.get('genre', ['N/A'])[0].lower()
        color = genre_colors.get(genre, "#F5F5F5")
        text_color = get_text_color(color)
        title = r.get('title', ['No title'])[0]
        year = r.get('year', ['N/A'])[0]
        plot_text = r.get('plot', ['No plot'])[0]
        director = r.get('director', ['N/A'])[0]
        origin = r.get('origin_ethnicity', ['N/A'])[0]
        poster_url = r.get('poster_url', [None])[0]

        with col:
            st.markdown(
                f"""
                <div style="
                    background-color: {color};
                    color: {text_color};
                    padding: 15px;
                    border-radius: 10px;
                    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
                    margin-bottom: 10px;
                ">
                <h4>🎬 {highlight_field(title, keyword)}</h4>
                <p><strong>Genre:</strong> {genre.title()} | <strong>Year:</strong> {year}</p>
                <p><strong>Director:</strong> {highlight_field(director, keyword)} | <strong>Origin:</strong> {highlight_field(origin, keyword)}</p>
                </div>
                """, unsafe_allow_html=True
            )

            if poster_url:
                st.image(poster_url, use_column_width=True)

            with st.expander("Show Plot"):
                st.markdown(highlight_field(plot_text, keyword), unsafe_allow_html=True)
else:
    st.warning("No results found!")
