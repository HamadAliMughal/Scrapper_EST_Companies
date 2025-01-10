import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import pandas as pd

# Function to fetch search results with pagination
def get_search_results(keyword, state, max_results=20):
    """Fetch search results using Google Custom Search API with pagination."""
    api_key = "AIzaSyAzqQLW_dVIlZck6OZs_jPSCH2V40Inf8I"  # Replace with your API key
    cse_id = "a3aa742eaa7154b6f"  # Replace with your Custom Search Engine ID
    search_query = f"{keyword} in {state} USA"
    all_links = []
    start_index = 1

    while len(all_links) < max_results:
        url = f"https://www.googleapis.com/customsearch/v1?q={search_query}&key={api_key}&cx={cse_id}&start={start_index}"
        print(f"Fetching: {url}")
        response = requests.get(url)
        if response.status_code != 200:
            print("Failed to fetch search results from API")
            break
        
        data = response.json()
        items = data.get("items", [])
        if not items:
            break
        
        links = [item["link"] for item in items]
        all_links.extend(links)
        start_index += 10  # Move to the next page of results

        # Stop if we reach the maximum desired results
        if len(all_links) >= max_results:
            break
    
    return all_links[:max_results]  # Return only the requested number of results


# Function to extract contact information (emails and phones) from the provided text using regex
def extract_contact_info(text):
    """Extract emails and phone numbers from the provided text using regex."""
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    phones = re.findall(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
    return list(set(emails)), list(set(phones))

# Function to prioritize contact/about pages and crawl the site
def scrape_contact_info(url, max_crawl=20):
    """Crawl a website and extract contact information."""
    visited = set()
    links_to_visit = [url]
    all_emails = []
    all_phones = []
    visited.add(url)
    crawl_count = 0

    # Keywords to prioritize contact or about pages
    contact_keywords = ['contact', 'about', 'contact-us', 'about-us']

    while links_to_visit and crawl_count < max_crawl:
        current_url = links_to_visit.pop(0)
        print(f"Visiting: {current_url}")
        try:
            response = requests.get(current_url, timeout=10)
            if response.status_code != 200:
                continue
            
            # Parse the HTML content
            print(current_url,'The url is here')
            soup = BeautifulSoup(response.text, "html.parser")
            page_text = soup.get_text()
            
            # Extract emails and phones from the page text
            emails, phones = extract_contact_info(page_text)
            all_emails.extend(emails)
            all_phones.extend(phones)

            # Stop crawling if 5 emails are found
            if len(all_emails) >= 5:
                print(f"5 emails found, stopping crawl for {current_url}")
                break

            # Find links to visit next, prioritize contact/about pages
            new_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(current_url, href)
                
                # Check if the link contains contact/about keywords
                if any(keyword in full_url.lower() for keyword in contact_keywords):
                    new_links.insert(0, full_url)  # Prioritize contact/about pages

                # Add valid links to the crawl queue (same domain, not visited)
                elif urlparse(full_url).netloc == urlparse(url).netloc and full_url not in visited:
                    new_links.append(full_url)

            links_to_visit.extend(new_links)
            visited.update(new_links)

            crawl_count += 1

        except Exception as e:
            print(f"Error scraping {current_url}: {e}")

    return list(set(all_emails)), list(set(all_phones))

def main():
    # Input keywords and state
    keyword = input("Enter the type of company to search for (e.g., estimation companies): ")
    state = input("Enter the U.S. state: ")
    
    # Fetch search results with pagination
    print("\nFetching search results...")
    links = get_search_results(keyword, state, max_results=20)
    
    # Scrape contact information for each link
    data = []
    for link in links:
        print(f"\nScraping: {link}")
        emails, phones = scrape_contact_info(link)
        
        # Collect the data for the current company
        data.append({
            "Company Name": link,  # Placeholder for company name
            "Emails": emails,
            "Phones": phones,
            "Website": link
        })
    
    # Ensure the 'data' directory exists
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

    # Save to CSV
    if data:
        output_file = os.path.join(output_dir, "output.csv")
        print(f"\nSaving data to {output_file}...")
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
        print("Data saved successfully!")
    else:
        print("No data extracted.")

if __name__ == "__main__":
    main()