import streamlit as st
import pandas as pd
import praw

# Streamlit app
def main():
    st.title("Reddit scraper")

    # User input for subreddit and search term
    subreddit_name = st.text_input("Enter Subreddit Name:", "chatgpt")
    search_terms = st.text_input("Enter Search Term:", "deepmind")

    # User input for replace_more limit
    replace_more_limit = st.slider("Replace More Limit (replies to comments)", min_value=0, max_value=100, value=0)

    # User input for search results limit
    search_results_limit = st.slider("Search Results Limit (includes comments under the post -no sub comments-)", min_value=1, max_value=100, value=10)

    # Button to trigger data retrieval
    if st.button("Search"):
        # Reddit API credentials
        client_id = "VIwxc27jUvf7aZ_35Ze0Eg"
        client_secret = "7LrJtwi77OZt1QNX5LjcBBINWiaLfA"
        user_agent = "sentiment_analysis by u/Additional-Fact-4810"

        # Reddit authentication
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

        # Retrieve subreddit and search results
        subreddit = reddit.subreddit(subreddit_name)
        results = subreddit.search(query=search_terms, limit=search_results_limit)
        print(f"Retrieved {search_results_limit} Reddit results")

        # Collect data
        data = []
        for post in results:
            post.comments.replace_more(limit=replace_more_limit)
            sorted_comments = sorted(post.comments.list(), key=lambda x: x.score, reverse=True)
            for comment in sorted_comments:
                if not ("[deleted]" in comment.body or comment.author is None):
                    data.append({
                        "Title": post.title,
                        "ID": post.id,
                        "Author": str(post.author),
                        "Score": post.score,
                        "Upvote Ratio": post.upvote_ratio,
                        "Comment Count": post.num_comments,
                        "URL": post.url,
                        "Created": post.created_utc,
                        "Comment Body": comment.body,
                        "Comment Author": str(comment.author),
                        "Comment Score": comment.score
                    })
        print("Collected data")

        # Create DataFrame
        df = pd.DataFrame(data)

        # Display data
        st.subheader("Reddit Data")
        st.dataframe(df)

if __name__ == "__main__":
    main()

