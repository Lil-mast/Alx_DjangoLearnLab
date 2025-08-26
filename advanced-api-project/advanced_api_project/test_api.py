import requests
import json

BASE_URL = "http://localhost:8000/api/books/"

def test_filtering():
    """Test various filtering options"""
    print("Testing Filtering...")
    
    # Exact year filter
    response = requests.get(f"{BASE_URL}?publication_year=1997")
    print(f"Exact year filter: {response.status_code}, {len(response.json())} results")
    
    # Range filter
    response = requests.get(f"{BASE_URL}?publication_year__gt=2000&publication_year__lt=2020")
    print(f"Range filter: {response.status_code}, {len(response.json())} results")
    
    # Author name filter
    response = requests.get(f"{BASE_URL}?author_name=rowling")
    print(f"Author name filter: {response.status_code}, {len(response.json())} results")

def test_searching():
    """Test search functionality"""
    print("\nTesting Searching...")
    
    # Basic search
    response = requests.get(f"{BASE_URL}?search=harry")
    print(f"Basic search: {response.status_code}, {len(response.json())} results")
    
    # Author search
    response = requests.get(f"{BASE_URL}?search=rowling")
    print(f"Author search: {response.status_code}, {len(response.json())} results")

def test_ordering():
    """Test ordering functionality"""
    print("\nTesting Ordering...")
    
    # Ascending order
    response = requests.get(f"{BASE_URL}?ordering=title")
    results = response.json()
    print(f"Ascending order: {response.status_code}, first title: {results[0]['title'] if results else 'N/A'}")
    
    # Descending order
    response = requests.get(f"{BASE_URL}?ordering=-publication_year")
    results = response.json()
    print(f"Descending order: {response.status_code}, first year: {results[0]['publication_year'] if results else 'N/A'}")

def test_combined():
    """Test combined parameters"""
    print("\nTesting Combined Parameters...")
    
    # Combined filter, search, and order
    response = requests.get(f"{BASE_URL}?publication_year__gt=1990&search=harry&ordering=-publication_year")
    print(f"Combined parameters: {response.status_code}, {len(response.json())} results")

if __name__ == "__main__":
    test_filtering()
    test_searching()
    test_ordering()
    test_combined()