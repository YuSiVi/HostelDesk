from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Avg, Q

from .models import Complaint, Remark
from .form import ComplaintForm, RemarkForm, SatisfactionForm


def home(request):
    complaints = Complaint.objects.all().order_by('-date_filed')

    # --- Filtering ---
    status_filter = request.GET.get('status', '')
    category_filter = request.GET.get('category', '')
    search_query = request.GET.get('q', '')

    if status_filter:
        complaints = complaints.filter(status=status_filter)
    if category_filter:
        complaints = complaints.filter(category=category_filter)
    if search_query:
        complaints = complaints.filter(
            Q(student_name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(room_number__icontains=search_query)
        )

    # --- Dashboard Stats ---
    all_complaints = Complaint.objects.all()
    total = all_complaints.count()
    pending = all_complaints.filter(status='pending').count()
    in_progress = all_complaints.filter(status='inprogress').count()
    resolved = all_complaints.filter(status='resolved').count()
    resolved_pct = round((resolved / total) * 100) if total > 0 else 0
    avg_satisfaction = all_complaints.filter(
        satisfaction__isnull=False
    ).aggregate(avg=Avg('satisfaction'))['avg']
    avg_satisfaction = round(avg_satisfaction, 1) if avg_satisfaction else None
    overdue_count = sum(1 for c in all_complaints if c.is_overdue)

    # Get upvoted complaint IDs from session
    upvoted_ids = request.session.get('upvoted_complaints', [])

    context = {
        'complaints': complaints,
        'total': total,
        'pending': pending,
        'in_progress': in_progress,
        'resolved': resolved,
        'resolved_pct': resolved_pct,
        'avg_satisfaction': avg_satisfaction,
        'overdue_count': overdue_count,
        'upvoted_ids': upvoted_ids,
        # Pass current filters back to template
        'current_status': status_filter,
        'current_category': category_filter,
        'current_search': search_query,
        'status_choices': Complaint.STATUS_CHOICES,
        'category_choices': Complaint.CATEGORY_CHOICES,
    }
    return render(request, 'home.html', context)


def submit(request):
    form = ComplaintForm()
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'submit.html', {'form': form})


def edit_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    form = ComplaintForm(instance=complaint)
    if request.method == 'POST':
        form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'edit.html', {'form': form, 'complaint': complaint})


def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    remarks = complaint.remarks.all()
    remark_form = RemarkForm()
    satisfaction_form = SatisfactionForm()
    upvoted_ids = request.session.get('upvoted_complaints', [])

    context = {
        'complaint': complaint,
        'remarks': remarks,
        'remark_form': remark_form,
        'satisfaction_form': satisfaction_form,
        'already_upvoted': complaint.id in upvoted_ids,
    }
    return render(request, 'detail.html', context)


def add_remark(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        form = RemarkForm(request.POST)
        if form.is_valid():
            remark = form.save(commit=False)
            remark.complaint = complaint
            remark.save()
    return redirect('complaint_detail', pk=pk)


def upvote_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        # Check if already upvoted in this session
        upvoted = request.session.get('upvoted_complaints', [])
        if complaint.id not in upvoted:
            complaint.upvotes += 1
            complaint.save()
            upvoted.append(complaint.id)
            request.session['upvoted_complaints'] = upvoted
    return redirect('complaint_detail', pk=pk)


def rate_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST' and complaint.status == 'resolved':
        try:
            score = int(request.POST.get('satisfaction', 0))
            if 1 <= score <= 5:
                complaint.satisfaction = score
                complaint.save()
        except (ValueError, TypeError):
            pass
    return redirect('complaint_detail', pk=pk)


def update_status(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Complaint.STATUS_CHOICES):
            complaint.status = new_status
            # Auto-set resolved_date when marking as resolved
            if new_status == 'resolved' and not complaint.resolved_date:
                complaint.resolved_date = timezone.now()
            # Clear resolved_date if un-resolving
            elif new_status != 'resolved':
                complaint.resolved_date = None
            complaint.save()
    return redirect('home')


def delete_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        complaint.delete()
    return redirect('home')
