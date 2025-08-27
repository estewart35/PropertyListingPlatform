from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Listing, ListingImage
from .forms import ListingForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    return render(request, 'plp_listings/home.html')


def all_listings(request):
    listings = Listing.objects.all()

    # Get filters from GET parameters
    location = request.GET.get('location')
    property_type = request.GET.get('property_type')
    min_bedrooms = request.GET.get('min_bedrooms')
    min_bathrooms = request.GET.get('min_bathrooms')
    max_price = request.GET.get('max_price')

    # Apply filters
    if location:
        listings = listings.filter(location__icontains=location)
    if property_type:
        listings = listings.filter(property_type__icontains=property_type)
    if min_bedrooms:
        listings = listings.filter(bedrooms__gte=min_bedrooms)
    if min_bathrooms:
        listings = listings.filter(bathrooms__gte=min_bathrooms)
    if max_price:
        listings = listings.filter(price__lte=max_price)

    paginator = Paginator(listings, 9)
    page = request.GET.get('page')
    listings = paginator.get_page(page)

    return render(request, 'plp_listings/all_listings.html', {'listings': listings})

@login_required
def your_listings(request):
    listings = Listing.objects.filter(owner=request.user)

    # Get filters from GET parameters
    location = request.GET.get('location')
    property_type = request.GET.get('property_type')
    min_bedrooms = request.GET.get('min_bedrooms')
    min_bathrooms = request.GET.get('min_bathrooms')
    max_price = request.GET.get('max_price')

    # Apply filters
    if location:
        listings = listings.filter(location__icontains=location)
    if property_type:
        listings = listings.filter(property_type__icontains=property_type)
    if min_bedrooms:
        listings = listings.filter(bedrooms__gte=min_bedrooms)
    if min_bathrooms:
        listings = listings.filter(bathrooms__gte=min_bathrooms)
    if max_price:
        listings = listings.filter(price__lte=max_price)

    paginator = Paginator(listings, 10)
    page = request.GET.get('page')
    listings = paginator.get_page(page)

    return render(request, 'plp_listings/your_listings.html', {'listings': listings})


def listing_details(request, id):
    listing = get_object_or_404(Listing, pk=id)
    images = listing.images.all()
    return render(request, 'plp_listings/listing_details.html', {'listing': listing, 'images': images})


@login_required
def new_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user  # Set the owner to the current user
            listing.save()

            # Handle multiple images
            images = request.FILES.getlist('images')
            for image in images:
                ListingImage.objects.create(listing=listing, image=image)

            messages.success(request, "Listing created successfully!")
            return redirect('your_listings')
    else:
        form = ListingForm()
    
    return render(request, 'plp_listings/listing_form.html', {'form': form})


@login_required
def edit_listing(request, id):
    listing = get_object_or_404(Listing, pk=id)

    # Check if the logged-in user is the owner of the listing
    if listing.owner != request.user:
        messages.error(request, "You are not authorized to edit this listing.")
        return redirect('all_listings')

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()

            if request.FILES:
                # Delete images from the filesystem and the database
                for image in listing.images.all():
                    image.image.delete()  # Deletes the file from the filesystem
                    image.delete()        # Deletes the record from the database

                # Handle new images
                images = request.FILES.getlist('images')
                for image in images:
                    ListingImage.objects.create(listing=listing, image=image)

            messages.success(request, "Listing edited successfully!")
            return redirect('your_listings')
    else:
        form = ListingForm(instance=listing)
    
    return render(request, 'plp_listings/listing_form.html', {'form': form, 'listing': listing})


@login_required
def delete_listing(request, id):
    listing = get_object_or_404(Listing, pk=id)

    # Check if the logged-in user is the owner of the listing
    if listing.owner != request.user:
        messages.error(request, "You are not authorized to delete this listing.")
        return redirect('all_listings')

    if request.method == 'POST':
        # Delete associated images from the filesystem
        for image in listing.images.all():
            image.image.delete()  # Deletes the file from the filesystem

        # Delete the listing
        listing.delete()
        messages.success(request, "Listing deleted successfully!")
        return redirect('your_listings')
    
    return render(request, 'plp_listings/listing_delete.html', {'listing': listing})


@login_required
def favorite(request, id):
    listing = get_object_or_404(Listing, pk=id)
    if request.user in listing.favorited_by.all():
        listing.favorited_by.remove(request.user)
        messages.success(request, f"{listing.title} - {listing.location} was unfavorited.")
    else:
        listing.favorited_by.add(request.user)
        messages.success(request, f"{listing.title} - {listing.location} was favorited!")
        
    return redirect('listing_details', id=id)


@login_required
def favorite_listings(request):
    listings = Listing.objects.filter(favorited_by=request.user)

    # Get filters from GET parameters
    location = request.GET.get('location')
    property_type = request.GET.get('property_type')
    min_bedrooms = request.GET.get('min_bedrooms')
    min_bathrooms = request.GET.get('min_bathrooms')
    max_price = request.GET.get('max_price')

    # Apply filters
    if location:
        listings = listings.filter(location__icontains=location)
    if property_type:
        listings = listings.filter(property_type__icontains=property_type)
    if min_bedrooms:
        listings = listings.filter(bedrooms__gte=min_bedrooms)
    if min_bathrooms:
        listings = listings.filter(bathrooms__gte=min_bathrooms)
    if max_price:
        listings = listings.filter(price__lte=max_price)

    paginator = Paginator(listings, 9)
    page = request.GET.get('page')
    listings = paginator.get_page(page)

    return render(request, 'plp_listings/favorite_listings.html', {'listings': listings})
    
