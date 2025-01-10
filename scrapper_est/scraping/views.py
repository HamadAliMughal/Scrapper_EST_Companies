# scraper/views.py

from django.shortcuts import render
from .models import Company
from .scrapper import get_search_results, scrape_contact_info
import asyncio
from asgiref.sync import sync_to_async
from django.db import DatabaseError, OperationalError

@sync_to_async
def fetch_or_scrape_data(keyword, state):
    try:
        
        companies = Company.objects.filter(keyword=keyword, state=state)
        if companies.exists():
            return list(companies.values())  
    except (DatabaseError, OperationalError) as e:
        
        if "no such table" in str(e):
            print("Table does not exist. Proceeding to scrape data...")
        else:
            raise e  
    
    links = get_search_results(keyword, state, max_results=20)
    data = []
    for link in links:
        emails, phones = scrape_contact_info(link)
        company_data = {
            "Company_Name": link,
            "Emails": emails[:5],  # Slice the first 5 emails
            "Phones": phones[:5],  # Slice the first 5 phones
            "Website": link
        }

        # Save unique data in the database
        try:
            company, created = Company.objects.get_or_create(
                keyword=keyword,
                state=state,
                Company_Name=company_data['Company_Name'],  # Corrected field name
                defaults={
                    "Emails": company_data['Emails'],  # Ensure correct field name
                    "Phones": company_data['Phones'],  # Ensure correct field name
                    "Website": company_data['Website']  # Ensure correct field name
                }
            )
        except (DatabaseError, OperationalError) as e:
            print(f"Error saving data: {e}")

        data.append(company_data)
    
    return data  # Return newly scraped data


# The index view (search form page)
async def index(request):
    if request.method == "POST":
        keyword = request.POST.get("keyword")
        state = request.POST.get("state")

        try:
            # Fetch data either from the database or scrape it asynchronously
            data = await fetch_or_scrape_data(keyword, state)
        except Exception as e:
            print(f"An error occurred: {e}")
            data = []  # Return empty data in case of unexpected errors

        return render(request, 'scraper/results.html', {'data': data})

    return render(request, 'scraper/index.html')
