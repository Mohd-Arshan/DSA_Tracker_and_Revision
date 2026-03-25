import requests
import json


def get_leetcode_question_info(question_number):
    # Check if we have the slug in our map
        # If not, fetch dynamically from problems API
    problems_url = "https://leetcode.com/api/problems/all/"
    problems_response = requests.get(problems_url)
    problems_data = problems_response.json()
    title_slug = None
    for problem in problems_data['stat_status_pairs']:  
        if problem['stat']['frontend_question_id'] == question_number:
            title_slug = problem['stat']['question__title_slug']
            break
    if not title_slug:
        return {"error": "Question number not found"}
    
    
    # GraphQL query for the info we want
    url = "https://leetcode.com/graphql"
    
    query = """
    query getQuestionDetail($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        title
        difficulty
        topicTags {
          name
        }
      }
    }
    """
    
    response = requests.post(url, json={
        "query": query,
        "variables": {"titleSlug": title_slug}
    })
    
    data = response.json()
    
    if 'data' in data and data['data'] and 'question' in data['data']:
        q = data['data']['question']
        return {
            "leetcode_number": question_number,
            "title": q['title'],
            "difficulty": q['difficulty'],
            "patterns": [tag['name'] for tag in q['topicTags']],
            "url": f"https://leetcode.com/problems/{title_slug}/"
        }
    
    return data
