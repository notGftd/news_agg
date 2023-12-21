import requests
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from bs4 import BeautifulSoup as BSoup
from news.models import Website1, Website2, Website3

from django.utils import timezone
from datetime import timedelta

requests.packages.urllib3.disable_warnings()

def delete_old_entries(model, days=3):
    cutoff_time = timezone.now() - timedelta(days=days)
    old_entries = model.objects.filter(scraped__lt=cutoff_time)
    old_entries.delete()

def scrape_and_save(url, model):
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}

    delete_old_entries(model, days=3)

    try:
        content = session.get(url, verify=False).content
        soup = BSoup(content, "html.parser")

        if model == Website1:
            # HTML structure tags for Website1
            news = soup.find_all('div', {"class": "blog-pic-wrap"})
        elif model == Website2:
            # HTML structure tags for Website2
            news = soup.find_all('div', {"class": "td-module-thumb"})
        elif model == Website3:
            # HTML structure tags for Website3
            news = soup.find_all('div', {"class": "td-module-thumb"})
        else:
            raise ValueError("Invalid model specified")

        for article in news:
            main = article.find_all('a')[0]
            link = main['href']

            if model == Website1:
                # Get image source for Website1 and Website2
                image_src = str(main.find('img')['src'])
            elif model == Website2:
                image_src = str(main.find('span')['data-img-url'])
            elif model == Website3:
                # Get image source for Website3
                image_style = main.find('span')['style']
                start_index = image_style.index("url('") + len("url('")
                end_index = image_style.index("')", start_index)
                image_src = image_style[start_index:end_index]
            
            title = main['title']

            # Check if a similar entry already exists in the database
            existing_entry = model.objects.filter(title=title).first()

            scraped_time = timezone.now()
            cutoff_time = scraped_time - timedelta(hours=36)

            if existing_entry is None:
                # Create and save a new Headline instance
                new_headline = model(title=title, url=link, image=image_src, scraped=scraped_time)
                new_headline.save()
            else:
                # Update the existing entry if needed
                # For example, it can update the URL or image source if they've changed
                if existing_entry.url != link or existing_entry.image != image_src:
                    existing_entry.url = link
                    existing_entry.image = image_src
                    existing_entry.save()
                    
    except Exception as e:
        print(f"Error scraping data from {url}: {e}")

#Site 1
def scrape1(request):
    url = "https://www.znbc.co.zm/news/"
    scrape_and_save(url, Website1)
    return redirect("site1")

def site1(request):
    cutoff_time = timezone.now() - timedelta(hours=36)
    headlines = Website1.objects.filter(scraped__gte=cutoff_time).order_by("-scraped")
    context = {
        'headlines': headlines,
    }
    return render(request, "site1.html", context)

#Site 2
def scrape2(request):
    url = "https://zambianobserver.com/"
    scrape_and_save(url, Website2)
    return redirect("site2")

def site2(request):
    cutoff_time = timezone.now() - timedelta(hours=36)
    headlines = Website2.objects.filter(scraped__gte=cutoff_time).order_by("-scraped")
    context = {
        'headlines': headlines,
    }
    return render(request, "site2.html", context)

#Site 3
def scrape3(request):
    url = "https://www.lusakatimes.com/"
    scrape_and_save(url, Website3)
    return redirect("site3")

def site3(request):
    cutoff_time = timezone.now() - timedelta(hours=36)
    headlines = Website3.objects.filter(scraped__gte=cutoff_time).order_by("-scraped")
    context = {
        'headlines': headlines,
    }
    return render(request, "site3.html", context)

#Homepage
def home(request):
    cutoff_time = timezone.now() - timedelta(hours=36)
    delete_old_entries(Website1, days=3)
    delete_old_entries(Website2, days=3)
    delete_old_entries(Website3, days=3)

    website1_headlines = Website1.objects.filter(scraped__gte=cutoff_time).order_by("-scraped")[:6]
    website2_headlines = Website2.objects.filter(scraped__gte=cutoff_time).order_by("-scraped")[:6]
    website3_headlines = Website3.objects.filter(scraped__gte=cutoff_time).order_by("-scraped")[:6]

    context = {
        'website1_headlines': website1_headlines,
        'website2_headlines': website2_headlines,
        'website3_headlines': website3_headlines,
    }

    return render(request, 'home.html', context)

class AboutPageView(TemplateView):
    template_name = 'about.html'

def search(request):
    query = request.GET.get('q')  

    if query:
        # Perform search across the three models
        results_website1 = Website1.objects.filter(title__icontains=query)  
        results_website2 = Website2.objects.filter(title__icontains=query)  
        results_website3 = Website3.objects.filter(title__icontains=query)   
        
        context = {
            'results_website1': results_website1,
            'results_website2': results_website2,
            'results_website3': results_website3,
            'query': query,
        }
        return render(request, 'search_results.html', context)
    else:
        return render(request, 'home')
    
def search_results(request):
    query = request.GET.get('q')  

    if query:
        # Perform search across the three models
        results_website1 = Website1.objects.filter(title__icontains=query)  
        results_website2 = Website2.objects.filter(title__icontains=query)  
        results_website3 = Website3.objects.filter(title__icontains=query)  
        
        context = {
            'results_website1': results_website1,
            'results_website2': results_website2,
            'results_website3': results_website3,
            'query': query,
        }
        return render(request, 'search_results.html', context)
    else:
        return render(request, 'search_results.html')