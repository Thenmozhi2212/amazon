import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# -------------------------------
# Recommendation function (memory-efficient)
# -------------------------------
def get_recommendations(df, cluster_labels, track_idx=None, label=None, 
                        features=['danceability','energy','valence','tempo'], 
                        mode="similar", n=5):
    X = df[features].values

    if mode == "similar":
        if track_idx is None:
            raise ValueError("Provide a track_idx for 'similar' mode.")
        target = X[track_idx].reshape(1, -1)
        sim_scores = cosine_similarity(target, X)[0]
        top_idx = np.argsort(sim_scores)[::-1][1:n+1]
        recs = df.iloc[top_idx][['name_song','name_artists','cluster','Cluster_Label'] + features]
        return recs.reset_index(drop=True)

    elif mode == "cluster":
        if track_idx is None:
            raise ValueError("Provide a track_idx for 'cluster' mode.")
        cluster_id = df.iloc[track_idx]['cluster']
        cluster_songs = df[df['cluster'] == cluster_id].drop(track_idx)
        recs = cluster_songs.sample(min(n, len(cluster_songs)))[['name_song','name_artists','cluster','Cluster_Label'] + features]
        return recs.reset_index(drop=True)

    elif mode == "playlist":
        if label is None:
            raise ValueError("Provide a cluster label for playlist mode.")
        matching_clusters = [c for c, l in cluster_labels.items() if l == label]
        recs = df[df['cluster'].isin(matching_clusters)].sample(n)[['name_song','name_artists','cluster','Cluster_Label'] + features]
        return recs.reset_index(drop=True)


# -------------------------------
# Streamlit UI
# -------------------------------
st.title("🎵 Music Recommendation System (Clustering)")

# Load your dataframe (replace with your CSV or pickle load)
df = pd.read_csv(r"C:\Users\ABC\Desktop\amazon\clustered_songs.csv")  
# columns must include: ['name_song','name_artists','cluster','Cluster_Label', danceability, energy, valence, tempo]

# cluster_labels dictionary from your earlier step
cluster_labels = {
    0: 'Mixed/Other',
    1: 'Happy/Pop',
    2: 'Chill/Acoustic',
    3: 'Party/Dance Songs'
}

st.sidebar.header("Select Recommendation Mode")
mode = st.sidebar.radio("Mode", ["similar", "cluster", "playlist"])

if mode == "similar":
    st.subheader("🎧 Find Similar Songs")
    song_list = df['name_song'].tolist()
    selected_song = st.selectbox("Choose a song:", song_list)
    n = st.slider("Number of recommendations", 1, 10, 5)
    if st.button("Recommend"):
        track_idx = df[df['name_song'] == selected_song].index[0]
        recs = get_recommendations(df, cluster_labels, track_idx=track_idx, mode="similar", n=n)
        st.write("### Recommended Songs")
        st.dataframe(recs)

elif mode == "cluster":
    st.subheader("🎶 Explore Songs in the Same Cluster")
    song_list = df['name_song'].tolist()
    selected_song = st.selectbox("Choose a song:", song_list)
    n = st.slider("Number of recommendations", 1, 10, 5)
    if st.button("Recommend"):
        track_idx = df[df['name_song'] == selected_song].index[0]
        recs = get_recommendations(df, cluster_labels, track_idx=track_idx, mode="cluster", n=n)
        st.write(f"### Songs from the same cluster ({df.iloc[track_idx]['Cluster_Label']})")
        st.dataframe(recs)

elif mode == "playlist":
    st.subheader("📀 Generate Playlist by Mood")
    selected_label = st.selectbox("Choose cluster label:", list(cluster_labels.values()))
    n = st.slider("Number of songs", 1, 20, 10)
    if st.button("Generate Playlist"):
        recs = get_recommendations(df, cluster_labels, label=selected_label, mode="playlist", n=n)
        st.write(f"### Playlist: {selected_label}")
        st.dataframe(recs)
