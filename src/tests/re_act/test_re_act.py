import os
import unittest
from unittest.mock import patch, MagicMock

from agent.re_act.utils import search

class TestSearchAction(unittest.TestCase):
    
    @patch('os.getenv')
    def test_search_missing_api_key(self, mock_getenv):
        """测试缺失 API Key 的情况"""
        mock_getenv.return_value = None
        result = search("Python")
        self.assertEqual(result, "错误:SERPAPI_KEY环境变量未设置")

    @patch('os.getenv')
    @patch('agent.re_act.utils.SerpApiClient')
    def test_search_success_with_results(self, mock_serp_client, mock_getenv):
        """测试搜索成功并返回结果的情况"""
        mock_getenv.return_value = "fake_key"
        # 模拟 SerpApi 返回的典型字典结构
        mock_instance = mock_serp_client.return_value
        mock_instance.get_dict.return_value = {
            "organic_results": [
                {"snippet": "Python 是一种编程语言。"}
            ]
        }
        
        result = search("Python")
        self.assertIn("Python 是一种编程语言", result)

    @patch('os.getenv')
    @patch('agent.re_act.utils.SerpApiClient')
    def test_search_answer_box(self, mock_serp_client, mock_getenv):
        """测试返回 answer_box 的情况"""
        mock_getenv.return_value = "fake_key"
        mock_instance = mock_serp_client.return_value
        mock_instance.get_dict.return_value = {
            "answer_box": {
                "answer": "Python 是一种解释型语言"
            }
        }
        
        result = search("Python")
        self.assertEqual(result, "Python 是一种解释型语言")

    @patch('os.getenv')
    @patch('agent.re_act.utils.SerpApiClient')
    def test_search_no_results(self, mock_serp_client, mock_getenv):
        """测试未找到结果的情况"""
        mock_getenv.return_value = "fake_key"
        mock_instance = mock_serp_client.return_value
        mock_instance.get_dict.return_value = {}
        
        result = search("NonExistentQuery")
        self.assertEqual(result, "没有查询到关于NonExistentQuery的信息")

    @patch('os.getenv')
    @patch('agent.re_act.utils.SerpApiClient')
    def test_search_exception(self, mock_serp_client, mock_getenv):
        """测试发生异常的情况"""
        mock_getenv.return_value = "fake_key"
        mock_instance = mock_serp_client.return_value
        mock_instance.get_dict.side_effect = Exception("API Error")
        
        result = search("Python")
        self.assertIn("错误:查询时遇到问题: API Error", result)

if __name__ == "__main__":
    unittest.main()