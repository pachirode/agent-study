import pytest
import os
import requests
from unittest.mock import patch, MagicMock
from agent.travel.travel_agent import get_weather, get_attraction, get_system_prompt, OpenAIClient, main

# Test get_weather
def test_get_weather_success():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'current_condition': [{
                'weatherDesc': [{'value': 'Sunny'}],
                'temp_C': '25'
            }]
        }
        mock_get.return_value = mock_response
        
        result = get_weather("Shanghai")
        assert "Shanghai当前天气:Sunny，气温25摄氏度" in result

def test_get_weather_failure():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        result = get_weather("Shanghai")
        assert "错误:查询天气时遇到网络问题" in result

# Test get_attraction
def test_get_attraction_no_api_key():
    with patch('os.getenv') as mock_getenv:
        mock_getenv.side_effect = lambda key: None if key == "TAVILY_API_KEY" else "other_value"
        result = get_attraction("Shanghai", "Sunny")
        assert "错误:TAVILY_API_KEY环境变量未设置" in result

def test_get_attraction_success():
    with patch('os.getenv') as mock_getenv:
        mock_getenv.side_effect = lambda key: "fake_tavily_key" if key == "TAVILY_API_KEY" else "other_value"
        with patch('agent.travel.travel_agent.TavilyClient') as mock_tavily:
            mock_client = MagicMock()
            mock_tavily.return_value = mock_client
            mock_client.search.return_value = {
                "answer": "The Bund is a great place to visit in Sunny weather."
            }
            
            result = get_attraction("Shanghai", "Sunny")
            assert "The Bund is a great place to visit" in result

# Test get_system_prompt
def test_get_system_prompt():
    with patch('builtins.open', MagicMock()) as mock_open_func:
        mock_f = MagicMock()
        mock_f.read.return_value = "system prompt content"
        mock_open_func.return_value.__enter__.return_value = mock_f
        
        result = get_system_prompt("fake_path")
        assert result == "system prompt content"

# Test OpenAIClient
def test_openai_client_generate():
    with patch('agent.travel.travel_agent.OpenAI') as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="LLM response"))]
        mock_client.chat.completions.create.return_value = mock_response
        
        client = OpenAIClient("model", "api_key", "base_url")
        result = client.generate("user prompt", "system prompt")
        assert result == "LLM response"

# Test main (basic run)
def test_main_runs():
    with patch('agent.travel.travel_agent.OpenAIClient.generate') as mock_generate, \
         patch('agent.travel.travel_agent.get_system_prompt') as mock_get_prompt, \
         patch('agent.travel.travel_agent.get_weather') as mock_weather:
        
        mock_get_prompt.return_value = "System prompt"
        mock_weather.return_value = "Shanghai is Sunny"
        
        # Mocking the sequence of LLM responses to simulate a full interaction
        mock_generate.side_effect = [
            "Thought: I need to check weather. Action: get_weather(city=\"Shanghai\")",
            "Thought: I have the weather. Action: Finish[Shanghai is nice and sunny!]"
        ]
        
        # We need to update the tools dict with our mock because it was populated at import time
        from agent.travel.travel_agent import tools
        original_weather = tools["get_weather"]
        tools["get_weather"] = mock_weather
        
        try:
            # Suppress prints for clean test output
            with patch('builtins.print'):
                main()
        finally:
            # Restore original tool
            tools["get_weather"] = original_weather
            
        assert mock_generate.call_count == 2
        mock_weather.assert_called_once_with(city="Shanghai")
