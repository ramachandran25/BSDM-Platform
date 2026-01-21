from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import ProjectRequest, RequestAttachment
from .forms import ProjectRequestForm


@login_required
def dashboard(request):
    return render(request, 'requests/dashboard.html')


@login_required
def create_request(request):
    if request.method == 'POST':
        form = ProjectRequestForm(request.POST)
        if form.is_valid():
            project_request = form.save(commit=False)
            project_request.user = request.user
            project_request.save()

            # Save multiple user attachments
            files = request.FILES.getlist('attachments')
            for f in files:
                RequestAttachment.objects.create(
                    project_request=project_request,
                    file=f,
                    uploaded_by='USER'
                )

            messages.success(
                request,
                f"Request submitted successfully. Request Number: {project_request.request_id}"
            )
            return redirect('my_requests')
    else:
        form = ProjectRequestForm()

    return render(
        request,
        'requests/create_request.html',
        {'form': form}
    )

@login_required
def my_requests(request):
    requests = ProjectRequest.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'requests/my_requests.html',
        {'requests': requests}
    )


@login_required
def request_detail(request, request_id):
    req = get_object_or_404(
        ProjectRequest,
        request_id=request_id,
        user=request.user
    )

    if request.method == 'POST':
        if req.status == 'CLOSED':
            messages.error(
                request,
                'This request is closed. You cannot upload more files.'
            )
            return redirect('request_detail', request_id=request_id)

        files = request.FILES.getlist('attachments')
        for f in files:
            RequestAttachment.objects.create(
                project_request=req,
                file=f,
                uploaded_by='USER'
            )

        messages.success(request, 'Files uploaded successfully.')
        return redirect('request_detail', request_id=request_id)

    return render(
        request,
        'requests/request_detail.html',
        {'request': req}
    )
