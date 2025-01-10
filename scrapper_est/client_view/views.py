from django.shortcuts import render, redirect
from admin_scraper.models import MainTable
from .models import ScrappingToBe


def view_data(request):
    company = request.GET.get("company", "")
    address = request.GET.get("address", "")
    visited_filter = request.GET.get("visited", "All")  # Default filter to "All"
    
    # Fetch data based on search query
    results = MainTable.objects.all()

    # Apply filters if any are provided
    if company:
        results = results.filter(keyword__icontains=company)
    
    if address:
        results = results.filter(state__icontains=address)

    # Apply visited status filter
    if visited_filter == "Visited":
        results = results.filter(visited=True)
    elif visited_filter == "NotVisited":
        results = results.filter(visited=False)

    if not results.exists():
        # Check if the keyword and state tuple already exists in the 'ScrappingToBe' table
        if not ScrappingToBe.objects.filter(keyword=company, state=address).exists():
            # If no such entry exists, add it to 'ScrappingToBe'
            ScrappingToBe.objects.create(keyword=company, state=address)
        return render(request, "client_view/nodata.html")

    # If data exists, render the view with the results
    return render(request, "client_view/view_data.html", {"results": results, "visited_filter": visited_filter})



def update_visited(request, record_id):
    try:
        # Get the corresponding record
        record = MainTable.objects.get(id=record_id)

        if request.method == "POST":
            # Update the 'visited' field based on the checkbox status
            visited_status = request.POST.get('visited', 'off') == 'on'
            record.visited = visited_status
            record.save()

    except MainTable.DoesNotExist:
        # Handle the case where the record doesn't exist
        return redirect('client_view:view_data')

    # Redirect back to the data view after updating
    return redirect('client_view:view_data')
