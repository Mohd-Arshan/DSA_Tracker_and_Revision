from django.utils.timezone import localdate
from datetime import timedelta
import math

time_difificulty_score_mapping = {
    'Easy': 15,
    'Medium': 30,
    'Hard': 60
}

mistake_score_mapping = {
    'edge_case': 5,
    'implementation': 2,
    'logical': 15,
    'optimization': 10,
}   

def getScore(status,hintCount,mistakes,timeTaken,difficulty):
    '''Calculates the score based on the status, hint count, mistakes, time taken, and difficulty.'''
    
    base_score = 100
    mistakes = mistakes or []
    
    if status == 'solved_with_hint':
        base_score -= min(hintCount * 5, 20) # Maximum hint penalty is 20 points
    elif status == 'solved_with_editorial': 
        base_score -= 40
        
        
    for key,value in mistakes.items():
        if value:
            base_score -= mistake_score_mapping.get(key, 0)
        
    
    expected_time = timedelta(minutes = time_difificulty_score_mapping[difficulty]) 
    if timeTaken > expected_time:
        time_penalty = (timeTaken - expected_time).total_seconds() / 60
        base_score -= min(time_penalty * 0.4, 20) # Maximum time penalty is 20 points
    
    return base_score

def growthFactor(score):
    if score >= 90:
        return 3.0
    elif score >= 80:
        return 2.5
    elif score >= 70:
        return 2.0
    elif score >= 60:
        return 1.5
    else:
        return 0.7
    
def getStability(avgScore,Score, stability):
    '''Calculates the stability of a problem based on the average score, the current score, and the previous stability. 
    The stability is calculated as the product of the previous stability and a multiplier based on the current score and the average score. 
    The multiplier is calculated using a growth factor function that returns a value based on the current score. 
    If the current score is less than the average score, the multiplier is capped at 0.9 to prevent the stability from decreasing too quickly.'''
    
    effectiveScore = Score
    
    if avgScore != 0:
        effectiveScore  = 0.7 * Score + 0.3 * avgScore
        
    multiplier = growthFactor(effectiveScore)
    
    if Score < avgScore:
        multiplier = min(multiplier, 0.9)
        
    return stability * multiplier
        
        

def nextRevisionDays(stability):
    '''Calculates the number of days until the next revision based on the stability.'''
    return min(180,max(1,math.ceil(-1 * stability * math.log(0.85)))) # Assuming a retention rate of 85%

    

    
    