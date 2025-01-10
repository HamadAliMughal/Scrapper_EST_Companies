from django.shortcuts import render
from .scrapper import get_search_results, scrape_contact_info
from .models import MainTable
from client_view.models import ScrappingToBe
from django.contrib.auth.decorators import login_required

@login_required
def process_scraper(request):
    if request.method == "POST":
        keywords = request.POST.get("keywords", "").split(",")
        states = request.POST.get("states", "").split(",")
        results = []

        for state in states:
            for keyword in keywords:
                state = state.strip()
                keyword = keyword.strip()

                # Fetch search results
                links = get_search_results(keyword, state, max_results=10)

                for link in links:
                    emails, phones = scrape_contact_info(link)

                    # Check for duplicate entries
                    if not MainTable.objects.filter(
                        keyword=keyword,
                        state=state,
                        website=link
                    ).exists():
                        # Save data to the MainTable if not duplicate
                        MainTable.objects.create(
                            keyword=keyword,
                            state=state,
                            company_name=link,
                            emails=", ".join(emails),
                            phones=", ".join(phones),
                            website=link
                        )

                        # Append data to results for displaying on the page
                        results.append({
                            "Company_Name": link,
                            "Emails": emails,
                            "Phones": phones,
                            "Website": link,
                            "Address": state,
                            "Company": keyword
                        })

        return render(request, "admin_scraper/results.html", {"results": results})

    # Render the form with entries from ScrappingToBe
    
    return render(request, "admin_scraper/form.html", {
        "scrapping_to_be_entries": ScrappingToBe.objects.all()
    })
    

def start_scraping(request):
    # Fetch a tuple from ScrappingToBe that needs scraping
    tuple_to_scrape = ScrappingToBe.objects.first()

    if tuple_to_scrape:
        # Perform scraping with the tuple
        keyword = tuple_to_scrape.keyword
        state = tuple_to_scrape.state
        links = get_search_results(keyword, state, max_results=10)

        for link in links:
            emails, phones = scrape_contact_info(link)

            # Save the data to MainTable
            MainTable.objects.create(
                keyword=keyword,
                state=state,
                company_name=link,
                emails=", ".join(emails),
                phones=", ".join(phones),
                website=link
            )

        # After scraping, delete the tuple from ScrappingToBe
        tuple_to_scrape.delete()

    return render(request, "admin_scraper/form.html", {
        "scrapping_to_be_entries": ScrappingToBe.objects.all()
    })
