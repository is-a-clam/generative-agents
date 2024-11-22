import enum

class State(enum.Enum):
    SUSCEPTIBLE = 0
    INFECTED = 1
    RECOVERED = 2

def find_grid_dimensions(total):
    for i in range(int(total**0.5), 1, -1):
        if total % i == 0:
            return i, total // i
    return 1, total

def generate_traits(random):
    agreeableness_pos = ['Cooperation', 'Amiability', 'Empathy', 'Leniency', 'Courtesy', 'Generosity', 'Flexibility', 'Modesty', 'Morality', 'Warmth', 'Earthiness', 'Naturalness']
    agreeableness_neg = ['Belligerence', 'Overcriticalness', 'Bossiness', 'Rudeness', 'Cruelty', 'Pomposity', 'Irritability', 'Conceit', 'Stubbornness', 'Distrust', 'Selfishness', 'Callousness']
    # Did not use Surliness, Cunning, Predjudice,Unfriendliness,Volatility, Stinginess

    conscientiousness_pos = ['Organization', 'Efficiency', 'Dependability', 'Precision', 'Persistence', 'Caution', 'Punctuality', 'Punctuality', 'Decisiveness', 'Dignity']
    # Did not use Predictability, Thrift, Conventionality, Logic
    conscientiousness_neg = ['Disorganization', 'Negligence', 'Inconsistency', 'Forgetfulness', 'Recklessness', 'Aimlessness', 'Sloth', 'Indecisiveness', 'Frivolity', 'Nonconformity']

    surgency_pos = ['Spirit', 'Gregariousness', 'Playfulness', 'Expressiveness', 'Spontaneity', 'Optimism', 'Candor'] 
    # Did not use Humor, Self-esteem, Courage, Animation, Assertion, Talkativeness, Energy level, Unrestraint
    surgency_neg = ['Pessimism', 'Lethargy', 'Passivity', 'Unaggressiveness', 'Inhibition', 'Reserve', 'Aloofness'] 
    # Did not use Shyness, Silenece

    emotional_stability_pos = ['Placidity', 'Independence']
    emotional_stability_neg = ['Insecurity', 'Emotionality'] 
    # Did not use Fear, Instability, Envy, Gullibility, Intrusiveness
    
    intellect_pos = ['Intellectuality', 'Depth', 'Insight', 'Intelligence'] 
    # Did not use Creativity, Curiousity, Sophistication
    intellect_neg = ['Shallowness', 'Unimaginativeness', 'Imperceptiveness', 'Stupidity']

    return [
        random.choice(agreeableness_pos + agreeableness_neg),
        random.choice(conscientiousness_pos + conscientiousness_neg),
        random.choice(surgency_pos + surgency_neg),
        random.choice(emotional_stability_pos + emotional_stability_neg),
        random.choice(intellect_pos + intellect_neg)
    ]

def chain_print(input):
    print(input)
    return input