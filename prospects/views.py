from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Prospect

PROSPECTS_PER_PAGE = 15


def dashboard(request):
    """
    Landing dashboard view — lists all Prospect records in a paginated table grid.
    GET /dashboard/?page=1
    """
    prospect_list = Prospect.objects.all()
    paginator = Paginator(prospect_list, PROSPECTS_PER_PAGE)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'prospects/dashboard.html', {
        'prospects': page_obj,
        'page_obj': page_obj,
        'total_count': paginator.count,
        'page_title': 'Prospect Dashboard',
    })


def prospect_form(request, pk=None):
    """
    Unified form router — handles both CREATE and UPDATE.
    GET  /dashboard/create/          → blank form (new record)
    GET  /dashboard/edit/<pk>/       → pre-filled form (existing record)
    POST /dashboard/create/          → save new record
    POST /dashboard/edit/<pk>/       → update existing record
    """
    prospect = None
    if pk:
        prospect = get_object_or_404(Prospect, pk=pk)

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        full_name = request.POST.get('full_name', '').strip() or None
        phone_number = request.POST.get('phone_number', '').strip() or None
        location = request.POST.get('location', '').strip() or None
        occupation = request.POST.get('occupation', '').strip() or None
        highest_degree = request.POST.get('highest_degree', '').strip() or None
        program = request.POST.get('program', '').strip() or None
        how_heard = request.POST.get('how_heard', '').strip() or None

        if not email:
            messages.error(request, 'Email is required.')
            return render(request, 'prospects/prospect_form.html', {
                'prospect': prospect,
                'how_heard_choices': Prospect.HOW_HEARD_CHOICES,
                'page_title': 'Edit Prospect' if prospect else 'Create Prospect',
            })

        # Check uniqueness (excluding current record on update)
        qs = Prospect.objects.filter(email=email)
        if prospect:
            qs = qs.exclude(pk=prospect.pk)
        if qs.exists():
            messages.error(request, f'A prospect with email "{email}" already exists.')
            return render(request, 'prospects/prospect_form.html', {
                'prospect': prospect,
                'how_heard_choices': Prospect.HOW_HEARD_CHOICES,
                'page_title': 'Edit Prospect' if prospect else 'Create Prospect',
            })

        if prospect:
            # UPDATE
            prospect.email = email
            prospect.full_name = full_name
            prospect.phone_number = phone_number
            prospect.location = location
            prospect.occupation = occupation
            prospect.highest_degree = highest_degree
            prospect.program = program
            prospect.how_heard = how_heard
            prospect.save()
            messages.success(request, f'Prospect "{email}" updated successfully.')
        else:
            # CREATE
            Prospect.objects.create(
                email=email,
                full_name=full_name,
                phone_number=phone_number,
                location=location,
                occupation=occupation,
                highest_degree=highest_degree,
                program=program,
                how_heard=how_heard,
            )
            messages.success(request, f'Prospect "{email}" created successfully.')

        return redirect('prospects:dashboard')

    return render(request, 'prospects/prospect_form.html', {
        'prospect': prospect,
        'how_heard_choices': Prospect.HOW_HEARD_CHOICES,
        'page_title': 'Edit Prospect' if prospect else 'Create Prospect',
    })


def prospect_delete(request, pk):
    """
    Safe POST-only record deletion.
    POST /dashboard/delete/<pk>/
    """
    if request.method == 'POST':
        prospect = get_object_or_404(Prospect, pk=pk)
        email = prospect.email
        prospect.delete()
        messages.success(request, f'Prospect "{email}" deleted successfully.')
    return redirect('prospects:dashboard')
