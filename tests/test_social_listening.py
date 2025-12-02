import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.social_sentinel import SocialSentinel, VoterProfiler, MatchEngine

def test_voter_profiler():
    print("Testing VoterProfiler...")
    profiler = VoterProfiler()
    
    # Test 1: Security Text
    text_sec = "Necesitamos más policía y seguridad en las calles para combatir el robo."
    sent, vec = profiler.analyze_text(text_sec)
    print(f"Text: {text_sec}\nVector: {vec}")
    assert vec[0] > 0, "Security dimension should be positive"
    
    # Test 2: Social Text
    text_soc = "La salud y la educación son derechos fundamentales para la comunidad."
    sent, vec = profiler.analyze_text(text_soc)
    print(f"Text: {text_soc}\nVector: {vec}")
    assert vec[2] > 0, "Social dimension should be positive"
    print("VoterProfiler Passed!\n")

def test_match_engine():
    print("Testing MatchEngine...")
    matcher = MatchEngine()
    
    # Candidate: Strong Security (0.9), Low Social (0.1)
    cand_vec = [0.9, 0.5, 0.1, 0.8, 0.2]
    
    # Voter 1: Matches Candidate (Security focused)
    voter_match = [0.8, 0.4, 0.2, 0.7, 0.1]
    score_high = matcher.calculate_match(cand_vec, voter_match)
    print(f"High Match Score: {score_high}")
    
    # Voter 2: Opposite (Social focused)
    voter_miss = [0.1, 0.2, 0.9, 0.1, 0.8]
    score_low = matcher.calculate_match(cand_vec, voter_miss)
    print(f"Low Match Score: {score_low}")
    
    assert score_high > score_low, "Matching logic failed: High match should be > Low match"
    print("MatchEngine Passed!\n")

def test_social_sentinel_integration():
    print("Testing SocialSentinel Integration...")
    sentinel = SocialSentinel()
    
    # Test Feed Generation (Simulation Mode)
    df = sentinel.generate_verified_feed()
    print(f"Generated Feed Size: {len(df)}")
    assert not df.empty, "Feed should not be empty"
    assert 'voter_vector' in df.columns, "Feed should have voter_vector"
    
    # Test Matching
    voter_id = df.iloc[0]['user_id']
    cand_vec = [0.5, 0.5, 0.5, 0.5, 0.5]
    match_score = sentinel.match_candidate_to_voter(cand_vec, voter_id)
    print(f"Integration Match Score for {voter_id}: {match_score}")
    assert match_score >= 0, "Match score should be valid"
    print("SocialSentinel Integration Passed!\n")

if __name__ == "__main__":
    test_voter_profiler()
    test_match_engine()
    test_social_sentinel_integration()
    print("ALL TESTS PASSED")
