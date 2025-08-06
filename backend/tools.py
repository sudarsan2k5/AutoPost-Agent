import requests
import tweepy
import openai
from config import LINKEDIN_ACCESS_TOKEN, LINKEDIN_PERSON_URN, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, OPENAI_API_KEY

def generate_social_content(topic: str, platform: str) -> str:
    """Generate engaging social media content using AI"""
    if platform.lower() == "linkedin":
        prompt = f"""
        Create an engaging LinkedIn post about {topic}.
        Requirements:
        - Professional yet engaging tone
        - Include valuable insights or tips
        - Add relevant hashtags (3-5)
        - Include a call-to-action
        - Keep it under 1000 characters
        - Make it thought-provoking
        """
    elif platform.lower() == "twitter":
        prompt = f"""
        Create an engaging Twitter post about {topic}.
        Requirements:
        - Catchy and concise
        - Include relevant hashtags (2-3)
        - Keep it under 280 characters
        - Make it shareable and engaging
        - Add a hook or interesting angle
        """
    else:
        prompt = f"Create an engaging social media post about {topic}."
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a social media expert who creates engaging, viral-worthy content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating content: {str(e)}"


# Setup LinkedIn API
def call_linkedin(topic: str) -> str:
    """ Generate and post to Linkedin """
    try:
        content = generate_social_content(topic, "linkedin")
        print(f"Generated LinkedIn post: {content}")

        # LinkedIn API posting Setup
        url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        data = {
            "author": LINKEDIN_PERSON_URN,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": content
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 201:
            return f" Successfully posted to your LinkedIn account ✅"
        else:
            return f"Failed to post to your LinkedIn Account ⚠️"
    except Exception as e:
        return f"Generated content but failed to post to LinkedIn"
    
# Setup Twitter API

def call_twitter(topic: str) -> str:
    """Generate and post content to Twitter"""
    try:
        content = generate_social_content(topic, "twitter")
        print(f"Generated Twitter post: {content}")
        # Setup Twitter API posting
        client = tweepy.Client(
            consumer_key=TWITTER_CONSUMER_KEY,
            consumer_secret=TWITTER_CONSUMER_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
        )

        # Post to Twitter
        response = client.create_tweet(text=content)
        return f"Successfully posted to your Twitter account ✅"
    except Exception as e:
        return f"Generated content but failed to post to Twitter ⚠️"