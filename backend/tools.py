import requests

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