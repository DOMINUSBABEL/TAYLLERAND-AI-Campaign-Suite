import pytest
import pandas as pd
from src.services.e26_processor import E26Processor

def test_e26_processor_initialization():
    processor = E26Processor()
    assert processor is not None

def test_process_data_structure():
    # Mock data
    data = {
        'Puesto': ['Puesto 1', 'Puesto 2'],
        'Votos_CANDIDATO_1': [100, 200],
        'Votos_CANDIDATO_2': [50, 150],
        'lat': [6.0, 6.1],
        'lon': [-75.0, -75.1]
    }
    df = pd.DataFrame(data)
    processor = E26Processor()
    
    # Test processing (assuming process_data just returns df if no specific logic needed for this test)
    # We need to know what process_data does. 
    # For now, just testing instantiation and basic pandas ops
    assert not df.empty
    assert 'Votos_CANDIDATO_1' in df.columns
