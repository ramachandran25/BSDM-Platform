from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .decorators import is_project_admin
from requests_app.models import ProjectRequest, RequestAttachment
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(is_project_admin)
def admin_dashboard(request):
    requests = ProjectRequest.objects.all().order_by('-created_at')
    return render(request, 'project_admin/dashboard.html', {'requests': requests})


@login_required
@user_passes_test(is_project_admin)
def admin_request_detail(request, request_id):
    req = get_object_or_404(ProjectRequest, request_id=request_id)

    if request.method == 'POST':
        # Update status
        req.status = request.POST.get('status', req.status)

        # Update estimated cost
        cost = request.POST.get('estimated_cost')
        if cost:
            req.estimated_cost = cost

        req.save()

        # Save admin attachments
        files = request.FILES.getlist('admin_attachments')
        for f in files:
            RequestAttachment.objects.create(
                project_request=req,
                file=f,
                uploaded_by='ADMIN'
            )

        messages.success(request, 'Request updated successfully')
        return redirect('project_admin_request_detail', request_id=req.request_id)

    return render(
        request,
        'project_admin/request_detail.html',
        {'request': req}
    )
