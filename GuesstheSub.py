import random
import time
import praw
from datetime import datetime

reddit = praw.Reddit(
)

SUBREDDITS = ['AskReddit', 'gaming', 'worldnews', 'funny', 'science', 'movies', 'aww']

TARGET_SUBREDDIT = 'GuesstheSubTest'  

today_str = datetime.now().strftime("%Y-%m-%d")

def pick_snippet():
    sub_name = random.choice(SUBREDDITS)
    subreddit = reddit.subreddit(sub_name)
    
    posts = list(subreddit.hot(limit=50))
    post = random.choice(posts)
    
    snippet = post.title
    return snippet, sub_name

def post_challenge(snippet):
    subreddit = reddit.subreddit(TARGET_SUBREDDIT)
    title = "Guess the Subreddit!"
    body = (f"Can you guess which subreddit this post title came from?\n\n"
            f"---\n\n"
            f"> {snippet}\n\n"
            f"Reply with the subreddit name (e.g., AskReddit) in the comments below! Good luck!")
    
    submission = subreddit.submit(title, selftext=body)
    return submission.id

def check_comments(post_id, correct_subreddit):
    submission = reddit.submission(id=post_id)
    submission.comments.replace_more(limit=0)
    
    for comment in submission.comments.list():
        guess = comment.body.strip().lower()
        if guess == correct_subreddit.lower():
            if any(reply.author == reddit.user.me() for reply in comment.replies):
                continue
            
            comment.reply(f"Congrats u/{comment.author}! You guessed correctly! The subreddit was r/{correct_subreddit}.")
            print(f"Winner found: u/{comment.author}")
            return True
    return False

def main():
    snippet, correct_subreddit = pick_snippet()
    print(f"Picked subreddit: {correct_subreddit}")
    print(f"Snippet: {snippet}")
    
    post_id = post_challenge(snippet)
    print(f"Posted challenge with ID: {post_id}")
    
    for _ in range(120):
        if check_comments(post_id, correct_subreddit):
            break
        time.sleep(30)
    else:
        print("No correct guesses this round.")

if __name__ == "__main__":
    main()
